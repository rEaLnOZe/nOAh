# Style DNA — the shared system

Everything in this file is what makes a card read as *this* viral style rather
than generic motion graphics. The archetypes differ in *what the hero is*; this
file is what they all share. Author every card against it.

## Canvas

- **9:16, 1080×1920.** This is a phone-first, vertical style.
- Safe zone: keep the hero and key text inside the middle ~80% vertically — the
  top ~8% and bottom ~15% are platform UI / caption strips.

## Background — never flat white

The base is white/off-white **with depth baked in**. Flat `#FFFFFF` is the #1 tell
of an amateur version.

- Base fill: `#F6F5F3`–`#FFFFFF`.
- **Soft shade:** a large, feathered dark vignette in one or two corners (in CapCut
  this is the "white to −40 + film-strip mask, feather 75" move). In CSS: a big
  `radial-gradient` of `rgba(0,0,0,0.10)` bleeding from a corner, heavily blurred.
- **Light overlay:** a faint diagonal light streak (`rgba(255,255,255,0.6)` soft
  linear gradient) crossing the frame — gives the paper a sheen.
- Optional texture: a **halftone dot pattern** or a faint **grid** at ~8–12%
  opacity in the margins (character cards especially). Keep it barely-there.

## Color — one accent, everything else grayscale

- **Accent:** exactly one per card. Default brand orange `#FF7A00` (dark stop
  `#FF3B00`); override to a topic-owned color when the subject has one (see the
  accent rule in SKILL.md). Use it on: bullet diamonds, ONE emphasized word, the
  card border/shadow glow, a single shape. Never more than ~3 elements.
- **Everything else is grayscale:** text and objects in near-black `#141414` /
  dark gray `#333`; watermark + decorative text in light gray `#B8B8B8`; shapes in
  `#2A2A2A`–`#3A3A3A` dark gray. Photos of objects/people keep their natural color
  but are pulled toward the frame (see grade below).
- Reference-frame accents for calibration: object→blue `#2563EB`, character→
  WhatsApp green `#25D366`, text→urgency red `#E0402E`.

## Typography

- **Hero display:** a heavy, slightly condensed sans, bold/black weight (SF Pro
  Display Bold, Anton, Archivo Black, or similar). Big — the hero word/phrase
  dominates. One word may be *italic + accent* for emphasis.
- **Watermark word (background):** the topic in a huge heavy font at **12–20%
  opacity**, oversized so it bleeds off the card edges, sitting *behind* the hero.
  This is the "magazine cover" backbone of every card.
- **Decorative micro-text:** tiny (5–8px equivalent) thin-weight lines of filler
  text in light gray, placed like magazine body copy for detail. Real or lorem —
  it's texture, not content.
- **Supporting labels:** small bold caps or a name/title, dark gray, tucked near
  the hero.

## Depth & shadow — the premium trick

Two moves do most of the "expensive 3D" work:

1. **Grounding shadow (do this on every hero):** duplicate the hero, crush it to
   solid black (curves all the way down), blur it heavily (~80–100px), drop opacity
   to **~50–60%**, and offset it *behind and slightly below* the hero. This is the
   single highest-yield technique in the style.
2. **Card stack:** put the hero inside a rounded-rect card (radius 24–40px) and
   place 1–2 duplicate rects behind it, offset a few px in the accent color — the
   "stacked cards" look with a colored drop shadow. Optional accent hairline border.

Finishing depth: a subtle **wide-angle / lens** feel (slight barrel + vignette) and
a light **chromatic aberration** (1–2px RGB split) applied to the whole card for a
tactile, tuned-not-seen finish. Keep both subtle — if you can point at "the effect,"
it's too strong.

## Motion — smooth, eased, performs then rests

The signature is smoothness. **Everything eases; nothing is linear; nothing
bounces or idle-wobbles.** Default easing = **cubic ease-out** (CapCut's "cubic
ease"), quad for gentler moves.

Entrance choreography (per card, ~3–5s on screen):

1. **Card in:** a fast **blur burn-off** — start blurred (~20px) + slightly small,
   resolve to sharp over ~0.2–0.3s (defocus→focus). No scale-bounce.
2. **Hero zoom:** the hero scales in (e.g. `50→100`, or a push `100→130`) over
   ~0.8–1.2s with cubic ease-out. Character heroes: a zoom-in that settles the
   subject into its box.
3. **Supporting reveals, staggered:** shapes slide in (slide-right / -up), the
   pen-curve line wipes in via a moving mask, the emphasized word pops (type-on),
   the dash/tick marks type in. Stagger by ~4–15 frames; heavier elements later.
4. **Settle:** one final **compound zoom** on the whole card — scale to ~120–130
   with a slight rotation (~8–10°), cubic-eased — so the card is gently moving as it
   holds, never a frozen frame. Optionally a blur-out on exit.

Rhythm: **1 hero move + 2–3 supporting reveals, then stop.** Minimal is the point.

## Texture elements (pick 1–2, not all)

- **Pen-curve line:** a thin light-gray hand-drawn curve for organic texture, often
  masked to wipe on. One per card max.
- **Dashes / tick marks:** a short row of `—` marks in dark gray that type in.
- **Scatter props:** for object cards, 2 small related props tucked into opposite
  corners, partly cropped by the card edge (e.g. two alarm clocks around the
  hourglass).
- **Caution/brand ribbon:** a diagonal repeated-text tape ("KEEP OUT", or the brand
  name) for urgency/brand beats.

## Calibration checklist

Before rendering, a card should pass all of these — they're the difference between
"looks like the reference" and "looks AI-generated":

- [ ] Exactly one accent color, on ≤3 elements; rest grayscale.
- [ ] Background is shaded/lit, not flat white.
- [ ] Hero is centered and clearly the single subject.
- [ ] Hero has the black-blur grounding shadow.
- [ ] A big low-opacity watermark word sits behind the hero.
- [ ] 1–2 texture elements, not a cluttered pile.
- [ ] Every motion is eased; there's a final settling zoom; nothing idle-wobbles.
- [ ] It would sit convincingly next to `assets/reference-frames/`.
