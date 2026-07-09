export interface TorrentSummary {
  hash: string
  name: string
  state: string
  progress: number
  size: number
  dlspeed: number
  eta: number
  save_path: string
}

export interface TorrentFile {
  name: string
  size: number
  progress: number
}
