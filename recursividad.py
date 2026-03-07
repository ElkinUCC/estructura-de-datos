##Log de Conversión — Recursividad, For y While (EJ 01–06)

---

#EJ 01 — Factorial

## Recursivo

def factorial_rec(n):
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if n == 0:
        return 1
    return n * factorial_rec(n-1)
print(factorial_rec(5))  # Salida: 120

##for

def factorial_for(n):
    resultado = 1
    for i in range(1, n+1):
        resultado *= i
    return resultado


##White

def factorial_while(n):
    resultado = 1
    i = 1
    while i <= n:
        resultado *= i
        i += 1
    return resultado


##ejercicio 2

##recursivo

def suma_digitos_rec(n):
    if n < 10:
        return n
    return (n % 10) + suma_digitos_rec(n // 10)

##for


def suma_digitos_for(n):
    suma = 0
    for digito in str(n):
        suma += int(digito)
    return suma

##white

def suma_digitos_while(n):
    suma = 0
    while n > 0:
        suma += n % 10
        n //= 10
    return suma

##ejercicio 3

##recursivo
def busqueda_binaria_rec(arr, objetivo, izq, der):
    if izq > der:
        return -1

    medio = (izq + der) // 2

    if arr[medio] == objetivo:
        return medio
    elif objetivo < arr[medio]:
        return busqueda_binaria_rec(arr, objetivo, izq, medio-1)
    else:
        return busqueda_binaria_rec(arr, objetivo, medio+1, der)
##for

def busqueda_binaria_for(arr, objetivo):
    izq = 0
    der = len(arr)-1

    for _ in range(len(arr)):
        if izq > der:
            return -1

        medio = (izq + der)//2

        if arr[medio] == objetivo:
            return medio
        elif objetivo < arr[medio]:
            der = medio - 1
        else:
            izq = medio + 1

    return -1

##white

def busqueda_binaria_while(arr, objetivo):
    izq = 0
    der = len(arr) - 1

    while izq <= der:
        medio = (izq + der) // 2

        if arr[medio] == objetivo:
            return medio
        elif objetivo < arr[medio]:
            der = medio - 1
        else:
            izq = medio + 1

    return -1


##ejercicio 4

##recursivo
def es_palindromo_rec(texto):
    texto = texto.replace(" ", "").lower()

    if len(texto) <= 1:
        return True

    if texto[0] != texto[-1]:
        return False

    return es_palindromo_rec(texto[1:-1])

##for

def es_palindromo_for(texto):
    texto = texto.replace(" ", "").lower()

    for i in range(len(texto)//2):
        if texto[i] != texto[-i-1]:
            return False
    return True

##while

def es_palindromo_while(texto):
    texto = texto.replace(" ", "").lower()

    izq = 0
    der = len(texto) - 1

    while izq < der:
        if texto[izq] != texto[der]:
            return False
        izq += 1
        der -= 1

    return True


##ejercicio 5

##recursivo

def hanoi(n, origen, destino, auxiliar):
    if n == 0:
        return

    hanoi(n-1, origen, auxiliar, destino)
    print(f"Mover disco {n} de {origen} a {destino}")
    hanoi(n-1, auxiliar, destino, origen)

##for

def hanoi_for(n):
    movimientos = (2**n) - 1
    for i in range(1, movimientos+1):
        print("Movimiento", i)

##white

def hanoi_while(n):
    movimientos = (2**n) - 1
    i = 1
    while i <= movimientos:
        print("Movimiento", i)
        i += 1


##ejercicio 6

##recursivo

def multiplicar_rec(a,b):
    if b == 0:
        return 0
    return a + multiplicar_rec(a, b-1)

##for

def multiplicar_for(a,b):
    resultado = 0
    for i in range(b):
        resultado += a
    return resultado

##white

def multiplicar_while(a,b):
    resultado = 0
    contador = 0

    while contador < b:
        resultado += a
        contador += 1

    return resultado