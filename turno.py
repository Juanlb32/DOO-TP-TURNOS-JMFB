from datetime import datetime
from cliente import Cliente

class Turno:
    cliente: Cliente
    
    def __init__(self, id_turno, cliente, servicio, fecha_hora, estado="Pendiente"):
        self.id_turno = id_turno
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_hora = fecha_hora
        self.estado = estado
    
    def __str__(self):
        fecha_str = self.fecha_hora.strftime('%Y-%m-%d %H:%M')
        return f"Turno {self.id_turno}: {self.cliente} - {self.servicio} ({fecha_str}) [{self.estado}]"
