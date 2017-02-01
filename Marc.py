'''IMPORTEREN VAN ALLE LIBRARY'S'''
import RPi.GPIO as GPIO
import time
import random
#---------------------------------------------------------

'''GPIO MODES OPZETTEN'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#---------------------------------------------------------

'''SETUP FOR PINS'''
pinLinksVooruit = 10
pinLinksAchteruit = 9
pinRechtsVooruit = 8
pinRechtsAchteruit = 7
lichtsensor = 25
outputafstandsensor = 17
inputechosensor = 18
lampje1 = 23
lampje2 = 22
#---------------------------------------------------------

'''GPIO IN/OUT-PUT'''
GPIO.setup(pinLinksVooruit, GPIO.OUT)
GPIO.setup(pinLinksAchteruit, GPIO.OUT)
GPIO.setup(pinRechtsVooruit, GPIO.OUT)
GPIO.setup(pinRechtsAchteruit, GPIO.OUT)
GPIO.setup(outputafstandsensor, GPIO.OUT)
GPIO.setup(inputechosensor, GPIO.IN)
GPIO.setup(lichtsensor, GPIO.IN)
#---------------------------------------------------------
'''FREQUENTIE VAN DE MOTORS'''
frequentie = 20
rondjesRechts = 30
rondjesLinks = 30
stop = 0
pwmMotorLinksVooruit = GPIO.PWM(pinLinksVooruit, frequentie)
pwmMotorLinksAchteruit = GPIO.PWM(pinLinksAchteruit, frequentie)
pwmMotorRechtsVooruit = GPIO.PWM(pinRechtsVooruit, frequentie)
pwmMotorRechtsAchteruit = GPIO.PWM(pinRechtsAchteruit, frequentie)
#---------------------------------------------------------
''' VARIABLES MAKEN'''
Hoedichtbij = 15.0
Achteruittijd = 0.5
Bochttijd = 0.75
Uturnrechtdoortijd = 0.5
#---------------------------------------------------------
'''ZET ALLE MOTORS UIT'''
def motorsUit():
	GPIO.output(pinLinksVooruit, 0)
	GPIO.output(pinLinksAchteruit, 0)
	GPIO.output(pinRechtsVooruit, 0)
	GPIO.output(pinRechtsAchteruit, 0)
#---------------------------------------------------------
'''RIJ VOORUIT'''
def rijVooruit():
	GPIO.output(pinLinksVooruit, 1)
	GPIO.output(pinLinksAchteruit, 0)
	GPIO.output(pinRechtsVooruit, 1)
	GPIO.output(pinRechtsAchteruit, 0)
#---------------------------------------------------------
'''RIJ ACHTERUIT'''
def rijAchteruit():
    	GPIO.output(pinLinksVooruit, 0)
    	GPIO.output(pinLinksAchteruit, 1)
    	GPIO.output(pinRechtsVooruit, 0)
    	GPIO.output(pinRechtsAchteruit, 1)
#---------------------------------------------------------
'''SLA LINKSAF'''
def Links():
	GPIO.output(pinLinksVooruit, 0)
	GPIO.output(pinLinksAchteruit, 1)
	GPIO.output(pinRechtsVooruit, 1)
    	GPIO.output(pinRechtsAchteruit, 0)
#---------------------------------------------------------
'''SLA RECHTSAF'''
def Rechts():
	GPIO.output(pinLinksVooruit, 1)
	GPIO.output(pinLinksAchteruit, 0)
	GPIO.output(pinRechtsVooruit, 1)
	GPIO.output(pinRechtsAchteruit, 0)
#---------------------------------------------------------
'''Functie voor het laten merken dat de stip gevonden is'''
def Gevonden():
	GPIO.output(pinLinksVooruit, 0)
	GPIO.output(pinLinksAchteruit, 1)
	GPIO.output(pinRechtsVooruit, 0)
	GPIO.output(pinRechtsAchteruit, 0)
	
	time.sleep(0.5)
#---------------------------------------------------------
'''functie voor het vinden van de witte stip'''
def Rijdtoverwittestip():
    if GPIO.input(pinLineFollower) == 1:
        return True
    else:
        return False
#---------------------------------------------------------
'''Het maken van een afstands afmeting'''
def Meting():
    GPIO.output(pinTrigger, True)
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    StartTime = time.time()
    StopTime = StartTime

    while GPIO.input(pinEcho)==0:
        StartTime = time.time()
        StopTime = StartTime

    while GPIO.input(pinEcho)==1:
        StopTime = time.time()

        if StopTime-StartTime >= 0.04:
            print("Hold on there!  You're too close for me to see.")
            StopTime = StartTime
            break

    ElapsedTime = StopTime - StartTime
    Distance = (ElapsedTime * 34300)/2

    return Distance
#---------------------------------------------------------
'''Geeft een true waarde als er een object in de buurt is'''
def Indebuurtvanobstakel(localHoedichtbij):
    Distance = Meting()

    print("Indebuurtvanobstakel: "+str(Distance))
    if Distance < localHoedichtbij:
        return True
    else:
        return False
#---------------------------------------------------------		
'''functie voor muur'''
def Uturn():
    # Naar achter
    print("Achteruit")
    rijAchteruit()
    time.sleep(Achteruittijd)
    motorsUit()

    # Maak een bocht naar rechts
    print("Bocht maken")
    Rechts()
    time.sleep(Bochttijd)
    motorsUit()
	
	#rechtdoor
	print("Rechtdoor")
	rijVooruit()
	time.sleep(Uturnrechtdoortijd)
	motorsUit()
	
	# Maak nog een bocht naar rechts
	print("Bocht maken")
    Rechts()
    time.sleep(Bochttijd)
    motorsUit()
#----------------------------------------------------------		
'''De try-line'''
try:
    # Set trigger to False (Low)
    GPIO.output(pinTrigger, False)

    # Allow module to settle
    time.sleep(0.1)

    #repeat the next indented block forever
    while True:
    Forwards()
    time.sleep(0.1)
    if IsNearObstacle(Hoedichtbij):
		StopMotors()
		AvoidObstacle()

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    GPIO.cleanup()
#-----------------------------------------------------------
