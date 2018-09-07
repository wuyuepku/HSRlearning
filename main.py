"""
to write your own scripts, just inherit from MatlabUtil, like this demo
"""

from MatlabUtil import MatlabUtil

def main():
    demo = MainDemo()
    demo.loaddata([1,2,2.5,2.7,2.5,2,1])
    demo.drawdata()

class MainDemo(MatlabUtil):
    def __init__(self):
        MatlabUtil.__init__(self, prefix='maindemo_')
    
    def loaddata(self, data):
        self._eq(self._nm("data"), data)
    
    def drawdata(self):
        self._do("plot(%s)" % self._nm("data"))

if __name__ == '__main__':
    main()
