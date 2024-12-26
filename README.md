# [UART]Lotto Number Generator

Lotto Number Generator 프로젝트는 UART(Universal Asynchronous Receiver/Transmitter) 통신을 활용하여 데이터를 수신하고, 이를 통해 로또 번호를 생성, 표시, 저장하는 데 목적이 있습니다. 이 프로젝트는 PyQt5를 기반으로 GUI를 제공하며, 직관적인 사용자 인터페이스를 통해 로또 번호를 처리할 수 있습니다.

## 주요 기능

### **lotto.py**
- **UART 연결 및 데이터 처리**
  - 사용자가 선택한 포트와 보드레이트로 UART 연결을 설정합니다.
  - UART를 통해 수신된 데이터를 처리하여 로또 번호를 생성합니다.

- **로또 번호 생성**
  - 버튼 클릭으로 로또 번호를 생성하여 GUI에 표시합니다.
  - 생성된 로또 번호는 시간 정보와 함께 로그에 저장됩니다.

- **Excel 파일로 저장**
  - 생성된 로또 번호 로그를 엑셀 파일로 저장할 수 있습니다.
  - 저장 경로는 파일 선택 대화 상자를 통해 지정됩니다.

---

### **lotto_custom.py**
- **UART 데이터 간소화**
  - 고정된 포트와 보드레이트(COM4, 115200)로 UART 데이터를 수신합니다.
  - 단순화된 GUI와 로직으로 빠르게 로또 번호를 생성하고 기록합니다.

- **Excel 저장**
  - 생성된 로또 번호를 실시간으로 `data.xlsx` 파일에 저장합니다.
  - 파일이 열려 있을 경우 저장되지 않도록 예외 처리를 제공합니다.

## 기술 스택
- **Python**: 주요 로직 구현
- **PyQt5**: GUI 구성 및 사용자 인터페이스 개발
- **OpenPyXL**: Excel 파일 저장 및 관리
- **Serial**: UART 통신

## 파일 구조
```
.
├── lotto.py               # 메인 로또 번호 생성기
├── lotto_custom.py        # 간소화된 로또 번호 생성기
├── data.xlsx              # 생성된 로또 번호 저장 파일 (기본 저장 경로)
├── README.md              # 프로젝트 설명 문서
```


## **lotto.py**
1. **UART 연결**:
   - 포트(COM1, COM2 등)과 보드레이트를 입력한 후 `Connect` 버튼을 클릭하여 UART 연결을 설정합니다.

2. **로또 번호 생성**:
   - `Gotcha!` 버튼을 클릭하여 로또 번호를 생성합니다.
   - 생성된 번호는 GUI에 표시되며, 로그에 기록됩니다.

3. **Excel로 저장**:
   - `Save` 버튼을 클릭하여 생성된 번호 로그를 Excel 파일로 저장합니다.

4. **UART 연결 해제**:
   - `Disconnect` 버튼을 클릭하여 UART 연결을 해제합니다.

---

## **lotto_custom.py**
1. **로또 번호 생성**:
   - `Gotcha!` 버튼을 클릭하여 로또 번호를 생성합니다.
   - 번호는 GUI에 표시되며, `data.xlsx`에 실시간으로 기록됩니다.

2. **파일 저장 오류 처리**:
   - 파일이 열려 있는 경우 저장되지 않으며, 콘솔에 에러 메시지가 표시됩니다.

## 주요 코드 설명

### 1. UART 데이터 처리 (lotto.py)
```python
def process_data(self):
    while self.serial_flag:
        self.uart_data = sorted(list(map(int, str(self.ser.readline())[2:-5].split(','))))
```
- UART 데이터를 실시간으로 읽어 정렬된 리스트 형태로 변환합니다.

### 2. 엑셀 저장 로직 (lotto_custom.py)
```python
self.records.append(data_list)
try:
    self.workbook.save('data.xlsx')
except PermissionError:
    print('파일이 열려있어서 저장할 수 없습니다. 파일을 닫은 후 다시 시도하세요.')
```
- 생성된 데이터를 엑셀에 기록하며, 파일 저장 중 발생할 수 있는 예외를 처리합니다.

### 3. 로또 번호 중복 검사 (lotto.py)
```python
def num_check(self):
    for i in self.prev_data:
        if i in self.uart_data:
            return 1
    return 0
```
- 이전에 생성된 번호와 현재 번호의 중복 여부를 확인합니다.
