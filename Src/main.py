import ctypes
from os import stat
from win32api import GetSystemMetrics
import win32api
import pygame
from ctypes import wintypes
import serial

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
savedpos = win32api.GetCursorPos()

pygame.init()
screen = pygame.display.set_mode((width*5/10, height*4/10))

pygame.display.set_caption("Stand up please!!!")
icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)

default_color_active=pygame.Color(248,203,173)
default_color_passive=pygame.Color(229,240,255)

clock = pygame.time.Clock()
FPS=20
count_sec=0
sec_loop=0

hwnd = pygame.display.get_wm_info()['window']
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]



soundObj = pygame.mixer.Sound("sound_project.mp3")

class settime:
    def __init__(self,hour=0,min=0,sec=0):
        self.hour=hour
        self.min=min
        self.min=sec
        self.time_count=0
        self.error=0
    def inputtime(self,x="",digit=0):
        spilit_text1=x.split(".")
        spilit_text2=x.split(":")
        spilit_text3=x.split(",")
        if(len(spilit_text1)>=len(spilit_text2) and len(spilit_text1)>=len(spilit_text3)):
            spilit_text=spilit_text1
        elif(len(spilit_text2)>=len(spilit_text1) and len(spilit_text2)>=len(spilit_text3)):
            spilit_text=spilit_text2
        else:
            spilit_text=spilit_text3

        if(len(spilit_text)==1):
            self.time_count=int(spilit_text[0])*60
        elif(len(spilit_text)==2):
            self.time_count=int(spilit_text[0])*60*60+int(spilit_text[1])*60
        elif(len(spilit_text)==2):
            self.time_count=int(spilit_text[0])*60*60+int(spilit_text[1])*60+int(spilit_text[2])
        else:
            self.error=1
    def printleft(self,time_now):
        self.hour=round((self.time_count-time_now)//(60*60))
        self.min=round(((self.time_count-time_now-self.hour*60*60)//60))
        self.sec=round((self.time_count-time_now)%(60))

        if(self.hour<=9):
            hour_print= "0"+str(self.hour)
        else:
            hour_print = ":"+str(self.hour)

        if(self.min<=9):
            min_print= ":0"+str(self.min)
        else:
            min_print = ":"+str(self.min)
        if(self.sec<=9):
            sec_print= ":0"+str(self.sec)
        else:
            sec_print = ":"+str(self.sec)

        print_word = hour_print+min_print+sec_print
        return print_word
    def print_time(self):
        self.hour=round((self.time_count)//(60*60))
        self.min=round(((self.time_count-self.hour*60*60)//60))
        self.sec=round((self.time_count)%(60))

        if(self.hour<=9):
            hour_print= "0"+str(self.hour)
        else:
            hour_print = ":"+str(self.hour)
            
        if(self.min<=9):
            min_print= ":0"+str(self.min)
        else:
            min_print = ":"+str(self.min)

        print_word = hour_print+min_print
        return print_word
    def that_time(self):
        if(self.hour+self.min+self.sec==0):
            return True
        else:
            return False


class InputText_BOX:
    def __init__(self,size,inputText,boxpos=[0,0,50,20],that_are_button=0,want_labbel=0,coloractive_input=default_color_active,coloractive_passive=default_color_passive,disX = 3,disY = 3,colorText = [0,0,0]):
        self.size = size
        self.Font = pygame.font.Font("calibri.ttf", self.size)
        self.text = inputText
        self.logic_button = that_are_button
        self.logic_labbel = want_labbel
        self.boxpos = boxpos
        self.rec = pygame.Rect(boxpos[0], boxpos[1],boxpos[2],boxpos[3])
        self.color= [coloractive_passive,coloractive_input]
        self.state= 0
        self.disX = disX
        self.disY= disY
        self.colorText = colorText

    def draw(self,screen_input):
        if(not self.logic_labbel):
            pygame.draw.rect(screen_input, self.color[self.state], self.rec)

        if(self.text!=""):
            text_surface = self.Font.render(self.text, True, pygame.Color(self.colorText))
            screen.blit(text_surface, (self.rec.x+self.disX, self.rec.y+self.disY))

    def update(self,event_input):
        if self.logic_button:
            self.state = False
        if self.rec.collidepoint(event_input.pos):
            self.state = not self.state

    def new_word(self,event_input):
        if(self.state):
            time_Confirm_label.text = ""
            if event_input.key == pygame.K_BACKSPACE:
  
                self.text = self.text[:-1]
            else:
                self.text += event.unicode


class InputPicture:
    def __init__(self,filePic,sizePic,posPic):
        self.filePic = filePic
        self.sizePic = sizePic
        self.posPic = posPic
    def showPic(self):
        pic = pygame.transform.scale(pygame.image.load(self.filePic),self.sizePic)
        screen.blit(pic,self.posPic)


time_len= settime()
time_len.inputtime("1.30")
time_snooze = settime()
time_snooze.inputtime("10")
time_for_afk=60*5

check_list=[[],[],[],[],[],[],[]]
new_word_list=[[],[],[],[],[],[],[]]
draw_list=[[],[],[],[],[],[],[]]
showPic_list = [[],[],[],[],[],[],[]]
state = 0
first_time=1
count = 0
that_afk=0

state_bluethooth_2=0
bluethooth_open=0
data_from_blue="1"
error_bluethooth_stack=0
stop_count=0
count_blue=0

if(True):
    Main_butSetting = InputText_BOX(40,"",[(width*5/10-80)*8/10,(height*4.5/10-180)*1/10,200,60],1,1)
    draw_list[0].append(Main_butSetting)
    check_list[0].append(Main_butSetting)
    new_word_list[0].append(Main_butSetting)

    Main_butStart = InputText_BOX(40,"",[(width*5/10-205)*1/2,(height*4.5/10+78)*6/10,200,60],1,1)
    draw_list[0].append(Main_butStart)
    check_list[0].append(Main_butStart)
    new_word_list[0].append(Main_butStart)

    main_picture = InputPicture("main picture.png",[530,370],[(width*5/10-160)*1/7,(height*4.5/10-1000)*1/20])
    showPic_list[0].append(main_picture)
    
    start_picture = InputPicture("start button.png",[450,320],[(width*5/10-160)*2.3/9,(height*4.5/10-150)*6/10])
    showPic_list[0].append(start_picture)

    setting_picture = InputPicture("setting button.png",[450,320],[(width*5/10)*1.1/2,(height*4.5/10-585)*6/10])
    showPic_list[0].append(setting_picture)
    # ---------------------------------------------

if(True):
    Blue_butmain = InputText_BOX(20,"",[(width*5/10+60)*8/10,(height*4.5/10-165)*1/10,66,65],1,1)
    draw_list[1].append(Blue_butmain)
    check_list[1].append(Blue_butmain)
    new_word_list[1].append(Blue_butmain)

    Blue_labbel = InputText_BOX(30,"Serial Port :",[(width*5/10-450)*4.5/20,(height*4.5/10)*2/10,160,50],1,1)
    draw_list[1].append(Blue_labbel)

    Blue_labbel3 = InputText_BOX(20,"",[(width*5/10)*10/20,(height*4.5/10)*3.5/10,160,50],1,1,colorText=[27,229,27])
    draw_list[1].append(Blue_labbel3)

    Blue_box = InputText_BOX(30,"COM",[(width*5/10-320)*1/2,(height*4.5/10-60)*2/10,140,60],1,0,disX=5,disY=18,colorText=[31,78,121])
    draw_list[1].append(Blue_box)
    check_list[1].append(Blue_box)
    new_word_list[1].append(Blue_box)

    Blue_labbel2 = InputText_BOX(18,"e.g. COM3 ",[(width*5/10-320)*1/2,(height*4.5/10)*1/3,160,30],1,1,colorText=[228,99,78])
    draw_list[1].append(Blue_labbel2)

    Blue_Confirm = InputText_BOX(20,"",[(width*5/10+200)*4/10,(height*4.5/10-215)*3.5/10,200,60],1,1)
    draw_list[1].append(Blue_Confirm)
    check_list[1].append(Blue_Confirm)

    Blue_labbel3 = InputText_BOX(20,"",[(width*5/10-160)*4/10+110,(height*4.5/10)*3.5/10,160,30],1,1)
    draw_list[1].append(Blue_labbel3)

    time_Confirm_label = InputText_BOX(20,"",[(width*5/10-160)*4/10+110,(height*4.5/10+200)*5/10,150,60],1,1)
    draw_list[1].append(time_Confirm_label)
    check_list[1].append(time_Confirm_label)
    new_word_list[1].append(time_Confirm_label)

    time_labbel = InputText_BOX(30,"Time :",[(width*5/10-360)*6.5/20,(height*4.5/10+100)*5/10,50,50],1,1)
    draw_list[1].append(time_labbel)

    time_box = InputText_BOX(30," 5.00 ",[(width*5/10-320)*1/2,(height*4.5/10+70)*5/10,140,60],1,0,disX=5,disY=18,colorText=[31,78,121])
    draw_list[1].append(time_box)
    check_list[1].append(time_box)
    new_word_list[1].append(time_box)


    Blue_labbel_eg = InputText_BOX(18,"HH:MM or MM ",[(width*5/10-320)*1/2,(height*4.5/10+490)*1/3,160,30],1,1,colorText=[228,99,78])
    draw_list[1].append(Blue_labbel_eg)

    time_Confirm = InputText_BOX(20,"",[(width*5/10-205)*6/10+50,(height*4.5/10+75)*5/10,150,60],1,1)
    draw_list[1].append(time_Confirm)
    check_list[1].append(time_Confirm)



    back_picture = InputPicture("back button.png",[310,210],[(width*5/10+220)*1.1/2,(height*4.5/10-480)*6/10])
    showPic_list[1].append(back_picture)

    bluetooth_picture = InputPicture("bluetooth button.png",[450,320],[(width*5/10-250)*1/2,(height*4.5/10-760)*2/10])
    showPic_list[1].append(bluetooth_picture)

    save_picture = InputPicture("save button.png",[450,300],[(width*5/10-350)*1/2,(height*4.5/10+150)*2/10])
    showPic_list[1].append(save_picture)

if(True):
    cout_butCancle = InputText_BOX(40,"",[(width*2/10+30)*1/4,(height*4/10+120)*5/10,150,60],1,1)
    draw_list[2].append(cout_butCancle)
    check_list[2].append(cout_butCancle)
    new_word_list[2].append(cout_butCancle)

    time_text_min = InputText_BOX(60,"",[(width*2/10)*15/100,(height*4/10+800)*10/100,160,50],1,1,colorText=[31,78,121])
    draw_list[2].append(time_text_min)
    check_list[2].append(time_text_min)
    new_word_list[2].append(time_text_min)

    cancle_picture = InputPicture("cancle button.png",[450,300],[(width*2/10-680)*1/4,(height*4/10-130)*5/10])
    showPic_list[2].append(cancle_picture)

    remaining_picture = InputPicture("remaining time text.png",[450,320],[(width*2/10-780)*1/4,(height*4/10-600)*5/10])
    showPic_list[2].append(remaining_picture)

    # ---------------------------------------------

if(True):

    alert_butOK = InputText_BOX(20,"",[(width*2/10+410)*1/8,(height*4/10+15)*5/10,150,60],1,1)
    draw_list[3].append(alert_butOK)
    check_list[3].append(alert_butOK)
    new_word_list[3].append(alert_butOK)

    alert_butSNOOZE = InputText_BOX(20,"",[(width*2/10-195)*6/8,(height*4/10+180)*5/10,150,60],1,1)
    draw_list[3].append(alert_butSNOOZE)
    check_list[3].append(alert_butSNOOZE)
    new_word_list[3].append(alert_butSNOOZE)

    alarm_picture = InputPicture("alarm picture.png",[400,250],[(width*5/10-1100)*1/7,(height*4.5/10-1000)*1/20])
    showPic_list[3].append(alarm_picture)

    snooze_picture = InputPicture("snooze button.png",[450,300],[(width*2/10-680)*1/4,(height*4/10-70)*5/10])
    showPic_list[3].append(snooze_picture)

    stand_picture = InputPicture("stand up button.png",[450,300],[(width*2/10-680)*1/4,(height*4/10-230)*5/10])
    showPic_list[3].append(stand_picture)

if(True):
    snooze_butCancle = InputText_BOX(40,"",[(width*2/10+30)*1/4,(height*4/10+120)*5/10,150,60],1,1)
    draw_list[4].append(snooze_butCancle)
    check_list[4].append(snooze_butCancle)
    new_word_list[4].append(snooze_butCancle)

    snooze_text_min = InputText_BOX(60,"123",[(width*2/10)*15/100,(height*4/10+800)*10/100,160,50],0,1,colorText=[31,78,121])
    draw_list[4].append(snooze_text_min)
    check_list[4].append(snooze_text_min)
    new_word_list[4].append(snooze_text_min)

    snooze_cancle_picture = InputPicture("cancle button.png",[450,300],[(width*2/10-680)*1/4,(height*4/10-130)*5/10])
    showPic_list[4].append(snooze_cancle_picture)

    snooze_remaining_picture = InputPicture("remaining time text.png",[450,320],[(width*2/10-780)*1/4,(height*4/10-600)*5/10])
    showPic_list[4].append(snooze_remaining_picture)

if(True):

    last_butOK = InputText_BOX(20,"",[(width*2/10+410)*1/8,(height*4/10+115)*5/10,150,60],1,1)
    draw_list[5].append(last_butOK)
    check_list[5].append(last_butOK)
    new_word_list[5].append(last_butOK)

    alarm_picture = InputPicture("alarm picture.png",[400,250],[(width*5/10-1100)*1/7,(height*4.5/10-600)*1/20])
    showPic_list[5].append(alarm_picture)

    last_stand_picture = InputPicture("stand up button.png",[450,300],[(width*2/10-680)*1/4,(height*4/10-130)*5/10])
    showPic_list[5].append(last_stand_picture)

if(True):

    Afk_pic = InputPicture("procrastination.png",[200,200],[(width*2/10-70)*1/4,(height*4/10-150)*5/10])
    showPic_list[6].append(Afk_pic)
    afk_labbel1 = InputText_BOX(32,"Away from keyboard",[(width)*1/100,(height*4/10)*1/10,160,50],1,1,colorText=[31,78,121])
    draw_list[6].append(afk_labbel1)
    afk_labbel2 = InputText_BOX(20,"Move mouse to reset",[(width)*4/100,(height*4/10)*2/10,160,50],1,1,colorText=[31,78,121])
    draw_list[6].append(afk_labbel2)
    

def main_screen():
    global first_time,state,that_afk
    if(first_time):
        user32.SetWindowPos(hwnd, 0, round(width*2.5/10), round(height*5.5/20), 0, 0, 0x0001)
        pygame.display.set_mode((width*5/10, height*4.5/10))
        first_time=0


    if(Main_butSetting.state):
        Main_butSetting.state= 0

        state=1
        first_time=1

    if(Main_butStart.state):
        Main_butStart.state= 0
        that_afk=0
        state=2
        first_time=1


    return None

def connecting():
    global data_from_blue,serial_mobile
    data_from_blue=serial_mobile.read()
    data_from_blue=data_from_blue.decode()
    print(data_from_blue)
    return None

def bluethooth():
    global first_time,state,state_open,state_bluethooth_2,bluethooth_open,error_bluethooth_stack,time_len
    if(first_time):
        user32.SetWindowPos(hwnd, 0, round(width*2.5/10), round(height*5.5/20), 0, 0, 0x0001)
        pygame.display.set_mode((width*5/10, height*4.5/10))
        first_time=0
        time_box.text = time_len.print_time()
        time_Confirm_label.text = "" 

    if(Blue_butmain.state):
        Blue_butmain.state=0
        state=0
        first_time=1

    if(Blue_Confirm.state and not bluethooth_open):
        global serial_mobile
        Blue_labbel3.text="Connenting....."

        serial_mobile = serial.Serial(
        port=Blue_box.text,\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0.1)
        print("connenting")
        bluethooth_open=1

    if(time_Confirm.state and sec_loop):
        
        time_len.inputtime(time_box.text)
        time_Confirm_label.text = "saved"
    
    return None

def coun():
    global first_time,state,count,sec_loop,savedpos,stop_count,time_len
    if(first_time):
        user32.SetWindowPos(hwnd, 0, round(width*8/10), round(height*6/10-70), 0, 0, 0x0001)
        pygame.display.set_mode((width*2/10, height*4/10))
        first_time=0
        time_text_min.text = time_len.printleft(0)
        if(state_bluethooth_2==2):
            serial_mobile.write(str(2).encode())

    if(cout_butCancle.state):
        cout_butCancle.state=0
        count = 0
        state=0
        first_time=1
        if(state_bluethooth_2==2):
            serial_mobile.write(str(1).encode())

    if(time_len.that_time()):
        count = 0
        state=3
        first_time=1

    if(sec_loop):
        count+=1
        time_text_min.text = time_len.printleft(count)

        if savedpos != Pos:
            stop_count = 0
            savedpos = Pos
        else:
            stop_count = stop_count + 1
            if stop_count == time_for_afk:
                state = 6
                stop_count=0
                first_time=1
                count = 0

                if(state_bluethooth_2==2):
                    serial_mobile.write(str(3).encode())
    return None

def alert():
    global first_time,state,state_bluethooth_2,serial_mobile
    user32.SetWindowPos(hwnd, 0, round(width*8/10), round(height*6/10-70), 0, 0, 0x0001)
    if(first_time):
        soundObj.play()
        pygame.display.set_mode((width*2/10, height*4/10))
        if(state_bluethooth_2==2):
            serial_mobile.write(str(4).encode())
        
        first_time=0
    if(alert_butOK.state):
        alert_butOK.state=0
        state=2
        first_time=1
        soundObj.stop()
    if(alert_butSNOOZE.state):
        alert_butSNOOZE.state=0
        state=4
        first_time=1
        soundObj.stop()
    if(state_bluethooth_2==2 and data_from_blue=="6"):
        alert_butOK.state=0
        state=2
        first_time=1
        soundObj.stop()
    if(state_bluethooth_2==2 and data_from_blue=="7"):
        alert_butOK.state=0
        state=4
        first_time=1
        soundObj.stop()

    return None

def snooze():
    global first_time,state,count,sec_loop,savedpos,stop_count,that_afk
    if(first_time):
        user32.SetWindowPos(hwnd, 0, round(width*8/10), round(height*6/10-70), 0, 0, 0x0001)
        pygame.display.set_mode((width*2/10, height*4/10))
        first_time=0
        snooze_text_min.text = time_snooze.printleft(0)
        if(state_bluethooth_2==2):
            serial_mobile.write(str(2).encode())

    if(snooze_butCancle.state):
        snooze_butCancle.state=0
        count = 0
        first_time=1
        state=0
        if(state_bluethooth_2==2):
            serial_mobile.write(str(1).encode())

    if time_snooze.that_time():
        count = 0
        state = 5
        first_time=1

    if(sec_loop):
        count+=1
        snooze_text_min.text = time_snooze.printleft(count)

        if savedpos != Pos:
            stop_count = 0
            savedpos = Pos
        else:
            stop_count = stop_count + 1
            if stop_count == time_for_afk:
                state = 0
                stop_count=0
                first_time=1
                that_afk=1
                if(state_bluethooth_2==2):
                    serial_mobile.write(str(3).encode())
    return None

def last():
    
    global first_time,state,serial_mobile,state_bluethooth_2
    user32.SetWindowPos(hwnd, 0, round(width*8/10), round(height*6/10-70), 0, 0, 0x0001)
    if(first_time):
        soundObj.play()
        pygame.display.set_mode((width*2/10, height*4/10))
        if(state_bluethooth_2==2):
            serial_mobile.write(str(5).encode())
        first_time=0
    if(last_butOK.state):
        alert_butOK.state=0
        state=0
        first_time=1
        soundObj.stop()
        if(state_bluethooth_2==2):
            serial_mobile.write(str(1).encode())
    if(state_bluethooth_2==2 and data_from_blue=="6"):
        alert_butOK.state=0
        state=2
        first_time=1
        soundObj.stop()
    return None

def afk1():
    global state,first_time
    if(first_time):
        user32.SetWindowPos(hwnd, -1, round(width*8/10), round(height*6/10-70), 0, 0, 0x0001)
        pygame.display.set_mode((width*2/10, height*4/10))
        first_time=0
        if(state_bluethooth_2==2):
            serial_mobile.write(str(3).encode())
    if(sec_loop):
        if savedpos != Pos:
            state = 2
            first_time=1
    return None

run = True
while run:
    screen.fill("white")
    Pos = win32api.GetCursorPos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            #* all will False
            for i in check_list[state]:
                i.update(event)
        
        if event.type == pygame.KEYDOWN:
            for i in new_word_list[state]:
                i.new_word(event)

    if(not run):
        break

    for i in draw_list[state]:
        i.draw(screen)
    
    for j in showPic_list[state]:
        j.showPic()

    if(bluethooth_open and sec_loop):
        connecting()
        if(data_from_blue == "0"):
            error_bluethooth_stack=0
            state_bluethooth_2=2
            Blue_labbel3.text="Connented"
        if(data_from_blue == ""):
            error_bluethooth_stack=error_bluethooth_stack+1
            state_bluethooth_2=1
            if(error_bluethooth_stack>5):
                Blue_labbel3.text="lost_connect"
    if(sec_loop):
        print("%d_%d" % (count_blue,error_bluethooth_stack))
    if(count_blue % 5 == 0 and error_bluethooth_stack < 5 and sec_loop and state_bluethooth_2==2):
        print("reset")
        serial_mobile.write("15".encode())

    if(state == 0):
        main_screen()
    elif(state==1):
        bluethooth()
    elif(state==2):
        coun()
    elif(state==3):
        alert()
    elif(state==4):
        snooze()
    elif(state==5):
        last()
    elif(state==6):
        afk1()


    pygame.display.update()
    count_sec=count_sec+1

    sec_loop=0
    if(count_sec==FPS):
        sec_loop=1
        count_sec=0
    if(sec_loop):
        count_blue=count_blue+1
    clock.tick(FPS)