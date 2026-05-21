<template>
  <main v-if="!isAuthenticated" class="login-shell">
    <div class="backdrop" aria-hidden="true"></div>
    <section class="login-hero">
      <span>Graduation Project 2026</span>
      <h1>高校毕业生就业态势感知与职业决策支持系统</h1>
      <p>本科毕业设计课题系统，围绕真实招聘岗位数据完成数据采集、预处理、可视化分析、薪资预测模型、职业推荐和答辩报告组织。</p>
      <div class="thesis-card">
        <div>
          <span>课题名称</span>
          <b>基于公开招聘数据的毕业生就业分析与职业决策支持平台</b>
        </div>
        <div>
          <span>技术路线</span>
          <b>Python 数据处理 · FastAPI · Vue3 · ECharts · 随机森林回归</b>
        </div>
        <div>
          <span>答辩重点</span>
          <b>真实数据来源、模型可解释性、平台完整功能、可视化交互</b>
        </div>
      </div>
      <div class="login-insights">
        <article>
          <b>{{ overviewData.totalJobs.toLocaleString('zh-CN') }}</b>
          <span>真实岗位样本</span>
        </article>
        <article>
          <b>{{ overviewData.coveredCities }}</b>
          <span>覆盖城市</span>
        </article>
        <article>
          <b>{{ overviewData.averageSalary.toLocaleString('zh-CN') }}</b>
          <span>平均月薪</span>
        </article>
      </div>
    </section>
    <section class="login-card">
      <div class="login-card__head">
        <LockKeyhole :size="22" />
        <div>
          <span>毕业设计系统登录</span>
          <h2>毕业设计演示入口</h2>
        </div>
      </div>
      <el-form class="login-form" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="账号">
          <el-input v-model="loginForm.username" size="large" placeholder="admin / teacher / student" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" size="large" type="password" show-password placeholder="任意非空密码可进入演示系统" />
        </el-form-item>
        <el-form-item label="登录角色">
          <el-select v-model="loginForm.role" size="large">
            <el-option label="就业指导教师" value="就业指导教师" />
            <el-option label="毕业生用户" value="毕业生用户" />
            <el-option label="系统管理员" value="系统管理员" />
          </el-select>
        </el-form-item>
        <el-button class="login-button" type="primary" size="large" native-type="button" @click="handleLogin">
          进入系统
        </el-button>
      </el-form>
      <div class="login-note">
        <span>演示账号：admin</span>
        <span>演示密码：任意非空</span>
      </div>
      <div class="defense-info">
        <article>
          <span>项目类型</span>
          <b>数据分析 + 机器学习 + 可视化系统</b>
        </article>
        <article>
          <span>运行模式</span>
          <b>前后端分离，后端异常时自动使用真实数据快照</b>
        </article>
      </div>
    </section>
  </main>

  <main v-else class="dashboard-shell" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <div class="backdrop" aria-hidden="true"></div>

    <aside class="platform-sidebar">
      <div class="platform-brand">
        <span>毕设</span>
        <div>
          <b>毕业设计系统</b>
          <em>就业数据分析平台</em>
        </div>
      </div>
      <button class="sidebar-toggle" type="button" :aria-label="isSidebarCollapsed ? '展开功能导航' : '收起功能导航'" @click="isSidebarCollapsed = !isSidebarCollapsed">
        <PanelLeftClose v-if="!isSidebarCollapsed" :size="16" />
        <PanelLeftOpen v-else :size="16" />
        <span>{{ isSidebarCollapsed ? '展开导航' : '收起导航' }}</span>
      </button>
      <div class="thesis-mini">
        <span>课题编号</span>
        <b>GEI-2026-01</b>
        <em>指导答辩演示版</em>
      </div>
      <nav class="module-nav" aria-label="功能模块">
        <button v-for="item in modules" :key="item.key" :class="{ active: activeModule === item.key }" type="button" :aria-label="item.label" :title="isSidebarCollapsed ? item.label : undefined" @click="activeModule = item.key">
          <component :is="item.icon" :size="15" />
          <span>{{ item.label }}</span>
        </button>
      </nav>
      <div class="sidebar-status">
        <b>数据快照</b>
        <span>{{ overviewData.publishStart || '未知' }} 至 {{ overviewData.publishEnd || '未知' }}</span>
        <em>{{ overviewData.totalJobs.toLocaleString('zh-CN') }} 条岗位记录</em>
      </div>
    </aside>

    <section class="platform-main">
      <header class="topbar">
        <div class="topbar__title">
          <span>{{ activeModuleMeta.group }}</span>
          <h1>{{ activeModuleMeta.title }}</h1>
        </div>
        <div class="topbar__status">
          <span>数据源：中国公共招聘网 + Kaggle 公开岗位数据</span>
          <strong>{{ currentTime }}</strong>
        </div>
        <div class="user-card">
          <UserRound :size="18" />
          <div>
            <b>{{ loginForm.username }}</b>
            <span>{{ loginForm.role }}</span>
          </div>
          <button type="button" title="退出登录" @click="logout">
            <LogOut :size="16" />
          </button>
        </div>
      </header>

    <section v-if="activeModule === 'home'" class="portal-home">
      <section class="home-hero">
        <span>本科毕业设计综合平台</span>
        <h2>从真实岗位数据采集、清洗、建模到可视化决策的一体化系统</h2>
        <p>当前项目不再只是态势大屏，而是具备登录入口、平台首页、业务分析、模型评估、报告管理和系统管理的完整就业数据分析系统。</p>
        <div class="thesis-meta-grid">
          <article>
            <span>研究对象</span>
            <b>高校毕业生就业岗位</b>
          </article>
          <article>
            <span>核心算法</span>
            <b>随机森林薪资预测</b>
          </article>
          <article>
            <span>系统架构</span>
            <b>Vue3 + Python FastAPI</b>
          </article>
        </div>
        <div class="home-actions">
          <button type="button" @click="activeModule = 'dashboard'">打开态势大屏</button>
          <button type="button" @click="activeModule = 'report'">查看答辩报告</button>
        </div>
      </section>
      <section class="home-metrics">
        <MetricCard label="岗位样本" :value="overviewData.totalJobs" suffix="条真实记录" icon="jobs" />
        <MetricCard label="有效薪资" :value="overviewData.salarySampleRows" suffix="条样本" icon="salary" />
        <MetricCard label="覆盖城市" :value="overviewData.coveredCities" suffix="个城市" :detail="`地图可定位 ${mappableCityCount} 个`" icon="city" />
        <MetricCard label="模型 R2" :value="44.31" suffix="%" icon="fresh" :decimals="2" />
      </section>
      <section class="home-grid">
        <article v-for="item in projectEntrances" :key="item.key" class="home-entry" @click="activeModule = item.key">
          <component :is="item.icon" :size="22" />
          <b>{{ item.title }}</b>
          <span>{{ item.text }}</span>
        </article>
      </section>
      <section class="home-grid home-grid--narrow">
        <ShellPanel title="项目完成度" subtitle="毕业设计检查项">
          <div class="progress-list">
            <article v-for="item in graduationChecks" :key="item.label">
              <b>{{ item.label }}</b>
              <span>{{ item.status }}</span>
              <div class="score-line"><i :style="{ width: `${item.progress}%` }"></i></div>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="近期岗位样本" subtitle="最新公开招聘记录">
          <LiveJobTicker :jobs="liveJobData" />
        </ShellPanel>
      </section>
      <section class="home-longform">
        <ShellPanel title="毕业设计验收说明" subtitle="面向答辩与服务器部署">
          <div class="acceptance-grid">
            <article v-for="item in acceptanceItems" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="系统部署准备" subtitle="上线前检查">
          <div class="deploy-list">
            <article v-for="item in deployChecklist" :key="item.title">
              <span>{{ item.no }}</span>
              <b>{{ item.title }}</b>
              <em>{{ item.text }}</em>
            </article>
          </div>
        </ShellPanel>
      </section>
    </section>

    <section v-else-if="activeModule === 'dashboard'" class="screen-grid">
      <aside class="left-column">
        <div class="metric-grid">
          <MetricCard label="全国岗位总数" :value="overviewData.totalJobs" suffix="招聘岗位" icon="jobs" />
          <MetricCard label="平均月薪" :value="overviewData.averageSalary" suffix="元/月" icon="salary" />
          <MetricCard label="覆盖城市" :value="overviewData.coveredCities" suffix="个城市" :detail="`地图可定位 ${mappableCityCount} 个`" icon="city" />
          <MetricCard label="应届友好度" :value="overviewData.freshFriendlyIndex" suffix="指数" icon="fresh" :decimals="1" />
        </div>

        <ShellPanel title="热门城市 TOP10" subtitle="真实样本排行" dense>
          <AutoRank :items="displayHotCities.hotCities" />
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
        <ShellPanel title="实时就业动态" subtitle="最新岗位样本">
          <LiveJobTicker :jobs="liveJobData" />
        </ShellPanel>
        <ShellPanel title="城市吸引力排行" subtitle="综合指数">
          <div class="city-strip">
            <article v-for="city in displayTopCities" :key="city.city">
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
        <ShellPanel title="城市就业吸引力评估" :subtitle="`完整展示 ${cityData.length} 个真实样本城市`">
          <div class="city-workbench">
            <article class="city-summary">
              <span>{{ cityData.length }}</span>
              <b>完整城市清单</b>
              <p>这里展示原始岗位数据中全部有岗位样本的城市，不再只展示地图可定位城市。</p>
            </article>
            <article class="city-summary">
              <span>{{ mappableCityCount }}</span>
              <b>地图可定位城市</b>
              <p>只有已维护经纬度的城市会进入态势大屏地图和流向线，避免无坐标点影响地图。</p>
            </article>
            <article v-for="city in cityData" :key="city.city" class="city-card">
              <span>No.{{ city.rankNo }}</span>
              <h3>
                {{ city.city }}
                <em v-if="!city.hasCoords">未定位</em>
              </h3>
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
          <DecisionPanel :cities="cityData" :industries="overviewData.hotIndustries" :skills="analysisData.skills" />
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
              <b>生产制造方向</b>
              <span>优先补齐安全规范、质量意识、设备基础和工艺流程，适合公共招聘网样本中的高频岗位。</span>
            </article>
            <article>
              <b>销售服务方向</b>
              <span>强化沟通、客户跟进、基础办公和渠道执行能力，匹配销售人员与生活服务类岗位。</span>
            </article>
            <article>
              <b>财务运营方向</b>
              <span>补齐 Excel、Office、会计基础、采购和仓储流程，适合办事、财务与运营类岗位。</span>
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
          <DecisionPanel :cities="cityData" :industries="overviewData.hotIndustries" :skills="analysisData.skills" />
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
        <ShellPanel title="数据治理与模型流水线" subtitle="公开岗位数据到平台指标库">
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
            <p>当前展示数据由 Kaggle China Jobs Data、Kaggle Job Posting Data in China 和中国公共招聘网公开岗位合并生成，共 {{ overviewData.totalJobs.toLocaleString('zh-CN') }} 条岗位；样本时间范围为 {{ overviewData.publishStart || '未知' }} 至 {{ overviewData.publishEnd || '未知' }}，有真实样本的省级区域为 {{ overviewData.coveredRegions || sampledRegionCount }}/{{ overviewData.totalRegions || provinceData.length }}。</p>
            <p>城市覆盖口径为原始岗位记录中的唯一城市数，共 {{ overviewData.coveredCities || cityData.length }} 个；其中 {{ mappableCityCount }} 个城市已维护经纬度，会用于地图散点和流向线。</p>
            <p>样本不足地区在指标中显示“样本不足”，不再用虚构岗位数、薪资或热度补齐。</p>
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

      <template v-if="activeModule === 'model'">
        <ShellPanel title="薪资预测模型评估" subtitle="RandomForestRegressor">
          <div class="model-score-grid">
            <article v-for="metric in modelMetrics" :key="metric.label">
              <span>{{ metric.value }}</span>
              <b>{{ metric.label }}</b>
              <em>{{ metric.note }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="模型特征工程" subtitle="答辩说明">
          <div class="feature-list">
            <article v-for="item in modelFeatures" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="训练流程" subtitle="Python 数据处理流水线">
          <div class="pipeline">
            <article v-for="(step, index) in trainingSteps" :key="step.title">
              <span>{{ index + 1 }}</span>
              <b>{{ step.title }}</b>
              <p>{{ step.text }}</p>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="模型应用范围" subtitle="使用边界">
          <div class="coverage-note">
            <p>薪资预测模型面向公开岗位样本中的城市、行业、学历、经验、企业规模、岗位类别和技能描述进行区间估计，适合作为毕业生投递前的参考，不替代企业实际薪酬。</p>
            <p>当前模型 R2 为 0.4431，说明公开岗位薪资受到城市、行业、经验等可解释变量影响，但仍存在企业福利、岗位级别、隐性奖金等外部因素。</p>
            <p>系统保留启发式兜底预测逻辑，后端不可用时仍可基于当前真实城市薪资均值生成演示结果。</p>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'report'">
        <ShellPanel title="毕业设计报告中心" subtitle="答辩材料组织">
          <div class="report-layout">
            <article v-for="item in reportSections" :key="item.title">
              <span>{{ item.index }}</span>
              <b>{{ item.title }}</b>
              <p>{{ item.text }}</p>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="系统功能清单" subtitle="验收点">
          <div class="feature-list">
            <article v-for="item in systemFeatures" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="答辩演示路线" subtitle="建议 5 分钟流程">
          <div class="demo-route">
            <article v-for="item in demoRoute" :key="item.step">
              <span>{{ item.step }}</span>
              <b>{{ item.title }}</b>
              <em>{{ item.text }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'admin'">
        <ShellPanel title="系统管理" subtitle="用户、权限与运行状态">
          <div class="admin-grid">
            <article v-for="item in adminCards" :key="item.title">
              <component :is="item.icon" :size="22" />
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="用户角色管理" subtitle="毕业设计演示权限">
          <div class="role-table">
            <article v-for="role in roleRows" :key="role.name">
              <b>{{ role.name }}</b>
              <span>{{ role.scope }}</span>
              <em>{{ role.permission }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="运行监控" subtitle="前后端服务状态">
          <div class="quality-grid">
            <article v-for="item in runtimeStatus" :key="item.label">
              <span>{{ item.value }}</span>
              <b>{{ item.label }}</b>
              <em>{{ item.note }}</em>
            </article>
          </div>
        </ShellPanel>
      </template>
    </section>
    </section>
  </main>
</template>

<script setup lang="ts">
import {
  BrainCircuit,
  ChartColumnIncreasing,
  Database,
  FileChartColumnIncreasing,
  Gauge,
  Home,
  LockKeyhole,
  LogOut,
  MapPinned,
  PanelLeftClose,
  PanelLeftOpen,
  Route,
  SearchCode,
  ServerCog,
  Settings,
  ShieldCheck,
  UserRound,
  UsersRound
} from 'lucide-vue-next'
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

type ModuleKey = 'home' | 'dashboard' | 'city' | 'salary' | 'skills' | 'career' | 'data' | 'model' | 'report' | 'admin'

const modules = [
  { key: 'home' as ModuleKey, label: '系统首页', icon: Home },
  { key: 'dashboard' as ModuleKey, label: '态势大屏', icon: Gauge },
  { key: 'city' as ModuleKey, label: '城市评估', icon: MapPinned },
  { key: 'salary' as ModuleKey, label: '薪资预测', icon: ChartColumnIncreasing },
  { key: 'skills' as ModuleKey, label: '技能挖掘', icon: SearchCode },
  { key: 'career' as ModuleKey, label: '职业推荐', icon: Route },
  { key: 'data' as ModuleKey, label: '数据治理', icon: Database },
  { key: 'model' as ModuleKey, label: '模型中心', icon: BrainCircuit },
  { key: 'report' as ModuleKey, label: '报告中心', icon: FileChartColumnIncreasing },
  { key: 'admin' as ModuleKey, label: '系统管理', icon: Settings }
]

const isAuthenticated = ref(false)
const loginForm = ref({
  username: 'admin',
  password: '123456',
  role: '就业指导教师'
})
const activeModule = ref<ModuleKey>('home')
const isSidebarCollapsed = ref(false)
const overviewData = ref<DashboardOverview>(overview)
const provinceData = ref<ProvinceMetric[]>(provinceMetrics)
const cityData = ref<CityMetric[]>(cityMetrics)
const analysisData = ref<DashboardAnalysis>(analysis)
const liveJobData = ref<JobLiveItem[]>(liveJobs)
const activeProvince = ref<ProvinceMetric | null>(provinceMetrics[0])
const now = ref(new Date())
let clockTimer = 0
let refreshTimer = 0

const moduleMeta: Record<ModuleKey, { title: string; group: string }> = {
  home: { title: '系统首页', group: '平台总览' },
  dashboard: { title: '就业态势大屏', group: '态势感知' },
  city: { title: '城市就业吸引力评估', group: '城市分析' },
  salary: { title: '岗位薪资预测', group: '职业决策' },
  skills: { title: '技能需求挖掘', group: '文本分析' },
  career: { title: '毕业生职业推荐', group: '推荐决策' },
  data: { title: '数据治理中心', group: '数据工程' },
  model: { title: '模型评估中心', group: '机器学习' },
  report: { title: '毕业设计报告中心', group: '答辩材料' },
  admin: { title: '系统管理', group: '平台运维' }
}

const currentTime = computed(() => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(now.value)
})

const activeModuleMeta = computed(() => moduleMeta[activeModule.value])
function cleanDisplayName(value: string) {
  return value
    .replace(/省省$/u, '省')
    .replace(/市市$/u, '市')
    .replace(/自治区自治区$/u, '自治区')
    .replace(/维吾尔$/u, '维吾尔自治区')
    .replace(/壮族$/u, '壮族自治区')
    .replace(/回族$/u, '回族自治区')
    .replace(/特别行政$/u, '特别行政区')
}

const displayHotCities = computed(() => ({
  ...overviewData.value,
  hotCities: overviewData.value.hotCities.map((item) => ({
    ...item,
    name: cleanDisplayName(item.name),
    tag: cleanDisplayName(item.tag)
  }))
}))
const displayCityData = computed(() => cityData.value.map((item) => ({
  ...item,
  city: cleanDisplayName(item.city),
  province: cleanDisplayName(item.province)
})))
const displayTopCities = computed(() => displayCityData.value.slice(0, 6))
const activeProvinceLabel = computed(() => {
  if (!activeProvince.value) {
    return '省份轮播高亮'
  }
  return `${activeProvince.value.province} · 热度 ${activeProvince.value.heatIndex}`
})

const sortedProvinces = computed(() => [...provinceData.value].sort((a, b) => b.heatIndex - a.heatIndex))
const mappableCityCount = computed(() => cityData.value.filter((item) => item.hasCoords && item.longitude && item.latitude).length)
const sampledRegionCount = computed(() => provinceData.value.filter((item) => item.jobCount > 0).length)
const topCityNames = computed(() => cityData.value.slice(0, 5).map((item) => item.city).join('、'))
const manufacturingCityNames = computed(() => cityData.value
  .filter((item) => ['苏州', '常州', '青岛', '南京', '无锡', '济南'].includes(item.city))
  .slice(0, 4)
  .map((item) => item.city)
  .join('、') || cityData.value.slice(5, 9).map((item) => item.city).join('、'))
const freshFriendlyCityNames = computed(() => [...cityData.value]
  .filter((item) => item.jobCount >= 10)
  .sort((a, b) => b.freshFriendlyIndex - a.freshFriendlyIndex)
  .slice(0, 3)
  .map((item) => item.city)
  .join('、'))
const cityInsights = computed(() => [
  { title: '样本规模城市', text: `${topCityNames.value || '当前高样本城市'}在当前真实样本中岗位规模靠前，适合优先观察。`, metric: '规模优先' },
  { title: '制造业承接城市', text: `${manufacturingCityNames.value || '制造业样本城市'}兼具岗位数量和制造业、专业技术岗位基础。`, metric: '产业匹配' },
  { title: '应届友好城市', text: `${freshFriendlyCityNames.value || '应届友好城市'}的经验门槛相对友好，可作为毕业生稳妥投递池。`, metric: '门槛较低' },
  { title: '地图定位口径', text: `城市评估展示 ${cityData.value.length} 个真实样本城市，地图仅使用 ${mappableCityCount.value} 个已维护经纬度的城市。`, metric: '口径一致' }
])
const salaryBenchmarks = computed(() => [
  { label: '主体区间', value: analysisData.value.salaryRanges[0]?.name ?? '未知', note: '当前清洗样本中占比最高，适合做毕业生保守薪资预期。' },
  { label: '提升区间', value: analysisData.value.salaryRanges[1]?.name ?? '未知', note: '第二高占比区间，需要结合城市、行业和岗位技能判断。' },
  { label: '冲刺区间', value: '10K+', note: '占比较小，多出现在样本较少的一线城市或专业技术岗位。' },
  { label: '全样本均值', value: overviewData.value.averageSalary.toLocaleString('zh-CN'), note: `基于 ${overviewData.value.salarySampleRows.toLocaleString('zh-CN')} 条有效薪资样本解析得到。` }
])
const qualityMetrics = computed(() => [
  { label: '省级样本覆盖', value: `${overviewData.value.coveredRegions || sampledRegionCount.value}/${overviewData.value.totalRegions || provinceData.value.length}`, note: '只统计真实岗位样本，不用虚构数据补齐。' },
  { label: '覆盖城市', value: `${overviewData.value.coveredCities || cityData.value.length}`, note: '来自合并后的真实岗位记录，城市评估页完整展示。' },
  { label: '地图可定位城市', value: `${mappableCityCount.value}`, note: '已维护经纬度，可用于地图散点和就业流向线。' },
  { label: '有效薪资样本', value: `${overviewData.value.salarySampleRows.toLocaleString('zh-CN')}`, note: '用于薪资分布和薪资模型训练。' }
])
const modelMetrics = computed(() => [
  { label: 'MAE 平均绝对误差', value: '1,560.88', note: '预测薪资与真实薪资的平均绝对偏差，单位为元。' },
  { label: 'RMSE 均方根误差', value: '2,678.21', note: '对大偏差更敏感，用于评估薪资区间波动。' },
  { label: 'R2 拟合优度', value: '0.4431', note: '公开岗位薪资受城市、行业、经验和企业等多因素影响。' },
  { label: '训练样本', value: `${overviewData.value.salarySampleRows.toLocaleString('zh-CN')}`, note: '使用清洗后的有效薪资岗位记录进行训练。' }
])
const runtimeStatus = computed(() => [
  { label: '前端应用', value: '正常', note: 'Vue 3 + Element Plus + ECharts。' },
  { label: '后端接口', value: '可降级', note: '接口不可用时自动使用本地真实快照数据。' },
  { label: '数据快照', value: `${overviewData.value.coveredCities || cityData.value.length} 城市`, note: '当前已加载真实岗位聚合指标。' },
  { label: '刷新策略', value: '30 秒', note: '大屏数据定时轮询，适合答辩演示。' }
])

const projectEntrances = [
  { key: 'dashboard' as ModuleKey, title: '就业态势大屏', text: '全国岗位热度、省份地图、城市排行和实时岗位动态。', icon: Gauge },
  { key: 'salary' as ModuleKey, title: '薪资预测决策', text: '按城市、行业、学历、经验和技能估算岗位薪资区间。', icon: ChartColumnIncreasing },
  { key: 'career' as ModuleKey, title: '职业推荐', text: '根据专业、技能和城市偏好生成毕业生投递方向。', icon: Route },
  { key: 'model' as ModuleKey, title: '模型评估中心', text: '展示模型指标、特征工程、训练流程和应用边界。', icon: BrainCircuit },
  { key: 'data' as ModuleKey, title: '数据治理', text: '说明公开数据来源、清洗流程、覆盖口径和质量校验。', icon: Database },
  { key: 'report' as ModuleKey, title: '报告中心', text: '组织毕业论文、答辩演示路线和系统验收功能点。', icon: FileChartColumnIncreasing }
]

const graduationChecks = [
  { label: '真实数据采集与清洗', status: '已完成', progress: 92 },
  { label: '可视化态势大屏', status: '已完成', progress: 90 },
  { label: '薪资预测模型', status: '已接入', progress: 82 },
  { label: '职业推荐功能', status: '已接入', progress: 84 },
  { label: '平台登录与系统页面', status: '本次新增', progress: 78 }
]

const acceptanceItems = [
  { title: '数据真实性', text: '系统指标来自公开岗位数据清洗结果，页面中保留数据来源、样本规模、城市覆盖和有效薪资样本说明。', status: '答辩重点' },
  { title: '功能完整性', text: '覆盖登录、首页、态势大屏、城市评估、薪资预测、技能挖掘、职业推荐、数据治理、模型中心和报告中心。', status: '已覆盖' },
  { title: '模型可解释性', text: '薪资预测展示模型评估指标、训练样本、特征工程和预测影响因子，便于论文和答辩说明。', status: '可截图' },
  { title: '系统可部署性', text: '前端可构建为静态资源，后端由 Python FastAPI 提供接口，适合部署到个人服务器或云服务器。', status: '可部署' }
]

const deployChecklist = [
  { no: '01', title: '前端构建', text: '执行 npm run build 生成 dist 静态文件，部署到 Nginx 或静态托管目录。' },
  { no: '02', title: '后端服务', text: '使用 Python FastAPI 启动接口服务，配置反向代理到 /api。' },
  { no: '03', title: '数据快照', text: '确认 mockData 与后端 demo_data 均使用真实清洗后的岗位指标。' },
  { no: '04', title: '演示口径', text: '答辩时说明澳门、台湾样本不足，不使用虚构数据补齐。' }
]

const salaryFactors = [
  { title: '城市样本', text: '城市岗位数量和公开薪资均值共同影响预测，不再按单一一线城市口径估算。' },
  { title: '行业结构', text: '当前样本以生产制造、专业技术、销售服务、机械加工和生活服务岗位为主。' },
  { title: '学历经验', text: '学历不限、大专、本科与经验不限岗位占比较高，适合分析毕业生可投范围。' },
  { title: '技能标签', text: '生产、管理、销售、机械、沟通、安全、质量、会计等词是当前真实样本高频需求。' }
]

const skillCombos = [
  { title: '生产制造岗', skills: '生产 / 安全 / 质量 / 工艺流程', fit: '高频组合' },
  { title: '销售服务岗', skills: '销售 / 沟通 / 客户服务 / Office', fit: '稳定需求' },
  { title: '机械电气岗', skills: '机械 / 电气 / 设备维护 / 质检', fit: '技术基础' },
  { title: '财务运营岗', skills: '会计 / 财务 / Excel / 采购仓储', fit: '职能岗位' }
]

const careerPaths = [
  { score: 92, title: '生产制造与设备操作', text: '适合工科、机电、材料和应用技术类毕业生，重点关注安全、质量和设备基础。' },
  { score: 86, title: '销售与客户服务', text: '适合管理、营销、商科和服务类专业，岗位数量稳定，核心能力是沟通和执行。' },
  { score: 84, title: '机械电气与质量管理', text: '适合机械、电气、自动化相关专业，建议准备质检、维修和工艺改进经历。' },
  { score: 79, title: '财务行政与运营支持', text: '适合财会、工商管理、物流和信息管理专业，重点准备办公软件和流程意识。' }
]

const capabilityGaps = [
  {
    target: '生产制造与设备操作',
    required: '安全规范、质量意识、设备基础、倒班适应',
    current: '当前准备度 76%',
    action: '补充实训、证书或生产现场经历。',
    priority: '优先补强',
    progress: 76
  },
  {
    target: '销售与客户服务',
    required: '沟通表达、客户跟进、Office、抗压执行',
    current: '当前准备度 72%',
    action: '准备客户沟通案例和业绩复盘。',
    priority: '次优先',
    progress: 72
  },
  {
    target: '财务行政与运营支持',
    required: 'Excel、会计基础、采购仓储、流程记录',
    current: '当前准备度 68%',
    action: '补一份可展示的台账或报表作品。',
    priority: '补充项',
    progress: 68
  }
]

const actionItems = [
  { week: '第 1 周', title: '定位岗位池', text: '按生产制造、销售服务、机械电气、财务运营建立城市和行业清单。' },
  { week: '第 2 周', title: '补齐证明材料', text: '整理实训、证书、实习、项目或报表作品，和目标岗位要求对应。' },
  { week: '第 3 周', title: '模拟面试', text: '围绕安全质量、沟通服务、办公软件和薪资预期做结构化复盘。' },
  { week: '第 4 周', title: '集中投递', text: '优先投递高样本城市，记录反馈后调整简历关键词和期望薪资。' }
]

const pipelineSteps = [
  { title: '真实采集', text: '下载 Kaggle 公开数据集，并采集中国公共招聘网省级岗位列表。' },
  { title: '字段映射', text: '统一岗位名称、城市、省份、薪资、学历、经验、行业、描述等字段。' },
  { title: '清洗标准化', text: '解析薪资区间，标准化学历经验，补全省份和经纬度。' },
  { title: '指标聚合', text: '生成省市就业热度、城市吸引力、应届友好度和行业排行。' },
  { title: '模型训练', text: '训练随机森林薪资模型，输出 MAE、RMSE、R2 等评估结果。' }
]

const modelFeatures = [
  { title: '城市与省份特征', text: '使用城市薪资均值、岗位数量、省份热度作为区域就业环境变量。' },
  { title: '岗位结构特征', text: '提取行业、岗位类别、企业规模、学历和经验要求，支撑薪资区间预测。' },
  { title: '文本技能特征', text: '从岗位描述中抽取生产、管理、销售、机械、沟通、安全、质量等关键词。' },
  { title: '可解释输出', text: '预测结果同时给出影响因子，便于毕业设计答辩解释模型逻辑。' }
]

const trainingSteps = [
  { title: '读取数据', text: '加载 Kaggle 与中国公共招聘网合并后的 project_jobs_real.csv。' },
  { title: '清洗编码', text: '解析薪资区间，处理缺失值，对城市、行业、学历和经验编码。' },
  { title: '训练评估', text: '使用随机森林回归模型训练，输出 MAE、RMSE、R2 指标。' },
  { title: '服务封装', text: '后端提供薪资预测接口，前端提供不可用时的真实数据兜底逻辑。' }
]

const reportSections = [
  { index: '01', title: '绪论与需求分析', text: '说明毕业生就业分析背景、研究意义、目标用户和功能需求。', status: '可写入论文' },
  { index: '02', title: '数据采集与预处理', text: '描述 Kaggle 与公共招聘网数据来源、字段映射、清洗和质量控制。', status: '重点说明' },
  { index: '03', title: '系统设计与实现', text: '展示前后端架构、模块设计、接口设计和可视化组件实现。', status: '已具备页面' },
  { index: '04', title: '模型训练与评估', text: '说明薪资预测模型特征、训练过程、评估指标和误差分析。', status: '可截图' },
  { index: '05', title: '系统测试与总结', text: '整理功能测试、页面截图、接口测试和后续优化方向。', status: '待补测试表' }
]

const systemFeatures = [
  { title: '登录与角色入口', text: '提供教师、学生、管理员角色入口，增强项目完整度和系统感。' },
  { title: '业务分析模块', text: '包含态势大屏、城市评估、薪资预测、技能挖掘和职业推荐。' },
  { title: '数据工程模块', text: '展示真实数据来源、清洗流程、覆盖口径和质量监控。' },
  { title: '模型评估模块', text: '展示模型指标、特征工程、训练流程和使用边界。' },
  { title: '报告与答辩模块', text: '提供论文结构、演示路线和系统验收点，方便毕业答辩。' }
]

const demoRoute = [
  { step: '1', title: '登录平台', text: '展示系统入口、角色和项目名称。' },
  { step: '2', title: '系统首页', text: '说明项目数据规模、核心功能和完成度。' },
  { step: '3', title: '态势大屏', text: '展示全国就业热度地图、城市排行和岗位趋势。' },
  { step: '4', title: '预测推荐', text: '演示薪资预测和职业推荐的交互流程。' },
  { step: '5', title: '数据模型', text: '说明真实数据来源、清洗流程和模型评估指标。' }
]

const adminCards = [
  { title: '用户权限', text: '教师、学生、管理员三类演示角色。', status: '已配置', icon: UsersRound },
  { title: '数据快照', text: '真实岗位聚合指标加载与前端兜底。', status: '运行中', icon: Database },
  { title: '模型服务', text: '薪资预测接口与本地预测逻辑。', status: '可调用', icon: ServerCog },
  { title: '安全控制', text: '登录态、角色展示和退出流程。', status: '演示级', icon: ShieldCheck }
]

const roleRows = [
  { name: '就业指导教师', scope: '查看态势、城市、薪资、技能和推荐结果', permission: '分析与指导' },
  { name: '毕业生用户', scope: '使用薪资预测、职业推荐和技能提升建议', permission: '个人决策' },
  { name: '系统管理员', scope: '查看数据治理、模型评估、运行状态和用户角色', permission: '系统维护' }
]

function handleLogin() {
  if (!loginForm.value.username.trim()) {
    loginForm.value.username = 'admin'
  }
  if (!loginForm.value.password.trim()) {
    loginForm.value.password = '123456'
  }
  isAuthenticated.value = true
  activeModule.value = 'home'
}

function logout() {
  isAuthenticated.value = false
}

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
  grid-template-columns: 15.5rem minmax(0, 1fr);
  gap: var(--space-sm);
  min-height: 100vh;
  min-height: 100dvh;
  overflow: visible;
  padding: var(--space-md);
  color: var(--text);
  background:
    linear-gradient(135deg, color-mix(in oklch, var(--bg), white 3%), color-mix(in oklch, var(--bg-deep), white 5%)),
    radial-gradient(circle at 80% 16%, color-mix(in oklch, var(--accent), transparent 90%), transparent 28rem);
}

.dashboard-shell.sidebar-collapsed {
  grid-template-columns: 4.7rem minmax(0, 1fr);
}

.login-shell {
  position: relative;
  display: grid;
  grid-template-columns: minmax(28rem, 1.05fr) minmax(22rem, 0.72fr);
  align-items: center;
  gap: clamp(1.5rem, 5vw, 5rem);
  min-height: 100vh;
  min-height: 100dvh;
  overflow: auto;
  padding: clamp(1.5rem, 4vw, 4rem);
  color: var(--text);
  background:
    linear-gradient(90deg, color-mix(in oklch, var(--accent), transparent 91%) 1px, transparent 1px),
    linear-gradient(color-mix(in oklch, var(--accent), transparent 93%) 1px, transparent 1px),
    linear-gradient(135deg, oklch(98% 0.007 248), var(--bg-deep));
  background-size: 34px 34px, 34px 34px, auto;
}

.backdrop {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(135deg, transparent 0 47%, color-mix(in oklch, var(--accent), transparent 92%) 47% 48%, transparent 48% 100%),
    radial-gradient(circle at 16% 16%, color-mix(in oklch, var(--accent), transparent 90%), transparent 18rem),
    radial-gradient(circle at 86% 82%, color-mix(in oklch, var(--accent-warm), transparent 90%), transparent 20rem);
  background-size: 64px 64px, auto, auto;
  opacity: 0.86;
}

.backdrop::after {
  content: "";
  position: absolute;
  inset: auto 5% 7% auto;
  width: min(42vw, 34rem);
  height: min(42vw, 34rem);
  border: 1px solid color-mix(in oklch, var(--accent), transparent 74%);
  border-radius: 50%;
  background:
    linear-gradient(90deg, transparent calc(50% - 1px), color-mix(in oklch, var(--accent), transparent 82%) calc(50% - 1px) calc(50% + 1px), transparent calc(50% + 1px)),
    linear-gradient(transparent calc(50% - 1px), color-mix(in oklch, var(--accent), transparent 82%) calc(50% - 1px) calc(50% + 1px), transparent calc(50% + 1px));
  opacity: 0.42;
}

.login-hero,
.login-card,
.platform-sidebar,
.platform-main {
  position: relative;
  z-index: 2;
}

.login-hero {
  display: grid;
  gap: var(--space-lg);
  max-width: 58rem;
}

.login-hero > span,
.topbar__title span,
.sidebar-status b {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

.login-hero h1 {
  margin: 0;
  color: var(--text-strong);
  font-size: clamp(2.1rem, 4.4vw, 4.8rem);
  line-height: 1.12;
  letter-spacing: 0;
}

.login-hero p {
  max-width: 48rem;
  margin: 0;
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.8;
}

.login-insights {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-sm);
}

.login-insights article,
.login-card,
.platform-sidebar,
.thesis-card,
.thesis-mini,
.home-entry,
.model-score-grid article,
.report-layout article,
.admin-grid article,
.role-table article,
.feature-list article,
.demo-route article,
.progress-list article {
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 8px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 1%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: var(--shadow-panel);
}

.thesis-card {
  display: grid;
  gap: var(--space-xs);
  max-width: 48rem;
  padding: var(--space-md);
}

.thesis-card div,
.defense-info article,
.thesis-meta-grid article {
  display: grid;
  gap: 0.15rem;
}

.thesis-card span,
.defense-info span,
.thesis-meta-grid span {
  color: var(--text-muted);
  font-size: 0.72rem;
}

.thesis-card b,
.defense-info b,
.thesis-meta-grid b {
  color: var(--text-strong);
  font-size: 0.9rem;
  line-height: 1.5;
}

.login-insights article {
  display: grid;
  gap: 0.25rem;
  padding: var(--space-md);
}

.login-insights b {
  color: var(--accent-warm);
  font-size: clamp(1.45rem, 3vw, 2.3rem);
  font-variant-numeric: tabular-nums;
}

.login-insights span,
.login-note,
.platform-brand em,
.sidebar-status span,
.sidebar-status em,
.user-card span,
.home-entry span,
.progress-list span,
.model-score-grid em,
.report-layout p,
.report-layout em,
.feature-list span,
.demo-route em,
.admin-grid span,
.admin-grid em,
.role-table span,
.role-table em {
  color: var(--text-muted);
  font-size: 0.82rem;
  line-height: 1.55;
}

.login-card {
  display: grid;
  gap: var(--space-lg);
  padding: var(--space-xl);
}

.login-card__head {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.login-card__head svg {
  color: var(--accent-warm);
}

.login-card__head span {
  color: var(--text-muted);
  font-size: 0.76rem;
}

.login-card__head h2 {
  margin: 0.15rem 0 0;
  color: var(--text-strong);
  font-size: 1.35rem;
}

.login-form {
  display: grid;
  gap: var(--space-xs);
}

.login-button {
  width: 100%;
}

.login-note {
  display: flex;
  justify-content: space-between;
  gap: var(--space-sm);
}

.defense-info {
  display: grid;
  gap: var(--space-xs);
  padding-top: var(--space-sm);
  border-top: 1px dashed color-mix(in oklch, var(--line), transparent 56%);
}

.platform-sidebar {
  display: grid;
  position: sticky;
  top: var(--space-md);
  grid-template-rows: auto auto auto minmax(0, 1fr) auto;
  gap: var(--space-md);
  max-height: calc(100vh - var(--space-md) * 2);
  min-height: calc(100vh - var(--space-md) * 2);
  padding: var(--space-md);
}

.platform-brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.platform-brand > span {
  display: grid;
  place-items: center;
  width: 2.6rem;
  height: 2.6rem;
  border-radius: 8px;
  color: oklch(98% 0.006 250);
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent), black 12%));
  font-weight: 900;
}

