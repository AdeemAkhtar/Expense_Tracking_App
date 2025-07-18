# Imports
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QHeaderView , QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt
import sys

# App Class
class ExpenseApp(QWidget):
    """
    A PyQt5-based GUI application for tracking personal expenses.

    This class creates a simple and interactive interface to:
    - Add expenses with date, category, amount, and description.
    - Delete selected expenses.
    - Display all expenses in a table.
    - Store and retrieve expenses from an SQLite database using Qt's SQL module.

    Attributes
    ----------
    date_box : QDateEdit
        Widget to select the date of the expense.
    dropdown : QComboBox
        Dropdown menu for selecting expense categories.
    amount : QLineEdit
        Input field for entering the amount of the expense.
    description : QLineEdit
        Input field for entering the description of the expense.
    add_button : QPushButton
        Button to trigger the addition of a new expense to the database.
    delete_button : QPushButton
        Button to delete the selected expense from the database.
    table : QTableWidget
        Table that displays the list of expenses from the database.
    master_layout : QVBoxLayout
        Main vertical layout for arranging all components.
    row1, row2, row3 : QHBoxLayout
        Horizontal layout rows for organizing widgets in the UI.

    Methods
    -------
    load_table():
        Loads all expense records from the database into the table widget.
    
    add_expense():
        Adds a new expense to the database and updates the table.

    delete_expense():
        Deletes the selected expense from the database and updates the table.
    """
    def __init__(self):
        """
        Initializes the ExpenseApp GUI, sets up UI components, styles, layouts,
        and connects buttons to their respective slots.
        """
        super().__init__()
        # Main App Object & Settings
        self.resize(550,500)
        self.setWindowTitle("Expense Tracker 2.0")

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton('Add Expense')
        self.delete_button = QPushButton('Delete Expense')

        self.table = QTableWidget()
        self.table.setColumnCount(5) #Id, Data, Catagory, Amount, Description
        self.table.setHorizontalHeaderLabels(['Id', 'Data', 'Catagory', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(0, Qt.DescendingOrder)

        self.dropdown.addItems(['Food', 'Transportation', 'Rent', 'Shopping', 'Enterntainment', 'Bills', 'Others'])
        
        # Style Sheet Styling
        self.setStyleSheet(
            """
                QWidget {background-color: #b8c9e1}

                QLabel{
                    color: #333;
                    font-size : 14px;    
                }

                QLineEdit, QComboBox, QDateEdit{
                    background-color: #b8c9e1;
                    color = #333;
                    border: 1px solid #444;
                    padding: 5px;
                }

                QTableWidget{
                    background-color : #b8c9e1;
                    color: #333;
                    border: 1px solid #444;
                    selection-background-color: #ddd;
                }

                QPushButton{
                    background-color: #4caf50;
                    color: #fff;
                    border: none;
                    padding: 8px 16px;
                    font-size: 14px
                }

                QPushButton:hover{
                    background-color: #45a049;
                }    

            """
        )

        # Design App With Layouts
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        # Row 1
        self.row1.addWidget(QLabel('Date: '))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel('Catagory: '))
        self.row1.addWidget(self.dropdown)

        #Row 2
        self.row2.addWidget(QLabel('Amount: '))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel('Description'))
        self.row2.addWidget(self.description)

        #Row 3
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)

        #Building Master layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        self.load_table()


    def load_table(self):
        """
        Loads all expenses from the 'expenses' table in the database and
        populates the table widget with the data.
        """
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            # Add Values to Table
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1
    
    def add_expense(self):
        """
        Inserts a new expense into the database using the form input values.
        Clears the input fields and refreshes the table after insertion.
        """
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare("""
                        INSERT INTO expenses (date, category, amount, description)
                        VALUES(?, ?, ?, ?)
                      """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()
        
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()


    def delete_expense(self):
        """
        Deletes the currently selected expense from the database after user confirmation.
        If no row is selected, a warning is shown. The table is updated after deletion.
        """
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Expense Chosen", "Please choose the expense to delete!")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())

        confirm = QMessageBox.question(self, "Are you Sure?", "Delete Expense", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()


# Create Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")

if not database.open():
    QMessageBox.critical(None, "Error", "Could not open Database")
    sys.exit(1)

query = QSqlQuery()
query.exec_("""
        CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
""")


# Run The App

if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()