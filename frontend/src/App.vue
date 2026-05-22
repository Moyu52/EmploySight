<template>
  <main v-if="!isAuthenticated" class="login-shell">
    <div class="backdrop" aria-hidden="true"></div>
    <section class="login-hero">
      <span>Spark Career Intelligence</span>
      <h1>中国就业趋势洞察与职业决策平台</h1>
      <p>面向求职者、就业服务机构和人才运营团队，提供岗位热度、城市机会、薪资参考、技能趋势和职业路径建议。</p>
      <div class="thesis-card">
        <div>
          <span>核心价值</span>
          <b>用岗位数据帮助用户更快判断城市、行业和职业方向</b>
        </div>
        <div>
          <span>服务对象</span>
          <b>求职者、转岗人群、就业指导人员与区域人才服务团队</b>
        </div>
        <div>
          <span>决策场景</span>
          <b>机会发现、薪资预估、技能补强、投递城市筛选</b>
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
          <span>身份访问</span>
          <h2>选择身份进入平台</h2>
        </div>
      </div>
      <div class="identity-guide" aria-label="登录身份说明">
        <div class="identity-guide__row">
          <UserRound :size="18" />
          <div>
            <b>普通用户</b>
            <span>使用默认账号或自定义账号，可进入就业趋势、薪资评估、技能趋势和职业建议模块。</span>
          </div>
        </div>
        <div class="identity-guide__row identity-guide__row--admin">
          <ShieldCheck :size="18" />
          <div>
            <b>管理员身份</b>
            <span>账号填写 <code>admin</code>，输入后端配置的管理员密码后进入平台状态与登录 IP 审计。</span>
          </div>
        </div>
      </div>
      <div class="demo-credentials" aria-label="演示登录账号">
        <article>
          <span>普通用户</span>
          <b>账号：用户</b>
          <em>密码：123456</em>
        </article>
        <article>
          <span>管理员</span>
          <b>账号：admin</b>
          <em>密码：admin123</em>
        </article>
      </div>
      <el-form class="login-form" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="账号">
          <el-input v-model="loginForm.username" size="large" placeholder="普通账号任意填写；管理员请输入 admin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" size="large" type="password" show-password placeholder="普通账号可用默认密码；管理员请输入管理员密码" />
        </el-form-item>
        <p v-if="loginError" class="login-error">{{ loginError }}</p>
        <el-button class="login-button" type="primary" size="large" native-type="button" @click="handleLogin">
          按身份进入平台
        </el-button>
      </el-form>
      <div class="login-note">
        <span>普通账号访问分析平台</span>
        <span>admin 账号解锁管理员审计</span>
      </div>
      <div class="defense-info">
        <article>
          <span>能力范围</span>
          <b>就业趋势洞察、薪资参考、技能趋势和职业建议</b>
        </article>
        <article>
          <span>数据口径</span>
          <b>基于公开招聘样本生成的聚合分析结果</b>
        </article>
      </div>
    </section>
  </main>

  <main v-else class="dashboard-shell" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <div class="backdrop" aria-hidden="true"></div>

    <aside class="platform-sidebar">
      <div class="platform-brand">
        <span>SP</span>
        <div>
          <b>Spark 职业洞察</b>
          <em>就业数据决策平台</em>
        </div>
      </div>
      <button class="sidebar-toggle" type="button" :aria-label="isSidebarCollapsed ? '展开功能导航' : '收起功能导航'" @click="isSidebarCollapsed = !isSidebarCollapsed">
        <PanelLeftClose v-if="!isSidebarCollapsed" :size="16" />
        <PanelLeftOpen v-else :size="16" />
        <span>{{ isSidebarCollapsed ? '展开导航' : '收起导航' }}</span>
      </button>
      <div class="thesis-mini">
        <span>统一访问</span>
        <b>全国岗位观察</b>
        <em>覆盖市场、城市、薪资、技能与平台状态</em>
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
          <span>公开招聘样本 · 聚合趋势分析</span>
          <strong>{{ currentTime }}</strong>
        </div>
        <div class="user-card">
          <UserRound :size="18" />
          <div>
            <b>{{ loginForm.username }}</b>
            <span>统一平台账号</span>
          </div>
          <button type="button" title="退出登录" @click="logout">
            <LogOut :size="16" />
          </button>
        </div>
      </header>

    <section v-if="activeModule === 'home'" class="portal-home">
      <section class="home-hero">
        <span>就业市场总览</span>
        <h2>把岗位、城市、薪资、技能和平台状态放在同一个决策视图里</h2>
        <p>平台将公开招聘样本转化为可阅读的就业市场信号，帮助用户判断机会集中在哪里、薪资区间是否合理、下一步该补强哪些能力。</p>
        <div class="thesis-meta-grid">
          <article>
            <span>岗位规模</span>
            <b>{{ overviewData.totalJobs.toLocaleString('zh-CN') }} 条样本</b>
          </article>
          <article>
            <span>城市覆盖</span>
            <b>{{ overviewData.coveredCities }} 个城市</b>
          </article>
          <article>
            <span>薪资参考</span>
            <b>{{ overviewData.salarySampleRows.toLocaleString('zh-CN') }} 条有效样本</b>
          </article>
        </div>
        <div class="home-actions">
          <button type="button" @click="activeModule = 'dashboard'">查看全国态势</button>
          <button type="button" @click="activeModule = 'career'">生成职业建议</button>
        </div>
      </section>
      <section class="home-metrics">
        <MetricCard label="岗位样本" :value="overviewData.totalJobs" suffix="条记录" icon="jobs" prominent />
        <MetricCard label="薪资样本" :value="overviewData.salarySampleRows" suffix="条记录" icon="salary" prominent />
        <MetricCard label="覆盖城市" :value="overviewData.coveredCities" suffix="个城市" :detail="`地图展示 ${mappableCityCount} 个城市`" icon="city" prominent />
        <MetricCard label="应届友好" :value="overviewData.freshFriendlyIndex" suffix="指数" icon="fresh" :decimals="1" prominent />
      </section>
      <section class="home-grid">
        <article v-for="item in projectEntrances" :key="item.key" class="home-entry" @click="activeModule = item.key">
          <component :is="item.icon" :size="22" />
          <b>{{ item.title }}</b>
          <span>{{ item.text }}</span>
        </article>
      </section>
      <section class="home-grid home-grid--narrow">
        <ShellPanel title="市场重点" subtitle="当前值得关注的就业信号">
          <div class="progress-list">
            <article v-for="item in marketHighlights" :key="item.label">
              <b>{{ item.label }}</b>
              <span>{{ item.status }}</span>
              <div class="score-line"><i :style="{ width: `${item.progress}%` }"></i></div>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="近期岗位样本" subtitle="最新招聘记录">
          <LiveJobTicker :jobs="liveJobData" />
        </ShellPanel>
      </section>
      <section class="home-longform">
        <ShellPanel title="核心能力" subtitle="对外可直接使用的功能">
          <div class="acceptance-grid">
            <article v-for="item in platformCapabilities" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="使用场景" subtitle="从观察到行动">
          <div class="deploy-list">
            <article v-for="item in userScenarios" :key="item.title">
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

        <ShellPanel title="热门城市 TOP10" subtitle="岗位样本排行" dense>
          <AutoRank :items="displayHotCities.hotCities" />
        </ShellPanel>

        <ShellPanel title="热门行业 TOP10" subtitle="机会规模" dense>
          <AutoRank :items="overviewData.hotIndustries" :duration="22" />
        </ShellPanel>
      </aside>

      <section class="center-stage">
        <ShellPanel title="全国就业热度地图" :subtitle="activeProvinceLabel" eyebrow="全国热度">
          <ChinaMap :provinces="provinceData" :cities="cityData" @province-change="activeProvince = $event" />
        </ShellPanel>
      </section>

      <aside class="right-column">
        <ShellPanel title="薪资 · 学历 · 经验" subtitle="结构分布">
          <DistributionCharts :analysis="analysisData" />
        </ShellPanel>

        <ShellPanel title="技能需求热度" subtitle="岗位关键词">
          <SkillCloud :skills="analysisData.skills" />
        </ShellPanel>
      </aside>

      <section class="bottom-band">
        <ShellPanel title="实时就业动态" subtitle="近期岗位样本">
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
        <ShellPanel title="城市就业吸引力评估" :subtitle="`${cityData.length} 个城市样本`">
          <div class="city-workbench">
            <article class="city-summary">
              <span>{{ cityData.length }}</span>
              <b>纳入评估城市</b>
              <p>展示公开招聘样本中具备有效岗位记录的城市，便于比较岗位规模和薪资水平。</p>
            </article>
            <article class="city-summary">
              <span>{{ mappableCityCount }}</span>
              <b>地图展示城市</b>
              <p>具备地理坐标的城市会进入全国热度地图，用于观察区域机会分布。</p>
            </article>
            <article v-for="city in cityData" :key="city.city" class="city-card">
              <span>No.{{ city.rankNo }}</span>
              <h3>
                {{ city.city }}
                <em v-if="!city.hasCoords">待上图</em>
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
        <ShellPanel title="省份机会分布" subtitle="全国省级区域指标">
          <div class="province-table">
            <article v-for="province in sortedProvinces" :key="province.province">
              <b>{{ province.province }}</b>
              <span>{{ province.heatIndex }}</span>
              <em>{{ province.topIndustry }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="城市选择建议" subtitle="投递优先级参考">
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
          <DecisionPanel mode="salary" :cities="cityData" :industries="overviewData.hotIndustries" :skills="analysisData.skills" />
        </ShellPanel>
        <ShellPanel title="薪资结构分析" subtitle="分布动态刷新">
          <DistributionCharts :analysis="analysisData" />
        </ShellPanel>
        <ShellPanel title="薪资影响因素" subtitle="区间参考依据">
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
        <ShellPanel title="技能需求趋势" subtitle="岗位关键词热度">
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
        <ShellPanel title="技能提升建议" subtitle="面向求职准备">
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
        <ShellPanel title="职业路径推荐" subtitle="专业 / 学历 / 技能 / 城市偏好 / 行业偏好">
          <DecisionPanel mode="career" :cities="cityData" :industries="overviewData.hotIndustries" :skills="analysisData.skills" />
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
        <ShellPanel title="数据处理概览" subtitle="公开岗位样本到趋势指标">
          <div class="pipeline">
            <article v-for="(step, index) in pipelineSteps" :key="step.title">
              <span>{{ index + 1 }}</span>
              <b>{{ step.title }}</b>
              <p>{{ step.text }}</p>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="数据覆盖说明" subtitle="公开样本统计口径">
          <div class="coverage-note">
            <p>当前展示数据来自公开招聘样本的聚合分析，共 {{ overviewData.totalJobs.toLocaleString('zh-CN') }} 条岗位；样本时间范围为 {{ overviewData.publishStart || '未知' }} 至 {{ overviewData.publishEnd || '未知' }}，覆盖省级区域 {{ overviewData.coveredRegions || sampledRegionCount }}/{{ overviewData.totalRegions || provinceData.length }}。</p>
            <p>城市覆盖口径为岗位记录中的唯一城市数，共 {{ overviewData.coveredCities || cityData.length }} 个；其中 {{ mappableCityCount }} 个城市进入地图展示。</p>
            <p>样本不足地区会保持谨慎展示，避免用不可靠数据影响判断。</p>
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
        <ShellPanel title="薪资评估可信度" subtitle="参考结果质量">
          <div class="model-score-grid">
            <article v-for="metric in modelMetrics" :key="metric.label">
              <span>{{ metric.value }}</span>
              <b>{{ metric.label }}</b>
              <em>{{ metric.note }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="评估依据" subtitle="主要影响维度">
          <div class="feature-list">
            <article v-for="item in modelFeatures" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="指标生成流程" subtitle="从样本到分析结果">
          <div class="pipeline">
            <article v-for="(step, index) in trainingSteps" :key="step.title">
              <span>{{ index + 1 }}</span>
              <b>{{ step.title }}</b>
              <p>{{ step.text }}</p>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="使用边界" subtitle="结果仅作决策参考">
          <div class="coverage-note">
            <p>薪资评估面向公开岗位样本中的城市、行业、学历、经验、企业规模、岗位类别和技能描述进行区间估计，适合作为投递前参考，不替代企业实际薪酬。</p>
            <p>公开薪资仍会受到企业福利、岗位级别、隐性奖金和招聘策略影响，平台会以区间方式呈现，避免给出绝对结论。</p>
            <p>当样本量不足时，页面会降低置信度并提醒用户结合更多渠道判断。</p>
          </div>
        </ShellPanel>
      </template>

      <template v-if="activeModule === 'report'">
        <ShellPanel title="就业洞察报告" subtitle="关键结论整理">
          <div class="report-layout">
            <article v-for="item in reportSections" :key="item.title">
              <span>{{ item.index }}</span>
              <b>{{ item.title }}</b>
              <p>{{ item.text }}</p>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="平台能力清单" subtitle="核心服务">
          <div class="feature-list">
            <article v-for="item in systemFeatures" :key="item.title">
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="分析路线" subtitle="从市场观察到行动建议">
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
        <ShellPanel title="平台状态" subtitle="访问与数据状态">
          <div class="admin-grid">
            <article v-for="item in adminCards" :key="item.title">
              <component :is="item.icon" :size="22" />
              <b>{{ item.title }}</b>
              <span>{{ item.text }}</span>
              <em>{{ item.status }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="登录 IP 审计" subtitle="管理员安全记录">
          <div v-if="adminSession" class="audit-console">
            <div class="audit-toolbar">
              <el-input v-model="adminAuditQuery" size="large" clearable placeholder="按用户名、IP、状态搜索" @keyup.enter="loadAdminAuditRecords" />
              <el-input v-model="adminDeletePassword" size="large" type="password" show-password placeholder="删除密码" />
              <button type="button" :disabled="adminAuditLoading" @click="loadAdminAuditRecords">
                {{ adminAuditLoading ? '读取中' : '刷新' }}
              </button>
            </div>
            <div class="audit-summary">
              <article>
                <span>{{ adminAuditStats.total }}</span>
                <b>审计记录</b>
              </article>
              <article>
                <span>{{ adminAuditStats.uniqueObservedIps }}</span>
                <b>后端记录 IP</b>
              </article>
              <article>
                <span>{{ adminAuditStats.failedAttempts }}</span>
                <b>失败尝试</b>
              </article>
              <article>
                <span>{{ adminBannedIps.length }}</span>
                <b>封禁 IP</b>
              </article>
            </div>
            <div class="unban-panel">
              <div>
                <b>解除封禁 IP</b>
                <span>用于删除密码输错达到上限后的临时封禁解除，解除密码单独校验。</span>
              </div>
              <el-input v-model="adminUnbanPassword" size="large" type="password" show-password placeholder="解除封禁密码" />
            </div>
            <div class="banned-ip-list">
              <article v-for="item in adminBannedIps" :key="item.ip">
                <b>{{ item.ip }}</b>
                <span>失败 {{ item.attempts }} 次 · 封禁至 {{ formatAuditTime(item.blockedUntil) }}</span>
                <button type="button" :disabled="adminAuditLoading" @click="unbanIp(item.ip)">解除封禁</button>
              </article>
              <div v-if="!adminBannedIps.length" class="audit-empty">暂无被封禁 IP</div>
            </div>
            <p class="audit-note">
              上报 IP 来自代理请求头，可能不可信；后端记录 IP 来自服务端请求对象，仍会受可信代理配置影响，用户使用 VPN 时通常为 VPN 出口。
            </p>
            <p class="audit-warning">
              删除密码最多可连续输错 3 次；输错时会提示剩余机会，达到上限后当前 IP 将被临时封禁，防止暴力破解删除密码。
            </p>
            <p v-if="adminUnbanMessage" class="audit-message">{{ adminUnbanMessage }}</p>
            <p v-if="adminAuditMessage" class="audit-message">{{ adminAuditMessage }}</p>
            <div class="audit-table">
              <div class="audit-table__head">
                <span>用户</span>
                <span>时间</span>
                <span>上报 IP</span>
                <span>后端记录 IP</span>
                <span>来源</span>
                <span>状态</span>
                <span>操作</span>
              </div>
              <article v-for="record in adminAuditRecords" :key="record.id">
                <b>{{ record.username }}</b>
                <span>{{ formatAuditTime(record.loginTime) }}</span>
                <span>{{ record.reportedIp || '未记录' }}</span>
                <span>{{ record.observedIp || '未记录' }}</span>
                <em>{{ auditSourceLabel(record.source) }}</em>
                <em :class="{ failed: record.status === 'failed' }">{{ auditStatusLabel(record.status) }}</em>
                <button type="button" :disabled="adminAuditLoading" @click="removeAuditRecord(record.id)">删除</button>
              </article>
              <div v-if="!adminAuditRecords.length" class="audit-empty">暂无审计记录</div>
            </div>
          </div>
          <div v-else class="audit-locked">
            <ShieldCheck :size="24" />
            <b>管理员审计未解锁</b>
            <span>使用 admin 账号登录后，可查看登录时间、上报 IP、后端记录 IP，并通过删除密码备份后删除记录。</span>
          </div>
        </ShellPanel>
        <ShellPanel title="统一访问" subtitle="单一账号的使用范围">
          <div class="role-table">
            <article v-for="item in accessRows" :key="item.name">
              <b>{{ item.name }}</b>
              <span>{{ item.scope }}</span>
              <em>{{ item.permission }}</em>
            </article>
          </div>
        </ShellPanel>
        <ShellPanel title="服务监控" subtitle="平台可用性状态">
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
  ShieldCheck,
  UserRound,
  UsersRound
} from 'lucide-vue-next'
import { ElMessageBox } from 'element-plus'
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
import {
  ApiRequestError,
  deleteAdminAuditRecord,
  fetchAdminBannedIps,
  fetchAdminAuditRecords,
  fetchAnalysis,
  fetchCities,
  fetchLiveJobs,
  fetchOverview,
  fetchProvinces,
  isAdminDeleteSecurityError,
  loginAdmin,
  recordPlatformLogin,
  unbanAdminIp
} from './services/dashboard'
import { analysis, cityMetrics, liveJobs, overview, provinceMetrics } from './services/mockData'
import type {
  AdminAuditRecord,
  AdminBannedIpRecord,
  AdminSession,
  CityMetric,
  DashboardAnalysis,
  DashboardOverview,
  JobLiveItem,
  ProvinceMetric
} from './types/dashboard'

type ModuleKey = 'home' | 'dashboard' | 'city' | 'salary' | 'skills' | 'career' | 'data' | 'model' | 'report' | 'admin'

const modules = [
  { key: 'home' as ModuleKey, label: '首页', icon: Home },
  { key: 'dashboard' as ModuleKey, label: '全国态势', icon: Gauge },
  { key: 'city' as ModuleKey, label: '城市机会', icon: MapPinned },
  { key: 'salary' as ModuleKey, label: '薪资评估', icon: ChartColumnIncreasing },
  { key: 'skills' as ModuleKey, label: '技能趋势', icon: SearchCode },
  { key: 'career' as ModuleKey, label: '职业建议', icon: Route },
  { key: 'data' as ModuleKey, label: '数据概览', icon: Database },
  { key: 'model' as ModuleKey, label: '模型评估', icon: ServerCog },
  { key: 'report' as ModuleKey, label: '洞察报告', icon: FileChartColumnIncreasing },
  { key: 'admin' as ModuleKey, label: '平台状态', icon: ShieldCheck }
]

const isAuthenticated = ref(false)
const loginForm = ref({
  username: '用户',
  password: '123456'
})
const loginError = ref('')
const adminSession = ref<AdminSession | null>(null)
const adminAuditRecords = ref<AdminAuditRecord[]>([])
const adminAuditQuery = ref('')
const adminAuditLoading = ref(false)
const adminDeletePassword = ref('')
const adminAuditMessage = ref('')
const adminBannedIps = ref<AdminBannedIpRecord[]>([])
const adminUnbanPassword = ref('')
const adminUnbanMessage = ref('')
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
  home: { title: '就业市场首页', group: '平台总览' },
  dashboard: { title: '全国就业态势', group: '市场观察' },
  city: { title: '城市就业吸引力评估', group: '城市分析' },
  salary: { title: '岗位薪资评估', group: '薪资参考' },
  skills: { title: '技能需求趋势', group: '能力洞察' },
  career: { title: '职业路径建议', group: '求职决策' },
  data: { title: '数据概览', group: '样本透明度' },
  model: { title: '薪资评估可信度', group: '质量说明' },
  report: { title: '就业洞察报告', group: '结论整理' },
  admin: { title: '平台状态', group: '服务状态' }
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
const adminAuditStats = computed(() => ({
  total: adminAuditRecords.value.length,
  uniqueObservedIps: new Set(adminAuditRecords.value.map((item) => item.observedIp).filter(Boolean)).size,
  failedAttempts: adminAuditRecords.value.filter((item) => item.status === 'failed').length
}))

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
    return '省份热度轮播'
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
  { title: '样本规模城市', text: `${topCityNames.value || '当前高样本城市'}岗位规模靠前，适合优先观察机会密度。`, metric: '规模优先' },
  { title: '制造业承接城市', text: `${manufacturingCityNames.value || '制造业样本城市'}兼具岗位数量和制造业、专业技术岗位基础。`, metric: '产业匹配' },
  { title: '应届友好城市', text: `${freshFriendlyCityNames.value || '应届友好城市'}经验门槛相对友好，可作为稳妥投递池。`, metric: '门槛较低' },
  { title: '地图展示口径', text: `城市评估展示 ${cityData.value.length} 个样本城市，地图展示 ${mappableCityCount.value} 个具备坐标的城市。`, metric: '口径一致' }
])
const salaryBenchmarks = computed(() => [
  { label: '主体区间', value: analysisData.value.salaryRanges[0]?.name ?? '未知', note: '当前样本中占比最高，适合作为保守薪资预期。' },
  { label: '提升区间', value: analysisData.value.salaryRanges[1]?.name ?? '未知', note: '第二高占比区间，需要结合城市、行业和岗位技能判断。' },
  { label: '冲刺区间', value: '10K+', note: '占比较小，多出现在样本较少的一线城市或专业技术岗位。' },
  { label: '全样本均值', value: overviewData.value.averageSalary.toLocaleString('zh-CN'), note: `基于 ${overviewData.value.salarySampleRows.toLocaleString('zh-CN')} 条有效薪资样本解析得到。` }
])
const qualityMetrics = computed(() => [
  { label: '省级样本覆盖', value: `${overviewData.value.coveredRegions || sampledRegionCount.value}/${overviewData.value.totalRegions || provinceData.value.length}`, note: '只统计公开岗位样本，样本不足地区谨慎展示。' },
  { label: '覆盖城市', value: `${overviewData.value.coveredCities || cityData.value.length}`, note: '来自公开岗位记录，城市评估页完整展示。' },
  { label: '地图展示城市', value: `${mappableCityCount.value}`, note: '具备地理坐标，可用于全国热度地图。' },
  { label: '有效薪资样本', value: `${overviewData.value.salarySampleRows.toLocaleString('zh-CN')}`, note: '用于薪资分布和区间参考。' }
])
const modelMetrics = computed(() => [
  { label: '平均偏差', value: '1,560.88', note: '薪资参考与样本薪资的平均偏差，单位为元。' },
  { label: '波动范围', value: '2,678.21', note: '用于衡量高低薪岗位带来的区间波动。' },
  { label: '解释能力', value: '44.31%', note: '公开岗位薪资受城市、行业、经验和企业等多因素影响。' },
  { label: '参考样本', value: `${overviewData.value.salarySampleRows.toLocaleString('zh-CN')}`, note: '使用有效薪资岗位记录生成参考区间。' }
])
const runtimeStatus = computed(() => [
  { label: '平台访问', value: '正常', note: '核心页面可正常访问。' },
  { label: '数据服务', value: '稳定', note: '聚合指标已加载，异常时保留最近一次有效快照。' },
  { label: '数据快照', value: `${overviewData.value.coveredCities || cityData.value.length} 城市`, note: '当前已加载岗位聚合指标。' },
  { label: '刷新策略', value: '30 秒', note: '就业态势页面定时刷新。' }
])

