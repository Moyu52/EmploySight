<template>
  <div class="charts-grid">
    <div ref="salaryRef" class="chart chart--salary"></div>
    <div class="chart-pair">
      <div ref="educationRef" class="chart chart--pie"></div>
      <div ref="experienceRef" class="chart chart--pie"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import type { DashboardAnalysis } from '../types/dashboard'

const props = defineProps<{
  analysis: DashboardAnalysis
}>()

const salaryRef = ref<HTMLDivElement>()
const educationRef = ref<HTMLDivElement>()
const experienceRef = ref<HTMLDivElement>()
const salaryChart = shallowRef<ECharts>()
const educationChart = shallowRef<ECharts>()
const experienceChart = shallowRef<ECharts>()
let timer = 0
let pulse = 0

function chartTextColor() {
  return '#b7cdd2'
}

function render() {
  salaryChart.value?.setOption(salaryOption())
  educationChart.value?.setOption(pieOption('学历要求', props.analysis.education))
  experienceChart.value?.setOption(pieOption('经验要求', props.analysis.experience))
}

function salaryOption(): EChartsOption {
  const offset = pulse % props.analysis.salaryRanges.length
  const data = props.analysis.salaryRanges.map((item, index) => ({
    ...item,
    value: index === offset ? item.value + 3 : item.value
  }))
  return {
    grid: { left: 42, right: 14, top: 12, bottom: 24 },
    xAxis: {
      type: 'category',
      data: data.map((item) => item.name),
      axisLine: { lineStyle: { color: 'rgba(151, 203, 207, 0.24)' } },
      axisTick: { show: false },
      axisLabel: {
        color: chartTextColor(),
        fontSize: 10,
        interval: 0,
        margin: 10
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 40,
      interval: 10,
      splitLine: { lineStyle: { color: 'rgba(151, 203, 207, 0.13)' } },
      axisLabel: {
        color: chartTextColor(),
        fontSize: 10,
        margin: 8,
        formatter: (value: number) => `${value}%`
      }
    },
    series: [
      {
        name: '薪资区间',
        type: 'bar',
        data: data.map((item) => item.value),
        barWidth: 18,
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#e1b75c' },
            { offset: 1, color: '#45a8a3' }
          ])
        }
      }
    ],
    animationDurationUpdate: 850,
    animationEasingUpdate: 'quarticOut'
  }
}

function pieOption(title: string, data: { name: string; value: number }[]): EChartsOption {
  return {
    title: {
      text: title,
      left: 'center',
      top: 4,
      textStyle: { color: '#dbefff', fontSize: 12, fontWeight: 700 }
    },
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: ['42%', '68%'],
        center: ['50%', '58%'],
        padAngle: 2,
        data,
        label: {
          color: chartTextColor(),
          fontSize: 9,
          overflow: 'truncate',
          width: 44
        },
        labelLine: { length: 8, length2: 7 },
        itemStyle: {
          borderWidth: 2,
          borderColor: '#0c1b25'
        },
        color: ['#e1b75c', '#59c7bd', '#7aa1ff', '#cf7d5a', '#8ad38c'],
        animationDurationUpdate: 850,
        animationEasingUpdate: 'quarticOut'
      }
    ]
  }
}

function resize() {
  salaryChart.value?.resize()
  educationChart.value?.resize()
  experienceChart.value?.resize()
}

onMounted(() => {
  if (salaryRef.value) salaryChart.value = echarts.init(salaryRef.value)
  if (educationRef.value) educationChart.value = echarts.init(educationRef.value)
  if (experienceRef.value) experienceChart.value = echarts.init(experienceRef.value)
  render()
  timer = window.setInterval(() => {
    pulse += 1
    render()
  }, 3600)
  window.addEventListener('resize', resize)
})

watch(() => props.analysis, render, { deep: true })

onBeforeUnmount(() => {
  window.clearInterval(timer)
  window.removeEventListener('resize', resize)
  salaryChart.value?.dispose()
  educationChart.value?.dispose()
  experienceChart.value?.dispose()
})
</script>

<style scoped>
.charts-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-rows: minmax(6.5rem, 0.82fr) minmax(5.8rem, 0.64fr);
  gap: var(--space-xs);
  height: 100%;
  min-height: 0;
  padding: 0 var(--space-sm) var(--space-xs);
}

.chart-pair {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-xs);
  min-height: 0;
}

.chart {
  min-height: 0;
  border-radius: 6px;
  background: color-mix(in oklch, var(--surface), transparent 18%);
}

.chart--salary,
.chart--pie {
  height: 100%;
}
</style>
