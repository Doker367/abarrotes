import datetime
from modules.db_connection import conectar_db

def registrar_venta(productos, tipo_venta, metodo_pago):
    """
    Registra una venta en la base de datos.
    :param productos: Lista de productos vendidos con cantidad y precio.
    :param tipo_venta: 'menudeo' o 'mayoreo'.
    :param metodo_pago: Método de pago utilizado.
    """
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            total = sum([p['cantidad'] * p['precio'] for p in productos])
            fecha = datetime.datetime.now()

            # Insertar la venta
            cursor.execute(
                "INSERT INTO ventas (fecha, tipo_venta, metodo_pago, total) VALUES (%s, %s, %s, %s)",
                (fecha, tipo_venta, metodo_pago, total)
            )
            id_venta = cursor.lastrowid

            # Insertar los detalles de la venta
            for producto in productos:
                cursor.execute(
                    "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio) VALUES (%s, %s, %s, %s)",
                    (id_venta, producto['id_producto'], producto['cantidad'], producto['precio'])
                )

                # Actualizar el stock del producto
                cursor.execute(
                    "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                    (producto['cantidad'], producto['id_producto'])
                )

            conexion.commit()
            print("Venta registrada exitosamente.")
        except Exception as e:
            conexion.rollback()
            print(f"Error al registrar la venta: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")

def corte_caja():
    """
    Genera un resumen de ventas del día por método de pago.
    """
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            fecha_hoy = datetime.date.today()

            # Obtener resumen de ventas por método de pago
            cursor.execute(
                "SELECT metodo_pago, SUM(total) FROM ventas WHERE DATE(fecha) = %s GROUP BY metodo_pago",
                (fecha_hoy,)
            )
            resumen = cursor.fetchall()

            print("Corte de caja del día:")
            for metodo, total in resumen:
                print(f"Método de pago: {metodo}, Total: ${total:.2f}")
        except Exception as e:
            print(f"Error al generar el corte de caja: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")