const projectEntrances = [
  { key: 'dashboard' as ModuleKey, title: '全国态势', text: '查看岗位热度、省份地图、城市排行和近期岗位动态。', icon: Gauge },
  { key: 'city' as ModuleKey, title: '城市机会', text: '比较城市岗位规模、薪资水平和应届友好度。', icon: MapPinned },
  { key: 'salary' as ModuleKey, title: '薪资评估', text: '按城市、行业、学历、经验和技能估算岗位薪资区间。', icon: ChartColumnIncreasing },
  { key: 'skills' as ModuleKey, title: '技能趋势', text: '观察不同岗位描述中的高频能力要求。', icon: SearchCode },
  { key: 'career' as ModuleKey, title: '职业建议', text: '根据专业、技能和城市偏好生成投递方向。', icon: Route },
  { key: 'data' as ModuleKey, title: '数据概览', text: '查看样本来源、处理流程、覆盖范围和质量口径。', icon: Database },
  { key: 'model' as ModuleKey, title: '模型评估', text: '查看薪资参考模型的误差、特征和可信度边界。', icon: ServerCog },
  { key: 'admin' as ModuleKey, title: '平台状态', text: '查看统一入口、数据服务、薪资服务和运行状态。', icon: ShieldCheck },
  { key: 'report' as ModuleKey, title: '洞察报告', text: '整理市场信号、城市机会和行动建议。', icon: FileChartColumnIncreasing }
]

