# coding=utf-8
from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import variables, sqlite3, conexion


def clearEntrys():
    variables.filares[0].set_text('')
    variables.filares[1].set_text('')
    variables.filares[2].set_active(-1)
    variables.filares[3].set_text('')
    variables.filares[4].set_text('')
    variables.filares[5].set_text('')
    variables.reserva = -1


def ponerListadoEnGUI():
    variables.listres.clear()
    variables.listhabnum.clear()
    clearEntrys()
    for registro in listarres():
        variables.listres.append(registro)
    for registro in listarnumhab():
        variables.listhabnum.append(registro)


def listarres():
    try:
        conexion.cur.execute("select id, cliente, habitacion, checkin, checkout, noches from reservas")
        listado = conexion.cur.fetchall()
        conexion.connect.commit()
        return listado
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def calcularnoches():
    try:
        diain = variables.filares[3].get_text()
        date_in = datetime.strptime(diain, '%d/%m/%Y').date()
        diaout = variables.filares[4].get_text()
        date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
        noches = (date_out - date_in).days
        if noches <= 0:
            variables.filares[5].set_text("Inválido")
        else:
            variables.filares[5].set_text(str(noches))
    except Exception:
        pass


def listarnumhab():
    try:
        conexion.cur.execute("select id from habitaciones")
        listado = conexion.cur.fetchall()
        conexion.connect.commit()
        return listado
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def insertarres(registro):
    try:
        if fechasdisponibles(registro[1], registro[2], registro[3]):
            conexion.cur.execute(
                "insert into reservas(cliente, habitacion, checkin, checkout, noches, regimen, parking, "
                "personas) values (?,?,?,?,?, 'alojamiento', 'no', 1)", registro)
            conexion.connect.commit()
        else:
            print(' fechas no disponibles')

    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()


def cogerapel(dni):
    try:
        conexion.cur.execute("select apel from clientes where dni = ?", (dni,))
        apel = conexion.cur.fetchone()
        conexion.connect.commit()
        return apel
    except sqlite3.OperationalError as e:
        print("Error: ", e)


def eliminar():
    try:
        conexion.cur.execute("delete from reservas where id = ?", (variables.reserva,))
        apel = conexion.cur.fetchone()
        conexion.connect.commit()
        return apel
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()

def modificar(registro):
    try:
        conexion.cur.execute("update reservas set checkin = ?, checkout = ?, noches = ? "
                             "where id = ?",
                             (registro[0], registro[1], registro[2], variables.reserva))
        conexion.connect.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.connect.rollback()

def fechasdisponibles(hab, cin, cout):
    try:
        conexion.cur.execute("select checkin, checkout from reservas where habitacion = ?", (hab,))
        reservas = conexion.cur.fetchall()
        conexion.connect.commit()

        fa = datetime.strptime(cin, '%d/%m/%Y')
        fb = datetime.strptime(cout, '%d/%m/%Y')
        for r in reservas:
            f1 = datetime.strptime(r[0], '%d/%m/%Y')
            f2 = datetime.strptime(r[1], '%d/%m/%Y')
            if f2 <= fa:
                pass
            elif f1 >= fb:
                pass
            else:
                return False

        return True
    except Exception as e:
        print(e)
