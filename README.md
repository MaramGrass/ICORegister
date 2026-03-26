# ICO Register – Isle of Man

Searchable register of Controllers and Processors, built from the official ICO export.

## Files

| File | Description |
|------|-------------|
| `index.html` | Self-contained search page — open in any browser |
| `registrars.json` | Data exported from the Excel spreadsheet |
| `update_data.py` | Re-generates `registrars.json` from a fresh Excel export |

## Usage

Just open `index.html` in a browser. No server needed.

For GitHub Pages: push the repo, enable Pages on `main`, and the site goes live at `https://<username>.github.io/<repo>/`.

## Updating the data

1. Download a fresh Excel export from the ICO portal
2. Run:
   ```bash
   python update_data.py --input "Active_Registration_Overviews_*.xlsx"
   ```
3. Commit the updated `registrars.json`

## Data fields

| Field | Source column |
|-------|--------------|
| `registration_no` | Name (the R-number) |
| `name` | Controller/Processor Name |
| `organisation_type` | Organisation Type |
| `status` | Registration Status |
| `fee_exempt` | Fee Exempt |
| `expiry_date` | Registration Expiry |
| `created_on` | Created On |
| `modified_on` | Modified On |