const marketHighlights = [
  { label: '城市机会集中度', status: '重点关注头部城市岗位密度', progress: 92 },
  { label: '薪资参考完整度', status: '有效薪资样本支撑区间判断', progress: 88 },
  { label: '应届友好程度', status: '经验门槛较低岗位可优先筛选', progress: 82 },
  { label: '技能需求热度', status: '生产、销售、质量、沟通等词频较高', progress: 86 },
  { label: '近期岗位活跃度', status: '持续追踪公开招聘样本变化', progress: 80 }
]

const platformCapabilities = [
  { title: '就业态势观察', text: '通过省份、城市、行业和岗位趋势，快速理解当前招聘市场热度。', status: '市场视图' },
  { title: '城市机会比较', text: '综合岗位数量、薪资水平和应届友好度，为城市选择提供参考。', status: '城市评估' },
  { title: '薪资区间参考', text: '按城市、行业、学历和经验生成薪资区间，辅助判断期望薪资是否合理。', status: '薪资参考' },
  { title: '职业行动建议', text: '结合技能趋势和岗位方向，输出更清晰的投递和能力补强路径。', status: '行动建议' }
]

const userScenarios = [
  { no: '01', title: '选城市', text: '先看岗位规模和应届友好度，再结合薪资水平选择投递城市。' },
  { no: '02', title: '定薪资', text: '用区间结果校准期望薪资，避免过低或过高影响沟通效率。' },
  { no: '03', title: '补技能', text: '根据高频技能词调整简历关键词，并补充可证明的项目或实训经历。' },
  { no: '04', title: '排优先级', text: '按城市、行业和匹配度建立投递清单，持续记录反馈并调整方向。' }
]

