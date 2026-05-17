# E-commerce Sales Analytics

## Project Overview

This is a complete, GitHub-ready data analytics portfolio project that analyzes synthetic e-commerce order data. The project simulates a realistic business environment where analysts need to understand revenue performance, customer behavior, product category trends, returns, delivery experience, and sales channel effectiveness.

The dataset contains exactly 10,000 raw rows and includes missing values, duplicates, outliers, seasonal demand patterns, categorical variables, numerical variables, and a date column.

## Problem Statement

An e-commerce company wants to improve revenue growth, reduce returns, and strengthen customer experience. The business needs a clear analysis of sales trends, customer segments, product categories, regional performance, discount behavior, delivery speed, and return patterns.

This project answers questions such as:

- Which product categories and customer segments drive the most revenue?
- How does revenue change over time?
- Which regions and channels perform best?
- Which categories have higher return risk?
- How are delivery time, rating, discounting, and order value related?
- What actions should the business take based on the data?

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Markdown

## Folder Structure

```text
Ecommerce_Sales_Analytics/
|
├── data/
│   └── dataset.csv
├── notebooks/
│   └── complete_analysis.ipynb
├── scripts/
│   └── analysis.py
├── visuals/
│   └── charts/
├── reports/
│   └── business_report.md
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Dataset Description

The synthetic dataset represents e-commerce orders from 2024 through 2025.

Raw dataset fields include:

- `order_id`: Unique order identifier
- `customer_id`: Customer identifier
- `order_date`: Date of purchase
- `region`: Customer region
- `customer_segment`: Customer type such as New, Returning, Loyal, or VIP
- `product_category`: Product category purchased
- `sales_channel`: Purchase channel
- `payment_method`: Payment option used
- `quantity`: Number of units ordered
- `unit_price`: Unit selling price
- `discount_pct`: Discount applied to the order
- `shipping_fee`: Shipping charge
- `delivery_days`: Delivery duration
- `customer_rating`: Customer satisfaction rating
- `returned`: Return flag

Calculated analysis field:

- `total_amount`: Final order value calculated from price, quantity, discount, and shipping fields

## Workflow

1. Generate a realistic 10,000-row synthetic dataset.
2. Inject missing values, duplicates, and outliers to simulate real-world data quality issues.
3. Clean the dataset using imputation, duplicate removal, data type conversion, and IQR-based outlier treatment.
4. Validate the cleaned dataset for business logic and data quality.
5. Perform exploratory data analysis.
6. Create and save visualizations.
7. Develop business insights and recommendations.
8. Write a professional business report.

## Installation

Clone or download the project folder, then install the required Python libraries:

```bash
pip install -r requirements.txt
```

## How to Run

Run the full pipeline from the project root:

```bash
python scripts/analysis.py
```

Open the notebook for a step-by-step explanation:

```bash
jupyter notebook notebooks/complete_analysis.ipynb
```

## Sample Outputs

Charts are saved in `visuals/charts/`.

Generated visuals include:

- Monthly revenue trend
- Monthly order volume trend
- Revenue by product category
- Revenue by region
- Order count by category
- Unit price distribution
- Quantity distribution by category
- Discount vs order value
- Correlation heatmap
- Return rate by category
- Average rating by sales channel
- Delivery days distribution
- Revenue by customer segment

## Key Insights

- Revenue performance is shaped by seasonality, product mix, and customer segment behavior.
- The highest-revenue category deserves focused inventory and campaign planning.
- Return rates vary by category, which suggests that product information, quality control, and customer expectations should be managed differently by category.
- Delivery speed is connected to satisfaction, making fulfillment performance a customer experience priority.
- Channel-level analysis helps identify where to invest in conversion optimization and where to improve the customer journey.

## Business Recommendations

- Prioritize inventory availability for top revenue categories during seasonal peaks.
- Investigate categories with high return rates and improve product detail pages, sizing guidance, and quality checks.
- Build targeted retention campaigns for high-value customer segments.
- Optimize regional logistics and promotions based on revenue concentration.
- Monitor deep discounting because aggressive promotions can increase order volume without improving customer quality.
- Improve slower delivery paths to protect customer satisfaction and reduce return risk.

## Future Scope

- Add profitability analysis using product cost and margin fields.
- Build a customer lifetime value model.
- Create a return prediction machine learning model.
- Add cohort analysis for customer retention.
- Build an interactive dashboard in Power BI, Tableau, Streamlit, or Plotly Dash.
- Connect the workflow to a database such as PostgreSQL or SQLite.

## Project Status

Complete and ready for GitHub upload.
