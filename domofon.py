#BUG WHEN READ CALL PIN AND OPEN
#timers for guest mode and in advance mode ?
#guest_mode Ответ ботом домофон в гостевом режиме. 
#30 минут - на стороне сервера, и подобное тож внеш память
#add tesmode for timers
#добиваться смены режима функция, пока не станет цифра не ноль
#покрутить выше чувствительность
#сделать таймер чаще, через микропайтон
# ПУСТЬ КРУТИТСЯ НА МОЕМ СЕРВИСЕ. СЕРВЕРЕ ВСЕ.

import urequests
import utime
import mcron
from machine import RTC
import urequests
from time import sleep
import machine
from ntptime import settime
import network
import ujson

rtc=RTC()
adc = machine.ADC(0)
ssid = "5th_hufflepuff"
ssid2 = "5th_bignumbers"
ssid3 = "5th_moominvalley"
passw = "100500100"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)



try:
	wlan.connect(ssid3, passw)
	sleep(5)
	
	
	response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
	response_text = response.text
	response.close()

	if response_text == "0":
		sleep(16)
		response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
		response.close()

	
	
	
	
	settime()

	read_call_pin_timer_activated = False

	mcron.init_timer()

	#pin = machine.Pin(2, machine.Pin.OUT)
	pin2 = machine.Pin(16, machine.Pin.OUT)
	pin2.off()
	#pin.off()
	sleep(3)
	pin2.on()

	#def reset(callback_id, current_time, callback_memory):

		#machine.reset()

	#mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, 1800), 'half_hour', reset)

	def nothing():
		global read_call_pin_timer_activated
		print("trying nothing")
		if not read_call_pin_timer_activated:
			print("nothing")
		else:
			print("Sorry nothing, but read_call_pin_timer_activated")

		pass

	def open_usual():
		global read_call_pin_timer_activated
		print("trying open_usual")
		if not read_call_pin_timer_activated:
			#if not in waiting mode
			print("open_usual")
			#pin.on()
			pin2.off()
			sleep(16)
			#pin.off()
			pin2.on()
			response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
			response.close()
		else:
			print("Sorry, open_usual, but read_call_pin_timer_activated...")

			response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=101")
			response_text = response.text
			response.close()

			if response_text == "0":
				sleep(16)
				response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=101")
				response.close()

	def open_guestmode():
		global read_call_pin_timer_activated
		print("open_guestmode")

		pass

	def wait_for_a_call():
		global read_call_pin_timer_activated
		print("trying wait_for_a_call")
		if not read_call_pin_timer_activated:
			print("wait_for_a_call")
			read_call_pin_timer_activated = True
			mcron.insert(mcron.PERIOD_MINUTE, range(0, mcron.PERIOD_MINUTE, 1), 'read_call_pin', read_call_pin)
		else:
			print("Sorry, wait_for_a_call, but read_call_pin_timer_activated...")

	def read_call_pin(callback_id, current_time, callback_memory):
		global read_call_pin_timer_activated
		print("trying read_call_pin")

		adc_read = adc.read()
		print("adc value:")
		print(adc_read)
		print("end adc value.")

		if adc_read>35:
			print("open in read_call_pin")
			#pin.on()
			pin2.off()
			sleep(16)
			#pin.off()
			pin2.on()

			response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
			response_text = response.text
			response.close()

			if response_text == "0":
				sleep(16)
				response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
				response.close()
			mcron.remove("read_call_pin")
			read_call_pin_timer_activated = False

		else:

			print("adc less than xxx waiting...")



	def update():
		print("trying update")
		r = urequests.get("https://raw.githubusercontent.com/stepangreenberg/homeautomation/master/domofon.py")
		rtext = r.text
		r.close()
		with open("boot.py","w") as f:
			f.write(rtext)	
		print("end adc value.")

		response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
		response_text = response.text
		response.close()

		if response_text == "0":
			sleep(16)
			response = urequests.get("https://api.thingspeak.com/update?api_key=CZ1A7QIZN41BT072&field1=0")
			response.close()



		machine.reset()

	def guest_mode_on():
		global read_call_pin_timer_activated
		print("guest_mode_on")

		pass

	def guest_mode_off():
		global read_call_pin_timer_activated
		print("guest_mode_off")

		pass
	def check_adc():
		adc_read = adc.read()
		print("sending adc to telegram")
		adc_url = "https://api.telegram.org/bot1451623366:AAGK87XRO94slqmP3eMj2loqt4Nce10QaKI/sendMessage?chat_id=478011973&text=adc"
		print(1)

		response = urequests.get(adc_url)
		print(2)
		response_text = response.text
		print(3)
		response.close()
		print(4)

		

	def get_code():

		adc_read = adc.read()
		print("adc value:")
		print(adc_read)
		print("end adc value.")


		global read_call_pin_timer_activated
		print("get_code")
		response = urequests.get("https://api.thingspeak.com/channels/1204431/feeds.json?api_key=0Q99T4THA5P1COUB&results=1")
		rt = response.text
		response.close()

		feed_val = ujson.loads(rt)
		btn_val = feed_val["feeds"][0]["field1"]
		btn_val_int = int(btn_val)
		return btn_val_int

	while True:
		run = {0: nothing, 1: open_usual, 100: update, 101: wait_for_a_call, 102: guest_mode_on, 103: guest_mode_off, 104: check_adc}
		run[get_code()]()
except:
	machine.reset()
