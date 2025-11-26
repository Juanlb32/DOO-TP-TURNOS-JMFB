from gestor_cliente import GestorCliente
from gestor_turnos import GestorTurno
from cliente import Cliente
from turno import Turno
from datetime import datetime

gestor_cliente = GestorCliente()
gestor_turno = GestorTurno()

def main():
    gestor_cliente.agenda_clientes()
    gestor_turno.cargar_turnos()
    mostar_menu()

#Menu de opciones
def mostar_menu():
    while True:
        print("\n--- Sistema de Gestión de Turnos ---")
        print("1. Registrar nuevo cliente")
        print("2. Solicitar turno")
        print("3. Listar turnos Disponibles")
        print("4. Cargar Turnos")
        print("5. Buscar turnos por cliente")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            dni =   input("Ingrese el DNI del cliente a cargar: ")
            gestor_cliente.buscar_cliente(dni)
        elif opcion == '2':
            gestor_turno.listar_turnos_disponibles()
        elif opcion == '3':
            gestor_turno.listar_turnos_disponibles()
        elif opcion == '4':
            gestor_turno.cargar_turnos()
        elif opcion == '5':
            dni_cliente = input("Ingrese el DNI del cliente: ") 
            gestor_turno.buscar_turnos_x_cliente(dni_cliente)
        elif opcion == '6':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


