<template>
  <div class="auto-rank">
    <div class="auto-rank__track" :class="{ 'is-looping': shouldLoop }" :style="{ animationDuration: `${duration}s` }">
      <div v-for="(item, index) in loopItems" :key="`${item.name}-${index}`" class="rank-row">
        <span class="rank-row__no">{{ rankNo(index) }}</span>
        <div class="rank-row__main">
          <div class="rank-row__title">
            <b>{{ item.name }}</b>
            <em>{{ item.tag }}</em>
          </div>
          <div class="rank-row__bar">
            <i :style="{ width: `${Math.min(item.score, 100)}%` }"></i>
          </div>
        </div>
        <strong>{{ formatValue(item.value) }}</strong>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { RankItem } from '../types/dashboard'

const props = withDefaults(defineProps<{
  items: RankItem[]
  duration?: number
}>(), {
  duration: 18
})

const shouldLoop = computed(() => props.items.length > 4)
const loopItems = computed(() => shouldLoop.value ? [...props.items, ...props.items] : props.items)

function rankNo(index: number) {
  return props.items.length > 0 ? (index % props.items.length) + 1 : index + 1
}

function formatValue(value: number) {
  if (value >= 10000) {
    return `${(value / 10000).toFixed(1)}万`
  }
  return value.toLocaleString('zh-CN')
}
</script>

<style scoped>
.auto-rank {
  position: relative;
  z-index: 1;
  overflow: hidden;
  height: 100%;
  min-height: 0;
  padding: 0 var(--space-md) var(--space-sm);
  mask-image: linear-gradient(180deg, transparent, black 10%, black 90%, transparent);
}

.auto-rank__track {
  display: grid;
  gap: var(--space-xs);
}

.auto-rank__track.is-looping {
  animation: rank-scroll linear infinite;
  will-change: transform;
}

.auto-rank:hover .auto-rank__track.is-looping {
  animation-play-state: paused;
}

.rank-row {
  display: grid;
  grid-template-columns: 1.8rem 1fr 3.8rem;
  align-items: center;
  gap: var(--space-xs);
  min-height: 2.34rem;
  padding: 0 var(--space-xs);
  border: 1px solid color-mix(in oklch, var(--line), transparent 42%);
  border-radius: 6px;
  background: color-mix(in oklch, var(--surface), transparent 16%);
}

.rank-row__no {
  display: grid;
  place-items: center;
  width: 1.45rem;
  height: 1.45rem;
  border-radius: 50%;
  color: var(--text-strong);
  background: color-mix(in oklch, var(--accent), transparent 74%);
  font-size: 0.74rem;
  font-variant-numeric: tabular-nums;
}

.rank-row__main {
  display: grid;
  gap: 0.22rem;
  min-width: 0;
}

.rank-row__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-xs);
  min-width: 0;
}

.rank-row b {
  overflow: hidden;
  color: var(--text);
  font-size: 0.8rem;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rank-row em {
  color: var(--text-muted);
  font-size: 0.68rem;
  font-style: normal;
  white-space: nowrap;
}

.rank-row strong {
  color: var(--accent-warm);
  font-size: 0.78rem;
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.rank-row__bar {
  overflow: hidden;
  height: 0.22rem;
  border-radius: 999px;
  background: color-mix(in oklch, var(--line), transparent 60%);
}

.rank-row__bar i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--accent-warm));
  transform-origin: left center;
  animation: bar-in 900ms var(--ease-out-quint) both;
}

@keyframes bar-in {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

@keyframes rank-scroll {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-50%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .auto-rank__track.is-looping {
    animation: none;
  }
}
</style>
