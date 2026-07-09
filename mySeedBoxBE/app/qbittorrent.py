from typing import Any

import httpx

from app.config import settings


class QBittorrentError(RuntimeError):
    pass


class QBittorrentClient:
    """Thin async wrapper around the qBittorrent WebUI API (v2)."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url=settings.qbit_url, timeout=30.0)
        self._logged_in = False

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _login(self) -> None:
        response = await self._client.post(
            "/api/v2/auth/login",
            data={"username": settings.qbit_username, "password": settings.qbit_password},
        )
        if response.status_code >= 400:
            raise QBittorrentError("Failed to authenticate with qBittorrent")
        self._logged_in = True

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        if not self._logged_in:
            await self._login()

        response = await self._client.request(method, path, **kwargs)
        if response.status_code == 403:
            # Session expired - re-authenticate once and retry.
            await self._login()
            response = await self._client.request(method, path, **kwargs)

        if response.status_code >= 400:
            raise QBittorrentError(f"qBittorrent API error {response.status_code} on {path}: {response.text}")

        return response

    async def add_magnet(self, magnet_uri: str) -> None:
        # A non-2xx status is already turned into a QBittorrentError by _request,
        # so reaching here means qBittorrent accepted the request.
        await self._request(
            "POST",
            "/api/v2/torrents/add",
            data={"urls": magnet_uri},
        )

    async def list_torrents(self) -> list[dict[str, Any]]:
        response = await self._request("GET", "/api/v2/torrents/info")
        return response.json()

    async def get_torrent(self, torrent_hash: str) -> dict[str, Any] | None:
        torrents = await self.list_torrents()
        for torrent in torrents:
            if torrent["hash"] == torrent_hash:
                return torrent
        return None

    async def get_torrent_files(self, torrent_hash: str) -> list[dict[str, Any]]:
        response = await self._request(
            "GET",
            "/api/v2/torrents/files",
            params={"hash": torrent_hash},
        )
        return response.json()

    async def delete_torrent(self, torrent_hash: str, delete_files: bool = False) -> None:
        await self._request(
            "POST",
            "/api/v2/torrents/delete",
            data={"hashes": torrent_hash, "deleteFiles": str(delete_files).lower()},
        )


qbittorrent_client = QBittorrentClient()
