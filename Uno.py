import random

cantidad_jugadores_maximos_pc=3
colores_cartas=("amarillo","azul","verde","rojo")
cartas_especiales_con_color=("Invertir sentido","Saltear jugador","+2","Descartar mitad")
cartas_especiales_sin_color=("+4","Cambiar color")
estado_inversion=True #eso es cuando va en sentido horario, cuando cambia va en sentido inverso
POZO_MAS_DOS = 0
POZO_MAS_CUATRO = 0
NOMBRE_JUGADORES_PC=("Superman","Batichica","Guasón")

class _Pila:
	def __init__(self):
		self.elementos=[]
	def __len__(self):
		return len(self.elementos)
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
	"""Representa una mesa donde dentro de cada nodo hay un jugador""" #tipo lista circular y doble!!
	def __init__(self): #recibe un mazo mezlcado con todas las cartas del uno y dps un mazo que está vacio
		"""Contructor de clase _lista doblemente enlazada circular"""
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
	def obtener_proximo(self):#con el sentido normal
		nodo_actual=self.nodo_actual
		nodo_proximo=nodo_actual.prox
		self.nodo_actual=nodo_proximo #ahora el actual es el siguiente
		return nodo_proximo.dato #devuelve al jugador en ese nodo
	def obtener_anterior(self): #para cuando el sentido se invierte
		nodo_actual=self.nodo_actual
		nodo_anterior=nodo_actual.prox
		self.nodo_actual=nodo_anterior
		return nodo_anterior.dato
	def obtener_actual(self):
		return self.nodo_actual.dato
	def __len__(self):
		return self.len

class _Jugador:
	"""clase que representa a un jugador del juego"""
	def __init__(self,nombre):
		"""Recibe como parámetro el nombre del jugador ...."""
		self.mano_de_cartas=[]
		self.nombre=str(nombre) #nombre del jugador
		self.cant_de_cartas=0
	def tirar_carta(self,pos_carta):
		"""Dada la posición de la carta en la mano de cartas, el jugador la tira."""
		self.cant_de_cartas-=1
		return self.mano_de_cartas.pop(pos_carta)
	def recibir_carta(self,carta):
		"""El jugador recibe una carta"""
		self.mano_de_cartas.append(carta)
		self.cant_de_cartas+=1
	def cartas_en_mano(self):
		"""devuelve una lista con todas las cartas del jugador"""
		return self.mano_de_cartas
	def mostrar_mano(self):
		for i,elem in enumerate(self.mano_de_cartas):
			print(i+1,end="_")
			print(elem)
			print()
	def gano(self):
		"""Devuelve True si gano y False si perdió"""
		return self.cant_de_cartas==0 #si la mano esta vacia entonces ganó
	def largo_mano(self):
		"""Devuelve la cantidad de cartas en la mano del jugador""" #sirve para algo???
		return self.cant_de_cartas
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
		return self.color
	def controlar_igualdad(self,otra):
		"""Compara si dos cartas, la que se tiene y una dada. Devolviendo True si son compatibles, y False en caso contrario"""
		if self.color==otra.color:
			return True
		if self.valor!="None" and otra.valor!="None" and self.valor==otra.valor: #si son iguales no importa el color
			return True #son compatibles
		if self.accion !="None" and otra.valor!="None" and self.accion==otra.accion:
			return True
		if self.color=="Sin color" or otra.color=="Sin color":
			return True
		else:
			return False
	def __str__(self):
		if self.valor=="None":
			return "[{},{}]".format(self.accion,self.color)
		if self.accion=="None":
			return "[{},{}]".format(self.valor,self.color)

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
	def dar_carta(self,otro=None): #otro es el mazo_auxiliar
		"""Devuelve la primer carta del mazo al jugador"""
		if otro != None:
			if len(self.cartas_en_mazo)==1:
				carta_arriba=otro.cartas_en_mazo.desapilar() #le va a dar la carta que está más arriba del auxiliar
				for i in range (len(otro.cartas_en_mazo)): #o sino un while mazo.aux.esta_vacio() != True:
					self.cartas_en_mazo.agregar_carta(otro.cartas_en_mazo.desapilar())
				otro.agregar_carta(carta_arriba) #se la añade arriva de todo
				self.mezclar()
		return self.cartas_en_mazo.desapilar()
	def mezclar(self):
		"""cambia de posición de manera aleatoria las cartas que están en el mazo"""
		cant_de_cartas=len(self.cartas_en_mazo)
		for i in range(cant_de_cartas):
			variante= random.randrange(i,cant_de_cartas)
			self.cartas_en_mazo.elementos[i],self.cartas_en_mazo.elementos[variante] = self.cartas_en_mazo.elementos[variante],self.cartas_en_mazo.elementos[i]
	def esta_vacio(self):
		return self.cartas_en_mazo.esta_vacia()
	def mostrar_carta_de_arriba(self):
		"""Imprime la primer carta del mazo, pero no se la saca"""
		carta_arriba=self.cartas_en_mazo.desapilar()
		self.cartas_en_mazo.apilar(carta_arriba)
		return str(carta_arriba)
	def devolver_carta_de_arriba(self):
		"""Devuelve la carta de arriba pero no la saca del mazo"""
		carta_arriba=self.cartas_en_mazo.desapilar()
		self.cartas_en_mazo.apilar(carta_arriba)
		return carta_arriba
	def llenar(self):
		"""Llena el mazo con todas las cartas del uno"""
		for color in colores_cartas: #agregar los números
			for numero in range(1,10):
				for veces in range(2):
					self.cartas_en_mazo.apilar(_CartaUno(numero,"None",color))
					self.len+=1
			self.cartas_en_mazo.apilar(_CartaUno(0,"None",color))
			self.len+=1
			for veces in range(2): #agregar las cartas especiales
				for accion in cartas_especiales_con_color: #porque agrega dos de cada una
					self.cartas_en_mazo.apilar(_CartaUno("None",accion,color))
					self.len+=1
			for accion in cartas_especiales_sin_color:
				self.cartas_en_mazo.apilar(_CartaUno("None",accion,"Sin color"))

