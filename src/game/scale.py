class Scale:
    threshSSS = 1.2  # 1200-1400
    threshSS = 1   # 1000-1199
    threshS = 0.9  # 900-999
    threshA = 0.8  # 800-899
    threshB = 0.7  # 700-799
    threshC = 0.6  # 600-699
    threshD = 0.5  # 500-599
    threshE = 0.4  # 400-499
    threshF = 0.3  # 300-399
    threshG = 0.2  # 200-299
    threshH = 0.1  # 100-199

    @staticmethod
    def get_scale(value, max_val):
        val = value / max_val
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
        elif val > Scale.threshF:
            return "F"
        elif val > Scale.threshG:
            return "G"
        elif val > Scale.threshH:
            return "H"
        else:
            return "I"

    @staticmethod
    def get_scale_as_number(value, max_val):
        val = value / max_val
        if val > Scale.threshSSS:
            return Scale.threshSSS
        elif val > Scale.threshSS:
            return Scale.threshSS
        elif val > Scale.threshS:
            return Scale.threshS
        elif val > Scale.threshA:
            return Scale.threshA
        elif val > Scale.threshB:
            return Scale.threshB
        elif val > Scale.threshC:
            return Scale.threshC
        elif val > Scale.threshD:
            return Scale.threshD
        elif val > Scale.threshE:
            return Scale.threshE
        elif val > Scale.threshF:
            return Scale.threshF
        elif val > Scale.threshG:
            return Scale.threshG
        elif val > Scale.threshH:
            return Scale.threshH
        else:
            return 0

    @staticmethod
    def get_scale_as_image_path(value, max_val):
        return "screens/stats/" + Scale.get_scale(value, max_val) + ".png"
