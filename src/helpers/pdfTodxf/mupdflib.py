#https://pymupdf.readthedocs.io/en/latest/
#See: https://pymupdf.readthedocs.io/en/latest/functions.html#Page.get_texttrace
#documentation of page.get_texttrace() which explains the various attributes of text (for example flags)

#Changed in v1.19.1: stroke and fill colors now always are either RGB or GRAY
#Also note, that the text color is encoded as the usual tuple of floats 0 <= f <= 1 – not in sRGB format
#'flags': 12, # font flags (1)

from math import atan2, pi
import pymupdf


def mupdfextract(fn, dr):
    "Extract drawing shapes and text from pdf file using pymupdf library; draw into drawing object dr."
    doc = pymupdf.open(fn)
    page = doc[0]
    xymm = page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1   #xmin, ymin, xmax, ymax of the page
    assert xymm[0] == 0.0 and xymm[1] == 0.0, "Lower left corner coordinates of page should be 0, 0"

    paths = page.get_drawings()
    for path in paths:
        lay = path.get('layer', '0')
        if lay.strip() == "": lay = "0"
        col = path['color']
        lineweight = path["width"]
        rgb = mucolor2rgb(col)
        for item in path["items"]:
            if item[0] == "l":  # line
                pa = item[1]
                pb = item[2]
                dr.draw_line(lay, rgb, lineweight, pa.x, xymm[3]-pa.y, pb.x, xymm[3]-pb.y)
            elif item[0] == "re":  # rectangle
                re = item[1]
                dr.draw_rect(lay, rgb, lineweight, re.x0, xymm[3]-re.y0, re.x1, xymm[3]-re.y1)
            elif item[0] == "qu":  # quad
                re = item[1]
                dr.draw_quad(lay, rgb, lineweight, re.ll[0], xymm[3]-re.ll[1], re.lr[0], xymm[3]-re.lr[1],
                                                   re.ur[0], xymm[3]-re.ur[1], re.ul[0], xymm[3]-re.ul[1])
            elif item[0] == "c":  # curve
                pa = item[1]
                pb = item[2]
                pc = item[3]
                pd = item[4]
                dr.draw_bezier(lay, rgb, lineweight, pa.x, xymm[3]-pa.y, pb.x, xymm[3]-pb.y,
                                                     pc.x, xymm[3]-pc.y, pd.x, xymm[3]-pd.y)
            else:
                raise ValueError("unhandled drawing", item)

    lay = "pdf_texts"
    for x, y, h, text, theta, col, tfont in itertexts(page):
        dr.draw_text(lay, rgb, tfont, x, xymm[3]-y, h, text, 360.0-theta)

    doc.close()


def itertexts(page):
    """Iterate through all the texts of a pdf page.

    Σαβ 28 Σεπ 2024 04:55:27 μμ EEST
    It seems:
    1. A pages has many textblocks, which are multiline texts.
    2. Each block has many lines of texts. Also, a number (a/a), a type,
       and a boundary box which are of no concern.
    3. Each line has many spans, presumably on the same line. 
       Also a wmode (?), a boundary box which are of no concern.
       And also a dir (direction) which is vector with 2 elements, which show
       the direction of all the spans in the line (like angle theta). It seems
       that it is a unit vector, but it is not guaranteed.
    4. Each span represents a text. It has
       size, font, color, text, origin, bbox (boundary)
       and flags (?), ascender (?), descender (?) which are ignored.
    """
    tpage = page.get_textpage()
    dtpage = tpage.extractDICT()
    blocks = dtpage["blocks"]
    del tpage, dtpage
    for b in blocks:   #loop over all multiline text blocks of the page
        for line1 in b["lines"]:  #loop over all text lines of a multline text block
            t = line1["dir"]
            theta = (atan2(t[1], t[0]) * 180.0 / pi) % 360.0   #angle of the text line in degrees
            for span1 in line1["spans"]:  #loop over all texts ("spans") of a text line
                x, y = span1["origin"]
                col = mucolor2rgb(span1["color"])
                flags  = span1["flags"]           #'flags': 12, # font flags
                yield x, y, span1["size"], span1["text"], theta, col, span1["font"]


def oldmucolor2rgb(col):
    "Convert color returned by pymupdf to RGB integer values between 0 and 255."
    #Changed in v1.19.1: stroke and fill colors now always are either RGB or GRAY
    def conv():
        "Convert color to tuple of 3."
        try: col+0
        except: pass
        else: return col, col, col  #Number -> grayscale
        try:
            n = len(col)
            if n == 1: return col[0], col[0], col[0]   #List/tuple with one element -> grayscale
            else:      return col[0], col[1], col[2]   #List/tuple with 3 elements -> RGB
        except (ValueError, IndexError, TypeError):
            raise ValueError("Not a valid pymupdf color: should be a number, or list/tuple with 1 number, or a list/tuple with 3 numbers")

    #print("col=", col)
    temp = conv()
    for x in temp:
        if x < 0 or x > 1: raise ValueError("Not a valid pymupdf color: should be between 0 and 1")

    rgb = tuple(int(round(x*255)) for x in conv())
    return rgb

def mucolor2rgb(col):
    "Convert color returned by pymupdf to RGB integer values between 0 and 255."
    #Changed in v1.19.1: stroke and fill colors now always are either RGB or GRAY
    print(col)
    isnum = True
    try: col+0
    except: isnum = False
    if isnum:
        if col != round(col):
            raise ValueError("Not a valid pymupdf color: {}".format(col))
        #probably a ARGBA color
        # Convert to unsigned 32-bit integer
        temp = col & 0xFFFFFFFF
        # Extract ARGB components
        alpha = (temp >> 24) & 0xFF
        red =   (temp >> 16) & 0xFF
        green = (temp >> 8) & 0xFF
        blue =  temp & 0xFF
        return red, green, blue
    try:
        n = len(col)
        if n == 1: temp = col[0], col[0], col[0]   #List/tuple with one element -> grayscale
        else:      temp = col[0], col[1], col[2]   #List/tuple with 3 elements -> RGB
    except (ValueError, IndexError, TypeError):
        raise ValueError("Not a valid pymupdf color: {}".format(col))

    for x in temp:
        if x < 0 or x > 1: 
            print("col=", col, "->", temp)
            raise ValueError("Not a valid pymupdf color, should be between 0 and 1: {}".format(col))

    rgb = tuple(int(round(x*255)) for x in temp)
    return rgb


def bezier2lines(xa, ya, xb, yb, xc, yc, xd, yd):
    """Approximate a cubic bezier curve with line segments."

    see https://en.wikipedia.org/wiki/B%C3%A9zier_curve ."""
    tt = [i*0.01 for i in range(0, 101)]
    xx = [(1-t)**3*xa + 3*(1-t)**2*t*xb + 3*(1-t)*t**2*xc + t**3*xd for t in tt]
    yy = [(1-t)**3*ya + 3*(1-t)**2*t*yb + 3*(1-t)*t**2*yc + t**3*yd for t in tt]
    return xx, yy
