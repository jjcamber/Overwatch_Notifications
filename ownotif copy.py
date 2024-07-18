import pyautogui
from PIL import Image
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

carriers = {
	'att': '@mms.att.net',
	'tmobile':'@tmomail.net',
	'verizon': '@vtext.com',
	'sprint': '@page.nextel.com'
}

email = "@gmail.com"
passw = ""
phonenum = '@vtext.com'

# Function to check if a color is within an acceptable range of the target color
def is_color_similar(color1, color2, tolerance=30):
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

# Function to send an email
def send_email():
    global email, passw, phonenum
    text = MIMEText("Game found!")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, passw)
    server.sendmail(email, phonenum, text.as_string())
    server.quit()

# Function to monitor a pixel for a range of similar colors
def monitor_pixel(x, y, target_hex, tolerance=30):
    target_color = tuple(int(target_hex[i:i+2], 16) for i in (0, 2, 4))
    while True:
        screenshot = pyautogui.screenshot(region=(x, y, 1, 1))
        rgb_im = screenshot.convert('RGB')
        pixel_color = rgb_im.getpixel((0, 0))
        if is_color_similar(pixel_color, target_color, tolerance):
            # print("Similar color detected at the specified pixel.")
            send_email()
            break
        sleep(0.1)

# Pixel coordinates and target color
x_coordinate = 1845
y_coordinate = 1405
target_hex = "B3601F"

# Start monitoring the pixel
monitor_pixel(x_coordinate, y_coordinate, target_hex)
