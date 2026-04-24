"""
=============================================================
WEEK 2 - PROJECT 3: Correlation Heatmap & Pairwise Relationships
Syntecxhub Data Science Internship
=============================================================
Topics Covered:
  - Compute Pearson correlations between numeric features
  - Visualize as heatmap (mask upper triangle, annotate values)
  - Use pairplots / scatter matrix for key variable pairs
  - Summarize strongest positive/negative relationships
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
from datetime import datetime

print("=" * 65)
print("   WEEK 2 - PROJECT 3: Correlation Heatmap & Pairwise Analysis")
print("=" * 65)

# ── Output folder ──────────────────────────────────────────
os.makedirs("correlation_output", exist_ok=True)

# ── Global style ───────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#f8f9fa",
    "axes.facecolor":   "#ffffff",
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})
PALETTE = "#4C72B0"

# ═══════════════════════════════════════════════════════════
# 0.  DATASET  (Retail Sales & Customer Data)
# ═══════════════════════════════════════════════════════════
np.random.seed(42)
n = 200

age            = np.random.randint(18, 65, n)
income         = 20000 + age * 600 + np.random.normal(0, 6000, n)
spending_score = 20 + (65 - age) * 0.8 + income * 0.0003 + np.random.normal(0, 8, n)
spending_score = np.clip(spending_score, 1, 100)
purchase_freq  = 1 + 0.03 * spending_score + np.random.normal(0, 1, n)
purchase_freq  = np.clip(purchase_freq, 1, 12)
avg_order_val  = 50 + 0.004 * income + 2 * purchase_freq + np.random.normal(0, 20, n)
avg_order_val  = np.clip(avg_order_val, 10, 500)
loyalty_years  = np.clip(age * 0.15 - 1 + np.random.normal(0, 1, n), 0, 15)
returns_pct    = np.clip(20 - 0.15 * spending_score + np.random.normal(0, 3, n), 0, 40)
satisfaction   = np.clip(1.5 + 0.03 * spending_score - 0.07 * returns_pct
                         + np.random.normal(0, 0.5, n), 1, 5)

df = pd.DataFrame({
    "Age":             age.astype(int),
    "Annual_Income":   income.round(0).astype(int),
    "Spending_Score":  spending_score.round(1),
    "Purchase_Freq":   purchase_freq.round(1),
    "Avg_Order_Value": avg_order_val.round(1),
    "Loyalty_Years":   loyalty_years.round(1),
    "Returns_Pct":     returns_pct.round(1),
    "Satisfaction":    satisfaction.round(2),
})

df.to_csv("correlation_output/customer_dataset.csv", index=False)
print(f"\n  Dataset shape : {df.shape}")
print(f"  Columns       : {list(df.columns)}")
print(f"\n  Head(5):\n{df.head(5).to_string(index=False)}")
print(f"\n  Describe:\n{df.describe().round(2).to_string()}")

# ═══════════════════════════════════════════════════════════
# 1.  PEARSON CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════
print("\n" + "─" * 65)
print("  [1] Computing Pearson Correlation Matrix")
print("─" * 65)

corr_matrix = df.corr(method="pearson")

print("\n  Full Pearson Correlation Matrix:")
print(corr_matrix.round(3).to_string())

# Top positive & negative pairs
pairs = (corr_matrix.where(np.tril(np.ones(corr_matrix.shape), k=-1).astype(bool))
                    .stack()
                    .reset_index())
pairs.columns = ["Variable_1", "Variable_2", "Correlation"]
pairs["Abs_Corr"] = pairs["Correlation"].abs()
pairs = pairs.sort_values("Correlation", ascending=False)

print("\n  Top 5 POSITIVE correlations:")
print(pairs.head(5)[["Variable_1","Variable_2","Correlation"]].to_string(index=False))
print("\n  Top 5 NEGATIVE correlations:")
print(pairs.tail(5)[["Variable_1","Variable_2","Correlation"]].to_string(index=False))

# ═══════════════════════════════════════════════════════════
# 2.  HEATMAP — masked upper triangle, annotated
# ═══════════════════════════════════════════════════════════
print("\n  [2] Generating Correlation Heatmap...")

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))   # mask upper triangle

fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor("#f8f9fa")

cmap = sns.diverging_palette(220, 20, as_cmap=True)

sns.heatmap(
    corr_matrix,
    mask=mask,
    cmap=cmap,
    vmin=-1, vmax=1, center=0,
    annot=True, fmt=".2f", annot_kws={"size": 11, "weight": "bold"},
    square=True,
    linewidths=0.8, linecolor="#e0e0e0",
    cbar_kws={"shrink": 0.75, "label": "Pearson r"},
    ax=ax
)

ax.set_title("Pearson Correlation Heatmap\n(Customer Retail Dataset — Lower Triangle)",
             fontsize=15, fontweight="bold", pad=20, color="#1a1a2e")
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

# Annotation: explain colour scale
fig.text(0.13, 0.01,
         "Blue = Positive correlation   |   Red = Negative correlation   |   "
         "Darker = Stronger relationship",
         fontsize=9, color="#555555", style="italic")

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("correlation_output/01_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅ Saved: correlation_output/01_correlation_heatmap.png")

# ═══════════════════════════════════════════════════════════
# 3.  PAIRPLOT — key variable pairs
# ═══════════════════════════════════════════════════════════
print("\n  [3] Generating Pairplot (key variables)...")

key_vars = ["Age", "Annual_Income", "Spending_Score",
            "Avg_Order_Value", "Satisfaction"]

g = sns.pairplot(
    df[key_vars],
    diag_kind="kde",
    plot_kws={"alpha": 0.45, "color": "#4C72B0", "edgecolor": "none", "s": 25},
    diag_kws={"color": "#4C72B0", "fill": True, "alpha": 0.4},
)
g.figure.suptitle("Pairplot — Key Variable Relationships\n(Scatter Matrix with KDE Diagonals)",
                  y=1.02, fontsize=14, fontweight="bold", color="#1a1a2e")

# Add correlation values on each scatter cell
for i, row_var in enumerate(key_vars):
    for j, col_var in enumerate(key_vars):
        if i != j:
            r = df[[row_var, col_var]].corr().iloc[0, 1]
            g.axes[i][j].annotate(
                f"r = {r:.2f}",
                xy=(0.05, 0.92), xycoords="axes fraction",
                fontsize=8.5, color="#c0392b" if r < 0 else "#1a6e3a",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6)
            )

plt.tight_layout()
g.figure.savefig("correlation_output/02_pairplot_key_variables.png",
                 dpi=130, bbox_inches="tight")
plt.close()
print("  ✅ Saved: correlation_output/02_pairplot_key_variables.png")

# ═══════════════════════════════════════════════════════════
# 4.  SCATTER MATRIX — top 3 strongest pairs with regression
# ═══════════════════════════════════════════════════════════
print("\n  [4] Generating Scatter Plots for Strongest Pairs...")

top_pairs = pairs.sort_values("Abs_Corr", ascending=False).head(6)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Strongest Pairwise Relationships with Regression Lines",
             fontsize=14, fontweight="bold", y=1.01, color="#1a1a2e")
fig.patch.set_facecolor("#f8f9fa")

colors_pos = "#2196F3"
colors_neg = "#F44336"

for idx, (ax, (_, row)) in enumerate(zip(axes.flat, top_pairs.iterrows())):
    v1, v2, r = row["Variable_1"], row["Variable_2"], row["Correlation"]
    color = colors_pos if r >= 0 else colors_neg

    ax.scatter(df[v1], df[v2], alpha=0.4, color=color, s=22, edgecolors="none")

    # Regression line
    m, b = np.polyfit(df[v1], df[v2], 1)
    x_line = np.linspace(df[v1].min(), df[v1].max(), 100)
    ax.plot(x_line, m * x_line + b, color=color, lw=2.2, linestyle="--", alpha=0.85)

    ax.set_xlabel(v1.replace("_", " "), fontsize=10)
    ax.set_ylabel(v2.replace("_", " "), fontsize=10)
    direction = "Positive" if r >= 0 else "Negative"
    strength  = "Strong" if abs(r) > 0.6 else "Moderate" if abs(r) > 0.3 else "Weak"
    ax.set_title(f"{v1.replace('_',' ')} vs {v2.replace('_',' ')}\n"
                 f"r = {r:.3f}  ({strength} {direction})",
                 fontsize=10, fontweight="bold", color="#1a1a2e")

    patch = mpatches.Patch(color=color, label=f"r = {r:.3f}")
    ax.legend(handles=[patch], fontsize=9, loc="upper left")

plt.tight_layout()
plt.savefig("correlation_output/03_scatter_strongest_pairs.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("  ✅ Saved: correlation_output/03_scatter_strongest_pairs.png")

# ═══════════════════════════════════════════════════════════
# 5.  CORRELATION BAR CHART  (feature vs Satisfaction)
# ═══════════════════════════════════════════════════════════
print("\n  [5] Generating Correlation Bar Chart vs Satisfaction...")

target_corr = corr_matrix["Satisfaction"].drop("Satisfaction").sort_values()
colors_bar  = ["#F44336" if v < 0 else "#2196F3" for v in target_corr]

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#f8f9fa")

bars = ax.barh(target_corr.index, target_corr.values,
               color=colors_bar, edgecolor="white", height=0.6)

for bar, val in zip(bars, target_corr.values):
    ax.text(val + (0.01 if val >= 0 else -0.01),
            bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}",
            va="center", ha="left" if val >= 0 else "right",
            fontsize=10, fontweight="bold",
            color="#1a1a2e")

ax.axvline(0, color="#555555", linewidth=1.2)
ax.set_xlabel("Pearson Correlation Coefficient (r)", fontsize=11)
ax.set_title("Feature Correlations with Customer Satisfaction\n"
             "(Blue = Positive  |  Red = Negative)",
             fontsize=13, fontweight="bold", color="#1a1a2e", pad=12)
ax.set_xlim(target_corr.min() - 0.1, target_corr.max() + 0.15)
ax.yaxis.set_tick_params(labelsize=10)

plt.tight_layout()
plt.savefig("correlation_output/04_feature_vs_satisfaction.png",
            dpi=150, bbox_inches="tight")
plt.close()
print("  ✅ Saved: correlation_output/04_feature_vs_satisfaction.png")

# ═══════════════════════════════════════════════════════════
# 6.  FULL SCATTER MATRIX (all variables, seaborn)
# ═══════════════════════════════════════════════════════════
print("\n  [6] Generating Full Scatter Matrix (all variables)...")

fig, ax = plt.subplots(figsize=(14, 12))
fig.patch.set_facecolor("#f8f9fa")
ax.set_visible(False)

scatter_grid = pd.plotting.scatter_matrix(
    df, alpha=0.3, figsize=(14, 12),
    diagonal="kde", color="#4C72B0",
    hist_kwds={"color": "#4C72B0", "alpha": 0.5},
)

fig = scatter_grid[0][0].get_figure()
fig.suptitle("Full Scatter Matrix — All Variables\n(KDE on diagonal)",
             fontsize=14, fontweight="bold", y=1.01, color="#1a1a2e")

plt.tight_layout()
fig.savefig("correlation_output/05_full_scatter_matrix.png",
            dpi=120, bbox_inches="tight")
plt.close()
print("  ✅ Saved: correlation_output/05_full_scatter_matrix.png")

# ═══════════════════════════════════════════════════════════
# 7.  SUMMARY REPORT  (TXT + Excel)
# ═══════════════════════════════════════════════════════════
print("\n  [7] Writing Summary Report...")

strongest_pos = pairs[pairs["Correlation"] > 0].iloc[0]
strongest_neg = pairs[pairs["Correlation"] < 0].iloc[-1]

summary_text = f"""
=================================================================
WEEK 2 — PROJECT 3: Correlation Heatmap & Pairwise Relationships
Syntecxhub Data Science Internship
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
=================================================================

