import pygame
import os
from pygame import *
from random import randint
from pygame.locals import *
from pygame.sprite import Sprite



def cargar_imagen(nombre,optimizar = False):
   ruta=os.path.join('images',nombre)
   imagen=pygame.image.load(ruta)
   if optimizar:
	return imagen.convert()
   else:
	return imagen.convert_alpha()

def spritecollideany(sprite,grupo):
   funcion_colision=sprite.rect_colision.colliderect

   for s in grupo:
	if funcion_colision(s.rect_colision):
	   return s
   return None


def a_coordenadas(fila,columna):
   return (60+columna * 48 , 80+fila*43)

def a_celdas(pos_x,pos_y):
   return ((pos_y-80)/43 , (pos_x-60)/48)




#clase final

class Final(Sprite):
   def __init__(self,x,y):
	Sprite.__init__(self)
	self.image=cargar_imagen('garu.png')
	self.rect= self.image.get_rect()
	self.rect.center = (x, y)
	self.rect_colision = self.rect.inflate(-30,-10)
	self.delay = 0
	self.terminar = True
   def update(self):
	pass

   def update_final(self):
	self.delay -=1
	if self.delay<1:
	   self.kill()

   def llegar(self):
	self.image=cargar_imagen('fin.png')
	self.delay =30
	self.update = self.update_final
	self.terminar=False


# clase puntos
class Puntos(Sprite):

   def __init__(self, x, y):
	Sprite.__init__(self)
	self.image=cargar_imagen('punto.png')
	self.rect= self.image.get_rect()
	self.rect.center = (x, y)
	self.rect_colision = self.rect.inflate(-30,-10)
	self.delay = 0
	self.se_puede_comer= True

   def update(self):
	pass

   def update_desaparecer(self):
	self.delay -=1
	if self.delay<1:
	   self.kill()

   def comer(self):
	self.image=cargar_imagen('explosion1.png')
	self.delay =20
	self.update = self.update_desaparecer
	self.se_puede_comer=False
   

#clase escenario
class Escenario:
    def __init__(self, nivel=1):
        self.pared = cargar_imagen('bloque.png')
	self.cesped=cargar_imagen('cesped.png')
        self.mapa = self.cargar_nivel(nivel)
	self.delay = None
    def imprimir(self, fondo):
	
        imagenes = {
	    '.': self.cesped,
            '#': self.pared,
	    
            }

        y = 0

        for fila in self.mapa:
            x = 0

            for celda in fila:
                if celda in imagenes:
                    #pos = (60 + x * 48- 55, 80 + y * 43 - 43)
                    pos = (60 + x * 48 - 20, 80 + y * 43 - 20)
                    fondo.blit(imagenes[celda], pos)

                x += 1

            y += 1

    def cargar_nivel(self, nivel):
        nombre_del_archivo = 'nivel_%d.txt' %nivel
        archivo = open(nombre_del_archivo, 'rt')
        mapa = archivo.readlines()
        archivo.close()
        return mapa

    def crear_objetos(self, puntos,final):
        y = 0
        for fila in self.mapa:
            x = 0
            for celda in fila:
                pos_x, pos_y = a_coordenadas(y, x)
		if celda == '+':
		     puntos.add(Puntos(pos_x, pos_y))
                elif celda == 'x':
                     final.add(Final(pos_x, pos_y))


                x += 1

            y += 1

    def puede_avanzar(self, (fila, columna), (df, dc)):


        # limites de la pantalla
        if fila + df < 0 or fila + df > 11:
            return False
        elif columna + dc < 0 or columna + dc > 11:
            return False

        if self.mapa[fila + df][columna + dc] in '# ':
            return False

        return True



#clase jugador

