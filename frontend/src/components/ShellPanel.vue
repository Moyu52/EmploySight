<template>
  <section class="shell-panel" :class="{ dense }">
    <header v-if="title || subtitle" class="shell-panel__header">
      <div>
        <p v-if="eyebrow" class="shell-panel__eyebrow">{{ eyebrow }}</p>
        <h2 v-if="title">{{ title }}</h2>
      </div>
      <span v-if="subtitle" class="shell-panel__subtitle">{{ subtitle }}</span>
    </header>
    <div class="shell-panel__body">
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
  subtitle?: string
  eyebrow?: string
  dense?: boolean
}>()
</script>

<style scoped>
.shell-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 8px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 1%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: var(--shadow-panel);
  min-width: 0;
}

.shell-panel::after {
  content: none;
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(90deg, transparent, color-mix(in oklch, var(--accent), transparent 86%), color-mix(in oklch, var(--accent-warm), transparent 90%), transparent);
  opacity: 0.42;
  transform: translateX(-100%);
  animation: scan-panel 7s var(--ease-out-quint) infinite;
  contain: paint;
}

.shell-panel__header {
  flex: 0 0 auto;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-md);
  padding: var(--space-md) var(--space-md) var(--space-sm);
  border-bottom: 1px solid color-mix(in oklch, var(--line), transparent 70%);
}

.shell-panel__body {
  position: relative;
  z-index: 1;
  flex: 1 1 auto;
  min-height: 0;
}

.dense .shell-panel__header {
  padding-bottom: var(--space-xs);
}

.shell-panel__eyebrow,
.shell-panel__subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.72rem;
}

.shell-panel__eyebrow {
  letter-spacing: 0;
}

.shell-panel h2 {
  margin: 0.1rem 0 0;
  color: var(--text-strong);
  font-size: 1rem;
  font-weight: 800;
}

@keyframes scan-panel {
  0%,
  32% {
    transform: translateX(-100%);
  }
  58%,
  100% {
    transform: translateX(100%);
  }
}
</style>
