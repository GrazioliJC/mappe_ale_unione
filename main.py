import os
from pathlib import Path
import time
import requests
import shutil
from PIL import Image
BASE_DIR = Path(__file__).resolve().parent
path = os.path.join(BASE_DIR, "img/")
#88 immagini x riga
#ultima img "http://www.asmilano.it/fast/iipsrv.fcgi?FIF=/opt/divenire/files/./tifs/05/37/537505.tif&jtl=7,4894"

img = "http://www.asmilano.it/fast/iipsrv.fcgi?FIF=/opt/divenire/files/./tifs/05/37/537505.tif&jtl=7,"
num = 0

def main():
    while True:
        decisione = input("Premi 1 per scaricare.\nPremi 2 per unire.\n")
        if decisione == "1":
            scarica()
            break
        elif decisione == "2":
            unisci()
            break

def scarica():
    global num, img
    while num <= 4894:
        link = img + str(num)
        name = str(num) + ".jpeg"
        immagini = os.listdir(r"img/")
        if name not in immagini:
            data = requests.get(link, stream=True)
            with open(r"img/" + name, 'wb') as f:
                shutil.copyfileobj(data.raw, f)
            f.close()
            print("Scaricato nr." + str(num))
            time.sleep(1.5)
        num += 1

def unisci():
    global row,index,temp
    row = 0
    first = True
    index = 0
    temp = 0
    while index <= 4894:
        print("Numero immagine: " + str(index) + "\n" + "Numero riga: " + str(row))
        print("Temp = " + str(temp))
        if temp <= 88:
            if first:
                mappa = os.path.join(path, str(index) + ".jpeg")
                mappa = Image.open(mappa)
                index += 1
                mappa2 = os.path.join(path, str(index) + ".jpeg")
                mappa2 = Image.open(mappa2)
                finale = os.path.join(os.path.join(path, "temp/", str(row) + ".jpeg"))
                concat_o(mappa, mappa2).save(finale)
                first = False
                index += 2
                temp += 2
            else:
                mappa = str(index) + ".jpeg"
                mappa = Image.open(os.path.join(path,mappa))
                mappona = Image.open((os.path.join(path, "temp/", str(row) + ".jpeg")))
                finale = os.path.join(os.path.join(path, "temp/", str(row) + ".jpeg"))
                concat_o(mappona,mappa).save(finale)
                temp += 1
                index += 1
        else:
            first = True
            row += 1
            temp = 0
            index -= 1

    print("Inizio y")
    immagini = os.listdir(os.path.join(path, "temp/"))
    numimg = len(immagini)
    index = 0
    first = True
    while index <= numimg:
        print("Nr riga: " + str(index))
        if first:
            mappa1 = str(index) + ".jpeg"
            mappa1 = Image.open(os.path.join(path, mappa1))
            index += 1
            mappa2 = str(index) + ".jpeg"
            mappa2 = Image.open(os.path.join(path, mappa1))
            finale = os.path.join(os.path.join(path, "temp/", "mappona.jpeg"))
            concat_y(mappa1, mappa2).save(finale)
            index += 2
        else:
            mappa1 = str(index) + ".jpeg"
            mappa1 = Image.open(os.path.join(path, mappa1))
            mappona = Image.open((os.path.join(path, "temp/","mappona.jpeg")))
            concat_o(mappona, mappa1).save(mappona)
            index += 1


def concat_o(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def concat_y(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

main()