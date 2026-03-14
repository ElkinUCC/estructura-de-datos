class Nodo:
    """
    Clase que representa un nodo en una estructura de datos enlazada.
    Cada nodo contiene datos y una referencia al siguiente nodo.
    """

    def __init__(self, dato):
        """
        Inicializa un nuevo nodo con el dato proporcionado.

        :param dato: El dato que almacenará el nodo.
        """
        self.dato = dato
        self.siguiente = None

    def __str__(self):
        """
        Devuelve una representación en cadena del nodo.

        :return: Cadena que representa el dato del nodo.
        """
        return str(self.dato)

    def __repr__(self):
        """
        Devuelve una representación detallada del nodo para depuración.

        :return: Cadena que representa el nodo con su dato.
        """
        return f"Nodo({self.dato})"