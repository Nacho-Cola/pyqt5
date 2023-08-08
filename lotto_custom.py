

import sys
from PyQt5.QtWidgets import *
import serial
import openpyxl
from datetime import datetime


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.get_number_btn = QPushButton('Gotcha!',self)
        self.ser = serial.Serial('COM4', 115200)
        self.workbook = openpyxl.Workbook()
        self.records = self.workbook.active
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setWindowTitle("Lotto")
        self.resize(400, 300)
        
        label1 = QLabel("Get Lucky Number!",self)
        label1.move(140,70)
        font1 = label1.font()
        font1.setPointSize(10)
        label1.setFont(font1)
        
        label2 = QLabel("#----!UART_data!----# ",self)
        label2.move(100,120)
        font1 = label1.font()
        font1.setPointSize(15)
        label2.setFont(font1)
        
        
        self.get_number_btn.move(160,200)
        self.get_number_btn.clicked.connect(lambda:self.get_number_btn_click(label2))
        
        self.layout.addWidget(label1)
        self.layout.addWidget(label2)
        self.layout.addWidget(self.get_number_btn)
        
        self.show()

    def get_number_btn_click(self, label):
        uart_data = sorted(list(map(int, str(self.ser.readline())[2:-5].split(','))))
        label.setText(str(uart_data))
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        data_list = [current_time] + uart_data
        self.records.append(data_list)
        try:
            self.workbook.save('data.xlsx')
        except PermissionError:
            print('파일이 열려있어서 저장할 수 없습니다. 파일을 닫은 후 다시 시도하세요.')
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())