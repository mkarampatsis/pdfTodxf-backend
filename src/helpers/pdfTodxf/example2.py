import p_gdxf, p_gcol
from src.helpers.pdfTodxf.mupdflib import mupdfextract, bezier2lines


class PrtDrawer:
    "A drawer which print the elements to screen."

    def __init__(self):
        "Open dxf and create dxf object."
        pass


    def draw_line(self, lay, rgb, lineweight, xa, ya, xb, yb):
        "Draw a line."
        print("line", lay, rgb, lineweight)
        print("    ",xa, ya, xb, yb)


    def draw_rect(self, lay, rgb, lineweight, x0, y0, x1, y1):
        "Draw a rectangle."
        print("rectangle", lay, rgb, lineweight)
        print("    ", x0, y0, x1, y1)


    def draw_quad(self, lay, rgb, lineweight, xll, yll, xlr, ylr, xur, yur, xul, yul):
        "Draw a closed quadrilateral."
        print("quad", lay, rgb, lineweight)
        print(xll, yll, xlr, ylr, xur, yur, xul, yul)


    def draw_bezier(self, lay, rgb, lineweight, xa, ya, xb, yb, xc, yc, xd, yd):
        "Draw a cubic bezier curve."
        print("bezier", lay, rgb, lineweight)
        print("    ", xa, ya, xb, yb, xc, yc, xd, yd)


    def draw_text(self, lay, rgb, tfont, x, y, h, text, theta):
        "Draw a text."
        print("text", lay, rgb, tfont)
        print("    ", x, y, h, text, theta)


def pymain():
    "Start here."
    fpref = "leptomereies_rev2_(1)-model"
    dr = PrtDrawer()
    mupdfextract("/home/markos/projects/pdfTodxf-backend/src/files/" + fpref + ".pdf", dr)


if __name__ == "__main__": pymain()
