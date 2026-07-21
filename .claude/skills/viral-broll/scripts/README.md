# ffmpeg + libass render path (no-browser fallback)

The primary render path for viral-broll cards is HyperFrames (HTML/GSAP → video).
But HyperFrames and Remotion both need a headless browser, whose download is
**blocked in locked-down sandboxes** (403 on the browser/model host). This
directory captures a fully self-contained fallback that renders the whole edit —
captions, a text-centered card, zoom punches, brand bug — with **only ffmpeg +
libass**, no browser, no network. It's how CB1 was actually cut in that
environment.

## What's here

- `example_cb1_build_edit.py` — a working reference generator (CB1, 0–19s). It
  emits an `.ass` subtitle file carrying TWO layers:
  - **word-punch captions** — ≤3 words/cue, pop-in (`\fscx` + `\t`), white with
    the accent (`#FF7A00` → ASS BGR `&H007AFF&`) on emphasis words, font
    auto-shrunk to the frame width (`fit_fs`) so wide lines never overflow.
  - **a text-centered card** — a full-frame off-white panel (`\p` drawing), a
    faint watermark word, an accent eyebrow with `◆` diamonds, and the hero lines
    revealed one-by-one — the object/text archetype rendered entirely in ASS.
  - a subtle brand bug.
- `example_cb1_edit.ass` — the generated output, as a concrete ASS reference.

Copy the generator and edit the `SEG` list (captions) + the CARD block for a new
video. It's a template, not a library — adapt per edit.

## Render command (the shape that works)

```bash
# zoom punches: hook-open ease + gaussian push-ins, CENTERED so no pan wobble
Z="1+0.12*(0.5+0.5*cos(PI*min(on/30\,1)))+0.07*exp(-pow((on/30-3.3)/0.45\,2))+0.09*exp(-pow((on/30-17.2)/0.5\,2))"
ffmpeg -y -i INPUT.mp4 \
  -vf "fps=30,zoompan=z='${Z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,subtitles=edit.ass:fontsdir=/usr/share/fonts" \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart \
  OUTPUT.mp4
```

Key correctness notes learned the hard way:
- **`subtitles` runs AFTER `zoompan`** so burned text is never magnified/cropped.
- **zoompan x/y kept exactly centered** (`iw/2-(iw/zoom/2)`) — the integer-pan
  wobble that makes zoompan look cheap only happens when you pan; pure centered
  zoom is smooth.
- **Shrink captions to total line width, not just longest word** — a 3-word line
  of short words still overflows at full size (`fit_fs` handles both).
- ASS colours are `&HBBGGRR` — orange `#FF7A00` = `&H007AFF&`.
- Match `PlayResX/Y` to the video (1080×1920) so `\pos` maps 1:1.

## When to prefer this vs HyperFrames

Use HyperFrames when a browser render is available — it gives real GSAP motion,
gradients, blur, and the full card fidelity. Use this ffmpeg path when the browser
is unavailable (sandbox) or for a fast, dependency-light caption+card pass. The
card here is a clean, honest approximation of the archetype look, not a
pixel-match of the HTML templates.
