<template>
  <div class="skill-cloud">
    <button
      v-for="(item, index) in skills"
      :key="item.skill"
      class="skill-pill"
      :style="pillStyle(item.heatIndex, index)"
      type="button"
      :title="`${item.skill}：热度 ${item.heatIndex}`"
    >
      <span>{{ item.skill }}</span>
      <small>{{ item.category }}</small>
    </button>
  </div>
</template>

<script setup lang="ts">
import type { SkillKeyword } from '../types/dashboard'

defineProps<{
  skills: SkillKeyword[]
}>()

function pillStyle(heat: number, index: number) {
  const scale = 0.86 + heat / 420
  const delay = `${index * 0.18}s`
  return {
    '--pill-scale': scale.toFixed(2),
    '--pill-delay': delay,
    '--pill-alpha': `${Math.min(0.34, 0.14 + heat / 480)}`
  }
}
</script>

<style scoped>
.skill-cloud {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  gap: var(--space-xs);
  height: 100%;
  min-height: 0;
  overflow: auto;
  padding: 0 var(--space-md) var(--space-sm);
  scrollbar-width: thin;
  scrollbar-color: color-mix(in oklch, var(--accent), transparent 42%) transparent;
}

.skill-pill {
  display: inline-grid;
  grid-template-columns: auto;
  gap: 0.1rem;
  min-width: 4.9rem;
  padding: 0.38rem 0.54rem;
  border: 1px solid color-mix(in oklch, var(--accent), transparent 48%);
  border-radius: 999px;
  color: var(--text);
  background:
    radial-gradient(circle at 20% 0%, color-mix(in oklch, var(--accent-warm), transparent 76%), transparent 70%),
    color-mix(in oklch, var(--accent), transparent calc(100% - (var(--pill-alpha) * 100%)));
  cursor: default;
  transform: scale(var(--pill-scale));
  transform-origin: center;
  animation: skill-float 4.8s var(--ease-out-quint) infinite;
  animation-delay: var(--pill-delay);
}

.skill-pill span {
  font-size: 0.76rem;
  font-weight: 700;
  line-height: 1;
}

.skill-pill small {
  color: var(--text-muted);
  font-size: 0.58rem;
}

@keyframes skill-float {
  0%,
  100% {
    transform: translateY(0) scale(var(--pill-scale));
  }
  50% {
    transform: translateY(-0.32rem) scale(var(--pill-scale));
  }
}
</style>
