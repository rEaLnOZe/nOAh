---
name: viral-broll
description: >-
  Generate "clean viral" short-form B-roll animation cards — the white-background,
  minimal-shape, one-accent-color, kinetic style that blows up on Reels/TikTok/Shorts
  (the "CapCut clean" look), rendered programmatically as HyperFrames HTML/CSS/GSAP
  compositions (→ MP4 or transparent overlay), NOT by clicking CapCut. Use this
  whenever a short needs designed B-roll / cutaway cards, an animated hook or
  stat/claim card, a "make me B-roll", "add cutaways", "clean animated cards",
  "object/character/text card", or when running B-roll detection over a transcript
  to decide WHERE cutaways go and WHICH card type fits each beat. Covers the three
  archetypes (object-centered, character-based, text-centered), the shared style
  system, and the transcript triggers that pick them. Reach for this for the
  cutaway/animation layer specifically; pair it with a captions skill for subtitles
  and with the main edit skill for speaker footage, zooms, and audio.
---

# Viral B-roll — clean short-form cutaway cards

This skill produces the **cutaway/B-roll layer** of a short: designed, animated
cards that sit between or over the speaker to visualize what's being said. The
look is the one that "has its own identity — clean design, minimal graphics,
simple shapes, smooth animations." It reads as expensive but is built from a few
repeatable parts.

It is **not** a CapCut macro. CapCut is a GUI we can't drive. Instead we rebuild
the *look* as HyperFrames compositions (HTML + CSS + a single seek-safe GSAP
timeline), which renders deterministically to MP4 or a transparent WebM overlay —
so the same style is generatable from a transcript, every time, no manual clicking.

## The one idea that makes it work

Every card is **one hero, centered, with everything else in a supporting role.**
Pick the hero first, commit the whole frame to it, keep the rest quiet. The three
archetypes are just *what the hero is*:

| Archetype | Hero is… | Trigger in the script | Accent example |
|---|---|---|---|
| **object-centered** | a single object / prop / metaphor | speaker names a concrete thing ("an hourglass", "the funnel", "a lock") | blue |
| **character-based** | a person or brand figure | speaker names a person or company with a face/logo ("Zuckerberg", "WhatsApp") | brand green |
| **text-centered** | a punchy phrase itself | speaker lands a claim / hook / one-liner | red |

Read `references/archetypes.md` for the full layout + motion recipe of each, and
look at `assets/reference-frames/` — three real frames of the exact target look
(one per archetype). Those frames are the ground truth; when in doubt, match them.

## Workflow

1. **Decide the beats.** Run `references/detection.md` over the transcript to find
   WHERE cards go and WHICH archetype each is. Don't carpet-bomb — ~1 card per
   4–8s, and always leave the speaker visible between two cards (no card-on-card).
2. **Pick the hero + accent per card.** One hero, one accent color for that card
   (see the accent rule below). Everything non-accent is grayscale.
3. **Author the composition.** Copy the matching template from `assets/templates/`,
   fill in the hero, watermark word, 1–3 supporting bits, and `--accent`. Keep the
   style contract in `references/style-dna.md` — that file is what makes it read as
   *this* style rather than generic motion graphics.
4. **Render** via HyperFrames (`hyperframes` CLI → MP4, or transparent overlay to
   composite over speaker footage). See `references/rendering.md`.
5. **Compose** the card onto the edit at its beat. As a cutaway it can be a
   full-frame takeover; as an overlay it sits over the speaker. Prefer full-frame
   for object/character heroes, overlay for a short text hit.

## Accent color rule

The whole style hangs on **one accent per card, used sparingly** (a bullet
diamond, one emphasized word, the card's shadow/border glow) against an otherwise
grayscale frame. Two rules for picking it:

- **If the topic owns a color, use it** — WhatsApp green, a red "danger/urgency"
  beat, a gold "money/win" beat. This is what sells the card as *about that thing*.
- **Otherwise default to the brand accent.** For CreatrLabs / InfluMatch that is
  **`#FF7A00` (brand orange)**, with `#FF3B00` as the darker gradient stop — the
  same palette as the `video-edit` skill, so a video's cutaways match its captions
  and overlays. Never introduce a random purple/gradient — that breaks the identity.

## Hard rules (what keeps it clean)

These are the failure modes that make the style collapse into "generic AI motion."

1. **One accent, everything else grayscale.** Color is a scalpel, not a bucket.
   A second accent color, or accent on more than ~3 elements, and it reads cheap.
2. **The hero is the show; supporting elements stay quiet and few.** 1 hero move +
   2–3 supporting reveals per card, no more. "For this style it's more minimal, so
   don't overdo it."
3. **Every motion is eased (cubic/quad), never linear, never a bounce/wobble.** The
   signature is *smooth*: zoom-in on the hero, staggered reveals, one settling
   compound zoom at the end. Idle wobble is banned — motion performs, then rests.
4. **White/off-white background with a soft shadow — never flat pure white.** The
   soft radial shade + light overlay is what gives the frame depth. See style-dna.
5. **Ground every hero with the black-blur shadow** (duplicate → crush to black →
   heavy blur → ~50–60% opacity, offset behind). This one trick is 80% of the
   "3D / premium" feel.
6. **Match the reference frames.** If your card doesn't look like it belongs next to
   `assets/reference-frames/`, it's wrong regardless of what the instructions said.

## Files

- `references/style-dna.md` — the shared visual + motion system (colors, type,
  shadow/texture techniques, the exact easing + entrance choreography). Read this
  before authoring any card.
- `references/archetypes.md` — per-archetype layout, hero treatment, supporting
  elements, and motion, keyed to the three reference frames.
- `references/detection.md` — how to scan a transcript for B-roll beats, hook
  beats, and pick the archetype + accent for each.
- `references/rendering.md` — turning a composition into MP4 / transparent overlay
  via HyperFrames, and how to composite it onto the edit.
- `assets/reference-frames/` — the three ground-truth frames (object / character /
  text). Look at these often.
- `assets/templates/` — HyperFrames HTML starting points, one per archetype.
