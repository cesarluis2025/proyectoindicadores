# control/ControlConexion.py
import psycopg2
from psycopg2 import extras
import traceback
import os
class ControlConexion:
    def __init__(self):
        self.conn = None

    def abrirBd(self, servidor, usuario, password, db, puerto):
        try:
            self.conn = psycopg2.connect(
                dbname=db,
                user=usuario,
                password=password,
                host=servidor,
                port=puerto
            )
            self.conn.set_session(autocommit=False)
            return self.conn       
        except psycopg2.OperationalError:
            # Captura específicamente errores de operación (como credenciales incorrectas)
            print("Error de conexión: Credenciales incorrectas (verifique host, bd, usuario, password, puerto) o servidor no disponible")
        except UnicodeDecodeError:
            # Captura errores de codificación
            print("Error de codificación al procesar la respuesta del servidor")
        except Exception as e:
            print("ERROR AL CONECTARSE AL SERVIDOR:")
            try:
                print(f"Tipo de error: {type(e).__name__}")
                print(f"Mensaje: {str(e)}")
                traceback.print_exc()
            except Exception:
                print("No se pudo mostrar la traza del error.")
        
        # En caso de cualquier error, retorna None en lugar de salir
        return None

    def cerrarBd(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def ejecutarComandoSql(self, sql, parametros=[]):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, parametros)
                self.conn.commit()
                return True
        except Exception as e:
            print("Error al ejecutar el comando SQL:", str(e))
            return False

    def ejecutarSelect(self, sql, parametros=[]):
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(sql, parametros)
                recordSet = cursor.fetchall()
                return [dict(record) for record in recordSet]
        except Exception as e:
            print("ERROR:", str(e))
            return False
