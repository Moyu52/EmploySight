<template>
  <div class="decision-panel">
    <el-tabs v-model="activeTab" :class="{ 'single-mode': props.mode !== 'both' }" stretch>
      <el-tab-pane v-if="props.mode !== 'career'" label="薪资预测" name="salary">
        <el-form class="decision-form" label-position="top">
          <el-row :gutter="8">
            <el-col :span="12">
              <el-form-item label="城市">
                <el-select v-model="salaryForm.city" size="small" filterable>
                  <el-option v-for="city in cityOptions" :key="city" :label="city" :value="city" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="行业">
                <el-select v-model="salaryForm.industry" size="small" filterable>
                  <el-option v-for="industry in industryOptions" :key="industry" :label="industry" :value="industry" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="8">
            <el-col :span="12">
              <el-form-item label="学历">
                <el-select v-model="salaryForm.education" size="small">
                  <el-option label="不限" value="不限" />
                  <el-option label="大专" value="大专" />
                  <el-option label="本科" value="本科" />
                  <el-option label="硕士" value="硕士" />
                  <el-option label="博士" value="博士" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="经验">
                <el-select v-model="salaryForm.experience" size="small">
                  <el-option label="不限" value="不限" />
                  <el-option label="应届/不限" value="应届/不限" />
                  <el-option label="1-3年" value="1-3年" />
                  <el-option label="3-5年" value="3-5年" />
                  <el-option label="5年以上" value="5年以上" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-button class="decision-button" size="small" type="primary" :loading="salaryLoading" :disabled="salaryLoading" @click="runSalary">
            <Activity :size="15" />
            预测薪资
          </el-button>
        </el-form>
        <div v-if="salaryLoading" class="ai-status" role="status" aria-live="polite">
          <Activity class="ai-status__icon" :size="15" />
          <div>
            <b>AI 薪资解释生成中</b>
            <span>正在结合城市薪资基准、岗位类别和技能因素生成分析，通常需要 10-30 秒，请稍候。</span>
          </div>
        </div>
        <div v-if="salaryResult" class="result-block">
          <span>预测月薪区间</span>
          <strong>{{ salaryResult.predictedMin.toLocaleString('zh-CN') }} - {{ salaryResult.predictedMax.toLocaleString('zh-CN') }}</strong>
          <p>参考置信度 {{ salaryResult.confidence }}% · {{ salaryResult.modelName }}</p>
          <p class="result-explanation">{{ salaryResult.explanation }}</p>
          <ul class="factor-list">
            <li v-for="factor in salaryResult.influenceFactors" :key="factor">{{ factor }}</li>
          </ul>
        </div>
      </el-tab-pane>
      <el-tab-pane v-if="props.mode !== 'salary'" label="职业推荐" name="career">
        <el-form class="decision-form" label-position="top">
          <el-form-item label="专业">
            <el-input v-model="careerForm.major" size="small" />
          </el-form-item>
          <el-form-item label="技能">
            <el-select v-model="careerForm.skills" size="small" multiple collapse-tags collapse-tags-tooltip>
              <el-option v-for="skill in skillOptions" :key="skill" :label="skill" :value="skill" />
            </el-select>
          </el-form-item>
          <el-button class="decision-button" size="small" type="primary" :loading="recommendLoading" :disabled="recommendLoading" @click="runRecommend">
            <Route :size="15" />
            生成建议
          </el-button>
        </el-form>
        <div v-if="recommendLoading" class="ai-status" role="status" aria-live="polite">
          <Activity class="ai-status__icon" :size="15" />
          <div>
            <b>AI 职业路径生成中</b>
            <span>正在综合专业画像、技能标签和公开招聘样本生成建议，通常需要 10-30 秒，请勿重复点击。</span>
          </div>
        </div>
        <div class="recommend-list">
          <article v-for="item in recommendations" :key="item.direction" class="recommend-item">
            <div class="recommend-head">
              <b>{{ item.direction }}</b>
              <span>{{ item.matchScore }}%</span>
            </div>
            <span>{{ item.city }} · {{ item.jobCategory }} · {{ item.industry }}</span>
            <p>{{ item.reason }}</p>
            <div v-if="item.skillGaps.length" class="gap-tags">
              <em v-for="gap in item.skillGaps" :key="gap">{{ gap }}</em>
            </div>
            <ul class="suggestion-list">
              <li v-for="suggestion in item.suggestions" :key="suggestion">{{ suggestion }}</li>
            </ul>
          </article>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { Activity, Route } from 'lucide-vue-next'
