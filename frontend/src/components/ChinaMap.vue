<template>
  <div class="map-wrap">
    <div ref="chartRef" class="map-chart" @click="handleFallbackClick"></div>
    <div class="province-card">
      <span>当前聚焦省份</span>
      <strong>{{ activeProvince?.province ?? '全国' }}</strong>
      <div class="province-card__grid">
        <p>
          <b>{{ activeProvince?.jobCount.toLocaleString('zh-CN') ?? '-' }}</b>
          <em>岗位数</em>
        </p>
        <p>
          <b>{{ activeProvince?.avgSalary ?? '-' }}</b>
          <em>平均薪资</em>
        </p>
        <p>
          <b>{{ activeProvince?.freshFriendlyIndex ?? '-' }}</b>
          <em>应届友好</em>
        </p>
        <p>
          <b>{{ activeProvince?.heatIndex ?? '-' }}</b>
          <em>热度指数</em>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import type { CityMetric, ProvinceMetric } from '../types/dashboard'
import chinaGeoJson from '../assets/china.geo.json'

const props = defineProps<{
  provinces: ProvinceMetric[]
  cities: CityMetric[]
}>()

const emit = defineEmits<{
  provinceChange: [province: ProvinceMetric]
}>()

const chartRef = ref<HTMLDivElement>()
const chart = shallowRef<echarts.ECharts>()
const activeIndex = ref(0)
let timer = 0

const activeProvince = computed(() => props.provinces[activeIndex.value])

function buildOption(): EChartsOption {
  const maxHeat = Math.max(...props.provinces.map((item) => item.heatIndex), 100)
  const mapData = props.provinces.map((item) => ({
    name: item.province,
    value: item.heatIndex,
    jobCount: item.jobCount,
    avgSalary: item.avgSalary,
    freshFriendlyIndex: item.freshFriendlyIndex,
    topIndustry: item.topIndustry
  }))

  const hotCities = props.cities.map((item) => ({
    name: item.city,
    value: [item.longitude, item.latitude, item.attractionIndex],
    jobCount: item.jobCount,
    avgSalary: item.avgSalary
  }))

  const flowTargets = props.cities.slice(1, 8).map((item) => ({
    coords: [
      [props.cities[0].longitude, props.cities[0].latitude],
      [item.longitude, item.latitude]
    ],
    value: item.attractionIndex
  }))

  return {
    animation: true,
    animationDurationUpdate: 900,
    animationEasingUpdate: 'quarticOut',
    tooltip: {
      trigger: 'item',
      borderWidth: 0,
      backgroundColor: 'rgba(11, 25, 34, 0.92)',
      textStyle: { color: '#dbefff' },
      formatter: (params: any) => {
        if (params.seriesType === 'map') {
          return `${params.name}<br/>就业热度：${params.value ?? '-'}<br/>岗位数：${params.data?.jobCount?.toLocaleString?.('zh-CN') ?? '-'}<br/>平均薪资：${params.data?.avgSalary ?? '-'} 元<br/>应届友好：${params.data?.freshFriendlyIndex ?? '-'}`
        }
        if (params.seriesType === 'effectScatter') {
          return `${params.name}<br/>吸引力：${params.value[2]}<br/>岗位数：${params.data.jobCount.toLocaleString('zh-CN')}`
        }
        return params.name
      }
    },
    visualMap: {
      min: 60,
      max: maxHeat,
      show: false,
      inRange: {
        color: ['#173345', '#246f6d', '#d7a84f']
      }
    },
    geo: {
      map: 'china-employment',
      roam: false,
      zoom: 1.34,
      center: [112.4, 36.2],
      itemStyle: {
        areaColor: 'rgba(24, 80, 91, 0.46)',
        borderColor: 'rgba(147, 221, 216, 0.65)',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: '#d6a84e',
          shadowBlur: 24,
          shadowColor: 'rgba(215, 168, 79, 0.55)'
        },
        label: {
          color: '#f7fbff',
          fontWeight: 700
        }
      },
      label: {
        show: true,
        color: 'rgba(222, 243, 245, 0.76)',
        fontSize: 11
      }
    },
    series: [
      {
        type: 'map',
        map: 'china-employment',
        geoIndex: 0,
        data: mapData
      },
      {
        name: '城市热点',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: hotCities,
        symbolSize: (value: number[]) => Math.max(8, value[2] / 6),
        rippleEffect: {
          brushType: 'stroke',
          scale: 4.5,
          period: 4
        },
        itemStyle: {
          color: '#f0b54d',
          shadowBlur: 18,
          shadowColor: 'rgba(240, 181, 77, 0.8)'
        },
        zlevel: 3
      },
      {
        name: '就业流向',
        type: 'lines',
        coordinateSystem: 'geo',
        data: flowTargets,
        effect: {
          show: true,
          period: 5,
          trailLength: 0.18,
          symbol: 'arrow',
          symbolSize: 8
        },
        lineStyle: {
          width: 1.2,
          color: '#78d8d4',
          opacity: 0.36,
          curveness: 0.22
        },
        zlevel: 2
      }
    ]
  }
}

