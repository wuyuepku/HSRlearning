from MatlabUtil import MatlabUtil

def main():
    m = HSR_CSI_NoMP()
    if True:  # use False if you have built it, to save time
        m.build(
            D = 1000.0,  # D is 1km, as known in some paper
            L = 10000.0,  # L is 10km, -5km ~ +5km
            N2 = 4,  # you can adjust this
            d2 = 0.05,  # half lambda of 3GHz signal
            f = 3e9,  # 3GHz
            deg = 30.0,  # you can adjust this
        )
    m.plot()

class HSR_CSI_NoMP(MatlabUtil):
    def __init__(self):
        MatlabUtil.__init__(self, prefix="HCN_")
    
    def build(self, D, L, N2, d2, f, deg):
        # build sequence with length L, interval lambda/10 (for 3GHz, λ/10 is 1cm, for 10km is 1e6 points)
        N = self._nm
        self._eq(N("lambda"), "3e8 / %f" % f)
        self._eq(N("D"), "%f" % D)
        self._eq(N("L"), "%f" % L)
        self._eq(N("d2"), "%f" % d2)
        self._eq(N("deg"), "%f" % deg)
        self._eq(N("point"), "%s/%s*10" % (N("L"), N("lambda")))
        self._eq(N("x"), "linspace(-%s/2,%s/2,%s)" % (N("L"), N("L"), N("point")))
        self._eq(N("xphi"), "atan(%s/%s)" % (N("x"), N("D")))
        self._eq(N("xsinphid2"), "sin(%s) * %s" % (N("xphi"), N("d2")))
        self._eq(N("d2sindeg"), "sin(%s*pi/180) * %s" % (N("deg"), N("d2")))
        # self._eq(N("deltaX"), "zeros(%d, %s)" % (N2, N("point")))
        # for i in range(N2):
        #     self._eq(N("deltaX(%d,:)" % (i+1)), "linspace(-%s/2+(%f*%s),%s/2+(%f*%s),%s)" % (N("L"), (N2/2-i-0.5), N("d2"), N("L"), (N2/2-i-0.5), N("d2"), N("point")))
        # self._eq(N("deltaL"), "sqrt(%s.^2+%s^2)" % (N("deltaX"), N("D")))
        self._eq(N("deltaL"), "zeros(%d, %s)" % (N2, N("point")))
        for i in range(N2):
            self._eq(N("deltaL(%d,:)" % (i+1)), "(%s - %s) * %f" % (N("xsinphid2"), N("d2sindeg"), (N2/2-i-0.5)))
        self._eq(N("deltaPhi"), "2*pi*%s/%s" % (N("deltaL"), N("lambda")))
        self._eq(N("basicIQ"), "exp(%s*i)" % (N("deltaPhi")))
        # basicIQ has not consider the distance effect, however, this is a nonnegligible factor
        self._eq(N("distIQ"), "%s ./ (sqrt(%s.^2+%s^2).^1)" % (N("basicIQ"), N("x"), N("D")))
    
    def plot(self):
        self._do("figure(1);")
        basicg = r"subplot(3,2,%d);"
        N = self._nm

        # first plot the beam pattern, which considers only degree but not distance
        self._do(basicg % 1)
        self._do("plot(abs(sum(%s)))" % (N("basicIQ")))
        self._do("title('without distance effect')")
        self._do("xlabel('x'),ylabel('amplitude')")
        self._do(basicg % 2)
        self._do("plot(abs(sum(%s)))" % (N("distIQ")))
        self._do("title('with distance considered')")
        self._do("xlabel('x'),ylabel('amplitude')")
    
if __name__ == '__main__':
    main()