const salaryFactors = [
  { title: '城市样本', text: '城市岗位数量和公开薪资均值共同影响预测，不再按单一一线城市口径估算。' },
  { title: '行业结构', text: '当前样本以生产制造、专业技术、销售服务、机械加工和生活服务岗位为主。' },
  { title: '学历经验', text: '学历不限、大专、本科与经验不限岗位占比较高，适合分析求职者可投范围。' },
  { title: '技能标签', text: '生产、管理、销售、机械、沟通、安全、质量、会计等词是当前真实样本高频需求。' }
]

const skillCombos = [
  { title: '生产制造岗', skills: '生产 / 安全 / 质量 / 工艺流程', fit: '高频组合' },
  { title: '销售服务岗', skills: '销售 / 沟通 / 客户服务 / Office', fit: '稳定需求' },
  { title: '机械电气岗', skills: '机械 / 电气 / 设备维护 / 质检', fit: '技术基础' },
  { title: '财务运营岗', skills: '会计 / 财务 / Excel / 采购仓储', fit: '职能岗位' }
]

const careerPaths = [
  { score: 92, title: '生产制造与设备操作', text: '适合工科、机电、材料和应用技术类求职者，重点关注安全、质量和设备基础。' },
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
  { title: '影响因素输出', text: '薪资结果同时给出关键影响因素，帮助用户理解区间变化来源。' }
]

const trainingSteps = [
  { title: '样本汇总', text: '汇总公开招聘岗位样本，并按城市、行业、薪资、学历和经验建立统一口径。' },
  { title: '质量校验', text: '识别缺失值和异常薪资，确保进入页面的指标可用于对比。' },
  { title: '指标计算', text: '生成城市吸引力、行业热度、技能热度和薪资区间参考。' },
  { title: '结果更新', text: '在平台页面展示最新可用快照，并保留清晰的数据时间范围。' }
]

const reportSections = [
  { index: '01', title: '市场总览', text: '概括岗位规模、城市覆盖、薪资样本和近期趋势。', status: '概览' },
  { index: '02', title: '城市机会', text: '比较岗位数量、薪资水平、应届友好度和区域分布。', status: '城市' },
  { index: '03', title: '行业与技能', text: '整理高频行业和能力关键词，辅助简历和学习计划调整。', status: '能力' },
  { index: '04', title: '薪资参考', text: '展示不同城市、行业、学历和经验下的薪资区间。', status: '薪资' },
  { index: '05', title: '行动建议', text: '形成投递优先级、能力补强和复盘节奏建议。', status: '行动' }
]

