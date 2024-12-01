from typing import TYPE_CHECKING
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QStackedWidget

from display_grid import Label
from operation_buttons import ButtonGrid

if TYPE_CHECKING:
    from math_functions import Equation

class Window(QMainWindow):
    #Classe que cria a janela principal da aplicação

    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)


        

        self.stackedWidget = QStackedWidget()
        self.main_label = Label()
        self.main_label.setText('Qual operação deseja realizar?')
        #Criação da parte central da janela, funções principais onde 
        #as ações devem acontecer
        self.myCentralWidget = QWidget()

        self.myVLayout = QVBoxLayout()
        self.myCentralWidget.setLayout(self.myVLayout)
        self.setCentralWidget(self.myCentralWidget)

        #Titulo da Janel
        self.setWindowTitle("Calculadora de matrizes")

        #Criação do menu de opções
        self.menu = self.menuBar()

        self.firstMenu = self.menu.addMenu("Menu")
        self.help = self.firstMenu.addAction('Ajuda')
        self.help.triggered.connect(self._make_slot(self.show_msg_box, 
            "Está é uma calculadora que realiza algumas das principais operações"+
            " em matrizes. São elas:\n\t● Adição (+)\n\t● Subtração (-)\n\t● Multiplicação "+
            " por escalar (x)\n\t● Multiplicação de matrizes (*)"))
        
        self.autores = self.firstMenu.addAction('Autores')
        self.autores.triggered.connect(self._make_slot(self.show_msg_box,
             'Calculadora desenvolvida utilizando a linguagem Python, com a biblioteca de PySide6'+
             ' para criação das interfaces. Desenvolvida por:\n\t●Leandro Rodrigues Silva Miranda'+
             '\n\t●Michel Ferreira de Moura'))

    def adjust_size(self):

        self.adjustSize()
        

    def show_msg_box(self, text):

        msg_box = self.create_msg_box()
        msg_box.setText(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()

    def create_msg_box(self):
        return QMessageBox(self)

    def _make_slot(self, func, *args, **kwargs):

        @Slot(bool)
        def _slot(_):
            func(*args, **kwargs)
        return _slot
    
    @Slot(bool)
    def change_window(self, label_text, equation: 'Equation',index = 1):

        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex()+index)
        self.main_label.setText(label_text)


    