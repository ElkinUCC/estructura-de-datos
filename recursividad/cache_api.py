import random


class NodoCache:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.anterior = None
        self.siguiente = None


class CacheLRU:

    def __init__(self, capacidad):

        self.capacidad = capacidad
        self.cache = {}

        # nodos centinela
        self.cabeza = NodoCache(0, 0)
        self.cola = NodoCache(0, 0)

        self.cabeza.siguiente = self.cola
        self.cola.anterior = self.cabeza

        self._hits = 0
        self._misses = 0


# ------------------------------------------------
# GET
# ------------------------------------------------

    def get(self, key):

        if key not in self.cache:
            self._misses += 1
            return -1

        nodo = self.cache[key]

        self._hits += 1
        nodo.freq += 1

        self._mover_al_frente(nodo)

        return nodo.value


# ------------------------------------------------
# PUT
# ------------------------------------------------

    def put(self, key, value):

        if key in self.cache:

            nodo = self.cache[key]
            nodo.value = value
            nodo.freq += 1

            self._mover_al_frente(nodo)

        else:

            nuevo = NodoCache(key, value)

            self.cache[key] = nuevo
            self._insertar_frente(nuevo)

            if len(self.cache) > self.capacidad:
                self._evict()


# ------------------------------------------------
# INSERTAR AL FRENTE
# ------------------------------------------------

    def _insertar_frente(self, nodo):

        nodo.siguiente = self.cabeza.siguiente
        nodo.anterior = self.cabeza

        self.cabeza.siguiente.anterior = nodo
        self.cabeza.siguiente = nodo


# ------------------------------------------------
# MOVER AL FRENTE
# ------------------------------------------------

    def _mover_al_frente(self, nodo):

        self._eliminar_nodo(nodo)
        self._insertar_frente(nodo)


# ------------------------------------------------
# ELIMINAR NODO
# ------------------------------------------------

    def _eliminar_nodo(self, nodo):

        anterior = nodo.anterior
        siguiente = nodo.siguiente

        anterior.siguiente = siguiente
        siguiente.anterior = anterior


# ------------------------------------------------
# EVICT LRU
# ------------------------------------------------

    def _evict(self):

        lru = self.cola.anterior

        self._eliminar_nodo(lru)

        del self.cache[lru.key]


# ------------------------------------------------
# HIT RATE
# ------------------------------------------------

    def hit_rate(self):

        total = self._hits + self._misses

        if total == 0:
            return 0

        return self._hits / total


# ------------------------------------------------
# ESTADO CACHE
# ------------------------------------------------

    def estado_cache(self):

        actual = self.cabeza.siguiente
        resultado = []

        while actual != self.cola:
            resultado.append(actual.key)
            actual = actual.siguiente

        return resultado


cache = CacheLRU(3)

cache.put("A", 10)
cache.put("B", 20)
cache.put("C", 30)

print(cache.estado_cache())
# ['C','B','A']

cache.get("A")

print(cache.estado_cache())
# ['A','C','B']

cache.put("D", 40)

print(cache.estado_cache())
# ['D','A','C']  (B fue eliminado)

capacidades = [10,50,100,500]

for cap in capacidades:

    cache = CacheLRU(cap)

    for _ in range(1000):

        k = random.randint(1,200)

        if random.random() < 0.7:
            cache.get(k)
        else:
            cache.put(k, random.randint(1,100))

    print(cap, "->", cache.hit_rate())


def grafico_hit_rate(resultados):

    for cap, rate in resultados:
        barra = "#" * int(rate * 50)
        print(f"{cap:4} | {barra} {rate:.2f}")