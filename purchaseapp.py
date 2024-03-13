
#PLAN:
#backend: utility algorithm, buttons, inputs, outputs
#GUI: two pages: Home, Type. 
#Home: Type buttons: New, Second-Hand, Giveaway
#Type: Cost etc. add something that has red font dont buy, yellow = risk and green do buy

#modules imports:
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit
import sys
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QColor,QFont
from PyQt6.QtGui import QIcon

#total expected utility calculator
def UtilityCalculator(cost,value,total_tix,total_entries):
    probability = total_entries/total_tix
    total_cost = cost*total_entries
    win_value = value-total_cost
    lose_value = -total_cost
    expected_utility = probability*win_value+(1-probability)*lose_value
    return expected_utility

# The main page that switches between pages
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()  # Stacked widget to switch pages on
        self.home_page = HomePage()
        self.giveaways_page = GiveAwaysPage()
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.giveaways_page)

        self.stack.setCurrentWidget(self.home_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        # self.setFixedSize(QSize(800, 500))
        self.setGeometry(100,100,800,600)

        self.home_page.button.clicked.connect(self.open_new_page)

    def open_new_page(self):
        self.stack.setCurrentWidget(self.giveaways_page)

class HoverButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QPushButton { background-color: #606364; }"
                           "QPushButton:hover { background-color: #3e4345; }"
                           "QPushButton:pressed { background-color: #393738; }")

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Home Page")

        font = QFont("Arial",50)
        self.label.setFont(font)

        layout.addWidget(self.label)

        self.button = HoverButton("Give Aways Utility Calculator") 
        font_butt = QFont("Arial",10)
        self.button.setFont(font_butt)
        self.button.setFixedSize(300,90)
        layout.addWidget(self.button)
        self.setLayout(layout)


class GiveAwaysPage(QWidget):
    def __init__(self,):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Give Aways Utility Calculator")
        font = QFont("Arial",50)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.explanation_label = QLabel("""This calculates the total expected utility of participating 
in a give-away lottery. Please input the price of a single ticket, 
the total value of the item if won, the total number of tickets 
available and the total number you bought/plan to buy.
""")
        font_description = QFont("Arial",15)
        self.explanation_label.setFont(font_description)
        layout.addWidget(self.explanation_label)

        font_new = QFont("Arial",10)

        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Cost")
        self.cost_input.setFont(font_new)
        #self.cost_input.setStyleSheet("background-color: green;")  # Set background color
        layout.addWidget(self.cost_input)

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value")
        self.value_input.setFont(font_new)
        layout.addWidget(self.value_input)

        self.total_tix_input = QLineEdit()
        self.total_tix_input.setPlaceholderText("Total Tickets")
        self.total_tix_input.setFont(font_new)
        layout.addWidget(self.total_tix_input)

        self.total_entries_input = QLineEdit()
        self.total_entries_input.setPlaceholderText("Total Entries")
        self.total_entries_input.setFont(font_new)
        layout.addWidget(self.total_entries_input)

        self.calculate_button = HoverButton("Calculate Utility")
        self.calculate_button.setFont(font_new)
        layout.addWidget(self.calculate_button)
        self.calculate_button.clicked.connect(self.calculate_utility)

#new
        self.back_button = HoverButton("Back to Home")
        layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.go_to_home_page)
#old
        
        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.buy_advice_label = QLabel() 

        self.setLayout(layout)

    def go_to_home_page(self):
        # Get the parent widget (MainWindow) and switch to the home page
        parent = self.parentWidget().parentWidget()
        parent.stack.setCurrentWidget(parent.home_page)
        #parent.open_new_page()  # Call the method to switch pages defined in MainWindow

    def calculate_utility(self):
        try:
            font_new = QFont("Arial",10)
            cost = float(self.cost_input.text())
            value = float(self.value_input.text())
            total_tix = float(self.total_tix_input.text())
            total_entries = float(self.total_entries_input.text())
            expected_utility = UtilityCalculator(cost,value,total_tix,total_entries)
            self.result_label.setFont(font_new)
            self.result_label.setText(f"Expected Utility: {expected_utility:.2f}")

            #ensures that buy_label is removed each time calculator is called
            if hasattr(self, 'buy_advice_label'):
                self.layout().removeWidget(self.buy_advice_label)
                self.buy_advice_label.deleteLater()
            
            #creates advice depending on values
            self.buy_advice_label.setFont(font_new)
            buy_advice = "You should buy." if expected_utility > 0 else "You shouldn't buy."
            self.buy_advice_label = QLabel(buy_advice)
            self.buy_advice_label.setStyleSheet("color: green;" if expected_utility > 0 else "color: red;")
            self.layout().addWidget(self.buy_advice_label)

        except ValueError:
            self.result_label.setText("Please enter valid numeric values.")

# Open the widgets and pages
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #262626;  /* Dark gray background */
            color: #FFFFFF;             /* White text color */
        }
    """)
    window = MainWindow()
    window.setWindowTitle('Purchase Decider App')
    window.show()
    sys.exit(app.exec())





