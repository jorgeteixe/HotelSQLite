# coding=utf-8
import conexion
import eventos
import variables
import funcionescli
import funcioneshab
import funcionesres
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

'''
El main contiene los elementos necesarios para lanzar la aplicación
así como la declaracion de los widgets que se usarán. También los módulos
que tenemos que importar de las librerías gráficas.
'''


class Empresa:
    def __init__(self):
        b = Gtk.Builder()
        b.add_from_file('glades/hotel.glade')
        self.wmain = b.get_object('wMain')

        # Widgets

        self.entdni = b.get_object('entDni')
        self.entapel = b.get_object('entApel')
        self.entnome = b.get_object('entNome')
        self.entdata = b.get_object('entData')
        variables.filacli = (self.entdni, self.entapel, self.entnome, self.entdata)
        variables.listclientes = b.get_object('listClientes')
        variables.treeclientes = b.get_object('treeClientes')

        variables.lbldnivalidated = b.get_object('lblDniValidated')
        variables.lnltitlecliente = b.get_object('lblTitleCliente')

        variables.wcalendar = b.get_object('wCalendar')
        variables.caldata = b.get_object('calData')

        variables.listhab = b.get_object('listHabitaciones')
        variables.treehab = b.get_object('treeHabitaciones')

        self.entnumhab = b.get_object('entNumeroHab')
        self.rdsingle = b.get_object('rdSingle')
        self.rddouble = b.get_object('rdDouble')
        self.rdfamily = b.get_object('rdFamily')
        self.entprezohab = b.get_object('entPrecioHab')
        variables.filahab = (self.entnumhab, (self.rdsingle, self.rddouble, self.rdfamily), self.entprezohab)

        variables.notebook = b.get_object('notebook')
        variables.wabout = b.get_object('wAbout')
        variables.wselectfile = b.get_object('wSelectFile')
        variables.lblfileselected = b.get_object('lblRestoreFileName')

        self.resdni = b.get_object('lblReservaDni')
        self.resapel = b.get_object('lblReservaApellido')
        self.reshab = b.get_object('cmbReservaHabitaciones')
        self.resin = b.get_object('entCheckIn')
        self.resout = b.get_object('entCheckOut')
        self.resnoches = b.get_object('lblReservaNoches')
        variables.filares = (self.resdni, self.resapel, self.reshab, self.resin, self.resout, self.resnoches)
        variables.treeres = b.get_object('treeReservas')
        variables.listres = b.get_object('listReservas')
        variables.listhabnum = b.get_object('listHabNum')

        variables.btnreserva = b.get_object('btnReserva')
        variables.preview = b.get_object('facturacion')
        variables.preview.hide()

        variables.header_preview = (
            b.get_object('nombreCliente'),
            b.get_object('fechaReserva'),
            b.get_object('numeroReserva'),
            b.get_object('habitacionReserva'),
        )
        variables.list_preview = (
            (b.get_object('concepto1'), b.get_object('cant1'), b.get_object('precio1'), b.get_object('total1')),
            (b.get_object('concepto2'), b.get_object('cant2'), b.get_object('precio2'), b.get_object('total2')),
            (b.get_object('concepto3'), b.get_object('cant3'), b.get_object('precio3'), b.get_object('total3')),
            (b.get_object('concepto4'), b.get_object('cant4'), b.get_object('precio4'), b.get_object('total4')),
            (b.get_object('concepto5'), b.get_object('cant5'), b.get_object('precio5'), b.get_object('total5')),
            (b.get_object('concepto6'), b.get_object('cant6'), b.get_object('precio6'), b.get_object('total6')),
            (b.get_object('concepto7'), b.get_object('cant7'), b.get_object('precio7'), b.get_object('total7')),
            (b.get_object('concepto8'), b.get_object('cant8'), b.get_object('precio8'), b.get_object('total8')),
            (b.get_object('concepto9'), b.get_object('cant9'), b.get_object('precio9'), b.get_object('total9')),
            (b.get_object('concepto10'), b.get_object('cant10'), b.get_object('precio10'), b.get_object('total10')),
            (b.get_object('concepto11'), b.get_object('cant11'), b.get_object('precio11'), b.get_object('total11')),
            (b.get_object('concepto12'), b.get_object('cant12'), b.get_object('precio12'), b.get_object('total12')),
            (b.get_object('concepto13'), b.get_object('cant13'), b.get_object('precio13'), b.get_object('total13')),
            (b.get_object('concepto14'), b.get_object('cant14'), b.get_object('precio14'), b.get_object('total14')),
        )
        variables.footer_preview = (
            b.get_object('base'),
            b.get_object('iva'),
            b.get_object('total'),
        )
        variables.treeser = b.get_object('treeServizos')
        variables.listser = b.get_object('listServizos')
        variables.rgservicios = (
            b.get_object('rdAlojamiento'),
            b.get_object('rdDesayuno'),
            b.get_object('rdMediaPension')
        )
        variables.entcantpersonas = b.get_object('entPersonas')
        variables.chkparking = b.get_object('chkParking')
        variables.serconcepto = b.get_object('entConcepto')
        variables.serprezo = b.get_object('entPrezoSer')

        variables.wselectprecios = b.get_object('wSetPrecios')

        variables.precios = (
            b.get_object('entPrecioDesayuno'),
            b.get_object('entPrecioMediaPension'),
            b.get_object('entPrecioParking'),
        )

        variables.lbldialog = b.get_object('lblDialog')
        variables.wdialog = b.get_object('wDialog')


        b.connect_signals(eventos.Eventos())
        self.wmain.show()
        conexion.Conexion().abrirbbdd()
        funcionescli.ponerListadoEnGUI()
        funcioneshab.ponerListadoEnGUI()
        funcionesres.ponerListadoEnGUI()


if __name__ == '__main__':
    main = Empresa()
    Gtk.main()
