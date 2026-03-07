from decimal import Decimal
from datetime import datetime
from enum import Enum

class TipoTransaccion(Enum):
    DEPOSITO = 'DEP'
    RETIRO = 'RET'
    TRANSFERENCIA = 'TRF'
    REVERSO = 'REV'


class EstadoTx(Enum):
    PENDIENTE = 'PENDIENTE'
    CONFIRMADA = 'CONFIRMADA'
    FALLIDA = 'FALLIDA'
    REVERTIDA = 'REVERTIDA'

class Transaccion:

    def __init__(self, id_tx, tipo, monto, origen, destino=None):

        self.id_tx = id_tx
        self.tipo = tipo
        self.monto = Decimal(str(monto))

        self.cuenta_origen = origen
        self.cuenta_destino = destino

        self.estado = EstadoTx.PENDIENTE
        self.timestamp = datetime.now()

        self.siguiente = None
        self.anterior = None

        self.saldo_origen_pre = None
        self.saldo_destino_pre = None

class CuentaBancaria:

    def __init__(self, numero, titular, saldo_inicial):

        self.numero = numero
        self.titular = titular
        self.saldo = Decimal(str(saldo_inicial))

        self.historial = None
        self.total_tx = 0


    def agregar_transaccion(self, tx):

        tx.siguiente = self.historial
        self.historial = tx

        self.total_tx += 1
        
class SistemaBancario:

    def __init__(self):

        self.cuentas = {}

        self.log_pendientes = None
        self.log_confirmadas = None

        self.grafo_transferencias = {}

        self._contador_tx = 0

    def crear_cuenta(self, numero, titular, saldo_inicial):

        cuenta = CuentaBancaria(numero, titular, saldo_inicial)

        self.cuentas[numero] = cuenta
        self.grafo_transferencias[numero] = []

    def depositar(self, numero_cuenta, monto):

        cuenta = self.cuentas[numero_cuenta]

        self._contador_tx += 1

        tx = Transaccion(self._contador_tx,
                         TipoTransaccion.DEPOSITO,
                         monto,
                         numero_cuenta)

        cuenta.saldo += tx.monto

        tx.estado = EstadoTx.CONFIRMADA

        cuenta.agregar_transaccion(tx)

    def retirar(self, numero_cuenta, monto):

        cuenta = self.cuentas[numero_cuenta]

        monto = Decimal(str(monto))

        if cuenta.saldo < monto:
            raise Exception("Saldo insuficiente")

        self._contador_tx += 1

        tx = Transaccion(self._contador_tx,
                         TipoTransaccion.RETIRO,
                         monto,
                         numero_cuenta)

        cuenta.saldo -= monto

        tx.estado = EstadoTx.CONFIRMADA

        cuenta.agregar_transaccion(tx)

    def transferir(self, origen, destino, monto):

        if origen not in self.cuentas or destino not in self.cuentas:
            raise Exception("Cuenta no existe")

        cuenta_origen = self.cuentas[origen]
        cuenta_destino = self.cuentas[destino]

        monto = Decimal(str(monto))

        if cuenta_origen.saldo < monto:
            raise Exception("Saldo insuficiente")

        self._contador_tx += 1

        tx = Transaccion(self._contador_tx,
                         TipoTransaccion.TRANSFERENCIA,
                         monto,
                         origen,
                         destino)

        try:

            tx.saldo_origen_pre = cuenta_origen.saldo
            tx.saldo_destino_pre = cuenta_destino.saldo

            cuenta_origen.saldo -= monto
            cuenta_destino.saldo += monto

            tx.estado = EstadoTx.CONFIRMADA

            cuenta_origen.agregar_transaccion(tx)
            cuenta_destino.agregar_transaccion(tx)

            self.grafo_transferencias[origen].append(destino)

            return tx.id_tx

        except Exception as e:

            cuenta_origen.saldo = tx.saldo_origen_pre
            cuenta_destino.saldo = tx.saldo_destino_pre

            tx.estado = EstadoTx.FALLIDA

            raise e

    def rollback(self, id_tx):

        for cuenta in self.cuentas.values():

            tx = cuenta.historial

            while tx:

                if tx.id_tx == id_tx and tx.estado == EstadoTx.CONFIRMADA:

                    origen = self.cuentas[tx.cuenta_origen]
                    destino = self.cuentas[tx.cuenta_destino]

                    origen.saldo = tx.saldo_origen_pre
                    destino.saldo = tx.saldo_destino_pre

                    tx.estado = EstadoTx.REVERTIDA

                    return True

                tx = tx.siguiente

        return False

    def detectar_ciclos_transferencia(self):

        visitado = set()
        stack = []


        def dfs(cuenta):

            visitado.add(cuenta)
            stack.append(cuenta)

            for vecino in self.grafo_transferencias.get(cuenta, []):

                if vecino not in visitado:

                    ciclo = dfs(vecino)
                    if ciclo:
                        return ciclo

                elif vecino in stack:

                    idx = stack.index(vecino)
                    return stack[idx:] + [vecino]

            stack.pop()
            return None


        for cuenta in self.grafo_transferencias:

            if cuenta not in visitado:

                ciclo = dfs(cuenta)
                if ciclo:
                    return ciclo

        return None

    def reporte_cuenta(self, numero_cuenta):

        cuenta = self.cuentas[numero_cuenta]

        print("\nEstado de cuenta")
        print("Cuenta:", cuenta.numero)
        print("Titular:", cuenta.titular)
        print("Saldo actual:", cuenta.saldo)

        print("\nHistorial:")

        tx = cuenta.historial

        while tx:

            print(tx.id_tx,
                  tx.tipo.value,
                  tx.monto,
                  tx.estado.value,
                  tx.timestamp)

            tx = tx.siguiente

banco = SistemaBancario()

banco.crear_cuenta('COL001','Ana García',5000000)
banco.crear_cuenta('COL002','Luis Torres',2500000)
banco.crear_cuenta('COL003','María Ruiz',1000000)

banco.depositar('COL001',500000)

banco.transferir('COL001','COL002',1000000)

banco.retirar('COL002',200000)

tx_id = banco.transferir('COL002','COL003',800000)

banco.rollback(tx_id)

banco.transferir('COL001','COL002',100000)
banco.transferir('COL002','COL003',100000)
banco.transferir('COL003','COL001',100000)

print("Ciclo:", banco.detectar_ciclos_transferencia())

banco.reporte_cuenta('COL001')
