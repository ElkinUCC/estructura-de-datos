## ciclo for
numeros = [3,5,8,9,12]

def sumar_numeros(numeros: list) -> int:
    resultado = 0
    for numero in numeros:
        resultado += numero
    return resultado

## ciclo white

def sumar_numeros_while(numeros: list) -> int:
    resultado = 0
    i = 0
    while i < len(numeros):
        resultado += numeros[i]
        i += 1
    return resultado

## recurion    

def sumar_numeros_recursivo(numeros: list) -> int:
    if len(numeros) == 0:
        return 0
    else:
        return numeros[0] + sumar_numeros_recursivo(numeros[1:])
    
print(list(range(1,5)))

## ejercicio con recursividad
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(5))

## ejercicio con for
def factorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

print(factorial(5))

## ejercicio con while
def factorial(n):
    resultado = 1
    i = 1
    while i <= n:
        resultado *= i
        i += 1
    return resultado
print(factorial(5));

##Ejercicio con recursividad para multiplicar dos numeros sin usar el operador de multiplicacion
def multiplicar(a, b):
    if b == 0:
        return 0
    return a + multiplicar(a, b - 1)

print(multiplicar(10, 6)) 

def multiplicar(a, b):
    if a == 0 or b == 0:
        return 0
    if b < 0:
        return -multiplicar(a, -b)
    return a + multiplicar(a, b - 1)
print(multiplicar(10, -6))

## for
def multiplicar(a, b):
    if a == 0 or b == 0:
        return 0
    resultado = 0
    negativo = False

    if b < 0:
        b = -b
        negativo = not negativo
    if a < 0:
        a = -a
        negativo = not negativo

    for i in range(b):
        resultado += a

    if negativo:
        return -resultado
    return resultado
print(multiplicar(10, -9))

##white
def multiplicar(a, b):
    if a == 0 or b == 0:
        return 0

    resultado = 0
    negativo = False

    # cambio signo
    if b < 0:
        b = -b
        negativo = not negativo
    if a < 0:
        a = -a
        negativo = not negativo

    while b > 0:
        resultado += a
        b -= 1

    if negativo:
        return -resultado
    return resultado
print(multiplicar(10, -6))