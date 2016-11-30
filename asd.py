import random

CANTIDAD_JUGADORES_MAXIMOS_PC=3
COLORES_CARTAS=("amarillo","azul","verde","rojo")
CARTAS_ESPECIALES_CON_COLOR=("Invertir sentido","Saltear jugador","+2","Descartar mitad")
CARTAS_ESPECIALES_SIN_COLOR=("+4","Cambiar color")
NOMBRE_JUGADORES_PC=("Superman","Batichica","Guasón")
CANT_CARTAS_POR_COLOR=2 #de las que poseen color
VALOR_NUMERICO_MAXIMO=9
CANT_CARTAS_INICIALES_EN_MANO=7


class _Pila:
	def __init__(self):
		self.elementos=[]

	def apilar (self,dato):
		self.elementos.append(dato)

	def obtener_tope(self):
		return self.elementos[-1]

	def desapilar(self):
		return self.elementos.pop()

	def esta_vacia(self):
		return len(self.elementos)==0


class _Nodo:
	def __init__(self,dato,prox=None,ant=None):
		self.dato=dato
		self.prox=prox
		self.ant=ant


class _ListaDoblementeEnlazadaCircular:
	"""Representa una mesa donde dentro de cada nodo hay un jugador"""
	def __init__(self):
		"""Constructor de clase _lista doblemente enlazada circular"""
		self.prim=None
		self.nodo_actual=None
		self.len=0

	def append(self,dato):
		"""Agrega un nodo"""
		nodo=_Nodo(dato)
		if self.len==0:
			nodo.prox=nodo
			nodo.ant=nodo
			self.prim=nodo
			self.nodo_actual=self.prim
		else:
			nodo.prox=self.prim
			nodo.ant=self.prim.ant
			nodo.ant.prox=nodo
			self.prim.ant=nodo
		self.len+=1

	def obtener_proximo(self):
		if self.len==0:
			return None
		nodo_actual=self.nodo_actual
		nodo_proximo=nodo_actual.prox
		self.nodo_actual=nodo_proximo #ahora el actual es el siguiente
		return nodo_proximo.dato

	def obtener_anterior(self): #para cuando el sentido se invierte
		if self.len==0:
			return None
		nodo_actual=self.nodo_actual
		nodo_anterior=nodo_actual.ant
		self.nodo_actual=nodo_anterior
		return nodo_anterior.dato

	def obtener_actual(self):
		if self.len==0:
			return None
		return self.nodo_actual.dato

	def __len__(self):
		return self.len


class _Mazo:
	"""Representa a un mazo de cartas"""
	def __init__(self):
		"""constructor de la clase _Mazo"""
		self.cartas_en_mazo=_Pila()
		self.len=0

	def __len__(self):
		return self.len

	def agregar_carta(self,carta):
		"""Agrega una carta al mazo"""
		self.cartas_en_mazo.apilar(carta)
		self.len+=1

	def dar_carta(self,otro=None): #otro es el mazo_auxiliar
		"""Devuelve la primer carta del mazo al jugador"""
		return self.cartas_en_mazo.desapilar()
		self.len-=1

	def mezclar(self):
		"""Cambia de posición de manera aleatoria las cartas que están en el mazo a traves de un cambio de lista a pila, pila a lista """
		cant_de_cartas=self.len
		lista=pila_a_lista(self.cartas_en_mazo)
		for i in range(cant_de_cartas):
			variante= random.randrange(i,cant_de_cartas)
			lista[i],lista[variante] = lista[variante],lista[i]
		self.cartas_en_mazo = lista_a_pila(lista)

	def esta_vacio(self):
		return self.cartas_en_mazo.esta_vacia()

	def mostrar_carta_de_arriba(self):
		"""Devuelve la representacion de la primer carta del mazo"""
		return str(self.ver_tope())

	def ver_tope(self):
		"""Devuelve la carta que se encuentra arriba del mazo pero no la saca"""
		carta_arriba=self.cartas_en_mazo.desapilar()
		self.cartas_en_mazo.apilar(carta_arriba)
		return carta_arriba

	def llenar(self,COLORES_CARTAS):
		"""Llena el mazo con todas las cartas del uno"""
		for color in COLORES_CARTAS: #agregar los números
			for numero in range(1,VALOR_NUMERICO_MAXIMO+1):
				for veces in range(CANT_CARTAS_POR_COLOR):
					self.cartas_en_mazo.apilar(_CartaUno(numero,"None",color))
					self.len+=1
			self.cartas_en_mazo.apilar(_CartaUno(0,"None",color))
			self.len+=1
			for veces in range(CANT_CARTAS_POR_COLOR): #agregar las cartas especiales
				for accion in CARTAS_ESPECIALES_CON_COLOR: #porque agrega dos de cada una
					self.cartas_en_mazo.apilar(_CartaUno("None",accion,color))
					self.len+=1
			for accion in CARTAS_ESPECIALES_SIN_COLOR:
				self.cartas_en_mazo.apilar(_CartaUno("None",accion,"Sin color"))
				self.len+=1


