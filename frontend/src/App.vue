<template>
  <main class="dashboard-shell">
    <div class="backdrop" aria-hidden="true"></div>

    <header class="topbar">
      <div class="topbar__title">
        <span>Graduate Employment Intelligence</span>
        <h1>中国就业态势感知与职业决策支持平台</h1>
      </div>
      <nav class="module-nav" aria-label="功能模块">
        <button v-for="item in modules" :key="item.key" :class="{ active: activeModule === item.key }" type="button" @click="activeModule = item.key">
          <component :is="item.icon" :size="15" />
          {{ item.label }}
        </button>
      </nav>
      <div class="topbar__status">
        <span>数据源：Kaggle China Jobs Data / Job Posting Data in China</span>
        <strong>{{ currentTime }}</strong>
      </div>
    </header>

    <section v-if="activeModule === 'dashboard'" class="screen-grid">
      <aside class="left-column">
        <div class="metric-grid">
          <MetricCard label="全国岗位总数" :value="overviewData.totalJobs" suffix="招聘岗位" icon="jobs" />
          <MetricCard label="平均月薪" :value="overviewData.averageSalary" suffix="元/月" icon="salary" />
          <MetricCard label="覆盖城市" :value="overviewData.coveredCities" suffix="个城市" icon="city" />
          <MetricCard label="应届友好度" :value="overviewData.freshFriendlyIndex" suffix="指数" icon="fresh" :decimals="1" />
        </div>

        <ShellPanel title="热门城市 TOP10" subtitle="自动轮播" dense>
          <AutoRank :items="overviewData.hotCities" :duration="20" />
        </ShellPanel>

        <ShellPanel title="热门行业 TOP10" subtitle="机会规模" dense>
          <AutoRank :items="overviewData.hotIndustries" :duration="22" />
        </ShellPanel>
      </aside>

      <section class="center-stage">
        <ShellPanel title="全国就业热度地图" :subtitle="activeProvinceLabel" eyebrow="态势感知主画布">
          <ChinaMap :provinces="provinceData" :cities="cityData" @province-change="activeProvince = $event" />
        </ShellPanel>
      </section>

      <aside class="right-column">
        <ShellPanel title="薪资 · 学历 · 经验" subtitle="定时刷新">
          <DistributionCharts :analysis="analysisData" />
        </ShellPanel>

        <ShellPanel title="技能需求热度" subtitle="TF-IDF / TextRank">
          <SkillCloud :skills="analysisData.skills" />
        </ShellPanel>
      </aside>

      <section class="bottom-band">
        <ShellPanel title="实时就业动态" subtitle="持续滚动">
          <LiveJobTicker :jobs="liveJobData" />
        </ShellPanel>
        <ShellPanel title="城市吸引力排行" subtitle="综合指数">
          <div class="city-strip">
            <article v-for="city in cityData.slice(0, 6)" :key="city.city">
              <span>{{ city.rankNo }}</span>
              <b>{{ city.city }}</b>
              <em>{{ city.attractionIndex }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="近 12 个月岗位趋势" subtitle="时间窗播放">
          <TrendChart :trends="overviewData.monthlyTrend" />
        </ShellPanel>
      </section>
    </section>

    <section v-else class="workbench" :class="`workbench--${activeModule}`">
      <template v-if="activeModule === 'city'">
        <ShellPanel title="城市就业吸引力评估" subtitle="岗位规模 / 薪资 / 应届友好 / 行业丰富度">
          <div class="city-workbench">
            <article v-for="city in cityData" :key="city.city" class="city-card">
              <span>No.{{ city.rankNo }}</span>
              <h3>{{ city.city }}</h3>
              <p>{{ city.province }} · {{ city.jobCount.toLocaleString('zh-CN') }} 个岗位 · 平均薪资 {{ city.avgSalary.toLocaleString('zh-CN') }} 元</p>
              <div class="score-line">
                <i :style="{ width: `${city.attractionIndex}%` }"></i>
              </div>
              <footer>
                <b>吸引力 {{ city.attractionIndex }}</b>
                <em>应届友好 {{ city.freshFriendlyIndex }}</em>
              </footer>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="省份覆盖完整性" subtitle="全国省级行政区指标">
          <div class="province-table">
            <article v-for="province in sortedProvinces" :key="province.province">
              <b>{{ province.province }}</b>
              <span>{{ province.heatIndex }}</span>
              <em>{{ province.topIndustry }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="城市选择建议" subtitle="面向毕业生投递策略">
          <div class="insight-list">
            <article v-for="item in cityInsights" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
              <em>{{ item.metric }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'salary'">
        <ShellPanel title="岗位薪资预测" subtitle="城市 / 行业 / 学历 / 经验 / 技能">
          <DecisionPanel />
        </ShellPanel>
        <ShellPanel title="薪资结构分析" subtitle="分布动态刷新">
          <DistributionCharts :analysis="analysisData" />
        </ShellPanel>
        <ShellPanel title="预测解释因子" subtitle="答辩可解释">
          <div class="explain-grid">
            <article v-for="item in salaryFactors" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="薪资谈判参考" subtitle="区间定位与投递优先级">
          <div class="benchmark-grid">
            <article v-for="item in salaryBenchmarks" :key="item.label">
              <span>{{ item.value }}</span>
              <b>{{ item.label }}</b>
              <em>{{ item.note }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'skills'">
        <ShellPanel title="技能需求挖掘" subtitle="jieba / TF-IDF / TextRank / 词频">
          <SkillCloud :skills="analysisData.skills" />
        </ShellPanel>
        <ShellPanel title="技能热度排行" subtitle="岗位描述关键词">
          <div class="skill-table">
            <article v-for="skill in analysisData.skills" :key="skill.skill">
              <b>{{ skill.skill }}</b>
              <span>{{ skill.category }}</span>
              <em>{{ skill.frequency.toLocaleString('zh-CN') }} 次</em>
              <strong>{{ skill.heatIndex }}</strong>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="技能提升建议" subtitle="面向毕业生">
          <div class="advice-list">
            <article>
              <b>数据方向</b>
              <span>SQL + Python + 可视化作品集，优先覆盖业务指标、A/B 分析和仪表盘项目。</span>
            </article>
            <article>
              <b>后端方向</b>
              <span>Python + FastAPI + MySQL + Redis，重点准备接口设计、部署和性能优化经验。</span>
            </article>
            <article>
              <b>算法方向</b>
              <span>机器学习基础模型 + 特征工程 + 模型评估，用应用型项目降低纯研究岗位门槛。</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="岗位技能组合" subtitle="高频共现路径">
          <div class="combo-grid">
            <article v-for="item in skillCombos" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.skills }}</span>
              <em>{{ item.fit }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'career'">
        <ShellPanel title="毕业生职业推荐" subtitle="专业 / 学历 / 技能 / 城市偏好 / 行业偏好">
          <DecisionPanel />
        </ShellPanel>
        <ShellPanel title="推荐方向矩阵" subtitle="岗位方向与城市组合">
          <div class="path-grid">
            <article v-for="item in careerPaths" :key="item.title">
              <span>{{ item.score }}%</span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="能力差距诊断" subtitle="目标岗位补强优先级">
          <div class="gap-diagnosis">
            <article v-for="item in capabilityGaps" :key="item.target">
              <header>
                <b>{{ item.target }}</b>
                <span>{{ item.priority }}</span>
              </header>
              <p>{{ item.required }}</p>
              <div class="gap-meter" :aria-label="`${item.target} 当前准备度 ${item.progress}%`">
                <i :style="{ width: `${item.progress}%` }"></i>
              </div>
              <footer>
                <em>{{ item.current }}</em>
                <strong>{{ item.action }}</strong>
              </footer>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="求职行动清单" subtitle="按 4 周准备节奏">
          <div class="action-list">
            <article v-for="item in actionItems" :key="item.week">
              <span>{{ item.week }}</span>
              <b>{{ item.title }}</b>
              <em>{{ item.text }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'data'">
        <ShellPanel title="数据治理与模型流水线" subtitle="Kaggle CSV 到平台指标库">
          <div class="pipeline">
            <article v-for="(step, index) in pipelineSteps" :key="step.title">
              <span>{{ index + 1 }}</span>
              <b>{{ step.title }}</b>
              <p>{{ step.text }}</p>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="数据覆盖说明" subtitle="避免缺失省份影响答辩">
          <div class="coverage-note">
            <p>平台演示数据已覆盖 34 个省级行政区，地图不再出现大量空白省份。当前数值用于原型演示；正式论文实验应使用 Kaggle 全量岗位数据，由 `data-processing/pipeline.py` 重新清洗、聚合、训练并导入 MySQL。</p>
            <p>如果真实数据中某省岗位样本不足，应在论文中标注“样本不足/置信度较低”，而不是简单留空。</p>
          </div>
        </ShellPanel>
        <ShellPanel title="数据质量监控" subtitle="清洗后指标校验">
          <div class="quality-grid">
            <article v-for="item in qualityMetrics" :key="item.label">
              <span>{{ item.value }}</span>
              <b>{{ item.label }}</b>
              <em>{{ item.note }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ChartColumnIncreasing, Database, Gauge, MapPinned, Route, SearchCode } from 'lucide-vue-next'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import AutoRank from './components/AutoRank.vue'
import ChinaMap from './components/ChinaMap.vue'
import DecisionPanel from './components/DecisionPanel.vue'
import DistributionCharts from './components/DistributionCharts.vue'
import LiveJobTicker from './components/LiveJobTicker.vue'
import MetricCard from './components/MetricCard.vue'
import ShellPanel from './components/ShellPanel.vue'
import SkillCloud from './components/SkillCloud.vue'
import TrendChart from './components/TrendChart.vue'
import { fetchAnalysis, fetchCities, fetchLiveJobs, fetchOverview, fetchProvinces } from './services/dashboard'
import { analysis, cityMetrics, liveJobs, overview, provinceMetrics } from './services/mockData'
import type { CityMetric, DashboardAnalysis, DashboardOverview, JobLiveItem, ProvinceMetric } from './types/dashboard'

type ModuleKey = 'dashboard' | 'city' | 'salary' | 'skills' | 'career' | 'data'

const modules = [
  { key: 'dashboard' as ModuleKey, label: '态势大屏', icon: Gauge },
  { key: 'city' as ModuleKey, label: '城市评估', icon: MapPinned },
  { key: 'salary' as ModuleKey, label: '薪资预测', icon: ChartColumnIncreasing },
  { key: 'skills' as ModuleKey, label: '技能挖掘', icon: SearchCode },
  { key: 'career' as ModuleKey, label: '职业推荐', icon: Route },
  { key: 'data' as ModuleKey, label: '数据治理', icon: Database }
]

const activeModule = ref<ModuleKey>('dashboard')
const overviewData = ref<DashboardOverview>(overview)
const provinceData = ref<ProvinceMetric[]>(provinceMetrics)
const cityData = ref<CityMetric[]>(cityMetrics)
const analysisData = ref<DashboardAnalysis>(analysis)
const liveJobData = ref<JobLiveItem[]>(liveJobs)
const activeProvince = ref<ProvinceMetric | null>(provinceMetrics[0])
const now = ref(new Date())
let clockTimer = 0
let refreshTimer = 0

const currentTime = computed(() => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(now.value)
})

const activeProvinceLabel = computed(() => {
  if (!activeProvince.value) {
    return '省份轮播高亮'
  }
  return `${activeProvince.value.province} · 热度 ${activeProvince.value.heatIndex}`
})

const sortedProvinces = computed(() => [...provinceData.value].sort((a, b) => b.heatIndex - a.heatIndex))

const salaryFactors = [
  { title: '城市基准', text: '一线城市和强产业城市薪资基准更高，是预测模型的重要特征。' },
  { title: '行业溢价', text: '人工智能、金融科技、云服务等行业对薪资有明显正向影响。' },
  { title: '学历经验', text: '学历门槛和经验年限影响薪资区间，同时也影响应届生可投比例。' },
  { title: '技能标签', text: 'Python、SQL、大数据、机器学习等技能会提高岗位匹配与薪资潜力。' }
]

const cityInsights = [
  { title: '优先冲刺城市', text: '深圳、北京、上海岗位规模和薪资基准高，适合技术能力较强的学生集中投递。', metric: '高薪高竞争' },
  { title: '稳妥承接城市', text: '杭州、成都、武汉、南京兼顾岗位数量和应届友好度，适合作为主投城市池。', metric: '机会均衡' },
  { title: '区域发展城市', text: '合肥、西安、长沙、郑州增长快，适合结合产业方向做差异化选择。', metric: '增长潜力' },
  { title: '样本不足处理', text: '低样本省份不直接留空，展示置信度提示并用相邻产业区域辅助解释。', metric: '答辩口径' }
]

const salaryBenchmarks = [
  { label: '本科应届目标', value: '10K-15K', note: '适合作为多数技术与数据岗位的合理期望区间。' },
  { label: '重点城市冲刺', value: '15K-25K', note: '需要项目作品、实习经历和技能组合支撑。' },
  { label: '算法高薪门槛', value: '25K+', note: '通常要求算法项目、论文竞赛或研究经历。' },
  { label: '保底投递区间', value: '6K-10K', note: '适合补充行业广度，提高 offer 稳定性。' }
]

const skillCombos = [
  { title: '数据分析岗', skills: 'SQL / Python / BI / 指标体系', fit: '匹配 94%' },
  { title: '后端开发岗', skills: 'Python / FastAPI / MySQL / Redis', fit: '匹配 88%' },
  { title: 'AI 应用岗', skills: '机器学习 / PyTorch / 特征工程', fit: '匹配 82%' },
  { title: '可视化开发岗', skills: 'Vue3 / TypeScript / ECharts', fit: '匹配 79%' }
]

const careerPaths = [
  { score: 94, title: '数据分析与商业智能', text: '适合统计、信管、计算机等专业，优先城市为深圳、杭州、上海。' },
  { score: 88, title: 'Python 后端与平台开发', text: '适合有项目经验的计算机类毕业生，强调 FastAPI、MySQL、Redis 和部署。' },
  { score: 82, title: 'AI 应用与算法工程', text: '薪资潜力高，但要求项目和数学基础，建议以应用型算法岗切入。' },
  { score: 79, title: '前端数据可视化', text: '适合对交互和可视化敏感的学生，重点准备 Vue3、TypeScript、ECharts。' }
]

const capabilityGaps = [
  {
    target: '数据分析与商业智能',
    required: 'SQL、Python、指标体系、BI 看板',
    current: '当前准备度 78%',
    action: '补 1 个 BI 看板项目，写清指标口径。',
    priority: '优先补强',
    progress: 78
  },
  {
    target: 'Python 后端与平台开发',
    required: 'FastAPI、MySQL、接口设计、部署',
    current: '当前准备度 71%',
    action: '补接口测试与部署说明。',
    priority: '次优先',
    progress: 71
  }
]

const actionItems = [
  { week: '第 1 周', title: '定位岗位池', text: '确定 2 个主方向和 1 个备选方向，建立城市和行业投递清单。' },
  { week: '第 2 周', title: '补齐作品集', text: '整理 1 个数据分析或后端项目，补充业务指标和部署说明。' },
  { week: '第 3 周', title: '模拟面试', text: '围绕 SQL、Python、项目难点和薪资预期进行结构化复盘。' },
  { week: '第 4 周', title: '集中投递', text: '按高匹配城市优先投递，并记录反馈迭代简历关键词。' }
]

const pipelineSteps = [
  { title: '字段映射', text: '统一岗位名称、城市、省份、薪资、学历、经验、行业、描述等字段。' },
  { title: '清洗标准化', text: '解析薪资区间，标准化学历经验，补全省份和经纬度。' },
  { title: '指标聚合', text: '生成省市就业热度、城市吸引力、应届友好度和行业排行。' },
  { title: '模型训练', text: '训练随机森林薪资模型，输出 MAE、RMSE、R2 等评估结果。' },
  { title: '接口服务', text: 'FastAPI 提供大屏、城市、技能、预测和推荐接口。' }
]

const qualityMetrics = [
  { label: '省级覆盖', value: '34/34', note: '演示口径覆盖全国省级行政区。' },
  { label: '重点城市', value: '38', note: '覆盖省会、直辖市和核心就业城市。' },
  { label: '字段完整率', value: '96.8%', note: '岗位、城市、薪资、学历经验字段通过清洗校验。' },
  { label: '模型可解释', value: '5 因子', note: '城市、行业、学历、经验、技能共同解释预测。' }
]

async function loadDashboard() {
  const [overviewResult, provinceResult, cityResult, analysisResult, liveJobResult] = await Promise.all([
    fetchOverview(),
    fetchProvinces(),
    fetchCities(),
    fetchAnalysis(),
    fetchLiveJobs()
  ])

  overviewData.value = overviewResult
  provinceData.value = provinceResult
  cityData.value = cityResult
  analysisData.value = analysisResult
  liveJobData.value = liveJobResult
}

onMounted(() => {
  loadDashboard()
  clockTimer = window.setInterval(() => {
    now.value = new Date()
  }, 1000)
  refreshTimer = window.setInterval(loadDashboard, 30000)
})

onBeforeUnmount(() => {
  window.clearInterval(clockTimer)
  window.clearInterval(refreshTimer)
})
</script>

<style scoped>
.dashboard-shell {
  position: relative;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: var(--space-sm);
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  padding: var(--space-md);
  color: var(--text);
  background:
    radial-gradient(circle at 18% 10%, rgba(81, 143, 132, 0.24), transparent 28rem),
    radial-gradient(circle at 86% 30%, rgba(184, 112, 74, 0.18), transparent 30rem),
    linear-gradient(135deg, var(--bg), var(--bg-deep));
}

.backdrop {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(color-mix(in oklch, var(--line), transparent 84%) 1px, transparent 1px),
    linear-gradient(90deg, color-mix(in oklch, var(--line), transparent 86%) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at center, black, transparent 82%);
  animation: grid-drift 26s linear infinite;
}

.backdrop::after {
  content: "";
  position: absolute;
  inset: -30%;
  background: conic-gradient(from 180deg, transparent, rgba(228, 180, 92, 0.11), transparent, rgba(93, 205, 196, 0.1), transparent);
  animation: aurora-turn 18s linear infinite;
}

.topbar {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(18rem, 1.1fr) auto minmax(18rem, 0.9fr);
  align-items: center;
  gap: var(--space-md);
  min-height: 5.4rem;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid color-mix(in oklch, var(--line), transparent 34%);
  border-radius: 8px;
  background: color-mix(in oklch, var(--panel), transparent 6%);
  box-shadow: var(--shadow-panel);
}

.topbar__title {
  display: grid;
  gap: 0.16rem;
}

.topbar__title span,
.topbar__status span {
  color: var(--text-muted);
  font-size: 0.76rem;
}

.topbar h1 {
  margin: 0;
  color: var(--text-strong);
  font-family: "Microsoft YaHei UI", "Bahnschrift", sans-serif;
  font-size: 1.58rem;
  font-weight: 800;
  letter-spacing: 0;
}

.module-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-xs);
}

.module-nav button {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-height: 2rem;
  padding: 0 var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 48%);
  border-radius: 999px;
  color: var(--text-muted);
  background: color-mix(in oklch, var(--surface), transparent 20%);
  cursor: pointer;
  transition: transform 180ms var(--ease-out-quint), border-color 180ms var(--ease-out-quint), color 180ms var(--ease-out-quint);
}

