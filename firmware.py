import time
import serial

class atGen():
    
    def __init__(self, com_port) -> None:
        self.UARTconfig(com_port)

    # UART configuration
    def UARTconfig(self, COM):
        self.serialPort = serial.Serial(
            port=COM, baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE
        ) 

    def HT_UART_command(self, command):
        command = command + ('\r\n')
        byteCommand = bytes(command, 'utf-8')
        self.serialPort.write(byteCommand)
        time.sleep(0.05)  # 50ms

    def test_Init(self):
        uart_command = input("Enter the UART command: ")  # Prompt the user for the command
        result = self.HT_UART_command(uart_command)  # Use the entered command
        print(result) 

if __name__ == "__main__":
    com_port = "COM4"  # Update with the correct COM port
    AT_tx = atGen(com_port)     
    AT_tx.test_Init()  
