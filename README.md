# 📊 Correlation Heatmap & Pairwise Relationships

**Week 2 — Project 3 | Syntecxhub Data Science Internship**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat-square&logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4C72B0?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)

---

## 📌 Project Overview

This project performs a complete **correlation analysis** on a retail customer dataset using Python. It computes Pearson correlation coefficients between all numeric features, visualizes them through multiple professional chart types, and summarizes the strongest positive and negative relationships with written interpretation.

> **Domain:** Retail & Customer Analytics  
> **Dataset:** 200 customer records × 8 numeric features  
> **Tools:** Python, Pandas, NumPy, Seaborn, Matplotlib

---

## 🎯 Objectives

- ✅ Compute **Pearson correlations** between all numeric features
- ✅ Visualize as a **heatmap** with masked upper triangle and annotated values
- ✅ Generate **pairplots / scatter matrix** for key variable pairs
- ✅ Summarize the **strongest positive and negative** relationships
- ✅ Export all charts to PNG and correlation data to Excel

---

## 📁 Project Structure

```
Week2_Project3_Correlation_Heatmap/
│
├── week2_project3_correlation_heatmap.py   # Main Python script
├── customer_dataset.csv                    # Input dataset (200 rows × 8 cols)
├── README.md                               # Project documentation
│
└── correlation_output/                     # Auto-generated on running script
    ├── 01_correlation_heatmap.png          # Masked & annotated Pearson heatmap
    ├── 02_pairplot_key_variables.png       # Pairplot with r-values
    ├── 03_scatter_strongest_pairs.png      # Top 6 pairs with regression lines
    ├── 04_feature_vs_satisfaction.png      # Feature correlation bar chart
    ├── 05_full_scatter_matrix.png          # All variables scatter matrix
    └── correlation_matrix.xlsx            # Excel: matrix + pairs + stats + data
```

---

## 📊 Dataset Description

The dataset simulates a **retail customer profile** with 8 numeric features:

| Feature | Description | Type |
|---|---|---|
| `Age` | Customer age (18–64) | Integer |
| `Annual_Income` | Yearly income in INR | Integer |
| `Spending_Score` | Spending behaviour score (5–95) | Float |
| `Purchase_Freq` | Average monthly purchases | Float |
| `Avg_Order_Value` | Average order value in INR | Float |
| `Loyalty_Years` | Years as a customer | Float |
| `Returns_Pct` | Percentage of orders returned | Float |
| `Satisfaction` | Customer satisfaction score (1–5) | Float |

---

## 🔍 Key Findings

### Strongest Positive Correlations
| Pair | r Value | Interpretation |
|---|---|---|
| Avg_Order_Value ↔ Annual_Income | **r = 0.938** | Higher income customers place significantly larger orders |
| Loyalty_Years ↔ Age | **r = 0.910** | Older customers naturally have longer loyalty history |
| Annual_Income ↔ Age | **r = 0.815** | Income tends to grow with age and career progression |
| Avg_Order_Value ↔ Age | **r = 0.754** | Older, higher-income customers spend more per order |

### Strongest Negative Correlations
| Pair | r Value | Interpretation |
|---|---|---|
| Satisfaction ↔ Returns_Pct | **r = −0.641** | More returns strongly associated with lower satisfaction |
| Spending_Score ↔ Returns_Pct | **r = −0.519** | High-spending customers return less frequently |
| Satisfaction ↔ Age | **r = −0.472** | Younger customers tend to report higher satisfaction |
| Spending_Score ↔ Age | **r = −0.686** | Younger customers have higher spending scores |

---

## 📈 Visualizations Generated

### 1. Pearson Correlation Heatmap
> Full lower-triangle heatmap with annotated r-values, diverging colour scale (blue = positive, red = negative).

### 2. Pairplot — Key Variables
> Scatter plots for all combinations of 5 key variables with KDE on the diagonal and r-values annotated on each cell.

### 3. Scatter Plots — Strongest Pairs
> Top 6 strongest relationships plotted individually with regression lines, showing direction and strength clearly.

### 4. Feature Correlation Bar Chart
> Horizontal bar chart ranking every feature by its correlation with Customer Satisfaction — colour-coded by direction.

### 5. Full Scatter Matrix
> Complete scatter matrix for all 8 variables with KDE distributions on the diagonal.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data manipulation, correlation computation |
| `numpy` | Numerical operations, masking |
| `seaborn` | Heatmap, pairplot, KDE visualizations |
| `matplotlib` | Scatter plots, bar charts, scatter matrix |
| `openpyxl` | Export results to multi-sheet Excel |

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/Syntecxhub_Project_Name.git
cd Syntecxhub_Project_Name/Week2_Project3_Correlation_Heatmap
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 3. Run the Script
```bash
python week2_project3_correlation_heatmap.py
```

### 4. View Outputs
All charts and reports are saved automatically inside the `correlation_output/` folder.

---

## 📤 Output Files

| File | Description |
|---|---|
| `01_correlation_heatmap.png` | Masked Pearson heatmap with annotated values |
| `02_pairplot_key_variables.png` | Pairplot of 5 key variables with KDE diagonals |
| `03_scatter_strongest_pairs.png` | Top 6 pairs with regression lines |
| `04_feature_vs_satisfaction.png` | All features ranked by correlation with Satisfaction |
| `05_full_scatter_matrix.png` | Full 8×8 scatter matrix |
| `correlation_matrix.xlsx` | Excel workbook with 4 sheets: Correlation Matrix, All Pairs Ranked, Dataset Stats, Raw Data |

---

## 💡 Chart Choice Discussion

| Chart Type | Why It Was Used |
|---|---|
| **Heatmap** | Best for showing all pairwise correlations simultaneously; masking the upper triangle avoids redundancy; annotation makes exact values readable at a glance |
| **Pairplot** | Combines scatter plots and KDE distributions in one view, ideal for exploring both relationships and distributions across multiple variables |
| **Scatter + Regression** | Isolates the strongest relationships individually; regression line makes the direction and slope of the relationship visually clear |
| **Bar Chart** | Most effective way to rank features by their influence on a single target variable (Satisfaction) with clear positive/negative colour coding |
| **Scatter Matrix** | Gives a complete bird's-eye view of all variable combinations in one compact figure |

---

## 🧠 Interpretation Summary

The analysis reveals that **Annual Income and Avg Order Value share the strongest linear relationship** (r = 0.938), which is expected — customers with higher incomes tend to spend more per transaction. **Loyalty Years and Age** (r = 0.910) also show a near-perfect correlation, simply because older customers have had more time to accumulate loyalty.

On the negative side, **Returns Percentage is the single strongest predictor of low Satisfaction** (r = −0.641), suggesting that reducing return rates should be a top priority for improving customer experience. Similarly, **younger customers score higher on Spending Score** but also report higher Satisfaction — pointing to an opportunity to better engage older, high-income segments.

---

## 👤 Author

**Syntecxhub Data Science Internship**  
📧 info@syntecxhub.com  
🌐 [www.syntecxhub.com](https://www.syntecxhub.com)

---

## 📄 License

This project was completed as part of the **Syntecxhub Internship Program**.  
© 2026 Syntecxhub. All rights reserved.
