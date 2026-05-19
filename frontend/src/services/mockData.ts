import type {
  CareerRecommendation,
  CityMetric,
  DashboardAnalysis,
  DashboardOverview,
  JobLiveItem,
  ProvinceMetric,
  SalaryPrediction
} from '../types/dashboard'

export const provinceMetrics: ProvinceMetric[] = [
  { province: '北京', jobCount: 112360, avgSalary: 19580, freshFriendlyIndex: 78.3, heatIndex: 86.4, topIndustry: '人工智能', growthRate: 7.9 },
  { province: '天津', jobCount: 29860, avgSalary: 11620, freshFriendlyIndex: 80.9, heatIndex: 65.2, topIndustry: '智能制造', growthRate: 5.1 },
  { province: '河北', jobCount: 45620, avgSalary: 9280, freshFriendlyIndex: 81.6, heatIndex: 66.8, topIndustry: '装备制造', growthRate: 5.4 },
  { province: '山西', jobCount: 28640, avgSalary: 9020, freshFriendlyIndex: 82.1, heatIndex: 61.6, topIndustry: '能源数字化', growthRate: 4.8 },
  { province: '内蒙古', jobCount: 21480, avgSalary: 9340, freshFriendlyIndex: 80.5, heatIndex: 58.9, topIndustry: '新能源', growthRate: 4.2 },
  { province: '辽宁', jobCount: 51240, avgSalary: 10460, freshFriendlyIndex: 80.8, heatIndex: 69.4, topIndustry: '软件服务', growthRate: 5.9 },
  { province: '吉林', jobCount: 24680, avgSalary: 8860, freshFriendlyIndex: 82.5, heatIndex: 58.4, topIndustry: '汽车电子', growthRate: 4.6 },
  { province: '黑龙江', jobCount: 23860, avgSalary: 8720, freshFriendlyIndex: 83.1, heatIndex: 57.8, topIndustry: '现代农业', growthRate: 4.4 },
  { province: '上海', jobCount: 104880, avgSalary: 18240, freshFriendlyIndex: 79.5, heatIndex: 86.9, topIndustry: '金融科技', growthRate: 8.7 },
  { province: '江苏', jobCount: 132870, avgSalary: 13260, freshFriendlyIndex: 82.4, heatIndex: 88.3, topIndustry: '智能制造', growthRate: 9.8 },
  { province: '浙江', jobCount: 128560, avgSalary: 14520, freshFriendlyIndex: 84.1, heatIndex: 87.6, topIndustry: '数字经济', growthRate: 10.4 },
  { province: '安徽', jobCount: 62340, avgSalary: 10840, freshFriendlyIndex: 84.2, heatIndex: 73.6, topIndustry: '新能源汽车', growthRate: 8.8 },
  { province: '福建', jobCount: 41870, avgSalary: 12420, freshFriendlyIndex: 82.8, heatIndex: 71.6, topIndustry: '数字贸易', growthRate: 7.6 },
  { province: '江西', jobCount: 36520, avgSalary: 9480, freshFriendlyIndex: 83.9, heatIndex: 67.1, topIndustry: '电子信息', growthRate: 6.5 },
  { province: '山东', jobCount: 76840, avgSalary: 10520, freshFriendlyIndex: 81.7, heatIndex: 76.8, topIndustry: '装备制造', growthRate: 6.6 },
  { province: '河南', jobCount: 52830, avgSalary: 9280, freshFriendlyIndex: 82.0, heatIndex: 69.8, topIndustry: '现代服务', growthRate: 5.8 },
  { province: '湖北', jobCount: 72180, avgSalary: 11240, freshFriendlyIndex: 83.1, heatIndex: 77.6, topIndustry: '光电子信息', growthRate: 9.3 },
  { province: '湖南', jobCount: 46820, avgSalary: 10350, freshFriendlyIndex: 84.7, heatIndex: 70.5, topIndustry: '移动互联网', growthRate: 7.4 },
  { province: '广东', jobCount: 186420, avgSalary: 15480, freshFriendlyIndex: 86.2, heatIndex: 94.8, topIndustry: '互联网/电子商务', growthRate: 12.6 },
  { province: '广西', jobCount: 27640, avgSalary: 9320, freshFriendlyIndex: 84.5, heatIndex: 62.8, topIndustry: '数字贸易', growthRate: 5.7 },
  { province: '海南', jobCount: 15680, avgSalary: 10120, freshFriendlyIndex: 83.6, heatIndex: 55.4, topIndustry: '旅游科技', growthRate: 6.2 },
  { province: '重庆', jobCount: 38520, avgSalary: 11080, freshFriendlyIndex: 84.8, heatIndex: 70.9, topIndustry: '汽车电子', growthRate: 8.1 },
  { province: '四川', jobCount: 87520, avgSalary: 11860, freshFriendlyIndex: 85.6, heatIndex: 80.7, topIndustry: '软件服务', growthRate: 11.9 },
  { province: '贵州', jobCount: 22460, avgSalary: 9160, freshFriendlyIndex: 85.2, heatIndex: 59.6, topIndustry: '大数据', growthRate: 6.8 },
  { province: '云南', jobCount: 25620, avgSalary: 9060, freshFriendlyIndex: 84.3, heatIndex: 60.4, topIndustry: '文旅数字化', growthRate: 5.3 },
  { province: '西藏', jobCount: 6820, avgSalary: 8860, freshFriendlyIndex: 79.4, heatIndex: 42.6, topIndustry: '公共服务', growthRate: 3.1 },
  { province: '陕西', jobCount: 43620, avgSalary: 11350, freshFriendlyIndex: 85.9, heatIndex: 72.4, topIndustry: '硬科技', growthRate: 8.4 },
  { province: '甘肃', jobCount: 18640, avgSalary: 8420, freshFriendlyIndex: 81.8, heatIndex: 51.6, topIndustry: '新能源', growthRate: 4.0 },
  { province: '青海', jobCount: 8260, avgSalary: 8580, freshFriendlyIndex: 80.6, heatIndex: 44.8, topIndustry: '清洁能源', growthRate: 3.4 },
  { province: '宁夏', jobCount: 10640, avgSalary: 8720, freshFriendlyIndex: 81.2, heatIndex: 47.3, topIndustry: '数字政务', growthRate: 3.8 },
  { province: '新疆', jobCount: 21860, avgSalary: 9120, freshFriendlyIndex: 82.6, heatIndex: 56.2, topIndustry: '能源化工', growthRate: 4.7 },
  { province: '台湾', jobCount: 32480, avgSalary: 13600, freshFriendlyIndex: 78.8, heatIndex: 62.5, topIndustry: '半导体', growthRate: 4.9 },
  { province: '香港', jobCount: 28620, avgSalary: 21200, freshFriendlyIndex: 74.5, heatIndex: 64.4, topIndustry: '金融服务', growthRate: 3.5 },
  { province: '澳门', jobCount: 6420, avgSalary: 16800, freshFriendlyIndex: 76.9, heatIndex: 43.8, topIndustry: '文旅会展', growthRate: 2.8 }
]