.platform-brand b {
  display: block;
  color: var(--text-strong);
}

.sidebar-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  min-height: 2.2rem;
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 7px;
  color: var(--accent);
  background: color-mix(in oklch, var(--panel), white 1%);
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 700;
}

.sidebar-toggle:hover {
  border-color: color-mix(in oklch, var(--accent), transparent 34%);
  background: color-mix(in oklch, var(--accent), transparent 92%);
}

.sidebar-collapsed .platform-sidebar {
  gap: var(--space-sm);
  padding: var(--space-sm);
}

.sidebar-collapsed .platform-brand {
  justify-content: center;
}

.sidebar-collapsed .platform-brand div,
.sidebar-collapsed .thesis-mini,
.sidebar-collapsed .sidebar-status,
.sidebar-collapsed .sidebar-toggle span,
.sidebar-collapsed .module-nav button span {
  display: none;
}

.sidebar-collapsed .module-nav button {
  justify-content: center;
  padding: 0;
}

.thesis-mini {
  display: grid;
  gap: 0.22rem;
  padding: var(--space-sm);
  background: linear-gradient(135deg, color-mix(in oklch, var(--accent), transparent 90%), color-mix(in oklch, var(--panel), white 2%));
}

.thesis-mini span {
  color: var(--text-muted);
  font-size: 0.7rem;
}

