class Cliente:
    def __init__(self, id_cliente, nombre, apellido, telefono, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.telefono} - {self.email}"
