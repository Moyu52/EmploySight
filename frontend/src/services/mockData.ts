import type {
  CareerRecommendation,
  CityMetric,
  DashboardAnalysis,
  DashboardOverview,
  JobLiveItem,
  ProvinceMetric,
  SalaryPrediction
} from '../types/dashboard'

// Generated from real Kaggle and China Public Recruitment Network data.
export const provinceMetrics: ProvinceMetric[] = [
  {
    "province": "北京",
    "jobCount": 2527,
    "avgSalary": 9101,
    "freshFriendlyIndex": 63.8,
    "heatIndex": 91.0,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "天津",
    "jobCount": 1604,
    "avgSalary": 5759,
    "freshFriendlyIndex": 47.8,
    "heatIndex": 52.8,
    "topIndustry": "未分类",
    "growthRate": 0
  },
  {
    "province": "河北",
    "jobCount": 1604,
    "avgSalary": 4229,
    "freshFriendlyIndex": 38.0,
    "heatIndex": 43.1,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "山西",
    "jobCount": 1603,
    "avgSalary": 4892,
    "freshFriendlyIndex": 39.2,
    "heatIndex": 46.5,
    "topIndustry": "居民服务人员",
    "growthRate": 0
  },
  {
    "province": "内蒙古",
    "jobCount": 58,
    "avgSalary": 7089,
    "freshFriendlyIndex": 58.8,
    "heatIndex": 31.2,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "辽宁",
    "jobCount": 1609,
    "avgSalary": 3838,
    "freshFriendlyIndex": 71.0,
    "heatIndex": 49.6,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "吉林",
    "jobCount": 1602,
    "avgSalary": 4626,
    "freshFriendlyIndex": 38.6,
    "heatIndex": 45.1,
    "topIndustry": "通用工程机械操作人员",
    "growthRate": 0
  },
  {
    "province": "黑龙江",
    "jobCount": 1605,
    "avgSalary": 4667,
    "freshFriendlyIndex": 66.6,
    "heatIndex": 52.3,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "上海",
    "jobCount": 439,
    "avgSalary": 8793,
    "freshFriendlyIndex": 67.1,
    "heatIndex": 48.9,
    "topIndustry": "销售人员",
    "growthRate": 0
  },
  {
    "province": "江苏",
    "jobCount": 1630,
    "avgSalary": 7237,
    "freshFriendlyIndex": 67.9,
    "heatIndex": 65.3,
    "topIndustry": "社会生产服务和生活服务人员",
    "growthRate": 0
  },
  {
    "province": "浙江",
    "jobCount": 1647,
    "avgSalary": 6824,
    "freshFriendlyIndex": 44.2,
    "heatIndex": 57.8,
    "topIndustry": "机械冷加工人员",
    "growthRate": 0
  },
  {
    "province": "安徽",
    "jobCount": 1602,
    "avgSalary": 5580,
    "freshFriendlyIndex": 64.1,
    "heatIndex": 56.0,
    "topIndustry": "其他工程技术人员",
    "growthRate": 0
  },
  {
    "province": "福建",
    "jobCount": 1601,
    "avgSalary": 6055,
    "freshFriendlyIndex": 70.8,
    "heatIndex": 59.9,
    "topIndustry": "其他专业技术人员",
    "growthRate": 0
  },
  {
    "province": "江西",
    "jobCount": 1600,
    "avgSalary": 4655,
    "freshFriendlyIndex": 59.4,
    "heatIndex": 50.4,
    "topIndustry": "生产制造及有关人员",
    "growthRate": 0
  },
  {
    "province": "山东",
    "jobCount": 1633,
    "avgSalary": 6132,
    "freshFriendlyIndex": 63.1,
    "heatIndex": 58.9,
    "topIndustry": "通用基础件装配制造人员",
    "growthRate": 0
  },
  {
    "province": "河南",
    "jobCount": 73,
    "avgSalary": 4482,
    "freshFriendlyIndex": 60.7,
    "heatIndex": 19.6,
    "topIndustry": "销售人员",
    "growthRate": 0
  },
  {
    "province": "湖北",
    "jobCount": 1642,
    "avgSalary": 6359,
    "freshFriendlyIndex": 44.1,
    "heatIndex": 55.5,
    "topIndustry": "专业技术人员",
    "growthRate": 0
  },
  {
    "province": "湖南",
    "jobCount": 1603,
    "avgSalary": 5203,
    "freshFriendlyIndex": 62.7,
    "heatIndex": 53.8,
    "topIndustry": "生产制造及有关人员",
    "growthRate": 0
  },
  {
    "province": "广东",
    "jobCount": 1666,
    "avgSalary": 6384,
    "freshFriendlyIndex": 68.4,
    "heatIndex": 62.1,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "广西",
    "jobCount": 1505,
    "avgSalary": 4962,
    "freshFriendlyIndex": 68.4,
    "heatIndex": 52.2,
    "topIndustry": "其他生产制造及有关人员",
    "growthRate": 0
  },
  {
    "province": "海南",
    "jobCount": 167,
    "avgSalary": 6196,
    "freshFriendlyIndex": 60.2,
    "heatIndex": 29.5,
    "topIndustry": "其他社会生产和生活服务人员",
    "growthRate": 0
  },
  {
    "province": "重庆",
    "jobCount": 1605,
    "avgSalary": 5702,
    "freshFriendlyIndex": 69.9,
    "heatIndex": 58.1,
    "topIndustry": "其他生产制造及有关人员",
    "growthRate": 0
  },
  {
    "province": "四川",
    "jobCount": 1615,
    "avgSalary": 5346,
    "freshFriendlyIndex": 79.9,
    "heatIndex": 59.1,
    "topIndustry": "其他专业技术人员",
    "growthRate": 0
  },
  {
    "province": "贵州",
    "jobCount": 185,
    "avgSalary": 6310,
    "freshFriendlyIndex": 66.7,
    "heatIndex": 32.0,
    "topIndustry": "机械冷加工人员",
    "growthRate": 0
  },
  {
    "province": "云南",
    "jobCount": 257,
    "avgSalary": 3915,
    "freshFriendlyIndex": 47.5,
    "heatIndex": 17.2,
    "topIndustry": "销售人员",
    "growthRate": 0
  },
  {
    "province": "西藏",
    "jobCount": 95,
    "avgSalary": 4503,
    "freshFriendlyIndex": 69.6,
    "heatIndex": 22.3,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "陕西",
    "jobCount": 1602,
    "avgSalary": 4783,
    "freshFriendlyIndex": 43.9,
    "heatIndex": 47.1,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "甘肃",
    "jobCount": 20,
    "avgSalary": 8375,
    "freshFriendlyIndex": 57.7,
    "heatIndex": 36.3,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "青海",
    "jobCount": 1600,
    "avgSalary": 5447,
    "freshFriendlyIndex": 80.1,
    "heatIndex": 59.3,
    "topIndustry": "事业单位负责人",
    "growthRate": 0
  },
  {
    "province": "宁夏",
    "jobCount": 167,
    "avgSalary": 5744,
    "freshFriendlyIndex": 40.7,
    "heatIndex": 22.4,
    "topIndustry": "不便分类的其他从业人员",
    "growthRate": 0
  },
  {
    "province": "新疆",
    "jobCount": 1601,
    "avgSalary": 4827,
    "freshFriendlyIndex": 65.3,
    "heatIndex": 52.7,
    "topIndustry": "销售人员",
    "growthRate": 0
  },
  {
    "province": "香港",
    "jobCount": 5,
    "avgSalary": 0,
    "freshFriendlyIndex": 85.0,
    "heatIndex": 29.4,
    "topIndustry": "engineering, support",
    "growthRate": 0
  },
  {
    "province": "澳门",
    "jobCount": 0,
    "avgSalary": 0,
    "freshFriendlyIndex": 0.0,
    "heatIndex": 0.0,
    "topIndustry": "样本不足",
    "growthRate": 0
  },
  {
    "province": "台湾",
    "jobCount": 0,
    "avgSalary": 0,
    "freshFriendlyIndex": 0.0,
    "heatIndex": 0.0,
    "topIndustry": "样本不足",
    "growthRate": 0
  }
]

