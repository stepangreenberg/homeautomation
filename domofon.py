#timers for guest mode and in advance mode ?
#guest_mode Ответ ботом домофон в гостевом режиме. 
#30 минут - на стороне сервера, и подобное тож внеш память
#add tesmode for timers

import urequests
import utime
import mcron
from machine import RTC
import urequests
from time import sleep
import machine
from ntptime import settime
import network

rtc=RTC()
adc = machine.ADC(0)
ssid = "5th_hufflepuff"
ssid2 = "5th_bignumbers"
ssid3 = "5th_moominvalley"
passw = "100500100"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid3, passw)
sleep(5)
settime()

mcron.init_timer()

pin = machine.Pin(2, machine.Pin.OUT)
pin2 = machine.Pin(16, machine.Pin.OUT)
pin2.off()
pin.off()
sleep(1)
pin.on()

def reset(callback_id, current_time, callback_memory):

	machine.reset()

mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, 1800), 'half_hour', reset)

def nothing():

	pass

def open_usual():
	pin.on()
	pin2.off()
	sleep(16)
	pin.off()
	pin2.on()
	response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
	response.close()

def open_guestmode():

	pass

def read_call_pin():
	if adc.read()>100:
		open_usual()
		mcron.remove("read_call_pin")

def wait_for_a_call():

	mcron.insert(mcron.PERIOD_MINUTE, range(0, mcron.PERIOD_MINUTE, 1), 'read_call_pin', read_call_pin)

def update():
	r = urequests.get("https://raw.githubusercontent.com/stepangreenberg/homeautomation/master/domofon.py")
	rtext = r.text
	r.close()
	with open("boot.py","w") as f:
		f.write(rtext)
	machine.reset()

def get_code():
	response = urequests.get("https://api.thingspeak.com/channels/1204431/feeds.json?api_key=0Q99T4THA5P1COUB&results=1")
	rt = response.text
	response.close()

	feed_val = ujson.loads(rt)
	btn_val = feed_val["feeds"][0]["field1"]
	btn_val_int = int(btn_val)
	return btn_val_int

def guest_mode_on():

	pass

def guest_mode_off():

	pass

while True:
	run = {0: nothing, 1: open_usual, 100: update, 101: wait_for_a_call, 102: guest_mode_on, 103: guest_mode_off}
	run[get_code()]()
