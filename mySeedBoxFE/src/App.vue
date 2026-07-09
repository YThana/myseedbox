<script setup lang="ts">
import TorrentDashboard from '@/components/torrents/TorrentDashboard.vue'
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-brand">
        <img src="/logo.png" alt="mySeedBox logo" class="app-brand-icon" width="28" height="28" />
        <h1 class="app-title">mySeedBox</h1>
      </div>
      <p class="app-subtitle">Grab a magnet link, seed it, download it.</p>
    </header>
    <main>
      <TorrentDashboard />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100dvh;
}

.app-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  padding: 2.5rem 1rem 0.5rem;
  text-align: center;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.app-brand-icon {
  display: block;
  border-radius: 7px;
}

.app-title {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.app-subtitle {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>
