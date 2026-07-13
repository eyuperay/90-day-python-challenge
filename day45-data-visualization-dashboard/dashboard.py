"""
Dashboard - Creates visualizations for sales data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


class SalesDashboard:
    """Creates interactive and static visualizations"""
    
    def __init__(self, sales_df: pd.DataFrame, customer_df: pd.DataFrame = None):
        self.sales_df = sales_df
        self.customer_df = customer_df
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_static_charts(self):
        """Generate static matplotlib/seaborn charts"""
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # 1. Monthly Sales Trend
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Sales by month
        self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
        monthly_sales = self.sales_df.groupby(self.sales_df['date'].dt.to_period('M'))['total'].sum()
        
        monthly_sales.plot(kind='bar', ax=axes[0, 0], color='skyblue')
        axes[0, 0].set_title('Monthly Sales Trend')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Total Sales (TRY)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Sales by Region (Pie Chart)
        region_sales = self.sales_df.groupby('region')['total'].sum()
        axes[0, 1].pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Sales Distribution by Region')
        
        # 3. Top Products by Revenue
        product_sales = self.sales_df.groupby('product')['total'].sum().sort_values(ascending=False).head(10)
        product_sales.plot(kind='barh', ax=axes[1, 0], color='lightcoral')
        axes[1, 0].set_title('Top 10 Products by Revenue')
        axes[1, 0].set_xlabel('Total Revenue (TRY)')
        
        # 4. Price vs Quantity Scatter
        axes[1, 1].scatter(self.sales_df['price'], self.sales_df['quantity'], alpha=0.5)
        axes[1, 1].set_title('Price vs Quantity Relationship')
        axes[1, 1].set_xlabel('Price (TRY)')
        axes[1, 1].set_ylabel('Quantity')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/static_dashboard.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Static dashboard saved to {self.output_dir}/static_dashboard.png")
    
    def create_interactive_dashboard(self):
        """Generate interactive Plotly dashboard"""
        
        # Create subplots with different chart types
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Monthly Sales Trend',
                'Sales by Category',
                'Regional Performance',
                'Product Performance'
            ),
            specs=[[{"secondary_y": False}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 1. Monthly sales trend (line chart)
        self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
        monthly_sales = self.sales_df.groupby(self.sales_df['date'].dt.to_period('M'))['total'].sum()
        months = monthly_sales.index.astype(str)
        
        fig.add_trace(
            go.Scatter(x=months, y=monthly_sales.values, mode='lines+markers', name='Monthly Sales'),
            row=1, col=1
        )
        
        # 2. Sales by category (pie)
        category_sales = self.sales_df.groupby('category')['total'].sum()
        fig.add_trace(
            go.Pie(labels=category_sales.index, values=category_sales.values, name='Categories'),
            row=1, col=2
        )
        
        # 3. Regional performance (bar)
        region_sales = self.sales_df.groupby('region')['total'].sum().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(x=region_sales.values, y=region_sales.index, orientation='h', name='Regions'),
            row=2, col=1
        )
        
        # 4. Top products (bar)
        product_sales = self.sales_df.groupby('product')['total'].sum().sort_values(ascending=False).head(8)
        fig.add_trace(
            go.Bar(x=product_sales.index, y=product_sales.values, name='Products'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Interactive Sales Dashboard",
            template="plotly_dark"
        )
        
        # Save as HTML
        fig.write_html(f"{self.output_dir}/interactive_dashboard.html")
        print(f"✓ Interactive dashboard saved to {self.output_dir}/interactive_dashboard.html")
        
        return fig
    
    def create_correlation_heatmap(self):
        """Generate correlation heatmap"""
        # Select numeric columns
        numeric_cols = self.sales_df.select_dtypes(include=['float64', 'int64']).columns
        corr = self.sales_df[numeric_cols].corr()
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Correlation Matrix of Numeric Features')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Correlation heatmap saved to {self.output_dir}/correlation_heatmap.png")
    
    def create_distribution_charts(self):
        """Generate distribution visualizations"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Distribution of sales amounts
        self.sales_df['total'].hist(bins=50, ax=axes[0], color='skyblue', edgecolor='black')
        axes[0].set_title('Distribution of Sales Amounts')
        axes[0].set_xlabel('Total Amount (TRY)')
        axes[0].set_ylabel('Frequency')
        
        # Boxplot by category
        self.sales_df.boxplot(column='total', by='category', ax=axes[1])
        axes[1].set_title('Sales Distribution by Category')
        axes[1].set_xlabel('Category')
        axes[1].set_ylabel('Total Amount (TRY)')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.suptitle('')  # Remove default title
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/distribution_charts.png", dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Distribution charts saved to {self.output_dir}/distribution_charts.png")
    
    def run_all(self):
        """Generate all visualizations"""
        print("\n" + "="*50)
        print("GENERATING SALES DASHBOARD")
        print("="*50 + "\n")
        
        self.create_static_charts()
        self.create_interactive_dashboard()
        self.create_correlation_heatmap()
        self.create_distribution_charts()
        
        print("\n" + "="*50)
        print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
        print(f"✓ Check the '{self.output_dir}' folder for outputs")
        print("="*50 + "\n")
