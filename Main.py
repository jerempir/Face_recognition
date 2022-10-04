import os
from tkinter import *
from PIL import Image , ImageTk
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import tkinter
from pathlib import Path
import cv2 as cv
from collections import Counter
from tkinter import filedialog

def randpair(width, height):  # Функция присваивания рандомной пары чисел в диапазоне размера картинки
    x = randint(0, width)
    y = randint(0, height)
    return x, y

def maskmethod(image,image2, width, height, valueofpixels): # метод масок
    a = 0

    for i in range(1, valueofpixels):
        x, y = randpair(width - 1, height - 1) # рандомные координаты в отличие от первого метода одни для обоих картинок
        b = image.getpixel((x, y)) # находим цвет x1 y1 пикселя у 1 картинки
        c = image2.getpixel((x, y)) # находим цвет x1 y1 пикселя у 2 картинки
        a += (abs(b-c)) #находим разницу цветов, если изображения одинаковые,то разница будет минимальной
    return a

def allcalc(image,blocks): # метод гистограмм
    arrayimg = np.asarray(image)
    arrayimg = nptoarray(arrayimg)
    c = plt.hist(arrayimg, blocks)
    #plt.show()
    return c[0]

def comparehist(hist1,hist2):
    hist1 = np.float32(hist1)
    hist2 = np.float32(hist2)
    a = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL) # сравниваем гистограммы
    return a

def nptoarray(arr): # двухмерный массив в одномерныый
    returnarray = []
    for i in arr:
        for j in i:
            returnarray.append(j)
    return returnarray

def imagearr(image, width, height): # переводит картинку в массив
    arr = []
    for i in range(width):
        for j in range(height):
            arr.append((image.getpixel((i, j))))
    return arr

def allmask2(baseimg,testimg,width,height):  # попиксельно сравниваем два изображения, на выходе сумма разностей
    a = 0
    arr1 = imagearr(baseimg,width,height)
    arr2 = imagearr(testimg,width,height)
    for i in range(len(arr1)):
        a += abs(arr1[i]-arr2[i])
    return a

def doublemin(arr):
    findex = arr.index(min(arr))
    arr[findex] = 10000000
    sindex = arr.index(min(arr))
    return findex,sindex

def doublemax(arr):
    findex = arr.index(max(arr))
    arr[findex] = -10000000
    sindex = arr.index(max(arr))
    return findex,sindex

def numbers(string,n):
    i = n
    num = ''
    string = str(string)
    while string[i] != '.':
       num+=string[i]
       i+=1
    return int(num)

def numbers2(string,n):
    i = n
    num = ''
    string = str(string)
    while string[i] != ' ':
       num+=string[i]
       i+=1
    return int(num)

def vouting(mask1,mask2,resize1,resize2,hist1,hist2):
    arr =[]
    arr.append(mask1)
    arr.append(mask1)
    arr.append(mask2)
    arr.append(resize1)
    arr.append(resize1)
    arr.append(resize1)
    arr.append(resize2)
    arr.append(hist1)
    arr.append(hist1)
    arr.append(hist2)
    c = Counter(arr)
    return c

def showimage():
    global fln
    fln = filedialog.askopenfilename(initiald=os.getcwd(),title = 'select image file')
    img = Image.open(fln)
    #img.thumbnail((350,350))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img


