from cliente import Cliente
import cliente
from turno import Turno
import datetime
import csv
import os

class GestorTurno:
    agenda_turnos = {}

    def __init__(self):
        pass

    def nombre_archivo(self, fecha=None):
        fecha = datetime.datetime.now()
        return f"turnos_{fecha.strftime('%Y%m%d')}.csv"

    def crear_csv_turnos(self, fecha=None):
        if fecha is None:
            fecha = datetime.datetime.now()

        # Obtener el nombre del archivo
        nombre_file = self.nombre_archivo()
        ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Turnos", nombre_file)

        # Verificar si el archivo ya existe
        if os.path.exists(ruta_archivo):
            print(f"El archivo {nombre_file} ya existe.")
            return ruta_archivo

        # Headers: id_turno + campos de Cliente + servicio, fecha_hora, estado
        fieldnames = ['id_turno', 'id_cliente', 'nombre', 'apellido', 'telefono', 'email', 'servicio', 'fecha_hora', 'estado']

        try:
            # Crear lista de turnos con horarios cada media hora de 10:00 a 20:00
            turnos = []
            hora_inicio = 10
            minuto = 0
            id_turno = 1
            
            for i in range(20):
                # Crear datetime con la fecha y hora especificada
                fecha_hora = datetime.datetime(fecha.year, fecha.month, fecha.day, hora_inicio, minuto)
                
                turno = {
                    'id_turno': id_turno,
                    'id_cliente': '',
                    'nombre': '',
                    'apellido': '',
                    'telefono': '',
                    'email': '',
                    'servicio': '',
                    'fecha_hora': fecha_hora.strftime('%Y-%m-%d %H:%M'),
                    'estado': 'Disponible'
                }
                turnos.append(turno)
                
                # Incrementar 30 minutos para el próximo turno
                minuto += 30
                if minuto == 60:
                    minuto = 0
                    hora_inicio += 1
                
                id_turno += 1
            
            with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
                escritor.writeheader()
                escritor.writerows(turnos)
            
            print(f"Archivo {nombre_file} creado exitosamente con 20 turnos.")
            return ruta_archivo

        except Exception as e:
            print(f"Error al crear archivo CSV de turnos: {e}")
            return None

    def cargar_turnos(self, fecha=None):
       # Obtener el nombre del archivo
        nombre_file = self.nombre_archivo()
        ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Turnos", nombre_file)

        try:
            if not os.path.exists(ruta_archivo):
                print(f"El archivo {nombre_file} no existe. Creando...")
                self.crear_csv_turnos()
        
            
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                for fila in lector:
                    id_turno = fila['id_turno']
                    
                    # Crear cliente si tiene datos
                    cliente = None
                    if fila['id_cliente']:
                        cliente = Cliente(
                            id_cliente=fila['id_cliente'],
                            nombre=fila['nombre'],
                            apellido=fila['apellido'],
                            telefono=fila['telefono'],
                            email=fila['email']
                        )
                    
                    turno = Turno(
                        id_turno=id_turno,
                        cliente=cliente,
                        servicio=fila['servicio'] if fila['servicio'] else None,
                        fecha_hora=datetime.datetime.strptime(fila['fecha_hora'], '%Y-%m-%d %H:%M'),
                        estado=fila['estado']
                    )
                    GestorTurno.agenda_turnos[id_turno] = turno
            
            print(f"Se cargaron {len(GestorTurno.agenda_turnos)} turnos desde {nombre_file}.")

        except Exception as e:
            print(f"Error al cargar turnos: {e}")

    def listar_turnos_disponibles(self, cliente=None):
        if not GestorTurno.agenda_turnos:
            print("No hay turnos cargados. Cargue los turnos primero.")
            return

        print(f"{'ID TURNO':<12} {'FECHA Y HORA':<20} {'ESTADO':<15}")

        for id_turno in sorted(GestorTurno.agenda_turnos.keys(), key=lambda x: int(x)):
            turno = GestorTurno.agenda_turnos[id_turno]
            if turno.estado == "Disponible":
                fecha_hora_str = turno.fecha_hora.strftime('%Y-%m-%d %H:%M')
                print(f"{turno.id_turno:<12} {fecha_hora_str:<20} {turno.estado:<15}")

        respuesta = input("\n¿Desea asignar un turno? (s/n): ").strip().lower()

        respuestas = ["s", "n"]
        while respuesta not in respuestas:
            respuesta = input("Respuesta inválida. Por favor ingrese 's' o 'n': ").strip().lower()

        if respuesta == "s":
            if cliente is None:
                dni_cliente = input("Ingrese el DNI del cliente: ").strip()
                from gestor_cliente import GestorCliente
                gestor_cliente = GestorCliente()
                cliente = gestor_cliente.buscar_cliente(dni_cliente, "1")
            
            if cliente:
                id_turno = input("Ingrese el ID del turno a asignar: ").strip()
                self.asignar_turno(id_turno, cliente)

    def asignar_turno(self, id_turno, cliente):
        if id_turno in GestorTurno.agenda_turnos:
            turno = GestorTurno.agenda_turnos[id_turno]
            turno.cliente = cliente
            turno.estado = "Asignado"
            turno.servicio = "Peluqueria"
            GestorTurno.agenda_turnos[id_turno] = turno


            fecha_hora_str = turno.fecha_hora.strftime('%Y-%m-%d %H:%M')
            print(f"\n--- Turno Asignado ---")
            print(f"Nombre: {cliente.nombre}")
            print(f"Apellido: {cliente.apellido}")
            print(f"DNI Cliente: {cliente.id_cliente}")
            print(f"Fecha y Hora: {fecha_hora_str}\n")

            input("Presione Enter para continuar...")


    def buscar_turnos_x_cliente(self, dni_cliente):
        turnos_encontrados = []
        for id_turno, turno in GestorTurno.agenda_turnos.items():
            if turno.cliente and turno.cliente.id_cliente == dni_cliente:
                turnos_encontrados.append(turno)

        if not turnos_encontrados:
            print(f"No hay turnos para el cliente con DNI {dni_cliente}")
            return


        print(f"{'ID TURNO':<12} {'ID CLIENTE':<15} {'NOMBRE':<15} {'APELLIDO':<15} {'TELÉFONO':<15} {'EMAIL':<20} {'SERVICIO':<15} {'FECHA Y HORA':<20} {'ESTADO':<15}")

        for turno in turnos_encontrados:
            nombre = turno.cliente.nombre if turno.cliente else ""
            apellido = turno.cliente.apellido if turno.cliente else ""
            telefono = turno.cliente.telefono if turno.cliente else ""
            email = turno.cliente.email if turno.cliente else ""
            id_cliente = turno.cliente.id_cliente if turno.cliente else ""
            servicio = turno.servicio if turno.servicio else ""
            fecha_hora_str = turno.fecha_hora.strftime('%Y-%m-%d %H:%M')
            
            print(f"{turno.id_turno:<12} {id_cliente:<15} {nombre:<15} {apellido:<15} {telefono:<15} {email:<20} {servicio:<15} {fecha_hora_str:<20} {turno.estado:<15}")
        
    def guardar_agenda(self):
        # Obtener el nombre del archivo
        nombre_file = self.nombre_archivo()
        ruta_archivo = os.path.join(os.path.dirname(__file__), "Agendas", "Turnos", nombre_file)

        try:
            with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
                fieldnames = ['id_turno', 'id_cliente', 'nombre', 'apellido', 'telefono', 'email', 'servicio', 'fecha_hora', 'estado']
                escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
                escritor.writeheader()

                for id_turno in sorted(GestorTurno.agenda_turnos.keys(), key=lambda x: int(x)):
                    turno = GestorTurno.agenda_turnos[id_turno]
                    fila = {
                        'id_turno': turno.id_turno,
                        'id_cliente': turno.cliente.id_cliente if turno.cliente else '',
                        'nombre': turno.cliente.nombre if turno.cliente else '',
                        'apellido': turno.cliente.apellido if turno.cliente else '',
                        'telefono': turno.cliente.telefono if turno.cliente else '',
                        'email': turno.cliente.email if turno.cliente else '',
                        'servicio': turno.servicio if turno.servicio else '',
                        'fecha_hora': turno.fecha_hora.strftime('%Y-%m-%d %H:%M'),
                        'estado': turno.estado
                    }
                    escritor.writerow(fila)
            
            print(f"Agenda de turnos guardada en {nombre_file}.")

        except Exception as e:
            print(f"Error al guardar agenda de turnos: {e}")