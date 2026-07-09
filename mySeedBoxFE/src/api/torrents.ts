import type { TorrentFile, TorrentSummary } from '@/types/torrent'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

async function parseOrThrow<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? `Request failed with status ${response.status}`)
  }
  return response.json() as Promise<T>
}

export async function fetchTorrents(): Promise<TorrentSummary[]> {
  const response = await fetch(`${BASE_URL}/api/torrents`)
  return parseOrThrow(response)
}

export async function addTorrent(magnetUri: string): Promise<void> {
  const response = await fetch(`${BASE_URL}/api/torrents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ magnet_uri: magnetUri }),
  })
  await parseOrThrow(response)
}

export async function removeTorrent(hash: string): Promise<void> {
  const response = await fetch(`${BASE_URL}/api/torrents/${hash}`, { method: 'DELETE' })
  await parseOrThrow(response)
}

export async function fetchTorrentFiles(hash: string): Promise<TorrentFile[]> {
  const response = await fetch(`${BASE_URL}/api/torrents/${hash}/files`)
  return parseOrThrow(response)
}

export function downloadUrl(hash: string, fileName: string): string {
  return `${BASE_URL}/api/torrents/${hash}/download?${new URLSearchParams({ file_name: fileName })}`
}
