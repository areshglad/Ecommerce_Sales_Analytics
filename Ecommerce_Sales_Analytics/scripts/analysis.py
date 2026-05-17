"""
Complete E-commerce Sales Analytics project.

This script generates a realistic synthetic dataset, performs cleaning and
validation, creates business-focused EDA visuals, and writes a markdown report.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CHART_DIR = PROJECT_ROOT / "visuals" / "charts"
REPORT_DIR = PROJECT_ROOT / "reports"
DATASET_PATH = DATA_DIR / "dataset.csv"
REPORT_PATH = REPORT_DIR / "business_report.md"

RANDOM_SEED = 42
ROW_COUNT = 10_000


def ensure_directories() -> None:
    """Create required output directories."""
    for directory in [DATA_DIR, CHART_DIR, REPORT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def weighted_dates(rng: np.random.Generator, n_rows: int) -> pd.DatetimeIndex:
    """Generate order dates with realistic monthly seasonality."""
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    month_weights = {
        1: 0.85,
        2: 0.80,
        3: 0.95,
        4: 1.00,
        5: 1.05,
        6: 1.10,
        7: 1.00,
        8: 1.05,
        9: 1.15,
        10: 1.25,
        11: 1.65,
        12: 1.55,
    }
    weights = np.array([month_weights[date.month] for date in dates], dtype=float)
    weights = weights / weights.sum()
    return pd.DatetimeIndex(rng.choice(dates, size=n_rows, replace=True, p=weights)).sort_values()


def generate_dataset(path: Path = DATASET_PATH, n_rows: int = ROW_COUNT) -> pd.DataFrame:
    """Create a reproducible synthetic e-commerce sales dataset."""
    rng = np.random.default_rng(RANDOM_SEED)

    categories = np.array(["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports", "Books"])
    category_probs = np.array([0.22, 0.24, 0.18, 0.14, 0.12, 0.10])
    category_base_price = {
        "Electronics": 210,
        "Fashion": 55,
        "Home & Kitchen": 85,
        "Beauty": 38,
        "Sports": 75,
        "Books": 24,
    }
    category_quantity_lambda = {
        "Electronics": 1.2,
        "Fashion": 2.0,
        "Home & Kitchen": 1.6,
        "Beauty": 2.3,
        "Sports": 1.7,
        "Books": 2.6,
    }

    order_dates = weighted_dates(rng, n_rows)
    product_category = rng.choice(categories, size=n_rows, p=category_probs)
    customer_segment = rng.choice(
        ["New", "Returning", "Loyal", "VIP"],
        size=n_rows,
        p=[0.34, 0.37, 0.22, 0.07],
    )
    region = rng.choice(
        ["North", "South", "East", "West", "Central"],
        size=n_rows,
        p=[0.24, 0.21, 0.20, 0.23, 0.12],
    ).astype(object)
    sales_channel = rng.choice(
        ["Website", "Mobile App", "Marketplace", "Social Commerce"],
        size=n_rows,
        p=[0.42, 0.34, 0.18, 0.06],
    ).astype(object)
    payment_method = rng.choice(
        ["Credit Card", "Debit Card", "Digital Wallet", "Cash on Delivery", "Buy Now Pay Later"],
        size=n_rows,
        p=[0.31, 0.20, 0.29, 0.14, 0.06],
    ).astype(object)

    quantity = np.array(
        [max(1, rng.poisson(category_quantity_lambda[cat])) for cat in product_category],
        dtype=int,
    )
    quantity_outliers = rng.choice(n_rows, size=int(n_rows * 0.007), replace=False)
    quantity[quantity_outliers] = rng.integers(18, 55, size=len(quantity_outliers))

    base_prices = np.array([category_base_price[cat] for cat in product_category], dtype=float)
    unit_price = rng.lognormal(mean=np.log(base_prices), sigma=0.35)
    price_outliers = rng.choice(n_rows, size=int(n_rows * 0.010), replace=False)
    unit_price[price_outliers] *= rng.uniform(4.0, 8.5, size=len(price_outliers))
    unit_price = np.round(unit_price, 2)

    discount_pct = rng.beta(1.6, 9.5, size=n_rows) * 0.45
    campaign_mask = pd.Series(order_dates).dt.month.isin([7, 11, 12]).to_numpy()
    discount_pct[campaign_mask] += rng.uniform(0.03, 0.18, size=campaign_mask.sum())
    discount_pct = np.clip(discount_pct, 0, 0.65)

    shipping_fee = rng.gamma(shape=2.0, scale=3.5, size=n_rows) + 2
    free_shipping = (customer_segment == "VIP") | (unit_price * quantity > 250)
    shipping_fee[free_shipping] *= rng.uniform(0.0, 0.35, size=free_shipping.sum())
    shipping_fee = np.round(shipping_fee, 2)

    delivery_days = rng.poisson(lam=3.2, size=n_rows) + 1
    slow_delivery_outliers = rng.choice(n_rows, size=int(n_rows * 0.012), replace=False)
    delivery_days[slow_delivery_outliers] = rng.integers(12, 27, size=len(slow_delivery_outliers))

    return_probability = (
        0.035
        + 0.020 * (product_category == "Fashion")
        + 0.018 * (product_category == "Electronics")
        + 0.025 * (delivery_days > 7)
        + 0.015 * (discount_pct > 0.30)
        + 0.012 * (sales_channel == "Marketplace")
    )
    returned = rng.binomial(1, np.clip(return_probability, 0.01, 0.18))

    customer_rating = (
        4.55
        - 0.055 * delivery_days
        - 0.75 * returned
        + rng.normal(0, 0.38, size=n_rows)
    )
    customer_rating = np.round(np.clip(customer_rating, 1.0, 5.0), 1)

    df = pd.DataFrame(
        {
            "order_id": [f"ORD-{100000 + idx}" for idx in range(n_rows)],
            "customer_id": [f"CUST-{rng.integers(10000, 14999)}" for _ in range(n_rows)],
            "order_date": order_dates.strftime("%Y-%m-%d"),
            "region": region,
            "customer_segment": customer_segment,
            "product_category": product_category,
            "sales_channel": sales_channel,
            "payment_method": payment_method,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": np.round(discount_pct, 3),
            "shipping_fee": shipping_fee,
            "delivery_days": delivery_days,
            "customer_rating": customer_rating,
            "returned": returned,
        }
    )

    missing_config = {
        "region": 0.020,
        "payment_method": 0.025,
        "sales_channel": 0.010,
        "discount_pct": 0.040,
        "customer_rating": 0.060,
    }
    for column, missing_rate in missing_config.items():
        mask = rng.random(n_rows) < missing_rate
        df.loc[mask, column] = np.nan

    duplicate_source = rng.choice(np.arange(0, n_rows - 50), size=20, replace=False)
    duplicate_target = np.arange(n_rows - 20, n_rows)
    df.iloc[duplicate_target] = df.iloc[duplicate_source].to_numpy()

    df = df.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def cap_outliers_iqr(df: pd.DataFrame, columns: Iterable[str]) -> Tuple[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """Cap numeric outliers using IQR boundaries and return summary metadata."""
    cleaned = df.copy()
    outlier_summary: Dict[str, Dict[str, float]] = {}
    for column in columns:
        q1 = cleaned[column].quantile(0.25)
        q3 = cleaned[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_mask = (cleaned[column] < lower_bound) | (cleaned[column] > upper_bound)
        outlier_summary[column] = {
            "count": int(outlier_mask.sum()),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
        }
        cleaned[column] = cleaned[column].clip(lower=lower_bound, upper=upper_bound)
    return cleaned, outlier_summary


def clean_data(raw_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Clean, validate, and enrich the dataset for analysis."""
    df = raw_df.copy()
    diagnostics: Dict[str, object] = {
        "raw_rows": len(df),
        "raw_columns": len(df.columns),
        "missing_before": df.isna().sum().to_dict(),
        "duplicate_rows_before": int(df.duplicated().sum()),
    }

    df = df.drop_duplicates().reset_index(drop=True)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    categorical_columns = ["region", "sales_channel", "payment_method"]
    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode(dropna=True)[0])

    df["discount_pct"] = df["discount_pct"].fillna(0)
    df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())

    numeric_columns = [
        "quantity",
        "unit_price",
        "discount_pct",
        "shipping_fee",
        "delivery_days",
        "customer_rating",
        "returned",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["order_id", "customer_id", "order_date", "product_category"])
    df["quantity"] = df["quantity"].round().astype(int)
    df["delivery_days"] = df["delivery_days"].round().astype(int)
    df["returned"] = df["returned"].round().astype(int)
    df["total_amount"] = np.round(
        (df["unit_price"] * df["quantity"] * (1 - df["discount_pct"])) + df["shipping_fee"],
        2,
    )

    df, outlier_summary = cap_outliers_iqr(
        df,
        ["quantity", "unit_price", "shipping_fee", "delivery_days", "total_amount"],
    )
    df["quantity"] = df["quantity"].round().clip(lower=1).astype(int)
    df["delivery_days"] = df["delivery_days"].round().clip(lower=1).astype(int)
    df["discount_pct"] = df["discount_pct"].clip(0, 0.80)
    df["customer_rating"] = df["customer_rating"].clip(1, 5)
    df["total_amount"] = np.round(
        (df["unit_price"] * df["quantity"] * (1 - df["discount_pct"])) + df["shipping_fee"],
        2,
    )
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["year"] = df["order_date"].dt.year

    validation_checks = {
        "no_missing_values": bool(df.isna().sum().sum() == 0),
        "positive_quantity": bool((df["quantity"] > 0).all()),
        "positive_prices": bool((df["unit_price"] > 0).all()),
        "valid_discounts": bool(df["discount_pct"].between(0, 0.80).all()),
        "valid_ratings": bool(df["customer_rating"].between(1, 5).all()),
        "valid_return_flag": bool(df["returned"].isin([0, 1]).all()),
    }

    diagnostics.update(
        {
            "clean_rows": len(df),
            "rows_removed": diagnostics["raw_rows"] - len(df),
            "missing_after": df.isna().sum().to_dict(),
            "outlier_summary": outlier_summary,
            "validation_checks": validation_checks,
        }
    )
    return df, diagnostics


