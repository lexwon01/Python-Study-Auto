# Meraki Daily Health Report

A command-line tool that pulls live data from the Meraki Dashboard API and produces a daily network health report — device status, firmware, top clients, VPN state, and dormant/offline flagging — as a plain-text report, a CSV export, and an HTML report.

Built as a Week 2 project in a structured Python network automation study programme (see the main [README](README.md)).

---

## Purpose

Manually checking Meraki dashboards across orgs, networks, and device types for a daily health check is slow and easy to miss things on. This script automates that check: one run pulls org, network, and device data, cross-references live status against inventory, and produces a report you can read in seconds or pipe into other tooling via CSV.

---

## Requirements

- Python 3.13+
- A Meraki Dashboard API key with read access to the target organisation
- Packages: `requests`, `python-dotenv`, `jinja2`

---

## Install

```bash
git clone <this-repo>
cd Python-Study-Auto
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv jinja2
```

Create a `.env` file in the repo root (never commit this file):

```
MERAKI_API_KEY=your_api_key_here
ORG_ID=your_org_name_here
NET_ID=your_network_name_here
```

> Note: despite the variable names `ORG_ID` / `NET_ID`, the script currently looks these up by **name** (`get_org_id`, `get_network_id` resolve name → ID), not by raw Meraki ID. Set them to the exact org/network name as shown in the Meraki dashboard.

Confirm `.env` is listed in `.gitignore` before running anything.

---

## Usage

```bash
python auto_w02-s10-01.py
```

This will:
1. Resolve the organisation and network ID from the names in `.env`
2. Pull device inventory, live device statuses, top clients (24h), and VPN status
3. Merge firmware data into the status list by serial number
4. Print a summary report to the terminal
5. Write a timestamped text report to `meraki_report.txt`
6. Write a CSV export to `meraki_report.csv`
7. Render and write an HTML report to `meraki_report.html` via a Jinja2 template (`report_template.html`)

---

## Sample output

Terminal summary (`print_summary`):

```
=== Meraki Health Report ===
Total devices: 6
Offline: 0

--- Device Status ---
RE-IPH-MX67 | MX67 | wired-19-2-8 | online | 2026-07-06T16:43:13.094000Z
RE-MLAB-MX67 | MX67 | wired-19-2-8 | online | 2026-07-06T16:43:52.481000Z
RE-MR53 | MR53 | wireless-30-7-1 | dormant | 2026-03-09T17:19:16.785000Z
RE-DC-CAM-01 | MV2 | camera-5-6-2 | dormant | 2026-03-09T17:21:29.122000Z
RE-MLAB-MR28 | MR28 | wireless-32-1-7 | online | 2026-07-06T16:43:33.229000Z
RE-MLAB-MS120 | MS120-8FP | switch-17-2-2 | online | 2026-07-06T16:43:39.289000Z

--- Top Clients (24h) ---
...

--- Site-to-Site VPN Details ---
Hub ID: ...
Local subnet: ... | In use: True/False

Device RE-MR53 is DORMANT
Device RE-DC-CAM-01 is DORMANT
```

CSV export (`meraki_report.csv`):

```csv
name,model,status,firmware,lastReportedAt
RE-IPH-MX67,MX67,online,wired-19-2-8,2026-07-06T16:43:13.094000Z
RE-MLAB-MX67,MX67,online,wired-19-2-8,2026-07-06T16:43:52.481000Z
RE-MR53,MR53,dormant,wireless-30-7-1,2026-03-09T17:19:16.785000Z
```

HTML export (`meraki_report.html`), rendered from `report_template.html`:

```html
<html>
<body>
<h1>Meraki Health Report</h1>
<ul>
    <li>RE-IPH-MX67 - online</li>
    <li>RE-MLAB-MX67 - online</li>
    <li>RE-MR53 - dormant</li>
</ul>
</body>
</html>
```

---

## What I learned

- Chaining Meraki's org → network → device API hierarchy, resolving names to IDs dynamically instead of hardcoding
- Checking `response.status_code` on every call rather than assuming success, and failing loudly with `exit()` when a required lookup comes back empty
- Merging two API responses (device inventory and live status) on a shared key (`serial`) to backfill firmware data that one endpoint doesn't return
- Managing secrets with `python-dotenv` / `os.getenv()` so no API key or org name is ever committed
- Writing the same data out through two different serialisations — free-text via `f.write()` and structured via `csv.DictWriter` — and the trade-offs between them (human-readable vs machine-consumable)
- `csv.DictWriter`'s `restval` and `extrasaction='ignore'` for handling dict rows with missing or extra keys against a fixed fieldname list
- Rendering a Jinja2 template (`{% for %}` loop over a list of dicts) to produce a third output format from the same in-memory data, and that a rendered template is just a string — writing it out is a plain `f.write()`, not a `csv.DictWriter`-style row-by-row process

---

## Future improvements

- Deduplicate the `print_*` and `write_report` logic — most sections are printed and written twice with near-identical formatting
- Expand the HTML template to include firmware, VPN, and dormant sections (currently name/status only)
- Handle devices with a missing/empty `name` field (seen in live data) instead of rendering a blank list item
- Pagination handling for orgs with device counts beyond a single API page
- Command-line arguments (e.g. `--org`, `--network`, `--format csv`) instead of `.env`-only configuration
- Scheduling (cron / Task Scheduler) for genuine daily automation rather than manual runs
- Alerting (e.g. Slack/email) when offline count exceeds a threshold

---

## Security notes

- No API keys, org IDs, or network names are hardcoded — all loaded via `.env` and `os.getenv()`
- `.env`, `meraki_report.txt`, `meraki_report.csv`, and `meraki_report.html` are excluded from version control via `.gitignore`
- Generated reports contain device names, models, and internal subnet details — treat exported files as internal-only, not for public sharing
