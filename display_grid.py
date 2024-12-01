from PySide6.QtWidgets import QLineEdit, QGridLayout, QWidget,QLabel
from PySide6.QtCore import Qt

class DisplayMain(QLineEdit):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.style_config()
        

    def style_config(self):

        self.setStyleSheet(f'font-size: 24px')
        self.setMaximumHeight(36)
        self.setMinimumWidth(200)

class DisplaySecondary(DisplayMain):

    def style_config(self):
        
        self.setStyleSheet(f'font-size: 22px')
        self.setMinimumHeight(40)
        self.setMaximumWidth(72)

class DisplayGrid(QWidget):

    def __init__(self,rows_input, columns_input, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.createGrid(rows_input, columns_input)
    
    def createGrid(self,rows = 3,columns = 3):
        for row in range(rows):
            for column in range(columns):

                display = DisplaySecondary()

                self.grid_layout.addWidget(display,row,column)

class Label(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet('font-size: 24px')
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setMargin(10)