function render() {
  if (!chart.value || props.provinces.length === 0) {
    return
  }
  chart.value.setOption(buildOption())
}

function focusProvince(index: number) {
  if (!chart.value || props.provinces.length === 0) {
    return
  }
  const previous = activeIndex.value
  activeIndex.value = index % props.provinces.length
  chart.value.dispatchAction({ type: 'downplay', seriesIndex: 0, dataIndex: previous })
  chart.value.dispatchAction({ type: 'highlight', seriesIndex: 0, dataIndex: activeIndex.value })
  chart.value.dispatchAction({ type: 'hideTip' })
  if (activeProvince.value) {
    emit('provinceChange', activeProvince.value)
  }
}

function startLoop() {
  window.clearInterval(timer)
  timer = window.setInterval(() => focusProvince(activeIndex.value + 1), 3200)
}

function handleFallbackClick() {
  focusProvince(activeIndex.value + 1)
}

onMounted(() => {
  if (!chartRef.value) {
    return
  }
  echarts.registerMap('china-employment', chinaGeoJson as any)
  chart.value = echarts.init(chartRef.value)
  chart.value.on('click', (params) => {
    const index = props.provinces.findIndex((item) => item.province === params.name)
    if (index >= 0) {
      focusProvince(index)
    }
  })
  render()
  focusProvince(0)
  startLoop()
  window.addEventListener('resize', resize)
})

watch(() => [props.provinces, props.cities], render, { deep: true })

function resize() {
  chart.value?.resize()
}

onBeforeUnmount(() => {
  window.clearInterval(timer)
  window.removeEventListener('resize', resize)
  chart.value?.dispose()
})
</script>

<style scoped>
.map-wrap {
  position: relative;
  z-index: 1;
  height: 100%;
  min-height: 0;
  padding: 0 var(--space-md) var(--space-md);
}

.map-wrap::after {
  content: "";
  position: absolute;
  right: 0;
  bottom: 0;
  z-index: 5;
  width: min(23rem, 45%);
  height: min(16rem, 42%);
  pointer-events: none;
  background: radial-gradient(ellipse at 76% 78%, color-mix(in oklch, var(--panel), black 8%) 0%, color-mix(in oklch, var(--panel), transparent 18%) 42%, transparent 76%);
}

.map-chart {
  width: 100%;
  height: 100%;
  min-height: 0;
}

.province-card {
  position: absolute;
  z-index: 6;
  right: calc(var(--space-md) + 0.25rem);
  bottom: calc(var(--space-md) + 0.25rem);
  width: min(18.25rem, calc(100% - 2.5rem));
  padding: var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--accent), transparent 58%);
  border-radius: 8px;
  background:
    linear-gradient(135deg, color-mix(in oklch, var(--surface), black 8%), color-mix(in oklch, var(--panel), black 4%));
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.36), 0 0 0 1px rgba(255, 255, 255, 0.04) inset;
  backdrop-filter: blur(10px);
}

.province-card span,
.province-card em {
  color: var(--text-muted);
  font-size: 0.74rem;
  font-style: normal;
}

.province-card strong {
  display: block;
  margin-top: 0.15rem;
  color: var(--text-strong);
  font-size: 1.22rem;
}

.province-card__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-xs);
  margin-top: var(--space-xs);
}

.province-card p {
  display: grid;
  gap: 0.15rem;
  margin: 0;
}

.province-card b {
  color: var(--accent-warm);
  font-size: 0.92rem;
  font-variant-numeric: tabular-nums;
}
</style>
