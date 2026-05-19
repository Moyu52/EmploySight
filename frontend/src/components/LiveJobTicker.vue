<template>
  <div class="live-ticker">
    <div class="live-ticker__track">
      <article v-for="(item, index) in loopItems" :key="`${item.time}-${item.title}-${index}`" class="job-row">
        <time>{{ item.time }}</time>
        <strong>{{ item.city }}</strong>
        <div>
          <b>{{ item.title }}</b>
          <span>{{ item.company }}</span>
        </div>
        <em>{{ item.salary }}</em>
        <small>{{ item.skills }}</small>
      </article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { JobLiveItem } from '../types/dashboard'

const props = defineProps<{
  jobs: JobLiveItem[]
}>()

const loopItems = computed(() => [...props.jobs, ...props.jobs])
</script>

<style scoped>
.live-ticker {
  position: relative;
  z-index: 1;
  overflow: hidden;
  height: 100%;
  min-height: 0;
  padding: 0 var(--space-sm) var(--space-sm);
  mask-image: linear-gradient(180deg, transparent, black 10%, black 88%, transparent);
}

.live-ticker__track {
  display: grid;
  gap: var(--space-xs);
  animation: live-scroll 16s linear infinite;
}

.live-ticker:hover .live-ticker__track {
  animation-play-state: paused;
}

.job-row {
  display: grid;
  grid-template-columns: 3rem 3.2rem minmax(0, 1fr) 4.2rem 6rem;
  align-items: center;
  gap: var(--space-xs);
  min-height: 2.08rem;
  padding: 0 var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 48%);
  border-radius: 6px;
  background: color-mix(in oklch, var(--surface), transparent 16%);
}

.job-row time {
  color: var(--accent);
  font-size: 0.74rem;
  font-variant-numeric: tabular-nums;
}

.job-row strong {
  color: var(--accent-warm);
  font-size: 0.78rem;
}

.job-row div {
  display: grid;
  min-width: 0;
}

.job-row b,
.job-row span,
.job-row small {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.job-row b {
  color: var(--text);
  font-size: 0.78rem;
}

.job-row span,
.job-row small {
  color: var(--text-muted);
  font-size: 0.66rem;
}

.job-row em {
  color: var(--text-strong);
  font-size: 0.78rem;
  font-style: normal;
  text-align: right;
}

@keyframes live-scroll {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-50%);
  }
}
</style>
