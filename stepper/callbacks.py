import math
import time
import os, sys
import RPi.GPIO as GPIO
from HR8825 import HR8825
from PyQt5 import uic
from PyQt5.QtCore import QFile, QRegExp, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QMessageBox,QTableWidgetItem
from subThread import SubThread
import pygame
#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Joystick initialized
try:
    from XboxController import XBOX
    joystick = XBOX()
except:
    print('Joystick not connected.')
    pass
else:
    print('Joystick initialized.')

# stepper motors
stepperSF = HR8825(dir_pin=13, step_pin=19, enable_pin=26)
stepperSR = HR8825(dir_pin=10, step_pin=9, enable_pin=11)
stepperBF = HR8825(dir_pin=21, step_pin=20, enable_pin=16)
stepperBR = HR8825(dir_pin=5, step_pin=6, enable_pin=12)

#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================

class GUI(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setupWindow()
        self.setupStepper()
        self.setupSubThread()
        
        self.setupTimer()

        self.setupFileMenu()
        self.setupHelpMenu()
        

    def closeEvent(self,event):
        stepperSF.Stop()
        stepperSR.Stop()
        stepperBF.Stop()
        stepperBR.Stop()
        print("All stepper motors stopped and released.")
        self.thrd.stop()
        try:
            joystick
        except NameError:
            pass
        else:
            joystick.quit()
        event.accept()

    def setupWindow(self): 
        self.btn_runDirectMotor.clicked.connect(self.on_btn_runDirectMotor)
        self.btn_runCatheterPos.clicked.connect(self.on_btn_runCatheterPos)
        self.chb_joystick.toggled.connect(self.on_chb_joystick)

    def setupStepper(self):
        stepperSF.SetMicroStep('hardware')
        stepperSR.SetMicroStep('hardware')
        stepperBF.SetMicroStep('hardware')
        stepperBR.SetMicroStep('hardware')
        
    def setupSubThread(self):
        try:
            joystick
        except:
            self.thrd = SubThread(stepperSF,stepperSR,stepperBF,stepperBR)
        else:
            self.thrd = SubThread(stepperSF,stepperSR,stepperBF,stepperBR,joystick)
            
        self.thrd.finished.connect(self.finishSubThreadProcess)
        
    @pyqtSlot()
    def finishSubThreadProcess(self):
        print('Joystick is terminated.')
        
    def setupTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(6) # msec
        
    def update(self):
        try:
            joystick
        except NameError:
            pass
        else:
            joystick.update()

    def about(self):
        QMessageBox.about(self, "About Stepper",
                "<p>Model of <b>Small Stepper</b>: 28H30H0604A2 <br>" \
                "Model of <b>Big Stepper</b>: 42BYGH152-B-24DH </p>"   
                "<p align='right'>Jason</p>")

    def setupFileMenu(self):
        fileMenu = QMenu("&File", self)
        self.menuBar().addMenu(fileMenu)
        fileMenu.addAction("&Exit", QApplication.instance().quit, "Ctrl+Q")

    def setupHelpMenu(self):
        helpMenu = QMenu("&Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("&About", self.about)

    def on_btn_runDirectMotor(self): #The default step of the motor driver is 1/4 step ("010"), thus steps are multiplied by 4
        stepSF = self.spb_stepperSF.value()
        if stepSF:
            dirSF = 'backward' if stepSF>0 else 'forward'
            motionSF = 'moving forwards' if stepSF>0 else 'moving backwards'
            print('Stepper Small Front:',motionSF,abs(stepSF),'steps,',abs(stepSF)*1.8,'deg')
            stepperSF.TurnStep(Dir=dirSF, steps=abs(stepSF)*4, stepdelay = 0.001)
        
        stepSR = self.spb_stepperSR.value()
        if stepSR:
            dirSR = 'backward' if stepSR>0 else 'forward'
            motionSR = 'moving forwards' if stepSR>0 else 'moving backwards'
            print('Stepper Small Rear:',motionSR,abs(stepSR),'steps,',abs(stepSR)*1.8,'deg')
            stepperSR.TurnStep(Dir=dirSR, steps=abs(stepSR)*4, stepdelay = 0.001)
        
        stepBF = self.spb_stepperBF.value()
        if stepBF:
            dirBF = 'forward' if stepBF>0 else 'backward'
            motionBF = 'rotating clockwise' if stepBF>0 else 'rotating counter-clockwise'
            print('Stepper Big Front:',motionBF,abs(stepBF),'steps,',abs(stepBF)*1.8,'deg')
            stepperBF.TurnStep(Dir=dirBF, steps=abs(stepBF)*4, stepdelay = 0.001)
        
        stepBR = self.spb_stepperBR.value()
        if stepBR:
            dirBR = 'forward' if stepBR>0 else 'backward'
            motionBR = 'rotating clockwise' if stepBR>0 else 'rotating counter-clockwise'
            print('Stepper Big Rear:',motionBR,abs(stepBR),'steps,',abs(stepBR)*1.8,'deg')
            stepperBR.TurnStep(Dir=dirBR, steps=abs(stepBR)*4, stepdelay = 0.001)

    def on_btn_runCatheterPos(self): #The default step of the motor driver is 1/4 step ("010"), thus steps are multiplied by 4
        transThick = self.spb_thickTransSF.value()
        if transThick:
            dirSF = 'backward' if transThick>0 else 'forward'
            translationThick = 'moving forwards' if transThick>0 else 'moving backwards'
            print('Thick wire',translationThick,'for',abs(transThick),'mm')
            stepperSF.TurnStep(Dir=dirSF, steps=int(abs(transThick)*800), stepdelay = 0.001)
            
        transThin = self.spb_thinTransSR.value()
        if transThin:
            dirSR = 'backward' if transThin>0 else 'forward'
            translationThin = 'moving forwards' if transThin>0 else 'moving backwards'
            print('Thin wire',translationThin,'for',abs(transThin),'mm')
            stepperSR.TurnStep(Dir=dirSR, steps=int(abs(transThin)*800), stepdelay = 0.001)
            
        rotThick = self.spb_thickRotBF.value()
        if rotThick:
            dirBF = 'forward' if rotThick>0 else 'backward'
            rotationThick = 'rotating clockwise' if rotThick>0 else 'rotating counter-clockwise'
            print('Thick wire',rotationThick,'for',round(int(round(abs(rotThick)/0.9))*0.9,1),'deg')
            stepperBF.TurnStep(Dir=dirBF, steps=int(abs(rotThick)/0.45), stepdelay = 0.001)
            
        rotThin = self.spb_thinRotBR.value()
        if rotThin:
            dirBR = 'forward' if rotThin>0 else 'backward'
            rotationThin = 'rotating clockwise' if rotThin>0 else 'rotating counter-clockwise'
            print('Thin wire',rotationThin,'for',round(int(round(abs(rotThin)/0.9))*0.9,1),'deg')
            stepperBR.TurnStep(Dir=dirBR, steps=int(abs(rotThin)/0.45), stepdelay = 0.001)
            
    def on_chb_joystick(self,state):
        if state:
            self.thrd.setup('joystick_start')
            self.thrd.start()
            print('Joystick starts controlling.')
        else:
            self.thrd.stop()