class Jugador(Sprite):

   def __init__(self,escenario):
	Sprite.__init__(self)
	self.cargar_imagenes()
	self.image=self.normal
	self.escenario=escenario
	self.en_movimiento=True
	self.columna_destino=1
	self.fila_destino=1
	self.delay = None
	self.x=-50
	self.y=200
	self.rect=self.image.get_rect()
	self.rect_colision=self.rect.inflate(-20,-20)
	self.se_puede_comer= True
	self.terminar = True
   def cargar_imagenes(self):
	self.normal = cargar_imagen('pucca.gif')
	

   def update(self):
	if not self.en_movimiento:
	   teclas=pygame.key.get_pressed()
	   if teclas[K_LEFT]:
		self.mover(-1, 0)		
	   elif teclas[K_RIGHT]:
		self.mover(+1, 0)
	   elif teclas[K_UP]:
		self.mover(0, -1)
	   elif teclas[K_DOWN]:
		self.mover(0, +1)
	else:
	   self.actualizar_posicion()
	
	self.actualizar_animacion()
	self.actualizar_rect_colision()

   def actualizar_posicion(self):
	pos= a_coordenadas(self.fila_destino,self.columna_destino)
	destino_x,destino_y= pos

	delta_x=(destino_x - self.x) / 10
	delta_y=(destino_y - self.y) / 10

	if abs(delta_x) <0.1 and abs(delta_y) < 0.1:
	   self.x = destino_x
	   self.y = destino_y
	   self.en_movimiento = False
	else:
	   self.x +=delta_x
	   self.y +=delta_y
	self.rect.centerx=int(self.x)
	self.rect.centery=int(self.y)
   

   def mover(self,desplazamiento_columna, desplazamiento_fila):
	self.en_movimiento = True

	pos_actual = (self.fila_destino, self.columna_destino)
	desplazamiento= (desplazamiento_fila, desplazamiento_columna)

	if self.escenario.puede_avanzar(pos_actual,desplazamiento):
	   self.fila_destino +=desplazamiento_fila
	   self.columna_destino += desplazamiento_columna

   def actualizar_rect_colision(self):
	self.rect_colision.midbottom = self.rect.midbottom

   def actualizar_animacion(self):
        if self.delay > 0:
            self.delay -= 1

            if self.delay < 1:
                self.image = self.normal	

   def desaparece(self):
         self.delay = 25


#####----------#####


def main():

	pygame.init()

	visor= pygame.display.set_mode((640,480))
	fuente=pygame.font.Font(None,30)
	fuente1=pygame.font.Font(None,70)
	pygame.display.set_caption("Pucca quiere a Garu")
	temporizador=pygame.time.Clock()
	color= (200,200,200)
	fondo = cargar_imagen('fondo.jpg', optimizar= True)
	logotipo=cargar_imagen('logo.gif')
	
	sprites = pygame.sprite.OrderedUpdates()

	puntos = pygame.sprite.Group()
	final = pygame.sprite.Group()	
	
	escenario = Escenario()
	escenario.imprimir(fondo)
	escenario.crear_objetos(puntos,final)
	jugador= Jugador(escenario)
	sprites.add(puntos)
	sprites.add(final)
	sprites.add(jugador)
	nivel = 1
	punto = 0
	salir=True
	#reloj = pygame.time.Clock()



	while salir:
		#reloj.tick(60)
		for evento in pygame.event.get():
		   if evento.type == pygame.QUIT:
			salir = False
		   elif evento.type == pygame.KEYDOWN:
			if evento.unicode == 'q':
			   salir= False
			elif evento.unicode == 'f':
			   pygame.display.toggle_fullscreen()
	
		puntos_en_colision1 = spritecollideany(jugador, puntos)
		puntos_en_colision2 = spritecollideany(jugador, final)
		
		# colision con puntos
		if puntos_en_colision1 and puntos_en_colision1.se_puede_comer:
		   puntos_en_colision1.comer()
		   punto = punto +10			
		
		if puntos_en_colision2 and puntos_en_colision2.terminar:
			if (nivel ==1 and punto == 50) or (nivel ==2 and punto == 100):
			   puntos_en_colision2.llegar()
			   jugador.desaparece()
			   
			   sprites.remove(jugador)
			   nivel= nivel + 1
			  		   
			   fondo = cargar_imagen('escenario.jpg', optimizar= True)
		   	   escenario = Escenario(nivel)
			   escenario.imprimir(fondo)
			   escenario.crear_objetos(puntos,final)
			   jugador= Jugador(escenario)
			   
			   sprites.add(puntos)
			   sprites.add(final)
			   sprites.add(jugador)

			if nivel ==3 and punto ==150:
					txt="ganaste"
					msj=fuente1.render(txt,1,(255,255,255))
					fondo=cargar_imagen('ganaste.jpg', optimizar= True)
					sprites.remove(jugador)	
					sprites.remove(final)					
					visor.blit(fondo,(158,183))						
					visor.blit(msj,(150,150))
					visor.blit(logotipo,(640-80,480-80))
					temporizador.tick(60)										
					salir=False
					

		texto="puntos: " + str(punto) + "               nivel:" + str(nivel)
		mensaje=fuente.render(texto,1,(255,255,255))
		visor.fill((30,145,255))
		visor.blit(fondo,(0,0))		
		visor.blit(mensaje,(15,5))
		pygame.draw.line(visor,(255,255,255),(0,25),(640,25) , 2)
		sprites.update()
		

		sprites.draw(visor)
		visor.blit(logotipo,(640-80,480-80))
		pygame.display.flip()
		temporizador.tick(60)


if __name__ == '__main__':
	main()