def save_chart(filename: str) -> None:
    """Save the active matplotlib figure."""
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close()


def create_visuals(df: pd.DataFrame) -> Dict[str, Path]:
    """Create and save business-focused EDA charts."""
    sns.set_theme(style="whitegrid", palette="Set2")
    chart_paths: Dict[str, Path] = {}

    monthly = df.groupby("month").agg(revenue=("total_amount", "sum"), orders=("order_id", "count")).reset_index()

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o", linewidth=2.5)
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    save_chart("01_monthly_revenue_trend.png")
    chart_paths["Monthly revenue trend"] = CHART_DIR / "01_monthly_revenue_trend.png"

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="month", y="orders", marker="o", color="#4C78A8", linewidth=2.5)
    plt.xticks(rotation=45)
    plt.title("Monthly Order Volume Trend")
    plt.xlabel("Month")
    plt.ylabel("Orders")
    save_chart("02_monthly_order_volume.png")
    chart_paths["Monthly order volume"] = CHART_DIR / "02_monthly_order_volume.png"

    category_revenue = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=category_revenue.values, y=category_revenue.index, color="#72B7B2")
    plt.title("Revenue by Product Category")
    plt.xlabel("Revenue")
    plt.ylabel("Product Category")
    save_chart("03_revenue_by_category.png")
    chart_paths["Revenue by category"] = CHART_DIR / "03_revenue_by_category.png"

    region_revenue = df.groupby("region")["total_amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=region_revenue.index, y=region_revenue.values, color="#F58518")
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    save_chart("04_revenue_by_region.png")
    chart_paths["Revenue by region"] = CHART_DIR / "04_revenue_by_region.png"

    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, y="product_category", order=df["product_category"].value_counts().index, color="#54A24B")
    plt.title("Order Count by Product Category")
    plt.xlabel("Orders")
    plt.ylabel("Product Category")
    save_chart("05_orders_by_category.png")
    chart_paths["Orders by category"] = CHART_DIR / "05_orders_by_category.png"

    plt.figure(figsize=(10, 5))
    sns.histplot(df["unit_price"], bins=45, kde=True, color="#B279A2")
    plt.title("Distribution of Unit Price After Outlier Treatment")
    plt.xlabel("Unit Price")
    plt.ylabel("Frequency")
    save_chart("06_unit_price_distribution.png")
    chart_paths["Unit price distribution"] = CHART_DIR / "06_unit_price_distribution.png"

    plt.figure(figsize=(11, 5))
    sns.boxplot(data=df, x="product_category", y="quantity")
    plt.title("Quantity Distribution by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Quantity")
    plt.xticks(rotation=25)
    save_chart("07_quantity_by_category_boxplot.png")
    chart_paths["Quantity by category"] = CHART_DIR / "07_quantity_by_category_boxplot.png"

    sample_df = df.sample(min(2500, len(df)), random_state=RANDOM_SEED)
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=sample_df,
        x="discount_pct",
        y="total_amount",
        hue="returned",
        alpha=0.45,
        palette={0: "#4C78A8", 1: "#E45756"},
    )
    plt.title("Discount vs Order Value by Return Status")
    plt.xlabel("Discount Percentage")
    plt.ylabel("Total Amount")
    save_chart("08_discount_vs_total_amount.png")
    chart_paths["Discount vs order value"] = CHART_DIR / "08_discount_vs_total_amount.png"

    corr_columns = ["quantity", "unit_price", "discount_pct", "shipping_fee", "delivery_days", "customer_rating", "returned", "total_amount"]
    plt.figure(figsize=(9, 7))
    sns.heatmap(df[corr_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap")
    save_chart("09_correlation_heatmap.png")
    chart_paths["Correlation heatmap"] = CHART_DIR / "09_correlation_heatmap.png"

    return_rate = df.groupby("product_category")["returned"].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(10, 5))
    sns.barplot(x=return_rate.values, y=return_rate.index, color="#E45756")
    plt.title("Return Rate by Product Category")
    plt.xlabel("Return Rate (%)")
    plt.ylabel("Product Category")
    save_chart("10_return_rate_by_category.png")
    chart_paths["Return rate by category"] = CHART_DIR / "10_return_rate_by_category.png"

    channel_rating = df.groupby("sales_channel")["customer_rating"].mean().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=channel_rating.index, y=channel_rating.values, color="#59A14F")
    plt.title("Average Customer Rating by Sales Channel")
    plt.xlabel("Sales Channel")
    plt.ylabel("Average Rating")
    plt.ylim(1, 5)
    plt.xticks(rotation=15)
    save_chart("11_rating_by_sales_channel.png")
    chart_paths["Rating by channel"] = CHART_DIR / "11_rating_by_sales_channel.png"

    plt.figure(figsize=(9, 5))
    sns.histplot(df["delivery_days"], bins=range(1, int(df["delivery_days"].max()) + 2), color="#9D755D")
    plt.title("Delivery Days Distribution")
    plt.xlabel("Delivery Days")
    plt.ylabel("Orders")
    save_chart("12_delivery_days_distribution.png")
    chart_paths["Delivery days distribution"] = CHART_DIR / "12_delivery_days_distribution.png"

    segment_revenue = df.groupby("customer_segment")["total_amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    sns.barplot(x=segment_revenue.index, y=segment_revenue.values, color="#EDC948")
    plt.title("Revenue by Customer Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Revenue")
    save_chart("13_revenue_by_customer_segment.png")
    chart_paths["Revenue by customer segment"] = CHART_DIR / "13_revenue_by_customer_segment.png"

    return chart_paths


def build_insights(df: pd.DataFrame, diagnostics: Dict[str, object]) -> Dict[str, object]:
    """Compute high-level business metrics and narrative inputs."""
    total_revenue = df["total_amount"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = df["total_amount"].mean()
    return_rate = df["returned"].mean() * 100
    avg_rating = df["customer_rating"].mean()
    avg_delivery = df["delivery_days"].mean()

    category_revenue = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)
    region_revenue = df.groupby("region")["total_amount"].sum().sort_values(ascending=False)
    channel_revenue = df.groupby("sales_channel")["total_amount"].sum().sort_values(ascending=False)
    segment_revenue = df.groupby("customer_segment")["total_amount"].sum().sort_values(ascending=False)
    monthly_revenue = df.groupby("month")["total_amount"].sum().sort_values(ascending=False)
    return_by_category = (df.groupby("product_category")["returned"].mean() * 100).sort_values(ascending=False)
    rating_by_channel = df.groupby("sales_channel")["customer_rating"].mean().sort_values(ascending=False)

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "return_rate": return_rate,
        "avg_rating": avg_rating,
        "avg_delivery": avg_delivery,
        "top_category": category_revenue.index[0],
        "top_category_revenue": category_revenue.iloc[0],
        "top_region": region_revenue.index[0],
        "top_region_revenue": region_revenue.iloc[0],
        "top_channel": channel_revenue.index[0],
        "top_channel_revenue": channel_revenue.iloc[0],
        "top_segment": segment_revenue.index[0],
        "top_segment_revenue": segment_revenue.iloc[0],
        "best_month": monthly_revenue.index[0],
        "best_month_revenue": monthly_revenue.iloc[0],
        "highest_return_category": return_by_category.index[0],
        "highest_return_rate": return_by_category.iloc[0],
        "best_rating_channel": rating_by_channel.index[0],
        "best_rating": rating_by_channel.iloc[0],
        "diagnostics": diagnostics,
    }


