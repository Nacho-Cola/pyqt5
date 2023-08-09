

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import serial
import openpyxl
import threading
from datetime import datetime
import time


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.data_thread = threading.Thread(target=self.process_data)
        self.serial_flag = 0
        self.prev_data = [46]
        self.number_log = []
        self.idx = 1
        self.initUI()
    
    def initUI(self):
        
        self.b_rate = QLineEdit()
        self.b_rate.setAlignment(Qt.AlignRight)
        self.b_rate.setValidator(QIntValidator())
        
        label1 = QLabel("Get Lucky Number!",self) 
        font1 = label1.font()
        font1.setPointSize(10)
        label1.setFont(font1)
        
        label2 = QLabel("#----!UART_data!----# ",self)
        label2.move(100,120)
        font1 = label1.font()
        font1.setPointSize(15)
        label2.setFont(font1)
        
        
        self.conn_uart_btn = QPushButton("Connect", self)
        self.conn_uart_btn.clicked.connect(self.conn_serial_data)
        self.dis_uart_btn = QPushButton("Disconnect", self)
        self.dis_uart_btn.clicked.connect(self.dis_serial_data)
        self.get_lotto_num_btn = QPushButton("Gotcha!", self)
        self.get_lotto_num_btn.clicked.connect(lambda:self.get_lotto_number(label2))
        self.save_btn = QPushButton("Save", self)
        self.save_btn.clicked.connect(lambda:self.save('example'))
        
        self.t_browser = QTextBrowser(self)
        self.t_browser.setAcceptRichText(True)
        
        self.body = QVBoxLayout(self)
        self.flo = QFormLayout(self)
        
        self.port_name = QComboBox(self)
        self.port_name.addItem('COM1')
        self.port_name.addItem('COM2')
        self.port_name.addItem('COM3')
        self.port_name.addItem('COM4')
        
        self.flo.addRow("Port Name :", self.port_name)
        self.flo.addRow("Boud Rate :", self.b_rate)
        
        self.body.addLayout(self.flo)
        self.body.addWidget(self.conn_uart_btn)
        self.body.addWidget(self.dis_uart_btn)
        self.body.addSpacing(50)
        self.body.addWidget(label1)
        self.body.addWidget(label2)
        self.body.addWidget(self.t_browser)
        self.body.addWidget(self.get_lotto_num_btn)
        self.body.addWidget(self.save_btn)
        
        
        self.setLayout(self.flo)
        self.setWindowTitle("Lotto")
        self.resize(400,400)
        
        self.show()
        
    def conn_serial_data(self):
        try:
            ser_port_name = self.port_name.currentText()
            ser_b_rate = int(self.b_rate.text())
        except:
            print("Null input")
        try:
            self.ser = serial.Serial(ser_port_name, ser_b_rate)
            print("UART Connected")
            self.serial_flag = 1
            self.data_thread.start()
        except:
            print("Check your port number.")   
            
    def dis_serial_data(self):
        try:
            self.ser.close()
            print("UART disconnected")
            self.serial_flag = 0
        except:
            print("UART is not working")
            
    def get_lotto_number(self,label):
        try:
            while self.num_check() and self.serial_flag :
                print("change")
            label.setText(str(self.uart_data))
            self.prev_data  = self.uart_data
            self.t_browser.append(str(self.prev_data))
            self.number_log.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]] + self.prev_data)
        except:
            print("UART connect First")
        
    def process_data(self):
        while self.serial_flag:
            self.uart_data = sorted(list(map(int, str(self.ser.readline())[2:-5].split(','))))
            
    
    def num_check(self):
        for i in self.prev_data:
            if i in self.uart_data:
                return 1
        return 0
    
    def save(self, file_name):
        default_dir ="/home/qt_user/Documents"
        default_filename = os.path.join(default_dir, file_name)
        finder, _ = QFileDialog.getSaveFileName(self,'Save Lotto numbers',default_filename,'Excel(*.xlsx)')
        if finder:
            self.save_as_excal(finder)
        
    def save_as_excal(self, file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        for row in self.number_log:
            sheet.append([self.idx]+row)
            self.idx = self.idx + 1
        workbook.save(file_path)
                

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())