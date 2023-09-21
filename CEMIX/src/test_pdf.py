import barcode
from barcode import generate

# Generate a barcode with the desired data
data = "123456789"
code128 = barcode.get('code128', data, writer=barcode.writer.ImageWriter())

# Save the barcode image to a file
barcode_path = "barcode.png"
code128.save(barcode_path)


from escpos.printer import Serial

# Create a printer instance with your serial port settings
# Replace 'COM1' with your actual serial port name (e.g., '/dev/ttyS0' on Linux)
printer = Serial('USB003', baudrate=9600, timeout=5)

# Send the barcode image to the printer
printer.image(barcode_path)

# Cut the paper (if supported by your printer)
printer.cut()