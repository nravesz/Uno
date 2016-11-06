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
		"""Cambia de posición de manera aleatoria las cartas que están en el mazo"""
		cant_de_cartas = len(self.cartas_en_mazo)
		for i in range(cant_de_cartas):
			variante = random.randrange(i,cant_de_cartas)
			self.mazo_de_cartas[i],self.mazo_de_cartas[variante] = self.mazo_de_cartas[variante],self.mazo_de_cartas[i]
	def esta_vacio(self):
		return self.mazo_de_cartas.esta_vacia()
	def mostrar_carta_de_arriba(self):
		"""Devuelve la infromación de la carta tope del mazo. La carta permanece en el mazo"""
		carta_arriba = self.mazo_de_cartas.desapilar()
		self.mazo_de_cartas.apilar(carta_arriba)
		return str(carta_arriba)
	def devolver_carta_de_arriba(self): #Me parece que cuando vos hiciste devolver_carta_de_arriba, la sacabas y la devolvías al mazo, como en mostrar_de_arriba
		"""Saca del mazo la carta de arriba y la devuelve"""
		carta_arriba = self.mazo_de_cartas.desapilar()
		return carta_arriba

class _Jugador:
	"Clase que representa a un jugador"
	def __init__(self,nombre):
		self.mano = []
		self.nombre = nombre
	def recibir_carta(self,carta):
		self.mano.append(carta)
	def tirar_carta(self,pos):
		return self.mano.pop(pos)
	def esta_vacia(self):
		return len(self.mano) == 0 #Como esto devuelve True si está vacía, lo podemos usar para comprobar si ganó o no
	def mostrar_mano(self):
		for i,carta in enumerate(self.mano):
			print(i+1,carta)
		
		
		
		
