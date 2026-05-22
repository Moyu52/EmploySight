<template>
  <div class="metric-card" :class="{ 'metric-card--prominent': prominent }">
    <div class="metric-card__icon">
      <component :is="iconComponent" :size="prominent ? 23 : 18" />
    </div>
    <div class="metric-card__body">
      <span>{{ label }}</span>
      <strong>{{ formatted }}</strong>
      <small>{{ suffix }}</small>
      <em v-if="detail">{{ detail }}</em>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, toRef } from 'vue'
import { BadgeCent, Building2, GraduationCap, MapPinned } from 'lucide-vue-next'
import { useAnimatedNumber } from '../composables/useAnimatedNumber'

const props = defineProps<{
  label: string
  value: number
  suffix?: string
  detail?: string
  icon: 'jobs' | 'salary' | 'city' | 'fresh'
  decimals?: number
  prominent?: boolean
}>()

const iconMap = {
  jobs: Building2,
  salary: BadgeCent,
  city: MapPinned,
  fresh: GraduationCap
}

const animated = useAnimatedNumber(toRef(props, 'value'))
const iconComponent = computed(() => iconMap[props.icon])
const formatted = computed(() => {
  const decimals = props.decimals ?? 0
  return animated.value.toLocaleString('zh-CN', {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals
  })
})
</script>

<style scoped>
.metric-card {
  position: relative;
  display: grid;
  grid-template-columns: 2.6rem 1fr;
  align-items: center;
  gap: var(--space-sm);
  min-height: 5.35rem;
  padding: var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 42%);
  border-left: 3px solid color-mix(in oklch, var(--official-blue), transparent 24%);
  border-radius: 8px;
  background: linear-gradient(180deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: 0 0.55rem 1.3rem rgba(20, 52, 99, 0.06);
  contain: layout paint;
  overflow: hidden;
}

.metric-card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 1px;
  background: linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 76%), transparent);
}

.metric-card__icon {
  display: grid;
  place-items: center;
  width: 2.3rem;
  height: 2.3rem;
  border-radius: 8px;
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 76%);
  color: var(--official-blue);
  background: linear-gradient(135deg, color-mix(in oklch, var(--official-blue-soft), white 4%), var(--panel));
  box-shadow: inset 0 1px 0 color-mix(in oklch, white, transparent 18%);
}

.metric-card__body {
  display: grid;
  min-width: 0;
}

.metric-card span {
  color: var(--text-muted);
  font-size: 0.74rem;
  font-weight: 700;
}

.metric-card strong {
  overflow: hidden;
  color: var(--official-blue-deep);
  font-size: 1.5rem;
  line-height: 1.05;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.metric-card small {
  color: var(--official-blue);
  font-size: 0.72rem;
  font-weight: 700;
}

.metric-card em {
  color: var(--text-muted);
  font-size: 0.64rem;
  font-style: normal;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.metric-card--prominent {
  grid-template-columns: 3.6rem minmax(0, 1fr);
  gap: 1rem;
  min-height: 100%;
  padding: 1.25rem;
}

.metric-card--prominent .metric-card__icon {
  width: 3rem;
  height: 3rem;
  border-radius: 10px;
}

.metric-card--prominent .metric-card__body {
  gap: 0.12rem;
}

.metric-card--prominent span {
  color: color-mix(in oklch, var(--text-muted), var(--official-blue-deep) 12%);
  font-size: 0.95rem;
  font-weight: 800;
}

.metric-card--prominent strong {
  font-size: clamp(2rem, 2.2vw, 2.65rem);
  line-height: 1;
}

.metric-card--prominent small {
  font-size: 0.92rem;
}

.metric-card--prominent em {
  font-size: 0.78rem;
}

@media (max-width: 760px) {
  .metric-card--prominent {
    grid-template-columns: 3rem minmax(0, 1fr);
    padding: var(--space-md);
  }

  .metric-card--prominent .metric-card__icon {
    width: 2.6rem;
    height: 2.6rem;
  }

  .metric-card--prominent strong {
    font-size: 1.8rem;
  }
}
</style>
