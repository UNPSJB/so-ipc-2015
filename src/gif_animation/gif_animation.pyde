add_library("gifAnimation")

imagen = None
x, y = 0, 0
dx, dy = 2, 3
ancho, alto = 500, 500
ancho_imagen, alto_imagen = 100, 100
def setup():
    global imagen
    size(ancho, alto)
    imagen = GifAnimation(this, "lechuza.gif")
    imagen.play()
    print dir(imagen)
    imagen.loop()

    
    
def draw():
    global imagen, x, y, dx, dy
    fill(255, 0, 0)
    background(0, 0, 0)
    image(imagen, x, y, ancho_imagen, alto_imagen)
    text("x:%d y:%d" % (x, y), x, y+alto_imagen+20)
    x += dx
    y += dy
    if x < 0:
        dx = -dx
    elif x > (ancho - ancho_imagen):
        dx = -dx
        
    if y < 0:
        dy = -dy
    elif y > (alto - alto_imagen):
        dy = -dy
    
