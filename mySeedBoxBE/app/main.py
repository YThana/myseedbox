from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import settings
from app.qbittorrent import QBittorrentError, qbittorrent_client
from app.schemas import AddTorrentRequest, TorrentFile, TorrentSummary


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await qbittorrent_client.aclose()


app = FastAPI(title="mySeedBox API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _resolve_host_path(save_path: str, file_name: str) -> Path:
    """Map a qBittorrent-reported path to the equivalent path on the host,
    using the shared bind-mounted downloads volume."""
    relative_save_path = save_path[len(settings.qbit_container_downloads_path) :].lstrip("/")
    return settings.downloads_dir / relative_save_path / file_name


@app.get("/api/health")
async def health() -> dict[str, str]:
    try:
        await qbittorrent_client.list_torrents()
    except QBittorrentError as exc:
        raise HTTPException(status_code=502, detail=f"qBittorrent unreachable: {exc}") from exc
    return {"status": "ok"}


@app.post("/api/torrents", status_code=201)
async def add_torrent(request: AddTorrentRequest) -> dict[str, str]:
    try:
        await qbittorrent_client.add_magnet(request.magnet_uri)
    except QBittorrentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"status": "added"}


@app.get("/api/torrents")
async def list_torrents() -> list[TorrentSummary]:
    try:
        torrents = await qbittorrent_client.list_torrents()
    except QBittorrentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return [
        TorrentSummary(
            hash=t["hash"],
            name=t["name"],
            state=t["state"],
            progress=t["progress"],
            size=t["size"],
            dlspeed=t["dlspeed"],
            eta=t["eta"],
            save_path=t["save_path"],
        )
        for t in torrents
    ]


@app.get("/api/torrents/{torrent_hash}")
async def get_torrent(torrent_hash: str) -> TorrentSummary:
    torrent = await qbittorrent_client.get_torrent(torrent_hash)
    if torrent is None:
        raise HTTPException(status_code=404, detail="Torrent not found")

    return TorrentSummary(
        hash=torrent["hash"],
        name=torrent["name"],
        state=torrent["state"],
        progress=torrent["progress"],
        size=torrent["size"],
        dlspeed=torrent["dlspeed"],
        eta=torrent["eta"],
        save_path=torrent["save_path"],
    )


@app.delete("/api/torrents/{torrent_hash}")
async def delete_torrent(torrent_hash: str, delete_files: bool = False) -> dict[str, str]:
    try:
        await qbittorrent_client.delete_torrent(torrent_hash, delete_files=delete_files)
    except QBittorrentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"status": "deleted"}


@app.get("/api/torrents/{torrent_hash}/files")
async def get_torrent_files(torrent_hash: str) -> list[TorrentFile]:
    try:
        files = await qbittorrent_client.get_torrent_files(torrent_hash)
    except QBittorrentError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return [TorrentFile(name=f["name"], size=f["size"], progress=f["progress"]) for f in files]


@app.get("/api/torrents/{torrent_hash}/download")
async def download_torrent_file(torrent_hash: str, file_name: str) -> FileResponse:
    torrent = await qbittorrent_client.get_torrent(torrent_hash)
    if torrent is None:
        raise HTTPException(status_code=404, detail="Torrent not found")

    files = await qbittorrent_client.get_torrent_files(torrent_hash)
    matching = next((f for f in files if f["name"] == file_name), None)
    if matching is None:
        raise HTTPException(status_code=404, detail="File not found in torrent")
    if matching["progress"] < 1.0:
        raise HTTPException(status_code=409, detail="File is not fully downloaded yet")

    host_path = _resolve_host_path(torrent["save_path"], file_name)
    if not host_path.is_file():
        raise HTTPException(status_code=404, detail=f"File missing on disk: {host_path}")

    return FileResponse(host_path, filename=host_path.name, media_type="application/octet-stream")
