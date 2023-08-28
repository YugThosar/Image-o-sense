import tkinter as tk
import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import colorchooser
from tkinter.filedialog import askopenfile
from wand.image import Image as WI
from PIL import Image, ImageTk

face=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Create an instance of tkinter frame
win = tk.Tk()
win.title('Image-O-Sense')
win.geometry("700x550")
clicked=tk.StringVar()

#Load the image
def View():
    cv2.imshow('Image',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def colorpicker():
    color_code=colorchooser.askcolor(title="choose the tint")
    # print(color_code)
    global im
    color_code=color_code[:-1]
    # im.tint(color="yellow",alpha=color_code)
    # im.save(im)
    red=np.full((im.shape),color_code,np.uint8)
    new_img=cv2.bitwise_or(im,red)   
    im=new_img
    return im    
    # color_code=color_code[:-1]
    # color_BGR=color_code[::-1]
    # im_hsv1=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    # result=cv2.bitwise_and(im_hsv1,im_hsv1,mask=color_BGR)
    
    



def SaveImage():
    global im
    print('save button is clicked')
    f_types = [('*.png', '*.jpg')]
    # nametosave=tk.Entry()
    # nametosave.grid(row=25,column=7)
    # name=nametosave.get()
    
    imagetosave=filedialog.asksaveasfilename(filetypes=f_types,defaultextension="*.jpg")
    cv2.imwrite(os.path.abspath(imagetosave),im)

def show():
    global im
    filter_label=tk.Label(win,text=clicked.get()).grid(row=40,column=10)
    
    if clicked.get() == "Monochrome":
        im_filtered=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        im=im_filtered
        return im
    elif clicked.get() == "HSV":
        im_hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
        im=im_hsv  
        return im
    elif clicked.get() == "YUV":
        im_tinted=cv2.cvtColor(im,cv2.COLOR_BGR2YUV)   
        im=im_tinted
        return im 
def display():
    global im
    w1=int(w.get())
    h1=int(h.get())
    im=cv2.resize(img,(w1,h1))
    
    
    drop=tk.OptionMenu(win,clicked,"Monochrome","HSV","YUV")
    drop.grid(row=28,column=8,padx=10,pady=10)
    filter_button=tk.Button(win,text="Show Selection",command=show).grid(row=35,column=8)
    b2=tk.Button(win,text='Preview',width=25,command=View)
    b2.grid(row=25,column=8)
    filter_button=tk.Button(win,text="Choose Tint",command=colorpicker).grid(row=45,column=8)


    
def OpenFile():
    global img,w,h
    f_types = [('*.png', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img=cv2.imread(filename=filename)
    w=tk.Entry(win,width=40)
    w.grid(row=10,column=8)
    h=tk.Entry(win,width=40)
    h.grid(row=12,column=8)

    Validate_width=tk.Button(win,text="Submit",width=30,command=display)
    Validate_width.grid(row=14,column=8)
    if display==True:
        w1=int(w.get())
        h1=int(h.get())
        
    # imgtk = ImageTk.PhotoImage(image=im)
    # label=tk.Label(win, image= imgtk).pack()
def FaceRecog():
    global im
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=face.detectMultiScale(gray,1.06,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),[0,255,0],1)
        roi_gray=gray[y:y+w,x:x+w]
        roi_color=im[y:y+h,x:x+w]
        # analyze=DeepFace.analyze(roi_color,actions=['emotion'])
        # print(analyze)
        View()
#Rearrange colors
# blue,green,red = cv2.split(img)
# img = cv2.merge((red,green,blue))
# im = Image.fromarray(img)
b1= tk.Button(win,text='Select Image',width=25,command=OpenFile)
b1.grid(row=5,column=10,padx=10,pady=10)

save_button=tk.Button(win,text='Save Image',width=30,command=SaveImage)
save_button.grid(row=30,column=8)

FaceDetect=tk.Button(win,text="Check Human Face",width=30,command=FaceRecog).grid(row=30,column=11,padx=15,pady=15)


#Create a Label to display the image

win.mainloop()