export const cityMetrics: CityMetric[] = [
  {
    "province": "陕西",
    "city": "西安",
    "jobCount": 1281,
    "avgSalary": 4710,
    "freshFriendlyIndex": 10.9,
    "attractionIndex": 70.2,
    "rankNo": 1,
    "longitude": 108.93977,
    "latitude": 34.341575
  },
  {
    "province": "北京",
    "city": "北京",
    "jobCount": 1099,
    "avgSalary": 11869,
    "freshFriendlyIndex": 22.1,
    "attractionIndex": 65.9,
    "rankNo": 2,
    "longitude": 116.407526,
    "latitude": 39.90403
  },
  {
    "province": "重庆",
    "city": "重庆",
    "jobCount": 814,
    "avgSalary": 5643,
    "freshFriendlyIndex": 71.1,
    "attractionIndex": 58.3,
    "rankNo": 3,
    "longitude": 106.551643,
    "latitude": 29.562849
  },
  {
    "province": "黑龙江",
    "city": "哈尔滨",
    "jobCount": 660,
    "avgSalary": 5543,
    "freshFriendlyIndex": 62.9,
    "attractionIndex": 48.5,
    "rankNo": 4,
    "longitude": 126.534967,
    "latitude": 45.803775
  },
  {
    "province": "吉林",
    "city": "长春",
    "jobCount": 775,
    "avgSalary": 6023,
    "freshFriendlyIndex": 0.1,
    "attractionIndex": 42.2,
    "rankNo": 5,
    "longitude": 125.323544,
    "latitude": 43.817072
  },
  {
    "province": "江苏",
    "city": "苏州",
    "jobCount": 489,
    "avgSalary": 6972,
    "freshFriendlyIndex": 56.4,
    "attractionIndex": 38.9,
    "rankNo": 6,
    "longitude": 120.585315,
    "latitude": 31.298886
  },
  {
    "province": "辽宁",
    "city": "大连",
    "jobCount": 353,
    "avgSalary": 4535,
    "freshFriendlyIndex": 82.7,
    "attractionIndex": 36.0,
    "rankNo": 7,
    "longitude": 121.614682,
    "latitude": 38.914003
  },
  {
    "province": "青海",
    "city": "西宁",
    "jobCount": 257,
    "avgSalary": 5447,
    "freshFriendlyIndex": 99.6,
    "attractionIndex": 34.8,
    "rankNo": 8,
    "longitude": 101.778228,
    "latitude": 36.617144
  },
  {
    "province": "山东",
    "city": "青岛",
    "jobCount": 264,
    "avgSalary": 5144,
    "freshFriendlyIndex": 91.7,
    "attractionIndex": 33.4,
    "rankNo": 9,
    "longitude": 120.382639,
    "latitude": 36.067082
  },
  {
    "province": "江苏",
    "city": "常州",
    "jobCount": 333,
    "avgSalary": 7077,
    "freshFriendlyIndex": 58.9,
    "attractionIndex": 31.3,
    "rankNo": 10,
    "longitude": 119.974092,
    "latitude": 31.811313
  },
  {
    "province": "江苏",
    "city": "南京",
    "jobCount": 217,
    "avgSalary": 9633,
    "freshFriendlyIndex": 75.6,
    "attractionIndex": 29.6,
    "rankNo": 11,
    "longitude": 118.796877,
    "latitude": 32.060255
  },
  {
    "province": "新疆",
    "city": "乌鲁木齐",
    "jobCount": 297,
    "avgSalary": 5858,
    "freshFriendlyIndex": 60.6,
    "attractionIndex": 29.2,
    "rankNo": 12,
    "longitude": 87.616848,
    "latitude": 43.825592
  },
  {
    "province": "河北",
    "city": "石家庄",
    "jobCount": 515,
    "avgSalary": 4372,
    "freshFriendlyIndex": 0.2,
    "attractionIndex": 27.9,
    "rankNo": 13,
    "longitude": 114.514976,
    "latitude": 38.042007
  },
  {
    "province": "广东",
    "city": "广州",
    "jobCount": 60,
    "avgSalary": 20040,
    "freshFriendlyIndex": 83.3,
    "attractionIndex": 27.2,
    "rankNo": 14,
    "longitude": 113.264385,
    "latitude": 23.129112
  },
  {
    "province": "上海",
    "city": "上海",
    "jobCount": 207,
    "avgSalary": 14004,
    "freshFriendlyIndex": 54.1,
    "attractionIndex": 26.6,
    "rankNo": 15,
    "longitude": 121.473701,
    "latitude": 31.230416
  },
  {
    "province": "四川",
    "city": "成都",
    "jobCount": 15,
    "avgSalary": 22500,
    "freshFriendlyIndex": 73.3,
    "attractionIndex": 23.9,
    "rankNo": 16,
    "longitude": 104.066541,
    "latitude": 30.572269
  },
  {
    "province": "天津",
    "city": "天津",
    "jobCount": 403,
    "avgSalary": 7444,
    "freshFriendlyIndex": 0.2,
    "attractionIndex": 23.3,
    "rankNo": 17,
    "longitude": 117.200983,
    "latitude": 39.084158
  },
  {
    "province": "内蒙古",
    "city": "呼和浩特",
    "jobCount": 7,
    "avgSalary": 8107,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 22.9,
    "rankNo": 18,
    "longitude": 111.749181,
    "latitude": 40.842585
  },
  {
    "province": "安徽",
    "city": "合肥",
    "jobCount": 74,
    "avgSalary": 3903,
    "freshFriendlyIndex": 90.5,
    "attractionIndex": 22.8,
    "rankNo": 19,
    "longitude": 117.227239,
    "latitude": 31.820586
  },
  {
    "province": "湖南",
    "city": "长沙",
    "jobCount": 51,
    "avgSalary": 8504,
    "freshFriendlyIndex": 84.3,
    "attractionIndex": 22.2,
    "rankNo": 20,
    "longitude": 112.938814,
    "latitude": 28.228209
  },
  {
    "province": "香港",
    "city": "香港",
    "jobCount": 5,
    "avgSalary": 0,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 21.9,
    "rankNo": 21,
    "longitude": 114.169361,
    "latitude": 22.319303
  },
  {
    "province": "广东",
    "city": "台山",
    "jobCount": 1,
    "avgSalary": 0,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 21.6,
    "rankNo": 22,
    "longitude": 112.793812,
    "latitude": 22.251947
  },
  {
    "province": "山东",
    "city": "日照",
    "jobCount": 1,
    "avgSalary": 0,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 21.6,
    "rankNo": 23,
    "longitude": 119.526888,
    "latitude": 35.416377
  },
  {
    "province": "山东",
    "city": "济南",
    "jobCount": 7,
    "avgSalary": 4500,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 21.4,
    "rankNo": 24,
    "longitude": 117.120128,
    "latitude": 36.652069
  },
  {
    "province": "宁夏",
    "city": "银川",
    "jobCount": 1,
    "avgSalary": 5250,
    "freshFriendlyIndex": 100.0,
    "attractionIndex": 21.4,
    "rankNo": 25,
    "longitude": 106.230909,
    "latitude": 38.487193
  },
  {
    "province": "湖北",
    "city": "武汉",
    "jobCount": 283,
    "avgSalary": 7529,
    "freshFriendlyIndex": 11.7,
    "attractionIndex": 19.4,
    "rankNo": 26,
    "longitude": 114.305393,
    "latitude": 30.593099
  },
  {
    "province": "江苏",
    "city": "无锡",
    "jobCount": 48,
    "avgSalary": 7061,
    "freshFriendlyIndex": 72.9,
    "attractionIndex": 19.2,
    "rankNo": 27,
    "longitude": 120.31191,
    "latitude": 31.49117
  },
  {
    "province": "广东",
    "city": "深圳",
    "jobCount": 88,
    "avgSalary": 9160,
    "freshFriendlyIndex": 58.0,
    "attractionIndex": 19.2,
    "rankNo": 28,
    "longitude": 114.057868,
    "latitude": 22.543099
  },
  {
    "province": "海南",
    "city": "海口",
    "jobCount": 130,
    "avgSalary": 6124,
    "freshFriendlyIndex": 50.0,
    "attractionIndex": 18.5,
    "rankNo": 29,
    "longitude": 110.198293,
    "latitude": 20.044001
  },
  {
    "province": "云南",
    "city": "昆明",
    "jobCount": 239,
    "avgSalary": 3894,
    "freshFriendlyIndex": 25.5,
    "attractionIndex": 18.4,
    "rankNo": 30,
    "longitude": 102.832891,
    "latitude": 24.880095
  },
  {
    "province": "西藏",
    "city": "拉萨",
    "jobCount": 15,
    "avgSalary": 7177,
    "freshFriendlyIndex": 66.7,
    "attractionIndex": 16.3,
    "rankNo": 31,
    "longitude": 91.140856,
    "latitude": 29.645554
  },
  {
    "province": "广西",
    "city": "南宁",
    "jobCount": 103,
    "avgSalary": 5446,
    "freshFriendlyIndex": 47.6,
    "attractionIndex": 16.3,
    "rankNo": 32,
    "longitude": 108.366543,
    "latitude": 22.817002
  },
  {
    "province": "贵州",
    "city": "贵阳",
    "jobCount": 2,
    "avgSalary": 16250,
    "freshFriendlyIndex": 50.0,
    "attractionIndex": 16.0,
    "rankNo": 33,
    "longitude": 106.630153,
    "latitude": 26.647661
  },
  {
    "province": "福建",
    "city": "厦门",
    "jobCount": 57,
    "avgSalary": 6712,
    "freshFriendlyIndex": 54.4,
    "attractionIndex": 15.8,
    "rankNo": 34,
    "longitude": 118.089425,
    "latitude": 24.479833
  },
  {
    "province": "河南",
    "city": "郑州",
    "jobCount": 42,
    "avgSalary": 4500,
    "freshFriendlyIndex": 57.1,
    "attractionIndex": 14.7,
    "rankNo": 35,
    "longitude": 113.625368,
    "latitude": 34.746599
  },
  {
    "province": "江西",
    "city": "南昌",
    "jobCount": 36,
    "avgSalary": 6801,
    "freshFriendlyIndex": 52.8,
    "attractionIndex": 14.4,
    "rankNo": 36,
    "longitude": 115.858197,
    "latitude": 28.682892
  },
  {
    "province": "浙江",
    "city": "嘉兴",
    "jobCount": 113,
    "avgSalary": 6995,
    "freshFriendlyIndex": 25.7,
    "attractionIndex": 13.1,
    "rankNo": 37,
    "longitude": 120.755486,
    "latitude": 30.746129
  },
  {
    "province": "辽宁",
    "city": "沈阳",
    "jobCount": 28,
    "avgSalary": 5600,
    "freshFriendlyIndex": 50.0,
    "attractionIndex": 13.0,
    "rankNo": 38,
    "longitude": 123.431475,
    "latitude": 41.805698
  },
  {
    "province": "甘肃",
    "city": "兰州",
    "jobCount": 14,
    "avgSalary": 8536,
    "freshFriendlyIndex": 42.9,
    "attractionIndex": 12.0,
    "rankNo": 39,
    "longitude": 103.834303,
    "latitude": 36.061089
  },
  {
    "province": "山东",
    "city": "威海",
    "jobCount": 2,
    "avgSalary": 0,
    "freshFriendlyIndex": 50.0,
    "attractionIndex": 11.7,
    "rankNo": 40,
    "longitude": 122.12042,
    "latitude": 37.513068
  },
  {
    "province": "福建",
    "city": "福州",
    "jobCount": 141,
    "avgSalary": 6397,
    "freshFriendlyIndex": 2.1,
    "attractionIndex": 9.6,
    "rankNo": 41,
    "longitude": 119.296494,
    "latitude": 26.074508
  },
  {
    "province": "山西",
    "city": "太原",
    "jobCount": 148,
    "avgSalary": 5183,
    "freshFriendlyIndex": 0.0,
    "attractionIndex": 9.1,
    "rankNo": 42,
    "longitude": 112.548879,
    "latitude": 37.87059
  },
  {
    "province": "浙江",
    "city": "杭州",
    "jobCount": 42,
    "avgSalary": 4623,
    "freshFriendlyIndex": 23.8,
    "attractionIndex": 8.0,
    "rankNo": 43,
    "longitude": 120.15507,
    "latitude": 30.274085
  },
  {
    "province": "浙江",
    "city": "宁波",
    "jobCount": 2,
    "avgSalary": 5400,
    "freshFriendlyIndex": 0.0,
    "attractionIndex": 1.5,
    "rankNo": 44,
    "longitude": 121.550357,
    "latitude": 29.874556
  }
]