def elegir_color_usuario(): #arreglar porque no va a poder ver los colores con los que puede jugar
	color=input("ingrese el color con el que desea que se siga jugando en el mazo: ")
	while not color.lower() in colores_cartas:
		color=input("ingrese el color con el que desea que se siga jugando en el mazo: ")
	return color

def tiene_movimientos(jugador,carta_mazo_aux): #cambiar el nombre urgente, pero se supone que mira si en el maso tiene un posible juego
	"""Devuelve True si el jugador puede realizar un movimiento y False si no puede"""
	lista_de_cartas=jugador.cartas_en_mano()
	for carta in lista_de_cartas:
		if posible_movimiento(carta,carta_mazo_aux):
			return True
	return False

def posible_movimiento(carta,carta_mazo_aux):
	"""Devuelve True si se puede realizar ese movimiento y false si no se puede"""
	return carta.controlar_igualdad(carta_mazo_aux)

def decision_pc(jugador,carta_mazo_aux):
	lista_de_cartas=jugador.cartas_en_mano()
	contador=0
	for carta in lista_de_cartas:
		if posible_movimiento(carta,carta_mazo_aux):
			return contador #se supone que la primera que le sirve va como piña, esa es su super inteligenia artificial
		else:
			contador+=1
	return None # si no había ninguna carta

def elegir_carta_a_tirar(jugador):
	decision=input("ingrese el numero de la carta que desea tirar: ")
	while not decision.isdigit() or int(decision)>jugador.largo_mano() or int(decision)<=0:
		print("No ha ingresado un número válido")
		decision=input("ingrese el numero de la carta que desea tirar: ")
	decision=int(decision)-1
	return int(decision)

def cuantos_jugadores():
	print("Puede jugar con 1,2 o 3 jugadores")
	cant_de_jugadores= input("¿Con cuantos jugadores desea jugár?")
	while not cant_de_jugadores.isdigit() or int(cant_de_jugadores)>cantidad_jugadores_maximos_pc or int(cant_de_jugadores)<=0 :
		print("Recuerde que debe ingresar un numero del 1 al 3")
		cant_de_jugadores= input("¿Con cuantos jugadores desea jugar?  ")
	return int(cant_de_jugadores)

def jugar_nuevamente():
	"""Le pregunta al usuario si desea jugar nuevamente, en caso afirmativo devuelve un True, en caso negativo, un False"""
	decision=input("Desea jugar nuevamente? si/no: ")
	while decision.lower!="si" and decision.lower!="no":
		print("Debe ingresar si o no")
		decision=input("Desea jugar nuevamente? si/no: ")
	if decision.lower()=="si":
		return True
	return False