class _Jugador:
	"""clase que representa a un jugador del juego"""
	def __init__(self,nombre):
		"""Recibe como parámetro el nombre del jugador ...."""
		self.mano_de_cartas=[]
		self.nombre=str(nombre) #nombre del jugador

	def tirar_carta(self,pos_carta):
		"""Dada la posición de la carta en la mano de cartas, el jugador la tira."""
		return self.mano_de_cartas.pop(pos_carta)

	def carta_a_tirar(self,pos_carta):
		"""Dada la posición de la carta en la mano de cartas, devuelve la carta que desea tirar pero no se la quita de su mano """
		carta_a_tirar=self.tirar_carta(pos_carta)
		self.recibir_carta(carta_a_tirar)
		return carta_a_tirar

	def recibir_carta(self,carta):
		"""El jugador recibe una carta"""
		self.mano_de_cartas.append(carta)

	def cartas_en_mano(self):
		"""devuelve una lista con todas las cartas del jugador"""
		return self.mano_de_cartas

	def mostrar_mano(self):
		"""Imprime una debajo de la otra las cartas pertenecientes a la mano del jugador"""
		for i,elem in enumerate(self.mano_de_cartas):
			print(i+1,end="_")
			print(elem)
			print()

	def gano(self):
		"""Devuelve True si gano y False si perdió"""
		return len(self.mano_de_cartas)==0

	def __len__(self):
		"""Devuelve la cantidad de cartas en la mano del jugador"""
		return len(self.mano_de_cartas)

	def __str__(self):
		"""Devuelve el nombre del jugador"""
		return self.nombre


class _CartaUno:
	"""Representa una carta del juego Uno"""# puede mejorarse esa doc jaja
	def __init__(self,valor,accion,color):
		self.valor=valor
		self.accion=accion
		self.color=color

	def valor(self):
		return self.valor

	def cambiar_color(self,color_nuevo):
		self.color=color_nuevo

	def accion(self):
		return self.accion

	def color(self):
		print(self.color)
		return self.color

	def igualdad(self,otra,color_ronda):
		"""Compara dos cartas, la que se tiene, una dada y el color actual de la ronda. Devolviendo True si son compatibles, y False en caso contrario""" #mejorar documentación
		if self.color==otra.color or self.color==color_ronda:
			return True
		if self.valor!="None" and otra.valor!="None" and self.valor==otra.valor: #si son iguales no importa el color
			return True #son compatibles
		if self.accion !="None" and self.accion==otra.accion:
			return True
		if self.color=="Sin color" :
			return True
		return False

	def __str__(self):
		if self.valor=="None":
			return "[{},{}]".format(self.accion,self.color)
		if self.accion=="None":
			return "[{},{}]".format(self.valor,self.color)


