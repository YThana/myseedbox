# mySeedBox

A self-hosted seedbox: paste a magnet link, let [qBittorrent](https://www.qbittorrent.org/) download and seed it, and grab the finished files from a clean web UI. Built to run entirely on your own machine first, with a straightforward path to hosting it on AWS later.

![mySeedBox screenshot](docs/screenshot.png)

## How it works

```
┌──────────────┐      REST       ┌──────────────┐     WebUI API    ┌──────────────┐
│  Vue frontend │ ───────────────▶│ FastAPI backend│ ───────────────▶│  qBittorrent  │
│  (port 5173) │◀─────────────── │  (port 8000)   │◀─────────────── │  (port 8080)  │
└──────────────┘   progress/JSON └──────────────┘   torrent status  └──────────────┘
                                                                              │
                                                                              ▼
                                                                     shared ./data/downloads
                                                                     (backend streams files
                                                                      from here to the browser)
```

- **qBittorrent** runs headless in Docker and does the actual downloading/seeding.
- **FastAPI backend** wraps qBittorrent's Web API — add a magnet, list torrents, list files, stream a completed file back to the browser.
- **Vue frontend** is the UI: add a magnet link, watch live progress, download finished files.

## Tech stack

| Layer | Stack |
|---|---|
| Frontend | Vue 3 (Composition API, `<script setup>`), TypeScript, Vite, Pinia, Vue Router |
| Backend | FastAPI, httpx, Pydantic Settings |
| Torrent engine | qBittorrent (headless, via Docker) |
| Package managers | pnpm (frontend), uv (backend) |

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for qBittorrent)
- [Node.js](https://nodejs.org/) ^22.18 or >=24.12, and [pnpm](https://pnpm.io/)
- Python 3.14+ and [uv](https://docs.astral.sh/uv/)

## Quick start (local)

### 1. Start qBittorrent

```bash
docker compose up -d
```

The first time it starts, qBittorrent prints a **temporary admin password** to its logs:

```bash
docker compose logs qbittorrent | grep -i password
```

Log in at [http://localhost:8080](http://localhost:8080) with user `admin` and that temporary password, then set a permanent password under **Tools → Options → Web UI**.

### 2. Configure and run the backend

```bash
cd mySeedBoxBE
cp .env.example .env   # then fill in the qBittorrent credentials you just set
uv sync
uv run uvicorn main:app --reload --port 8000
```

The API is now live at [http://localhost:8000](http://localhost:8000) (interactive docs at `/docs`).

### 3. Configure and run the frontend

```bash
cd mySeedBoxFE
cp .env.example .env   # defaults already point at localhost:8000
pnpm install
pnpm run dev
```

Open [http://localhost:5173](http://localhost:5173), paste a magnet link, and watch it download.

## Environment variables

**`mySeedBoxBE/.env`**

| Variable | Default | Description |
|---|---|---|
| `QBIT_URL` | `http://localhost:8080` | qBittorrent Web UI base URL |
| `QBIT_USERNAME` | `admin` | qBittorrent Web UI username |
| `QBIT_PASSWORD` | — | qBittorrent Web UI password |

**`mySeedBoxFE/.env`**

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Base URL of the FastAPI backend |

## API overview

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Checks connectivity to qBittorrent |
| `POST` | `/api/torrents` | Add a torrent by magnet link |
| `GET` | `/api/torrents` | List all torrents with live progress |
| `GET` | `/api/torrents/{hash}` | Get a single torrent's status |
| `DELETE` | `/api/torrents/{hash}` | Remove a torrent |
| `GET` | `/api/torrents/{hash}/files` | List files inside a torrent |
| `GET` | `/api/torrents/{hash}/download?file_name=...` | Stream a completed file |

## Project structure

```
my seed box/
├── docker-compose.yml     # qBittorrent container definition
├── data/                  # shared runtime volume (gitignored)
│   ├── downloads/         # completed/in-progress torrent files
│   └── qbittorrent-config/
├── mySeedBoxBE/           # FastAPI backend
│   └── app/
│       ├── config.py      # settings (reads .env)
│       ├── qbittorrent.py # qBittorrent Web API client
│       ├── schemas.py     # Pydantic response models
│       └── main.py        # API routes
└── mySeedBoxFE/           # Vue frontend
    └── src/
        ├── api/           # typed fetch wrapper for the backend
        ├── composables/   # useTorrents() — polling + state
        ├── components/torrents/
        └── utils/
```

## Roadmap

- [ ] Tests (backend + frontend)
- [ ] Torrent categories / multi-file selection UI
- [ ] Deploy to AWS (ECS/EC2 running the same Docker Compose setup, S3/EBS for storage)