.module-nav button:hover,
.module-nav button.active {
  border-color: color-mix(in oklch, var(--accent-warm), transparent 18%);
  color: var(--text-strong);
  transform: translateY(-1px);
}

.module-nav button.active {
  background: color-mix(in oklch, var(--accent-warm), transparent 82%);
}

.topbar__status {
  display: grid;
  justify-items: end;
  gap: 0.3rem;
  text-align: right;
}

.topbar__status strong {
  color: var(--accent-warm);
  font-size: 1rem;
  font-variant-numeric: tabular-nums;
}

.screen-grid,
.workbench {
  position: relative;
  z-index: 1;
  min-height: 0;
}

.screen-grid {
  display: grid;
  grid-template-columns: minmax(20rem, 24rem) minmax(38rem, 1fr) minmax(21rem, 26rem);
  grid-template-rows: minmax(0, 1fr) clamp(9rem, 20vh, 11rem);
  grid-template-areas:
    "left center right"
    "bottom bottom bottom";
  gap: var(--space-sm);
  height: 100%;
}

.workbench {
  display: grid;
  grid-template-columns: minmax(24rem, 1fr) minmax(24rem, 1fr);
  gap: var(--space-sm);
  height: 100%;
  min-height: 0;
  overflow: auto;
}

.workbench--career {
  grid-template-rows: minmax(0, 1fr) minmax(0, 1fr);
  overflow: hidden;
}

