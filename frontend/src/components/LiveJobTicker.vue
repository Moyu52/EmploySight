<template>
  <div class="live-ticker">
    <div class="live-ticker__track" :class="{ 'is-looping': shouldLoop }">
      <article v-for="(item, index) in loopJobs" :key="`${item.time}-${item.title}-${index}`" class="job-row">
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

const shouldLoop = computed(() => props.jobs.length > 3)
const loopJobs = computed(() => shouldLoop.value ? [...props.jobs, ...props.jobs] : props.jobs)
</script>

<style scoped>
.live-ticker {
  position: relative;
  z-index: 1;
  overflow: hidden;
  height: 100%;
  min-height: 0;
  max-height: none;
  padding: 0 var(--space-sm) var(--space-sm);
  mask-image: linear-gradient(180deg, transparent, black 12%, black 88%, transparent);
}

.live-ticker__track {
  display: grid;
  gap: var(--space-xs);
}

.live-ticker__track.is-looping {
  animation: job-scroll 22s linear infinite;
  will-change: transform;
}

.live-ticker:hover .live-ticker__track.is-looping {
  animation-play-state: paused;
}

.job-row {
  display: grid;
  grid-template-columns: 3rem 3.2rem minmax(0, 1fr) 4.2rem 6rem;
  align-items: center;
  gap: var(--space-xs);
  min-height: 2.08rem;
  padding: 0 var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 38%);
  border-left: 3px solid color-mix(in oklch, var(--official-blue), transparent 32%);
  border-radius: 6px;
  background: color-mix(in oklch, var(--panel), white 1%);
}

.job-row time {
  color: var(--official-blue);
  font-size: 0.74rem;
  font-variant-numeric: tabular-nums;
}

.job-row strong {
  color: var(--official-gold);
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
  color: var(--official-blue-deep);
  font-size: 0.78rem;
  font-weight: 800;
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
  font-weight: 700;
}

@keyframes job-scroll {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-50%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .live-ticker__track.is-looping {
    animation: none;
  }
}
</style>
