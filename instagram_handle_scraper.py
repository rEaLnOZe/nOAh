#!/usr/bin/env python3
"""
Instagram-Handle-Scraper (einmalig lauffaehig).

Liest eine CSV mit einer Domain-Spalte ein, sucht pro Domain den
Instagram-Handle und schreibt das Ergebnis in eine neue CSV.

Fetch-Strategie:
  1. httpx mit Browser-User-Agent (schnell).
  2. Falls kein instagram.com-Link im HTML gefunden wird -> Fallback auf
     Playwright/Chromium (JS-Render), es wird die ganze Seite gescannt.

Regeln:
  - Bestehende Zeilen/Spalten bleiben erhalten, es wird nur die
    Instagram-Spalte gefuellt und es werden Ergebnis-Spalten ergaenzt.
  - Fehler werden pro Zeile abgefangen; ein einzelner Fehler killt nie
    den ganzen Lauf.
  - Kein Fund wird sauber als "none" markiert (nicht geraten).

Aufruf:
    python3 instagram_handle_scraper.py INPUT.csv [-o OUTPUT.csv]

Abhaengigkeiten:
    pip install httpx playwright
    python -m playwright install chromium   # nur wenn Chromium fehlt
"""

from __future__ import annotations

import argparse
import csv
import glob
import os
import re
import sys
import time
from pathlib import Path

import httpx

# Playwright wird erst im Fallback importiert, damit das Skript auch dann
# grundsaetzlich laeuft, wenn Playwright (noch) nicht installiert ist.

# --------------------------------------------------------------------------
# Konfiguration
# --------------------------------------------------------------------------

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

HTTPX_TIMEOUT = 20.0        # Sekunden pro httpx-Request
PLAYWRIGHT_TIMEOUT = 30000  # Millisekunden pro Playwright-Navigation
REQUEST_PAUSE = 0.5         # kleine Pause zwischen Domains (hoeflich)

# Instagram-Pfade, die keine Handles sind und rausgefiltert werden.
RESERVED_SLUGS = {"p", "reel", "reels", "explore", "tv", "stories"}

# instagram.com/<slug> -- Slug erlaubt Buchstaben, Ziffern, _ und .
IG_LINK_RE = re.compile(
    r"instagram\.com/([A-Za-z0-9_.]+)", re.IGNORECASE
)

# Moegliche Namen fuer die Domain-Spalte (case-insensitive, Teilstring).
DOMAIN_COL_CANDIDATES = ["domain", "website", "url"]
# Moegliche Namen fuer die (zu fuellende) Instagram-Spalte.
INSTAGRAM_COL_CANDIDATES = ["instagram"]

# Neue Ergebnis-Spalten. Der Name der Status-Spalte wird zur Laufzeit
# aufgeloest (siehe resolve_status_col), damit eine bereits vorhandene
# "Status"-Spalte nicht ueberschrieben wird.
OUT_HANDLE_COL = "Instagram_Handle"
OUT_URL_COL = "IG_URL"
OUT_SOURCE_COL = "Quelle"
OUT_STATUS_COL_DEFAULT = "Status"
OUT_STATUS_COL_FALLBACK = "Scrape_Status"


# --------------------------------------------------------------------------
# Parsing-Helfer
# --------------------------------------------------------------------------

def extract_handle(html: str) -> str | None:
    """Ersten validen Instagram-Slug aus HTML extrahieren, sonst None."""
    if not html:
        return None
    for match in IG_LINK_RE.finditer(html):
        slug = match.group(1).strip().strip(".")
        if not slug:
            continue
        if slug.lower() in RESERVED_SLUGS:
            continue
        return slug
    return None


def normalize_domain(raw: str) -> str:
    """Domain-Zelle in eine aufrufbare URL umwandeln."""
    d = (raw or "").strip()
    d = d.replace("http://", "").replace("https://", "").strip("/")
    return d


# --------------------------------------------------------------------------
# Fetch-Layer
# --------------------------------------------------------------------------

