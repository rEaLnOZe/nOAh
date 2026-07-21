# B-roll detection — reading a transcript for cards

Goal: given a word-level transcript (with timings), decide **where** cutaway cards
go, **which archetype** each is, and **what accent**. The output is a small plan of
beats — deliberately sparse. Empty space with just the speaker is fine; a wrong or
constant card is worse than none.

## The gate: every card must mean something specific

Before adding a card, state in one sentence WHY it appears at this exact moment and
what the viewer should understand. If the answer is "general vibes" or "they're
talking about business" — don't add it. This `reason` is mandatory.

## Scan for trigger types

Walk the transcript. At each beat, ask what kind of thing the speaker is on:

- **Concrete object / prop / metaphor** ("an hourglass", "a funnel", "a lock", "a
  trophy", a named product you can picture) → **object-centered**.
- **Person or brand with a face/logo** ("Zuckerberg", "the CEO", "WhatsApp",
  "OpenAI", "our founder Sarah") → **character-based**.
- **Claim / hook / thesis / one-liner** with no single object or person to show
  ("hesitation steals your opportunities", "most people quit here", a stat phrased
  as a sentence) → **text-centered**.
- **Enumeration** ("three types…", "first / second / third") → a text-centered card
  per item, or one card that reveals the list — still minimal.

If two apply, pick what the *sentence is about* (see archetypes tie-breakers).

## Hook detection

The **hook** is the first strong claim in the first ~3 seconds — the line that makes
someone stop scrolling. It almost always gets a **text-centered** hero card (the
phrase IS the hook), landed right as the claim is spoken. The **CTA / closer**
(last line, "go try it", "follow for more") also gets a text-centered card.

Signals for the hook line: a bold absolute ("this is blowing up", "nobody tells
you"), a promise ("by the end you'll…"), a provocative claim, or a number/stat. Mark
one — don't turn every early sentence into a card.

## Placement & density rules (borrowed from the main edit doctrine)

- **~1 card per 4–8s.** Above that it feels frantic; the speaker carries the show.
- **First card lands 1.5–3.5s in** — not before 1.5s (let the viewer lock onto the
  speaker first), not after ~5s (cold open goes flat).
- **Never two cards back-to-back.** Leave ≥1.5s of just-the-speaker between any two
  cards so each lands as its own beat, not a slideshow.
- **Each card ≤5s on screen.** Beyond that it's a static frame; the speaker returns.
- **Snap to speech.** Start a card ~0.1s before its trigger word; end after the
  point is made. Align to real word boundaries from the transcript.

## Accent per card

Follow SKILL.md's accent rule: topic-owned color if the subject has one (WhatsApp
green, red for danger/urgency, gold for money/win), else the brand default
`#FF7A00`. One accent per card.

## Output shape

Emit a compact beat plan — one row per card. Example:

```json
[
  { "start_s": 2.1, "end_s": 5.4, "archetype": "text-centered",
    "hero_text": "this style is BLOWING UP", "accent": "#FF7A00",
    "reason": "hook — the opening claim that earns the scroll-stop" },
  { "start_s": 41.0, "end_s": 45.2, "archetype": "object-centered",
    "hero": "hourglass", "watermark": "SAVE TIME", "accent": "#2563EB",
    "reason": "speaker says a single object stays at the center — show the object" },
  { "start_s": 48.0, "end_s": 52.0, "archetype": "character-based",
    "hero": "Mark Zuckerberg", "brand": "WhatsApp", "accent": "#25D366",
    "reason": "speaker names the person a card is built around" }
]
```

Keep it short. A 30–60s short is typically 4–8 cards total.

## When transcription isn't available

If you can't get a word-level transcript in the current environment (e.g. ASR is
network-blocked), you have three fallbacks, best first:
1. Use a **canonical script** the user provides (paste / file) — better than ASR
   anyway, it states brand names exactly.
2. Use a **transcript the user pastes** and estimate timings from speech pacing.
3. Ask the user to mark the 4–8 beats they want cards on. A few good human-chosen
   beats beat a wall of auto-detected ones.