class _Ronda:
	def __init__(self,jugador,mazo_principal,mazo_aux,nombre,mesa):
		"""Constructor de la clase ronda que recibe como parámetro un jugador, un mazo principal y auxiliar, el nombre del usuario y una mesa"""
		self.ESTADO_INVERSION=True #eso es cuando va en sentido horario, cuando cambia va en sentido inverso
		self.POZO_MAS_DOS = 0
		self.POZO_MAS_CUATRO = 0
		self.mazo_principal=mazo_principal
		self.mesa=mesa
		self.nombre=nombre #nombre del usuario
		self.jugador=jugador
		self.carta_arriba=None
		self.mazo_aux=mazo_aux
		self.color_ronda=None

	def juego(self):
		"""Donde se llevan a cabo las funciones relacionadas a la jugabilidad. Si un jugador queda sin cartas,
		 imprime su nombre y lo felicita informándole que ganó el juego"""
		while not self.jugador.gano(): #porque cuando ganó uno ya está, terminó todo.
			self.carta_arriba = self.mazo_aux.ver_tope()
			print("La carta que se encuentra arriba es : {} ".format(self.carta_arriba))
			print()
			if str(self.jugador) == self.nombre: # el juego del usuario
				self.juego_usuario()
			else: #juega la compu
				self.juego_compu()
			carta_actual_arriba=self.mazo_aux.ver_tope() #la carta que quedo arriba
			self.color_ronda=self.color_ronda_actual(carta_actual_arriba)
			if carta_actual_arriba != self.carta_arriba: #si la carta no es la misma
				self.ESTADO_INVERSION=invertir_sentido(carta_actual_arriba,self.jugador,self.nombre,self.ESTADO_INVERSION)
				self.cambio_variables(carta_actual_arriba)
				self.jugador=cambio_jugador(self.jugador,carta_actual_arriba,self.mesa,self.ESTADO_INVERSION)
			else:
				if self.ESTADO_INVERSION==True:
					self.jugador=self.mesa.obtener_proximo()
				else:
					self.jugador=self.mesa.obtener_anterior()
		print()
		print("Felicitaciones {},has ganado".format(str(self.jugador)))
		self.jugador=self.mesa.obtener_proximo()
		while not self.jugador.gano():
			print("Mano de {} :".format(str(self.jugador)))
			self.jugador.mostrar_mano()
			self.jugador=self.mesa.obtener_proximo()
			print()

	def juego_usuario(self):
		"""Imprime la mano del usuario y se verifica si tiene movimientos. De ser así, se le pide que elija una carta hasta que coincida con el tope del mazo.
		La carta se agrega al mazo auxiliar. De no tener movimientos, toma una carta y se verifica si la puede jugar"""
		print("Es tu turno {}".format(self.nombre))
		self.jugador.mostrar_mano() #se le muestra su mano
		if  not no_hay_movimientos(self.jugador.cartas_en_mano(),self.carta_arriba,self.color_ronda): #si no tiene movimientos disponibles
			if self.POZO_MAS_DOS!=0 or self.POZO_MAS_CUATRO!=0: # porque si no puede realizar ningun movimiento de seguro que agarra las cartas resagadas
				self.sumas_2(None)
				self.sumas_4(None)
			else:
				print("No puedes realizar ningun movimiento, tomas una carta.")
				self.mazo_vacio
				carta=self.mazo_principal.dar_carta(self.mazo_aux)
				print ("Tomas la carta {}".format(str(carta)))
				decision=tirar_carta_tomada()
				self.ejecutar_decision_usuario(decision,carta)
		else: #puede hacer un movimiento
			carta_pos=elegir_carta_a_tirar(self.jugador) #
			carta=self.jugador.carta_a_tirar(carta_pos)
			while carta.igualdad(self.carta_arriba,self.color_ronda) == False: #esto es si elige una que no puede usar
				print("no puedes tirar esa carta, debes tirar un carta válida")
				carta_pos=elegir_carta_a_tirar(self.jugador)
				carta=self.jugador.carta_a_tirar(carta_pos)
			if self.POZO_MAS_DOS!=0 or self.POZO_MAS_CUATRO!=0:
				self.sumas_2(carta)
				self.sumas_4(carta)
			else:#no hay ninguna suma rara
				print("El jugador {} tira la carta {}".format(self.nombre,str(carta)))
				carta=self.jugador.tirar_carta(len(self.jugador)-1)
				self.mazo_aux.agregar_carta(carta)

	def juego_compu(self):
		"""Jugada del jugador_pc. Si decisión da una posición, se juega la carta. Sino, toma una. Se verifica el pozo +2/+4"""
		nombre_pc=str(self.jugador)
		print("Es el turno de {}".format((nombre_pc)))
		decision=decision_pc(self.jugador,self.carta_arriba,self.color_ronda) #es un número que indica la posicion
		if decision==None: #no tiene cartas para jugar
			if self.POZO_MAS_DOS!=0:
				for i in range(self.POZO_MAS_DOS):
					self.mazo_vacio()
					self.jugador.recibir_carta(self.mazo_principal.dar_carta(self.mazo_aux))
				print("{} toma {} cartas".format(str(self.jugador),self.POZO_MAS_DOS))
				self.POZO_MAS_DOS=0
			elif self.POZO_MAS_CUATRO!=0:
				for i in range(self.POZO_MAS_DOS):
					self.mazo_vacio()
					self.jugador.recibir_carta(self.mazo_principal.dar_carta(self.mazo_aux))
				print("{} toma {} cartas".format(str(self.jugador),self.POZO_MAS_CUATRO))
				self.POZO_MAS_CUATRO=0
			else:
				print("{} toma una carta".format(str(self.jugador)))
				self.mazo_vacio()
				carta_a_agarrar=self.mazo_principal.dar_carta(self.mazo_aux)
				if carta_a_agarrar.igualdad(self.carta_arriba,self.color_ronda) == True: #no sé si es super necesario el igual a true
					self.mazo_aux.agregar_carta(carta_a_agarrar)
					print("{} tira la carta {}".format(nombre_pc,str(carta_a_agarrar)))
				else:
					self.jugador.recibir_carta(carta_a_agarrar)
		else: #tiene cartas para jugar
			carta=self.jugador.tirar_carta(decision)
			if self.POZO_MAS_DOS!=0 or self.POZO_MAS_CUATRO!=0:
				self.sumas_2(carta)
				self.sumas_4(carta)
			else:#no hay ninguna suma
				print("El jugador {} tira la carta {}".format(nombre_pc,str(carta)))
				self.mazo_aux.agregar_carta(carta)

	def elegir_color_ronda(self,carta):
		"Cambia el color de la ronda respecto a la decision del usuario u de la pc "
		if "Cambiar color" in str(carta) or "+4" in str(carta):
			if str(self.jugador) == self.nombre:
				color_elegido= elegir_color_usuario() #elige el color que quiere
			else:
				color_elegido=elegir_color_pc(self.jugador.cartas_en_mano())
			print("El color de la ronda cambia a {}".format(color_elegido))
			self.color_ronda=color_elegido

	def color_ronda_actual(self,carta):
		"""Actualiza el color de la ronda respecto a la carta que se encuentra arriba del mazo auxiliar"""
		if "+4" in str(carta) or "Cambiar color" in str(carta):
			return self.color_ronda
		for color in COLORES_CARTAS:
		    if color in str(carta):
		        return color

	def sumas_2(self,carta):
		"""Modifica el POZO_MAS_DOS o la mano del jugador dado, dependiendo el estado del pozo"""
		if  "+2" in str(carta) and "+2" in str(self.carta_arriba):
			self.POZO_MAS_DOS+=2
			self.mazo_aux.agregar_carta(carta)
			print("El jugador {} tira la carta {}".format(str(self.jugador),str(carta)))
		elif "+2" in str(self.carta_arriba) and "+2" not in str(carta):
			if str(self.jugador) == self.nombre:
				print("No puedes tirar la carta")
				print("Se agregan {} cartas a tu mano".format(self.POZO_MAS_DOS))
			else:
				print("{} toma {} cartas".format(str(self.jugador),self.POZO_MAS_DOS))
			self.jugador.recibir_carta(carta) #es como que al final no la tira
			for i in range(self.POZO_MAS_DOS):
				self.mazo_vacio
				self.jugador.recibir_carta(self.mazo_principal.dar_carta(self.mazo_aux))
			self.POZO_MAS_DOS=0

	def sumas_4(self,carta):
		"""Modifica el POZO_MAS_CUATRO dado o la mano del jugador dado, dependiendo el estado del pozo"""
		if "+4" in str(carta) and "+4" in str(self.carta_arriba):
			self.POZO_MAS_CUATRO+=4
			if str(self.jugador) == self.nombre:
				color= elegir_color_usuario()
			else:
				color= elegir_color_pc()
			print("{} tira la carta {}".format(str(self.ugador),str(carta)))
			print("El color del juego cambia a {}".format(color))
			self.color_ronda=color
			self.mazo_aux.agregar_carta(carta)
		elif "+4" in str(self.carta_arriba) and "+4" not in str(carta):
			self.jugador.recibir_carta(carta)
			if str(self.jugador) == self.nombre:
				print("No puedes tirar la carta")
				print("Se suman {} cartas a tu mano".format(self.POZO_MAS_CUATRO))
			else:
				print("{} toma {} cartas".format(str(self.jugador),self.POZO_MAS_CUATRO))
			for i in range(self.POZO_MAS_CUATRO):
				self.mazo_vacio()
				self.jugador.recibir_carta(self.mazo_principal.dar_carta(self.mazo_aux)) #si no tiro una de mas cuatro se come las q se juntaron
			self.POZO_MAS_CUATRO=0 #vuelve a cero hasta que de nuevo se empieze a sumar

	def cambio_variables(self,carta):
		"""Evalúa la carta que está en el tope del mazo auxiliar y, de tener un efecto especial, realiza la acción de la carta"""
		descartar_mitad(carta,self.jugador,self.mazo_aux,self.nombre)
		self.elegir_color_ronda(carta)
		if "+2" in str(carta) and self.POZO_MAS_DOS==0:
			self.POZO_MAS_DOS=2
		elif "+4"in str(carta) and self.POZO_MAS_CUATRO==0:
			self.POZO_MAS_CUATRO=4

	def mazo_vacio(self):
		"""En caso de estar el mazo vacío lo llena con las cartas que se encuentran en el mazo aux pero sin la que se encuentra arriba del todo de este"""
		if len(self.mazo_principal)==1:
			carta_arriba=self.mazo_aux.cartas_en_mazo.desapilar() #le va a dar la carta que está más arriba del auxiliar
			for i in range (len(self.mazo_aux)):
				self.mazo_principal.agregar_carta(self.mazo_aux.desapilar())
			self.mazo_aux.agregar_carta(carta_arriba) #se la añade arriva de todo
			self.mazo_principal.mezclar()

	def ejecutar_decision_usuario(self,decision,carta):
		"""Si la decisión es sí, verifica la carta y de ser válida la agrega al mazo auxiliar. Si la decisión es no o la carta es inválida, la agrega a su mano"""
		if decision=="si":
			if self.POZO_MAS_DOS != 0:
				self.sumas_2(carta)
			elif self.POZO_MAS_CUATRO!=0:
				self.sumas_4(carta)
			else:
				if carta.igualdad(self.carta_arriba,self.color_ronda):
					self.mazo_aux.agregar_carta(carta)
				else:
					self.jugador.recibir_carta(carta)
		else:
			self.jugador.recibir_carta(carta)