const systemFeatures = [
  { title: '统一访问入口', text: '支持单一账号查看核心市场指标和完整分析模块。' },
  { title: '市场分析模块', text: '包含全国态势、城市机会、薪资评估、技能趋势和职业建议。' },
  { title: '数据透明度', text: '展示样本时间范围、覆盖城市、有效薪资样本和质量口径。' },
  { title: '薪资参考模块', text: '呈现薪资区间、影响因素和使用边界，避免绝对化判断。' },
  { title: '洞察报告模块', text: '把关键趋势整理为可阅读的结论和行动建议。' }
]

const demoRoute = [
  { step: '1', title: '看市场', text: '从首页了解岗位规模、城市覆盖和近期就业信号。' },
  { step: '2', title: '选城市', text: '比较城市吸引力、薪资水平和应届友好度。' },
  { step: '3', title: '定方向', text: '结合行业热度和技能趋势锁定职业路径。' },
  { step: '4', title: '估薪资', text: '用区间结果校准期望薪资和投递优先级。' },
  { step: '5', title: '做行动', text: '形成技能补强、简历关键词和投递节奏建议。' }
]

const adminCards = [
  { title: '统一入口', text: '单一账号进入完整平台，所有分析入口统一展示。', status: '可用', icon: UsersRound },
  { title: '数据快照', text: '岗位聚合指标已加载，页面展示当前可用样本。', status: '运行中', icon: Database },
  { title: '薪资服务', text: '薪资区间和影响因素可正常生成。', status: '可用', icon: ServerCog },
  { title: '访问控制', text: '保留登录态、账号展示和退出流程。', status: '可用', icon: ShieldCheck }
]

const accessRows = [
  { name: '市场洞察', scope: '查看首页、全国就业态势、城市机会和技能趋势', permission: '统一开放' },
  { name: '个人决策', scope: '使用薪资评估、职业路径建议和技能提升建议', permission: '统一开放' },
  { name: '平台管理', scope: '查看数据概览、模型评估、洞察报告和平台状态', permission: '统一开放' }
]

function auditSourceLabel(source: string) {
  return source === 'admin' ? '管理员' : '平台'
}

function auditStatusLabel(status: string) {
  return status === 'failed' ? '失败' : '成功'
}

function formatAuditTime(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date)
}

function formatBlockedUntil(value: string) {
  if (!value) {
    return ''
  }
  return formatAuditTime(value)
}

function adminDeleteErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError && isAdminDeleteSecurityError(error.detail)) {
    const detail = error.detail
    if (detail.banned) {
      const blockedUntil = formatBlockedUntil(detail.blockedUntil)
      return blockedUntil
        ? `删除密码错误次数过多，当前 IP 已被封禁，请在 ${blockedUntil} 后再试。`
        : '删除密码错误次数过多，当前 IP 已被封禁，请稍后再试。'
    }
    return `删除密码错误，还剩 ${detail.remainingAttempts} 次机会，否则当前 IP 将会被封禁。`
  }
  if (error instanceof ApiRequestError && error.status === 404) {
    return '删除失败，该审计记录不存在或已被删除。'
  }
  if (error instanceof ApiRequestError && error.status === 401) {
    return '删除失败，管理员会话已失效，请重新登录。'
  }
  return '删除失败，请检查删除密码或管理员会话。'
}

async function loadAdminAuditRecords() {
  if (!adminSession.value) {
    return
  }
  adminAuditLoading.value = true
  adminAuditMessage.value = ''
  try {
    adminAuditRecords.value = await fetchAdminAuditRecords(adminSession.value.token, adminAuditQuery.value)
    adminBannedIps.value = await fetchAdminBannedIps(adminSession.value.token)
  } catch {
    adminAuditMessage.value = '审计记录读取失败，请确认后端服务和管理员会话仍然有效。'
  } finally {
    adminAuditLoading.value = false
  }
}

async function unbanIp(ip: string) {
  if (!adminSession.value) {
    adminUnbanMessage.value = '请先使用管理员账号登录。'
    return
  }
  if (!adminUnbanPassword.value.trim()) {
    adminUnbanMessage.value = '解除封禁前需要输入解除封禁密码。'
    return
  }
  try {
    await ElMessageBox.confirm(
      `确认解除 ${ip} 的删除操作封禁吗？`,
      '确认解除封禁',
      {
        confirmButtonText: '确认解除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch {
    adminUnbanMessage.value = '已取消解除封禁操作。'
    return
  }

  adminAuditLoading.value = true
  adminUnbanMessage.value = ''
  try {
    const result = await unbanAdminIp(adminSession.value.token, ip, adminUnbanPassword.value)
    adminUnbanMessage.value = result.unbanned ? `已解除 ${result.ip} 的封禁。` : `${result.ip} 当前没有封禁记录。`
    adminBannedIps.value = await fetchAdminBannedIps(adminSession.value.token)
  } catch (error) {
    if (error instanceof ApiRequestError && error.status === 403) {
      adminUnbanMessage.value = '解除封禁密码错误。'
    } else if (error instanceof ApiRequestError && error.status === 401) {
      adminUnbanMessage.value = '解除失败，管理员会话已失效，请重新登录。'
    } else {
      adminUnbanMessage.value = '解除封禁失败，请稍后重试。'
    }
  } finally {
    adminAuditLoading.value = false
  }
}

async function removeAuditRecord(recordId: string) {
  if (!adminSession.value) {
    adminAuditMessage.value = '请先使用管理员账号登录。'
    return
  }
  if (!adminDeletePassword.value.trim()) {
    adminAuditMessage.value = '删除记录前需要输入删除密码。'
    return
  }
  const record = adminAuditRecords.value.find((item) => item.id === recordId)
  try {
    await ElMessageBox.confirm(
      `确认删除 ${record?.username || '该用户'} 的这条登录审计记录吗？删除前系统会自动备份审计文件。`,
      '确认删除审计记录',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        distinguishCancelAndClose: true
      }
    )
  } catch {
    adminAuditMessage.value = '已取消删除操作。'
    return
  }
  adminAuditLoading.value = true
  adminAuditMessage.value = ''
  try {
    const result = await deleteAdminAuditRecord(adminSession.value.token, recordId, adminDeletePassword.value)
    adminAuditMessage.value = `记录已删除，备份文件：${result.backupFile}`
    await loadAdminAuditRecords()
  } catch (error) {
    adminAuditMessage.value = adminDeleteErrorMessage(error)
    if (error instanceof ApiRequestError && isAdminDeleteSecurityError(error.detail) && error.detail.banned && adminSession.value) {
      adminBannedIps.value = await fetchAdminBannedIps(adminSession.value.token).catch(() => adminBannedIps.value)
    }
  } finally {
    adminAuditLoading.value = false
  }
}

async function handleLogin() {
  loginError.value = ''
  if (!loginForm.value.username.trim()) {
    loginForm.value.username = '用户'
  }
  if (!loginForm.value.password.trim()) {
    loginForm.value.password = '123456'
  }
  const username = loginForm.value.username.trim()
  const password = loginForm.value.password

  if (username.toLowerCase() === 'admin') {
    try {
      loginForm.value.username = 'admin'
      adminSession.value = await loginAdmin('admin', password)
      isAuthenticated.value = true
      activeModule.value = 'admin'
      await loadAdminAuditRecords()
    } catch {
      adminSession.value = null
      loginError.value = '管理员账号或密码错误，或后端服务未启动。'
    }
    return
  }

  adminSession.value = null
  adminAuditRecords.value = []
  isAuthenticated.value = true
  activeModule.value = 'home'
  void recordPlatformLogin(username).catch(() => undefined)
}

function logout() {
  isAuthenticated.value = false
  adminSession.value = null
  adminAuditRecords.value = []
  adminBannedIps.value = []
  adminDeletePassword.value = ''
  adminUnbanPassword.value = ''
  adminAuditMessage.value = ''
  adminUnbanMessage.value = ''
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
    linear-gradient(135deg, color-mix(in oklch, var(--bg), white 3%), color-mix(in oklch, var(--bg-deep), white 6%)),
    linear-gradient(90deg, color-mix(in oklch, var(--accent), transparent 96%) 1px, transparent 1px),
    linear-gradient(color-mix(in oklch, var(--accent), transparent 97%) 1px, transparent 1px);
  background-size: auto, 44px 44px, 44px 44px;
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
    linear-gradient(135deg, oklch(99% 0.004 238), var(--bg-deep)),
    linear-gradient(90deg, color-mix(in oklch, var(--accent), transparent 94%) 1px, transparent 1px),
    linear-gradient(color-mix(in oklch, var(--accent), transparent 96%) 1px, transparent 1px);
  background-size: auto, 36px 36px, 36px 36px;
}

.backdrop {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(135deg, transparent 0 47%, color-mix(in oklch, var(--accent), transparent 94%) 47% 48%, transparent 48% 100%);
  background-size: 72px 72px;
  opacity: 0.48;
}

.backdrop::after {
  content: none;
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
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 3%));
  box-shadow: var(--shadow-panel);
}

