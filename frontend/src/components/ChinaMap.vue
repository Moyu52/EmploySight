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

  const mappableCities = props.cities.filter((item) => item.hasCoords && item.longitude && item.latitude)
  const hotCities = mappableCities.map((item) => ({
    name: item.city,
    value: [item.longitude, item.latitude, item.attractionIndex],
    jobCount: item.jobCount,
    avgSalary: item.avgSalary
  }))

  const flowTargets = mappableCities.slice(1, 8).map((item) => ({
    coords: [
      [mappableCities[0].longitude, mappableCities[0].latitude],
      [item.longitude, item.latitude]
    ],
    value: item.attractionIndex
  })).filter(() => mappableCities.length > 1)

  return {
    animation: true,
    animationDurationUpdate: 900,
    animationEasingUpdate: 'quarticOut',
    tooltip: {
      trigger: 'item',
      borderWidth: 1,
      borderColor: 'rgba(75, 102, 145, 0.34)',
      backgroundColor: 'rgba(255, 255, 255, 0.96)',
      textStyle: { color: '#13233d' },
      extraCssText: 'box-shadow: 0 18px 38px rgba(42, 60, 95, 0.16); backdrop-filter: blur(8px);',
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
        color: ['#eef5ff', '#bfd2ed', '#6f99d4', '#d7b45d']
      }
    },
    geo: {
      map: 'china-employment',
      roam: false,
      layoutCenter: ['43%', '44%'],
      layoutSize: '90%',
      zoom: 1.08,
      center: [105.8, 36.2],
      itemStyle: {
        areaColor: 'rgba(198, 218, 242, 0.84)',
        borderColor: 'rgba(72, 111, 166, 0.46)',
        borderWidth: 1.08,
        shadowBlur: 8,
        shadowColor: 'rgba(36, 76, 133, 0.1)'
      },
      emphasis: {
        itemStyle: {
          areaColor: '#dfbd68',
          shadowBlur: 16,
          shadowColor: 'rgba(201, 149, 45, 0.28)'
        },
        label: {
          color: '#071326',
          fontWeight: 900,
          textBorderColor: 'rgba(255, 244, 199, 0.94)',
          textBorderWidth: 2,
          textShadowBlur: 0
        }
      },
      label: {
        show: true,
        color: 'rgba(20, 35, 61, 0.86)',
        fontSize: 11,
        textBorderColor: 'rgba(255, 255, 255, 0.94)',
        textBorderWidth: 3,
        textShadowBlur: 0
      }
    },
    series: [
      {
        type: 'map',
        map: 'china-employment',
        geoIndex: 0,
        data: mapData,
        emphasis: {
          label: {
            color: '#071326',
            fontWeight: 900,
            textBorderColor: 'rgba(255, 244, 199, 0.94)',
            textBorderWidth: 2,
            textShadowBlur: 0
          }
        }
      },
      {
        name: '城市热点',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: hotCities,
        symbolSize: (value: number[]) => Math.max(6, value[2] / 8),
        rippleEffect: {
          brushType: 'stroke',
          scale: 3.4,
          period: 4.8
        },
        itemStyle: {
          color: 'rgba(215, 180, 93, 0.78)',
          shadowBlur: 6,
          shadowColor: 'rgba(201, 149, 45, 0.2)'
        },
        zlevel: 2
      },
      {
        name: '就业流向光轨',
        type: 'lines',
        coordinateSystem: 'geo',
        data: flowTargets,
        silent: true,
        lineStyle: {
          width: 1.6,
          color: 'rgba(88, 133, 198, 0.16)',
          opacity: 0.34,
          curveness: 0.24,
          shadowBlur: 4,
          shadowColor: 'rgba(36, 87, 168, 0.14)'
        },
        zlevel: 1
      },
      {
        name: '就业流向',
        type: 'lines',
        coordinateSystem: 'geo',
        data: flowTargets,
        effect: {
          show: true,
          period: 4.4,
          trailLength: 0.16,
          symbol: 'path://M0,-5 L12,0 L0,5 L3,0 Z',
          symbolSize: 7,
          color: 'rgba(36, 87, 168, 0.5)'
        },
        lineStyle: {
          width: 0.9,
          color: 'rgba(36, 87, 168, 0.34)',
          opacity: 0.48,
          curveness: 0.24,
          shadowBlur: 0
        },
        emphasis: {
          lineStyle: {
            width: 2.4,
            opacity: 1
          }
        },
        zlevel: 3
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
  width: min(17rem, 32%);
  height: min(11rem, 30%);
  pointer-events: none;
  opacity: 0.36;
  background: radial-gradient(ellipse at 76% 78%, color-mix(in oklch, var(--panel), white 2%) 0%, color-mix(in oklch, var(--panel), transparent 45%) 42%, transparent 76%);
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
  width: min(15.6rem, calc(100% - 2.5rem));
  padding: 0.68rem var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 58%);
  border-radius: 8px;
  background: linear-gradient(180deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: 0 0.85rem 2rem rgba(20, 52, 99, 0.12);
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
  color: var(--official-blue);
  font-size: 1.1rem;
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
  color: var(--official-blue);
  font-size: 0.84rem;
  font-variant-numeric: tabular-nums;
}
</style>
