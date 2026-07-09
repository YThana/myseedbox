<script setup lang="ts">
import { Inbox } from '@lucide/vue'
import TorrentListItem from '@/components/torrents/TorrentListItem.vue'
import type { TorrentSummary } from '@/types/torrent'

defineProps<{
  torrents: readonly TorrentSummary[]
}>()

const emit = defineEmits<{
  remove: [hash: string]
}>()
</script>

<template>
  <div v-if="torrents.length === 0" class="torrent-list-empty">
    <Inbox :size="28" aria-hidden="true" />
    <p>No torrents yet. Paste a magnet link above to get started.</p>
  </div>
  <ul v-else class="torrent-list">
    <TorrentListItem
      v-for="torrent in torrents"
      :key="torrent.hash"
      :torrent="torrent"
      @remove="emit('remove', $event)"
    />
  </ul>
</template>

<style scoped>
.torrent-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0;
  margin: 0;
}

.torrent-list-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 3rem 1rem;
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-faint);
  text-align: center;
}

.torrent-list-empty p {
  margin: 0;
  font-size: 0.9rem;
}
</style>
