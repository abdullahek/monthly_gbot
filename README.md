# 🤖 Genesis Analytics G:Bot (monthly_gbot)

> **A keyword-driven WhatsApp marketing & information chatbot for Genesis Analytics — the foundational G:Bot template that powers the wider WageWise survey ecosystem. Visitors message the bot to learn about the firm, its core values, COVID-19 tools, careers, regional offices, and corporate enquiries.**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-000000?logo=flask)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.3-D71F00)](https://www.sqlalchemy.org/)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-F22F46?logo=twilio&logoColor=white)](https://www.twilio.com/)
[![SQL Server](https://img.shields.io/badge/Azure_SQL-MSSQL-CC2927?logo=microsoftsqlserver&logoColor=white)](https://azure.microsoft.com/en-us/products/azure-sql/)
[![Azure](https://img.shields.io/badge/Azure-Web_App-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![Deploy MonthlyApp](https://github.com/abdullahek/monthly_gbot/actions/workflows/master_monthlyapp.yml/badge.svg)](https://github.com/abdullahek/monthly_gbot/actions/workflows/master_monthlyapp.yml)
[![Deploy wagewise-monthly](https://github.com/abdullahek/monthly_gbot/actions/workflows/master_wagewise-monthly.yml/badge.svg)](https://github.com/abdullahek/monthly_gbot/actions/workflows/master_wagewise-monthly.yml)

---

## 🌟 Overview

**monthly_gbot** is the original **G:Bot** — a lightweight Twilio WhatsApp chatbot built for **Genesis Analytics** (Africa's largest economics-based consulting firm). It is the **template repo** that the more elaborate **WageWise** survey bots (`wagwise-monthly`, `wagewise-endline`, `Campaign_Responses`) all descend from.

In its current incarnation it serves as a **public-facing marketing FAQ**: a visitor sends a WhatsApp message to a configured Twilio number and the bot responds based on simple keyword matching, returning rich-text messages about the firm, its work, regional offices, COVID-19 dashboards, careers, and how to get in touch.

Every incoming message is logged to an Azure SQL table called `Data_for_G:Bot` so the marketing team has a record of who has interacted with the bot and what they asked.

---

## ✨ Core Features

### 💬 Keyword-driven Conversation (`glogic/bot_view.py`)
A single Twilio webhook (`POST /message`) maps user input to canned replies stored in `glogic/gresponses.py`:

| User keyword (any of) | Response |
|------------------------|----------|
| `hi`, `hello`, `menu` | Main welcome menu |
| `about` | Who Genesis Analytics is |
| `values` | The three core values (Siyakhana / Plus Ultra / Glass Box) |
| `value` | Recent value-unlocked projects (live web-scrape, currently disabled) |
| `news` | News submenu (headlines / newsletters / reports) |
| `headline`, `newsletter`, `report` | Live-scraped news lists (currently disabled) |
| `covid` | COVID-19 tools menu |
| `1` / `africa` | "Is Africa Flattening The Curve" dashboard info |
| `2` / `healthcare` | "Healthcare Risk Calculator" info |
| `3` / `info` | COVID-19 news (live-scrape, currently disabled) |
| `contact` | Contact submenu (BDU / Careers / Offices / Corporate) |
| `bdu`, `careers`, `corporate` | Department contact details |
| `offices` | Country list (ZA / KE / UK / CA / AE / IN / NG) |
| `za`, `ke`, `uk`, `ca`, `ae`, `in`, `ng` | Office address + contact for that country |
| `are you still working` | Health-ping reply ("Yes, all is well") |
| _anything else_ | Friendly retry hint |

Every reply is suffixed with *"If you would like to return the menu, just say *Hi* or type *Menu*."*.

### 🗃️ Conversation Logging
Every inbound message is persisted to MSSQL **before** any response logic runs:

```python
db.save(User(number=num, response=incoming_msg))
```

→ Stored in the `Data_for_G:Bot` table with `id`, `number`, `response`, `date_added` — handy for analytics on which marketing keywords drive engagement.

### 🌐 Live Web-Scraping Stub (`glogic/WebScrape.py`)
Originally the bot scraped Genesis Analytics' website (`/news`, `/covid19`, `/value-unlocked-intro`) using `requests` + `BeautifulSoup` to pull the latest 3 headlines, newsletters, reports, and value-unlocked projects on demand.

The whole module is **currently commented out** — the keywords (`headline`, `newsletter`, `report`, `info`, `value`) still resolve to `WebScrape.<attr>` references that will throw `AttributeError` at runtime until you re-enable the scraper or replace those branches with a static dictionary entry.

### ☁️ Dual-target Azure Deployment
Two GitHub Actions workflows ship the same code to two separate Azure Web Apps:

| Workflow | Azure App Service | Trigger |
|----------|-------------------|---------|
| `master_monthlyapp.yml` | `MonthlyApp` (Production slot) | push to `master` |
| `master_wagewise-monthly.yml` | `wagewise-monthly` (Production slot) | push to `master` |

Both use Python 3.10, install `requirements.txt`, and deploy via `azure/webapps-deploy@v2` with publish-profile secrets.

---

## 🏗️ Architecture

```
              ┌──────────────────────────┐
              │    WhatsApp visitor      │
              │  (any phone number)      │
              └──────────┬───────────────┘
                         │
                         ▼
              ┌──────────────────────────┐
              │         Twilio           │
              │   WhatsApp Business API  │
              └──────────┬───────────────┘
                         │  POST /message
                         ▼
       ┌────────────────────────────────────────┐
       │         Flask App (Azure Web App)      │
       │                                        │
       │  ┌──────────────────────────────────┐  │
       │  │      glogic/bot_view.py          │  │
       │  │   ─ log message → MSSQL          │  │
       │  │   ─ keyword match                │  │
       │  │   ─ build TwiML response         │  │
       │  └────┬──────────────┬──────────────┘  │
       │       │              │                 │
       │       ▼              ▼                 │
       │ ┌──────────┐ ┌─────────────────┐       │
       │ │ gresponses│ │   WebScrape    │       │
       │ │ Dictionary│ │ (commented out)│       │
       │ └──────────┘ └─────────────────┘       │
       └─────────────────┬──────────────────────┘
                         ▼
              ┌──────────────────────┐
              │   Azure SQL DB       │
              │  Data_for_G:Bot      │
              │  (id, number,        │
              │   response, date)    │
              └──────────────────────┘
```

---

## 📦 Project Structure

```
monthly_gbot/
├── .github/
│   └── workflows/
│       ├── master_monthlyapp.yml          # Deploys → Azure App "MonthlyApp"
│       └── master_wagewise-monthly.yml    # Deploys → Azure App "wagewise-monthly"
├── glogic/                                # Flask application package
│   ├── __init__.py                        # App + DB factory (prepare_app)
│   ├── config.py                          # MSSQL & Test config (env-driven)
│   ├── models.py                          # User → table "Data_for_G:Bot"
│   ├── views.py                           # Root + view-module loader
│   ├── bot_view.py                        # /message — keyword → reply router
│   ├── gresponses.py                      # Static reply dictionary
│   └── WebScrape.py                       # (Commented out) live news/value scraper
├── migrations/                            # Alembic / Flask-Migrate
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── f1c869d78699_.py               # Initial schema migration
├── manage.py                              # Flask-Script CLI entrypoint (db commands)
├── startup.sh                             # Azure container boot script
├── requirements.txt
├── .env.template                          # Sample env-var manifest
└── README.md
```

---

## 🗃️ Database Schema (`glogic/models.py`)

| Table | Column | Type | Notes |
|-------|--------|------|-------|
| **`Data_for_G:Bot`** | `id` | Integer (PK) | Auto-increment |
| | `number` | String(20) | WhatsApp sender number, **unique** |
| | `response` | String | The raw message body the user sent |
| | `date_added` | DateTime | Defaults to `datetime.now` on insert |

> ⚠️ The `unique=True` on `number` means **only the first message** from a given number can be persisted — subsequent inserts will raise an `IntegrityError`. If you want a full message log, drop the unique constraint or model a separate `messages` table that references `users` by FK.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10 (CI) — code itself is 3.6+ compatible |
| Web framework | Flask 1.1.2 |
| WSGI server | Gunicorn (production) / Flask dev server (local) |
| ORM / Migrations | SQLAlchemy 1.3 + Flask-Migrate (Alembic) + Flask-Script |
| Raw SQL driver | pyodbc 4 (ODBC Driver 18 for SQL Server) |
| Database | Azure SQL (MSSQL) |
| Messaging | Twilio WhatsApp (TwiML `MessagingResponse`) |
| Scraping (disabled) | requests, beautifulsoup4, lxml |
| Hosting | Azure App Service (Linux) |
| CI/CD | GitHub Actions → Azure publish-profile deploy |

---

## 🛠️ Local Development

### Prerequisites
- Python **3.6+** (CI builds with 3.10)
- ODBC Driver 18 for SQL Server ([Microsoft download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))
- An Azure SQL instance (or use the bundled `TestConfig` SQLite mode by switching `prepare_app(environment='test')` in `manage.py`)
- Twilio account with the WhatsApp Sandbox enabled
- `ngrok` for exposing the local server to Twilio

### 1. Clone & install

```bash
git clone https://github.com/abdullahek/monthly_gbot.git
cd monthly_gbot

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.template` to `.env` and fill in the values:

```bash
export SECRET_KEY="<run: python3 -c 'import secrets; print(secrets.token_hex(50))'>"
export DEBUG=True

# Azure SQL (consumed by glogic/config.py)
export SERVER="your-server.database.windows.net"
export DATABASE="your-db"
export NAME="your-username"
export PASSWORD="your-password"
```

> **Note:** `glogic/config.py` reads `NAME` (not `USERNAME`) for the SQL login. The `.env.template` ships without `NAME` — add it manually.

Source it:

```bash
source .env
```

### 3. Apply migrations

```bash
python manage.py db upgrade        # Creates Data_for_G:Bot via Alembic
```

### 4. Run the bot

**Flask-Script dev server:**
```bash
python manage.py runserver
```

**Gunicorn (production-like):**
```bash
gunicorn --bind=0.0.0.0 --timeout 600 manage:app
```

### 5. Expose to Twilio

```bash
ngrok http 5000
```

Set your Twilio WhatsApp Sandbox webhook → `https://<ngrok-id>.ngrok.io/message`. Visit the root URL to see *"I'm working"* as a sanity check.

---

## 🌐 API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` / `POST` | `/` | Health check — returns *"I'm working"* |
| `GET` / `POST` | `/message` | Twilio webhook — keyword router + DB log |

---

## 🔄 Conversation Flow

```
                 POST /message  (Twilio)
                        │
                        ▼
          ┌──────────────────────────────┐
          │ db.save(User(number, body))  │
          │ → INSERT into Data_for_G:Bot │
          └──────────────┬───────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │  Lower-case `incoming_msg`   │
          │  Keyword cascade (if/elif)   │
          └──────────────┬───────────────┘
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
  ┌────────┐       ┌─────────┐       ┌──────────────┐
  │ menu   │       │ static  │       │ web-scrape   │
  │ keyword│       │ topic   │       │ keyword      │
  │ → hello│       │ → reply │       │ → currently  │
  │        │       │         │       │   raises     │
  └────┬───┘       └────┬────┘       │   AttrError  │
       │                │            └──────┬───────┘
       └────────┬───────┘                   │
                ▼                           │
       ┌────────────────────┐               │
       │ append "say *Hi*"  │◀──────────────┘
       │ menu hint          │
       └─────────┬──────────┘
                 ▼
            TwiML response
```

---

## 🚢 Deployment (Azure)

This repo ships **two independent GitHub Actions workflows**, both triggered on push to `master`:

### `master_monthlyapp.yml`
- Target App Service: **`MonthlyApp`** (Production slot)
- Publish-profile secret: `AZUREAPPSERVICE_PUBLISHPROFILE_694E55DB06854880B8B47C6980A4D44D`

### `master_wagewise-monthly.yml`
- Target App Service: **`wagewise-monthly`** (Production slot)
- Publish-profile secret: `AZUREAPPSERVICE_PUBLISHPROFILE_C8945B0642C2413F8E1E7D6A6E6BC47A`

> ⚠️ Both workflows deploy the **same artifact** to two different App Services. If `wagewise-monthly` is meant to host the elaborate WageWise survey app (from the sibling `wagwise-monthly` repo), **disable** the `master_wagewise-monthly.yml` workflow here to avoid overwriting the production survey deployment with this marketing bot.

### Container start (`startup.sh`)
```bash
apt-get update
apt-get install -y unixodbc-dev
ACCEPT_EULA=Y apt-get install msodbcsql17
gunicorn --bind=0.0.0.0 --timeout 600 manage:app
```

### Required Azure App Settings
| Setting | Used by |
|---------|---------|
| `SECRET_KEY` | Flask sessions |
| `DEBUG` | Flask config |
| `SERVER`, `DATABASE`, `NAME`, `PASSWORD` | Azure SQL connection |

### Twilio webhook
Point your WhatsApp sender to:

```
https://<your-app>.azurewebsites.net/message
```

---

## 🔒 Security & Tech-Debt Notes

A few things worth tightening before any further public roll-out:

- 🔴 **`unique=True` on `User.number`** silently breaks logging after the first message from any given number — every subsequent insert raises `IntegrityError` and the bot's reply still goes out, which masks the failure. Either drop the constraint or migrate to a 1-to-many `messages` table.
- 🔴 **WebScrape.py is fully commented out** but `bot_view.py` still references `WebScrape.covnews`, `WebScrape.bulletins`, `WebScrape.headlines`, `WebScrape.reports`, and `WebScrape.value`. Hitting any of those keywords (`info`, `newsletter`, `headline`, `report`, `value`) will raise `AttributeError`. Either re-enable the scraper or replace those branches with `Dictionary` lookups.
- 🟠 **No Twilio request-signature validation** — anyone can POST to `/message` and write into your Azure SQL database.
- 🟠 **`SECRET_KEY` has no fallback** — if Azure App Settings are missing it, Flask sessions silently fail.
- 🟠 **`.env.template` is missing `NAME`** even though `config.py` requires it — local-dev DB connections will crash with `TypeError: must be str, not None` until added.
- 🟠 **Two workflows, same code, two production targets** — one of them is almost certainly stepping on a sibling app's deployment. Audit and disable as needed.
- 🟢 **`requirements.txt`** mixes pinned (`==`) and compatible (`~=`) constraints with packages that have nothing to do with the runtime (`numpy`, `cryptography`, `keyring`, `Babel`, `ipython`). Trim it down.
- 🟢 **`migrations/versions/f1c869d78699_.py`** lives in the repo but the table name (`Data_for_G:Bot`) contains a colon — fine for MSSQL but it will quote-escape oddly in some tools.

---

## 🧪 Useful Commands

```bash
# Apply DB migrations
python manage.py db upgrade

# Generate a new migration after editing models.py
python manage.py db migrate -m "describe change"

# Run the dev server
python manage.py runserver

# Production
gunicorn --bind=0.0.0.0 --timeout 600 manage:app
```

---

## 📄 License

This project is private and proprietary to its owner. All rights reserved.

---

## 👤 Author / Maintainer

**Abdullah EK** — [@abdullahek](https://github.com/abdullahek)

> **G:Bot** is the foundational template originally authored by **Genesis Analytics**. This repository (`monthly_gbot`) is the marketing/info-bot incarnation; sibling repos (`wagwise-monthly`, `wagewise-endline`, `Campaign_Responses`) reuse the same skeleton for the WageWise financial-literacy survey programme.

---

<p align="center">
  Built with ❤️ for friendly first-touch marketing on WhatsApp
</p>
