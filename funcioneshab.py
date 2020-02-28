# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import variables, sqlite3, conexion, funcionesres


def clearEntrys():
    variables.filahab[0].set_text('')
    variables.filahab[1][1].set_active(True)
    variables.filahab[2].set_text('')


def insertarhab(registro):
    try:
        conexion.cur.execute("insert into habitaciones(id, tipo, prezo) values (?,?,?)", registro)
        conexion.connect.commit()
        funcionesres.ponerListadoEnGUI()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def bajahab(id):
    try:
        conexion.cur.execute("delete from habitaciones where id = ?", (id,))
        funcionesres.ponerListadoEnGUI()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def listarhab():
    try:
        conexion.cur.execute("select id, tipo, prezo from habitaciones")
        listado = conexion.cur.fetchall()
        conexion.connect.commit()
        return listado
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def modifhab(registro):
    try:
        conexion.cur.execute("update habitaciones set tipo= ?, prezo=? where id = ?",
                             (registro[1], registro[2], registro[0]))
        conexion.connect.commit()
        funcionesres.ponerListadoEnGUI()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()

def prezohab(hab):
    try:
        conexion.cur.execute("select prezo from habitaciones where id = ?", (hab,))
        prezo = conexion.cur.fetchone()
        conexion.connect.commit()
        return prezo
    except sqlite3.OperationalError as e:
        print("Error: ", e)

def ponerListadoEnGUI():
    variables.listhab.clear()
    clearEntrys()
    for registro in listarhab():
        variables.listhab.append(registro)
