export type TorrentStatus = 'downloading' | 'seeding' | 'paused' | 'error' | 'queued'

const STATUS_BY_STATE: Record<string, TorrentStatus> = {
  downloading: 'downloading',
  metaDL: 'downloading',
  forcedDL: 'downloading',
  allocating: 'downloading',
  checkingDL: 'downloading',
  uploading: 'seeding',
  stalledUP: 'seeding',
  forcedUP: 'seeding',
  checkingUP: 'seeding',
  pausedUP: 'paused',
  pausedDL: 'paused',
  stalledDL: 'paused',
  queuedUP: 'queued',
  queuedDL: 'queued',
  error: 'error',
  missingFiles: 'error',
}

const LABEL_BY_STATE: Record<string, string> = {
  downloading: 'Downloading',
  metaDL: 'Fetching metadata',
  forcedDL: 'Downloading',
  allocating: 'Allocating',
  checkingDL: 'Checking',
  uploading: 'Seeding',
  stalledUP: 'Seeding (idle)',
  forcedUP: 'Seeding',
  checkingUP: 'Checking',
  pausedUP: 'Paused',
  pausedDL: 'Paused',
  stalledDL: 'Stalled',
  queuedUP: 'Queued',
  queuedDL: 'Queued',
  error: 'Error',
  missingFiles: 'Files missing',
}

export function torrentStatus(state: string): TorrentStatus {
  return STATUS_BY_STATE[state] ?? 'queued'
}

export function torrentStateLabel(state: string): string {
  return LABEL_BY_STATE[state] ?? state
}