import { predictSalary, recommendCareer } from '../services/dashboard'
import type { CareerRecommendation, CityMetric, RankItem, SalaryPrediction, SkillKeyword } from '../types/dashboard'

const props = withDefaults(defineProps<{
  cities?: CityMetric[]
  industries?: RankItem[]
  skills?: SkillKeyword[]
  mode?: 'salary' | 'career' | 'both'
}>(), {
  mode: 'both'
})
const activeTab = ref(props.mode === 'career' ? 'career' : 'salary')

const fallbackCities = ['西安', '北京', '重庆', '哈尔滨', '长春', '苏州', '大连', '西宁', '青岛', '常州']
const fallbackIndustries = ['生产制造及有关人员', '专业技术人员', '销售人员', '机械冷加工人员', '社会生产服务和生活服务人员']
const fallbackSkills = ['生产', '管理', '销售', '机械', '沟通', '安全', '质量', '会计', '电气', 'Excel']

const cityOptions = computed(() => {
  const names = (props.cities ?? [])
    .map((item) => item.city)
    .filter(Boolean)
  return [...new Set(names.length ? names : fallbackCities)]
})

const industryOptions = computed(() => {
  const names = (props.industries ?? [])
    .map((item) => item.name)
    .filter(Boolean)
  return [...new Set(names.length ? names : fallbackIndustries)]
})

const skillOptions = computed(() => {
  const names = (props.skills ?? [])
    .map((item) => item.skill)
    .filter(Boolean)
  return [...new Set(names.length ? names : fallbackSkills)]
})

const salaryForm = reactive({
  city: '西安',
  industry: '生产制造及有关人员',
  education: '大专',
  experience: '不限',
  companySize: '500-999人',
  jobCategory: '生产制造与设备操作',
  skills: '生产,安全,质量'
})

const careerForm = reactive({
  major: '机械设计制造及其自动化',
  education: '大专',
  skills: ['生产', '安全', '质量'],
  expectedCities: ['西安', '重庆', '苏州'],
  expectedIndustries: ['生产制造及有关人员', '专业技术人员'],
  expectedSalary: 6000
})

const salaryResult = ref<SalaryPrediction>()
const recommendations = ref<CareerRecommendation[]>([])
const salaryLoading = ref(false)
const recommendLoading = ref(false)
let salaryRequestId = 0
let recommendRequestId = 0

watch(cityOptions, (options) => {
  if (options.length && !options.includes(salaryForm.city)) {
    salaryForm.city = options[0]
    careerForm.expectedCities = options.slice(0, 3)
    runSalary()
    runRecommend()
  }
}, { immediate: true })

watch(industryOptions, (options) => {
  if (options.length && !options.includes(salaryForm.industry)) {
    salaryForm.industry = options[0]
    careerForm.expectedIndustries = options.slice(0, 3)
    runSalary()
    runRecommend()
  }
}, { immediate: true })

watch(skillOptions, (options) => {
  const nextSkills = careerForm.skills.filter((item) => options.includes(item))
  if (options.length && nextSkills.length !== careerForm.skills.length) {
    careerForm.skills = nextSkills.length ? nextSkills : options.slice(0, 3)
    runRecommend()
  }
}, { immediate: true })

watch(() => props.mode, (mode) => {
  activeTab.value = mode === 'career' ? 'career' : 'salary'
}, { immediate: true })

async function runSalary() {
  const requestId = ++salaryRequestId
  salaryLoading.value = true
  try {
    const result = await predictSalary({ ...salaryForm })
    if (requestId === salaryRequestId) {
      salaryResult.value = result
    }
  } finally {
    if (requestId === salaryRequestId) {
      salaryLoading.value = false
    }
  }
}

async function runRecommend() {
  const requestId = ++recommendRequestId
  recommendLoading.value = true
  try {
    const result = await recommendCareer({
      ...careerForm,
      skills: [...careerForm.skills],
      expectedCities: [...careerForm.expectedCities],
      expectedIndustries: [...careerForm.expectedIndustries]
    })
    if (requestId === recommendRequestId) {
      recommendations.value = result
    }
  } finally {
    if (requestId === recommendRequestId) {
      recommendLoading.value = false
    }
  }
}

runSalary()
runRecommend()
</script>

<style scoped>
.decision-panel {
  position: relative;
  z-index: 2;
  min-height: 0;
  height: 100%;
  overflow: visible;
  padding: 0 var(--space-md) var(--space-sm);
}

