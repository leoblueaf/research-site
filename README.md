# research.graybearstudio.com

Hidden Structure Research Group site. Standalone, separate from the GrayBear Studio app pages.

- `research/` is maintained by the Observer Limit Program chat (`research.py` holds every page, result and correction).
- `assets/site.css` is a copy of the studio base stylesheet; `research/research.css` styles the pages.
- Build: `pip install latex2mathml && python3 build.py` (output in `dist/`). GitHub Actions builds and deploys on every push to `main`.
