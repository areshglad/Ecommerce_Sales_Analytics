# E-commerce Sales Analytics Business Report

## Objective

The objective of this project is to analyze two years of synthetic e-commerce order activity and identify practical opportunities to improve revenue, customer experience, return management, and channel performance. The analysis is designed to mirror the kind of business questions a retail analytics team would answer for leadership.

## Dataset Overview

- Rows generated: 10,000
- Rows after cleaning: 9,980
- Columns in raw dataset: 15
- Time period: 2024-01-01 to 2025-12-31
- Total clean revenue: $1,604,097.06
- Total clean orders: 9,980
- Average order value: $160.73
- Overall return rate: 4.38%
- Average customer rating: 4.27 out of 5
- Average delivery time: 4.21 days

The dataset contains order identifiers, customers, order dates, regions, customer segments, product categories, sales channels, payment methods, quantities, prices, discounts, shipping fees, delivery days, ratings, return flags, and order value.

## Methodology

1. Generated a realistic synthetic e-commerce dataset with 10,000 rows, business categories, seasonal demand, pricing variation, missing values, duplicate rows, and outliers.
2. Checked duplicate records and removed exact duplicates.
3. Converted date and numeric columns to proper data types.
4. Treated missing categorical values with mode imputation.
5. Treated missing discounts as 0 because a missing discount in transactional data usually indicates no recorded promotion.
6. Treated missing customer ratings with median imputation to avoid exaggerating satisfaction or dissatisfaction.
7. Detected numeric outliers with the IQR method and capped extreme values for stable business analysis.
8. Recalculated order value after cleaning price, quantity, shipping, and discount fields.
9. Validated the cleaned dataset for missing values, positive quantities, valid discounts, valid ratings, and binary return flags.
10. Created exploratory charts for trends, categories, distributions, correlations, customer segments, channels, delivery, and returns.

## Cleaning and Validation Summary

Missing values before treatment:

|                 |   Missing Count |
|:----------------|----------------:|
| customer_rating |             580 |
| discount_pct    |             426 |
| region          |             230 |
| payment_method  |             226 |
| sales_channel   |             114 |

Duplicate rows before cleaning: 20

Outlier detection summary:

| Column | Outliers Detected | Lower Bound | Upper Bound |
|---|---:|---:|---:|
| quantity | 115 | -2.00 | 6.00 |
| unit_price | 786 | -76.89 | 242.31 |
| shipping_fee | 216 | -7.57 | 20.54 |
| delivery_days | 288 | 0.00 | 8.00 |
| total_amount | 639 | -138.31 | 420.49 |

Validation checks after cleaning:

| Check | Result |
|---|---|
| No Missing Values | Passed |
| Positive Quantity | Passed |
| Positive Prices | Passed |
| Valid Discounts | Passed |
| Valid Ratings | Passed |
| Valid Return Flag | Passed |


## Key Findings

### Revenue Performance

- The business generated $1,604,097.06 in clean revenue across 9,980 orders.
- The strongest revenue month was 2024-11 with $85,106.47, showing the impact of seasonal demand and campaign periods.
- Electronics was the leading product category, contributing $615,869.70. This indicates that category-level merchandising and inventory planning should be treated as a high-priority revenue lever.

### Product and Category Insights

- Electronics leads revenue, while lower-priced categories still contribute order volume and customer engagement.
- Fashion has the highest return rate at 5.50%. This suggests a need to review product descriptions, sizing or specifications, quality checks, and post-purchase expectations.
- Quantity patterns differ by category, which supports separate inventory policies instead of a single replenishment rule across all products.

### Customer and Channel Insights

- Returning customers generated the highest segment revenue at $589,505.63. This segment should be prioritized for retention, loyalty offers, and personalized recommendations.
- Website is the strongest revenue channel with $696,302.47.
- Marketplace has the best average rating at 4.28, indicating a stronger customer experience in that purchase path.

### Regional Insights

- North is the top revenue region with $417,723.08.
- Regional revenue differences suggest opportunities for localized campaigns, shipping optimization, and inventory positioning.

### Returns and Customer Experience

- The overall return rate is 4.38%.
- Higher delivery times and returned orders are associated with lower customer ratings, which makes fulfillment speed a direct customer experience metric.
- Discount-heavy orders should be monitored carefully because promotions can increase volume while also attracting lower-intent purchases.

## Visual Outputs

The analysis generated the following charts in `visuals/charts/`:

- Monthly revenue trend: `visuals\charts\01_monthly_revenue_trend.png`
- Monthly order volume: `visuals\charts\02_monthly_order_volume.png`
- Revenue by category: `visuals\charts\03_revenue_by_category.png`
- Revenue by region: `visuals\charts\04_revenue_by_region.png`
- Orders by category: `visuals\charts\05_orders_by_category.png`
- Unit price distribution: `visuals\charts\06_unit_price_distribution.png`
- Quantity by category: `visuals\charts\07_quantity_by_category_boxplot.png`
- Discount vs order value: `visuals\charts\08_discount_vs_total_amount.png`
- Correlation heatmap: `visuals\charts\09_correlation_heatmap.png`
- Return rate by category: `visuals\charts\10_return_rate_by_category.png`
- Rating by channel: `visuals\charts\11_rating_by_sales_channel.png`
- Delivery days distribution: `visuals\charts\12_delivery_days_distribution.png`
- Revenue by customer segment: `visuals\charts\13_revenue_by_customer_segment.png`


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