.thesis-mini b {
  color: var(--accent);
  font-size: 1rem;
}

.thesis-mini em {
  color: var(--text-muted);
  font-size: 0.72rem;
  font-style: normal;
}

.module-nav {
  display: grid;
  align-content: start;
  gap: var(--space-xs);
  min-height: 0;
  overflow: auto;
}

.sidebar-status {
  display: grid;
  gap: 0.35rem;
  padding: var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 8px;
  background: color-mix(in oklch, var(--surface), white 2%);
}

.platform-main {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: var(--space-sm);
  min-width: 0;
  min-height: calc(100vh - var(--space-md) * 2);
}

.topbar {
  position: relative;
  display: grid;
  grid-template-columns: minmax(18rem, 1fr) minmax(18rem, auto) auto;
  align-items: center;
  gap: var(--space-md);
  min-height: 5.4rem;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid color-mix(in oklch, var(--line), transparent 34%);
  border-radius: 8px;
  background: linear-gradient(110deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--panel-strong), white 1%));
  box-shadow: var(--shadow-panel);
}

.topbar__title {
  display: grid;
  gap: 0.16rem;
}

.topbar__status span {
  color: var(--text-muted);
  font-size: 0.76rem;
}

.topbar h1 {
  margin: 0;
  color: var(--text-strong);
  font-size: 1.58rem;
  font-weight: 800;
  letter-spacing: 0;
}

