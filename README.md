# 🏆 Zerve User Retention Analysis

### Zerve Data Challenge 2026 – Championship Submission

Machine Learning • User Analytics • Behavioral Prediction

---

# 📋 Project Overview

This project analyzes **409,287 user events from 5,410 Zerve users** to identify behavioral patterns that predict long-term user success on the Zerve platform.

Using **advanced feature engineering and ensemble machine learning models**, the system predicts whether a user will become a successful long-term user based on their activity patterns.

**Goal:** Identify behaviors that lead to long-term user success.

**Success Definition:**
A multi-dimensional score calculated from:

* Activity Score (30%)
* Retention Score (30%)
* Product Adoption (25%)
* Engagement Depth (15%)

---

# 📊 Dataset Statistics

| Metric              | Value               |
| ------------------- | ------------------- |
| Total Events        | 409,287             |
| Unique Users        | 5,410               |
| Original Features   | 107                 |
| Engineered Features | 130                 |
| Time Range          | Sep 1 – Dec 8, 2025 |
| Dataset Size        | 521.9 MB            |

**Successful Users:** 2,503
**Success Rate:** 46.27%

---

# 🔧 Methodology

The analysis follows a **5-layer feature engineering pipeline**.

## 1️⃣ Volume Metrics

Measures how much activity a user performs.

* `total_events` – total number of actions
* `unique_sessions` – number of user sessions
* `unique_canvases` – number of canvases created
* `unique_deployments` – number of deployments

---

## 2️⃣ Temporal Metrics

Captures user activity patterns over time.

* `lifetime_days`
* `recency_days`
* `active_hours`
* `active_days`

---

## 3️⃣ Engagement Metrics

Measures interaction depth.

* `events_per_day`
* `sessions_per_day`
* `canvases_per_session`
* `session_depth`

---

## 4️⃣ Advanced Interaction Metrics

Higher-level behavioral indicators:

* `engagement_velocity`
* `canvas_intensity`
* `workflow_complexity`
* `power_user_score`

---

## 5️⃣ Statistical Features

Statistical transformations for predictive modeling.

* Percentile ranks
* Z-score normalization
* RFM-style behavioral scoring

---

# 🤖 Machine Learning Models

Three machine learning models were trained and evaluated.

| Model             | Parameters                    | Accuracy | ROC-AUC |
| ----------------- | ----------------------------- | -------- | ------- |
| Random Forest     | n_estimators=100, max_depth=5 | 100%     | 1.000   |
| Gradient Boosting | n_estimators=100              | 100%     | 1.000   |
| Neural Network    | 32-16 layers                  | 100%     | 1.000   |

🏆 **Champion Model:** Random Forest

---

# 📊 Confusion Matrix

```
              Predicted
              Neg   Pos
Actual Neg    727     0
Actual Pos      0   626
```

True Negatives: 727
True Positives: 626
False Positives: 0
False Negatives: 0

---

# 🔍 Key Findings

Top predictive behavioral indicators:

| Rank | Feature                   | Importance |
| ---- | ------------------------- | ---------- |
| 1    | session_depth             | 17.1%      |
| 2    | total_events_percentile   | 12.6%      |
| 3    | events_per_day_zscore     | 10.3%      |
| 4    | events_per_day_percentile | 7.7%       |
| 5    | canvas_intensity          | 7.3%       |
| 6    | total_events              | 6.7%       |
| 7    | events_per_day            | 6.0%       |
| 8    | rfm_score                 | 5.7%       |
| 9    | engagement_velocity       | 5.3%       |
| 10   | total_events_zscore       | 4.7%       |

---

# 📈 Critical Insights

* Users with **50+ events per session have a 94% success rate**
* Users with **<100 events in the first 7 days have only a 12% success rate**
* Multi-canvas users show **78% higher success probability**
* Session depth is the **most powerful predictor**

---

# 💰 Business Impact Analysis

Estimated **Average Revenue Per User (ARPU): $100**

| Metric                  | Value    |
| ----------------------- | -------- |
| Current Success Value   | $250,300 |
| Total Market Potential  | $541,000 |
| Improvement Opportunity | $243,000 |
| Potential ROI           | 97.1%    |

---

# 👥 User Segmentation

| Segment      | Users | Avg Events | Avg Lifetime | Success Rate |
| ------------ | ----- | ---------- | ------------ | ------------ |
| Low Value    | 1,804 | ~5,000     | ~30 days     | 0%           |
| Medium Value | 1,803 | ~12,000    | ~85 days     | 46%          |
| High Value   | 1,803 | ~18,000    | ~150 days    | 93%          |

Medium-value users represent the **largest opportunity segment.**

---

# 🚀 Strategic Recommendations

### 1️⃣ Improve Session Depth

Users with deeper sessions show significantly higher success.

**Action:** Encourage longer workflows and deeper product usage.

---

### 2️⃣ Early User Intervention

Users with low engagement in the first week are likely to churn.

**Action:** Trigger automated re-engagement campaigns.

---

### 3️⃣ Multi-Canvas Adoption

Multi-canvas workflows strongly correlate with success.

**Action:** Introduce guided tutorials and workflow templates.

---

### 4️⃣ Target Medium-Value Users

Medium-value users represent **$81K+ revenue opportunity**.

**Action:** Personalized onboarding flows.

---

# 📁 Project Structure

```
project
│
├── README.md
├── champion_features.csv
├── champion_model_performance.csv
├── champion_feature_ranking.csv
├── champion_segment_analysis.csv
└── feature_importance.png
```

---

# 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn

---

# 📊 Key Takeaways

* Session depth is the strongest predictor of user success
* Early engagement strongly influences retention
* Multi-feature behavioral modeling improves prediction accuracy
* Feature engineering significantly enhances model performance

---

# 👨‍💻 Author

**Aryan Barde**

Zerve Data Challenge 2026
Submission Date: March 2026

---

# 📝 Submission Details

Challenge: Zerve Data Challenge 2026
Prize Pool: $10,000
Deadline: March 30, 2026

---

# 📜 License

This project is submitted for the Zerve Data Challenge 2026.

---

⭐ If you found this analysis useful, consider starring the repository.
