# ICO Register – Isle of Man

## Files
| File | Purpose |
|------|---------|
| `index.html` | The ready-to-use search page — open directly in any browser |
| `index_template.html` | Template used to rebuild the page |
| `build.py` | Rebuild `index.html` from a fresh Excel export |
| `register.xlsx` | The source data (keep for reference) |

## Updating the data
1. Download a fresh export from the ICO portal
2. Place it in this folder
3. Run: `python build.py --input your_new_export.xlsx`
4. Commit the new `index.html`

## GitHub Pages
Push this repo, enable Pages on the `main` branch root, done.
No server needed — the data is baked directly into `index.html`.
