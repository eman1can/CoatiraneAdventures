class Scale:
    threshSSS = 1.30
    threshSS = 1.10
    threshS = 0.95
    threshA = 0.85
    threshB = 0.77
    threshC = 0.66
    threshD = 0.55
    threshE = 0.44
    @staticmethod
    def getScale(value, max):
        val = value/max
        if val > Scale.threshSSS:
            return "SSS"
        elif val > Scale.threshSS:
            return "SS"
        elif val > Scale.threshS:
            return "S"
        elif val > Scale.threshA:
            return "A"
        elif val > Scale.threshB:
            return "B"
        elif val > Scale.threshC:
            return "C"
        elif val > Scale.threshD:
            return "D"
        elif val > Scale.threshE:
            return "E"
        else:
            return "F"

    @staticmethod
    def getScale_as_number(value, max):
        val = value / max
        if val > Scale.threshSSS:
            return 1.3
        elif val > Scale.threshSS:
            return 1.1
        elif val > Scale.threshS:
            return 1
        elif val > Scale.threshA:
            return 1
        elif val > Scale.threshB:
            return .8
        elif val > Scale.threshC:
            return .6
        elif val > Scale.threshD:
            return .4
        elif val > Scale.threshE:
            return .2
        else:
            return 0


    @staticmethod
    def getScaleAsImagePath(value, max):
        val = value / max
        # print(str(value) + " " + str(max) + " " + str(val))
        # print(str(Scale.threshA) + str(val > Scale.threshA))
        if val > Scale.threshSSS:
            # print("return scale SSS")
            return '../res/screens/stats/GradeSSS.png'
        elif val > Scale.threshSS:
            # print("return scale SS")
            return '../res/screens/stats/GradeSS.png'
        elif val > Scale.threshS:
            # print("return scale S")
            return '../res/screens/stats/GradeS.png'
        elif val > Scale.threshA:
            # print("return scale A")
            return '../res/screens/stats/GradeA.png'
        elif val > Scale.threshB:
            # print("return scale B")
            return '../res/screens/stats/GradeD.png'
        elif val > Scale.threshC:
            # print("return scale C")
            return '../res/screens/stats/GradeC.png'
        elif val > Scale.threshD:
            # print("return scale D")
            return '../res/screens/stats/GradeD.png'
        elif val > Scale.threshE:
            # print("return scale E")
            return '../res/screens/stats/GradeE.png'
        else:
            # print("return scale F")
            return '../res/screens/stats/GradeF.png'