.module-nav button {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  width: 100%;
  min-height: 2rem;
  padding: 0 var(--space-sm);
  border: 1px solid transparent;
  border-radius: 7px;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  text-align: left;
  transition: transform 180ms var(--ease-out-quint), border-color 180ms var(--ease-out-quint), color 180ms var(--ease-out-quint);
}

.module-nav button:hover,
.module-nav button.active {
  border-color: color-mix(in oklch, var(--accent), transparent 10%);
  color: var(--text-strong);
  transform: translateY(-1px);
}

.module-nav button.active {
  background: color-mix(in oklch, var(--accent), transparent 88%);
  box-shadow: inset 0 0 0 1px color-mix(in oklch, var(--accent), transparent 62%);
}

.topbar__status {
  display: grid;
  justify-items: end;
  gap: 0.3rem;
  text-align: right;
}

.topbar__status strong {
  color: var(--accent);
  font-size: 1rem;
  font-variant-numeric: tabular-nums;
}

.user-card {
  display: grid;
  grid-template-columns: auto minmax(7rem, 1fr) auto;
  align-items: center;
  gap: var(--space-xs);
  min-width: 12rem;
  padding: 0.45rem var(--space-xs);
  border: 1px solid color-mix(in oklch, var(--line), transparent 52%);
  border-radius: 8px;
  background: color-mix(in oklch, var(--surface), white 2%);
}

