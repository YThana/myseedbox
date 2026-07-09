import { onMounted, onUnmounted, readonly, ref, shallowRef } from 'vue'
import * as torrentsApi from '@/api/torrents'
import type { TorrentSummary } from '@/types/torrent'

const POLL_INTERVAL_MS = 2000

export function useTorrents() {
  const torrents = ref<TorrentSummary[]>([])
  const loading = shallowRef(false)
  const error = shallowRef<string | null>(null)

  let pollHandle: ReturnType<typeof setInterval> | undefined

  async function fetchTorrents() {
    try {
      torrents.value = await torrentsApi.fetchTorrents()
      error.value = null
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load torrents'
    }
  }

  async function addTorrent(magnetUri: string) {
    loading.value = true
    error.value = null
    try {
      await torrentsApi.addTorrent(magnetUri)
      await fetchTorrents()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add torrent'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function addTorrentFile(file: File) {
    loading.value = true
    error.value = null
    try {
      await torrentsApi.addTorrentFile(file)
      await fetchTorrents()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add torrent file'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function removeTorrent(hash: string) {
    try {
      await torrentsApi.removeTorrent(hash)
      await fetchTorrents()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to remove torrent'
    }
  }

  onMounted(() => {
    fetchTorrents()
    pollHandle = setInterval(fetchTorrents, POLL_INTERVAL_MS)
  })

  onUnmounted(() => {
    clearInterval(pollHandle)
  })

  return {
    torrents: readonly(torrents),
    loading: readonly(loading),
    error: readonly(error),
    addTorrent,
    addTorrentFile,
    removeTorrent,
  }
}