.thesis-card {
  display: grid;
  gap: var(--space-xs);
  max-width: 48rem;
  padding: var(--space-md);
}

.thesis-card div,
.identity-guide__row,
.defense-info article,
.thesis-meta-grid article {
  display: grid;
  gap: 0.15rem;
}

.thesis-card span,
.identity-guide__row span,
.defense-info span,
.thesis-meta-grid span {
  color: var(--text-muted);
  font-size: 0.72rem;
  line-height: 1.55;
}

.thesis-card b,
.identity-guide__row b,
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

.identity-guide {
  display: grid;
  gap: var(--space-xs);
}

.demo-credentials {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-xs);
}

.demo-credentials article {
  display: grid;
  gap: 0.18rem;
  padding: 0.75rem;
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 70%);
  border-radius: 7px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--official-blue-soft), white 2%), var(--panel));
}

.demo-credentials span {
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 700;
}

.demo-credentials b,
.demo-credentials em {
  color: var(--official-blue-deep);
  font-size: 0.86rem;
  font-style: normal;
  line-height: 1.45;
  overflow-wrap: anywhere;
}

.demo-credentials em {
  color: var(--official-blue);
  font-weight: 800;
}

.identity-guide__row {
  grid-template-columns: 2.15rem minmax(0, 1fr);
  align-items: start;
  padding: 0.75rem;
  border: 1px solid color-mix(in oklch, var(--line), transparent 54%);
  border-radius: 7px;
  background: color-mix(in oklch, var(--panel), white 1%);
}

.identity-guide__row svg {
  display: block;
  margin-top: 0.1rem;
  color: var(--accent);
}

.identity-guide__row--admin {
  border-color: color-mix(in oklch, var(--official-gold), transparent 58%);
  background:
    linear-gradient(90deg, color-mix(in oklch, var(--official-gold), transparent 86%) 0 0.18rem, transparent 0.18rem 100%),
    color-mix(in oklch, var(--official-blue-soft), white 4%);
}

.identity-guide__row--admin svg,
.identity-guide__row--admin b {
  color: var(--official-blue-deep);
}

.identity-guide code {
  padding: 0.08rem 0.32rem;
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 72%);
  border-radius: 5px;
  color: var(--official-blue-deep);
  background: color-mix(in oklch, var(--panel), white 2%);
  font-family: "Cascadia Mono", "Consolas", monospace;
  font-size: 0.76rem;
  font-weight: 800;
}

.login-form {
  display: grid;
  gap: var(--space-xs);
}

.login-error {
  margin: 0;
  padding: 0.65rem 0.75rem;
  border: 1px solid color-mix(in oklch, var(--accent-hot), transparent 58%);
  border-radius: 7px;
  color: var(--accent-hot);
  background: color-mix(in oklch, var(--accent-hot), transparent 94%);
  font-size: 0.82rem;
  line-height: 1.5;
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
  font-size: clamp(1.75rem, 2.8vw, 2.85rem);
  line-height: 1.15;
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
  grid-template-rows: repeat(2, minmax(0, 1fr));
  grid-auto-rows: minmax(0, 1fr);
  gap: var(--space-sm);
  align-self: stretch;
  min-height: 0;
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

.workbench--admin > :nth-child(2) {
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

.audit-console {
  display: grid;
  gap: var(--space-sm);
}

.audit-toolbar {
  display: grid;
  grid-template-columns: minmax(16rem, 1fr) minmax(12rem, 0.5fr) auto;
  gap: var(--space-sm);
  align-items: center;
}

.audit-toolbar button,
.audit-table button {
  min-height: 2.35rem;
  border: 1px solid color-mix(in oklch, var(--accent), transparent 58%);
  border-radius: 7px;
  color: var(--text-strong);
  background: color-mix(in oklch, var(--surface), white 2%);
  cursor: pointer;
  font-weight: 800;
}

.audit-toolbar button {
  padding: 0 var(--space-md);
  color: oklch(98% 0.006 250);
  background: linear-gradient(135deg, var(--accent), color-mix(in oklch, var(--accent), black 12%));
}

.audit-toolbar button:disabled,
.audit-table button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.audit-summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-sm);
}

.audit-summary article,
.banned-ip-list article,
.audit-table article,
.audit-locked {
  display: grid;
  gap: var(--space-xs);
  padding: var(--space-md);
  border: 1px solid color-mix(in oklch, var(--line), transparent 58%);
  border-radius: 8px;
  background: linear-gradient(135deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 3%));
  box-shadow: var(--shadow-panel);
}

.unban-panel {
  display: grid;
  grid-template-columns: minmax(16rem, 1fr) minmax(14rem, 0.52fr);
  gap: var(--space-sm);
  align-items: center;
  padding: var(--space-md);
  border: 1px solid color-mix(in oklch, var(--accent-hot), transparent 68%);
  border-radius: 8px;
  background: color-mix(in oklch, var(--accent-hot), transparent 96%);
}

.unban-panel div {
  display: grid;
  gap: 0.2rem;
  min-width: 0;
}

.unban-panel b,
.banned-ip-list b {
  color: var(--text-strong);
}