def pila_a_lista(pila):
	"Dada un pila pasada por parámetro devuelve una lista con sus mismo datos"
	lista=[]
	while not pila.esta_vacia():
		lista.append(pila.desapilar())
	return lista

def lista_a_pila(lista):
	"Dada un lista pasado por parámetro de vuelve un lista con los mismo datos"
	pila=_Pila()
	while len(lista)!=0:
		pila.apilar(lista.pop(0))
	return pila

def elegir_color_pc(mano_de_cartas): #inteligencia, no elige cualquier color sino el que más le conviene
	"""Devuelve el color que más tiene el jugador_pc en su mano"""
	dic={}
	for color in COLORES_CARTAS:
		dic[color]=0
		for carta in mano_de_cartas:
			if color in str(carta):
				dic[color]+=1
	mayor=dic[COLORES_CARTAS[0]]
	for color in COLORES_CARTAS:
		if mayor < dic[color]:
			mayor=dic[color]
	for color in COLORES_CARTAS:
		if dic[color]==mayor:
			return color

def descartar_mitad(carta,jugador,mazo_aux,nombre_usuario):
	"""Carta especial. Si la carta que recibe coincide con Descartar mitad, descarta la mitad de las cartas del jugador y las agrega al mazo auxiliar"""
	if carta.accion == "Descartar mitad": #aca esta la carta especial
		if str(jugador) == nombre_usuario:
			print("Descartas la mitad de tu mano")
		else:
			print("{} descarta la mitad de su mano".format(str(jugador)))
		cantidad=len(jugador)
		descarte=cantidad//2
		for x in range(descarte):
			eleccion=random.randrange(cantidad-1)
			carta = jugador.tirar_carta(eleccion)
			cantidad = cantidad - 1
			mazo_aux.agregar_carta(carta)