def fetch_httpx(url: str) -> str | None:
    """HTML per httpx holen. Gibt HTML oder None (bei Fehler) zurueck."""
    headers = {
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    }
    try:
        with httpx.Client(
            headers=headers,
            timeout=HTTPX_TIMEOUT,
            follow_redirects=True,
            verify=True,
        ) as client:
            resp = client.get(url)
            if resp.status_code >= 400:
                return None
            return resp.text
    except Exception as exc:  # noqa: BLE001 - bewusst breit, pro Zeile abfangen
        print(f"    [httpx] Fehler: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None


def fetch_playwright(url: str) -> str | None:
    """HTML per Playwright/Chromium (JS-gerendert) holen, sonst None."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # noqa: BLE001
        print(f"    [playwright] nicht verfuegbar: {exc}", file=sys.stderr)
        return None

    def _launch(pw):
        """Chromium starten; bei Versions-Mismatch auf ein vorinstalliertes
        Binary unter PLAYWRIGHT_BROWSERS_PATH ausweichen."""
        try:
            return pw.chromium.launch(headless=True)
        except Exception:  # noqa: BLE001
            base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
            for pat in (
                os.path.join(base, "chromium-*", "chrome-linux", "chrome"),
                os.path.join(base, "chromium-*", "chrome-linux64", "chrome"),
            ):
                for exe in sorted(glob.glob(pat)):
                    if os.path.exists(exe):
                        return pw.chromium.launch(headless=True, executable_path=exe)
            raise

    try:
        with sync_playwright() as pw:
            browser = _launch(pw)
            try:
                context = browser.new_context(user_agent=BROWSER_UA)
                page = context.new_page()
                page.goto(url, timeout=PLAYWRIGHT_TIMEOUT, wait_until="domcontentloaded")
                # Footer-Links sind oft erst nach dem Scrollen im DOM.
                try:
                    page.mouse.wheel(0, 20000)
                    page.wait_for_timeout(1500)
                except Exception:  # noqa: BLE001
                    pass
                return page.content()
            finally:
                browser.close()
    except Exception as exc:  # noqa: BLE001
        print(f"    [playwright] Fehler: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None


def find_handle_for_domain(domain: str) -> tuple[str | None, str]:
    """
    Liefert (handle, quelle). quelle in {"httpx", "playwright", "none"}.
    handle ist None, wenn nichts gefunden wurde.
    """
    dom = normalize_domain(domain)
    if not dom:
        return None, "none"

    for scheme in ("https://", "http://"):
        url = scheme + dom

        # 1) httpx
        html = fetch_httpx(url)
        handle = extract_handle(html) if html else None
        if handle:
            return handle, "httpx"

        # 2) Playwright-Fallback nur, wenn httpx ueberhaupt HTML lieferte
        #    ODER die Seite evtl. JS-gerendert ist. Wir versuchen es in
        #    jedem Fall einmal pro Scheme.
        html_pw = fetch_playwright(url)
        handle = extract_handle(html_pw) if html_pw else None
        if handle:
            return handle, "playwright"

        # Wenn httpx erfolgreich HTML lieferte (Seite erreichbar), kein
        # zweites Scheme mehr probieren.
        if html:
            break

    return None, "none"


# --------------------------------------------------------------------------
# CSV-Handling
# --------------------------------------------------------------------------

def detect_column(fieldnames: list[str], candidates: list[str]) -> str | None:
    for col in fieldnames:
        low = col.lower()
        if any(cand in low for cand in candidates):
            return col
    return None


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if not fieldnames:
        print("FEHLER: keine Kopfzeile in der CSV gefunden.", file=sys.stderr)
        sys.exit(1)

    domain_col = detect_column(fieldnames, DOMAIN_COL_CANDIDATES)
    instagram_col = detect_column(fieldnames, INSTAGRAM_COL_CANDIDATES)

    if not domain_col:
        print(
            f"FEHLER: keine Domain-Spalte gefunden. Spalten: {fieldnames}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Domain-Spalte:    {domain_col!r}")
    print(f"Instagram-Spalte: {instagram_col!r}")
    print(f"Zeilen:           {len(rows)}")
    print("-" * 60)

    # Status-Spaltenname aufloesen: nur wenn "Status" noch nicht existiert,
    # wird sie verwendet -- sonst "Scrape_Status", um vorhandene Daten
    # (z.B. "zu verifizieren") nicht zu ueberschreiben.
    status_col = (
        OUT_STATUS_COL_DEFAULT
        if OUT_STATUS_COL_DEFAULT not in fieldnames
        else OUT_STATUS_COL_FALLBACK
    )
    print(f"Status-Spalte:    {status_col!r}")

    # Ausgabespalten: alle Originalspalten + neue Spalten (falls noch nicht da).
    out_fieldnames = list(fieldnames)
    for col in (OUT_HANDLE_COL, OUT_URL_COL, OUT_SOURCE_COL, status_col):
        if col not in out_fieldnames:
            out_fieldnames.append(col)

    found = 0
    total = len(rows)

    for i, row in enumerate(rows, start=1):
        domain = (row.get(domain_col) or "").strip()
        brand = row.get("Brand") or row.get(fieldnames[0]) or ""
        print(f"[{i}/{total}] {brand} -> {domain}")

        try:
            handle, quelle = find_handle_for_domain(domain)
        except Exception as exc:  # noqa: BLE001 - Sicherheitsnetz pro Zeile
            print(f"    unerwarteter Fehler: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            handle, quelle = None, "none"

        if handle:
            ig_url = f"https://www.instagram.com/{handle}/"
            status = "gefunden"
            found += 1
            print(f"    OK ({quelle}): {handle}")
            if instagram_col:
                row[instagram_col] = handle
        else:
            ig_url = ""
            status = "none"
            quelle = "none"
            print("    kein Handle gefunden -> none")

        row[OUT_HANDLE_COL] = handle or "none"
        row[OUT_URL_COL] = ig_url
        row[OUT_SOURCE_COL] = quelle
        row[status_col] = status

        time.sleep(REQUEST_PAUSE)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("-" * 60)
    print(f"Report: {found} von {total} gefunden")
    print(f"Ausgabe geschrieben: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Instagram-Handle-Scraper")
    parser.add_argument("input", help="Pfad zur Input-CSV")
    parser.add_argument(
        "-o", "--output", help="Pfad zur Output-CSV (Standard: <input>_out.csv)"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"FEHLER: Datei nicht gefunden: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(input_path.stem + "_out.csv")

    run(input_path, output_path)


if __name__ == "__main__":
    main()
