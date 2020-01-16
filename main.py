import tkinter       #Tkinter is the standard GUI library for Python #inbuild
import cv2           #OpenCV-Python is a library of Python bindings designed to solve computer vision problems #pip install opencv-python
from PIL import Image,ImageTk       #Python Imaging Library is a free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats
                                    #The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage objects from PIL images.
                                    #pip install pillow

from functools import partial       #this is because we cannot pass argument in function within command of btn
import threading                    #due to thread, program is not get blocked and will change images on gui
import imutils
import time

stream= cv2.VideoCapture("Clip.mp4")
def play(speed):
    print(f"You clicked on play. Speed is {speed} ")
    #Play the video in reverse or forward mode
    frame1=stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)   #eg frames 100-2 =98, 100+2 =102
    grabbed,frame= stream.read()

    if not grabbed:     #if video gets end
        exit()

    frame= imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) #to convert any video into resize
    frame=ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    canvas.create_text(200,50,fill='red',font="Times 26 bold", text="Decision Pending")



def pending(decision):
    #1.display decision pending image
    frame=cv2.cvtColor(cv2.imread("Decision.jpg"),cv2.COLOR_BGR2RGB)
    frame= imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) #to convert any image into resize
    frame=ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    #2.wait for 1sec
    time.sleep(1)

    #3.display sponsor image
    frame=cv2.cvtColor(cv2.imread("Sponsor.jpg"),cv2.COLOR_BGR2RGB)
    frame= imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) #to convert any image into resize
    frame=ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    #4.wait for 1.5sec
    time.sleep(1.5)

    #5.display out/not_out image
    if decision == 'out':
        decisionImg="Out.jpg"
    else:
        decisionImg="Not_out.jpg"
    frame=cv2.cvtColor(cv2.imread(decisionImg),cv2.COLOR_BGR2RGB)
    frame= imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT) #to convert any image into resize
    frame=ImageTk.PhotoImage(image=Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
    

def out():
    thread=threading.Thread(target=pending,args=("out",)) #, is important
    thread.daemon=1 #keep as daemon program
    thread.start()
    print("you are out")

def not_out():
    thread=threading.Thread(target=pending,args=("not out",))
    thread.daemon=1
    thread.start()
    print("you are  not out")


 #dimensions for frame, caps because constant.
SET_WIDTH = 620
SET_HEIGHT= 350

#tkinter GUI starts here
window=tkinter.Tk()      #creating frame
window.title("DRS SYSTEM")
cv_img=cv2.cvtColor(cv2.imread("DRS.jpg"),cv2.COLOR_BGR2RGB) #give the file name, color code 3
canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT) #created just a canvas 1
photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img)) #read image in form array as it is cv image. 2
image_on_canvas = canvas.create_image(0,0,ancho=tkinter.NW,image=photo)#make it into canvas 4
canvas.pack()       #jus pack 5


#buttons to control playback
#(to learn more abt tkinter www.effbot.com search google as tkinter as tkinter docs)

btn = tkinter.Button(window,text="<<Previous FAST",width=50,command=partial(play,-25))
btn.pack()

btn = tkinter.Button(window,text="<<<<Previous SLOW",width=50,command=partial(play,-2))
btn.pack()

btn = tkinter.Button(window,text="Next SLOW>>>>",width=50,command=partial(play,2))
btn.pack()

btn = tkinter.Button(window,text="Next FAST>>",width=50,command=partial(play,25)) #command will take it jus play.. due to partial module we can do this.
btn.pack()

btn = tkinter.Button(window,text="Give OUT",width=50,command=out)
btn.pack()

btn = tkinter.Button(window,text="Give NOT OUT",width=50,command=not_out)
btn.pack()

window.mainloop()