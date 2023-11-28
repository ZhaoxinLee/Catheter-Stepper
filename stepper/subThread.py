import sys
import time
from PyQt5.QtCore import pyqtSignal, QMutexLocker, QMutex, QThread
import pygame
import threading

pygame.init()
pygame.joystick.init()
try:
    joystick = pygame.joystick.Joystick(0)
except:
    pass
else:
    joystick.init()

def subthreadNotDefined():
    print('Subthread not defined.')
    return

class SubThread(QThread):
    statusSignal = pyqtSignal(str)

    def __init__(self, stepperSF, stepperSR, stepperBF, stepperBR, joystick=None, parent=None):
        super(SubThread, self).__init__(parent)
        self.stopped = False
        self.mutex = QMutex()
        self._subthreadName = ''
        self.joystick = joystick
        self.stepperSF = stepperSF
        self.stepperSR = stepperSR
        self.stepperBF = stepperBF
        self.stepperBR = stepperBR
        self.thick_state = 'CW'
        self.thin_state = 'CW'
        
    def setup(self,subThreadName):
        self._subthreadName = subThreadName
        self.stopped = False
        
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True
            
    def run(self):
        subthreadFunction = getattr(self,self._subthreadName,subthreadNotDefined)
        subthreadFunction()
        
    def joystick_start(self):
        startTime = time.time()
        try:
            joystick
        except:
            print('Joystick not connected')
        else:
            while True:
                t = time.time() - startTime # elapsed time (sec)
                if joystick.get_button(0):
                    self.thick_state = 'CW'
                if joystick.get_button(1):
                    self.thick_state = 'CCW'
                if joystick.get_button(2):
                    self.thin_state = 'CW'
                if joystick.get_button(3):
                    self.thin_state = 'CCW'
                
                # Multithreading programming
                # thick translational
                thickTransThread = threading.Thread(target=self.thick_trans,args=())
                
                # thin translational
                thinTransThread = threading.Thread(target=self.thin_trans,args=())
                
                # thick rotational
                thickRotThread = threading.Thread(target=self.thick_rot,args=())
                
                # thin rotational
                thinRotThread = threading.Thread(target=self.thin_rot,args=())
                
                thickTransThread.start()
                thinTransThread.start()
                thickRotThread.start()
                thinRotThread.start()

                thickTransThread.join()
                thinTransThread.join()
                thickRotThread.join()
                thinRotThread.join()
                    
                if self.stopped:
                    return

    def thick_trans(self):
        if joystick.get_axis(1)<-0.2:
            self.stepperSF.TurnStep('forward',1,0.001)
        elif joystick.get_axis(1)>0.2:
            self.stepperSF.TurnStep('backward',1,0.001)
            
    def thin_trans(self):
        if joystick.get_axis(4)<-0.2:
            self.stepperSR.TurnStep('forward',1,0.001)
        elif joystick.get_axis(4)>0.2:
            self.stepperSR.TurnStep('backward',1,0.001)
            
    def thick_rot(self):
        if self.thick_state == 'CW' and joystick.get_axis(2)>-0.8:
            self.stepperBF.TurnStep('backward',1,0.001)
        elif self.thick_state == 'CCW' and joystick.get_axis(2)>-0.8:
            self.stepperBF.TurnStep('forward',1,0.001)
            
    def thin_rot(self):
        if self.thin_state == 'CW' and joystick.get_axis(5)>-0.8:
            self.stepperBR.TurnStep('backward',1,0.001)
        elif self.thin_state == 'CCW' and joystick.get_axis(5)>-0.8:
            self.stepperBR.TurnStep('forward',1,0.001)
