
import os
import sys
from pathlib import Path


from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon,QIntValidator


from main_window import Window
from display_grid import DisplayMain,DisplayGrid,Label
from operation_buttons import ButtonGrid,Button
from math_functions import Equation

ICON_PATH = Path(__file__).parent / 'files/icon.png'




if __name__ == "__main__":


    app = QApplication(sys.argv)
    window = Window()

    icon = QIcon(str(ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    equation = Equation()
    window.main_label.setText('Qual operação deseja realizar?')

    window.myVLayout.addWidget(window.main_label)

    #Operation
    buttonGrid = ButtonGrid(myWindow=window, equation=equation)
    window.stackedWidget.addWidget(buttonGrid)

    
    #Get matrix Size
    display1 = DisplayMain('')
    display1.setValidator(QIntValidator(1,100000))
    XLabel = QLabel('X')
    display2 = DisplayMain('')
    display2.setValidator(QIntValidator(1,100000))
    
    sendSize = Button('Enviar tamanhos')
    
    matrixSizeInput = ButtonGrid(myWindow=window,equation=equation,display1=display1, display2=display2, 
                                 created_button=sendSize,auto_create=False)
    matrixSizeInput.gridLayout.addWidget(display1,1,1)
    matrixSizeInput.gridLayout.addWidget(XLabel,1,2)
    matrixSizeInput.gridLayout.addWidget(display2,1,3)
    matrixSizeInput.gridLayout.addWidget(sendSize,2,1,1,4)

    window.stackedWidget.addWidget(matrixSizeInput)


    window.myVLayout.addWidget(window.stackedWidget)
    
    window.adjust_size()
    window.show()
    sys.exit(app.exec())