.user-card svg {
  color: var(--accent);
}

.user-card b {
  display: block;
  color: var(--text);
  font-size: 0.82rem;
}

.user-card button {
  display: grid;
  place-items: center;
  width: 1.9rem;
  height: 1.9rem;
  border-radius: 6px;
  color: var(--text-muted);
  background: color-mix(in oklch, var(--panel-strong), white 2%);
  cursor: pointer;
}

.user-card button:hover {
  color: var(--accent-warm);
}

.screen-grid,
.workbench,
.portal-home {
  position: relative;
  z-index: 1;
  min-height: 0;
}

.portal-home {
  display: grid;
  grid-template-columns: minmax(28rem, 1fr) minmax(24rem, 0.86fr);
  grid-template-rows: auto auto;
  gap: var(--space-sm);
  align-content: start;
  min-height: 100%;
  overflow: visible;
}

.home-hero {
  display: grid;
  align-content: center;
  gap: var(--space-md);
  min-height: 18rem;
  padding: var(--space-xl);
  border: 1px solid color-mix(in oklch, var(--line), transparent 34%);
  border-radius: 8px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--panel-strong), white 1%));
  box-shadow: var(--shadow-panel);
}

.home-hero span {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 800;
}

.home-hero h2 {
  max-width: 54rem;
  margin: 0;
  color: var(--text-strong);
  font-size: clamp(1.8rem, 3.4vw, 3.4rem);
  line-height: 1.08;
}

