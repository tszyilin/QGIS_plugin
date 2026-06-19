import math

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QDoubleSpinBox, QDialogButtonBox, QMessageBox,
)
from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature,
    QgsGeometry, QgsPointXY, QgsField,
)


class ProfileToolDialog(QDialog):
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setWindowTitle('Create Profile Grid')
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.x_distance = QDoubleSpinBox()
        self.x_distance.setRange(1, 1_000_000)
        self.x_distance.setDecimals(1)
        self.x_distance.setValue(1400)
        self.x_distance.setSuffix(' m')

        self.x_segment = QDoubleSpinBox()
        self.x_segment.setRange(0.1, 100_000)
        self.x_segment.setDecimals(1)
        self.x_segment.setValue(100)
        self.x_segment.setSuffix(' m')

        self.y_min = QDoubleSpinBox()
        self.y_min.setRange(-10_000, 10_000)
        self.y_min.setDecimals(1)
        self.y_min.setValue(830)
        self.y_min.setSuffix(' m RL')

        self.y_max = QDoubleSpinBox()
        self.y_max.setRange(-10_000, 10_000)
        self.y_max.setDecimals(1)
        self.y_max.setValue(930)
        self.y_max.setSuffix(' m RL')

        self.y_interval = QDoubleSpinBox()
        self.y_interval.setRange(0.1, 10_000)
        self.y_interval.setDecimals(1)
        self.y_interval.setValue(2)
        self.y_interval.setSuffix(' m')

        form.addRow('X Distance:', self.x_distance)
        form.addRow('X Segment interval:', self.x_segment)
        form.addRow('Y Min (RL):', self.y_min)
        form.addRow('Y Max (RL):', self.y_max)
        form.addRow('Y Interval:', self.y_interval)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._generate_grid)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _generate_grid(self):
        x_dist = self.x_distance.value()
        x_seg = self.x_segment.value()
        y_min = self.y_min.value()
        y_max = self.y_max.value()
        y_int = self.y_interval.value()

        if y_min >= y_max:
            QMessageBox.warning(self, 'Invalid Input', 'Y Min must be less than Y Max.')
            return
        if x_seg <= 0 or y_int <= 0:
            QMessageBox.warning(self, 'Invalid Input', 'Segment and interval must be greater than zero.')
            return

        crs = QgsProject.instance().crs().authid()
        layer = QgsVectorLayer(f'LineString?crs={crs}', 'Profile Grid', 'memory')
        provider = layer.dataProvider()
        provider.addAttributes([QgsField('type', QVariant.String)])
        layer.updateFields()

        features = []

        # Outer border
        border = QgsFeature()
        border.setAttributes(['border'])
        border.setGeometry(QgsGeometry.fromPolylineXY([
            QgsPointXY(0, y_min),
            QgsPointXY(x_dist, y_min),
            QgsPointXY(x_dist, y_max),
            QgsPointXY(0, y_max),
            QgsPointXY(0, y_min),
        ]))
        features.append(border)

        # Vertical gridlines — use integer steps to avoid float drift
        n_x = int(math.floor(x_dist / x_seg))
        for i in range(1, n_x):
            x = i * x_seg
            f = QgsFeature()
            f.setAttributes(['grid_x'])
            f.setGeometry(QgsGeometry.fromPolylineXY([
                QgsPointXY(x, y_min),
                QgsPointXY(x, y_max),
            ]))
            features.append(f)

        # Horizontal gridlines
        n_y = int(math.floor((y_max - y_min) / y_int))
        for i in range(1, n_y):
            y = y_min + i * y_int
            f = QgsFeature()
            f.setAttributes(['grid_y'])
            f.setGeometry(QgsGeometry.fromPolylineXY([
                QgsPointXY(0, y),
                QgsPointXY(x_dist, y),
            ]))
            features.append(f)

        provider.addFeatures(features)
        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)
        self.iface.mapCanvas().setExtent(layer.extent())
        self.iface.mapCanvas().refresh()
        self.accept()
