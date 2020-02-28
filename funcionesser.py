# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import variables
import sqlite3
import conexion


def clearEntries():
    variables.rgservicios[0].set_active(True)
    variables.entcantpersonas.set_text('0')
    variables.chkparking.set_active(False)
    variables.serconcepto.set_text('')
    variables.serprezo.set_text('0')
    variables.selectedservizo = ''


def ponerListadoEnGUI():
    variables.listser.clear()
    clearEntries()
    for registro in listarser():
        variables.listser.append(registro)
    reg = selectInfoReserva()[0]
    regimen = str(reg[0])
    parking = str(reg[1])
    personas = str(reg[2])
    if regimen == 'alojamiento':
        variables.rgservicios[0].set_active(True)
    elif regimen == 'desayuno':
        variables.rgservicios[1].set_active(True)
    elif regimen == 'mp':
        variables.rgservicios[2].set_active(True)
    if parking == 'si':
        variables.chkparking.set_active(True)
    else:
        variables.chkparking.set_active(False)
    variables.entcantpersonas.set_text(personas)


def listarser():
    try:
        conexion.cur.execute("select concepto, precio from servicios where reserva = ?",
                             (variables.header_preview[2].get_text(),))
        listado = conexion.cur.fetchall()
        conexion.connect.commit()
        return listado
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def selectTipoHab(chab):
    try:
        conexion.cur.execute("select tipo from habitaciones where id = ?", (chab,))
        tipo = conexion.cur.fetchone()
        conexion.connect.commit()
        return tipo
    except sqlite3.OperationalError as e:
        print("Error: ", e)


def selectInfoReserva():
    try:
        conexion.cur.execute("select regimen, parking, personas from reservas where id = ?",
                         (variables.header_preview[2].get_text(),))
        registro = conexion.cur.fetchall()
        conexion.connect.commit()
        return registro
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def actualizarReserva(regimen, parking, personas):
    try:
        conexion.cur.execute("update reservas set regimen = ?, parking = ?, personas = ? where id = ?",
                             (regimen, parking, personas, variables.header_preview[2].get_text()))
        registro = conexion.cur.fetchall()
        conexion.connect.commit()
        return registro
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def insertarServizo(concepto, prezo):
    try:
        conexion.cur.execute("insert into servicios(reserva, concepto, precio) values (?, ?, ?)",
                             (variables.header_preview[2].get_text(), concepto, prezo))
        conexion.connect.commit()
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def eliminarServizo(concepto):
    try:
        conexion.cur.execute("delete from servicios where reserva = ? and concepto = ?",
                             (variables.header_preview[2].get_text(), concepto))
        conexion.connect.commit()
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        conexion.connect.rollback()


def cogerPreciosDefecto():
    try:
        conexion.cur.execute("select desayuno, media_pension, parking from precios where id = 1")
        return conexion.cur.fetchone()
    except Exception as e:
        print('Detalles: ', e)


def listarServiciosEnPreview():
    try:
        for i in range(12):
            for e in range(4):
                variables.list_preview[i+1][e].set_text('')
        index = 1
        infoReserva = selectInfoReserva()[0]
        listaServizos = listarser()
        defaultPrecios = cogerPreciosDefecto()
        iva = float(variables.list_preview[0][3].get_text()) * 0.1
        if infoReserva[0] == 'desayuno':
            variables.list_preview[index][0].set_text('Desayuno')
            variables.list_preview[index][1].set_text(str(int(infoReserva[2])))
            variables.list_preview[index][2].set_text(str(float(defaultPrecios[0])))
            variables.list_preview[index][3].set_text(str(float(round(float(
                int(infoReserva[2]))*float(variables.list_preview[index][2].get_text()), 2))))
            iva += float(variables.list_preview[index][3].get_text()) * 0.1
            index += 1
        elif infoReserva[0] == 'mp':
            variables.list_preview[index][0].set_text('Media pensión')
            variables.list_preview[index][1].set_text(str(int(infoReserva[2])))
            variables.list_preview[index][2].set_text(str(float(defaultPrecios[1])))
            variables.list_preview[index][3].set_text(str(float(round(float(
                int(infoReserva[2]))*float(variables.list_preview[index][2].get_text()), 2))))
            iva += float(variables.list_preview[index][3].get_text()) * 0.1
            index += 1
        if infoReserva[1] == 'si':
            variables.list_preview[index][0].set_text('Parking')
            variables.list_preview[index][3].set_text(str(defaultPrecios[2]))
            iva += float(variables.list_preview[index][3].get_text()) * 0.21
            index += 1
        for servizo in listaServizos:
            variables.list_preview[index][0].set_text(servizo[0])
            variables.list_preview[index][3].set_text(servizo[1])
            iva += float(variables.list_preview[index][3].get_text()) * 0.21
            index += 1
        base = 0
        for i in range(13):
            if variables.list_preview[i][3].get_text() != '':
                base += float(variables.list_preview[i][3].get_text())
        variables.footer_preview[0].set_text(str(round(base, 2)))
        variables.footer_preview[1].set_text(str(round(iva, 2)))
        variables.footer_preview[2].set_text(str(round(base + iva, 2)) + ' €')
    except Exception as e:
        print('Detalles: ', e)
