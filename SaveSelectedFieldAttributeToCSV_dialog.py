import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.core import QgsProject
from . import SaveSelectedFieldAttributeToCSV

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'SaveSelectedFieldAttributeToCSV_dialog_base.ui'))

class SaveSelectedFieldAttributeToCSVDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SaveSelectedFieldAttributeToCSVDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = parent

        self.btnSelectFields.clicked.connect(self.selectFields)
        self.btnRemoveFields.clicked.connect(self.removeFields)
        self.btnBrowseOutput.clicked.connect(self.browseOutputFile)

    def setLayers(self, layers):
        self.cmbLayers.clear()
        for layer in layers:
            self.cmbLayers.addItem(layer.name(), layer.id())

    def getSelectedLayer(self):
        layer_index = self.cmbLayers.currentIndex()
        if layer_index >= 0:
            layer_id = self.cmbLayers.itemData(layer_index)
            return QgsProject.instance().mapLayer(layer_id)
        else:
            return None

    def getSelectedFields(self):
        selected_fields = []
        for i in range(self.lstFields.count()):
            selected_fields.append(self.lstFields.item(i).text())
        return selected_fields

    def getOutputFile(self):
        return self.txtOutputFile.text()

    def selectFields(self):
        layer = self.getSelectedLayer()
        if layer:
            fields = layer.fields()
            for field in fields:
                field_name = field.name()
                if field_name not in [self.lstFields.item(i).text() for i in range(self.lstFields.count())]:
                    self.lstFields.addItem(field_name)

    def removeFields(self):
        for item in self.lstFields.selectedItems():
            self.lstFields.takeItem(self.lstFields.row(item))

    def browseOutputFile(self):
        output_file, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        self.txtOutputFile.setText(output_file)
