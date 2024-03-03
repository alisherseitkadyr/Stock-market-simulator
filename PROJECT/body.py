from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PyQt5.QtMultimedia import QSound

class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ax = None
        self.canvas = None
        self.cash = 10000
        self.stock_portfolio = {'AAPL': 10, 'AMZN': 10, 'TSLA': 10, 'MSFT': 10,'HSBK.L':0}
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('Stock Trading App')

        self.central_widget = QFrame(self)
        self.setCentralWidget(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_account_widget()
        self.create_graph_widget()
        self.create_stock_list_widget()

    def create_account_widget(self):
        account_widget = QFrame(self.central_widget)
        account_layout = QVBoxLayout(account_widget)

        user_id_label = QLabel('User ID: 123456')
        user_name_label = QLabel('Name: John Maichle')
        cash_label = QLabel(f'Cash: ${self.cash}')

        account_layout.addWidget(user_id_label)
        account_layout.addWidget(user_name_label)
        account_layout.addWidget(cash_label)

        portfolio_label = QLabel(f'Portfolio: {self.stock_portfolio}')
        account_layout.addWidget(portfolio_label)

        self.layout.addWidget(account_widget)

    def create_graph_widget(self):
        graph_widget = QFrame(self.central_widget)
        graph_layout = QVBoxLayout(graph_widget)

        fig, self.ax = plt.subplots(figsize=(5, 4), tight_layout=True)
        self.canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar2QT(self.canvas, self)
        graph_layout.addWidget(toolbar)
        graph_layout.addWidget(self.canvas)

        stock_data = yf.download('AAPL', start="2023-04-01", end=datetime.today().strftime('%Y-%m-%d'))
        self.ax.plot(stock_data.index, stock_data['Close'])
        self.ax.set_title('AAPL Stock Price')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Closing Price')

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())

        self.canvas.draw()

        self.layout.addWidget(graph_widget)

    def create_stock_list_widget(self):
        stock_list_widget = QFrame(self.central_widget)
        stock_list_layout = QVBoxLayout(stock_list_widget)

        stock_buttons = []
        stocks = ['AAPL', 'AMZN', 'TSLA', 'MSFT','HSBK.L']

        for stock in stocks:
            stock_button = QPushButton(stock, self)
            stock_button.clicked.connect(lambda checked, s=stock: self.show_stock_graph(s))
            stock_buttons.append(stock_button)
            stock_list_layout.addWidget(stock_button)

        self.layout.addWidget(stock_list_widget)

    def show_stock_graph(self, stock):
        stock_data = yf.download(stock, start="2023-04-01", end=datetime.today().strftime('%Y-%m-%d'))

        self.ax.clear()

        self.ax.plot(stock_data.index, stock_data['Close'])
        self.ax.set_title(f'{stock} Stock Price')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Closing Price')

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mdates.MonthLocator())

        self.canvas.draw()
        self.buyorsell(stock)

    def buyorsell(self, stock):
        input_frame = None
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QFrame) and widget.objectName() == "input_frame":
                input_frame = widget
                break

        if input_frame is None:
            input_frame = QFrame(self.central_widget)
            input_frame.setObjectName("input_frame")
            input_layout = QVBoxLayout(input_frame)

            input_label = QLabel(f"Enter the number of {stock} stocks:")
            input_edit = QLineEdit(self)
            buy_button = QPushButton("Buy", self)
            sell_button = QPushButton("Sell", self)
            close_button = QPushButton("Close", self)

            buy_button.clicked.connect(lambda: self.handle_buy_sell(stock, 'buy', input_edit.text()))
            sell_button.clicked.connect(lambda: self.handle_buy_sell(stock, 'sell', input_edit.text()))
            close_button.clicked.connect(lambda: self.hide_buttons())

            input_layout.addWidget(input_label)
            input_layout.addWidget(input_edit)
            input_layout.addWidget(buy_button)
            input_layout.addWidget(sell_button)
            input_layout.addWidget(close_button)

            self.layout.addWidget(input_frame)

    def handle_buy_sell(self, stock, action, quantity_str):
        try:
            quantity = int(quantity_str)
        except ValueError:
            error_message = "Invalid quantity. Please enter a valid number."
            self.show_message(error_message)
            QSound.play("C:\\Users\\Admin\\IdeaProjects\\cashmusic\\archivo.wav")
            return

        stock_data = yf.download(stock, start="2023-01-01", end=datetime.today().strftime('%Y-%m-%d'))
        current_price = stock_data['Close'].iloc[-1]

        if action == 'buy':
            cost = quantity * current_price
            if self.cash >= cost:
                self.cash -= cost
                self.stock_portfolio[stock] += quantity
                success_message = f"Successfully bought {quantity} {stock} stocks. Remaining cash: ${self.cash}"
                QSound.play("C:\\Users\\Admin\\IdeaProjects\\cashmusic\\cashier-quotka-chingquot-sound-effect-129698.wav")
                self.show_message(success_message)
            else:
                insufficient_funds_message = "Insufficient funds to buy. Transaction canceled."
                QSound.play("C:\\Users\\Admin\\IdeaProjects\\cashmusic\\archivo.wav")
                self.show_message(insufficient_funds_message)

        elif action == 'sell':
            if self.stock_portfolio[stock] >= quantity:
                self.cash += quantity * current_price
                self.stock_portfolio[stock] -= quantity
                success_message = f"Successfully sold {quantity} {stock} stocks. Remaining cash: ${self.cash}"
                QSound.play("C:\\Users\\Admin\\IdeaProjects\\cashmusic\\cashier-quotka-chingquot-sound-effect-129698.wav")
                self.show_message(success_message)
            else:
                insufficient_stocks_message = f"Insufficient {stock} stocks to sell. Transaction canceled."
                QSound.play("C:\\Users\\Admin\\IdeaProjects\\cashmusic\\archivo.wav")
                self.show_message(insufficient_stocks_message)

        self.hide_buttons()
        self.update_portfolio_label()
        self.update_cash_label()

    def hide_buttons(self):
        input_frame = self.central_widget.findChild(QFrame, "input_frame")
        if input_frame is not None:
            self.close_input_frame(input_frame)

    def close_input_frame(self, input_frame):
        for i in range(input_frame.layout().count()):
            widget = input_frame.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.disconnect()

        self.layout.removeWidget(input_frame)
        input_frame.deleteLater()

    def update_cash_label(self):
        cash_label = self.layout.itemAt(0).widget().layout().itemAt(2).widget()
        cash_label.setText(f'Cash: ${int(self.cash)}')

    def update_portfolio_label(self):
        portfolio_label = self.layout.itemAt(0).widget().layout().itemAt(3).widget()
        portfolio_label.setText(f'Portfolio: {self.stock_portfolio}')

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.setWindowTitle("Stock Trading App")
        msg_box.exec_()

app = QApplication([])
stock_app = StockApp()
stock_app.show()
app.exec_()
