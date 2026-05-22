<template>
  <div class="skill-cloud">
    <button
      v-for="(item, index) in sortedSkills"
      :key="item.skill"
      class="skill-pill"
      :style="pillStyle(item, index)"
      type="button"
      :title="`${item.skill}：热度 ${item.heatIndex}，出现 ${item.frequency.toLocaleString('zh-CN')} 次`"
    >
      <span>{{ item.skill }}</span>
      <small>{{ item.category }}</small>
      <strong>{{ item.heatIndex }}</strong>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SkillKeyword } from '../types/dashboard'

const props = defineProps<{
  skills: SkillKeyword[]
}>()

const sortedSkills = computed(() => [...props.skills].sort((a, b) => b.heatIndex - a.heatIndex))

function pillStyle(item: SkillKeyword, index: number) {
  const heat = item.heatIndex
  const size = 0.86 + heat / 360
  const delay = `${index * 0.08}s`
  const highHeat = heat >= 93
  return {
    '--pill-size': `${size.toFixed(2)}rem`,
    '--pill-delay': delay,
    '--pill-alpha': `${Math.min(0.42, 0.16 + heat / 430)}`,
    '--pill-columns': highHeat ? 'span 2' : 'span 1'
  }
}
</script>

<style scoped>
.skill-cloud {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(6.2rem, 1fr));
  grid-auto-rows: minmax(3.8rem, 1fr);
  grid-auto-flow: dense;
  align-content: stretch;
  gap: var(--space-xs);
  height: 100%;
  min-height: 0;
  overflow: auto;
  padding: 0 var(--space-md) var(--space-sm);
  scrollbar-width: thin;
  scrollbar-color: color-mix(in oklch, var(--accent), transparent 42%) transparent;
}

.skill-pill {
  grid-column: var(--pill-columns);
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  grid-template-rows: 1fr auto;
  align-items: end;
  gap: 0.12rem var(--space-xs);
  min-width: 0;
  min-height: 3.8rem;
  padding: var(--space-xs) var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 56%);
  border-left: 3px solid color-mix(in oklch, var(--official-blue), transparent 28%);
  border-radius: 7px;
  color: var(--text);
  background:
    linear-gradient(135deg, color-mix(in oklch, var(--official-blue-soft), white 2%), color-mix(in oklch, var(--panel), white 2%)),
    color-mix(in oklch, var(--official-blue), transparent calc(100% - (var(--pill-alpha) * 35%)));
  box-shadow: 0 0.45rem 1rem rgba(20, 52, 99, 0.06);
  cursor: default;
  overflow: hidden;
  transition: border-color 180ms var(--ease-out-quint), transform 180ms var(--ease-out-quint);
}

.skill-pill:hover {
  border-color: color-mix(in oklch, var(--official-blue), transparent 28%);
  transform: translateY(-1px);
}

.skill-pill span {
  grid-column: 1 / -1;
  min-width: 0;
  color: var(--official-blue-deep);
  font-size: var(--pill-size);
  font-weight: 800;
  line-height: 1.05;
  overflow-wrap: anywhere;
}

.skill-pill small {
  color: var(--text-muted);
  font-size: 0.66rem;
}

.skill-pill strong {
  color: var(--official-blue);
  font-size: 0.72rem;
  font-variant-numeric: tabular-nums;
}

@media (max-height: 820px) {
  .skill-cloud {
    grid-template-columns: repeat(auto-fit, minmax(5rem, 1fr));
    grid-auto-rows: minmax(3.2rem, 1fr);
    gap: 0.35rem;
    padding: 0 var(--space-sm) var(--space-xs);
  }

  .skill-pill {
    min-height: 3.2rem;
    padding: 0.35rem 0.5rem;
  }

  .skill-pill span {
    font-size: calc(var(--pill-size) * 0.86);
  }

  .skill-pill small,
  .skill-pill strong {
    font-size: 0.58rem;
  }
}
</style>