def elegir_color_usuario():
	"""Pide al usuario que ingrese un color y lo valida. Devuelve el color"""
	color=input("ingrese el color con el que desea que se siga jugando en el mazo: ")
	while not color.lower() in COLORES_CARTAS:
		color=input("ingrese el color con el que desea que se siga jugando en el mazo: ")
	return color

def tiene_movimientos(jugador,carta_mazo_aux,color_ronda):
	"""Devuelve True si el jugador puede realizar un movimiento y False si no puede"""
	lista_de_cartas=jugador.cartas_en_mano()
	for carta in lista_de_cartas:
		if posible_movimiento(carta,carta_mazo_aux,color_ronda):
			return True
	return False

def posible_movimiento(carta,carta_mazo_aux,color_ronda):
	"""Devuelve True si se puede realizar ese movimiento y false si no se puede"""
	return carta.igualdad(carta_mazo_aux,color_ronda)

def decision_pc(jugador,carta_mazo_aux,color_ronda):
	"""Recorre la mano del jugador_pc. Si la carta puede jugarse, devuelve la posición, en caso contrario, devuelve None"""
	lista_de_cartas=jugador.cartas_en_mano()
	contador=0
	for carta in lista_de_cartas:
		if posible_movimiento(carta,carta_mazo_aux,color_ronda):
			return contador
		else:
			contador+=1
	return None

