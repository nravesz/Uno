import random

cantidad_jugadores_maximos_pc=3
colores_cartas=["amarillo","azul","verde","rojo"]
cartas_especiales_con_color=["Invertir sentido","Saltear jugador","+2"]
cartas_especiales_sin_color=["+4","Cambiar color"]
estado_inversion=True #eso es cuando va en sentido horario, cuando cambia va en sentido inverso
pozo_mas_dos=0
pozo_mas_cuatro=0
color_juego=None

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
		self.nombre=nombre #nombre del jugador
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
	def __init__(self,valor_accion,color="Sin color"):
		self.valor_accion=valor_accion
		self.color=color
	def valor_accion(self):
		return self.valor_accion
	def color(self):
		return self.color
	def controlar_igualdad(self,otra):
		"""compara si dos cartas, la que se tiene y una dada. Devolviendo True si son compatibles, y False en caso contrario"""
		if self.valor_accion==otra.valor_accion: #si son iguales no importa el color
			return True #son compatibles
		if self.color==otra.color:
			return True
		if self.color=="Sin color" or otra.color=="Sin color":
			return True
		else:
			return False
	def __str__(self):
		return "[{},{}]".format(self.valor_accion,self.color)

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
	def dar_carta(self):
		"""Devuelve la primer carta del mazo al jugador"""
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
		colores=["amarillo","azul","verde","rojo"]
		#agregar los números
		for color in colores: #Aca el nombre estaba mal
			for numero in range(1,10):
				for veces in range(2):
					self.cartas_en_mazo.apilar(_CartaUno(numero,color)) #me convienes un str(i)??
					self.len+=1
			self.cartas_en_mazo.apilar(_CartaUno(0,color)) #Aca pusiste los valores al reves
			self.len+=1
		#agregar las cartas especiales
			for veces in range(2):
				for accion in cartas_especiales_con_color: #porque agrega dos de cada una
					self.cartas_en_mazo.apilar(_CartaUno(accion,color))
					self.len+=1
			for accion in cartas_especiales_sin_color:
				self.cartas_en_mazo.apilar(_CartaUno(accion))

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
	decision=input("Ingrese el numero de la carta que desea tirar: ")
	while not decision.isdigit() or int(decision)>jugador.largo_mano() or int(decision)<=0:
		print("No ha ingresado un número válido")
		decision=input("Ingrese el numero de la carta que desea tirar: ")
	numero = int(decision) - 1
	return numero

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
		nombre_pc= "pc"+ str(i)
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

def verificar_mazo_vacio(mazo_principal,mazo_aux):
	if mazo_principal.esta_vacio():
		carta_arriba=mazo_aux.dar_carta() #le va a dar la carta que está más arriba
		for i in range (len(mazo_aux)): #o sino un while mazo.aux.esta_vacio() != True:
			mazo_principal.agregar_carta(mazo.aux.dar_carta())
	return mazo_principal #si no entró al if simplemente está como estaba

def juego(mazo_principal,mazo_aux,mesa,jugador,nombre_usuario):
		while not jugador.gano(): #porque cuando ganó uno ya está, terminó todo.
			print(mazo_aux.mostrar_carta_de_arriba())
			carta_arriba= mazo_aux.devolver_carta_de_arriba()
			mazo_principal=verificar_mazo_vacio(mazo_principal,mazo_aux)
			if str(jugador) == nombre_usuario: # el juego del usuario
				juego_usuario(jugador,carta_arriba,mazo_principal,mazo_aux,nombre_usuario)
			else: #juega la compu
				juego_compu(jugador,carta_arriba,mazo_principal,mazo_aux)
			cambio_variables(carta) #tanto usuario como pc tiran un carta_a_agarrar
			jugador=cambio_jugador(jugador,carta)
		#felicitar al que ganó, o al menos decir quien ganó

def juego_usuario(jugador,carta_arriba,mazo_principal,mazo_aux,nombre):
	"""El usuario realiza su movimiento. Si se queda sin movimientos, agarra una carta, comprueba si puede jugarla y si no, pasa de turno"""
	print("Es tu turno {}".format(nombre))
	jugador.mostrar_mano()
	movimientos_disponibles = 2
	carta_pos = elegir_carta_a_tirar(jugador)
	carta = jugador.tirar_carta(carta_pos)
	comparacion = carta.controlar_igualdad(carta_arriba)
	while movimientos_disponibles>0 or comparacion == False: #Mientras tenga movimientos disponibles o la carta no coincida, se repite esto
		jugador.recibir_carta(carta) #Hay que volver a ponerla en su mano
		print("No puedes tirar esa carta, debes tirar un carta válida")
		print("Te quedan {} movimientos".format(movimientos_disponibles))
		jugador.mostrar_mano() #Si no le mostramos su mano devuelta, va a poner cualquier cosa. Ya me paso
		carta_pos=elegir_carta_a_tirar(jugador)
		carta=jugador.tirar_carta(carta_pos)
		movimientos_disponibles -= 1
		comparacion = carta.controlar_igualdad(carta_arriba)
	if movimientos_disponibles<=0 or comparacion == False: #Si se le acaban los movimientos, toma una carta
		movimientos_disponibles = 2
		print("Te has quedado sin movimientos. Tomas una carta.")
		carta_recibida = mazo_principal.dar_carta()
		comparacion = carta.controlar_igualdad(carta_arriba)
		if comparacion == True: #Si la carta coincide, automaticamente la juega. No sé si rpeferís que le preguntemos
			mazo_aux.agregar_carta(carta_recibida)
		else: #Si no coincide, la agrega a su mano
			jugador.recibir_carta(carta_recibida)
	if comparacion == True:
		mazo_aux.agregar_carta(carta)
	accion1=sumas_2(carta,carta_arriba,jugador) #Si da False, se salvó, si da True, se le agregan las cartas ya en la función.
	accion2=sumas_4(carta,carta_arriba,jugador) #Por eso me parece que está bien poner esto al final, sino puede que no se comprueben.

