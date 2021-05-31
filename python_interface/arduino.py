import serial
import compressor

class ArduinoInterface:
  def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
    self.port = port
    self.console = serial.Serial(port=port, baudrate=baudrate)
    if not self.console.is_open:
      self.console.open()
    self.console.flush()
    self.console.reset_output_buffer()

  def __del__(self):
    if self.console.is_open:
      self.console.flush()
      self.console.close()

  def write(self, data):
    success = self.console.write(data) == len(data)
    self.console.flush()
    return success

  def print(self, text):
    return self.write(text.encode('utf-8'))

  def println(self, text=''):
    return self.print(text+'\r\n')

  def setPattern(self, pattern):
    return self.write(compressor.compress(pattern))

  def readline(self):
    return self.console.read_until()