def bienvenida():
	print("Bienvenido al juego de cartas Uno")
	nombre=input("Ingrese el nombre con el que desea jugar: ")
	while nombre =="":
		print("Debe ingresar un nombre para poder jugar")
		nombre=input("Ingrese el nombre con el que desea jugar: ")
	return nombre

def llenar_lista(nombre_usuario,lista_enlazada,cant_jugadores_pc):
	"""LLena la lista_enlazada con un nodo que tiene como dato al jugador usuario y luego de 1 a 3 más jugadores_pc, también como dato de nuevos nodos"""
	usuario=_Jugador(nombre_usuario)
	lista_enlazada.append(usuario)
	for i in range(cant_jugadores_pc): #lo hac por la cantidad de jugadores que quiere el usuario
		nombre_pc= NOMBRE_JUGADORES_PC[i]
		pc=_Jugador(nombre_pc)
		lista_enlazada.append(pc)

def repartir(mesa_con_jug,mazo):
	"""recibe como parámetro el mazo principal y reparte siete cartas a cada jugador en la mesa_con_jug recibida también por parámetro"""
	for i in range(len(mesa_con_jug)):
		for i in range(7): #porque da siete cartas
			carta=mazo.dar_carta()
			jugador=mesa_con_jug.obtener_actual()
			jugador.recibir_carta(carta)
			mesa_con_jug.obtener_proximo() #se supone que pasa al siguiente jugador

def no_hay_movimientos(mano_de_cartas,carta_mazo_aux):
	for carta in (mano_de_cartas):
		if carta.controlar_igualdad(carta_mazo_aux):
			return True
	return False

def algo(decision,carta,carta_arriba,jugador,mazo_principal,mazo_aux,nombre_usuario): #cambiar nombre
	if decision=="si": # tengo que verificar la carta, pero fiaca ahora
		if POZO_MAS_DOS != 0 or POZO_MAS_CUATRO!=0:
			sumas(carta,carta_arriba,jugador,mazo_aux,mazo_principal,nombre_usuario)                      
		else:
			if carta.controlar_igualdad(carta_arriba) == True: #verifico si coinciden las cartas
				mazo_aux.agregar_carta(carta)		#la agrego al mazo de juego
			else:
				jugador.recibir_carta(carta)
	else:
		jugador.recibir_carta(carta) #si no la puede usar se la queda

def juego(mazo_principal,mazo_aux,mesa,jugador,nombre_usuario):
	global POZO_MAS_DOS
	global POZO_MAS_CUATRO
	while not jugador.gano(): #porque cuando ganó uno ya está, terminó todo.
		print("La carta que se encuentra arriba es : {} ".format(mazo_aux.mostrar_carta_de_arriba()))
		print()
		carta_actual_arriba= mazo_aux.devolver_carta_de_arriba()
		if str(jugador) == nombre_usuario: # el juego del usuario
			juego_usuario(jugador,carta_actual_arriba,mazo_principal,mazo_aux,nombre_usuario)
		else: #juega la compu
			juego_compu(jugador,carta_actual_arriba,mazo_principal,mazo_aux,nombre_usuario)
		carta_actual_arriba=mazo_aux.devolver_carta_de_arriba()
		cambio_variables(carta_actual_arriba,jugador,nombre_usuario,mazo_aux) #agregue el mazo como parametro
		jugador=cambio_jugador(jugador,carta_actual_arriba,mesa)
	print("Felicitaciones {},has ganado".format(str(jugador)))

