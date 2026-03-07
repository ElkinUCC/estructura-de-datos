class Producto:

    def __init__(self, id, nombre, precio, categoria, stock_disponible):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock_disponible = stock_disponible


class ItemCarrito:

    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.descuento_aplicado = 0
        self.siguiente = None


class Carrito:

    def __init__(self, usuario):
        self.usuario = usuario
        self.cabeza = None


# -------------------------------------------------
# AGREGAR ITEM
# -------------------------------------------------

    def agregar_item(self, producto, cantidad):

        actual = self.cabeza

        while actual is not None:

            if actual.producto.id == producto.id:
                actual.cantidad += cantidad
                return

            actual = actual.siguiente

        nuevo = ItemCarrito(producto, cantidad)

        if self.cabeza is None:
            self.cabeza = nuevo
            return

        actual = self.cabeza

        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo


# -------------------------------------------------
# ELIMINAR ITEM
# -------------------------------------------------

    def eliminar_item(self, id_producto):

        actual = self.cabeza
        anterior = None

        while actual is not None:

            if actual.producto.id == id_producto:

                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                return True

            anterior = actual
            actual = actual.siguiente

        return False


# -------------------------------------------------
# MODIFICAR CANTIDAD
# -------------------------------------------------

    def modificar_cantidad(self, id_producto, nueva_cantidad):

        actual = self.cabeza

        while actual is not None:

            if actual.producto.id == id_producto:
                actual.cantidad = nueva_cantidad
                return True

            actual = actual.siguiente

        return False


# -------------------------------------------------
# APLICAR DESCUENTO
# -------------------------------------------------

    def aplicar_descuento(self, id_producto, porcentaje):

        actual = self.cabeza

        while actual is not None:

            if actual.producto.id == id_producto:
                actual.descuento_aplicado = porcentaje
                return True

            actual = actual.siguiente

        return False


# -------------------------------------------------
# CALCULAR TOTAL
# -------------------------------------------------

    def calcular_total(self):

        total = 0
        actual = self.cabeza

        while actual is not None:

            subtotal = actual.producto.precio * actual.cantidad

            if actual.descuento_aplicado > 0:
                subtotal = subtotal * (1 - actual.descuento_aplicado / 100)

            total += subtotal
            actual = actual.siguiente

        return total


# -------------------------------------------------
# MOVER ITEM ARRIBA (INTERCAMBIO DE NODOS)
# -------------------------------------------------

    def mover_item_arriba(self, id_producto):

        if self.cabeza is None or self.cabeza.producto.id == id_producto:
            return

        prev_prev = None
        prev = self.cabeza
        actual = self.cabeza.siguiente

        while actual is not None:

            if actual.producto.id == id_producto:

                prev.siguiente = actual.siguiente
                actual.siguiente = prev

                if prev_prev is None:
                    self.cabeza = actual
                else:
                    prev_prev.siguiente = actual

                return

            prev_prev = prev
            prev = actual
            actual = actual.siguiente


# -------------------------------------------------
# RESUMEN DEL CARRITO
# -------------------------------------------------

    def obtener_resumen(self):

        print("┌─────────────────────────────────────────────┐")
        print(f"│ CARRITO: {self.usuario:<35}│")
        print("├──────────────────────────┬──────┬──────────┤")
        print("│ Producto                 │ Cant │ Subtotal │")
        print("├──────────────────────────┼──────┼──────────┤")

        actual = self.cabeza

        while actual is not None:

            nombre = actual.producto.nombre
            precio = actual.producto.precio
            cantidad = actual.cantidad

            subtotal = precio * cantidad

            if actual.descuento_aplicado > 0:
                subtotal *= (1 - actual.descuento_aplicado / 100)
                nombre += f" (-{actual.descuento_aplicado}%)"

            print(f"│ {nombre:<24} │ {cantidad:^4} │ {int(subtotal):>8,} │")

            actual = actual.siguiente

        total = self.calcular_total()

        print("├──────────────────────────┴──────┼──────────┤")
        print(f"│ TOTAL                           │ {int(total):>8,} │")
        print("└─────────────────────────────────┴──────────┘")


# -------------------------------------------------
# DIAGRAMA ASCII
# -------------------------------------------------

    def diagrama(self):

        actual = self.cabeza

        while actual is not None:
            print(f"[{actual.producto.nombre} | {actual.cantidad}] -> ", end="")
            actual = actual.siguiente

        print("None")

carrito = Carrito('usuario_123')

carrito.agregar_item(Producto('P01','Laptop',2500000,'Tech',5), 1)
carrito.agregar_item(Producto('P02','Mouse',45000,'Tech',20), 2)
carrito.agregar_item(Producto('P03','Teclado',120000,'Tech',15), 1)

carrito.aplicar_descuento('P01', 10)

carrito.obtener_resumen()

carrito.diagrama()

carrito1 = Carrito("usuario_1")
carrito2 = Carrito("usuario_2")
carrito3 = Carrito("usuario_3")


def comparar_carritos(c1, c2):

    print("Comparando carritos...\n")

    actual = c1.cabeza

    while actual is not None:

        encontrado = False
        otro = c2.cabeza

        while otro is not None:

            if actual.producto.id == otro.producto.id:
                encontrado = True

                if actual.cantidad != otro.cantidad:
                    print(f"Diferencia en {actual.producto.nombre}: "
                          f"{actual.cantidad} vs {otro.cantidad}")

            otro = otro.siguiente

        if not encontrado:
            print(f"{actual.producto.nombre} solo está en carrito 1")

        actual = actual.siguiente