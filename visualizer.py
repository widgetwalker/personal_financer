import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame

class FinanceVisualizer:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def pie_chart_by_category(self, transaction_type, start_date=None, end_date=None):
        df = self.data_handler.get_summary_by_category(transaction_type, start_date, end_date)
        
        if df.empty:
            return None
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(df['total'], labels=df['category'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        title = f'{transaction_type.capitalize()} Distribution by Category'
        if start_date and end_date:
            title += f" ({start_date} to {end_date})"
        
        ax.set_title(title)
        
        return fig
    
    def bar_chart_monthly_summary(self, year):
        df = self.data_handler.get_monthly_summary(year)
        
        if df.empty:
            return None
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        months = df['month_name']
        income = df['income']
        expense = df['expense']
        saving = df['saving']
        
        x = np.arange(len(months))
        width = 0.25
        
        ax.bar(x - width, income, width, label='Income')
        ax.bar(x, expense, width, label='Expense')
        ax.bar(x + width, saving, width, label='Saving')
        
        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45)
        ax.set_ylabel('Amount')
        ax.set_title(f'Monthly Financial Summary - {year}')
        ax.legend()
        
        plt.tight_layout()
        
        return fig
    
    def line_chart_balance_over_time(self, year):
        df = self.data_handler.get_monthly_summary(year)
        
        if df.empty:
            return None
        
        # Calculate balance (income - expense)
        df['balance'] = df['income'] - df['expense']
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(df['month_name'], df['balance'], marker='o', linestyle='-')
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Balance (Income - Expense)')
        ax.set_title(f'Balance Over Time - {year}')
        ax.grid(True)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def stacked_area_chart(self, year):
        df = self.data_handler.get_monthly_summary(year)
        
        if df.empty:
            return None
        
        # Create stacked area chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        months = df['month_name']
        
        ax.stackplot(months, df['income'], df['expense'], df['saving'], 
                    labels=['Income', 'Expense', 'Saving'],
                    alpha=0.8)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title(f'Financial Flow - {year}')
        ax.legend(loc='upper left')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
        
    def fig_to_surface(self, fig):
        """Convert a matplotlib figure to a pygame surface"""
        # Create a canvas and render the figure
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        # Get the RGBA buffer from the figure
        buf = canvas.buffer_rgba()

        # Get the dimensions of the figure
        width, height = fig.canvas.get_width_height()

        # Convert the buffer to a Pygame surface
        surf = pygame.image.frombuffer(buf, (width, height), "RGBA")
        
        plt.close(fig)  # Close the figure to free memory
        
        return surf