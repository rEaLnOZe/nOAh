// Brand typography loader for the CreatrLabs / InfluMatch design system.
//
// Alexandria is the brand's Sans + Display face (§3 of the design system). The
// block templates reference it as "Alexandria, system-ui, sans-serif"; this
// module injects the Google Fonts stylesheet once per page load so the render
// machine actually has the face, mirroring the Caveat injection already used by
// WordPop / HookTitle. `display=swap` keeps text visible on the system-ui
// fallback until Alexandria arrives — no invisible-text window at video pace.
let __brandFontInjected = false;

export const ensureBrandFontLoaded = (): void => {
  if (typeof document === "undefined" || __brandFontInjected) return;
  __brandFontInjected = true;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href =
    "https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700;800&display=swap";
  document.head.appendChild(link);
};

// Kick the request off at module load so the face is in flight before the
// first frame paints.
ensureBrandFontLoaded();
