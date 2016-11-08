class _Nodo:
	def __init__(self,dato,prox=None,ant=None):
		self.dato = dato
		self.prox = prox
		self.ant = ant

class _Pila:
	def __init__(self):
		self.elementos = []
	def __len__(self):
		return len(self.elementos)
	def apilar(self,dato):
		self.elementos.append(dato)
	def obtener_tome(self):
		return self.elementos[-1]
	def desapilar(self):
		return self.elementos.pop()
	def esta_vacia(self):
		return len(self.elementos) == 0

class _CartaUno:
	"""Representa una carta del juego Uno"""
	def __init__(self,valor_accion="None",color="None"):
		self.valor_accion = valor_accion
		self.color = color
	def controlar_igualdad(self,otra):
		"""Compara si dos cartas son compatibles"""
		if self.valor.accion == otra.valor_accion:
			return True #son compatibles
		elif self.color == otra.color or self.color == "None" or otra.color == "None":
			return True #son compatibles
		else:
			return False #no es posible realizar la jugada
	def devolver_valor_accion(self):
		return self.valor_accion
	def devolver_color(self): #Agregué esta
		return self.color
	def __str__(self):
		return "[{},{}]".format(self.valor_accion,self.color)

class _Mazo:
	"""Representa un mazo de cartas"""
	def __init__(self):
		"""Constructor de la clase _Mazo"""
		self.mazo_de_cartas = _Pila()
	def agregar_carta(self,carta):
		"""Agrega una carta al mazo"""
		self.mazo_de_cartas.apilar(carta)
	def dar_carta(self):
		"""Devuelve la primera carta del mazo al jugador"""
		self.mazo_de_cartas.desapilar()
	def mezclar(self):
		"""cambia de posicion de manera aleatoria las cartas que estan en el mazo"""
		cant_de_cartas = len(self.cartas_en_mazo)
		for i in range(cant_de_cartas):
			variante = random.randrange(i,cant_de_cartas)
			self.mazo_de_cartas[i],self.mazo_de_cartas[variante] = self.mazo_de_cartas[variante],self.mazo_de_cartas[i]
	def esta_vacio(self):
		return self.mazo_de_cartas.esta_vacia()
	def mostrar_carta_de_arriba(self):
		"""Devuelve la infromacion de la carta tope del mazo. La carta permanece en el mazo"""
		carta_arriba = self.mazo_de_cartas.desapilar()
		self.mazo_de_cartas.apilar(carta_arriba)
		return str(carta_arriba)

class _Jugador:
	"Clase que representa a un jugador"
	def __init__(self,nombre,numero):
		self.mano = []
		self.nombre = nombre
		self.len = 0
		self.numero = numero
	def recibir_carta(self,carta):
		self.mano.append(carta)
		self.len = self.len + 1
	def tirar_carta(self,pos):
		return self.mano.pop(pos)
		self.len = self.len - 1
	def esta_vacia(self):
		return len(self.mano) == 0 #Como esto devuelve True si esta vacia, lo podemos usar para comprobar si gano o no
	def mostrar_mano(self):
		for i,carta in enumerate(self.mano):
			print(i+1,carta)
	def largo_mano(self):
		return self.len
	def devolver_mano(self): #Agregué esta, para poder recorrer la mano como una lista en otra funcion
		return self.mano

class _Mesa:
	def __init__(self,mazo_principal,mazo_aux):
		"""Constructor de la clase mesa"""
		self.prim = None
		self.cant_jugadores = cant_jugadores
		self.mazo_principal = mazo_principal
		self.mazo_aux = mazo_aux
	def agregar_jugador(self,nombre):
		"""Agrega un jugador a la mesa"""
		if self.prim == None:
			self.prim = _Nodo(nombre) #Acá tengo una duda, no iría _Nodo(_Jugador(nombre)) o eso es cualquier cosa? xD Porque no sé cómo hacer para que el dato sea una clase jugador
		else:
			nodo = self.prim
			while nodo.prox! = self.prim:
				nodo = nodo.prox
			anterior = nodo
			nodo.prox = _Nodo(nombre,self.prim,anterior)
		self.cant_jugadores = self.cant_jugadores + 1
	def repartir(self,otro): #otro es el mazo auxiliar
		"""Reparte siete cartas a cada jugador y al final agrega una carta al mazo auxiliar"""
		jugador=self.prim
		for veces in range(7):
			for i in range(self.cant_jugadores):
				carta=self.mazo.dar_carta()
				jugador.dato.recibir_carta(carta)
				jugador=jugador.prox
		otro.agregar_carta(self.mazo.dar_carta()) #la carta que sigue la agrega al mazo auxiliar

def jugada_usuario(jugador,mazo_principal,mazo_aux):
	"""Función que recibe un jugador, el mazo principal y el auxiliar"""
	cantidad = jugador.largo_mano()
	mano = jugador.mostrar_mano()
	carta_aux = mazo_aux.dar_carta()
	while not int(eleccion) in range(1,cant_cartas+1) or not str(eleccion).isdigit():
		print("Opción inválida")
		eleccion = input("¿Qué carta desea jugar?")
	carta = jugador.tirar_carta(eleccion-1)
	if carta.controlar_igualdad(carta_aux) == True or carta.devolver_color() == "negro": #Me parece que es mejor poner negro que None, por si nos da algún error raro al comparar algo de tipo None con una cadena
		mazo_aux.recibir_carta(carta_aux)
		mazo_aux.recibir_carta(carta)
	else: #Si no encuentra coincidencia, vuelve a poner la carta en su mano y recibe una nueva carta
		nueva_carta = mazo_principal.dar_carta()
		jugador.recibir_carta(carta)
		jugador.recibir_carta(nueva_carta)
	#Lo que no sé es si debería hacer que devuelva algo
	
def jugada_pc(jugador,mazo_principal,mazo_aux)
	"""La pc elije una carta basándose en un orden de prioridad (o al menos eso intento AJJAJA)"""
	cantidad = jugador.largo_mano()
	mano = jugador.devolver_mano()
	carta_aux = mazo_aux.dar_carta()
	for i in mano:
		if "negro" in i: #Así pone lo más horrible primero
			posicion = mano.index(i)
			carta = jugador.tirar_carta(posicion)
			mazo_aux.recibir_carta(carta_aux)
			mazo_aux.recibir_carta(carta)
			break
		elif carta_aux.devolver_color in i or carta_aux.devolver_valor in i:
			posicion = mano.index(i)
			carta = jugador.tirar_carta(posicion)
			mazo_aux.recibir_carta(carta_aux)
			mazo_aux.recibir_carta(carta)
			break
		else:
			nueva_carta = mazo_principal.dar_carta()
			jugador.recibir_carta(nueva_carta)
			break
	#tampoco sé si hacer que devuelva algo JAJAJA
