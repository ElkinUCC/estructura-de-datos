from sistema_undo import Accion, HistorialAcciones, TipoAccion


class EditorTexto:

    def __init__(self, max_historial=50):
        self.documento = ""
        self.historial = HistorialAcciones(max_historial)


# ---------------------------------------------------

    def escribir(self, texto, posicion=None):

        if posicion is None:
            posicion = len(self.documento)

        antes = self.documento

        self.documento = (
            self.documento[:posicion] +
            texto +
            self.documento[posicion:]
        )

        despues = self.documento

        accion = Accion(
            TipoAccion.INSERTAR,
            antes,
            despues,
            posicion
        )

        self.historial.registrar(accion)


# ---------------------------------------------------

    def borrar(self, inicio, fin):

        antes = self.documento

        self.documento = (
            self.documento[:inicio] +
            self.documento[fin:]
        )

        despues = self.documento

        accion = Accion(
            TipoAccion.ELIMINAR,
            antes,
            despues,
            inicio
        )

        self.historial.registrar(accion)


# ---------------------------------------------------

    def deshacer(self):

        estado = self.historial.retroceder()

        if estado is not None:
            self.documento = estado

        return self.documento


# ---------------------------------------------------

    def rehacer(self):

        estado = self.historial.avanzar()

        if estado is not None:
            self.documento = estado

        return self.documento


# ---------------------------------------------------

    def ver_historial(self):
        self.historial.visualizar()



editor = EditorTexto()

# 20 acciones
for i in range(20):
    editor.escribir(f"{i}")

print("Documento:", editor.documento)

# 10 undo
for _ in range(10):
    editor.deshacer()

print("Tras undo:", editor.documento)

# 5 redo
for _ in range(5):
    editor.rehacer()

print("Tras redo:", editor.documento)

# 3 nuevas acciones (borra redos pendientes)
editor.escribir("A")
editor.escribir("B")
editor.escribir("C")

print("Final:", editor.documento)

print("\nHistorial:")
editor.ver_historial()