.workbench--city > :first-child,
.workbench--data > :first-child {
  grid-column: span 2;
}

.left-column,
.right-column {
  display: grid;
  gap: var(--space-sm);
  min-height: 0;
}

.left-column {
  grid-area: left;
  grid-template-rows: auto 1fr 1fr;
}

.right-column {
  grid-area: right;
  grid-template-rows: minmax(16rem, 1.15fr) minmax(11rem, 0.85fr);
}

.center-stage {
  grid-area: center;
  min-height: 0;
}

.center-stage :deep(.shell-panel) {
  height: 100%;
}

.right-column :deep(.shell-panel),
.left-column :deep(.shell-panel),
.bottom-band :deep(.shell-panel) {
  min-height: 0;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-sm);
}

.bottom-band {
  grid-area: bottom;
  display: grid;
  grid-template-columns: minmax(24rem, 1.1fr) minmax(18rem, 0.7fr) minmax(30rem, 1.2fr);
  gap: var(--space-sm);
  min-height: 0;
}

.city-strip,
.city-workbench,
.province-table,
.skill-table,
.explain-grid,
.path-grid,
.pipeline,
.advice-list,
.insight-list,
.benchmark-grid,
.combo-grid,
.action-list,
.gap-diagnosis,
.quality-grid {
  position: relative;
  z-index: 1;
  padding: 0 var(--space-md) var(--space-md);
}

