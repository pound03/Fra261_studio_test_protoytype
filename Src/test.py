class settime:
    def __init__(self,hour=0,min=0,sec=0):
        self.hour=hour
        self.min=sec
        self.min=sec
        self.time_count=0
        self.error=0
    def inputtime(self,x=""):
        spilit_text1=x.split(".")
        spilit_text2=x.split(",")
        spilit_text3=x.split(" ")
        if(len(spilit_text1)>=len(spilit_text2) and len(spilit_text1)>=len(spilit_text3)):
            spilit_text=spilit_text1
        elif(len(spilit_text2)>=len(spilit_text1) and len(spilit_text2)>=len(spilit_text3)):
            spilit_text=spilit_text2
        else:
            spilit_text=spilit_text3

        if(len(spilit_text)==1):
            self.time_count=int(spilit_text[0])*60*60
        elif(len(spilit_text)==2):
            self.time_count=int(spilit_text[0])*60*60+int(spilit_text[1])*60
        elif(len(spilit_text)==3):
            self.time_count=int(spilit_text[0])*60*60+int(spilit_text[1])*60+int(spilit_text[2])
        else:
            self.error=1
    def printleft(self,time_now):
        self.hour=round((self.time_count-time_now)//(60*60))
        self.min=round(((self.time_count-time_now-self.hour*60*60)//60))
        self.sec=round((self.time_count-time_now)%(60))

        hour_print = str(self.hour)
        if(self.min<=9):
            min_print= " : 0"+str(self.min)
        else:
            min_print = " : "+str(self.min)
        if(self.sec<=9):
            sec_print= " : 0"+str(self.sec)
        else:
            sec_print = " : "+str(self.sec)

        print_word = hour_print+min_print+sec_print
        return print_word

pound=settime()
pound.inputtime("12,12,3")
print(pound.printleft(100))