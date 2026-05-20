<template>
  <div class="metric-card">
    <div class="metric-card__icon">
      <component :is="iconComponent" :size="18" />
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
  min-height: 5.2rem;
  padding: var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 8px;
  background: linear-gradient(150deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 3%));
  box-shadow: 0 0.55rem 1.4rem rgba(42, 60, 95, 0.07);
  contain: layout paint;
  overflow: hidden;
}

.metric-card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 1px;
  background: linear-gradient(90deg, color-mix(in oklch, var(--accent), transparent 44%), transparent);
}

.metric-card__icon {
  display: grid;
  place-items: center;
  width: 2.3rem;
  height: 2.3rem;
  border-radius: 8px;
  color: oklch(98% 0.006 250);
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent), black 12%));
  box-shadow: 0 0.45rem 0.95rem color-mix(in oklch, var(--accent), transparent 82%);
}

.metric-card__body {
  display: grid;
  min-width: 0;
}

.metric-card span {
  color: var(--text-muted);
  font-size: 0.74rem;
}

.metric-card strong {
  overflow: hidden;
  color: var(--text-strong);
  font-size: 1.45rem;
  line-height: 1.05;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.metric-card small {
  color: var(--accent);
  font-size: 0.72rem;
}

.metric-card em {
  color: var(--text-muted);
  font-size: 0.64rem;
  font-style: normal;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
