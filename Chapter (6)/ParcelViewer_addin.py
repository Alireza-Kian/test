import os
import sys
sys.path.append(os.path.dirname(__file__))
import arcpy
import pythonaddins

class ParcelViewer(object):
    """Implementation for ParcelViewer_addin.extension (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self._wxApp = None
        self._enabled = None
    def startup(self):
        try:
            from wx import PySimpleApp
            self._wxApp = PySimpleApp()
            self._wxApp.MainLoop()
        except:
            pythonaddins.MessageBox("Error starting Parcel Viewer extension.", "Extension Error", 0)

    @property
    def enabled(self):
        """Enable or disable the  button when the extension is turned on or off."""
        if self._enabled == False:
            wxpybutton.enabled = False
        else:
            wxpybutton.enabled = True
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """Set the enabled property of this extension when the extension is turned on or off in the Extension Dlalog of ArcMap."""
        self._enabled = value
        
class ParcelViewerButton(object):
    """Implementation for ParcelViewer_addin.button (Button)"""
    _dlg = None

    @property
    def dlg(self):
        """Return the MainFrame dialog."""
        if self._dlg is None:
            from Interface import MainFrame
            self._dlg = MainFrame()
        return self._dlg
    
    def __init__(self):
        self.enabled = True
        self.checked = False
        
    def onClick(self):
        try:
            self.dlg.Show(True)
        except Exception as e:
            pythonaddins.MessageBox(e.message, "Error", 0)
