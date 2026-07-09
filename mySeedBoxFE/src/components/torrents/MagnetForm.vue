<script setup lang="ts">
import { Loader2, Plus } from '@lucide/vue'
import { shallowRef } from 'vue'

const props = defineProps<{
  submitting?: boolean
}>()

const emit = defineEmits<{
  submit: [magnetUri: string]
}>()

const magnetUri = shallowRef('')

function handleSubmit() {
  const trimmed = magnetUri.value.trim()
  if (!trimmed) return
  emit('submit', trimmed)
  magnetUri.value = ''
}
</script>

<template>
  <form class="magnet-form" @submit.prevent="handleSubmit">
    <input
      v-model="magnetUri"
      class="magnet-form-input"
      type="text"
      inputmode="url"
      autocomplete="off"
      placeholder="Paste a magnet link…"
      aria-label="Magnet link"
      :disabled="props.submitting"
    />
    <button
      class="magnet-form-submit"
      type="submit"
      :disabled="props.submitting || !magnetUri.trim()"
    >
      <Loader2 v-if="props.submitting" class="magnet-form-spinner" :size="16" aria-hidden="true" />
      <Plus v-else :size="16" aria-hidden="true" />
      {{ props.submitting ? 'Adding…' : 'Add Torrent' }}
    </button>
  </form>
</template>

<style scoped>
.magnet-form {
  display: flex;
  gap: 0.6rem;
}

.magnet-form-input {
  flex: 1;
  min-width: 0;
  height: 44px;
  padding: 0 0.9rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: 0.95rem;
  transition: border-color 150ms ease;
}

.magnet-form-input::placeholder {
  color: var(--color-text-faint);
}

.magnet-form-input:hover:not(:disabled) {
  border-color: rgba(255, 255, 255, 0.16);
}

.magnet-form-input:focus-visible {
  border-color: var(--color-accent-hover);
}

.magnet-form-input:disabled {
  opacity: 0.6;
}

.magnet-form-submit {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  height: 44px;
  padding: 0 1.1rem;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-accent);
  color: var(--color-accent-foreground);
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  transition:
    background-color 150ms ease,
    transform 150ms ease;
}

.magnet-form-submit:hover:not(:disabled) {
  background: var(--color-accent-hover);
}

.magnet-form-submit:active:not(:disabled) {
  background: var(--color-accent-active);
  transform: scale(0.97);
}

.magnet-form-submit:disabled {
  background: var(--color-secondary);
  color: var(--color-text-faint);
}

.magnet-form-spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
