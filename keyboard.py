import time
import RPi.GPIO as GPIO
from motor import Step_motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class keypad:
    
    def __init__(self,row1,row2,row3,row4,col1,col2,col3,col4):
        self.rows=[row1,row2,row3,row4]
        self.cols=[col1,col2,col3,col4]
        self.keys=[['1','2','3','A'],
               ['4','5','6','B'],
               ['7','8','9','C'],
               ['*','0','#','D']]
        for row_pin in self.rows:
            GPIO.setup(row_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

        for col_pin in self.cols:
            GPIO.setup(col_pin,GPIO.OUT)

    def get_key(self):
        key = 0
        for col_num,col_pin in enumerate(self.cols):
            GPIO.output(col_pin,1)
            for row_num,row_pin in enumerate(self.rows):
                if GPIO.input(row_pin):
                    key=self.keys[row_num][col_num]
            GPIO.output(col_pin,0)
        return key
if __name__=="__main__":
    #Inpassword=input("please set a 6-digit password for the lock")
    Inpassword='123456'
    motor=Step_motor(2,3,14,15)
    keyboard=keypad(12,16,20,21,6,13,19,26)
    Outpassword=''
    try:
        while(True):
            word =keyboard.get_key()
            time.sleep(0.2)
            word =keyboard.get_key()   
            if word:
                print(word)
                Outpassword += str(word)
                time.sleep(0.1)
                if len(Outpassword) == 6:
                    if Outpassword == Inpassword:
                        print('success to open the lock')
                        motor.forward(5,500)
                        
                        Outpassword=''
                        
                    else :
                        print('password wrong')
    finally:
        print('clean')
        GPIO.cleanup()
           
    
