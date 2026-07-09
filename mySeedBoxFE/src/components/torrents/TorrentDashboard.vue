<script setup lang="ts">
import MagnetForm from '@/components/torrents/MagnetForm.vue'
import TorrentList from '@/components/torrents/TorrentList.vue'
import { useTorrents } from '@/composables/useTorrents'

const { torrents, loading, error, addTorrent, removeTorrent } = useTorrents()

async function handleSubmit(magnetUri: string) {
  try {
    await addTorrent(magnetUri)
  } catch {
    // error state is already surfaced via the composable's `error` ref
  }
}
</script>

<template>
  <section class="torrent-dashboard">
    <MagnetForm :submitting="loading" @submit="handleSubmit" />
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