def juego_compu(jugador,carta_arriba,mazo_principal,mazo_aux):
	print("Es el turno de {}".format(jugador.nombre()))
	decision=decision_pc(jugador,carta_arriba) #es un número que indica la posicion
	if decision==None:
		print("El jugador toma una carta")
		carta_a_agarrar=mazo_principal.dar_carta()
		if carta_a_agarrar.controlar_igualdad(carta_arriba) == True: #no sé si es super necesario el igual a true
			mazo_aux.agregar_carta(carta_a_agarrar)
		else:
			jugador.recibir_carta(carta_a_agarrar)
	else:
		carta=jugador.tirar_carta(decision)
		accion1=sumas_2(carta,carta_arriba,jugador) #ver que nombre poner
		accion2=sumas_4(carta,carta_arriba,jugador)
		if accion1!=True or accion2!=True:
			mazo.aux.agregar_carta(carta) #agregó la carta

def cambio_jugador(jugador,carta):
	if estado_inversion==True:
		if carta.valor_accion() =="Saltear jugador":
			jugador=mesa.obtener_proximo() # osea se saltea a uno
		jugador=mesa.obtener_proximo()
	else: #osea va al revez
		if carta.valor_accion() =="Saltear jugador":
			jugador=mesa.obtener_anterior()
		jugador=mesa.obtener_anterior()
	return jugador

def cambio_variables(carta):
	if carta.valor_accion== "Invertir": #ver de hacerlo tipo lista[1] para que se mas cambiable el nobre o lo que sea
		print("Se invierte el sentido de la ronda")
		estado_inversion=False
	elif carta.valor_accion== "+4":
		pozo_mas_cuatro+=4
	elif carta.valor_accion=="+2":
		pozo_mas_dos+=2
	elif carta.valor_accion=="Cambiar color":
		color_juego= elegir_color_usuario() #elige el color que quiere
		print("El color de la ronda cambia a {}").format(color_juego)

def sumas_2(carta,carta_arriba,jugador,mazo_aux):
	if pozo_mas_dos != 0:
		if carta.valor_accion()==carta_arriba.valor_accion():
			pozo_mas_dos+=2
			mazo_aux.agregar_carta(carta)
			return False
		else:
			jugador.recibir_carta(carta) #es como que al final no la tira
			for i in range(pozo_mas_dos):
				jugador.recibir_carta(mazo_principal.dar_carta()) #si no tira un +2 se come las que quedaron rezagadas
				mazo_principal=verificar_mazo_vacio(mazo_principal,mazo_aux) #esto es por si se vacía el mazo
			pozo_mas_dos=0
			return True

def sumas_4(carta,carta_arriba,jugador):
	if pozo_mas_cuatro!=0:
		if carta.valor_accion()==carta_arriba.valor_accion():
			pozo_mas_cuatro+=4
			mazo_aux.agregar_carta(carta)
			return False
		else:
			jugador.recibir_carta(carta)
			for i in range(pozo_mas_cuatro):
				jugador.recibir_carta(mazo_principal.dar_carta()) #si no tiro una de mas cuatro se come las q se juntaron
				mazo_principal=verificar_mazo_vacio(mazo_principal,mazo_aux) #esto es por si se vacía el mazo
			pozo_mas_cuatro=0 #vuelve a cero hasta que de nuevo se empieze a sumar
			return True

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
	while decision.lower() != "si" or decision.lower() != "no": #Acá va or
		decision=input("Debes ingresar si o no, deseas tirar la carta tomada? ")
	return decision.lower()

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
		mazo_aux.agregar_carta(mazo_principal.dar_carta()) #le da una carta al mazo auxiliar, ver que esta sea numérica si no no se la da
		jugador=mesa.obtener_actual() #primero el juegador es el usuario
		juego(mazo_principal,mazo_aux,mesa,jugador,nombre)

main()