export const cityMetrics: CityMetric[] = [
  { province: '广东', city: '深圳', jobCount: 82450, avgSalary: 18620, freshFriendlyIndex: 83.8, attractionIndex: 96.2, rankNo: 1, longitude: 114.057868, latitude: 22.543099 },
  { province: '北京', city: '北京', jobCount: 112360, avgSalary: 19580, freshFriendlyIndex: 78.3, attractionIndex: 95.8, rankNo: 2, longitude: 116.407526, latitude: 39.90403 },
  { province: '上海', city: '上海', jobCount: 104880, avgSalary: 18240, freshFriendlyIndex: 79.5, attractionIndex: 94.7, rankNo: 3, longitude: 121.473701, latitude: 31.230416 },
  { province: '浙江', city: '杭州', jobCount: 64230, avgSalary: 16880, freshFriendlyIndex: 85.2, attractionIndex: 93.6, rankNo: 4, longitude: 120.15507, latitude: 30.274085 },
  { province: '广东', city: '广州', jobCount: 72180, avgSalary: 15120, freshFriendlyIndex: 86.1, attractionIndex: 91.4, rankNo: 5, longitude: 113.264385, latitude: 23.129112 },
  { province: '江苏', city: '南京', jobCount: 51260, avgSalary: 13950, freshFriendlyIndex: 83.7, attractionIndex: 88.3, rankNo: 6, longitude: 118.796877, latitude: 32.060255 },
  { province: '四川', city: '成都', jobCount: 69340, avgSalary: 12680, freshFriendlyIndex: 87.2, attractionIndex: 87.9, rankNo: 7, longitude: 104.066541, latitude: 30.572269 },
  { province: '湖北', city: '武汉', jobCount: 55870, avgSalary: 11980, freshFriendlyIndex: 84.6, attractionIndex: 84.2, rankNo: 8, longitude: 114.305393, latitude: 30.593099 },
  { province: '陕西', city: '西安', jobCount: 43620, avgSalary: 11350, freshFriendlyIndex: 85.9, attractionIndex: 81.5, rankNo: 9, longitude: 108.93977, latitude: 34.341575 },
  { province: '山东', city: '青岛', jobCount: 38960, avgSalary: 10840, freshFriendlyIndex: 82.3, attractionIndex: 78.6, rankNo: 10, longitude: 120.382639, latitude: 36.067082 },
  { province: '江苏', city: '苏州', jobCount: 61280, avgSalary: 14860, freshFriendlyIndex: 81.4, attractionIndex: 87.7, rankNo: 11, longitude: 120.585315, latitude: 31.298886 },
  { province: '天津', city: '天津', jobCount: 29860, avgSalary: 11620, freshFriendlyIndex: 80.9, attractionIndex: 74.2, rankNo: 12, longitude: 117.200983, latitude: 39.084158 },
  { province: '安徽', city: '合肥', jobCount: 48250, avgSalary: 11260, freshFriendlyIndex: 85.1, attractionIndex: 76.8, rankNo: 13, longitude: 117.227239, latitude: 31.820586 },
  { province: '湖南', city: '长沙', jobCount: 46820, avgSalary: 10350, freshFriendlyIndex: 84.7, attractionIndex: 75.4, rankNo: 14, longitude: 112.938814, latitude: 28.228209 },
  { province: '河南', city: '郑州', jobCount: 52830, avgSalary: 9280, freshFriendlyIndex: 82.0, attractionIndex: 73.8, rankNo: 15, longitude: 113.625368, latitude: 34.746599 },
  { province: '福建', city: '厦门', jobCount: 31840, avgSalary: 13520, freshFriendlyIndex: 82.1, attractionIndex: 73.2, rankNo: 16, longitude: 118.089425, latitude: 24.479833 },
  { province: '重庆', city: '重庆', jobCount: 38520, avgSalary: 11080, freshFriendlyIndex: 84.8, attractionIndex: 72.5, rankNo: 17, longitude: 106.551643, latitude: 29.562849 },
  { province: '山东', city: '济南', jobCount: 37880, avgSalary: 10460, freshFriendlyIndex: 82.4, attractionIndex: 71.6, rankNo: 18, longitude: 117.120128, latitude: 36.652069 },
  { province: '辽宁', city: '大连', jobCount: 32450, avgSalary: 11280, freshFriendlyIndex: 80.6, attractionIndex: 70.8, rankNo: 19, longitude: 121.614682, latitude: 38.914003 },
  { province: '福建', city: '福州', jobCount: 28620, avgSalary: 11880, freshFriendlyIndex: 83.0, attractionIndex: 70.1, rankNo: 20, longitude: 119.296494, latitude: 26.074508 },
  { province: '辽宁', city: '沈阳', jobCount: 31260, avgSalary: 10140, freshFriendlyIndex: 81.2, attractionIndex: 69.2, rankNo: 21, longitude: 123.431475, latitude: 41.805698 },
  { province: '云南', city: '昆明', jobCount: 25620, avgSalary: 9060, freshFriendlyIndex: 84.3, attractionIndex: 66.9, rankNo: 22, longitude: 102.832891, latitude: 24.880095 },
  { province: '江西', city: '南昌', jobCount: 36520, avgSalary: 9480, freshFriendlyIndex: 83.9, attractionIndex: 66.5, rankNo: 23, longitude: 115.858197, latitude: 28.682892 },
  { province: '广西', city: '南宁', jobCount: 27640, avgSalary: 9320, freshFriendlyIndex: 84.5, attractionIndex: 64.8, rankNo: 24, longitude: 108.366543, latitude: 22.817002 },
  { province: '贵州', city: '贵阳', jobCount: 22460, avgSalary: 9160, freshFriendlyIndex: 85.2, attractionIndex: 63.6, rankNo: 25, longitude: 106.630153, latitude: 26.647661 },
  { province: '山西', city: '太原', jobCount: 28640, avgSalary: 9020, freshFriendlyIndex: 82.1, attractionIndex: 62.7, rankNo: 26, longitude: 112.548879, latitude: 37.87059 },
  { province: '黑龙江', city: '哈尔滨', jobCount: 23860, avgSalary: 8720, freshFriendlyIndex: 83.1, attractionIndex: 61.4, rankNo: 27, longitude: 126.534967, latitude: 45.803775 },
  { province: '吉林', city: '长春', jobCount: 24680, avgSalary: 8860, freshFriendlyIndex: 82.5, attractionIndex: 60.9, rankNo: 28, longitude: 125.323544, latitude: 43.817072 },
  { province: '新疆', city: '乌鲁木齐', jobCount: 21860, avgSalary: 9120, freshFriendlyIndex: 82.6, attractionIndex: 59.8, rankNo: 29, longitude: 87.616848, latitude: 43.825592 },
  { province: '甘肃', city: '兰州', jobCount: 18640, avgSalary: 8420, freshFriendlyIndex: 81.8, attractionIndex: 57.2, rankNo: 30, longitude: 103.834303, latitude: 36.061089 },
  { province: '内蒙古', city: '呼和浩特', jobCount: 21480, avgSalary: 9340, freshFriendlyIndex: 80.5, attractionIndex: 56.6, rankNo: 31, longitude: 111.749181, latitude: 40.842585 },
  { province: '宁夏', city: '银川', jobCount: 10640, avgSalary: 8720, freshFriendlyIndex: 81.2, attractionIndex: 52.4, rankNo: 32, longitude: 106.230909, latitude: 38.487193 },
  { province: '海南', city: '海口', jobCount: 15680, avgSalary: 10120, freshFriendlyIndex: 83.6, attractionIndex: 51.9, rankNo: 33, longitude: 110.198293, latitude: 20.044001 },
  { province: '西藏', city: '拉萨', jobCount: 6820, avgSalary: 8860, freshFriendlyIndex: 79.4, attractionIndex: 46.2, rankNo: 34, longitude: 91.140856, latitude: 29.645554 },
  { province: '青海', city: '西宁', jobCount: 8260, avgSalary: 8580, freshFriendlyIndex: 80.6, attractionIndex: 45.8, rankNo: 35, longitude: 101.778228, latitude: 36.617144 },
  { province: '香港', city: '香港', jobCount: 28620, avgSalary: 21200, freshFriendlyIndex: 74.5, attractionIndex: 64.4, rankNo: 36, longitude: 114.169361, latitude: 22.319303 },
  { province: '澳门', city: '澳门', jobCount: 6420, avgSalary: 16800, freshFriendlyIndex: 76.9, attractionIndex: 43.8, rankNo: 37, longitude: 113.543873, latitude: 22.198745 },
  { province: '台湾', city: '台北', jobCount: 32480, avgSalary: 13600, freshFriendlyIndex: 78.8, attractionIndex: 62.5, rankNo: 38, longitude: 121.565418, latitude: 25.032969 }
]

