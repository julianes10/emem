import serial

ser = serial.Serial(
  port='/dev/rfcomm0',\
  baudrate=9600,\
  parity=serial.PARITY_NONE,\
  stopbits=serial.STOPBITS_ONE,\
  bytesize=serial.EIGHTBITS,\
  timeout=10)

print("connected to: " + ser.portstr)
count=1

while True:
  line = ser.readline()
  print("RX: " + line)
  ser.write("GRACIAS")

ser.close()
