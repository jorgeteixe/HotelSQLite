# coding=utf-8
import sqlite3

class Conexion:
    def abrirbbdd(self):
        try:
            global bbdd, connect, cur
            bbdd = 'empresa.sqlite'
            connect = sqlite3.connect(bbdd)
            cur = connect.cursor()
            print('Conexión realizada correctamente')
        except connect.err.OperationalError as e:
            print('Error al abrir: ', e)

    def cerrarbbdd(self):
        try:
            cur.close()
            connect.close()
            print('Conexión terminada satisfactoriamente')
        except sqlite3.err.OperationalError as e:
            print('Error al cerrar: ', e)