.city-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-xs);
  height: 100%;
  overflow: hidden;
}

.city-strip article,
.province-table article,
.skill-table article,
.explain-grid article,
.path-grid article,
.pipeline article,
.advice-list article,
.insight-list article,
.benchmark-grid article,
.combo-grid article,
.action-list article,
.gap-diagnosis article,
.quality-grid article,
.city-card {
  border: 1px solid color-mix(in oklch, var(--line), transparent 46%);
  border-radius: 7px;
  background: color-mix(in oklch, var(--surface), transparent 14%);
}

.city-strip article {
  display: grid;
  grid-template-columns: 1.8rem 1fr auto;
  align-items: center;
  gap: var(--space-xs);
  min-width: 0;
  min-height: 3rem;
  padding: 0 var(--space-sm);
}

.city-strip span,
.pipeline span,
.city-card > span {
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: var(--bg);
  background: var(--accent-warm);
  font-size: 0.72rem;
  font-weight: 800;
}

.city-strip span {
  width: 1.45rem;
  height: 1.45rem;
}

.city-strip b,
.province-table b,
.skill-table b,
.explain-grid b,
.path-grid h3,
.pipeline b,
.advice-list b,
.city-card h3 {
  color: var(--text);
}

.city-strip b,
.province-table b,
.skill-table b,
.city-card h3,
.path-grid h3,
.pipeline b,
.advice-list b {
  min-width: 0;
  overflow-wrap: anywhere;
}

