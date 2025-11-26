import csv
import os
import datetime
from cliente import Cliente
from turno import Turno

class GestorCliente:
    agenda_clientes = {}

    def __init__(self):
        pass


    def cargar_agenda_clientes(self, ruta_archivo=None):
 
        
        if ruta_archivo is None:
            ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Clientes", "clientes.csv")
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    id_cliente = fila['dni_cliente']
                    cliente = Cliente(
                        id_cliente=id_cliente,
                        nombre=fila['nombre'],
                        apellido=fila['apellido'],
                        telefono=fila['telefono'],
                        email=fila['email']
                    )
                    GestorCliente.agenda_clientes[id_cliente] = cliente
                    
        except FileNotFoundError:
            print(f"Error: El archivo {ruta_archivo} no fue encontrado.")
        except KeyError as e:
            print(f"Error: Columna faltante en el CSV: {e}")
        except Exception as e:
            print(f"Error al cargar clientes: {e}")



    def buscar_cliente(self, dni_cliente, opcion=None):

        if dni_cliente in GestorCliente.agenda_clientes:
            cliente = GestorCliente.agenda_clientes[dni_cliente]
            print(f"Cliente encontrado: {cliente}")
            if opcion == None:
                while True:
                    print("\n¿Qué desea hacer?")
                    print("1. Asignar un turno")
                    print("2. Modificar cliente")
                    print("3. Eliminar cliente")
                    print("4. Volver")
                    
                    opcion = input("Seleccione una opción (1-4): ").strip()
                    
                    if opcion == "1":
                        print("Asignando turno...")
                        from gestor_turnos import GestorTurno
                        gestor_turno = GestorTurno()
                        gestor_turno.listar_turnos_disponibles()
                        return cliente
                    elif opcion == "2":
                        cliente = self.modificar_cliente(dni_cliente)
                        return cliente
                    elif opcion == "3":
                        self.eliminar_cliente(dni_cliente)
                        return None
                    elif opcion == "4":
                        return cliente
                    else:
                        print("Opción inválida. Intente de nuevo.")
            else:
                return cliente   
        else:
            print(f"Cliente con DNI {dni_cliente} no encontrado.")
            return  self.alta_cliente(dni_cliente)

    def alta_cliente(self,dni):
        nombre = input("Ingrese nombre: ").strip()
        apellido = input("Ingrese apellido: ").strip()
        telefono = input("Ingrese teléfono: ").strip()
        email = input("Ingrese email: ").strip()
        
        nuevo_cliente = Cliente(dni, nombre, apellido, telefono, email)
        
        # Guardar el nuevo cliente en el CSV
        ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Clientes", "clientes.csv")
        
        try:
            with open(ruta_archivo, 'a', encoding='utf-8', newline='') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=['dni_cliente', 'nombre', 'apellido', 'telefono', 'email'])
                escritor.writerow({
                    'dni_cliente': dni,
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'email': email
                })
            
        except Exception as e:
            print(f"Error al guardar cliente en CSV: {e}")
        
        GestorCliente.agenda_clientes[dni] = nuevo_cliente
        print(f"Cliente registrado: {nuevo_cliente}")
        return nuevo_cliente

    def modificar_cliente(self, dni_cliente):

            if dni_cliente in GestorCliente.agenda_clientes:
                del GestorCliente.agenda_clientes[dni_cliente]
                print(f"Cliente con DNI {dni_cliente} eliminado del diccionario.")
            else:
                print(f"Cliente con DNI {dni_cliente} no encontrado en el diccionario.")
            
            return self.alta_cliente(dni_cliente)

    def eliminar_cliente(self, dni_cliente):

        if dni_cliente in GestorCliente.agenda_clientes:
            del GestorCliente.agenda_clientes[dni_cliente]
            print(f"Cliente con DNI {dni_cliente} eliminado del diccionario.")
            
            # Eliminar del CSV
            ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Clientes", "clientes.csv")
            
            try:
                # Leer todas las filas excepto la del cliente a eliminar
                filas = []
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    lector = csv.DictReader(archivo)
                    fieldnames = lector.fieldnames
                    for fila in lector:
                        if fila['dni_cliente'] != dni_cliente:
                            filas.append(fila)
                
                # Escribir de nuevo el archivo sin la fila eliminada
                with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
                    escritor.writeheader()
                    escritor.writerows(filas)
                
                print(f"Cliente con DNI {dni_cliente} eliminado del CSV.")
            except Exception as e:
                print(f"Error al eliminar cliente del CSV: {e}")
        else:
            print(f"Cliente con DNI {dni_cliente} no encontrado en el diccionario.")
