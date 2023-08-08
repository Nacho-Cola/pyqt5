

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import serial
import openpyxl
import threading
from datetime import datetime


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.data_thread = threading.Thread(target=self.process_data)
        self.serial_flag = 0
        self.initUI()
    
    def initUI(self):
        self.port_name = QLineEdit("COM1")
        self.port_name.setAlignment(Qt.AlignRight)
        
        self.b_rate = QLineEdit()
        self.b_rate.setAlignment(Qt.AlignRight)
        self.b_rate.setValidator(QIntValidator())
        
        self.conn_uart_btn = QPushButton("Connect", self)
        self.conn_uart_btn.clicked.connect(self.conn_serial_data)
        self.dis_uart_btn = QPushButton("Disconnect", self)
        self.dis_uart_btn.clicked.connect(self.dis_serial_data)
        self.get_lotto_num_btn = QPushButton("Gotcha!", self)
        self.get_lotto_num_btn.clicked.connect(self.get_lotto_number)
        
        label1 = QLabel("Get Lucky Number!",self)
        font1 = label1.font()
        font1.setPointSize(10)
        label1.setFont(font1)
        
        label2 = QLabel("#----!UART_data!----# ",self)
        label2.move(100,120)
        font1 = label1.font()
        font1.setPointSize(15)
        label2.setFont(font1)
        
        
        self.body = QVBoxLayout(self)
        
        self.flo = QFormLayout(self)
        self.flo.addRow("Port Name :", self.port_name)
        self.flo.addRow("Boud Rate :", self.b_rate)
        
        self.body.addLayout(self.flo)
        self.body.addWidget(self.conn_uart_btn)
        self.body.addWidget(self.dis_uart_btn)
        self.body.addSpacing(50)
        self.body.addWidget(label1)
        self.body.addWidget(label2)
        
        
        self.setLayout(self.flo)
        self.setWindowTitle("Lotto")
        self.resize(400,400)
        
        self.show()
        
    def conn_serial_data(self):
        try:
            ser_port_name = self.port_name.text()
            ser_b_rate = int(self.b_rate.text())
        except:
            print("Null input")
        try:
            self.ser = serial.Serial(ser_port_name, ser_b_rate)
            print("UART Connected")
            self.serial_flag = 1
        except:
            print("Check your port number.")   
            
    def dis_serial_data(self):
        try:
            self.ser.close()
            print("UART disconnected")
            self.serial_flag = 0
        except:
            print("UART is not working")
            
    def get_lotto_number(self):
        
    def process_data(self):
        while self.serial_flag:
        
        

    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())