from reportlab.pdfgen import canvas    
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch  


def printColors(canvas):  
    canvas.setFont("Helvetica",10)
    y = x = 0; dy=inch*1/2.0; dx=1*inch; w=h=dy/2  
    rdx=(dx-w)/2; rdy=h/5.0
    available_paper = 10*inch

    for name, color in colors.getAllNamedColors().iteritems():

    # for [namedcolor, name] in (  
        # 'darkseagreen', 'darkslateblue',
        #  [colors.darkblue, 'darkblue'],
        #  [colors.darkcyan, 'darkcyan'],
        #  [colors.darkolivegreen, 'darkolivegreen'],
        #  [colors.cornflower, 'cornflower'],
        #  [colors.orchid, 'orchid'],
        
        #  [colors.lavenderblush, "lavenderblush"],  
        #  [colors.lawngreen, "lawngreen"],  
        #  [colors.lemonchiffon, "lemonchiffon"],  
        #  [colors.lightblue, "lightblue"],  
        #  [colors.lightcoral, "lightcoral"]):  
        canvas.setFillColor(color)  
        canvas.rect(x+rdx, y+rdy, w, h, fill=1)
        canvas.setFillColor(colors.black)  
        canvas.drawString(x+dx/4 + 1*inch, y+rdy, name)  
        rdy += .2*inch
        available_paper -= (y+rdy)
        if available_paper < 1*inch:
            c.showPage()
            y = x = 0; dy=inch*1/2.0; dx=1*inch; w=h=dy/2  
            rdx=(dx-w)/2; rdy=h/5.0
            available_paper = 10*inch
 
  
if __name__ == "__main__":  
    c = canvas.Canvas("colors.pdf", pagesize=letter)    
    printColors(c)  
    c.save()  