def elegir_carta_a_tirar(jugador):
	"""Pide al usuario la posición de la carta que desea jugar y la valida. Devuelve el número de la posición"""
	decision=input("ingrese el numero de la carta que desea tirar: ")
	while not decision.isdigit() or int(decision)>len(jugador) or int(decision)<=0:
		print("No ha ingresado un número válido")
		decision=input("ingrese el numero de la carta que desea tirar: ")
	decision=int(decision)-1
	return decision

def cuantos_jugadores(cant_de_jugadores_max_pc):
	"""Le pregunta al usuario con cuantos jugadores desea jugar"""
	texto="Puede jugar con "
	for numero in range(1,CANTIDAD_JUGADORES_MAXIMOS_PC+1):
		if numero==CANTIDAD_JUGADORES_MAXIMOS_PC:
			texto+=" o " + str(numero) + "jugadores"
		else:
			texto+=str(numero) + ","
	print(texto)
	cant_de_jugadores= input("¿Con cuantos jugadores desea jugár?")
	while not cant_de_jugadores.isdigit() or int(cant_de_jugadores)>cant_de_jugadores_max_pc or int(cant_de_jugadores)<=0 :
		print("Recuerde que debe ingresar un numero del 1 al 3")
		cant_de_jugadores= input("¿Con cuantos jugadores desea jugar?  ")
	return int(cant_de_jugadores)

def jugar_nuevamente():
	"""Le pregunta al usuario si desea jugar nuevamente, en caso afirmativo devuelve un True, en caso negativo, un False"""
	decision=input("Desea jugar nuevamente? si/no: ")
	while decision.lower!="si" and decision.lower!="no":
		print("Debe ingresar si o no")
		decision=input("Desea jugar nuevamente? si/no: ")
	return decision.lower()=="si"

def bienvenida():
	"""Saluda al usuario y pregunta por el nombre con el cual desea jugar"""
	print("Bienvenido al juego de cartas Uno")
	nombre=input("Ingrese el nombre con el que desea jugar: ")
	while nombre =="":
		print("Debe ingresar un nombre para poder jugar")
		nombre=input("Ingrese el nombre con el que desea jugar: ")
	return nombre