.city-strip em,
.province-table span,
.skill-table strong,
.city-card footer b {
  color: var(--accent);
  font-style: normal;
  font-variant-numeric: tabular-nums;
}

.city-workbench {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  gap: var(--space-sm);
  height: 100%;
  min-height: 0;
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in oklch, var(--accent), transparent 42%) transparent;
}

.city-card {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-sm);
}

.city-card > span {
  width: fit-content;
  padding: 0.15rem 0.55rem;
}

.city-card h3,
.path-grid h3 {
  margin: 0;
  font-size: 1.05rem;
}

.city-card p,
.path-grid p,
.pipeline p,
.coverage-note p,
.advice-list span,
.explain-grid span,
.insight-list span,
.benchmark-grid em,
.combo-grid span,
.action-list em,
.gap-diagnosis p,
.gap-diagnosis em,
.quality-grid em {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.78rem;
  line-height: 1.55;
}

.score-line {
  overflow: hidden;
  height: 0.38rem;
  border-radius: 999px;
  background: color-mix(in oklch, var(--line), transparent 68%);
}

.score-line i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--accent-warm));
}

.city-card footer {
  display: flex;
  justify-content: space-between;
  gap: var(--space-sm);
  min-width: 0;
}

.city-card footer em,
.province-table em,
.skill-table span,
.skill-table em {
  color: var(--text-muted);
  font-size: 0.72rem;
  font-style: normal;
}

