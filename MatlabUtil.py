# since starting a new engine really consume time, it's recommended to connect to a shared MATLAB session
# to shared the session in MATLAB GUI, just call this in MATLAB ------------------  `matlab.engine.shareEngine`
# I found that if there's no shared sessions, it will automatically create one and then delete, which really consume time (about 5s)

import matlab.engine, os, math

class MatlabUtil:
    def __init__(self, prefix=""):  # using prefix to separate different apps
        self.eng = matlab.engine.connect_matlab()  # connect otherwise create one
        self.prefix = prefix
    
    def eq(self, var, command):
        return self.eng.eval("%s = %s;" % (var, command), nargout=0)

    def do(self, command):
        return self.eng.eval("%s;" % command, nargout=0)
    
    def nm(self, name):
        return self.prefix + name