export const overview: DashboardOverview = {
  "totalJobs": 37772,
  "averageSalary": 5681,
  "coveredCities": 350,
  "freshFriendlyIndex": 48.6,
  "hotCities": [
    {
      "name": "西安",
      "value": 1281,
      "score": 70.2,
      "tag": "陕西"
    },
    {
      "name": "北京",
      "value": 1099,
      "score": 65.9,
      "tag": "北京"
    },
    {
      "name": "重庆",
      "value": 814,
      "score": 58.3,
      "tag": "重庆"
    },
    {
      "name": "哈尔滨",
      "value": 660,
      "score": 48.5,
      "tag": "黑龙江"
    },
    {
      "name": "长春",
      "value": 775,
      "score": 42.2,
      "tag": "吉林"
    },
    {
      "name": "苏州",
      "value": 489,
      "score": 38.9,
      "tag": "江苏"
    },
    {
      "name": "大连",
      "value": 353,
      "score": 36.0,
      "tag": "辽宁"
    },
    {
      "name": "西宁",
      "value": 257,
      "score": 34.8,
      "tag": "青海"
    },
    {
      "name": "青岛",
      "value": 264,
      "score": 33.4,
      "tag": "山东"
    },
    {
      "name": "常州",
      "value": 333,
      "score": 31.3,
      "tag": "江苏"
    }
  ],
  "hotIndustries": [
    {
      "name": "不便分类的其他从业人员",
      "value": 4978,
      "score": 100.0,
      "tag": "真实样本"
    },
    {
      "name": "生产制造及有关人员",
      "value": 2632,
      "score": 52.9,
      "tag": "真实样本"
    },
    {
      "name": "专业技术人员",
      "value": 1986,
      "score": 39.9,
      "tag": "真实样本"
    },
    {
      "name": "销售人员",
      "value": 1827,
      "score": 36.7,
      "tag": "真实样本"
    },
    {
      "name": "其他专业技术人员",
      "value": 1558,
      "score": 31.3,
      "tag": "真实样本"
    },
    {
      "name": "其他生产制造及有关人员",
      "value": 1544,
      "score": 31.0,
      "tag": "真实样本"
    },
    {
      "name": "机械冷加工人员",
      "value": 1225,
      "score": 24.6,
      "tag": "真实样本"
    },
    {
      "name": "社会生产服务和生活服务人员",
      "value": 1066,
      "score": 21.4,
      "tag": "真实样本"
    },
    {
      "name": "其他工程技术人员",
      "value": 973,
      "score": 19.5,
      "tag": "真实样本"
    },
    {
      "name": "未分类",
      "value": 791,
      "score": 15.9,
      "tag": "真实样本"
    }
  ],
  "monthlyTrend": [
    {
      "month": "2025-06",
      "jobs": 3,
      "freshJobs": 2,
      "aiJobs": 0
    },
    {
      "month": "2025-07",
      "jobs": 13,
      "freshJobs": 4,
      "aiJobs": 0
    },
    {
      "month": "2025-08",
      "jobs": 908,
      "freshJobs": 3,
      "aiJobs": 0
    },
    {
      "month": "2025-09",
      "jobs": 222,
      "freshJobs": 2,
      "aiJobs": 0
    },
    {
      "month": "2025-10",
      "jobs": 208,
      "freshJobs": 1,
      "aiJobs": 0
    },
    {
      "month": "2025-11",
      "jobs": 12,
      "freshJobs": 5,
      "aiJobs": 0
    },
    {
      "month": "2025-12",
      "jobs": 1482,
      "freshJobs": 752,
      "aiJobs": 5
    },
    {
      "month": "2026-01",
      "jobs": 274,
      "freshJobs": 103,
      "aiJobs": 0
    },
    {
      "month": "2026-02",
      "jobs": 515,
      "freshJobs": 362,
      "aiJobs": 1
    },
    {
      "month": "2026-03",
      "jobs": 3577,
      "freshJobs": 2595,
      "aiJobs": 9
    },
    {
      "month": "2026-04",
      "jobs": 9456,
      "freshJobs": 4868,
      "aiJobs": 32
    },
    {
      "month": "2026-05",
      "jobs": 19727,
      "freshJobs": 9219,
      "aiJobs": 38
    }
  ]
}

