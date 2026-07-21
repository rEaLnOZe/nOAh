# Rendering & compositing

The cards are HyperFrames compositions — HTML + CSS + a single seek-safe GSAP
timeline — rendered to video by the HyperFrames toolchain. This keeps them
deterministic and generatable, which is the whole point of rebuilding the CapCut
look programmatically.

## Author to the HyperFrames contract

Before writing composition HTML, load the **`hyperframes-core`** skill for the exact
composition contract (the `data-*` timing attributes, `class="clip"`, the single
paused master timeline, deterministic-render rules) and **`hyperframes-animation`**
for the GSAP eases and scene choreography. The templates in `assets/templates/` are
style-correct starting points; align their timeline wiring to whatever
`hyperframes-core` specifies in this version before rendering.

The style rules in `style-dna.md` are framework-agnostic — the CSS (shaded bg,
grounding shadow, watermark, one-accent) ports directly; only the timeline wiring is
HyperFrames-specific.

## Render

Use the **`hyperframes-cli`** skill for the dev loop (`init`, `add`, `check`,
`preview`, `render`, and `transcribe` / `remove-background` for assets). Typical:

- **Preview** while iterating (fast, low-res) — check timing and the look.
- **Render MP4** for a full-frame cutaway card (opaque, on the shaded background).
- **Render transparent overlay** (WebM/alpha) when the card should sit *over* the
  speaker instead of replacing them — e.g. a short text hit in the lower third.

Environment note: HyperFrames renders through a headless browser. In a locked-down
container the default browser download can be blocked — if so, point it at the
preinstalled Chromium in new-headless mode (the same fix used for Remotion:
`--chrome-mode=chrome-for-testing --browser-executable=/opt/pw-browsers/chromium`,
or the equivalent HyperFrames flag). Verify with a one-frame render before a batch.

## Compose onto the edit

- **Full-frame cutaway:** drop the MP4 in at the beat's `start_s…end_s`, replacing
  the speaker. Best for object/character heroes that deserve the whole frame.
- **Overlay:** composite the transparent card over the speaker (lower/mid frame),
  keeping the speaker visible. Best for short text hits.
- Respect the density rules in `detection.md` (≤5s each, ≥1.5s speaker gap between
  cards, snap to speech). Add captions with a captions skill and the speaker
  footage / zooms / audio with the main edit skill — this skill owns only the
  cutaway layer.

## Accent wiring

Every template exposes `--accent` (and `--accent-dark`) as CSS variables. Set them
per card from the beat plan (`detection.md`). Default `#FF7A00` / `#FF3B00` (brand),
override to the topic color when the subject owns one.
