import threading, time

"""
credits:
https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval/48709380#48709380
"""
class SetInterval:
    def __init__(self,interval,action):
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime+=self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()