export const analysis: DashboardAnalysis = {
  "salaryRanges": [
    {
      "name": "6K以下",
      "value": 63
    },
    {
      "name": "6K-10K",
      "value": 30
    },
    {
      "name": "10K-15K",
      "value": 5
    },
    {
      "name": "15K-25K",
      "value": 2
    },
    {
      "name": "25K以上",
      "value": 1
    }
  ],
  "education": [
    {
      "name": "不限",
      "value": 73
    },
    {
      "name": "大专",
      "value": 17
    },
    {
      "name": "本科",
      "value": 9
    },
    {
      "name": "硕士",
      "value": 1
    },
    {
      "name": "博士",
      "value": 0
    }
  ],
  "experience": [
    {
      "name": "应届/不限",
      "value": 49
    },
    {
      "name": "1-3年",
      "value": 47
    },
    {
      "name": "3-5年",
      "value": 1
    },
    {
      "name": "5年以上",
      "value": 4
    }
  ],
  "skills": [
    {
      "skill": "生产",
      "frequency": 8027,
      "heatIndex": 100.0,
      "category": "综合岗位",
      "trendScore": 100.0
    },
    {
      "skill": "管理",
      "frequency": 4489,
      "heatIndex": 55.9,
      "category": "综合岗位",
      "trendScore": 55.9
    },
    {
      "skill": "销售",
      "frequency": 3957,
      "heatIndex": 49.3,
      "category": "综合岗位",
      "trendScore": 49.3
    },
    {
      "skill": "机械",
      "frequency": 3490,
      "heatIndex": 43.5,
      "category": "综合岗位",
      "trendScore": 43.5
    },
    {
      "skill": "沟通",
      "frequency": 2910,
      "heatIndex": 36.3,
      "category": "综合岗位",
      "trendScore": 36.3
    },
    {
      "skill": "安全",
      "frequency": 1374,
      "heatIndex": 17.1,
      "category": "综合岗位",
      "trendScore": 17.1
    },
    {
      "skill": "质量",
      "frequency": 1269,
      "heatIndex": 15.8,
      "category": "综合岗位",
      "trendScore": 15.8
    },
    {
      "skill": "运营",
      "frequency": 986,
      "heatIndex": 12.3,
      "category": "综合岗位",
      "trendScore": 12.3
    },
    {
      "skill": "会计",
      "frequency": 923,
      "heatIndex": 11.5,
      "category": "综合岗位",
      "trendScore": 11.5
    },
    {
      "skill": "电气",
      "frequency": 694,
      "heatIndex": 8.6,
      "category": "综合岗位",
      "trendScore": 8.6
    },
    {
      "skill": "财务",
      "frequency": 643,
      "heatIndex": 8.0,
      "category": "综合岗位",
      "trendScore": 8.0
    },
    {
      "skill": "金融",
      "frequency": 548,
      "heatIndex": 6.8,
      "category": "综合岗位",
      "trendScore": 6.8
    },
    {
      "skill": "仓储",
      "frequency": 504,
      "heatIndex": 6.3,
      "category": "综合岗位",
      "trendScore": 6.3
    },
    {
      "skill": "采购",
      "frequency": 482,
      "heatIndex": 6.0,
      "category": "综合岗位",
      "trendScore": 6.0
    },
    {
      "skill": "护理",
      "frequency": 366,
      "heatIndex": 4.6,
      "category": "综合岗位",
      "trendScore": 4.6
    },
    {
      "skill": "Excel",
      "frequency": 353,
      "heatIndex": 4.4,
      "category": "综合岗位",
      "trendScore": 4.4
    },
    {
      "skill": "英语",
      "frequency": 310,
      "heatIndex": 3.9,
      "category": "综合岗位",
      "trendScore": 3.9
    },
    {
      "skill": "物流",
      "frequency": 304,
      "heatIndex": 3.8,
      "category": "综合岗位",
      "trendScore": 3.8
    },
    {
      "skill": "Office",
      "frequency": 285,
      "heatIndex": 3.6,
      "category": "综合岗位",
      "trendScore": 3.6
    },
    {
      "skill": "客户服务",
      "frequency": 212,
      "heatIndex": 2.6,
      "category": "综合岗位",
      "trendScore": 2.6
    },
    {
      "skill": "数据分析",
      "frequency": 198,
      "heatIndex": 2.5,
      "category": "综合岗位",
      "trendScore": 2.5
    },
    {
      "skill": "银行",
      "frequency": 165,
      "heatIndex": 2.1,
      "category": "综合岗位",
      "trendScore": 2.1
    },
    {
      "skill": "Python",
      "frequency": 34,
      "heatIndex": 0.4,
      "category": "综合岗位",
      "trendScore": 0.4
    },
    {
      "skill": "人工智能",
      "frequency": 33,
      "heatIndex": 0.4,
      "category": "算法工程师",
      "trendScore": 0.4
    },
    {
      "skill": "SQL",
      "frequency": 33,
      "heatIndex": 0.4,
      "category": "综合岗位",
      "trendScore": 0.4
    },
    {
      "skill": "大数据",
      "frequency": 25,
      "heatIndex": 0.3,
      "category": "综合岗位",
      "trendScore": 0.3
    },
    {
      "skill": "MySQL",
      "frequency": 21,
      "heatIndex": 0.3,
      "category": "综合岗位",
      "trendScore": 0.3
    },
    {
      "skill": "Linux",
      "frequency": 17,
      "heatIndex": 0.2,
      "category": "综合岗位",
      "trendScore": 0.2
    },
    {
      "skill": "前端开发",
      "frequency": 11,
      "heatIndex": 0.1,
      "category": "前端开发",
      "trendScore": 0.1
    },
    {
      "skill": "后端开发",
      "frequency": 7,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "Redis",
      "frequency": 11,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "Vue",
      "frequency": 6,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "云计算",
      "frequency": 7,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "PyTorch",
      "frequency": 7,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "机器学习",
      "frequency": 6,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    },
    {
      "skill": "深度学习",
      "frequency": 9,
      "heatIndex": 0.1,
      "category": "综合岗位",
      "trendScore": 0.1
    }
  ]
}