.province-table,
.skill-table {
  display: grid;
  align-content: start;
  gap: var(--space-xs);
  height: 100%;
  min-height: 0;
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in oklch, var(--accent), transparent 42%) transparent;
}

.province-table article {
  display: grid;
  grid-template-columns: 5rem 4rem 1fr;
  align-items: center;
  gap: var(--space-sm);
  min-height: 2.35rem;
  padding: 0 var(--space-sm);
}

.skill-table article {
  display: grid;
  grid-template-columns: 1fr 7rem 6rem 3.8rem;
  align-items: center;
  gap: var(--space-sm);
  min-height: 2.6rem;
  padding: 0 var(--space-sm);
}

.explain-grid,
.path-grid,
.pipeline,
.advice-list,
.insight-list,
.benchmark-grid,
.combo-grid,
.action-list,
.gap-diagnosis,
.quality-grid {
  display: grid;
  gap: var(--space-sm);
}

.explain-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.benchmark-grid,
.combo-grid,
.quality-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.path-grid {
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
}

.explain-grid article,
.path-grid article,
.advice-list article,
.insight-list article,
.benchmark-grid article,
.combo-grid article,
.gap-diagnosis article,
.quality-grid article {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-md);
}

.path-grid span {
  color: var(--accent-warm);
  font-size: 1.5rem;
  font-weight: 800;
}