.decision-panel :deep(.el-tabs) {
  height: 100%;
}

.decision-panel :deep(.el-tabs.single-mode .el-tabs__header) {
  display: none;
}

.decision-panel :deep(.el-tabs__content),
.decision-panel :deep(.el-tab-pane) {
  height: calc(100% - 2.65rem);
  min-height: 0;
}

.decision-panel :deep(.el-tabs.single-mode .el-tabs__content),
.decision-panel :deep(.el-tabs.single-mode .el-tab-pane) {
  height: 100%;
}

.decision-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-sm);
  align-content: start;
}

.decision-button {
  width: 100%;
  grid-column: span 2;
  min-height: 2.15rem;
}

.decision-button :deep(span) {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.ai-status {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: var(--space-xs);
  margin-top: var(--space-sm);
  padding: 0.52rem var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 76%);
  border-radius: 7px;
  background: color-mix(in oklch, var(--official-blue-soft), white 5%);
}

.ai-status__icon {
  color: var(--official-blue);
  animation: ai-status-spin 1s linear infinite;
}

.ai-status div {
  display: grid;
  gap: 0.08rem;
  min-width: 0;
}

.ai-status b {
  color: var(--official-blue-deep);
  font-size: 0.74rem;
}

.ai-status span {
  color: var(--text-muted);
  font-size: 0.68rem;
  line-height: 1.45;
}

@keyframes ai-status-spin {
  to {
    transform: rotate(360deg);
  }
}

.result-block {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 0.12rem var(--space-xs);
  margin-top: var(--space-md);
  padding: var(--space-md);
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 72%);
  border-left: 3px solid var(--official-blue);
  border-radius: 7px;
  background: color-mix(in oklch, var(--official-blue-soft), white 4%);
}

.result-block span,
.result-block p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.72rem;
}

.result-block strong {
  grid-row: span 2;
  color: var(--official-blue);
  font-size: 1.48rem;
  font-variant-numeric: tabular-nums;
}

.result-explanation,
.factor-list {
  grid-column: 1 / -1;
}

.result-explanation {
  line-height: 1.45;
}

.factor-list,
.suggestion-list {
  margin: 0;
  padding-left: 1rem;
  color: var(--text-muted);
  font-size: 0.7rem;
  line-height: 1.45;
}

.recommend-list {
  display: grid;
  gap: var(--space-xs);
  margin-top: var(--space-xs);
  max-height: min(20rem, 48vh);
  overflow: auto;
}

.recommend-item {
  display: grid;
  gap: 0.28rem;
  padding: 0.42rem var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 48%);
  border-left: 3px solid color-mix(in oklch, var(--official-blue), transparent 32%);
  border-radius: 7px;
  background: color-mix(in oklch, var(--panel), white 1%);
}

.recommend-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
}

.recommend-head b {
  min-width: 0;
  color: var(--official-blue-deep);
  font-size: 0.78rem;
}

.recommend-head span {
  flex: none;
  color: var(--official-blue);
  font-weight: 700;
  font-size: 0.72rem;
}

.recommend-item span {
  color: var(--text-muted);
  font-size: 0.72rem;
}

.recommend-item .recommend-head span {
  color: var(--official-blue);
  font-weight: 700;
}

.recommend-item p {
  margin: 0;
  color: var(--text-strong);
  font-size: 0.72rem;
  line-height: 1.45;
}

.gap-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.gap-tags em {
  padding: 0.1rem 0.36rem;
  border-radius: 999px;
  background: color-mix(in oklch, var(--official-blue-soft), white 8%);
  color: var(--official-blue-deep);
  font-size: 0.66rem;
  font-style: normal;
}

:deep(.el-tabs__item) {
  color: var(--text-muted);
  font-size: 0.82rem;
}

:deep(.el-tabs__item.is-active) {
  color: var(--official-blue);
}

:deep(.el-tabs__active-bar) {
  background-color: var(--official-blue);
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: color-mix(in oklch, var(--line), transparent 48%);
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-form-item__label) {
  color: var(--text-muted);
  font-size: 0.76rem;
  line-height: 1.2;
  margin-bottom: 0.16rem;
}

:deep(.el-tabs__header) {
  margin-bottom: 0.35rem;
}

:deep(.el-row) {
  display: contents;
}

:deep(.el-col) {
  max-width: none;
  padding-left: 0 !important;
  padding-right: 0 !important;
}
</style>