export const liveJobs: JobLiveItem[] = [
  {
    "time": "2026-05-19",
    "city": "邢台",
    "title": "抬板封架工",
    "company": "河北省人才交流服务中心",
    "salary": "5000-5000元",
    "skills": "不便分类的其他从业人员"
  },
  {
    "time": "2026-05-18",
    "city": "随州",
    "title": "人事文员",
    "company": "随州市就业局",
    "salary": "3000-4000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "咸宁",
    "title": "维修工",
    "company": "咸宁市就业局",
    "salary": "5000-7000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "铲车工",
    "company": "黄冈市劳动就业管理局",
    "salary": "4000-5000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "行车学徒",
    "company": "黄冈市劳动就业管理局",
    "salary": "4000-5000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "营销文员",
    "company": "黄冈市劳动就业管理局",
    "salary": "4000-5000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "车位工",
    "company": "黄冈市劳动就业管理局",
    "salary": "5000-7000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "注塑机调机维护技术员",
    "company": "黄冈市劳动就业管理局",
    "salary": "7000-10000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "SMT机台操作岗",
    "company": "黄冈市劳动就业管理局",
    "salary": "5000-7000元",
    "skills": "专业技术人员"
  },
  {
    "time": "2026-05-18",
    "city": "黄冈",
    "title": "车位工（生手）",
    "company": "黄冈市劳动就业管理局",
    "salary": "3000-4000元",
    "skills": "专业技术人员"
  }
]

export const mockSalaryPrediction: SalaryPrediction = {
  predictedMin: Math.round(overview.averageSalary * 0.82),
  predictedMax: Math.round(overview.averageSalary * 1.24),
  predictedAvg: overview.averageSalary,
  confidence: 72.5,
  modelName: 'RealDataBaseline',
  explanation: '基于真实岗位样本平均薪资生成的前端兜底预测；后端可接入 data-processing 输出的模型文件。',
  influenceFactors: ['真实样本平均薪资', '城市岗位样本', '行业样本', '学历经验分布', '技能文本']
}

export const mockRecommendations: CareerRecommendation[] = [
  {
    direction: '生产制造与设备操作方向',
    city: cityMetrics[0]?.city ?? '西安',
    industry: '生产制造及有关人员',
    jobCategory: '生产制造与设备操作',
    matchScore: 82,
    salaryPotential: overview.averageSalary,
    reason: '根据最新真实样本中的城市、行业和技能热度生成兜底推荐。',
    skillGaps: ['安全', '质量', '机械'],
    suggestions: ['优先选择真实样本岗位数较高的城市', '补齐安全、质量和设备基础', '投递前核对目标岗位薪资是否公开']
  }
]
