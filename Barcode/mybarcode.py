from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart


class MyBarcodeDrawing(Drawing):
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing('Code128', value=text_value, barHeight=5*mm, barWidth=2, humanReadable=True)
        Drawing.__init__(self, barcode.width, barcode.height, *args, **kw)
        self.add(barcode, name='barcode')

    def g(self, barcode, name):
        MyBarcodeDrawing(barcode).save(formats=['png'], outDir='./uploads/barcode', fnRoot=name)


def generate_barcode(barcode):
    text = str(barcode)
    MyBarcodeDrawing(text).save(formats=['png'], outDir='./uploads/barcode', fnRoot=text)
    return 'Done'