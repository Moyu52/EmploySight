<template>
  <div class="metric-card">
    <div class="metric-card__icon">
      <component :is="iconComponent" :size="18" />
    </div>
    <div class="metric-card__body">
      <span>{{ label }}</span>
      <strong>{{ formatted }}</strong>
      <small>{{ suffix }}</small>
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
  border: 1px solid color-mix(in oklch, var(--line), transparent 24%);
  border-radius: 8px;
  background:
    linear-gradient(150deg, color-mix(in oklch, var(--panel-strong), transparent 4%), color-mix(in oklch, var(--surface), transparent 8%));
  contain: layout paint;
}

.metric-card__icon {
  display: grid;
  place-items: center;
  width: 2.3rem;
  height: 2.3rem;
  border-radius: 50%;
  color: var(--accent-warm);
  background: color-mix(in oklch, var(--accent-warm), transparent 88%);
  box-shadow: 0 0 1.4rem color-mix(in oklch, var(--accent-warm), transparent 78%);
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
  font-family: "Bahnschrift", "Microsoft YaHei UI", sans-serif;
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
</style>