.benchmark-grid span,
.quality-grid span {
  color: var(--accent-warm);
  font-size: 1.35rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.insight-list article {
  grid-template-columns: minmax(8rem, 0.8fr) minmax(0, 1fr) auto;
  align-items: center;
}

.insight-list em,
.combo-grid em,
.action-list span {
  color: var(--accent);
  font-size: 0.72rem;
  font-style: normal;
}

.combo-grid article {
  min-height: 6.1rem;
}

.action-list article {
  display: grid;
  grid-template-columns: 4.5rem minmax(7rem, 0.8fr) minmax(0, 1fr);
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
}

.workbench--career .path-grid,
.workbench--career .action-list,
.workbench--career .gap-diagnosis {
  height: 100%;
}

.workbench--career .path-grid,
.workbench--career .gap-diagnosis {
  grid-auto-rows: minmax(0, 1fr);
}

.workbench--career .action-list {
  align-content: stretch;
  grid-auto-rows: minmax(0, 1fr);
}

.workbench--career .path-grid article {
  padding: var(--space-sm) var(--space-md);
}

.gap-diagnosis article {
  grid-template-columns: minmax(10rem, 0.9fr) minmax(0, 1fr);
  align-items: center;
  gap: var(--space-xs) var(--space-md);
  min-height: 0;
  padding: var(--space-md);
}

.gap-diagnosis header,
.gap-diagnosis footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
  min-width: 0;
}

.gap-diagnosis header {
  grid-column: span 2;
}

.gap-diagnosis header b {
  color: var(--text);
  overflow-wrap: anywhere;
}

.gap-diagnosis header span {
  flex: 0 0 auto;
  color: var(--accent-warm);
  font-size: 0.72rem;
}

.gap-diagnosis footer strong {
  color: var(--text);
  font-size: 0.76rem;
  font-weight: 600;
  line-height: 1.45;
  text-align: right;
}

.gap-diagnosis em {
  flex: 0 0 auto;
  font-style: normal;
}

.gap-diagnosis p {
  line-height: 1.35;
}

.gap-meter {
  overflow: hidden;
  height: 0.42rem;
  border-radius: 999px;
  background: color-mix(in oklch, var(--line), transparent 66%);
}

.gap-meter i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent), var(--accent-warm));
}

.pipeline article {
  display: grid;
  grid-template-columns: 2rem 9rem 1fr;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm);
}

.pipeline span {
  width: 1.6rem;
  height: 1.6rem;
}

.coverage-note {
  position: relative;
  z-index: 1;
  display: grid;
  gap: var(--space-sm);
  padding: 0 var(--space-md) var(--space-md);
}

@keyframes grid-drift {
  from {
    background-position: 0 0;
  }
  to {
    background-position: 48px 48px;
  }
}

@keyframes aurora-turn {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1280px) {
  .dashboard-shell {
    overflow: auto;
  }

  .topbar,
  .screen-grid,
  .workbench {
    grid-template-columns: 1fr;
  }

  .screen-grid {
    grid-template-areas:
      "center"
      "left"
      "right"
      "bottom";
    grid-template-rows: auto;
    height: auto;
  }

  .workbench > :first-child {
    grid-column: span 1;
  }

  .bottom-band,
  .explain-grid {
    grid-template-columns: 1fr;
  }
}
</style>
