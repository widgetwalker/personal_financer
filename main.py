import pygame
import pygame.freetype
import sys
from datetime import datetime
import os

# Import our modules
from db_setup import create_database
from data_handler import FinanceDataHandler
from visualizer import FinanceVisualizer

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (100, 100, 255)
LIGHT_GREEN = (144, 238, 144)  # Light green for main screen
LIGHT_PURPLE = (221, 160, 221)  # Light purple for charts screen

# Load fonts
pygame.freetype.init()
font_small = pygame.freetype.SysFont("Arial", 16)
font_medium = pygame.freetype.SysFont("Arial", 20)
font_large = pygame.freetype.SysFont("Arial", 24)
font_title = pygame.freetype.SysFont("Arial", 32, bold=True)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=LIGHT_BLUE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)
        
        text_surf, text_rect = font_medium.render(self.text, self.text_color)
        text_rect.center = self.rect.center
        screen.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class TextInput:
    def __init__(self, x, y, width, height, placeholder="", text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, screen):
        color = LIGHT_GRAY if self.active else WHITE
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)
        
        if self.text:
            text_surf, text_rect = font_medium.render(self.text, BLACK)
        else:
            text_surf, text_rect = font_medium.render(self.placeholder, DARK_GRAY)
        
        text_rect.topleft = (self.rect.x + 10, self.rect.y + (self.rect.height - text_rect.height) // 2)
        screen.blit(text_surf, text_rect)
        
        if self.active and self.cursor_visible:
            if self.text:
                cursor_x = text_rect.right + 2
            else:
                cursor_x = self.rect.x + 10
            pygame.draw.line(screen, BLACK, (cursor_x, self.rect.y + 5), (cursor_x, self.rect.y + self.rect.height - 5), 2)
    
    def update(self, events):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.active = False
                else:
                    self.text += event.unicode

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.active = False
        self.selected = options[0] if options else ""
        self.dropdown_rect = pygame.Rect(x, y + height, width, height * len(options))
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)
        
        text_surf, text_rect = font_medium.render(self.selected, BLACK)
        text_rect.topleft = (self.rect.x + 10, self.rect.y + (self.rect.height - text_rect.height) // 2)
        screen.blit(text_surf, text_rect)
        
        pygame.draw.polygon(screen, BLACK, [
            (self.rect.right - 20, self.rect.centery - 5),
            (self.rect.right - 10, self.rect.centery - 5),
            (self.rect.right - 15, self.rect.centery + 5)
        ])
        
        if self.active:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + i * self.rect.height, 
                                         self.rect.width, self.rect.height)
                pygame.draw.rect(screen, WHITE, option_rect)
                pygame.draw.rect(screen, DARK_GRAY, option_rect, 1)
                
                text_surf, text_rect = font_medium.render(option, BLACK)
                text_rect.topleft = (option_rect.x + 10, option_rect.y + (option_rect.height - text_rect.height) // 2)
                screen.blit(text_surf, text_rect)
    
    def update(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_pos):
                    self.active = not self.active
                elif self.active:
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + i * self.rect.height, 
                                                self.rect.width, self.rect.height)
                        if option_rect.collidepoint(mouse_pos):
                            self.selected = option
                            self.active = False
                            return True
                    self.active = False
        return False

