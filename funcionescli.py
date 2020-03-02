# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import variables, sqlite3, conexion


def validoDNI(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
               and tabla[int(dni) % 23] == dig_control
    return False


def clearEntrys():
    for i in range(len(variables.filacli)):
        variables.filacli[i].set_text('')
    variables.lnltitlecliente.set_text("Nuevo Cliente")
    variables.lbldnivalidated.set_text('')


def insertarCliente(registro):
    try:
        conexion.cur.execute("insert into clientes(dni, apel, nome, data) values (?,?,?,?)", registro)
        conexion.connect.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def bajaCliente(dni):
    try:
        conexion.cur.execute("delete from clientes where dni = ?", (dni,))
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def listarcli():
    try:
        conexion.cur.execute("select dni, apel, nome, data from clientes")
        listado = conexion.cur.fetchall()
        conexion.connect.commit()
        return listado
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def modifcli(registro, id):
    try:
        conexion.cur.execute("update clientes set dni=?, apel= ?, nome=?, data = ? where id = ?",
                             (registro[0], registro[1], registro[2], registro[3], id))
        conexion.connect.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def ponerListadoEnGUI():
    variables.listclientes.clear()
    clearEntrys()
    for registro in listarcli():
        variables.listclientes.append(registro)


def cogerIdCliente(dni):
    try:
        conexion.cur.execute("select id from clientes where dni = ?", (dni,))
        id = conexion.cur.fetchall()
        conexion.connect.commit()
        return id
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()

def leerDatosCli():
    try:
        conexion.cur.execute("select dni, apel, nome, data from clientes where dni = ?", (variables.filares[0].get_text(),))
        filacli = conexion.cur.fetchall()[0]
        conexion.connect.commit()
        resul = (
            'Cliente: ' + str(filacli[0]),
            str(filacli[2]) + ' ' + str(filacli[1]),
        )
        return resul
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()