from pydantic import BaseModel


class AddTorrentRequest(BaseModel):
    magnet_uri: str


class TorrentSummary(BaseModel):
    hash: str
    name: str
    state: str
    progress: float
    size: int
    dlspeed: int
    eta: int
    save_path: str


class TorrentFile(BaseModel):
    name: str
    size: int
    progress: float