export const overview: DashboardOverview = {
  totalJobs: provinceMetrics.reduce((sum, item) => sum + item.jobCount, 0),
  averageSalary: Math.round(provinceMetrics.reduce((sum, item) => sum + item.avgSalary * item.jobCount, 0) / provinceMetrics.reduce((sum, item) => sum + item.jobCount, 0)),
  coveredCities: 337,
  freshFriendlyIndex: Number((provinceMetrics.reduce((sum, item) => sum + item.freshFriendlyIndex * item.jobCount, 0) / provinceMetrics.reduce((sum, item) => sum + item.jobCount, 0)).toFixed(1)),
  hotCities: cityMetrics.slice(0, 10).map((item) => ({ name: item.city, value: item.jobCount, score: item.attractionIndex, tag: item.province })),
  hotIndustries: [
    { name: '互联网/电子商务', value: 186420, score: 96.4, tag: '岗位增长快' },
    { name: '软件服务', value: 151260, score: 92.8, tag: '应届友好' },
    { name: '人工智能', value: 98240, score: 91.6, tag: '薪资高' },
    { name: '智能制造', value: 87350, score: 87.9, tag: '区域扩张' },
    { name: '金融科技', value: 76820, score: 84.7, tag: '门槛较高' },
    { name: '数字贸易', value: 64150, score: 81.3, tag: '复合岗位' },
    { name: '咨询服务', value: 53840, score: 78.5, tag: '数据需求' },
    { name: '云服务', value: 50260, score: 77.4, tag: '技能驱动' },
    { name: '光电子信息', value: 48630, score: 75.8, tag: '区域集群' },
    { name: '装备制造', value: 45280, score: 73.1, tag: '稳定吸纳' }
  ],
  monthlyTrend: [
    { month: '2025-06', jobs: 612000, freshJobs: 186000, aiJobs: 42000 },
    { month: '2025-07', jobs: 628000, freshJobs: 191000, aiJobs: 43800 },
    { month: '2025-08', jobs: 654000, freshJobs: 204000, aiJobs: 45200 },
    { month: '2025-09', jobs: 702000, freshJobs: 232000, aiJobs: 48600 },
    { month: '2025-10', jobs: 688000, freshJobs: 226000, aiJobs: 50100 },
    { month: '2025-11', jobs: 716000, freshJobs: 240000, aiJobs: 52400 },
    { month: '2025-12', jobs: 735000, freshJobs: 248000, aiJobs: 54800 },
    { month: '2026-01', jobs: 701000, freshJobs: 236000, aiJobs: 55900 },
    { month: '2026-02', jobs: 742000, freshJobs: 254000, aiJobs: 58200 },
    { month: '2026-03', jobs: 795000, freshJobs: 286000, aiJobs: 63600 },
    { month: '2026-04', jobs: 836000, freshJobs: 304000, aiJobs: 68100 },
    { month: '2026-05', jobs: 873000, freshJobs: 321000, aiJobs: 72400 }
  ]
}

