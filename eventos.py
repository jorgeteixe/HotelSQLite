# coding=utf-8
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexion
import variables
import funcionescli
import funcionesser
import funcioneshab
import funcionesres
from subprocess import call
import zipfile
import datetime
import os
import xlrd
import xlwt
import facturatron


class Eventos():
    '''
    Eventos generales
    '''

    def on_wMain_destroy(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_btnToolSalir_clicked(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    '''
    Eventos clientes
    '''

    def on_btnAltaCli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '' and apel != '' and nome != '':
                if funcionescli.validoDNI(dni):
                    funcionescli.insertarCliente(registro)
                    funcionescli.ponerListadoEnGUI()
                else:
                    print('DNI no válido.')
            else:
                print('Algún campo está vacío')
        except Exception as e:
            print('Detalles: ', e)

    def on_treeClientes_cursor_changed(self, widget):
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla
            # iter es el numero que identifica la fila que marcamos
            if iter is not None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata == None:
                    sdata = ''
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.id = funcionescli.cogerIdCliente(sdni)[0]
                variables.lnltitlecliente.set_text("Cliente "+str(variables.id[0]))
                variables.filares[0].set_text(str(sdni))
                variables.filares[1].set_text(str(sapel))

        except Exception as e:
            print('Detalles: ', e)

    def on_entDni_key_release_event(self, widget, arg):
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.validoDNI(dni):
                variables.lbldnivalidated.set_text('✅')
            else:
                variables.lbldnivalidated.set_text('❌')
        except Exception as e:
            print('Detalles: ', e)

    def on_btnBajaCli_clicked(self, widget):
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla
            # iter es el numero que identifica la fila que marcamos
            if iter is not None:
                sdni = model.get_value(iter, 0)
                funcionescli.bajaCliente(sdni)
                funcionescli.ponerListadoEnGUI()
        except Exception as e:
            print('Detalles: ', e)

    def on_btnModificarCli_clicked(self, widget):
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '' and apel != '' and nome != '':
                if funcionescli.validoDNI(dni):
                    funcionescli.modifcli(registro, variables.id[0])
                    funcionescli.ponerListadoEnGUI()
                else:
                    print('DNI no válido.')
            else:
                print('Algún campo está vacío')
        except Exception as e:
            print('Detalles: ', e)

    def on_btnCalendar_clicked(self, widget):
        try:
            variables.wcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.wcalendar.show()
            variables.caldata.select_day(datetime.datetime.date(datetime.datetime.now()).day)
            variables.caldata.select_month(datetime.datetime.date(datetime.datetime.now()).month - 1,
                                           datetime.datetime.date(datetime.datetime.now()).year)
            variables.campofecha = 0
        except Exception as e:
            print('Detalles: ', e)

    def on_calData_day_selected_double_click(self, widget):
        try:
            ano, mes, dia = variables.caldata.get_date()
            if variables.campofecha == 0:
                variables.filacli[3].set_text(str(dia).zfill(2)+"/"+str(mes+1).zfill(2)+"/"+str(ano))
            elif variables.campofecha == 1:
                variables.filares[3].set_text(str(dia).zfill(2) + "/" + str(mes+1).zfill(2) + "/" + str(ano))
            elif variables.campofecha == 2:
                variables.filares[4].set_text(str(dia).zfill(2) + "/" + str(mes+1).zfill(2) + "/" + str(ano))

            variables.wcalendar.hide()
        except Exception as e:
            print('Detalles: ', e)

    def on_btnAltaHab_clicked(self, widget):
        try:
            num = variables.filahab[0].get_text()

            if variables.filahab[1][0].get_active():
                tipo = 'Simple'
            if variables.filahab[1][1].get_active():
                tipo = 'Double'
            if variables.filahab[1][2].get_active():
                tipo = 'Family'

            prezo = variables.filahab[2].get_text()
            registro = (num, tipo, prezo)
            if num != '' and tipo != '' and prezo != '':
                funcioneshab.insertarhab(registro)
                funcioneshab.ponerListadoEnGUI()
            else:
                print('Algún campo está vacío')
        except Exception as e:
            print('Detalles: ', e)

    def on_btnBajaHab_clicked(self, widget):
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            # model es el modelo de la tabla
            # iter es el numero que identifica la fila que marcamos
            if iter is not None:
                sid = model.get_value(iter, 0)
                funcioneshab.bajahab(sid)
                funcioneshab.ponerListadoEnGUI()
        except Exception as e:
            print('Detalles: ', e)

    def on_btnModificarHab_clicked(self, widget):
        try:
            id = variables.filahab[0].get_text()
            if variables.filahab[1][0].get_active():
                tipo = 'Simple'
            if variables.filahab[1][1].get_active():
                tipo = 'Double'
            if variables.filahab[1][2].get_active():
                tipo = 'Family'
            prezo = variables.filahab[2].get_text()
            registro = (id, tipo, prezo)
            print(registro)
            if id != '' and tipo != '' and prezo != '':
                funcioneshab.modifhab(registro)
                funcioneshab.ponerListadoEnGUI()
            else:
                print('Algún campo está vacío')
        except Exception as e:
            print('Detalles: ', e)

    def on_treeHabitaciones_cursor_changed(self, widget):
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            # model es el modelo de la tabla
            # iter es el numero que identifica la fila que marcamos
            if iter is not None:
                sid = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprezo = model.get_value(iter, 2)
                variables.filahab[0].set_text(str(sid))
                variables.filahab[2].set_text(str(sprezo))
                if stipo == 'Simple':
                    variables.filahab[1][0].set_active(True)
                if stipo == 'Double':
                    variables.filahab[1][1].set_active(True)
                if stipo == 'Family':
                    variables.filahab[1][2].set_active(True)

        except Exception as e:
            print('Detalles: ', e)


    def on_btnCalculator_clicked(self, widget):
        call('gnome-calculator')

    def on_btnToolClientes_clicked(self, widget):
        variables.notebook.set_current_page(0)

    def on_btnToolHabitaciones_clicked(self, widget):
        variables.notebook.set_current_page(2)

    def on_btnPrintTool_clicked(self, widget):
        if variables.header_preview[2].get_text() != '':
            facturatron.factura()

    def on_btnToolReservas_clicked(self, widget):
        variables.notebook.set_current_page(1)

    def on_btnToolClean_clicked(self, widget):
        funcionescli.clearEntrys()
        funcioneshab.clearEntrys()
        funcionesres.clearEntrys()
        funcionesser.clearEntries()
        variables.preview.hide()

    def on_btnCerrarAcercaDe_clicked(self, widget):
        variables.wabout.hide()

    def on_menuAcercaDe_activate(self, widget):
        variables.wabout.connect('delete-event', lambda w, e: w.hide() or True)
        variables.wabout.show()

    def on_menuSalir_activate(self, widget):
        conexion.Conexion().cerrarbbdd()
        Gtk.main_quit()

    def on_btnFileSalir_clicked(self, widget):
        variables.wselectfile.hide()

    def on_menuBackup_activate(self, widget):
        variables.wselectfile.connect('delete-event', lambda w, e: w.hide() or True)
        variables.wselectfile.show()

    def on_btnFileBackup_clicked(self, widget):
        '''GUARDAMOS ESTADO ACTUAL PARA EVITAR PERDIDAS'''
        print('Cerrando conexión para crear copia.')
        try:
            bdname = 'empresa.sqlite'
            conexion.Conexion.cerrarbbdd(self)
            endname = 'copia.zip'
            destino = './.papelera/'
            if not os.path.exists(destino):
                os.system('mkdir ' + destino)
                os.system('chmod 777 ' + destino)
            copia = zipfile.ZipFile(endname, 'w')
            copia.write('empresa.sqlite', compress_type=zipfile.ZIP_DEFLATED)
            copia.close()
            finalname = 'archivo-borrado.zip'
            os.rename(endname, finalname)
            os.system('mv "' + finalname + '" ' + destino)
            '''RESTAURAMOS ARCHIVO'''
            os.system('rm '+bdname)
            print('bd borrada')
            backupfilenametorestore = variables.wselectfile.get_filename()
            print(backupfilenametorestore)
            os.system('unzip "'+backupfilenametorestore+'" -d .')
            print('Copia creada satistactoriamente, volviendo a conectar.')
            conexion.Conexion.abrirbbdd(self)
            funcionescli.ponerListadoEnGUI()
            funcioneshab.ponerListadoEnGUI()
        except Exception as e:
            print('Error en la restauración')



    def on_btnToolBackup_clicked(self, widget):
        print('Cerrando conexión para crear copia.')
        try:
            conexion.Conexion.cerrarbbdd(self)
            endname = 'copia.zip'
            destino = './backups/'
            if not os.path.exists(destino):
                os.system('mkdir '+destino)
                os.system('chmod 777 '+destino)
            fecha = datetime.datetime.now()
            copia = zipfile.ZipFile(endname, 'w')
            copia.write('empresa.sqlite', compress_type = zipfile.ZIP_DEFLATED)
            copia.close()
            finalname = str(fecha) + '-copia.zip'
            os.rename(endname, finalname)
            os.system('mv "'+finalname+'" '+destino)
            print('Copia creada satistactoriamente, volviendo a conectar.')
            conexion.Conexion.abrirbbdd(self)
        except Exception as e:
            print('Error en el backup')
            e.with_traceback()

    def on_wSelectFile_selection_changed(self, widget):
        file = os.path.basename(str(variables.wselectfile.get_filename()))
        variables.lblfileselected.set_text(file)
        if file == str(None):
            variables.lblfileselected.set_text('')

    def on_btnCalendarIn_clicked(self, widget):
        try:
            variables.wcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.wcalendar.show()
            campo = variables.filares[3].get_text()
            if campo != '':
                variables.caldata.select_day(datetime.datetime.strptime(campo, '%d/%m/%Y').date().day)
                variables.caldata.select_month(datetime.datetime.strptime(campo, '%d/%m/%Y').date().month - 1,
                                               datetime.datetime.strptime(campo, '%d/%m/%Y').date().year)
            else:
                variables.caldata.select_day(datetime.datetime.date(datetime.datetime.now()).day)
                variables.caldata.select_month(datetime.datetime.date(datetime.datetime.now()).month - 1,
                                               datetime.datetime.date(datetime.datetime.now()).year)
            variables.campofecha = 1
        except Exception as e:
            print('Detalles: ', e)

    def on_btnCalendarOut_clicked(self, widget):
        try:
            variables.wcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.wcalendar.show()
            variables.wcalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.wcalendar.show()
            campo = variables.filares[4].get_text()
            campo2 = variables.filares[3].get_text()
            if campo != '':
                variables.caldata.select_day(datetime.datetime.strptime(campo, '%d/%m/%Y').date().day)
                variables.caldata.select_month(datetime.datetime.strptime(campo, '%d/%m/%Y').date().month - 1,
                                               datetime.datetime.strptime(campo, '%d/%m/%Y').date().year)
            elif campo2 != '':
                variables.caldata.select_day(datetime.datetime.strptime(campo2, '%d/%m/%Y').date().day)
                variables.caldata.select_month(datetime.datetime.strptime(campo2, '%d/%m/%Y').date().month - 1,
                                               datetime.datetime.strptime(campo2, '%d/%m/%Y').date().year)
            else:
                variables.caldata.select_day(datetime.datetime.date(datetime.datetime.now()).day)
                variables.caldata.select_month(datetime.datetime.date(datetime.datetime.now()).month - 1,
                                               datetime.datetime.date(datetime.datetime.now()).year)
            variables.campofecha = 2
        except Exception as e:
            print('Detalles: ', e)

    def on_btnReserva_clicked(self, widget):
        try:
            dni = variables.filares[0].get_text()
            hab = variables.filares[2].get_model()[variables.filares[2].get_active()][0]
            chin = variables.filares[3].get_text()
            chout = variables.filares[4].get_text()
            noches = variables.filares[5].get_text()
            registro = (dni, hab, chin, chout, noches)
            if dni != '' and hab != '' and chin != '' and chout != '' and noches != '':
                funcionesres.insertarres(registro)
                funcionesres.ponerListadoEnGUI()
        except Exception as e:
            print('Detalles: ', e)

    def on_btnCheckIn_clicked(self, widget):
        variables.filares[3].set_text(datetime.date.today().strftime('%d/%m/%Y'))

    def on_btnCheckOut_clicked(self, widget):
        variables.filares[4].set_text(datetime.date.today().strftime('%d/%m/%Y'))

    def on_btnModificarReserva_clicked(self, widget):
        try:
            chin = variables.filares[3].get_text()
            chout = variables.filares[4].get_text()
            noches = variables.filares[5].get_text()
            registro = (chin, chout, noches)
            if chin != '' and chout != '' and noches != '':
                funcionesres.modificar(registro)
                funcionesres.ponerListadoEnGUI()
        except Exception as e:
            print('Detalles: ', e)

    def on_btnEliminarReserva_clicked(self, widget):
        if variables.reserva != -1:
            funcionesres.eliminar()
            funcionesres.ponerListadoEnGUI()

    def on_treeReservas_cursor_changed(self, widget):
        try:
            for i in range(14):
                for e in range(4):
                    variables.list_preview[i][e].set_text('')

            model, iter = variables.treeres.get_selection().get_selected()
            if iter is not None:
                scod = model.get_value(iter, 0)
                sdni = model.get_value(iter, 1)
                shab = model.get_value(iter, 2)
                sin = model.get_value(iter, 3)
                sout = model.get_value(iter, 4)
                snoches = model.get_value(iter, 5)
                variables.filares[0].set_text(str(sdni))
                variables.filares[1].set_text(str(funcionesres.cogerapel(sdni)[0]))
                lista = funcionesres.listarnumhab()
                m = -1
                for i, x in enumerate(lista):
                    if str(x[0]) == str(shab):
                        m = i
                variables.filares[2].set_active(m)
                variables.filares[3].set_text(str(sin))
                variables.filares[4].set_text(str(sout))
                variables.filares[5].set_text(str(snoches))
                variables.reserva = scod
                variables.header_preview[0].set_text(funcionesres.cogerapel(sdni)[0])
                variables.header_preview[1].set_text(str(sout))
                variables.header_preview[2].set_text(str(scod))
                variables.header_preview[3].set_text(str(shab))

                variables.list_preview[0][0].set_text('Alojamiento')
                variables.list_preview[0][1].set_text(str(snoches))
                variables.list_preview[0][2].set_text(str(float(funcioneshab.prezohab(shab)[0])))
                variables.list_preview[0][3].set_text(str(round(float(funcioneshab.prezohab(shab)[0])*float(snoches), 2)))

                funcionesser.listarServiciosEnPreview()
                variables.preview.show()
                funcionesser.ponerListadoEnGUI()

        except Exception as e:
            print('Detalles: ', e)

    def on_entCheckOut_changed(self, widget):
        funcionesres.calcularnoches()

    def on_entCheckIn_changed(self, widget):
        funcionesres.calcularnoches()

    def on_btnPrintFactura_clicked(self, widget):
        facturatron.factura()

    def on_btnToolServicios_clicked(self, widget):
        variables.notebook.set_current_page(3)

    def on_btnBajaSer_clicked(self, widget):
        if variables.header_preview[2].get_text() != '':
            try:
                concepto = variables.selectedservizo
                if concepto != '':
                    funcionesser.eliminarServizo(concepto)
                    funcionesser.ponerListadoEnGUI()
            except Exception as e:
                print('Detalles: ', e)

    def on_btnGuardarSer_clicked(self, widget):
        if variables.header_preview[2].get_text() != '':
            try:
                if variables.rgservicios[0].get_active():
                    regimen = 'alojamiento'
                elif variables.rgservicios[1].get_active():
                    regimen = 'desayuno'
                else:
                    regimen = 'mp'
                if variables.chkparking.get_active():
                    parking = 'si'
                else:
                    parking = 'no'
                personas = int(variables.entcantpersonas.get_text())
                if personas <= 0:
                    print('error no puede haber 0 personas o menos')
                else:
                    funcionesser.actualizarReserva(regimen, parking, personas)
                funcionesser.listarServiciosEnPreview()
            except Exception as e:
                print('Detalles: ', e)

    def on_btnAddSer_clicked(self, widget):
        if variables.header_preview[2].get_text() != '':
            try:
                concepto = variables.serconcepto.get_text()
                prezo = float(variables.serprezo.get_text())
                prezo = str(prezo)
                if concepto != '' and float(prezo) > 0:
                    funcionesser.insertarServizo(concepto, prezo)
                    funcionesser.ponerListadoEnGUI()
                    funcionesser.listarServiciosEnPreview()
            except Exception as e:
                print('Detalles: ', e)

    def on_treeServizos_cursor_changed(self, widget):
        model, iter = variables.treeser.get_selection().get_selected()
        if iter is not None:
            concepto = model.get_value(iter, 0)
            prezo = model.get_value(iter, 1)
            variables.selectedservizo = concepto

    def on_excelImport_activate(self, widget):
        try:
            # Excel workbook has to be on the main directory and it will automatically import all rows if no error found
            document = xlrd.open_workbook("listadoclientes.xls")  # Searches for this filename always.
            clientes = document.sheet_by_index(0)
            for i in range(1, clientes.nrows + 1):
                fila = clientes.row_values(i)
                funcionescli.insertarCliente((str(fila[0]), str(fila[1]), str(fila[2]),
                                              xlrd.xldate.xldate_as_datetime(int(fila[3]), 0).strftime("%d/%m/%Y")))
                funcionescli.ponerListadoEnGUI()
        except Exception as e:
            print('Detalles: ', e)

    def on_excelExport_activate(self, widget):
        try:
            listado = funcionescli.listarcli()
            book = xlwt.Workbook()
            sheet = book.add_sheet('sheet_clients', cell_overwrite_ok=True)
            sheet.write(0, 0, 'DNI')
            sheet.write(0, 1, 'Apelidos')
            sheet.write(0, 2, 'Nome')
            sheet.write(0, 3, 'Data')
            for r in range(1, len(listado)):
                for c in range(0, 4):
                    sheet.write(r, c, listado[r][c])
            book.save('test_clientes.xls')
        except Exception as e:
            print('Detalles: ', e)

    def on_editarPrecios_activate(self, widget):
        try:
            variables.wselectprecios.connect('delete-event', lambda w, e: w.hide() or True)
            variables.wselectprecios.show()
            resultado = funcionesser.cogerPreciosDefecto()
            variables.precios[0].set_text(str(resultado[0]))
            variables.precios[1].set_text(str(resultado[1]))
            variables.precios[2].set_text(str(resultado[2]))
        except Exception as e:
            print('Detalles: ', e)

    def on_btnPreciosGuardar_clicked(self, widget):
        try:
            desayuno = float(variables.precios[0].get_text())
            mediap = float(variables.precios[1].get_text())
            parking = float(variables.precios[2].get_text())
            if desayuno > 0 and mediap > 0 and parking > 0:
                conexion.cur.execute("update precios set desayuno = ?, media_pension = ?, parking = ? where id = 1",
                                     (desayuno, mediap, parking))
                conexion.connect.commit()
            variables.wselectprecios.hide()
            funcionesser.listarServiciosEnPreview()
        except Exception as e:
            print('Detalles:', e)
            conexion.connect.rollback()