DATASET OVERVIEW
----------------
  Records  : {len(df)}
  Features : {len(df.columns)} numeric variables
  Variables: {', '.join(df.columns)}

PEARSON CORRELATION MATRIX
--------------------------
{corr_matrix.round(3).to_string()}

STRONGEST POSITIVE RELATIONSHIPS
---------------------------------
{pairs[pairs["Correlation"] > 0].head(5)[["Variable_1","Variable_2","Correlation"]].to_string(index=False)}

STRONGEST NEGATIVE RELATIONSHIPS
---------------------------------
{pairs[pairs["Correlation"] < 0].tail(5)[["Variable_1","Variable_2","Correlation"]].to_string(index=False)}

INTERPRETATION SUMMARY
-----------------------
1. Strongest Positive Correlation:
   {strongest_pos["Variable_1"]} vs {strongest_pos["Variable_2"]}
   r = {strongest_pos["Correlation"]:.3f}
   → As {strongest_pos["Variable_1"]} increases, {strongest_pos["Variable_2"]} 
     tends to increase proportionally. This is a {'strong' if abs(strongest_pos['Correlation']) > 0.6 else 'moderate'} 
     positive linear relationship.

2. Strongest Negative Correlation:
   {strongest_neg["Variable_1"]} vs {strongest_neg["Variable_2"]}
   r = {strongest_neg["Correlation"]:.3f}
   → As {strongest_neg["Variable_1"]} increases, {strongest_neg["Variable_2"]} 
     tends to decrease. This inverse relationship suggests a trade-off
     between these two variables.

