CREATE DATABASE IF NOT EXISTS graduate_employment
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE graduate_employment;

DROP TABLE IF EXISTS career_recommendation;
DROP TABLE IF EXISTS salary_prediction_record;
DROP TABLE IF EXISTS graduate_profile;
DROP TABLE IF EXISTS skill_keyword;
DROP TABLE IF EXISTS city_employment_index;
DROP TABLE IF EXISTS province_employment_index;
DROP TABLE IF EXISTS job_post;

CREATE TABLE job_post (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '岗位ID',
  job_title VARCHAR(160) NOT NULL COMMENT '岗位名称',
  company_name VARCHAR(180) NOT NULL COMMENT '公司名称',
  province VARCHAR(60) NOT NULL COMMENT '工作省份',
  city VARCHAR(60) NOT NULL COMMENT '工作城市',
  salary_text VARCHAR(80) COMMENT '原始薪资文本',
  salary_min DECIMAL(10,2) COMMENT '最低月薪，单位元',
  salary_max DECIMAL(10,2) COMMENT '最高月薪，单位元',
  salary_avg DECIMAL(10,2) COMMENT '平均月薪，单位元',
  education_requirement VARCHAR(60) COMMENT '学历要求',
  experience_requirement VARCHAR(80) COMMENT '经验要求',
  industry VARCHAR(120) COMMENT '行业类别',
  major_requirement VARCHAR(180) COMMENT '专业要求',
  company_size VARCHAR(80) COMMENT '公司规模',
  company_type VARCHAR(80) COMMENT '公司性质',
  job_category VARCHAR(120) COMMENT '岗位类别',
  job_description TEXT COMMENT '岗位描述',
  skills VARCHAR(500) COMMENT '技能标签，逗号分隔',
  longitude DECIMAL(10,6) COMMENT '经度',
  latitude DECIMAL(10,6) COMMENT '纬度',
  publish_date DATE COMMENT '发布时间',
  source_dataset VARCHAR(120) COMMENT '来源数据集',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_job_city (province, city),
  INDEX idx_job_industry (industry),
  INDEX idx_job_publish_date (publish_date),
  INDEX idx_job_salary (salary_avg)
) COMMENT='清洗后的招聘岗位明细表';

CREATE TABLE province_employment_index (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  province VARCHAR(60) NOT NULL,
  job_count INT NOT NULL DEFAULT 0,
  avg_salary DECIMAL(10,2) NOT NULL DEFAULT 0,
  fresh_friendly_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  employment_heat_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  top_industry VARCHAR(120),
  growth_rate DECIMAL(6,2) DEFAULT 0,
  stat_month CHAR(7) NOT NULL COMMENT '统计月份 YYYY-MM',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_province_month (province, stat_month),
  INDEX idx_province_heat (employment_heat_index)
) COMMENT='省份就业态势指标表';

CREATE TABLE city_employment_index (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  province VARCHAR(60) NOT NULL,
  city VARCHAR(60) NOT NULL,
  job_count INT NOT NULL DEFAULT 0,
  avg_salary DECIMAL(10,2) NOT NULL DEFAULT 0,
  industry_diversity DECIMAL(6,2) NOT NULL DEFAULT 0,
  fresh_friendly_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  education_threshold_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  experience_threshold_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  city_attraction_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  rank_no INT,
  longitude DECIMAL(10,6),
  latitude DECIMAL(10,6),
  stat_month CHAR(7) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_city_month (city, stat_month),
  INDEX idx_city_rank (rank_no),
  INDEX idx_city_attraction (city_attraction_index)
) COMMENT='城市就业吸引力指标表';

CREATE TABLE skill_keyword (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  skill_name VARCHAR(80) NOT NULL,
  job_category VARCHAR(120),
  industry VARCHAR(120),
  frequency_count INT NOT NULL DEFAULT 0,
  tfidf_weight DECIMAL(10,6) NOT NULL DEFAULT 0,
  textrank_weight DECIMAL(10,6) NOT NULL DEFAULT 0,
  trend_score DECIMAL(6,2) NOT NULL DEFAULT 0,
  heat_index DECIMAL(6,2) NOT NULL DEFAULT 0,
  stat_month CHAR(7) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_skill_category_month (skill_name, job_category, stat_month),
  INDEX idx_skill_heat (heat_index)
) COMMENT='技能关键词热度表';

CREATE TABLE graduate_profile (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  student_no VARCHAR(60),
  major VARCHAR(120) NOT NULL,
  education VARCHAR(60) NOT NULL,
  skills VARCHAR(500),
  expected_cities VARCHAR(300),
  expected_industries VARCHAR(300),
  expected_salary DECIMAL(10,2),
  preference_note VARCHAR(500),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT='高校毕业生职业画像表';

CREATE TABLE salary_prediction_record (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  city VARCHAR(60) NOT NULL,
  industry VARCHAR(120) NOT NULL,
  education VARCHAR(60) NOT NULL,
  experience VARCHAR(80) NOT NULL,
  company_size VARCHAR(80),
  job_category VARCHAR(120) NOT NULL,
  predicted_salary_min DECIMAL(10,2) NOT NULL,
  predicted_salary_max DECIMAL(10,2) NOT NULL,
  predicted_salary_avg DECIMAL(10,2) NOT NULL,
  confidence_score DECIMAL(6,2) NOT NULL DEFAULT 0,
  model_name VARCHAR(80) NOT NULL,
  model_version VARCHAR(40) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_salary_prediction_city (city),
  INDEX idx_salary_prediction_created (created_at)
) COMMENT='薪资预测记录表';

CREATE TABLE career_recommendation (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  profile_id BIGINT,
  recommended_direction VARCHAR(160) NOT NULL,
  recommended_city VARCHAR(60) NOT NULL,
  recommended_industry VARCHAR(120) NOT NULL,
  recommended_job_category VARCHAR(120) NOT NULL,
  match_score DECIMAL(6,2) NOT NULL,
  salary_potential DECIMAL(10,2),
  reason_text VARCHAR(800),
  skill_gap VARCHAR(500),
  improvement_suggestion VARCHAR(800),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_recommendation_profile
    FOREIGN KEY (profile_id) REFERENCES graduate_profile(id)
    ON DELETE SET NULL,
  INDEX idx_recommendation_profile (profile_id),
  INDEX idx_recommendation_score (match_score)
) COMMENT='职业推荐结果表';