.unban-panel span,
.banned-ip-list span {
  color: var(--text-muted);
  font-size: 0.78rem;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.banned-ip-list {
  display: grid;
  gap: 0.45rem;
}

.banned-ip-list article {
  grid-template-columns: minmax(8rem, 0.5fr) minmax(14rem, 1fr) auto;
  align-items: center;
  box-shadow: none;
}

.banned-ip-list button {
  min-height: 2rem;
  padding: 0 var(--space-sm);
  border: 1px solid color-mix(in oklch, var(--accent-hot), transparent 62%);
  border-radius: 7px;
  color: var(--accent-hot);
  background: color-mix(in oklch, var(--panel), white 2%);
  cursor: pointer;
  font-weight: 800;
}

.banned-ip-list button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.audit-summary span {
  color: var(--accent-warm);
  font-size: 1.55rem;
  font-weight: 900;
  font-variant-numeric: tabular-nums;
}

.audit-summary b,
.audit-locked b {
  color: var(--text-strong);
}

.audit-note,
.audit-warning,
.audit-message {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.82rem;
  line-height: 1.6;
}

.audit-warning {
  color: var(--accent-hot);
}

.audit-message {
  color: var(--accent-warm);
}

.audit-table {
  display: grid;
  gap: 0.45rem;
  overflow-x: auto;
}

.audit-table__head,
.audit-table article {
  display: grid;
  grid-template-columns: minmax(6rem, 0.7fr) minmax(8rem, 0.8fr) minmax(9rem, 1fr) minmax(9rem, 1fr) minmax(5rem, 0.55fr) minmax(4.5rem, 0.45fr) minmax(4.8rem, 0.45fr);
  align-items: center;
  gap: 0.65rem;
  min-width: 58rem;
}

.audit-table__head {
  padding: 0 0.35rem;
  color: var(--text-muted);
  font-size: 0.74rem;
  font-weight: 800;
}

.audit-table article {
  padding: 0.75rem;
  box-shadow: none;
}

.audit-table b {
  color: var(--text-strong);
  overflow-wrap: anywhere;
}

.audit-table span,
.audit-table em,
.audit-empty,
.audit-locked span {
  color: var(--text-muted);
  font-size: 0.78rem;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.audit-table em {
  color: var(--accent);
  font-style: normal;
  font-weight: 800;
}

.audit-table em.failed {
  color: var(--accent-hot);
}

.audit-table button {
  min-height: 2rem;
  color: var(--accent-hot);
  border-color: color-mix(in oklch, var(--accent-hot), transparent 62%);
  background: color-mix(in oklch, var(--accent-hot), transparent 94%);
}

.audit-empty {
  padding: var(--space-md);
  border: 1px dashed color-mix(in oklch, var(--line), transparent 46%);
  border-radius: 8px;
  text-align: center;
}

.audit-locked {
  justify-items: start;
}

.audit-locked svg {
  color: var(--accent-warm);
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

.action-list span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4.35rem;
  min-height: 1.45rem;
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 78%);
  border-radius: 999px;
  color: var(--official-blue);
  background: color-mix(in oklch, var(--official-blue-soft), white 4%);
  box-shadow: inset 0 1px 0 color-mix(in oklch, white, transparent 18%);
  font-weight: 700;
  white-space: nowrap;
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

/* Official release polish */
.dashboard-shell {
  grid-template-columns: 16rem minmax(0, 1fr);
  gap: 1rem;
  padding: 1rem;
  overflow-x: hidden;
  background:
    linear-gradient(180deg, color-mix(in oklch, var(--panel), white 1%) 0, color-mix(in oklch, var(--bg), white 1%) 18rem, var(--bg-deep) 100%),
    linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 96%) 1px, transparent 1px),
    linear-gradient(color-mix(in oklch, var(--official-blue), transparent 97%) 1px, transparent 1px);
  background-size: auto, 48px 48px, 48px 48px;
}

.dashboard-shell.sidebar-collapsed {
  grid-template-columns: 4.7rem minmax(0, 1fr);
}

.login-shell {
  background:
    linear-gradient(118deg, color-mix(in oklch, var(--official-blue-soft), white 5%) 0 36%, color-mix(in oklch, var(--panel), white 1%) 36% 100%),
    linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 95%) 1px, transparent 1px),
    linear-gradient(color-mix(in oklch, var(--official-blue), transparent 97%) 1px, transparent 1px);
  background-size: auto, 40px 40px, 40px 40px;
}

.backdrop {
  background:
    linear-gradient(120deg, transparent 0 64%, color-mix(in oklch, var(--official-blue), transparent 95%) 64% 64.4%, transparent 64.4% 100%),
    linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 97%) 1px, transparent 1px);
  background-size: 88px 88px, 56px 56px;
  opacity: 0.62;
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
.progress-list article,
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
.acceptance-grid article,
.deploy-list article,
.city-card {
  border-color: color-mix(in oklch, var(--line), transparent 42%);
  background: linear-gradient(180deg, color-mix(in oklch, var(--panel), white 2%), color-mix(in oklch, var(--surface), white 1%));
  box-shadow: 0 0.55rem 1.25rem rgba(20, 52, 99, 0.055);
}

.platform-sidebar {
  gap: 0.85rem;
  padding: 0.85rem;
  border-color: color-mix(in oklch, var(--official-blue), transparent 72%);
  background:
    linear-gradient(180deg, var(--panel), color-mix(in oklch, var(--official-blue-soft), white 4%)),
    linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 86%) 0 3px, transparent 3px 100%);
  box-shadow: var(--shadow-raised);
}

.platform-sidebar::before,
.topbar::before,
.home-hero::before {
  content: "";
  position: absolute;
  pointer-events: none;
}

.platform-sidebar::before {
  inset: 0 auto 0 0;
  width: 3px;
  border-radius: 8px 0 0 8px;
  background: linear-gradient(
    180deg,
    color-mix(in oklch, var(--official-blue), transparent 70%),
    color-mix(in oklch, var(--official-gold), transparent 76%)
  );
}

.platform-brand > span {
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 72%);
  color: var(--official-blue);
  background: linear-gradient(135deg, color-mix(in oklch, var(--official-blue-soft), white 3%), var(--panel));
  box-shadow: inset 0 1px 0 color-mix(in oklch, white, transparent 18%);
}

.platform-brand b {
  color: var(--official-blue-deep);
  font-size: 0.98rem;
}

.sidebar-toggle,
.module-nav button,
.sidebar-status,
.user-card,
.thesis-mini {
  background: color-mix(in oklch, var(--panel), white 1%);
}

.sidebar-toggle {
  min-height: 2.35rem;
  border-color: color-mix(in oklch, var(--official-blue), transparent 78%);
  color: var(--official-blue);
}

.module-nav {
  gap: 0.38rem;
  padding-right: 0.1rem;
}

.module-nav button {
  min-height: 2.35rem;
  padding: 0 0.7rem;
  border-color: transparent;
  border-left: 3px solid transparent;
  border-radius: 6px;
  font-weight: 700;
}

.module-nav button svg {
  flex: 0 0 auto;
}

.module-nav button:hover,
.module-nav button.active {
  border-color: color-mix(in oklch, var(--official-blue), transparent 76%);
  border-left-color: var(--official-blue);
  color: var(--official-blue-deep);
  background: color-mix(in oklch, var(--official-blue-soft), white 2%);
  transform: none;
}

.module-nav button.active {
  box-shadow: inset 0 0 0 1px color-mix(in oklch, var(--official-blue), transparent 82%);
}

.thesis-mini,
.sidebar-status {
  border-color: color-mix(in oklch, var(--line), transparent 46%);
}

.thesis-mini {
  background: linear-gradient(135deg, color-mix(in oklch, var(--official-blue-soft), white 2%), var(--panel));
}

.thesis-mini b,
.sidebar-status b,
.topbar__title span,
.login-hero > span,
.home-hero span {
  color: var(--official-blue);
}

.platform-main {
  gap: 1rem;
}

.topbar {
  min-height: 4.9rem;
  padding: 0.7rem 0.95rem;
  border-color: color-mix(in oklch, var(--official-blue), transparent 72%);
  background: linear-gradient(180deg, var(--panel), color-mix(in oklch, var(--surface), white 2%));
  box-shadow: var(--shadow-panel);
}

.topbar::before {
  inset: 0 0 auto;
  height: 2px;
  border-radius: 8px 8px 0 0;
  background: linear-gradient(
    90deg,
    color-mix(in oklch, var(--official-blue), transparent 72%),
    color-mix(in oklch, var(--official-gold), transparent 78%)
  );
}

.topbar h1 {
  color: var(--official-blue-deep);
  font-size: 1.48rem;
}

.topbar__status strong {
  color: var(--official-blue);
}

.user-card {
  min-height: 3rem;
  border-color: color-mix(in oklch, var(--line), transparent 48%);
}