def juego_usuario(jugador,carta_arriba,mazo_principal,mazo_aux,nombre):
	global POZO_MAS_DOS
	global POZO_MAS_CUATRO
	print("Es tu turno {}".format(nombre))
	jugador.mostrar_mano() #se le muestra su mano
	if no_hay_movimientos(jugador.cartas_en_mano(),carta_arriba)==False: #si no tiene movimientos disponibles
		print("No puedes realizar ningun movimiento, tomas una carta.")
		carta=mazo_principal.dar_carta(mazo_aux)
		print ("Tomas la carta {}".format(str(carta)))
		decision=tirar_carta_tomada()
		algo(decision,carta,carta_arriba,jugador,mazo_principal,mazo_aux,nombre)
	else: #puede hacer un movimiento
		carta_pos=elegir_carta_a_tirar(jugador) #
		carta=jugador.tirar_carta(carta_pos)
		while carta.controlar_igualdad(carta_arriba) == False: #esto es si elige una que no puede usar
			print("no puedes tirar esa carta, debes tirar un carta válida")
			jugador.mostrar_mano() #si no se la mostramos otra vez, mete cualquier cosa
			jugador.recibir_carta(carta)
			carta_pos=elegir_carta_a_tirar(jugador)
			carta=jugador.tirar_carta(carta_pos)
		mazo_aux.agregar_carta(carta)
		sumas(carta,carta_arriba,jugador,mazo_aux,mazo_principal,nombre)

def juego_compu(jugador,carta_arriba,mazo_principal,mazo_aux,nombre):
	global POZO_MAS_DOS
	global POZO_MAS_CUATRO
	nombre_pc=str(jugador)
	print("Es el turno de {}".format((nombre_pc)))
	decision=decision_pc(jugador,carta_arriba) #es un número que indica la posicion
	if decision==None:
		print("{} toma una carta".format(str(jugador)))
		carta_a_agarrar=mazo_principal.dar_carta(mazo_aux)
		if carta_a_agarrar.controlar_igualdad(carta_arriba) == True: #no sé si es super necesario el igual a true
			mazo_aux.agregar_carta(carta_a_agarrar)
			print("{} tira la carta {}".format(nombre_pc,str(carta_a_agarrar)))
		else:
			jugador.recibir_carta(carta_a_agarrar)
	else:
		carta=jugador.tirar_carta(decision)
		if POZO_MAS_DOS!=0 or POZO_MAS_CUATRO!=0:
			sumas_2(carta,carta_arriba,jugador,mazo_aux,nombre,mazo_principal)
			sumas_4(carta,carta_arriba,jugador,mazo_aux,nombre,mazo_principal)
		else:#no hay ninguna suma rara
			print("El jugador {} tira la carta {}".format(nombre_pc,str(carta)))
			mazo_aux.agregar_carta(carta)

def cambio_jugador(jugador,carta,mesa):
	if estado_inversion==True:
		if "None" in str(carta):
			if "Saltear jugador" in str(carta):
				jugador=mesa.obtener_proximo() # osea se saltea a uno
				print("Se saltea al jugador {}".format(str(jugador)))
		jugador=mesa.obtener_proximo()
	else: #osea va al revez
		if accion =="Saltear jugador":
			jugador=mesa.obtener_anterior()
		jugador=mesa.obtener_anterior()
	return jugador

def elegir_color_pc():
	"""El jugador pc elige de manera aleatoria un color con el que jugar"""
	eleccion=random.randrange(cantidad_jugadores_maximos_pc+1)
	color=colores_cartas[eleccion]
	return color

def cambio_variables(carta,jugador,nombre_usuario,mazo_aux): #agregue al mazo como parametro
	global POZO_MAS_DOS
	global POZO_MAS_CUATRO
	if carta!=None:
		if carta.accion== "Invertir sentido": #ver de hacerlo tipo lista[1] para que se mas cambiable el nobre o lo que sea
			print("Se invierte el sentido de la ronda")
			estado_inversion=False
		elif carta.accion=="+2":
			POZO_MAS_DOS=2
		elif carta.accion=="+4":
			POZO_MAS_CUATRO=4
		elif carta.accion=="Cambiar color":
			if str(jugador) == nombre_usuario:
				color_elegido= elegir_color_usuario() #elige el color que quiere
			else:
				color_elegido= elegir_color_pc()
				carta.cambiar_color(str(color_elegido)) #no sé si es necesario el str
				print("El color de la ronda cambia a {}".format(color_elegido))
		elif carta.accion == "Descartar mitad": #aca esta la carta especial
			print("Descartas la mitad de tu mano")
			descartar_mitad(jugador,mazo_aux) #DESCARTAR MITAD

def sumas(carta,carta_arriba,jugador,mazo_aux,mazo_principal,nombre_usuario):
	sumas_2(carta,carta_arriba,jugador,mazo_aux,nombre_usuario,mazo_principal)
	sumas_4(carta,carta_arriba,jugador,mazo_aux,nombre_usuario,mazo_principal)