.home-hero p {
  max-width: 50rem;
  margin: 0;
  color: var(--text-muted);
  font-size: 0.98rem;
  line-height: 1.7;
}

.thesis-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-sm);
}

.thesis-meta-grid article {
  padding: var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--line), transparent 62%);
  border-radius: 7px;
  background: color-mix(in oklch, var(--surface), white 4%);
}

.home-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.home-actions button {
  min-height: 2.35rem;
  padding: 0 var(--space-md);
  border-radius: 7px;
  color: oklch(98% 0.006 250);
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent), black 12%));
  cursor: pointer;
  font-weight: 800;
}

.home-actions button + button {
  color: var(--text);
  background: color-mix(in oklch, var(--surface), white 2%);
  box-shadow: 0 0 0 1px color-mix(in oklch, var(--line), transparent 42%) inset;
}

.home-metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-sm);
}

.home-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-sm);
}

.home-grid:not(.home-grid--narrow) {
  grid-column: 1 / -1;
  grid-template-columns: repeat(6, minmax(0, 1fr));
}

.home-grid--narrow {
  grid-column: span 2;
  grid-template-columns: minmax(24rem, 0.8fr) minmax(28rem, 1.2fr);
  align-items: stretch;
  height: clamp(25rem, 42vh, 28rem);
  min-height: 25rem;
  overflow: hidden;
}

