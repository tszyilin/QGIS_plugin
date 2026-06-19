import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon


class ProfileTool:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None

    def initGui(self):
        self.action = QAction('Profile Tool', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu('&Profile Tool', self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu('&Profile Tool', self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        from .profile_tool_dialog import ProfileToolDialog
        dialog = ProfileToolDialog(self.iface, self.iface.mainWindow())
        dialog.exec_()