def sumas_2(carta,carta_arriba,jugador,mazo_aux,nombre_usuario,mazo_principal):
	global POZO_MAS_DOS
	if POZO_MAS_DOS != 0:
		if  "+2" in str(carta) and "+2" in str(carta_arriba):
			POZO_MAS_DOS+=2
			mazo_aux.agregar_carta(carta)
			print("{} tira la carta {}".format(nombre_pc,str(carta)))
			mazo_aux.agregar_carta(carta)
		else:
			if str(jugador) == nombre_usuario:
				print("No puedes tirar la carta, se agrega a tu mano")
				print("Se suman {} cartas a tu mano".format(POZO_MAS_DOS))
			else:
				print("{} toma {} cartas".format(str(jugador),POZO_MAS_DOS))
			jugador.recibir_carta(carta) #es como que al final no la tira
			for i in range(POZO_MAS_DOS):
				jugador.recibir_carta(mazo_principal.dar_carta(mazo_aux))
			POZO_MAS_DOS=0

def sumas_4(carta,carta_arriba,jugador,mazo_aux,nombre_usuario,mazo_principal):
	global POZO_MAS_CUATRO
	if POZO_MAS_CUATRO!=0:
		if  "+4" in str(carta) and "+4" in str(carta_arriba):
			POZO_MAS_CUATRO+=4
			if str(jugador) == nombre_usuario:
				color= elegir_color_usuario()
			else:
				color= elegir_color_pc()
			print("El color del juego cambia a {}".format(color))
			carta.cambiar_color(color)
			mazo_aux.agregar_carta(carta)
		else:
			jugador.recibir_carta(carta)
			if str(jugador) == nombre_usuario:
				print("No puedes tirar la carta, se agrega a tu mano")
				print("Se suman {} cartas a tu mano".format(POZO_MAS_CUATRO))
			for i in range(POZO_MAS_CUATRO):
				jugador.recibir_carta(mazo_principal.dar_carta(mazo_aux)) #si no tiro una de mas cuatro se come las q se juntaron
			POZO_MAS_CUATRO=0 #vuelve a cero hasta que de nuevo se empieze a sumar

def decision_pc(jugador,carta_mazo_aux):
	lista_de_cartas=jugador.cartas_en_mano()
	contador=0
	for carta in lista_de_cartas:
		if posible_movimiento(carta,carta_mazo_aux):
			return contador #se supone que la primera que le sirve va como piña, esa es su super inteligenia artificial
		else:
			contador+=1
	return None # si no había ninguna carta

def tirar_carta_tomada():
	decision=input("Deseas tirar la carta tomada? ")
	while decision.lower() != "si" and decision.lower() != "no":
		decision=input("Debes ingresar si o no, deseas tirar la carta tomada? ")
	return decision.lower()
	
def descartar_mitad(jugador,mazo_aux):
	"""Carta especial. Si la carta que recibe coincide con Descartar mitad, descarta la mitad de las cartas del jugador y las agrega al mazo auxiliar"""
	cantidad=jugador.largo_mano()
	descarte=cantidad//2
	for x in range(descarte):
		eleccion=random.randrange(cantidad-1)
		carta = jugador.tirar_carta(eleccion)
		cantidad = cantidad - 1
		mazo_aux.agregar_carta(carta)

def main():
	nombre=bienvenida() #nombre con el que desea jugar
	while True:
		cant_jugadores_pc=cuantos_jugadores() #cantidad de jugadores con los que desea jugar
		mazo_principal=_Mazo() #creo el mazo principal
		mazo_principal.llenar() #lleno el mazo
		mazo_principal.mezclar() #mezclo el maso
		mazo_aux=_Mazo() #creo el mazo auxiliar
		mesa=_ListaDoblementeEnlazadaCircular()
		llenar_lista(nombre,mesa,cant_jugadores_pc) #ahora la lista/mesa ya tiene a todos los jugadores
		repartir(mesa,mazo_principal)
		mazo_aux.agregar_carta(mazo_principal.dar_carta(mazo_aux)) #le da una carta al mazo auxiliar, ver que esta sea numérica si no no se la da
		jugador=mesa.obtener_actual() #primero el juegador es el usuario
		print()
		juego(mazo_principal,mazo_aux,mesa,jugador,nombre)

main()