export const analysis: DashboardAnalysis = {
  salaryRanges: [
    { name: '6K以下', value: 8 },
    { name: '6K-10K', value: 18 },
    { name: '10K-15K', value: 28 },
    { name: '15K-25K', value: 31 },
    { name: '25K以上', value: 15 }
  ],
  education: [
    { name: '不限', value: 10 },
    { name: '大专', value: 21 },
    { name: '本科', value: 54 },
    { name: '硕士', value: 13 },
    { name: '博士', value: 2 }
  ],
  experience: [
    { name: '应届/不限', value: 38 },
    { name: '1-3年', value: 34 },
    { name: '3-5年', value: 20 },
    { name: '5年以上', value: 8 }
  ],
  skills: [
    { skill: 'Python', frequency: 48210, heatIndex: 96.4, category: '数据分析', trendScore: 88.6 },
    { skill: 'FastAPI', frequency: 42380, heatIndex: 94.2, category: '后端开发', trendScore: 78.2 },
    { skill: 'SQL', frequency: 46570, heatIndex: 92.7, category: '数据分析', trendScore: 82.5 },
    { skill: '大数据', frequency: 31860, heatIndex: 90.8, category: '数据开发', trendScore: 85.2 },
    { skill: '人工智能', frequency: 28420, heatIndex: 90.1, category: '算法工程师', trendScore: 91.3 },
    { skill: '前端开发', frequency: 36750, heatIndex: 86.9, category: '前端开发', trendScore: 74.6 },
    { skill: '数据分析', frequency: 33880, heatIndex: 86.5, category: '数据分析', trendScore: 80.1 },
    { skill: '机器学习', frequency: 24660, heatIndex: 85.6, category: '算法工程师', trendScore: 89.4 },
    { skill: 'Vue', frequency: 22640, heatIndex: 80.4, category: '前端开发', trendScore: 70.8 },
    { skill: '云计算', frequency: 21980, heatIndex: 80.1, category: '云平台工程师', trendScore: 83.9 }
  ]
}

