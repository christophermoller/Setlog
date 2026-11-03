# Setlog

Chris's workout tracker. Vanilla JS single-file app.

- Edit `src/app_src.html` (and `src/lib.json` for the exercise library). Never edit `index.html` by hand.
- Build: `python3 tools/build.py` → `index.html` + `sw.js` + `manifest.webmanifest` (GitHub Pages PWA at https://christophermoller.github.io/Setlog/) and `dist/artifact.html` (Claude artifact build).
- The PWA stores data only in the phone's localStorage (`saetlog.v2`). Never change that key or the data shape without a migration.
- UI text: English, minimal, fitness lingo, no commas or "·" or "~" as separators. Chris writes in Danish.
- Commit and push to `main` after building; Pages deploys automatically.