def currency(value: float) -> str:
    """Format currency values for reports."""
    return f"${value:,.2f}"


def write_report(df: pd.DataFrame, insights: Dict[str, object], chart_paths: Dict[str, Path]) -> None:
    """Write the business report in markdown."""
    diagnostics = insights["diagnostics"]
    missing_before = pd.Series(diagnostics["missing_before"])
    missing_summary = missing_before[missing_before > 0].sort_values(ascending=False)
    outlier_summary = diagnostics["outlier_summary"]
    validation_checks = diagnostics["validation_checks"]

    report = f"""# E-commerce Sales Analytics Business Report

## Objective

The objective of this project is to analyze two years of synthetic e-commerce order activity and identify practical opportunities to improve revenue, customer experience, return management, and channel performance. The analysis is designed to mirror the kind of business questions a retail analytics team would answer for leadership.

## Dataset Overview

- Rows generated: {diagnostics['raw_rows']:,}
- Rows after cleaning: {diagnostics['clean_rows']:,}
- Columns in raw dataset: {diagnostics['raw_columns']}
- Time period: {df['order_date'].min().date()} to {df['order_date'].max().date()}
- Total clean revenue: {currency(insights['total_revenue'])}
- Total clean orders: {insights['total_orders']:,}
- Average order value: {currency(insights['avg_order_value'])}
- Overall return rate: {insights['return_rate']:.2f}%
- Average customer rating: {insights['avg_rating']:.2f} out of 5
- Average delivery time: {insights['avg_delivery']:.2f} days

The dataset contains order identifiers, customers, order dates, regions, customer segments, product categories, sales channels, payment methods, quantities, prices, discounts, shipping fees, delivery days, ratings, return flags, and order value.


## Cleaning and Validation Summary

Missing values before treatment:

{missing_summary.rename("Missing Count").to_frame().to_markdown()}

Duplicate rows before cleaning: {diagnostics['duplicate_rows_before']:,}

Outlier detection summary:

| Column | Outliers Detected | Lower Bound | Upper Bound |
|---|---:|---:|---:|
"""

    for column, values in outlier_summary.items():
        report += f"| {column} | {values['count']:,} | {values['lower_bound']:.2f} | {values['upper_bound']:.2f} |\n"

    report += "\nValidation checks after cleaning:\n\n| Check | Result |\n|---|---|\n"
    for check, result in validation_checks.items():
        report += f"| {check.replace('_', ' ').title()} | {'Passed' if result else 'Failed'} |\n"

    report += f"""

## Key Findings

### Revenue Performance

- The business generated {currency(insights['total_revenue'])} in clean revenue across {insights['total_orders']:,} orders.
- The strongest revenue month was {insights['best_month']} with {currency(insights['best_month_revenue'])}, showing the impact of seasonal demand and campaign periods.
- {insights['top_category']} was the leading product category, contributing {currency(insights['top_category_revenue'])}. This indicates that category-level merchandising and inventory planning should be treated as a high-priority revenue lever.

### Product and Category Insights

- {insights['top_category']} leads revenue, while lower-priced categories still contribute order volume and customer engagement.
- {insights['highest_return_category']} has the highest return rate at {insights['highest_return_rate']:.2f}%. This suggests a need to review product descriptions, sizing or specifications, quality checks, and post-purchase expectations.
- Quantity patterns differ by category, which supports separate inventory policies instead of a single replenishment rule across all products.

### Customer and Channel Insights

- {insights['top_segment']} customers generated the highest segment revenue at {currency(insights['top_segment_revenue'])}. This segment should be prioritized for retention, loyalty offers, and personalized recommendations.
- {insights['top_channel']} is the strongest revenue channel with {currency(insights['top_channel_revenue'])}.
- {insights['best_rating_channel']} has the best average rating at {insights['best_rating']:.2f}, indicating a stronger customer experience in that purchase path.

### Regional Insights

- {insights['top_region']} is the top revenue region with {currency(insights['top_region_revenue'])}.
- Regional revenue differences suggest opportunities for localized campaigns, shipping optimization, and inventory positioning.

### Returns and Customer Experience

- The overall return rate is {insights['return_rate']:.2f}%.
- Higher delivery times and returned orders are associated with lower customer ratings, which makes fulfillment speed a direct customer experience metric.
- Discount-heavy orders should be monitored carefully because promotions can increase volume while also attracting lower-intent purchases.

## Visual Outputs

The analysis generated the following charts in `visuals/charts/`:

"""
    for name, path in chart_paths.items():
        report += f"- {name}: `{path.relative_to(PROJECT_ROOT)}`\n"

    report += """

## Recommendations

1. Protect the top revenue category with stronger inventory forecasting, campaign planning, and product availability monitoring.
2. Investigate the highest-return category by reviewing product detail pages, sizing/specification clarity, supplier quality, and customer complaints.
3. Build segment-specific retention campaigns for the highest-value customer segment instead of applying the same promotion strategy to all customers.
4. Use regional performance differences to plan localized promotions and place inventory closer to high-revenue regions.
5. Monitor discount depth against return rate and order value to ensure campaigns increase profitable demand rather than low-quality transactions.
6. Improve delivery reliability for slower orders because fulfillment delays are connected to weaker ratings and higher return risk.
7. Track sales channel performance separately; the strongest channel should receive conversion optimization investment, while lower-rated channels need user experience improvements.

## Conclusion

This analysis shows that revenue growth is influenced by a combination of product category mix, seasonal demand, channel performance, customer segment behavior, delivery experience, and return management. The project demonstrates a complete analytics workflow from synthetic data generation through cleaning, exploratory analysis, visualization, insight development, and business reporting.
"""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")


def run_pipeline() -> None:
    """Execute the full analytics workflow."""
    ensure_directories()
    raw_df = generate_dataset(DATASET_PATH, ROW_COUNT)
    cleaned_df, diagnostics = clean_data(raw_df)
    chart_paths = create_visuals(cleaned_df)
    insights = build_insights(cleaned_df, diagnostics)
    write_report(cleaned_df, insights, chart_paths)

    print("E-commerce Sales Analytics pipeline completed.")
    print(f"Dataset saved to: {DATASET_PATH}")
    print(f"Charts saved to: {CHART_DIR}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Raw rows: {diagnostics['raw_rows']:,}")
    print(f"Clean rows: {diagnostics['clean_rows']:,}")


if __name__ == "__main__":
    run_pipeline()