.home-grid--narrow :deep(.shell-panel) {
  height: 100%;
  min-height: 0;
}

.home-grid--narrow :deep(.shell-panel__body) {
  min-height: 0;
  overflow: hidden;
}

.home-grid--narrow :deep(.live-ticker) {
  height: 100%;
  min-height: 0;
  max-height: none;
}

.home-longform {
  grid-column: span 2;
  display: grid;
  grid-template-columns: minmax(26rem, 1fr) minmax(26rem, 1fr);
  gap: var(--space-sm);
  align-items: start;
}

.home-entry {
  display: grid;
  align-content: start;
  gap: var(--space-xs);
  min-height: 8.2rem;
  padding: var(--space-md);
  cursor: pointer;
  transition: transform 180ms var(--ease-out-quint), border-color 180ms var(--ease-out-quint);
}

.home-entry:hover {
  border-color: color-mix(in oklch, var(--accent), transparent 16%);
  transform: translateY(-2px);
}

.home-entry svg,
.admin-grid svg {
  color: var(--accent-warm);
}

.home-entry b,
.progress-list b,
.feature-list b,
.model-score-grid b,
.report-layout b,
.demo-route b,
.admin-grid b,
.role-table b {
  color: var(--text);
}

.screen-grid {
  display: grid;
  grid-template-columns: minmax(20rem, 24rem) minmax(38rem, 1fr) minmax(21rem, 26rem);
  grid-template-rows: minmax(0, 1fr) clamp(9rem, 20vh, 11rem);
  grid-template-areas:
    "left center right"
    "bottom bottom bottom";
  gap: var(--space-sm);
  height: calc(100vh - 7.1rem);
  min-height: 44rem;
}

.workbench {
  display: grid;
  grid-template-columns: minmax(24rem, 1fr) minmax(24rem, 1fr);
  gap: var(--space-sm);
  align-content: start;
  min-height: calc(100vh - 7.1rem);
  overflow: visible;
}

.workbench--career {
  grid-template-rows: auto auto;
  overflow: visible;
}

.workbench--salary {
  grid-template-rows: minmax(19rem, 1.05fr) minmax(18rem, 1fr);
  min-height: calc(100vh - 7.1rem);
  align-content: stretch;
}

.workbench--salary :deep(.shell-panel) {
  height: 100%;
  min-height: 0;
}

.workbench--city > :first-child,
.workbench--data > :first-child,
.workbench--model > :first-child,
.workbench--report > :first-child,
.workbench--admin > :first-child {
  grid-column: span 2;
}

