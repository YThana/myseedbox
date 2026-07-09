<script setup lang="ts">
import { ChevronDown, ChevronUp, Download, Trash2 } from '@lucide/vue'
import { computed, ref, shallowRef } from 'vue'
import { downloadUrl, fetchTorrentFiles } from '@/api/torrents'
import type { TorrentFile, TorrentSummary } from '@/types/torrent'
import { formatBytes, formatEta, formatSpeed } from '@/utils/format'
import { torrentStateLabel, torrentStatus } from '@/utils/torrentState'

const props = defineProps<{
  torrent: TorrentSummary
}>()

const emit = defineEmits<{
  remove: [hash: string]
}>()

const filesExpanded = shallowRef(false)
const filesLoading = shallowRef(false)
const filesError = shallowRef<string | null>(null)
const files = ref<TorrentFile[]>([])

const progressPercent = computed(() => Math.round(props.torrent.progress * 100))
const isComplete = computed(() => props.torrent.progress >= 1)
const status = computed(() => torrentStatus(props.torrent.state))
const stateLabel = computed(() => torrentStateLabel(props.torrent.state))

async function toggleFiles() {
  filesExpanded.value = !filesExpanded.value
  if (!filesExpanded.value || files.value.length > 0) return

  filesLoading.value = true
  filesError.value = null
  try {
    files.value = await fetchTorrentFiles(props.torrent.hash)
  } catch (err) {
    filesError.value = err instanceof Error ? err.message : 'Failed to load files'
  } finally {
    filesLoading.value = false
  }
}

function fileDownloadUrl(fileName: string): string {
  return downloadUrl(props.torrent.hash, fileName)
}
</script>

<template>
  <li class="torrent-card">
    <div class="torrent-card-header">
      <span class="torrent-name" :title="torrent.name">{{ torrent.name }}</span>
      <span class="status-badge" :class="`status-${status}`">{{ stateLabel }}</span>
    </div>

    <div class="torrent-progress-track">
      <div
        class="torrent-progress-fill"
        :class="`fill-${status}`"
        :style="{ width: `${progressPercent}%` }"
      />
    </div>

    <div class="torrent-stats">
      <span class="torrent-stat-percent">{{ progressPercent }}%</span>
      <span>{{ formatBytes(torrent.size) }}</span>
      <span v-if="!isComplete">{{ formatSpeed(torrent.dlspeed) }}</span>
      <span v-if="!isComplete">ETA {{ formatEta(torrent.eta) }}</span>
    </div>

    <div class="torrent-actions">
      <button class="btn btn-ghost" type="button" @click="toggleFiles">
        <ChevronUp v-if="filesExpanded" :size="15" aria-hidden="true" />
        <ChevronDown v-else :size="15" aria-hidden="true" />
        {{ filesExpanded ? 'Hide files' : 'Show files' }}
      </button>
      <button
        class="btn btn-ghost btn-danger"
        type="button"
        @click="emit('remove', torrent.hash)"
      >
        <Trash2 :size="15" aria-hidden="true" />
        Remove
      </button>
    </div>

    <ul v-if="filesExpanded" class="torrent-files">
      <li v-if="filesLoading" class="torrent-files-status">Loading files…</li>
      <li v-else-if="filesError" class="torrent-files-status torrent-files-error">{{ filesError }}</li>
      <li v-for="file in files" v-else :key="file.name" class="torrent-file">
        <span class="torrent-file-name" :title="file.name">{{ file.name }}</span>
        <span class="torrent-file-size">{{ formatBytes(file.size) }}</span>
        <a
          v-if="file.progress >= 1"
          class="torrent-file-download"
          :href="fileDownloadUrl(file.name)"
          download
        >
          <Download :size="14" aria-hidden="true" />
          Download
        </a>
        <span v-else class="torrent-file-pending">{{ Math.round(file.progress * 100) }}%</span>
      </li>
    </ul>
  </li>
</template>

<style scoped>
.torrent-card {
  list-style: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  transition: border-color 150ms ease;
}

.torrent-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.torrent-name {
  font-weight: 600;
  font-size: 0.95rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  flex-shrink: 0;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.status-downloading {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.status-seeding {
  background: rgba(4, 120, 87, 0.18);
  color: #34d399;
}

.status-paused {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
}

.status-error {
  background: rgba(220, 38, 38, 0.15);
  color: #f87171;
}

.status-queued {
  background: rgba(217, 119, 6, 0.15);
  color: #fbbf24;
}

.torrent-progress-track {
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.torrent-progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 300ms ease;
}

.fill-downloading {
  background: #3b82f6;
}

.fill-seeding {
  background: var(--color-accent-hover);
}

.fill-paused {
  background: #94a3b8;
}

.fill-error {
  background: var(--color-destructive);
}

.fill-queued {
  background: #d97706;
}

.torrent-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.82rem;
  font-family: var(--font-mono);
  color: var(--color-text-muted);
}

.torrent-stat-percent {
  color: var(--color-text);
  font-weight: 600;
}

.torrent-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  height: 32px;
  padding: 0 0.65rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 0.82rem;
  font-weight: 500;
  transition:
    background-color 150ms ease,
    color 150ms ease,
    border-color 150ms ease;
}

.btn-ghost:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
  border-color: rgba(255, 255, 255, 0.16);
}

.btn-danger:hover {
  color: #f87171;
  border-color: rgba(220, 38, 38, 0.4);
  background: rgba(220, 38, 38, 0.1);
}

.torrent-files {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0;
  margin: 0.25rem 0 0;
  border-top: 1px solid var(--color-border);
}

.torrent-file {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.85rem;
  padding: 0.45rem 0;
  border-bottom: 1px solid var(--color-border);
}

.torrent-file:last-child {
  border-bottom: none;
}

.torrent-file-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-muted);
}

.torrent-file-size {
  flex-shrink: 0;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--color-text-faint);
}

.torrent-file-download {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--color-accent-hover);
  font-weight: 600;
  text-decoration: none;
  transition: color 150ms ease;
}

.torrent-file-download:hover {
  color: #34d399;
  text-decoration: underline;
}

.torrent-file-pending {
  flex-shrink: 0;
  color: var(--color-text-faint);
  font-family: var(--font-mono);
  font-size: 0.78rem;
}

.torrent-files-status {
  list-style: none;
  padding: 0.5rem 0;
  color: var(--color-text-faint);
  font-size: 0.85rem;
}

.torrent-files-error {
  color: #f87171;
}
</style>