export const liveJobs: JobLiveItem[] = [
  { time: '09:41', city: '深圳', title: '数据分析师', company: '华南数字科技有限公司', salary: '15K-25K', skills: 'SQL / Python' },
  { time: '09:43', city: '杭州', title: 'Python 后端开发工程师', company: '长三角智能软件有限公司', salary: '18K-30K', skills: 'Python / FastAPI' },
  { time: '09:45', city: '北京', title: '人工智能算法工程师', company: '中关村智能研究院', salary: '25K-40K', skills: 'Python / PyTorch' },
  { time: '09:48', city: '广州', title: '前端开发工程师', company: '珠江云端科技有限公司', salary: '12K-20K', skills: 'Vue3 / TypeScript' },
  { time: '09:52', city: '成都', title: '大数据开发工程师', company: '西部数据智能有限公司', salary: '14K-24K', skills: 'Spark / Hive' },
  { time: '09:55', city: '武汉', title: '产品数据运营', company: '光谷产业服务平台', salary: '10K-18K', skills: 'SQL / BI' },
  { time: '09:57', city: '南京', title: '嵌入式软件工程师', company: '江北智能制造集团', salary: '13K-22K', skills: 'C++ / Linux' }
]

export const mockSalaryPrediction: SalaryPrediction = {
  predictedMin: 14760,
  predictedMax: 22320,
  predictedAvg: 18000,
  confidence: 86.5,
  modelName: 'RandomForestRegressor',
  explanation: '基于城市、行业、学历、经验、岗位类别和技能因子生成演示预测。',
  influenceFactors: ['城市薪资基准', '行业溢价', '学历门槛', '经验要求', '岗位类别']
}

export const mockRecommendations: CareerRecommendation[] = [
  {
    direction: '数据分析与商业智能方向',
    city: '深圳',
    industry: '互联网/电子商务',
    jobCategory: '数据分析师',
    matchScore: 94,
    salaryPotential: 16000,
    reason: '与专业背景、SQL 和 Python 技能匹配，岗位密度高。',
    skillGaps: ['可视化', '统计分析'],
    suggestions: ['补强 SQL 窗口函数', '完成行业数据分析作品集']
  }
]
