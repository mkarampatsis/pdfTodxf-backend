from src.helpers.pdfTodxf import p_gdxf, p_gcol
from src.helpers.pdfTodxf.mupdflib import mupdfextract, bezier2lines
import os

class DxfDrawer:
    "A drawer which draws into a dxf file."

    def __init__(self, fn):
        "Open dxf and create dxf object."
        fw = open(fn, "w", encoding="iso8859_7")
        print("3>>", fw)
        self.dxf = p_gdxf.ThanDxfPlot()
        self.dxf.thanDxfPlots(fw)


    def close(self):
        "Close the drawing."
        self.dxf.thanDxfPlot(0,0,999)


    def draw_line(self, lay, rgb, lineweight, xa, ya, xb, yb):
        "Draw a line."
        icol = p_gcol.thanRgb2DxfColCodeApprox(rgb)
        self.dxf.thanDxfSetLayer(lay)
        self.dxf.thanDxfSetColor(icol)

        self.dxf.thanDxfPlot(xa, ya, 3)
        self.dxf.thanDxfPlot(xb, yb, 2)


    def draw_rect(self, lay, rgb, lineweight, x0, y0, x1, y1):
        "Draw a rectangle."
        icol = p_gcol.thanRgb2DxfColCodeApprox(rgb)
        self.dxf.thanDxfSetLayer(lay)
        self.dxf.thanDxfSetColor(icol)

        self.dxf.thanDxfPlotPolyVertex(x0, y0, 2)
        self.dxf.thanDxfPlotPolyVertex(x1, y0, 2)
        self.dxf.thanDxfPlotPolyVertex(x1, y1, 2)
        self.dxf.thanDxfPlotPolyVertex(x0, y1, 2)
        self.dxf.thanDxfPlotPolyVertex(x0, y0, 2)
        self.dxf.thanDxfPlotPolyVertex(x0, y0, 2)
        self.dxf.thanDxfPlotPolyVertex(0, 0, 999)


    def draw_quad(self, lay, rgb, lineweight, xll, yll, xlr, ylr, xur, yur, xul, yul):
        "Draw a closed quadrilateral."
        icol = p_gcol.thanRgb2DxfColCodeApprox(rgb)
        self.dxf.thanDxfSetLayer(lay)
        self.dxf.thanDxfSetColor(icol)

        self.dxf.thanDxfPlotPolyVertex(xll, yll, 2)
        self.dxf.thanDxfPlotPolyVertex(xlr, ylr, 2)
        self.dxf.thanDxfPlotPolyVertex(xur, yur, 2)
        self.dxf.thanDxfPlotPolyVertex(xul, yul, 2)
        self.dxf.thanDxfPlotPolyVertex(xll, yll, 2)
        self.dxf.thanDxfPlotPolyVertex(0, 0, 999)


    def draw_bezier(self, lay, rgb, lineweight, xa, ya, xb, yb, xc, yc, xd, yd):
        """Draw a cubic bezier curve.

        see https://en.wikipedia.org/wiki/B%C3%A9zier_curve ."""
        icol = p_gcol.thanRgb2DxfColCodeApprox(rgb)
        self.dxf.thanDxfSetLayer(lay)
        self.dxf.thanDxfSetColor(icol)

        xx, yy = bezier2lines(xa, ya, xb, yb, xc, yc, xd, yd)  #Approximate a cubic bezier curve with line segments.
        self.dxf.thanDxfPlotPolyline(xx, yy)


    def draw_text(self, lay, rgb, tfont, x, y, h, text, theta):
        "Draw a text."
        icol = p_gcol.thanRgb2DxfColCodeApprox(rgb)
        self.dxf.thanDxfSetLayer(lay)
        self.dxf.thanDxfSetColor(icol)

        self.dxf.thanDxfPlotSymbol(x, y, h, text, theta)


def pymain():
    "Start here."
    fpref = "leptomereies_rev2_(1)-model"
    dr = DxfDrawer("/home/markos/projects/pdfTodxf-backend/src/files/" + fpref + ".dxf")
    print("112>>",os.path)
    mupdfextract("/home/markos/projects/pdfTodxf-backend/src/files/" + fpref + ".pdf", dr)
    dr.close()


if __name__ == "__main__": pymain()
