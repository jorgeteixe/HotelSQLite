# coding=utf-8
import os
import traceback
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import conexion
import funcioneshab
import funcionesser
import variables
import funcionescli
import funcionesres

x_size = 595.275590551181
y_size = 841.8897637795275
margin_h = 50
pos = 0

def basico(factura = True, file = 'factura.pdf', first = True, bill = None):
    try:
        if first:
            bill = canvas.Canvas(file, pagesize=A4)
        subtitle = 'Si no le ha gustado, no vuelva. Pero no deje mala nota en TripAdvisor.'
        bill.setFont('Helvetica-Bold', size=16)
        bill.drawCentredString(x_size/2, 800, 'HOTEL LITE')
        bill.setFont('Times-Italic', size=10)
        bill.drawCentredString(x_size/2, 785, subtitle)
        bill.setFont('Helvetica', size=10)
        bill.drawImage('./img/receptionist.png', margin_h, 770, width=64, height=64)
        empresa(bill, margin_h, 750)
        if factura:
            cliente(bill, x_size - margin_h, 750 - 15)
            nFactura(bill, x_size - margin_h, 750)
        separador(bill, 750 - 15 * 4)
        textpie = 'Hotel Lite, CIF = B65432154 Tlfo = 981763481 mail = hotelite@sqlite.es'
        bill.setFont('Times-Italic', size=8)
        bill.drawString(170, 20, textpie)
        separador(bill, 30)
        return bill
    except Exception:
        traceback.print_exc()

def datosReserva(bill):
    # Titulo reserva
    lineas = []
    ancho = (x_size - 2 * margin_h) / 4 + 10
    bill.setFont('Helvetica-Bold', size=10)
    bill.drawString(13 + margin_h, 677, "CONCEPTO")
    bill.drawString(13 + margin_h + ancho, 677, "CANTIDAD")
    bill.drawString(13 + margin_h + 2 * ancho, 677, "PRECIO/UD")
    bill.drawString(13 + margin_h + 3 * ancho, 677, "TOTAL")
    separador(bill, 670)
    bill.setFont('Helvetica', size=10)
    infoRes = funcionesser.selectInfoReserva()[0]
    precios = funcionesser.cogerPreciosDefecto()
    npersonas = infoRes[2]
    lineas.append([
        "Alojamiento",
        str(variables.list_preview[0][1].get_text()),
        str(funcioneshab.prezohab(variables.header_preview[3].get_text())[0]),
        str(float(variables.list_preview[0][1].get_text()) * float(funcioneshab.prezohab(variables.header_preview[3].get_text())[0]))
    ])
    regimen = infoRes[0]
    if regimen == 'desayuno':
        lineas.append([
            "Desayuno",
            str(npersonas),
            str(precios[0]),
            str(float(npersonas) * precios[0])
        ])
    if regimen == 'mp':
        lineas.append([
            "Media pensión",
            str(npersonas),
            str(precios[1]),
            str(float(npersonas) * precios[1])
        ])
    parking = infoRes[1]
    if parking == 'si':
        lineas.append([
            "Parking",
            "",
            "",
            str(precios[2])
        ])
    servizos = funcionesser.listarser()
    for ser in servizos:
        lineas.append([
            ser[0],
            '',
            '',
            ser[1]
        ])
    y = 655
    for line in lineas:
        x = 13 + margin_h
        bill.drawString(x, y, line[0])
        x += ancho + 30
        bill.drawRightString(x, y, line[1])
        x += ancho
        if line[2] != '':
            txt = "{0:.2f}".format(float(line[2]))
            if txt != '':
                txt += ' €'
            bill.drawRightString(x + 10, y, txt)
        x += ancho
        bill.drawRightString(x, y, "{0:.2f}".format(float(line[3])) + " €")
        x += ancho
        y -= 15

    totalx1 = x_size / 2 + margin_h
    totalx2 = x_size - margin_h
    totaly1 = 100
    totaly2 = 160

    bill.line(totalx1, totaly1, totalx2, totaly1)
    bill.line(totalx1, totaly2, totalx2, totaly2)
    bill.line(totalx1, totaly1, totalx1, totaly2)
    bill.line(totalx2, totaly1, totalx2, totaly2)

    subtotal = 0
    iva = 0
    for line in lineas:
        subtotal += float(line[3])
    iva += float(line[3]) * 0.1
    for line in lineas[1:]:
        iva += float(line[3]) * 0.21
    total = subtotal + iva
    subtotal = "{0:.2f}".format(subtotal)
    iva = "{0:.2f}".format(iva)
    total = "{0:.2f}".format(total)
    bill.setFont('Helvetica', size=12)
    bill.drawRightString((totalx1 + totalx2) / 2 - 15, totaly2 - 15 - 3, "Subtotal: ")
    bill.drawRightString((totalx1 + totalx2) / 2 + 40, totaly2 - 15 - 3, subtotal + " €")

    bill.drawRightString((totalx1 + totalx2) / 2 - 15, totaly2 - 30 - 3, "IVA: ")
    bill.drawRightString((totalx1 + totalx2) / 2 + 40, totaly2 - 30 - 3, iva + " €")

    bill.setFont('Helvetica-Bold', size=12)
    bill.drawRightString((totalx1 + totalx2) / 2 - 15, totaly2 - 45 - 3, "TOTAL: ")
    bill.drawRightString((totalx1 + totalx2) / 2 + 40, totaly2 - 45 - 3, total + " €")