.workbench--model,
.workbench--report,
.workbench--admin {
  grid-template-columns: minmax(24rem, 1fr) minmax(24rem, 1fr);
  grid-auto-rows: minmax(12rem, auto);
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
  grid-template-columns: minmax(25rem, 1.05fr) minmax(28rem, 1.05fr) minmax(23rem, 0.82fr);
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
.quality-grid,
.model-score-grid,
.feature-list,
.report-layout,
.demo-route,
.admin-grid,
.role-table,
.progress-list {
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
.model-score-grid article,
.feature-list article,
.report-layout article,
.demo-route article,
.admin-grid article,
.role-table article,
.progress-list article,
.city-card {
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 7px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 1%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: 0 0.55rem 1.4rem rgba(42, 60, 95, 0.07);
}

.city-strip article {
  display: grid;
  grid-template-columns: 1.55rem minmax(0, 1fr) 2.6rem;
  align-items: center;
  gap: 0.38rem;
  min-width: 0;
  min-height: 3rem;
  padding: 0 0.52rem;
}

.city-strip span,
.pipeline span,
.city-card > span {
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: oklch(98% 0.006 250);
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent), black 12%));
  box-shadow: 0 0.45rem 0.95rem color-mix(in oklch, var(--accent), transparent 82%);
  font-size: 0.72rem;
  font-weight: 800;
}

.city-strip span {
  width: 1.35rem;
  height: 1.35rem;
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

.city-strip b {
  font-size: 0.86rem;
  line-height: 1.05;
}

.city-strip em,
.province-table span,
.skill-table strong,
.city-card footer b {
  color: var(--accent);
  font-style: normal;
  font-variant-numeric: tabular-nums;
}

.city-strip em {
  font-size: 0.82rem;
  text-align: right;
}

.city-workbench {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  gap: var(--space-sm);
  max-height: 38rem;
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in oklch, var(--accent), transparent 42%) transparent;
}

.city-summary {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: var(--space-xs) var(--space-sm);
  min-height: 7.2rem;
  padding: var(--space-md);
  border-color: color-mix(in oklch, var(--accent), transparent 62%);
  background: linear-gradient(135deg, color-mix(in oklch, var(--accent), transparent 90%), color-mix(in oklch, var(--panel), white 2%));
}

.city-summary span {
  grid-row: span 2;
  color: var(--accent);
  font-size: 2rem;
  font-weight: 900;
  font-variant-numeric: tabular-nums;
}

.city-summary b {
  color: var(--text-strong);
}

.city-summary p {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.78rem;
  line-height: 1.5;
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

.city-card h3 em {
  display: inline-flex;
  margin-left: 0.35rem;
  padding: 0.08rem 0.38rem;
  border: 1px solid color-mix(in oklch, var(--accent-warm), transparent 54%);
  border-radius: 999px;
  color: var(--accent-warm);
  font-size: 0.58rem;
  font-style: normal;
  vertical-align: middle;
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
  font-size: 0.82rem;
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
  font-size: 0.76rem;
  font-style: normal;
}

.province-table,
.skill-table {
  display: grid;
  align-content: start;
  gap: var(--space-xs);
  max-height: 34rem;
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
.quality-grid,
.model-score-grid,
.feature-list,
.report-layout,
.demo-route,
.admin-grid,
.role-table,
.progress-list {
  display: grid;
  gap: var(--space-sm);
}

.explain-grid,
.model-score-grid,
.admin-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.benchmark-grid,
.combo-grid,
.quality-grid,
.report-layout {
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
.quality-grid article,
.model-score-grid article,
.feature-list article,
.report-layout article,
.demo-route article,
.admin-grid article,
.role-table article,
.progress-list article {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-md);
}

.path-grid span {
  color: var(--accent-hot);
  font-size: 1.5rem;
  font-weight: 800;
}

.benchmark-grid span,
.quality-grid span,
.model-score-grid span,
.report-layout span,
.demo-route span {
  color: var(--accent-warm);
  font-size: 1.35rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.model-score-grid article {
  min-height: 8rem;
}

.feature-list article,
.role-table article {
  grid-template-columns: minmax(9rem, 0.7fr) minmax(0, 1fr);
  align-items: center;
}

.report-layout article {
  grid-template-columns: 3.5rem minmax(8rem, 0.8fr) minmax(0, 1fr) auto;
  align-items: center;
}

.demo-route article,
.role-table article {
  grid-template-columns: 2.4rem minmax(10rem, 0.75fr) minmax(0, 1fr);
  align-items: center;
}

.admin-grid article {
  align-content: start;
  min-height: 8.6rem;
}

.progress-list {
  align-content: start;
  height: 100%;
  overflow: hidden;
  gap: 0.55rem;
}

.progress-list article {
  gap: 0.32rem;
  min-height: 0;
  padding: 0.55rem var(--space-md);
}

.acceptance-grid,
.deploy-list {
  position: relative;
  z-index: 1;
  display: grid;
  gap: var(--space-sm);
  padding: 0 var(--space-md) var(--space-md);
}

.acceptance-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.acceptance-grid article,
.deploy-list article {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-md);
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 7px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 1%), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: 0 0.55rem 1.4rem rgba(42, 60, 95, 0.07);
}

.deploy-list article {
  grid-template-columns: 2.4rem minmax(8rem, 0.85fr) minmax(0, 1fr);
  align-items: center;
}

.deploy-list span {
  display: grid;
  place-items: center;
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 999px;
  color: oklch(98% 0.006 250);
  background: var(--accent);
  font-size: 0.72rem;
  font-weight: 800;
}

.acceptance-grid b,
.deploy-list b {
  color: var(--text-strong);
}

.acceptance-grid span,
.acceptance-grid em,
.deploy-list em {
  color: var(--text-muted);
  font-size: 0.82rem;
  font-style: normal;
  line-height: 1.55;
}

.acceptance-grid em {
  color: var(--accent);
  font-weight: 700;
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
  min-height: 100%;
}

.workbench--career .path-grid,
.workbench--career .gap-diagnosis {
  grid-auto-rows: auto;
}

.workbench--career .action-list {
  align-content: stretch;
  grid-auto-rows: auto;
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
  background: linear-gradient(90deg, var(--accent), var(--accent-green), var(--accent-warm));
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

@media (max-width: 1280px) {
  .dashboard-shell,
  .login-shell {
    overflow: auto;
  }

  .dashboard-shell,
  .login-shell {
    grid-template-columns: 1fr;
    height: auto;
    min-height: 100vh;
  }

  .platform-sidebar {
    grid-template-rows: auto auto auto;
    position: relative;
    top: auto;
    min-height: auto;
    max-height: none;
  }

  .module-nav {
    grid-template-columns: repeat(auto-fit, minmax(8.6rem, 1fr));
  }

  .topbar,
  .screen-grid,
  .workbench,
  .portal-home {
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

  .home-grid,
  .home-grid--narrow,
  .home-longform,
  .bottom-band,
  .explain-grid,
  .model-score-grid,
  .report-layout,
  .admin-grid,
  .acceptance-grid {
    grid-template-columns: 1fr;
  }

  .home-grid--narrow {
    grid-column: span 1;
  }

  .home-longform {
    grid-column: span 1;
  }
}

@media (max-width: 760px) {
  .dashboard-shell,
  .login-shell {
    padding: var(--space-sm);
  }

  .topbar {
    grid-template-columns: 1fr;
  }

  .topbar__status {
    justify-items: start;
    text-align: left;
  }

  .login-insights,
  .home-metrics,
  .metric-grid,
  .benchmark-grid,
  .combo-grid,
  .quality-grid {
    grid-template-columns: 1fr;
  }

  .report-layout article,
  .feature-list article,
  .demo-route article,
  .role-table article,
  .deploy-list article {
    grid-template-columns: 1fr;
  }
}
</style>
