# Day 45 - Data Visualization Dashboard

## About This Project
This project creates comprehensive sales dashboards using synthetic data with both static and interactive visualizations.

## Features
- Generates synthetic sales and customer data
- Creates static charts using Matplotlib and Seaborn
- Creates interactive dashboards using Plotly
- Includes correlation analysis
- Shows distribution patterns

## Visualizations Generated

### Static Charts (PNG)
1. Monthly Sales Trend
2. Sales Distribution by Region (Pie Chart)
3. Top 10 Products by Revenue
4. Price vs Quantity Scatter Plot
5. Correlation Heatmap
6. Distribution Charts

### Interactive Dashboard (HTML)
- Monthly sales trend with line chart
- Category distribution with pie chart
- Regional performance with bar chart
- Product performance comparison

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Check outputs
- Static charts: output/ folder (PNG files)
- Interactive dashboard: output/interactive_dashboard.html
- Raw data: data/ folder (CSV files)

## Output Files
- static_dashboard.png - Static dashboard with 4 subplots
- interactive_dashboard.html - Interactive Plotly dashboard
- correlation_heatmap.png - Correlation matrix
- distribution_charts.png - Sales distribution visualizations
- sales_data.csv - Generated sales data
- customer_data.csv - Generated customer data

## Libraries Used
- pandas - Data manipulation
- numpy - Numerical operations
- matplotlib - Static visualizations
- seaborn - Statistical visualizations
- plotly - Interactive visualizations

## Learning Objectives
- Creating dashboards with multiple chart types
- Static vs interactive visualization techniques
- Data summarization and aggregation
- Correlation analysis
- Professional data presentation
