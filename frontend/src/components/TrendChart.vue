<template>
  <div ref="chartRef" class="trend-chart"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption, LineSeriesOption } from 'echarts'
import type { TrendPoint } from '../types/dashboard'

const props = defineProps<{
  trends: TrendPoint[]
}>()

const chartRef = ref<HTMLDivElement>()
const chart = shallowRef<ECharts>()
const activeWindow = ref(8)
let timer = 0

function option(): EChartsOption {
  const start = Math.max(0, props.trends.length - activeWindow.value)
  const view = props.trends.slice(start)
  const colors = ['#e1b75c', '#5fd0c8', '#cf7d5a']
  return {
    color: colors,
    grid: { left: 46, right: 18, top: 24, bottom: 28 },
    legend: {
      right: 8,
      top: 0,
      textStyle: { color: '#a9bec4', fontSize: 10 },
      itemWidth: 12,
      itemHeight: 8
    },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: view.map((item) => item.month.slice(5)),
      axisLine: { lineStyle: { color: 'rgba(151, 203, 207, 0.24)' } },
      axisTick: { show: false },
      axisLabel: { color: '#a9bec4', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#a9bec4',
        fontSize: 10,
        formatter: (value: number) => `${Math.round(value / 10000)}万`
      },
      splitLine: { lineStyle: { color: 'rgba(151, 203, 207, 0.13)' } }
    },
    series: [
      line('岗位总量', view.map((item) => item.jobs), colors[0]),
      line('应届岗位', view.map((item) => item.freshJobs), colors[1]),
      line('算法/AI岗位', view.map((item) => item.aiJobs), colors[2])
    ],
    animationDurationUpdate: 850,
    animationEasingUpdate: 'quarticOut'
  }
}

function line(name: string, data: number[], color: string): LineSeriesOption {
  return {
    name,
    type: 'line',
    smooth: true,
    showSymbol: false,
    data,
    color,
    itemStyle: { color },
    lineStyle: { width: 2, color },
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: `${color}55` },
        { offset: 1, color: `${color}05` }
      ])
    }
  }
}

function render() {
  chart.value?.setOption(option())
}

function resize() {
  chart.value?.resize()
}

onMounted(() => {
  if (chartRef.value) {
    chart.value = echarts.init(chartRef.value)
  }
  render()
  timer = window.setInterval(() => {
    activeWindow.value = activeWindow.value >= props.trends.length ? 7 : activeWindow.value + 1
    render()
  }, 3200)
  window.addEventListener('resize', resize)
})

watch(() => props.trends, render, { deep: true })

onBeforeUnmount(() => {
  window.clearInterval(timer)
  window.removeEventListener('resize', resize)
  chart.value?.dispose()
})
</script>

<style scoped>
.trend-chart {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  min-height: 0;
}
</style>
