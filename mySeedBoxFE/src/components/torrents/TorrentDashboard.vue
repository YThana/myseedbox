<script setup lang="ts">
import MagnetForm from '@/components/torrents/MagnetForm.vue'
import TorrentFileUpload from '@/components/torrents/TorrentFileUpload.vue'
import TorrentList from '@/components/torrents/TorrentList.vue'
import { useTorrents } from '@/composables/useTorrents'

const { torrents, loading, error, addTorrent, addTorrentFile, removeTorrent } = useTorrents()

async function handleSubmit(magnetUri: string) {
  try {
    await addTorrent(magnetUri)
  } catch {
    // error state is already surfaced via the composable's `error` ref
  }
}

async function handleUpload(file: File) {
  try {
    await addTorrentFile(file)
  } catch {
    // error state is already surfaced via the composable's `error` ref
  }
}
</script>

<template>
  <section class="torrent-dashboard">
    <div class="torrent-dashboard-add">
      <MagnetForm :submitting="loading" @submit="handleSubmit" />
      <div class="torrent-dashboard-divider">
        <span>or</span>
      </div>
      <TorrentFileUpload :uploading="loading" @upload="handleUpload" />
    </div>
    <p v-if="error" class="torrent-dashboard-error" role="alert">{{ error }}</p>
    <TorrentList :torrents="torrents" @remove="removeTorrent" />
  </section>
</template>

<style scoped>
.torrent-dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-width: 680px;
  margin: 0 auto;
  padding: 1.5rem 1rem 4rem;
}

.torrent-dashboard-add {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.torrent-dashboard-divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-text-faint);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.torrent-dashboard-divider::before,
.torrent-dashboard-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.torrent-dashboard-error {
  margin: 0;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  background: rgba(220, 38, 38, 0.12);
  border: 1px solid rgba(220, 38, 38, 0.35);
  color: #fca5a5;
  font-size: 0.9rem;
}
</style>