class FinanceTrackerApp:
    def __init__(self):
        create_database()
        self.data_handler = FinanceDataHandler()
        self.visualizer = FinanceVisualizer(self.data_handler)
        self.current_screen = "main"
        self.transactions = []
        self.categories = []
        self.current_year = str(datetime.now().year)
        self.chart_type = "pie_expense"
        self.current_chart_surface = None
        self.zoom_scale = 1.0
        self.fullscreen = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Personal Finance Tracker")
        self.load_data()
        self.init_ui()
        
    def load_data(self):
        transactions_df = self.data_handler.get_all_transactions()
        self.transactions = transactions_df.to_dict('records') if not transactions_df.empty else []
        categories_df = self.data_handler.get_all_categories()
        self.categories = categories_df.to_dict('records') if not categories_df.empty else []
        self.income_categories = [cat['name'] for cat in self.categories if cat['type'] == 'income']
        self.expense_categories = [cat['name'] for cat in self.categories if cat['type'] == 'expense']
        self.saving_categories = [cat['name'] for cat in self.categories if cat['type'] == 'saving']
        if not self.income_categories: self.income_categories = ['Salary']
        if not self.expense_categories: self.expense_categories = ['Groceries']
        if not self.saving_categories: self.saving_categories = ['Savings']
    
    def init_ui(self):
        self.main_buttons = [
            Button(WIDTH//2 - 150, 200, 300, 60, "Add Transaction", GRAY, LIGHT_BLUE),
            Button(WIDTH//2 - 150, 300, 300, 60, "View Transactions", GRAY, LIGHT_BLUE),
            Button(WIDTH//2 - 150, 400, 300, 60, "Charts & Analytics", GRAY, LIGHT_BLUE),
            Button(WIDTH//2 - 150, 500, 300, 60, "Export Data", GRAY, LIGHT_BLUE),
            Button(WIDTH//2 - 150, 600, 300, 60, "Exit", GRAY, RED)
        ]
        self.date_input = TextInput(400, 150, 200, 40, "YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
        self.amount_input = TextInput(400, 200, 200, 40, "Amount")
        self.description_input = TextInput(400, 250, 400, 40, "Description")
        self.transaction_type_dropdown = Dropdown(400, 300, 200, 40, ["Income", "Expense", "Saving"])
        self.category_dropdown = Dropdown(400, 350, 200, 40, self.income_categories)
        self.add_transaction_buttons = [
            Button(400, 450, 150, 50, "Save", GREEN),
            Button(600, 450, 150, 50, "Cancel", RED)
        ]
        self.transaction_page = 0
        self.transactions_per_page = 10
        self.view_transactions_buttons = [
            Button(300, 700, 150, 50, "Previous", BLUE),
            Button(500, 700, 150, 50, "Next", BLUE),
            Button(700, 700, 150, 50, "Back", RED)
        ]
        self.chart_buttons = [
            Button(50, 150, 200, 40, "Expense Pie Chart", BLUE),
            Button(50, 200, 200, 40, "Income Pie Chart", BLUE),
            Button(50, 250, 200, 40, "Saving Pie Chart", BLUE),
            Button(50, 300, 200, 40, "Monthly Summary", BLUE),
            Button(50, 350, 200, 40, "Balance Over Time", BLUE),
            Button(50, 400, 200, 40, "Financial Flow", BLUE),
            Button(50, 600, 200, 40, "Back", RED)
        ]
        self.year_input = TextInput(50, 500, 100, 40, "Year", self.current_year)
        self.update_chart_button = Button(170, 500, 80, 40, "Update", GREEN)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            events = []
            
            for event in pygame.event.get():
                events.append(event)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.zoom_scale = min(2.0, self.zoom_scale + 0.1)
                        self.generate_chart()
                    elif event.key == pygame.K_MINUS:
                        self.zoom_scale = max(0.5, self.zoom_scale - 0.1)
                        self.generate_chart()
            
            # Draw background based on current screen
            self.draw_background()
            
            if self.current_screen == "main":
                self.handle_main_screen(mouse_pos, mouse_clicked)
            elif self.current_screen == "add_transaction":
                self.handle_add_transaction_screen(events, mouse_pos, mouse_clicked)
            elif self.current_screen == "view_transactions":
                self.handle_view_transactions_screen(mouse_pos, mouse_clicked)
            elif self.current_screen == "charts":
                self.handle_charts_screen(events, mouse_pos, mouse_clicked)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def draw_background(self):
        if self.current_screen == "main":
            # Light green gradient
            for y in range(HEIGHT):
                r = max(144, min(255, 144 + (y * 2 // HEIGHT) * 111))  # Gradient from light green to white
                g = max(238, min(255, 238 + (y * 2 // HEIGHT) * 17))
                b = max(144, min(255, 144 + (y * 2 // HEIGHT) * 111))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
            # Optional: Uncomment to use an image
            # background = pygame.image.load("main_background.png").convert()
            # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            # self.screen.blit(background, (0, 0))
        elif self.current_screen == "add_transaction":
            # Light blue gradient
            for y in range(HEIGHT):
                r = max(100, min(255, 100 + (y * 2 // HEIGHT) * 155))
                g = max(100, min(255, 100 + (y * 2 // HEIGHT) * 155))
                b = max(255, min(255, 255 + (y * 2 // HEIGHT) * 0))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
            # Optional: Uncomment to use an image
            # background = pygame.image.load("add_transaction_background.png").convert()
            # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            # self.screen.blit(background, (0, 0))
        elif self.current_screen == "view_transactions":
            # Light gray gradient with subtle pattern
            for y in range(HEIGHT):
                r = max(230, min(255, 230 + (y * 2 // HEIGHT) * 25))
                g = max(230, min(255, 230 + (y * 2 // HEIGHT) * 25))
                b = max(230, min(255, 230 + (y * 2 // HEIGHT) * 25))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
            # Optional subtle lines for pattern
            for x in range(0, WIDTH, 50):
                pygame.draw.line(self.screen, (220, 220, 220), (x, 0), (x, HEIGHT), 1)
            # Optional: Uncomment to use an image
            # background = pygame.image.load("view_transactions_background.png").convert()
            # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            # self.screen.blit(background, (0, 0))
        elif self.current_screen == "charts":
            # Light purple gradient
            for y in range(HEIGHT):
                r = max(221, min(255, 221 + (y * 2 // HEIGHT) * 34))
                g = max(160, min(255, 160 + (y * 2 // HEIGHT) * 95))
                b = max(221, min(255, 221 + (y * 2 // HEIGHT) * 34))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
            # Optional: Uncomment to use an image
            # background = pygame.image.load("charts_background.png").convert()
            # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            # self.screen.blit(background, (0, 0))

    def handle_add_transaction_screen(self, events, mouse_pos, mouse_clicked):
        font_title.render_to(self.screen, (WIDTH//2 - 150, 80), "Add Transaction", BLACK)
        font_medium.render_to(self.screen, (250, 160), "Date:", BLACK)
        font_medium.render_to(self.screen, (250, 210), "Amount:", BLACK)
        font_medium.render_to(self.screen, (250, 260), "Description:", BLACK)
        font_medium.render_to(self.screen, (250, 310), "Type:", BLACK)
        font_medium.render_to(self.screen, (250, 360), "Category:", BLACK)
        
        self.date_input.update(events)
        self.date_input.draw(self.screen)
        self.amount_input.update(events)
        self.amount_input.draw(self.screen)
        self.description_input.update(events)
        self.description_input.draw(self.screen)
        
        type_changed = self.transaction_type_dropdown.update(events, mouse_pos)
        if type_changed:
            if self.transaction_type_dropdown.selected == "Income":
                self.category_dropdown = Dropdown(400, 350, 200, 40, self.income_categories)
            elif self.transaction_type_dropdown.selected == "Expense":
                self.category_dropdown = Dropdown(400, 350, 200, 40, self.expense_categories)
            elif self.transaction_type_dropdown.selected == "Saving":
                self.category_dropdown = Dropdown(400, 350, 200, 40, self.saving_categories)
        
        self.category_dropdown.update(events, mouse_pos)
        
        for button in self.add_transaction_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Save":
                    self.save_transaction()
                elif button.text == "Cancel":
                    self.current_screen = "main"
        
        if self.transaction_type_dropdown.active:
            self.category_dropdown.draw(self.screen)
            self.transaction_type_dropdown.draw(self.screen)
        else:
            self.transaction_type_dropdown.draw(self.screen)
            self.category_dropdown.draw(self.screen)
    
    def handle_main_screen(self, mouse_pos, mouse_clicked):
        font_title.render_to(self.screen, (WIDTH//2 - 250, 100), "Personal Finance Tracker", BLACK)
        for button in self.main_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Add Transaction":
                    self.current_screen = "add_transaction"
                elif button.text == "View Transactions":
                    self.current_screen = "view_transactions"
                    self.load_data()
                elif button.text == "Charts & Analytics":
                    self.current_screen = "charts"
                    self.generate_chart()
                elif button.text == "Export Data":
                    filename = self.data_handler.export_to_csv("finance_data.csv")
                    print(f"Data exported to {filename}")
                elif button.text == "Exit":
                    pygame.quit()
                    sys.exit()
    
    def save_transaction(self):
        try:
            date_str = self.date_input.text
            amount = float(self.amount_input.text)
            description = self.description_input.text
            transaction_type = self.transaction_type_dropdown.selected.lower()
            category = self.category_dropdown.selected
            
            if not date_str or amount <= 0 or not category:
                print("Please fill all required fields correctly")
                return
            
            self.data_handler.add_transaction(date_str, amount, category, description, transaction_type)
            self.amount_input.text = ""
            self.description_input.text = ""
            self.current_screen = "main"
            print("Transaction added successfully")
        except ValueError:
            print("Please enter a valid amount")
    
    def handle_view_transactions_screen(self, mouse_pos, mouse_clicked):
        font_title.render_to(self.screen, (WIDTH//2 - 150, 50), "Transactions", BLACK)
        if not self.transactions:
            font_medium.render_to(self.screen, (WIDTH//2 - 150, 300), "No transactions found", BLACK)
        else:
            start_idx = self.transaction_page * self.transactions_per_page
            end_idx = min(start_idx + self.transactions_per_page, len(self.transactions))
            headers = ["Date", "Amount", "Category", "Type", "Description"]
            header_positions = [100, 250, 400, 550, 650]
            for header, x_pos in zip(headers, header_positions):
                font_medium.render_to(self.screen, (x_pos, 100), header, BLACK)
            pygame.draw.line(self.screen, BLACK, (50, 120), (WIDTH-50, 120), 2)
            
            # Create delete buttons for each transaction
            delete_buttons = []
            for i, transaction in enumerate(self.transactions[start_idx:end_idx]):
                y_pos = 150 + i * 50
                date_str = transaction['date']
                amount_str = f"{transaction['amount']:.2f}"
                font_small.render_to(self.screen, (100, y_pos), date_str, BLACK)
                font_small.render_to(self.screen, (250, y_pos), amount_str, BLACK)
                font_small.render_to(self.screen, (400, y_pos), transaction['category'], BLACK)
                font_small.render_to(self.screen, (550, y_pos), transaction['transaction_type'].capitalize(), BLACK)
                description = transaction['description']
                if description and len(description) > 30:
                    description = description[:27] + "..."
                font_small.render_to(self.screen, (650, y_pos), description or "", BLACK)
                
                # Add delete button for this transaction
                delete_button = Button(900, y_pos - 10, 80, 30, "Delete", RED)
                delete_buttons.append((delete_button, transaction))
                delete_button.draw(self.screen)
            
            page_text = f"Page {self.transaction_page + 1} of {max(1, (len(self.transactions) - 1) // self.transactions_per_page + 1)}"
            font_medium.render_to(self.screen, (WIDTH//2 - 50, 650), page_text, BLACK)
            for button in self.view_transactions_buttons:
                button.update(mouse_pos)
                button.draw(self.screen)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Previous" and self.transaction_page > 0:
                        self.transaction_page -= 1
                    elif button.text == "Next" and (self.transaction_page + 1) * self.transactions_per_page < len(self.transactions):
                        self.transaction_page += 1
                    elif button.text == "Back":
                        self.current_screen = "main"
            
            # Handle delete button clicks
            for delete_button, transaction in delete_buttons:
                delete_button.update(mouse_pos)
                if mouse_clicked and delete_button.is_clicked(mouse_pos, mouse_clicked):
                    self.delete_transaction(transaction)
                    self.load_data()  # Reload transactions after deletion
                    break
    
    def delete_transaction(self, transaction):
        # Assuming transaction has a unique identifier (e.g., 'id' from the database)
        transaction_id = transaction.get('id')
        if transaction_id is not None:
            self.data_handler.delete_transaction(transaction_id)
            print(f"Transaction {transaction_id} deleted successfully")
        else:
            print("Error: Transaction ID not found")

    def handle_charts_screen(self, events, mouse_pos, mouse_clicked):
        font_title.render_to(self.screen, (WIDTH//2 - 150, 50), "Charts & Analytics", BLACK)
        for button in self.chart_buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                if button.text == "Expense Pie Chart":
                    self.chart_type = "pie_expense"
                    self.generate_chart()
                elif button.text == "Income Pie Chart":
                    self.chart_type = "pie_income"
                    self.generate_chart()
                elif button.text == "Saving Pie Chart":
                    self.chart_type = "pie_saving"
                    self.generate_chart()
                elif button.text == "Monthly Summary":
                    self.chart_type = "monthly_summary"
                    self.generate_chart()
                elif button.text == "Balance Over Time":
                    self.chart_type = "balance_over_time"
                    self.generate_chart()
                elif button.text == "Financial Flow":
                    self.chart_type = "financial_flow"
                    self.generate_chart()
                elif button.text == "Back":
                    self.current_screen = "main"
        
        self.year_input.update(events)
        self.year_input.draw(self.screen)
        self.update_chart_button.update(mouse_pos)
        self.update_chart_button.draw(self.screen)
        if mouse_clicked and self.update_chart_button.is_clicked(mouse_pos, mouse_clicked):
            self.current_year = self.year_input.text
            self.generate_chart()
        
        if self.current_chart_surface:
            chart_width, chart_height = self.current_chart_surface.get_size()
            scaled_width = int(chart_width * self.zoom_scale)
            scaled_height = int(chart_height * self.zoom_scale)
            scaled_surface = pygame.transform.scale(self.current_chart_surface, (scaled_width, scaled_height))
            
            chart_x = (self.screen.get_width() - scaled_width) // 2
            chart_y = 150
            self.screen.blit(scaled_surface, (chart_x, chart_y))
    
    def generate_chart(self):
        fig = None
        if self.chart_type == "pie_expense":
            fig = self.visualizer.pie_chart_by_category("expense")
        elif self.chart_type == "pie_income":
            fig = self.visualizer.pie_chart_by_category("income")
        elif self.chart_type == "pie_saving":
            fig = self.visualizer.pie_chart_by_category("saving")
        elif self.chart_type == "monthly_summary":
            fig = self.visualizer.bar_chart_monthly_summary(self.current_year)
        elif self.chart_type == "balance_over_time":
            fig = self.visualizer.line_chart_balance_over_time(self.current_year)
        elif self.chart_type == "financial_flow":
            fig = self.visualizer.stacked_area_chart(self.current_year)
        
        if fig:
            self.current_chart_surface = self.visualizer.fig_to_surface(fig)
        else:
            self.current_chart_surface = None

if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()