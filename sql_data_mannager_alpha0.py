import mysql.connector
from mysql.connector import Error

datos = {'host':'DOMINIO',
'database':'NOMBRE DE BASE DE DATOS',
'user':'USUARIO',
'password':'CONTRASEÑA'
}

#Manejador de base de datos
class db:
    #Metodo de conexión
    def __init__(self,data_connection):
        try:
            self.db = mysql.connector.connect(**data_connection)
            self.message = "Conexión alcanzada"
            if not self.db.is_connected():
                self.message = "Conexión no alcanzada"
        except Error as e:
            self.message = str(e)
    #Método de creación de tablas
    #EL CREADOR DE TABLAS PODRÏA AGREGARSE A INTERFAZ MAESTRA (NO CLIENTE)
    def create_table(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("CREATE TABLE Estados (ESTADO_ID int NOT NULL AUTO_INCREMENT, ESTADO VARCHAR(255) NO NULL, PRIMARY KEY (ESTADO_ID))")
            self.message = "Tabla creada de manera exitos"
        except:
            self.message = "Tabla no creada de manera exitosa"
    #Método de cerradura
    def close_connection(self):
        self.db.close()
        self.message = "Conexión terminada"


base_de_datos = db(datos)
print(base_de_datos.message)
base_de_datos.close_connection()
print(base_de_datos.message)
