# Python Network Automation

**Network automation study repository** — practical Python automation for network engineers, built around real-world tooling: Cisco IOS-XE, Meraki, and ISE.

---

## About

I'm a network engineer with ~4 years of hands-on experience working daily with Cisco IOS-XE, Meraki, 802.1X/ISE, firewalls, and VPNs. This repository documents my structured progression from Python fundamentals into practical network automation.

Study plan: 6–8 hours/week across a 12-week structured programme covering foundations, REST APIs, RESTCONF/NETCONF, Ansible, and industrial protocols.

---

## Projects in Progress

### 1. Device Inventory Parser
**Status:** Complete (Week 1 milestone)

A modular inventory tool that ingests device data from CSV or JSON, filters by any field, counts by type or site, and prints a formatted summary report. Built to mirror real network documentation workflows.

**Key features:**
- Single `load_devices(filename)` function with automatic extension detection (`.csv` / `.json`)
- Generic `filter_by_field(devices, field, value)` — one function replaces multiple hardcoded filters
- `count_by_field()` for dynamic summary counts (by type, by site)
- `print_summary()` combining counts and full device listing
- Graceful error handling: `FileNotFoundError`, unsupported formats, `None` guards

**Skills demonstrated:** `csv.DictReader`, `json.load()`, dict manipulation, list comprehension patterns, function decomposition, error handling.

---

### 2. Meraki Daily Health Report *(in progress — Week 2)*
**Status:** Core report generation working end-to-end, CSV export added

Automated health report pulling live data from the Meraki Dashboard API — organisations, networks, devices, offline/dormant detection, firmware status, top clients, and site-to-site VPN state — written to a timestamped text report and a CSV export.

**Key features so far:**
- Authenticated `requests.get()` calls with `X-Cisco-Meraki-API-Key` header and status code checks on every call
- Secrets management via `python-dotenv` / `os.getenv()` — no hardcoded credentials
- Dynamic org/network ID resolution (`get_org_id`, `get_network_id`) — no hardcoded IDs
- Org → Network → Devices API chain, plus org-level device and status endpoints
- Firmware merge across devices/statuses data by serial number
- Offline and dormant device flagging
- Top clients (24h) usage report
- Site-to-site VPN status (hubs, subnets)
- `write_report()` — formatted, timestamped output to text file
- `write_report_csv()` — structured CSV export via `csv.DictWriter`

**Planned:** HTML export, tidy up print vs write duplication.

See [README-meraki.md](README-meraki.md) for full setup, usage, and sample output for this project.

---

### 3. Cisco IOS XE Config/State Checker *(planned — Weeks 6–8)*

Pre/post-change validation using RESTCONF and NETCONF. YAML device inventory, Jinja2 config templates, intended vs actual state comparison.

---

### 4. Python Modbus Sensor Logger *(planned — Weeks 11–12)*

RS485 Modbus client reading temperature/humidity registers, logging to CSV, threshold alerting.

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.13 |
| HTTP / APIs | `requests`, Meraki Dashboard API, RESTCONF |
| Data formats | CSV, JSON, YAML, Jinja2 |
| Config management | Ansible (planned, Weeks 9–10) |
| Protocols | NETCONF / ncclient (planned) |
| Industrial | Modbus TCP/RTU, RS485 (planned) |
| Secrets | `python-dotenv`, `.env` |
| Networking platforms | Cisco IOS-XE, Meraki, ISE, 802.1X |

---

## Repository Structure

```
Python-Study-Auto/
├── auto_w01-s08-01.py      # Device Inventory Parser — final working version (Week 1)
├── auto_w02-s01-01.py      # Meraki API — first live calls
├── auto_w02-s02-01.py      # Dynamic org/network ID lookups
├── auto_w02-s03-01.py      # Status code checking on API calls
├── auto_w02-s03-02.py      # Live device status pulls
├── auto_w02-s04-01.py      # Formatted health report + write-to-file
├── auto_w02-s05-01.py      # Firmware merge + top clients
├── auto_w02-s06-01.py      # VPN status integration
├── auto_w02-s07-01.py      # VPN status + dormant flagging
├── auto_w02-s09-01.py      # Current Meraki Daily Health Report — adds CSV export
├── inventory.py            # Earlier inventory iteration
├── devices.csv             # Sample device data (CSV)
├── devices.json            # Sample device data (JSON)
├── meraki_report.txt       # Generated output — Meraki health report (gitignored)
├── meraki_report.csv       # Generated output — Meraki health report CSV (gitignored)
├── README-meraki.md        # Dedicated README for the Meraki Daily Health Report project
├── sessions/               # Structured session logs + study notes (W1S1 → present)
├── python-auto-log.md      # Running session log (gitignored, local only)
└── .env                    # Not committed — API keys via dotenv
```

> Earlier `auto_w1*.py` files (`auto_w1-p1.py`, `auto_w1b.py`, etc.) are draft iterations from early Week 1 exercises, kept for history — `auto_w01-s08-01.py` is the consolidated version.

---

## Security Practices

- No credentials, tokens, or API keys are committed to this repository
- All secrets loaded at runtime via `python-dotenv` and `os.getenv()`
- `.env` excluded via `.gitignore`

---

## Study Roadmap

| Weeks | Focus | Status |
|---|---|---|
| 1–2 | Python foundations — data structures, file I/O, CSV/JSON, error handling | ✅ Week 1 complete |
| 3–5 | REST APIs, Meraki Dashboard API, pagination, CSV/HTML export | 🔄 In progress — health report core complete, export formats pending |
| 6–8 | YAML, Jinja2, RESTCONF, NETCONF, IOS XE state checks | Planned |
| 9–10 | Ansible — inventory, playbooks, network modules, config backup | Planned |
| 11–12 | Modbus — register reads, CSV logging, threshold alerts | Planned |

---

## Background & Goals

This repo is evidence of deliberate, hands-on skill-building — practical automation applied to the platforms I work with daily, not generic Python exercises.

Certifications: CCNA · Studying CCNP ENCOR

---

*Session logs in `/sessions/` track every topic covered, concepts flagged for review, and next tasks — a structured record of the learning process.*
