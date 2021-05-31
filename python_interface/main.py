from patterns import PatternManager
from arduino import ArduinoInterface
from time import sleep
import weather

from threading import Thread

# number of seconds to display each screen before flashing the next
TIMEOUT = 5

def monitor_output (iface):
  print('Received serial output: %s' % iface.readline())

def user_interface(port='/dev/ttyUSB0'):
  iface = ArduinoInterface(port=port)
  patman = PatternManager()

  monitor = Thread(target=monitor_output, args=(iface,))
  monitor.start()

  while True:
    # gets the weather, then the screens for it
    icons = weather.get_icons()

    for icon_set in icons:
      pattern = patman.getPatterns(icon_set)
      iface.setPattern(pattern)

      # this is python, we can sleep without causing danger
      sleep(TIMEOUT)

  monitor.join()

if __name__ == '__main__':
  port = input('Enter Arduino serial port (defaults to /dev/ttyUSB0): ')
  if len(port) < 1:
    port = '/dev/ttyUSB0'
  user_interface(port)
