#!/usr/bin/python
# -*- coding: utf-8 -*-
#######################################################################
###                                               Diálogo de definición de bombas, UI_pump                                                   ###
#######################################################################

from functools import partial

from PyQt4 import QtCore, QtGui

from lib.unidades import Pressure, Length, Power, VolFlow, Currency
from tools.costIndex import CostData
from equipment.parents import UI_equip
from equipment.pump import Pump
from UI import UI_corriente, bombaCurva
from UI.widgets import Entrada_con_unidades


class UI_equipment(UI_equip):
    """Diálogo de definición de bombas"""
    Equipment=Pump()
    def __init__(self, equipment=None, parent=None):
        """
        equipment: instancia de equipo inicial
        """
        super(UI_equipment, self).__init__(Pump, entrada=False, salida=False, parent=parent)
        self.curva=[0, 0, []]

        #Pestaña calculo
        gridLayout_Calculo = QtGui.QGridLayout(self.tabCalculo)
        gridLayout_Calculo.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Output Pressure")),1,1,1,1)
        self.Pout=Entrada_con_unidades(Pressure)
        self.Pout.valueChanged.connect(partial(self.cambiar_data, "Pout"))
        gridLayout_Calculo.addWidget(self.Pout,1,2,1,1)
        gridLayout_Calculo.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Pressure increase")),2,1,1,1)
        self.deltaP=Entrada_con_unidades(Pressure)
        self.deltaP.valueChanged.connect(partial(self.cambiar_data, "deltaP"))
        gridLayout_Calculo.addWidget(self.deltaP,2,2,1,1)
        gridLayout_Calculo.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Head")),3,1,1,1)
        self.Carga=Entrada_con_unidades(Length, "Head")
        self.Carga.valueChanged.connect(partial(self.cambiar_data, "Carga"))
        gridLayout_Calculo.addWidget(self.Carga,3,2,1,1)
        gridLayout_Calculo.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),4,1,1,2)
        self.usarCurva = QtGui.QCheckBox(QtGui.QApplication.translate("pychemqt", "Pump curve"))
        self.usarCurva.toggled.connect(self.usarCurvaToggled)
        gridLayout_Calculo.addWidget(self.usarCurva,5,1,2,2)
        gridLayout_Calculo.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Efficiency")),7,1,1,1)
        self.rendimiento=Entrada_con_unidades(float, min=0, max=1, spinbox=True, step=0.01)
        self.rendimiento.valueChanged.connect(partial(self.cambiar_data, "rendimiento"))
        gridLayout_Calculo.addWidget(self.rendimiento,7,2,1,1)
        gridLayout_Calculo.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),8,1,1,6)

        self.groupBox_Curva = QtGui.QGroupBox(QtGui.QApplication.translate("pychemqt", "Pump curve"))
        self.groupBox_Curva.setEnabled(False)
        gridLayout_Calculo.addWidget(self.groupBox_Curva,5,4,3,1)
        layout = QtGui.QGridLayout(self.groupBox_Curva)

        self.bottonCurva = QtGui.QPushButton(QtGui.QApplication.translate("pychemqt", "Curve"))
        self.bottonCurva.clicked.connect(self.bottonCurva_clicked)
        layout.addWidget(self.bottonCurva,1,1,1,2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Variable")),2,1,1,1)
        self.incognita=QtGui.QComboBox(self.tabCalculo)
        self.incognita.setToolTip(QtGui.QApplication.translate("pychemqt", "If use curve, it can calculate the head or the flowrate, in that case it override flow of input stream"))
        self.incognita.addItem(QtGui.QApplication.translate("pychemqt", "Output pressure"))
        self.incognita.addItem(QtGui.QApplication.translate("pychemqt", "Flowrate"))
        self.incognita.currentIndexChanged.connect(partial(self.cambiar_data, "incognita"))
        layout.addWidget(self.incognita,2,2,1,1)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Diameter")),3,1,1,1)
        self.diametro=Entrada_con_unidades(float, spinbox=True, step=0.1, suffix='"')
        self.diametro.valueChanged.connect(partial(self.cambiar_data, "diametro"))
        layout.addWidget(self.diametro,3,2,1,1)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "RPM")),4,1,1,1)
        self.velocidad=Entrada_con_unidades(int, spinbox=True, step=1)
        self.velocidad.valueChanged.connect(partial(self.cambiar_data, "velocidad"))
        layout.addWidget(self.velocidad,4,2,1,1)

        self.groupBox_Resultados = QtGui.QGroupBox(QtGui.QApplication.translate("pychemqt", "Results"))
        gridLayout_3 = QtGui.QGridLayout(self.groupBox_Resultados)
        gridLayout_3.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Power")),0,0,1,1)
        self.power=Entrada_con_unidades(Power, retornar=False, readOnly=True)
        gridLayout_3.addWidget(self.power,0,1,1,1)        
        gridLayout_3.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Output Pressure")),0,4,1,1)
        self.PoutCalculada=Entrada_con_unidades(Pressure, retornar=False, readOnly=True)
        gridLayout_3.addWidget(self.PoutCalculada,0,5,1,1)
        gridLayout_3.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Flowrate")),1,0,1,1)
        self.volflow=Entrada_con_unidades(VolFlow, "QLiq", retornar=False, readOnly=True)
        gridLayout_3.addWidget(self.volflow,1,1,1,1)
        gridLayout_3.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Head")),1,4,1,1)
        self.headCalculada=Entrada_con_unidades(Length, retornar=False, readOnly=True)
        gridLayout_3.addWidget(self.headCalculada,1,5,1,1)
        gridLayout_3.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Efficiency")),2,0,1,1)
        self.rendimientoCalculado=Entrada_con_unidades(float, width=60, readOnly=True)
        gridLayout_3.addWidget(self.rendimientoCalculado,2,1,1,1)
        gridLayout_3.addItem(QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum),0,3,1,1)
        gridLayout_Calculo.addWidget(self.groupBox_Resultados,9,1,1,6)
        gridLayout_Calculo.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),10,1,1,6)


        #Pestaña diseño
        self.tabDiseno = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout(self.tabDiseno)
        self.gridLayout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Not implemented\n\nRef: Gülich - Centrifugal Pumps", None, QtGui.QApplication.UnicodeUTF8)),0,0,1,1)
        self.tabWidget.insertTab(2, self.tabDiseno,QtGui.QApplication.translate("pychemqt", "Design"))

        
        #Costos
        gridLayout_Costos = QtGui.QGridLayout(self.tabCostos)
        gridLayout_Costos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Pump type")),1,1,1,1)
        self.tipo_bomba = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_BOMBA:
            self.tipo_bomba.addItem(txt)
        self.tipo_bomba.currentIndexChanged.connect(self.bomba_currentIndexChanged)
        gridLayout_Costos.addWidget(self.tipo_bomba,1,2,1,1)
        gridLayout_Costos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Centrifuge type")),2,1,1,1)
        self.tipo_centrifuga = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_CENTRIFUGA:
            self.tipo_centrifuga.addItem(txt)
        self.tipo_centrifuga.currentIndexChanged.connect(partial(self.changeParamsCoste, "tipo_centrifuga"))
        gridLayout_Costos.addWidget(self.tipo_centrifuga,2,2,1,1)
        gridLayout_Costos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Material")),3,1,1,1)
        self.material = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MATERIAL:
            self.material.addItem(txt)
        self.material.currentIndexChanged.connect(partial(self.changeParamsCoste, "material"))
        gridLayout_Costos.addWidget(self.material,3,2,1,1)
        gridLayout_Costos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Motor type")),4,1,1,1)
        self.motor = QtGui.QComboBox()
        for txt in self.Equipment.TEXT_MOTOR:
            self.motor.addItem(txt)
        self.motor.currentIndexChanged.connect(partial(self.changeParamsCoste, "motor"))
        gridLayout_Costos.addWidget(self.motor,4,2,1,1)
        gridLayout_Costos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Motor RPM")),5,1,1,1)
        self.rpm = QtGui.QComboBox(self.tabCostos)
        for txt in self.Equipment.TEXT_RPM:
            self.rpm.addItem(txt)
        self.rpm.currentIndexChanged.connect(partial(self.changeParamsCoste, "rpm"))
        gridLayout_Costos.addWidget(self.rpm,5,2,1,1)
        
        self.Costos=CostData(self.Equipment)
        self.Costos.valueChanged.connect(self.changeParamsCoste)
        gridLayout_Costos.addWidget(self.Costos,6,1,2,4)

        gridLayout_Costos.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),7,1,1,4)
        self.groupBox_Costos = QtGui.QGroupBox(QtGui.QApplication.translate("pychemqt", "Stimated costs"))
        gridLayout_Costos.addWidget(self.groupBox_Costos,8,1,1,4)
        gridLayout_5 = QtGui.QGridLayout(self.groupBox_Costos)
        gridLayout_5.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Pump")),0,0,1,1)
        self.C_bomba=Entrada_con_unidades(Currency, retornar=False, readOnly=True)
        gridLayout_5.addWidget(self.C_bomba,0,1,1,1)
        gridLayout_5.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Motor")),1,0,1,1)
        self.C_motor=Entrada_con_unidades(Currency, retornar=False , readOnly=True)
        gridLayout_5.addWidget(self.C_motor,1,1,1,1)
        gridLayout_5.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Purchase cost")),0,4,1,1)
        self.C_adq=Entrada_con_unidades(Currency, retornar=False, readOnly=True)
        gridLayout_5.addWidget(self.C_adq,0,5,1,1)
        gridLayout_5.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Installed cost")),1,4,1,1)
        self.C_inst=Entrada_con_unidades(Currency, retornar=False, readOnly=True)
        gridLayout_5.addWidget(self.C_inst,1,5,1,1)
        gridLayout_Costos.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),9,1,1,4)
        
        if equipment:
            self.setEquipment(equipment)


    def cambiar_data(self, parametro, valor):
        if parametro=="Pout":
            self.Carga.clear()
            self.deltaP.clear()
        elif parametro=="deltaP":
            self.Pout.clear()
            self.Carga.clear()
        else:
            self.Pout.clear()
            self.deltaP.clear()
        self.changeParams(parametro, valor)
        
    def bomba_currentIndexChanged(self, int):
        self.tipo_centrifuga.setDisabled(int)
        self.changeParamsCoste("tipo_bomba", int)

    def usarCurvaToggled(self, int):
        self.groupBox_Curva.setEnabled(int)
        self.rendimiento.setReadOnly(int)
        self.changeParams("usarCurva", int)

    def bottonCurva_clicked(self):
        dialog = bombaCurva.Ui_bombaCurva(self.Equipment.kwargs["curvaCaracteristica"], self)
        if dialog.exec_():
            self.curva=dialog.curva
            self.diametro.setValue(dialog.curva[0])
            self.velocidad.setValue(dialog.curva[1])
            self.changeParams("curvaCaracteristica", dialog.curva)


if __name__ == "__main__":
    import sys        
    from lib.corriente import Corriente
    app = QtGui.QApplication(sys.argv)
    agua=Corriente(T=300, P=101325, caudalMasico=1, fraccionMolar=[1.])
    bomba=Pump(entrada=agua, rendimiento=0.75, deltaP=20*101325, tipo_bomba=1)
    dialogBomba = UI_equipment(equipment=bomba)
    dialogBomba.show()
    sys.exit(app.exec_())
