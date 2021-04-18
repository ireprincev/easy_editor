
#создай тут фоторедактор Easy Editor!
from PIL import Image,ImageFilter
from PIL.ImageFilter import SHARPEN
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QMessageBox,QListWidget,QFileDialog
from PyQt5.QtGui import QPixmap
app = QApplication([])
wind = QWidget()
win = QLabel()
listt = QListWidget()
btn_dir = QPushButton("Папка")
btn1 = QPushButton("Лево")
btn2 = QPushButton("Право")
btn3 = QPushButton("Зеркало")
btn4 = QPushButton("Резкость")
btn5 = QPushButton("Размытие")
btn6 = QPushButton("Ч/Б")
btn7= QPushButton("Барельеф")
wind.resize(700,400)
wind.setWindowTitle("Easy Editor")
row = QHBoxLayout()
lh = QHBoxLayout()
lv1 = QVBoxLayout()
lv2 = QVBoxLayout()
lv2.addWidget(win)    
lh.addWidget(btn1)
lh.addWidget(btn2)
lh.addWidget(btn3)
lh.addWidget(btn4)
lh.addWidget(btn5)
lh.addWidget(btn6)
lh.addWidget(btn7)
lv2.addLayout(lh)
lv1.addWidget(btn_dir)
lv1.addWidget(listt)
row.addLayout(lv1)
row.addLayout(lv2)
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extensioins):
    m=[]
    for name in files:
        for ex in extensioins:
            if name.endswith(ex):
                m.append(name)
    return m
def showFilenamesList():
    extensions = ["jpeg","jpg","png"] #добавляет все а не jpg
    global workdir
    chooseWorkdir()
    filenames = os.listdir(workdir)
    names = filter(filenames,extensions)
    listt.clear()
    for name in names:
        listt.addItem(name)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "modie"
    def loadImage(self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def showImage(label,path):
        win.hide()
        pixmapimage = QPixmap(path)
        w,h = win.width(),win.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        win.setPixmap(pixmapimage)
        win.show()
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_emboss(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_sharp(self): #Почему вылетает?
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
wokimage = ImageProcessor()

def showChosenImage():
    if listt.currentRow() >=0:
        filename = listt.currentItem().text()
        wokimage.loadImage(filename)
        image_path = os.path.join(workdir,wokimage.filename)
        wokimage.showImage(image_path)

btn7.clicked.connect(wokimage.do_emboss)
btn6.clicked.connect(wokimage.do_bw)
btn5.clicked.connect(wokimage.do_blur)
btn3.clicked.connect(wokimage.do_flip)
btn4.clicked.connect(wokimage.do_sharp)
btn1.clicked.connect(wokimage.do_right)
btn2.clicked.connect(wokimage.do_left)
listt.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)
wind.setLayout(row)
wind.show()
app.exec()