def Main(imagepath):
    blocks10 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
                230, 240, 255]  # блоки для гистограммы
    blocks32 = [0, 32, 64, 96, 128, 160, 192, 224, 255]
    blocks8 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184,
               192, 200, 208, 216, 224, 232, 240, 248, 255]
    blocks = blocks32
    valueofpixels = 800  # кол-во рандомных пикселей
    images = []

    for txt_path in Path("venv/image/").glob("**/*.pgm"):
        images.append(txt_path)

    testImg = Image.open(imagepath)  # задаем переменную для Тестовой картинки

    width, height = testImg.size  # границы фоток
    resizedwidth = int(width * 0.25)
    resizedheight = int(height * 0.25)

    Alltesthist = allcalc(testImg, blocks)  # считаем гистограмму всех точек
    resizetestImg = testImg.resize((resizedwidth, resizedheight), Image.LANCZOS)  # масштабируем изображение

    resultofmask = []
    resultofallresizedmask = []
    resultofallhist = []

    for i in images:
        baseimg = Image.open(i)  # задаем переменную для базовой картинки
        resizedbaseimg = baseimg.resize((resizedwidth, resizedheight), Image.LANCZOS)  # меняем масштаб картинки

        mask = maskmethod(baseimg, testImg, width, height,
                          valueofpixels)  # 2 метод основанный на одинаковых рандомных точках
        resultofmask.append(
            mask)  # массив сравнений 2 метода содержит значение соответствия тестового изобр. с кажд. образцовой

        allresizedmask = allmask2(resizedbaseimg, resizetestImg, resizedwidth, resizedheight)
        resultofallresizedmask.append(allresizedmask)

        baseallhist = allcalc(baseimg, blocks)  # метод 4 строит гистограмму всех пикселейизображения
        compareall = comparehist(Alltesthist, baseallhist)
        resultofallhist.append(compareall)

    firstmaskindex, secondmaskindex = doublemin(resultofmask)
    firstmaskvalue = numbers(images[firstmaskindex], 11)
    secondmaskvalue = numbers(images[secondmaskindex], 11)
    print(firstmaskvalue, 'first value of mask')
    print(secondmaskvalue, 'second value of mask')

    firstresizeindex, secondresizeindex = doublemin(resultofallresizedmask)
    firstresizevalue = numbers(images[firstresizeindex], 11)
    secondresizevalue = numbers(images[secondresizeindex], 11)
    print(firstresizevalue, 'first value of resizedmask')
    print(secondresizevalue, 'second value of resizedmask')

    firsthistindex, secondhistindex = doublemax(resultofallhist)
    firsthistvalue = numbers(images[firsthistindex], 11)
    secondhistvalue = numbers(images[secondhistindex], 11)
    print(firsthistvalue, 'first value of hist')
    print(secondhistvalue, 'second value of hist')

    c = vouting(firstmaskvalue, secondmaskvalue, firstresizevalue, secondresizevalue, firsthistvalue, secondhistvalue)
    i = c.most_common(1)[0][0]
    bn = c.most_common(1)[0][1]
    nn = c.most_common(2)[1][1]
    if bn == nn:
        i = firstresizevalue
    print("answer=", i)

    if i == firstmaskvalue:
        path = firstmaskindex
    elif i ==secondmaskvalue:
        path = secondmaskindex
    elif i == firstresizevalue:
        path = firstresizeindex
    elif i == secondresizevalue:
        path = secondresizeindex
    elif i == firsthistvalue:
        path = firsthistindex
    elif i == secondhistvalue:
        path = secondhistindex
    global lbl2
    lbl2 = Label(root)
    path = images[path]

    img = Image.open(path)
    # img.thumbnail((350,350))
    img = ImageTk.PhotoImage(img)
    lbl2.configure(image=img)
    lbl2.image = img
    lbl2.pack()

def delete():
    lbl2.pack_forget()


root = Tk()
root.title('Faces')
frm = Frame(root)
frm.pack(side=BOTTOM,padx=15,pady=15)
lbl = Label(root)
lbl.pack()

btn = Button(frm,text = "Browse Image",command = showimage)
btn.pack(side=tkinter.LEFT)

btn2 = Button(frm,text = "Exit",command = lambda:exit())
btn2.pack(side=tkinter.LEFT,padx = 40)

btn3 = Button(frm,text = "Start",command = lambda:Main(fln))
btn3.pack(side=tkinter.LEFT,padx = 20)

btn4 = Button(frm,text = "Delete ",command = delete)
btn4.pack(side=tkinter.LEFT,padx = 20)

# Set the resolution of window
root.geometry("550x300")


root.mainloop()







