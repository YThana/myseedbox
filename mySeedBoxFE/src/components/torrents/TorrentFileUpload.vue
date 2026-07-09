<script setup lang="ts">
import { Loader2, Upload } from '@lucide/vue'
import { shallowRef, useTemplateRef } from 'vue'

const props = defineProps<{
  uploading?: boolean
}>()

const emit = defineEmits<{
  upload: [file: File]
}>()

const inputRef = useTemplateRef<HTMLInputElement>('input')
const isDragging = shallowRef(false)
const localError = shallowRef<string | null>(null)

function openPicker() {
  if (props.uploading) return
  inputRef.value?.click()
}

function handleDragEnter() {
  if (props.uploading) return
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  if (props.uploading) return
  processFile(event.dataTransfer?.files?.[0])
}

function handleChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  processFile(file)
}

function processFile(file: File | undefined) {
  if (!file) return
  if (!file.name.toLowerCase().endsWith('.torrent')) {
    localError.value = `"${file.name}" isn't a .torrent file`
    return
  }
  localError.value = null
  emit('upload', file)
}
</script>

<template>
  <div
    class="dropzone"
    :class="{ 'dropzone-active': isDragging, 'dropzone-disabled': props.uploading }"
    role="button"
    tabindex="0"
    aria-label="Add a torrent by uploading a .torrent file"
    @dragenter.prevent="handleDragEnter"
    @dragover.prevent
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    @click="openPicker"
    @keydown.enter="openPicker"
    @keydown.space.prevent="openPicker"
  >
    <div class="dropzone-content">
      <Loader2 v-if="props.uploading" class="dropzone-spinner" :size="18" aria-hidden="true" />
      <Upload v-else :size="18" aria-hidden="true" />
      <p class="dropzone-text">
        <template v-if="props.uploading">Uploading…</template>
        <template v-else>Drag &amp; drop a <strong>.torrent</strong> file, or click to browse</template>
      </p>
    </div>
  </div>
  <p v-if="localError" class="dropzone-error" role="alert">{{ localError }}</p>
  <input
    ref="input"
    class="upload-input"
    type="file"
    accept=".torrent"
    aria-hidden="true"
    tabindex="-1"
    @change="handleChange"
  />
</template>

<style scoped>
.dropzone {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 72px;
  padding: 0.75rem 1rem;
  border: 1.5px dashed var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text-muted);
  cursor: pointer;
  transition:
    background-color 150ms ease,
    border-color 150ms ease,
    color 150ms ease;
}

.dropzone:hover:not(.dropzone-disabled) {
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--color-text);
}

.dropzone-active {
  border-color: var(--color-accent-hover);
  background: rgba(4, 120, 87, 0.1);
  color: var(--color-text);
}

.dropzone-disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.dropzone-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none;
}

.dropzone-text {
  margin: 0;
  font-size: 0.85rem;
}

.dropzone-text strong {
  color: var(--color-text);
  font-weight: 600;
}

.dropzone-spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.dropzone-error {
  margin: 0.4rem 0 0;
  color: #f87171;
  font-size: 0.82rem;
}

.upload-input {
  display: none;
}
</style>