def factura():
    try:
        bill = basico()
        datosReserva(bill)
        bill.setTitle('Factura Hotel Lite')
        bill.showPage()
        bill.save()
        directorio = os.getcwd()
        os.system('/usr/bin/open ' + directorio + '/factura.pdf')
    except Exception:
        traceback.print_exc()


def listado_entradas():
    try:
        bill = basico(factura=False, file='clientes.pdf')
        bill.setTitle('Clientes Hotel Lite')
        entrada(bill, x_size - margin_h, 750 - 15)
        # listar entradas
        entradas = listar_entradas()
        ancho = (x_size - 2 * margin_h) / 4 + 10
        bill.setFont('Helvetica-Bold', size=10)
        bill.drawString(13 + margin_h, 677, "HABITACIÓN")
        bill.drawString(13 + margin_h + ancho, 677, "ENTRADA")
        bill.drawString(13 + margin_h + 2 * ancho, 677, "SALIDA")
        bill.drawString(13 + margin_h + 3 * ancho, 677, "CLIENTE")
        bill.setFont('Helvetica', size=10)
        separador(bill, 670)
        y = 655
        for line in entradas:
            x = 13 + margin_h
            bill.drawString(x + 20, y, line[0])
            x += ancho
            bill.drawString(x, y, line[1])
            x += ancho
            bill.drawString(x - 5, y, line[2])
            x += ancho
            bill.drawString(x, y,  '***' + line[3][3:])
            x += ancho
            y -= 15


        bill.showPage()
        canvas.Canvas._pageNumber = 2
        basico(factura=False, first=False, bill=bill)
        salida(bill, x_size - margin_h, 750 - 15)
        # listar salidas
        salidas = listar_salidas()
        ancho = (x_size - 2 * margin_h) / 4 + 10
        bill.setFont('Helvetica-Bold', size=10)
        bill.drawString(13 + margin_h, 677, "HABITACIÓN")
        bill.drawString(13 + margin_h + ancho, 677, "ENTRADA")
        bill.drawString(13 + margin_h + 2 * ancho, 677, "SALIDA")
        bill.drawString(13 + margin_h + 3 * ancho, 677, "CLIENTE")
        bill.setFont('Helvetica', size=10)
        separador(bill, 670)
        y = 655
        for line in salidas:
            x = 13 + margin_h
            bill.drawString(x + 20, y, line[0])
            x += ancho
            bill.drawString(x, y, line[1])
            x += ancho
            bill.drawString(x - 5, y, line[2])
            x += ancho
            bill.drawString(x, y, '***' + line[3][3:])
            x += ancho
            y -= 15

        bill.showPage()
        bill.save()
        directorio = os.getcwd()
        os.system('/usr/bin/open ' + directorio + '/clientes.pdf')
    except Exception:
        traceback.print_exc()


def nFactura(bill, posx, posy):
    bill.setFont('Helvetica-Bold', size=10)
    bill.drawRightString(posx, posy, 'Factura: ' + variables.header_preview[2].get_text())


def cliente(bill, posx, posy):
    bill.setFont('Helvetica', size=10)
    for line in funcionescli.leerDatosCli():
        bill.drawRightString(posx, posy, line)
        posy -= 15
    bill.drawRightString(posx, posy, 'Fecha factura: ' + variables.header_preview[1].get_text())


def empresa(bill, posx, posy):
    bill.setFont('Helvetica', size=10)
    for line in variables.datos_hotel:
        bill.drawString(posx, posy, line)
        posy -= 15


def separador(bill, h):
    bill.line(margin_h, h, x_size - margin_h, h)


def entrada(bill, posx, posy):
    bill.setFont('Helvetica-Bold', size=10)
    lineas = (
        'Entradas       ',
        'Fecha: %s ' % datetime.now().strftime('%d/%m/%Y'),
    )
    for line in lineas:
        bill.drawRightString(posx, posy, line)
        bill.setFont('Helvetica', size=10)
        posy -= 15


def salida(bill, posx, posy):
    bill.setFont('Helvetica-Bold', size=10)
    lineas = (
        'Salidas       ',
        'Fecha: %s ' % datetime.now().strftime('%d/%m/%Y'),
    )
    for line in lineas:
        bill.drawRightString(posx, posy, line)
        bill.setFont('Helvetica', size=10)
        posy -= 15


def listar_salidas():
    try:
        conexion.cur.execute("select habitacion, checkin, checkout, cliente from reservas where checkout = ?", (datetime.now().strftime('%d/%m/%Y'),))
        salidas = conexion.cur.fetchall()
        conexion.connect.commit()
        return salidas
    except Exception as e:
        print('Detalles: ', e)


def listar_entradas():
    try:
        conexion.cur.execute("select habitacion, checkin, checkout, cliente from reservas where checkin = ?", (datetime.now().strftime('%d/%m/%Y'),))
        entradas = conexion.cur.fetchall()
        conexion.connect.commit()
        return entradas
    except Exception as e:
        print('Detalles: ', e)