def llenar_mesa(nombre_usuario,mesa,cant_jugadores_pc,NOMBRE_JUGADORES_PC):
	"""LLena una mesa con el jugador usuario más 1 a 3 jugadores_pc"""
	usuario=_Jugador(nombre_usuario)
	mesa.append(usuario)
	for i in range(cant_jugadores_pc):
		nombre_pc= NOMBRE_JUGADORES_PC[i]
		pc=_Jugador(nombre_pc)
		mesa.append(pc)

def repartir(mesa_con_jug,mazo):
	"""Recibe como parámetro el mazo principal y reparte siete cartas a cada jugador en la mesa_con_jug recibida también por parámetro"""
	for i in range(len(mesa_con_jug)):
		for i in range(CANT_CARTAS_INICIALES_EN_MANO):
			carta=mazo.dar_carta()
			jugador=mesa_con_jug.obtener_actual()
			jugador.recibir_carta(carta)
			mesa_con_jug.obtener_proximo()

def no_hay_movimientos(mano_de_cartas,carta_mazo_aux,color_ronda):
	"""Recorre la mano del jugador y verifica si existe un movimiento válido. De existir, devuelve True, en caso contrario, False"""
	for carta in (mano_de_cartas):
		if carta.igualdad(carta_mazo_aux,color_ronda):
			return True
	return False

def cambio_jugador(jugador,carta,mesa,ESTADO_INVERSION):
	"""Pasa al siguiente jugador. Si la carta jugada es "Saltear jugador", se saltea a uno. Devuelve al jugador"""
	if ESTADO_INVERSION==True:
		if "Saltear jugador" in str(carta):
			jugador=mesa.obtener_proximo()
			print("Se saltea al jugador {}".format(str(jugador)))
		jugador=mesa.obtener_proximo()
	else:
		if "Saltear jugador" in str(carta):
			jugador=mesa.obtener_anterior()
			print("Se saltea al jugador {}".format(str(jugador)))
		jugador=mesa.obtener_anterior()
	return jugador

def invertir_sentido(carta,jugador,nombre_usuario,ESTADO_INVERSION):
	"""Invierte el sentido del juego, siendo los sentidos posibles, True=horario y False=antihorario"""
	if "Invertir sentido" in str(carta): #ver de hacerlo tipo lista[1] para que se mas cambiable el nobre o lo que sea
		print("Se invierte el sentido de la ronda")
		if ESTADO_INVERSION==True:
			ESTADO_INVERSION=False
		else:
			ESTADO_INVERSION=True
	return ESTADO_INVERSION

def tirar_carta_tomada():
	"""Dada un carta tomada del mazo se le da a elegir al usuario si quiere o no tomarla, devolviendo su decision"""
	decision=input("Deseas tirar la carta tomada? ")
	while decision.lower() != "si" and decision.lower() != "no":
		decision=input("Debes ingresar si o no, deseas tirar la carta tomada? ")
	return decision.lower()

def main():
	"""Función principal del juego UNO"""
	nombre=bienvenida() #nombre con el que desea jugar
	while True:
		cant_jugadores_pc=cuantos_jugadores(CANTIDAD_JUGADORES_MAXIMOS_PC) #cantidad de jugadores con los que desea jugar
		mazo_principal=_Mazo() #creo el mazo principal
		mazo_principal.llenar(COLORES_CARTAS) #lleno el mazo
		mazo_principal.mezclar() #mezclo el maso
		mazo_aux=_Mazo() #creo el mazo auxiliar
		mesa=_ListaDoblementeEnlazadaCircular()
		llenar_mesa(nombre,mesa,cant_jugadores_pc,NOMBRE_JUGADORES_PC) #ahora la lista/mesa ya tiene a todos los jugadores
		repartir(mesa,mazo_principal)
		mazo_aux.agregar_carta(mazo_principal.dar_carta(mazo_aux)) #le da una carta al mazo auxiliar, ver que esta sea numérica si no no se la da
		jugador=mesa.obtener_actual() #primero el juegador es el usuario
		print()
		ronda=_Ronda(jugador,mazo_principal,mazo_aux,nombre,mesa)
		ronda.juego()

main()