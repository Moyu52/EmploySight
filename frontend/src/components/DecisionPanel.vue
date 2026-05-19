<template>
  <div class="decision-panel">
    <el-tabs v-model="activeTab" stretch>
      <el-tab-pane label="薪资预测" name="salary">
        <el-form class="decision-form" label-position="top">
          <el-row :gutter="8">
            <el-col :span="12">
              <el-form-item label="城市">
                <el-select v-model="salaryForm.city" size="small">
                  <el-option v-for="city in cities" :key="city" :label="city" :value="city" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="行业">
                <el-select v-model="salaryForm.industry" size="small">
                  <el-option v-for="industry in industries" :key="industry" :label="industry" :value="industry" />
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
          <el-button class="decision-button" size="small" type="primary" @click="runSalary">
            <Activity :size="15" />
            预测薪资
          </el-button>
        </el-form>
        <div v-if="salaryResult" class="result-block">
          <span>预测月薪区间</span>
          <strong>{{ salaryResult.predictedMin.toLocaleString('zh-CN') }} - {{ salaryResult.predictedMax.toLocaleString('zh-CN') }}</strong>
          <p>{{ salaryResult.modelName }} · 置信度 {{ salaryResult.confidence }}%</p>
        </div>
      </el-tab-pane>
      <el-tab-pane label="职业推荐" name="career">
        <el-form class="decision-form" label-position="top">
          <el-form-item label="专业">
            <el-input v-model="careerForm.major" size="small" />
          </el-form-item>
          <el-form-item label="技能">
            <el-select v-model="careerForm.skills" size="small" multiple collapse-tags collapse-tags-tooltip>
              <el-option v-for="skill in skillOptions" :key="skill" :label="skill" :value="skill" />
            </el-select>
          </el-form-item>
          <el-button class="decision-button" size="small" type="primary" @click="runRecommend">
            <Route :size="15" />
            生成建议
          </el-button>
        </el-form>
        <div class="recommend-list">
          <article v-for="item in recommendations" :key="item.direction" class="recommend-item">
            <b>{{ item.direction }}</b>
            <span>{{ item.city }} · {{ item.jobCategory }} · 匹配 {{ item.matchScore }}%</span>
          </article>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Activity, Route } from 'lucide-vue-next'
import { predictSalary, recommendCareer } from '../services/dashboard'
import type { CareerRecommendation, SalaryPrediction } from '../types/dashboard'

const activeTab = ref('salary')
const cities = ['西安', '北京', '重庆', '哈尔滨', '长春', '苏州', '大连', '西宁', '青岛', '常州']
const industries = ['生产制造及有关人员', '专业技术人员', '销售人员', '机械冷加工人员', '社会生产服务和生活服务人员']
const skillOptions = ['生产', '管理', '销售', '机械', '沟通', '安全', '质量', '会计', '电气', 'Excel']

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

async function runSalary() {
  salaryResult.value = await predictSalary(salaryForm)
}

async function runRecommend() {
  recommendations.value = await recommendCareer(careerForm)
}

runSalary()
runRecommend()
</script>

<style scoped>
.decision-panel {
  position: relative;
  z-index: 2;
  height: 100%;
  min-height: 0;
  overflow: hidden;
  padding: 0 var(--space-md) var(--space-sm);
}

.decision-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.3rem var(--space-xs);
}

.decision-button {
  width: 100%;
  grid-column: span 2;
}

.decision-button :deep(span) {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.result-block {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 0.12rem var(--space-xs);
  margin-top: var(--space-xs);
  padding: 0.42rem var(--space-sm);
  border-radius: 7px;
  background: color-mix(in oklch, var(--surface), transparent 12%);
}

.result-block span,
.result-block p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.72rem;
}

.result-block strong {
  grid-row: span 2;
  color: var(--accent-warm);
  font-size: 0.95rem;
  font-variant-numeric: tabular-nums;
}

.recommend-list {
  display: grid;
  gap: var(--space-xs);
  margin-top: var(--space-xs);
  max-height: 5.8rem;
  overflow: hidden;
}

.recommend-item {
  display: grid;
  gap: 0.2rem;
  padding: 0.42rem var(--space-sm);
  border-radius: 7px;
  background: color-mix(in oklch, var(--surface), transparent 14%);
}

.recommend-item b {
  color: var(--text);
  font-size: 0.78rem;
}

.recommend-item span {
  color: var(--text-muted);
  font-size: 0.68rem;
}

:deep(.el-tabs__item) {
  color: var(--text-muted);
  font-size: 0.78rem;
}

:deep(.el-tabs__item.is-active) {
  color: var(--accent-warm);
}

:deep(.el-tabs__active-bar) {
  background-color: var(--accent-warm);
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: color-mix(in oklch, var(--line), transparent 48%);
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-form-item__label) {
  color: var(--text-muted);
  font-size: 0.7rem;
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