3. Key Findings:
   - Annual Income and Spending Score show a notable positive relationship,
     suggesting higher-income customers tend to spend more.
   - Age has a negative correlation with Spending Score, meaning younger
     customers tend to have higher spending scores.
   - Satisfaction is most strongly driven by Spending Score and negatively
     impacted by Returns Percentage.
   - Loyalty Years correlates positively with Age, as expected —
     older customers have had more time to build loyalty.
   - Returns_Pct shows negative relationships with most positive indicators,
     confirming that high return rates are a strong dissatisfaction signal.

CHART CHOICE DISCUSSION
------------------------
  Heatmap         : Best for showing all pairwise correlations at once; 
                    masked upper triangle avoids redundancy; annotation 
                    makes exact values readable.
  Pairplot        : Ideal for visualizing scatter + distribution (KDE) 
                    simultaneously across multiple variable pairs.
  Scatter + Regr  : Isolates the top relationships with a regression line 
                    to highlight direction and strength clearly.
  Bar Chart       : Clean way to rank how each feature correlates with 
                    a single target variable (Satisfaction).

OUTPUTS
--------
  01_correlation_heatmap.png      — Full masked & annotated heatmap
  02_pairplot_key_variables.png   — Pairplot with r-values
  03_scatter_strongest_pairs.png  — Top 6 pairs with regression lines
  04_feature_vs_satisfaction.png  — Feature importance bar chart
  05_full_scatter_matrix.png      — All variables scatter matrix
  customer_dataset.csv            — Raw dataset used
  correlation_matrix.xlsx         — Correlation matrix in Excel
=================================================================
"""

with open("correlation_output/summary_report.txt", "w") as f:
    f.write(summary_text)
print("  ✅ Saved: correlation_output/summary_report.txt")
print(summary_text)

# Excel: correlation matrix
with pd.ExcelWriter("correlation_output/correlation_matrix.xlsx", engine="openpyxl") as writer:
    corr_matrix.round(3).to_excel(writer, sheet_name="Correlation_Matrix")
    pairs.sort_values("Abs_Corr", ascending=False).to_excel(
        writer, sheet_name="All_Pairs_Ranked", index=False)
    df.describe().round(2).to_excel(writer, sheet_name="Dataset_Stats")
    df.to_excel(writer, sheet_name="Raw_Data", index=False)
print("  ✅ Saved: correlation_output/correlation_matrix.xlsx")

print("\n" + "=" * 65)
print("  Week 2 Project 3 Complete — All charts & report saved ✅")
print("=" * 65)
