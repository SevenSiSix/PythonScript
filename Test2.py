'''Libraries importeren'''
import RPi.GPIO as GPIO 
import time
import threading as Thread
#-----------------------------------------
'''GPIO Modes instellen'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#-----------------------------------------
'''Variabeles voor de GPIO-Pins'''
pinAvooruit = 10
pinAachteruit = 9
pinBvooruit = 8
pinBachteruit = 7
echoOutput = 17
echoInput = 18
lichtinput = 25
led1 = 22
led2 = 23
#----------------------------------------
'''Frequentie van de wielen'''
Frequency = 22
'''Percentage dat de banden gebruikt worden'''
DutyCycleA = 27
DutyCycleB = 28
Stop = float(0.0000000)
#----------------------------------------
'''Set the GPIO Pin mode to be Output'''
GPIO.setup(pinAvooruit, GPIO.OUT)
GPIO.setup(pinAachteruit, GPIO.OUT)
GPIO.setup(pinBvooruit, GPIO.OUT)
GPIO.setup(pinBachteruit, GPIO.OUT)

GPIO.setup(echoOutput, GPIO.OUT)
GPIO.setup(echoInput, GPIO.IN)

GPIO.setup(lichtinput, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
#----------------------------------------
'''Andere variabelen'''
Grens_afstand = 22
achteruit_tijd = 0.5
omdraai_tijd = 0.6
Uturn_tijd = 0.7
Rondje_draaien = 8
#----------------------------------------
'''GPIO naar PWM-software naar frequentie in Hertz'''
pwmpinAvooruit = GPIO.PWM(pinAvooruit, Frequency)
pwmpinAachteruit = GPIO.PWM(pinAachteruit, Frequency)
pwmpinBvooruit = GPIO.PWM(pinBvooruit, Frequency)
pwmpinBachteruit = GPIO.PWM(pinBachteruit, Frequency)
#----------------------------------------
'''De software starten waarbij de auto stil zal staan'''
pwmpinAvooruit.start(Stop)
pwmpinAachteruit.start(Stop)
pwmpinBvooruit.start(Stop)
pwmpinBachteruit.start(Stop)
#---------------------------------------
'''stop functie'''
def stop():
	pwmpinAvooruit.ChangeDutyCycle(Stop)
	pwmpinAachteruit.ChangeDutyCycle(Stop)
	pwmpinBvooruit.ChangeDutyCycle(Stop)
	pwmpinBachteruit.ChangeDutyCycle(Stop)
#---------------------------------------
'''Vooruit rij functie'''
def Vooruit():
	pwmpinAvooruit.ChangeDutyCycle(DutyCycleA)
	pwmpinAachteruit.ChangeDutyCycle(float(0))
	pwmpinBvooruit.ChangeDutyCycle(DutyCycleB)
	pwmpinBachteruit.ChangeDutyCycle(Stop)
#---------------------------------------
'''Achteruit rij functie'''
def Achteruit():
	pwmpinAvooruit.ChangeDutyCycle(Stop)
	pwmpinAachteruit.ChangeDutyCycle(DutyCycleA)
	pwmpinBvooruit.ChangeDutyCycle(Stop)
	pwmpinBachteruit.ChangeDutyCycle(DutyCycleB)
#--------------------------------------
'''Links afslaan'''
def Links():
	pwmpinAvooruit.ChangeDutyCycle(Stop)
	pwmpinAachteruit.ChangeDutyCycle(DutyCycleA)
	pwmpinBvooruit.ChangeDutyCycle(DutyCycleB)
	pwmpinBachteruit.ChangeDutyCycle(Stop)
#--------------------------------------
'''Rechts afslaan'''
def Rechts():
	pwmpinAvooruit.ChangeDutyCycle(DutyCycleA)
	pwmpinAachteruit.ChangeDutyCycle(Stop)
	pwmpinBvooruit.ChangeDutyCycle(Stop)
	pwmpinBachteruit.ChangeDutyCycle(DutyCycleB)
#--------------------------------------
'''Meting maken'''
def Meting():
	GPIO.output(echoOutput, True)
	time.sleep(0.00001)
	GPIO.output(echoOutput, False)
	StartTime = time.time()
	StopTime = StartTime

	while GPIO.input(echoInput)==0:
		StartTime = time.time()
		StopTime = StartTime

	while GPIO.input(echoInput)==1:
        	StopTime = time.time()
        if StopTime-StartTime >= 0.04:
			print("Hold on there!  You're too close for me to see.")
			StopTime = StartTime

    	ElapsedTime = StopTime - StartTime
    	Afstand = (ElapsedTime * 34300)/2

    	return Afstand
#-------------------------------------
'''Functie die true geeft als de sensor een 1 geeft'''
def Dichtbij(localGrens_afstand):
	Afstand = Meting()

	print("Grens_afstand: "+str(Afstand))
	if Afstand < localGrens_afstand:
		return True
	else:
		return False
#------------------------------------
'''Functie die een Uturn maakt'''
def Uturn():
	#Klein stukje achteruit
	print("Achteruit")	
	Achteruit()
	time.sleep(achteruit_tijd)
	stop()

	#Naar rechts
    	print("Rechts")
    	Rechts()
    	time.sleep(omdraai_tijd)
    	stop()	
	#Vooruit
	print("Vooruit")
	Vooruit()
	time.sleep(Uturn_tijd)
	stop()
	
	#Naar rechts
    	print("Rechts")
    	Rechts()
    	time.sleep(omdraai_tijd)
    	stop()
#------------------------------------
'''Witte stip vinden'''
def RijdtoverZwart():
	if GPIO.input(lichtinput) == 0:
		return True
	else:
		return False
#-------------------------------------
'''Sirene maken'''
class sirene(Thread):
	def Sirene():
		GPIO.output(led1, 1)
		time.sleep(0.5)
		GPIO.output(led1, 0)
		GPIO.output(led2, 1)
		time.sleep(0.5)
		GPIO.output(led2, 0)
#---------------------------------------
'''Gevonden!'''
def Gevonden():
	if RijdtoverZwart == True:
		Sirene()
		Links()
		time.sleep(rondje_draaien)
		Rechtdoor()
		time.sleep(0.7)


'''Try-line om de volgorde van handelen te vertellen'''
try:
	GPIO.output(echoOutput, False)
	time.sleep(0.1)
	#Herhalen van de commands
    	while True:
		Vooruit()
        	time.sleep(0.1)
        	if Dichtbij(Grens_afstand):
            		stop()
            		Uturn()
		elif RijdtoverZwart():
			stop()
			Sirene()
			Gevonden()
			
	# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
	GPIO.cleanup()
#------------------------------------