.user-card button {
  background: color-mix(in oklch, var(--official-blue-soft), white 5%);
}

.portal-home {
  grid-template-columns: minmax(34rem, 1.08fr) minmax(24rem, 0.9fr);
  gap: 1rem;
}

.home-hero {
  position: relative;
  min-height: 19rem;
  padding: 2rem;
  border-color: color-mix(in oklch, var(--official-blue), transparent 72%);
  background:
    linear-gradient(90deg, color-mix(in oklch, var(--official-blue), transparent 91%) 0 0.35rem, transparent 0.35rem 100%),
    linear-gradient(135deg, var(--panel) 0%, color-mix(in oklch, var(--official-blue-soft), white 3%) 100%);
  box-shadow: var(--shadow-raised);
  overflow: hidden;
}

.home-hero::before {
  inset: auto 0 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    color-mix(in oklch, var(--official-blue), transparent 68%),
    color-mix(in oklch, var(--accent-green), transparent 74%),
    color-mix(in oklch, var(--official-gold), transparent 70%)
  );
}

.home-hero h2 {
  max-width: 44rem;
  color: var(--official-blue-deep);
  font-size: 2.48rem;
  line-height: 1.18;
}

.home-hero p {
  max-width: 45rem;
  color: color-mix(in oklch, var(--text-muted), var(--official-blue-deep) 10%);
}

.thesis-meta-grid article {
  border-left: 3px solid color-mix(in oklch, var(--official-blue), transparent 40%);
  background: color-mix(in oklch, var(--panel), white 1%);
}

.thesis-meta-grid b {
  color: var(--official-blue-deep);
}

.home-actions button {
  min-height: 2.5rem;
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 64%);
  border-radius: 6px;
  background: linear-gradient(135deg, var(--official-blue), color-mix(in oklch, var(--accent), white 8%));
  box-shadow: 0 0.45rem 1rem color-mix(in oklch, var(--official-blue), transparent 86%);
}

.home-actions button + button {
  color: var(--official-blue);
  background: var(--panel);
}

.home-metrics {
  grid-auto-rows: minmax(0, 1fr);
}

.home-grid:not(.home-grid--narrow) {
  gap: 0.85rem;
}

.home-entry {
  min-height: 7.7rem;
  border-top: 3px solid color-mix(in oklch, var(--official-gold), transparent 24%);
  background: linear-gradient(180deg, var(--panel), color-mix(in oklch, var(--official-blue-soft), white 4%));
}

.home-entry:hover {
  border-color: color-mix(in oklch, var(--official-blue), transparent 54%);
  border-top-color: var(--official-blue);
  box-shadow: 0 0.85rem 1.7rem rgba(20, 52, 99, 0.09);
  transform: translateY(-1px);
}

.home-entry svg,
.admin-grid svg {
  color: var(--official-gold);
}

.home-entry b,
.progress-list b,
.feature-list b,
.model-score-grid b,
.report-layout b,
.demo-route b,
.admin-grid b,
.role-table b {
  color: var(--official-blue-deep);
}

.screen-grid {
  grid-template-columns: minmax(18rem, 21.5rem) minmax(34rem, 1fr) minmax(19rem, 23.5rem);
  grid-template-rows: minmax(0, 1fr) clamp(9.5rem, 20vh, 11.5rem);
  gap: 0.85rem;
}

.dashboard-shell.sidebar-collapsed .screen-grid {
  grid-template-columns: minmax(18rem, 21.5rem) minmax(32rem, 1fr) minmax(23.5rem, 0.42fr);
}

.left-column,
.right-column,
.bottom-band {
  gap: 0.85rem;
}

.bottom-band {
  grid-template-columns: minmax(24rem, 1.05fr) minmax(27rem, 1fr) minmax(22rem, 0.82fr);
}

.score-line {
  height: 0.34rem;
  background: color-mix(in oklch, var(--line), transparent 58%);
}

.score-line i,
.gap-meter i,
.rank-row__bar i {
  background: linear-gradient(
    90deg,
    color-mix(in oklch, var(--official-blue), white 12%),
    color-mix(in oklch, var(--accent-green), white 12%),
    color-mix(in oklch, var(--official-gold), white 10%)
  );
}

.city-strip span,
.pipeline span,
.city-card > span,
.deploy-list span {
  border: 1px solid color-mix(in oklch, var(--official-blue), transparent 76%);
  color: var(--official-blue);
  background: color-mix(in oklch, var(--official-blue-soft), white 4%);
  box-shadow: inset 0 1px 0 color-mix(in oklch, white, transparent 18%);
}

.city-strip em,
.province-table span,
.skill-table strong,
.city-card footer b,
.path-grid span,
.benchmark-grid span,
.quality-grid span,
.model-score-grid span,
.report-layout span,
.demo-route span,
.insight-list em,
.combo-grid em {
  color: var(--official-blue);
}

.province-table article,
.skill-table article {
  min-height: 2.5rem;
  background: color-mix(in oklch, var(--panel), white 1%);
}

.workbench {
  gap: 1rem;
}

@media (min-width: 1281px) {
  .dashboard-shell .platform-main {
    --main-scale: 0.86;
    zoom: var(--main-scale);
  }

  .dashboard-shell .screen-grid {
    height: calc(116.28vh - 8.26rem);
  }

  .dashboard-shell .workbench {
    min-height: calc(116.28vh - 8.26rem);
  }

  .dashboard-shell .workbench--salary {
    min-height: calc(116.28vh - 8.26rem);
  }
}

@media (min-width: 1500px) {
  .dashboard-shell .platform-main {
    --main-scale: 0.88;
  }

  .dashboard-shell .screen-grid {
    height: calc(113.64vh - 8.07rem);
  }

  .dashboard-shell .workbench,
  .dashboard-shell .workbench--salary {
    min-height: calc(113.64vh - 8.07rem);
  }
}

@media (min-width: 1800px) {
  .dashboard-shell .platform-main {
    --main-scale: 0.9;
  }

  .dashboard-shell .screen-grid {
    height: calc(111.11vh - 7.89rem);
  }

  .dashboard-shell .workbench,
  .dashboard-shell .workbench--salary {
    min-height: calc(111.11vh - 7.89rem);
  }
}

@media (min-width: 2200px) {
  .dashboard-shell .platform-main {
    --main-scale: 0.92;
  }

  .dashboard-shell .screen-grid {
    height: calc(108.7vh - 7.72rem);
  }

  .dashboard-shell .workbench,
  .dashboard-shell .workbench--salary {
    min-height: calc(108.7vh - 7.72rem);
  }
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
  .home-grid:not(.home-grid--narrow),
  .home-grid--narrow,
  .home-longform,
  .bottom-band,
  .audit-toolbar,
  .audit-summary,
  .unban-panel,
  .explain-grid,
  .model-score-grid,
  .report-layout,
  .admin-grid,
  .acceptance-grid {
    grid-template-columns: 1fr;
  }

  .workbench--admin > :nth-child(2) {
    grid-column: span 1;
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
  .thesis-meta-grid,
  .demo-credentials,
  .home-metrics,
  .audit-summary,
  .metric-grid,
  .benchmark-grid,
  .combo-grid,
  .quality-grid {
    grid-template-columns: 1fr;
  }

  .home-hero {
    padding: var(--space-lg);
  }

  .home-hero h2 {
    font-size: 2rem;
  }

  .home-actions button {
    width: 100%;
  }

  .home-entry {
    min-height: auto;
  }

  .report-layout article,
  .feature-list article,
  .demo-route article,
  .role-table article,
  .banned-ip-list article,
  .deploy-list article {
    grid-template-columns: 1fr;
  }
}
</style>
