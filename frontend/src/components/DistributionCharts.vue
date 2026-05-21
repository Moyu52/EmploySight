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
  return '#344b6e'
}

function render() {
  salaryChart.value?.setOption(salaryOption())
  educationChart.value?.setOption(pieOption('学历要求', props.analysis.education, 'left'))
  experienceChart.value?.setOption(pieOption('经验要求', props.analysis.experience, 'right'))
}

function salaryOption(): EChartsOption {
  const offset = pulse % props.analysis.salaryRanges.length
  const data = props.analysis.salaryRanges.map((item, index) => ({
    ...item,
    value: index === offset ? item.value + 3 : item.value
  }))
  return {
    grid: { left: 52, right: 16, top: 16, bottom: 30 },
    xAxis: {
      type: 'category',
      data: data.map((item) => item.name),
      axisLine: { lineStyle: { color: 'rgba(74, 101, 145, 0.34)' } },
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
      max: 70,
      interval: 10,
      splitLine: { lineStyle: { color: 'rgba(74, 101, 145, 0.16)' } },
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
            { offset: 0, color: '#d29a2e' },
            { offset: 0.48, color: '#2d5fbd' },
            { offset: 1, color: '#41a980' }
          ])
        }
      }
    ],
    animationDurationUpdate: 850,
    animationEasingUpdate: 'quarticOut'
  }
}

function pieOption(title: string, data: { name: string; value: number }[], titleSide: 'left' | 'right'): EChartsOption {
  const isRightChart = titleSide === 'right'
  return {
    title: {
      text: title,
      left: titleSide === 'left' ? 8 : undefined,
      right: titleSide === 'right' ? 8 : undefined,
      top: 4,
      textStyle: { color: '#13233d', fontSize: 12, fontWeight: 800 }
    },
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: ['39%', '62%'],
        center: [isRightChart ? '43%' : '48%', '58%'],
        padAngle: 2,
        data,
        label: {
          color: chartTextColor(),
          fontSize: 10,
          overflow: 'break',
          width: isRightChart ? 74 : 62
        },
        labelLayout: {
          hideOverlap: true,
          moveOverlap: 'shiftY'
        },
        labelLine: { length: 6, length2: isRightChart ? 4 : 6 },
        itemStyle: {
          borderWidth: 2,
          borderColor: '#f7fbff'
        },
        color: ['#2d5fbd', '#d29a2e', '#d86b4a', '#41a980', '#7b86d9'],
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

function resizeSoon() {
  window.requestAnimationFrame(resize)
}

onMounted(() => {
  if (salaryRef.value) salaryChart.value = echarts.init(salaryRef.value)
  if (educationRef.value) educationChart.value = echarts.init(educationRef.value)
  if (experienceRef.value) experienceChart.value = echarts.init(experienceRef.value)
  render()
  resizeSoon()
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
  grid-template-rows: minmax(9.5rem, 1.1fr) minmax(8rem, 0.9fr);
  gap: var(--space-sm);
  height: 100%;
  min-height: 0;
  padding: 0 var(--space-md) var(--space-md);
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
  border: 1px solid color-mix(in oklch, var(--line), transparent 68%);
  background: linear-gradient(145deg, color-mix(in oklch, var(--surface), white 3%), color-mix(in oklch, var(--panel), white 2%));
  box-shadow: inset 0 0 0 1px color-mix(in oklch, var(--line), transparent 80%);
}

.chart--salary,
.chart--pie {
  height: 100%;
}
</style>
