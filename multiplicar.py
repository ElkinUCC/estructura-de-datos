##Ejercicio con recursividad para multiplicar dos numeros sin usar el operador de multiplicacion
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
print(multiplicar(10, 8))