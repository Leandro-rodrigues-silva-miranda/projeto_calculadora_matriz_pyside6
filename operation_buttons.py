from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget,QMessageBox
from PySide6.QtCore import Slot,Qt
from PySide6.QtGui import QIntValidator

import sys,os
from subprocess import Popen

from display_grid import DisplayMain,DisplaySecondary
if TYPE_CHECKING:
    from main_window import Window
    from typing import Tuple
    from math_functions import Equation

class Button(QPushButton):

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()

    def config_style(self):
        font = self.font()
        font.setPixelSize(24)
        font.setBold(True)
        self.setFont(font)
        self.setMinimumHeight(80)

class ButtonGrid(QWidget):



    def __init__(self, myWindow: 'Window', equation: 'Equation', display1: 'DisplayMain' = None, display2:'DisplayMain' = None, 
                 created_button: Button = None, auto_create = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if myWindow:
            self._window = myWindow
        if equation:
            self._equation = equation


        if display1 or display2:
            self.display1 = display1
            self.display2 = display2
        
        self.gridLayout = QGridLayout(self)

        if created_button:
            self._button_connection(created_button)

        if auto_create:
            self.buttons = ['+','-','x','*']
            self.create_grid()


    def create_grid(self):

        for key,item in enumerate(self.buttons):
            
            button = Button(item)

            self.gridLayout.addWidget(button,1,key)
            self._button_connection(button)

    def _connectClickedButton(self, button: Button, slot):
        button.clicked.connect(slot)


    def _make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def slot(_):
            func(*args, **kwargs)
        return slot
    
    def _button_connection(self, button: Button):

        text = button.text()
    

        match text:
            case '+':
                self._connectClickedButton(button, self.add)
            case '-':
                self._connectClickedButton(button, self.sub)
            case 'x':
                self._connectClickedButton(button, self.esc_multiply)
            case '*':
                self._connectClickedButton(button, self.matrix_multiply)
            case 'Enviar tamanhos':
                self._connectClickedButton(button, self.send_size)


    def add(self):
        self._equation.operation = 'add'
        self._window.change_window('Digite o tamanho das matrizes:',self._equation)
        
    
    def sub(self):
        self._equation.operation = 'sub'
        self._window.change_window('Digite o tamanho das matrizes:',self._equation)

    def esc_multiply(self):
        self._equation.operation = 'esc'
        self._window.change_window('Digite o tamanho da matriz:',self._equation)
        

    def matrix_multiply(self):
        self._equation.operation = 'mult'
        self._window.change_window('Digite o tamanho da matriz:', self._equation)

    @Slot()
    def send_size(self):


        self._equation.sizeMatrix = [int(self.display1.text()),int(self.display2.text())]

        self.matrix_grid()

    def matrix_grid(self, result=False,
                    label = 'Entre com os dados da matriz:', escalar = False, multiply = False):

        try:
            self._window.main_label.setText(label)
            if escalar:
                rows,columns = 1,1
            elif multiply and result:
                rows = len(self._equation.result)
                columns = len(self._equation.result)
            elif multiply:
                columns,rows = self._equation.sizeMatrix
            else:
                rows,columns = self._equation.sizeMatrix

            if rows<=0 or columns<=0:
                
                raise ValueError('Dimensões devem ser maiores que zero')

            self.clear_layout()
            self.inputs = []

            for row in range(rows):
                input_row = []
                for column in range(columns):
                    input_field = DisplaySecondary()
                    input_field.setValidator(QIntValidator(0,1000))
                    input_field.setPlaceholderText(f'({row+1},{column+1})')
                    input_field.setAlignment(Qt.AlignCenter)
                    if result:
                        input_field.setText(str(self._equation.result[row][column]))
                    self.gridLayout.addWidget(input_field,row,column)
                    input_row.append(input_field)

                self.inputs.append(input_row)


        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira valores válidos")
        if not result:
            sendMatrix = Button('Enviar matriz')
            sendMatrix.clicked.connect(self.send_matrix)

            self.gridLayout.addWidget(sendMatrix,row+1,(columns/2)-1,1,2 if columns%2==0 else 3,
                                  Qt.AlignmentFlag.AlignCenter)
        else:
            restart = Button('Reiniciar')
            restart.clicked.connect(self.restart)

            self.gridLayout.addWidget(restart,row+1,(columns/2)-1,1,2 if columns%2==0 else 3,
                                  Qt.AlignmentFlag.AlignCenter)

    def clear_layout(self):
        

        while self.gridLayout.count():

            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def send_matrix(self):

        if self._equation.current_stage == 'matrixA':
            for row in self.inputs:
                temp_row = []
                for column in row:
                    temp_row.append(int(column.text()))
                self._equation.matrixA.append(temp_row)
            self._equation.current_stage = 'matrixB'
            if self._equation.operation == 'esc':
                self.matrix_grid(escalar=True, label='Insira o escalar que vai multiplicar a matriz')
            elif self._equation.operation == 'mult':
                self.matrix_grid(multiply=True)
            else:
                self.matrix_grid()

        elif self._equation.current_stage == "matrixB":

            for row in self.inputs:
                temp_row = []
                for column in row:
                    temp_row.append(int(column.text()))
                self._equation.matrixB.append(temp_row)
                
            self._equation.result.clear()
            if self._equation.operation != 'mult':
                for row in range(self._equation.sizeMatrix[0]):
                    result_row = []
                    for column in range(self._equation.sizeMatrix[1]):
                        if self._equation.operation == 'add':
                            result_row.append(self._equation.matrixA[row][column]
                                            + self._equation.matrixB[row][column])
                        elif self._equation.operation == 'sub':
                            result_row.append(self._equation.matrixA[row][column]
                                            - self._equation.matrixB[row][column])
                        elif self._equation.operation == 'esc':
                            result_row.append(self._equation.matrixA[row][column]
                                            * self._equation.matrixB[0][0])
                    self._equation.result.append(result_row)
                
            else:
                result_range = self._equation.sizeMatrix[0]
                temp_result = [[0 for _ in range(result_range)] for _ in range(result_range)]

                for i in range(len(self._equation.matrixA)):
                    for j in range(len(self._equation.matrixB[0])):
                        for k in range(len(self._equation.matrixB)):
                            temp_result[i][j] += self._equation.matrixA[i][k] * self._equation.matrixB[k][j]


                self._equation.result = temp_result

            self._equation.current_stage = 'result'
            label = "O resultado da {} é: ".format("soma" if self._equation.operation == "add" else
                                        "subtração" if self._equation.operation == "sub" else
                                        "multiplicação por escalar" if self._equation.operation == "esc" else 
                                        "multiplicação de matrizes" if self._equation.operation == "mult" else "")
            if not self._equation.operation == 'mult':
                self.matrix_grid(result=True, label=label)
            else: self.matrix_grid(result=True,label=label, multiply=True)




    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)