import wx
import arcpy
import pythonaddins
import webbrowser

class PageOwner(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        staticTxtOwner = wx.StaticText(self, -1, "Owner Name")
        self.txtOwner = wx.TextCtrl(self, wx.ID_ANY, "")

        btnOK = wx.Button(self, 1, 'Search')
        btnOK.Bind(wx.EVT_BUTTON, self.OnOk, id=1)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.lc)
        self.lc.InsertColumn(0, 'Property ID')
        self.lc.InsertColumn( 1, 'Owner')
        self.lc.InsertColumn(2, 'Address')
        self.lc.InsertColumn(3, 'City')
        self.lc.InsertColumn(4, 'Land Value')
        self.lc.InsertColumn(5, 'Improvement Value')
        self.lc.InsertColumn(6, 'Total Value')

        sizer.AddSpacer(10) 
        sizer.Add(staticTxtOwner)
        sizer.Add(self.txtOwner)
        sizer.AddSpacer(10) 
        sizer.Add(btnOK)
        sizer.AddSpacer(25)
        sizer.Add(self.lc)
        
        self.SetSizer(sizer)
        
    def OnClick(self,event):
        prop_id = event.GetText()
        try:
            mxd = arcpy.mapping.MapDocument("CURRENT")
            
            arcpy.MakeFeatureLayer_management("Kendall_Parcels.shp","parcels_lyr")
            arcpy.SelectLayerByAttribute_management("parcels_lyr", "NEW_SELECTION", "PROP_ID = " + prop_id)
            result = arcpy.GetCount_management("parcels_lyr")
            count = int(result.getOutput(0))

            df = arcpy.mapping.ListDataFrames(mxd)[0]
            layer = arcpy.mapping.ListLayers(mxd, "parcels_lyr", df)[0]
            df.extent = layer.getSelectedExtent()

            webbrowser.open_new('http://esearch.kendallad.org/Property/View/' + prop_id)
            
        except Exception as e:
            print(e.message)
        
    def OnOk(self, event):
        if self.txtOwner.GetValue():
            owner = self.txtOwner.GetValue().upper()
            queryString =  "file_as_na LIKE \'%" + owner + "%\'"

            self.lc.DeleteAllItems()

            with arcpy.da.SearchCursor("Kendall_Parcels.shp", ("PROP_ID","file_as_na", "situs_num" , "situs_st_1", "situs_st_2", "situs_city", "land_val", "imprv_val", "market"), queryString) as cursor:
                flag = False
                for row in cursor:
                    flag = True
                    pos = self.lc.InsertStringItem(0, str(row[0]))
                    self.lc.SetStringItem(pos,1,row[1])
                    self.lc.SetStringItem(pos,2,row[2] + " " + row[3] + " " + row[4])
                    self.lc.SetStringItem(pos,3,row[5])
                    self.lc.SetStringItem(pos,4,str(row[6]))
                    self.lc.SetStringItem(pos,5,str(row[7]))
                    self.lc.SetStringItem(pos,6,str(row[8]))
        
                if not flag:
                    pythonaddins.MessageBox("No records found", "Query Error", 0)
        else:
            pythonaddins.MessageBox("Enter an owner name or portion of a name", "Query Error", 0)
                
class PageAddress(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)


        staticTxtStreetName = wx.StaticText(self, -1, "Street Name")
        self.txtStreetName = wx.TextCtrl(self, wx.ID_ANY, "")

        staticTxtSubdivision = wx.StaticText(self, -1, "Subdivision")
        subdivisions = ['Stone Creek Ranch', 'Cordillera', 'Waterstone', 'Coveney Ranch' ]
        self.comboBoxSub = wx.ComboBox(self, -1, size=(150, -1), choices=subdivisions, style=wx.CB_READONLY)

        btnOK = wx.Button(self, 1, 'Search')
        btnOK.Bind(wx.EVT_BUTTON, self.OnOk, id=1)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.lc)
        self.lc.InsertColumn(0, 'Property ID')
        self.lc.InsertColumn( 1, 'Owner')
        self.lc.InsertColumn(2, 'Address')
        self.lc.InsertColumn(3, 'City')
        self.lc.InsertColumn(4, 'Land Value')
        self.lc.InsertColumn(5, 'Improvement Value')
        self.lc.InsertColumn(6, 'Total Value')

        sizer.AddSpacer(10) 
        sizer.Add(staticTxtStreetName)
        sizer.Add(self.txtStreetName)
        sizer.AddSpacer(10) 
        sizer.Add(staticTxtSubdivision)
        sizer.Add(self.comboBoxSub)
        sizer.AddSpacer(10) 
        sizer.Add(btnOK)
        sizer.AddSpacer(25)
        sizer.Add(self.lc)
        self.SetSizer(sizer)
        
    def OnClick(self,event):
        prop_id = event.GetText()
        try:
            mxd = arcpy.mapping.MapDocument("CURRENT")
            
            arcpy.MakeFeatureLayer_management("Kendall_Parcels.shp","parcels_lyr")
            arcpy.SelectLayerByAttribute_management("parcels_lyr", "NEW_SELECTION", "PROP_ID = " + prop_id)
            result = arcpy.GetCount_management("parcels_lyr")
            count = int(result.getOutput(0))

            df = arcpy.mapping.ListDataFrames(mxd)[0]
            layer = arcpy.mapping.ListLayers(mxd, "parcels_lyr", df)[0]
            df.extent = layer.getSelectedExtent()

            webbrowser.open_new('http://esearch.kendallad.org/Property/View/' + prop_id)
            
        except Exception as e:
            print(e.message)
            
    def OnOk(self, event):
        strStreetName = self.txtStreetName.GetValue().upper()
        strSubdivision = self.comboBoxSub.GetValue().upper()

        if strStreetName or strSubdivision:
            if strStreetName and not strSubdivision:
                queryString =  "situs_st_1 LIKE \'%" + strStreetName + "%\'"
            elif strSubdivision and not strStreetName:
                queryString =  "DESC_ LIKE \'%" + strSubdivision + "%\'"
            elif strSubdivision and strStreetName:
                queryString =  "DESC_ LIKE \'%" + strSubdivision + "%\' and situs_st_1 LIKE \'%" + strStreetName + "%\'"
                

            self.lc.DeleteAllItems()

            with arcpy.da.SearchCursor("Kendall_Parcels.shp", ("PROP_ID","file_as_na", "situs_num" , "situs_st_1", "situs_st_2", "situs_city", "land_val", "imprv_val", "market"), queryString) as cursor:
                flag = False
                for row in cursor:
                    flag = True
                    pos = self.lc.InsertStringItem(0, str(row[0]))
                    self.lc.SetStringItem(pos,1,row[1])
                    self.lc.SetStringItem(pos,2,row[2] + " " + row[3] + " " + row[4])
                    self.lc.SetStringItem(pos,3,row[5])
                    self.lc.SetStringItem(pos,4,str(row[6]))
                    self.lc.SetStringItem(pos,5,str(row[7]))
                    self.lc.SetStringItem(pos,6,str(row[8]))
        
                if not flag:
                    pythonaddins.MessageBox("No records found", "Query Error", 0)
        else:
            pythonaddins.MessageBox("Enter a street name or subdivision", "Query Error", 0)

class PageID(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        staticTxtID = wx.StaticText(self, -1, "Unique Identifier")
        self.txtID = wx.TextCtrl(self, wx.ID_ANY, "")
        btnOK = wx.Button(self, 1, 'Search')

        btnOK.Bind(wx.EVT_BUTTON, self.OnOk, id=1)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.lc)
        self.lc.InsertColumn(0, 'Property ID')
        self.lc.InsertColumn(1, 'Owner')
        self.lc.InsertColumn(2, 'Address')
        self.lc.InsertColumn(3, 'City')
        self.lc.InsertColumn(4, 'Land Value')
        self.lc.InsertColumn(5, 'Improvement Value')
        self.lc.InsertColumn(6, 'Total Value')
      

        sizer.AddSpacer(10) 
        sizer.Add(staticTxtID)
        sizer.Add(self.txtID)
        sizer.AddSpacer(10) 
        sizer.Add(btnOK)
        sizer.AddSpacer(25)
        sizer.Add(self.lc)
        self.SetSizer(sizer)

    def OnClick(self,event):
        prop_id = event.GetText()
        try:
            mxd = arcpy.mapping.MapDocument("CURRENT")
            
            arcpy.MakeFeatureLayer_management("Kendall_Parcels.shp","parcels_lyr")
            arcpy.SelectLayerByAttribute_management("parcels_lyr", "NEW_SELECTION", "PROP_ID = " + prop_id)
            result = arcpy.GetCount_management("parcels_lyr")
            count = int(result.getOutput(0))

            df = arcpy.mapping.ListDataFrames(mxd)[0]
            layer = arcpy.mapping.ListLayers(mxd, "parcels_lyr", df)[0]
            df.extent = layer.getSelectedExtent()

            webbrowser.open_new('http://esearch.kendallad.org/Property/View/' + prop_id)
            
        except Exception as e:
            print(e.message)
        
    def OnOk(self, event):
        if self.txtID.GetValue():
            id = self.txtID.GetValue()
            queryString =  "PROP_ID = " + id

            self.lc.DeleteAllItems()

            with arcpy.da.SearchCursor("Kendall_Parcels.shp", ("PROP_ID","file_as_na", "situs_num" , "situs_st_1", "situs_st_2", "situs_city", "land_val", "imprv_val", "market"), queryString) as cursor:
                flag = False
                for row in cursor:
                    flag = True
                    pos = self.lc.InsertStringItem(0, str(row[0]))
                    self.lc.SetStringItem(pos,1,row[1])
                    self.lc.SetStringItem(pos,2,row[2] + " " + row[3] + " " + row[4])
                    self.lc.SetStringItem(pos,3,row[5])
                    self.lc.SetStringItem(pos,4,str(row[6]))
                    self.lc.SetStringItem(pos,5,str(row[7]))
                    self.lc.SetStringItem(pos,6,str(row[8]))

                if not flag:
                    pythonaddins.MessageBox("No records found", "Query Error", 0)
        else:
            pythonaddins.MessageBox("Enter an ID", "Query Error", 0)


class PageAdvanced(wx.Panel):
     def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(10) 

        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)

        staticTxtOwner = wx.StaticText(self, -1, "Owner Name")
        self.txtOwner = wx.TextCtrl(self, wx.ID_ANY, "")

        staticTxtStreetName = wx.StaticText(self, -1, "Street Name")
        self.txtStreetName = wx.TextCtrl(self, wx.ID_ANY, "")

        inputOneSizer.Add(staticTxtOwner)
        inputOneSizer.Add(self.txtOwner)
        inputOneSizer.AddSpacer(10) 
        inputOneSizer.Add(staticTxtStreetName)
        inputOneSizer.Add(self.txtStreetName)

        staticTxtSubdivision = wx.StaticText(self, -1, "Subdivision")
        subdivisions = ['Stone Creek Ranch', 'Cordillera', 'Waterstone', 'Coveney Ranch' ]
        self.comboBoxSub = wx.ComboBox(self, -1, size=(150, -1), choices=subdivisions, style=wx.CB_READONLY)

        inputTwoSizer.Add(staticTxtSubdivision)
        inputTwoSizer.Add(self.comboBoxSub)

        staticTxtMinVal = wx.StaticText(self, -1, "Minimum Value")
        self.txtMinVal = wx.TextCtrl(self, wx.ID_ANY, "")

        staticTxtMaxVal = wx.StaticText(self, -1, "Maximum Value")
        self.txtMaxVal = wx.TextCtrl(self, wx.ID_ANY, "")

        inputThreeSizer.Add(staticTxtMinVal)
        inputThreeSizer.Add(self.txtMinVal)
        inputThreeSizer.AddSpacer(10) 
        inputThreeSizer.Add(staticTxtMaxVal)
        inputThreeSizer.Add(self.txtMaxVal)

        btnOK = wx.Button(self, 1, 'Search')
        btnOK.Bind(wx.EVT_BUTTON, self.OnOk, id=1)
        btnSizer.Add(btnOK)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick, self.lc)
        self.lc.InsertColumn(0, 'Property ID')
        self.lc.InsertColumn(1, 'Owner')
        self.lc.InsertColumn(2, 'Address')
        self.lc.InsertColumn(3, 'City')
        self.lc.InsertColumn(4, 'Land Value')
        self.lc.InsertColumn(5, 'Improvement Value')
        self.lc.InsertColumn(6, 'Total Value')
        inputFourSizer.Add(self.lc)

        sizer.Add(inputOneSizer)
        sizer.AddSpacer(25)
        sizer.Add(inputTwoSizer)
        sizer.AddSpacer(25)
        sizer.Add(inputThreeSizer)
        sizer.AddSpacer(25)
        sizer.Add(btnSizer)
        sizer.AddSpacer(25)
        sizer.Add(inputFourSizer)

        self.SetSizer(sizer)

     def OnClick(self,event):
        prop_id = event.GetText()
        try:
            mxd = arcpy.mapping.MapDocument("CURRENT")
            
            arcpy.MakeFeatureLayer_management("Kendall_Parcels.shp","parcels_lyr")
            arcpy.SelectLayerByAttribute_management("parcels_lyr", "NEW_SELECTION", "PROP_ID = " + prop_id)
            result = arcpy.GetCount_management("parcels_lyr")
            count = int(result.getOutput(0))

            df = arcpy.mapping.ListDataFrames(mxd)[0]
            layer = arcpy.mapping.ListLayers(mxd, "parcels_lyr", df)[0]
            df.extent = layer.getSelectedExtent()

            webbrowser.open_new('http://esearch.kendallad.org/Property/View/' + prop_id)
            
        except Exception as e:
            print(e.message)
     def OnOk(self, event):

        queryString = ""
        flagOwner = False
        if self.txtOwner.GetValue():
            flagOwner = True
            owner = self.txtOwner.GetValue().upper()
            queryString =  "file_as_na LIKE \'%" + owner + "%\'"

        flagStreet = False
        if self.txtStreetName.GetValue():
            flagStreet = True
            strStreetName = self.txtStreetName.GetValue().upper()
            if flagOwner:
                queryString = queryString + " AND " + "situs_st_1 LIKE \'%" + strStreetName + "%\'"
            else:
                queryString = "situs_st_1 LIKE \'%" + strStreetName + "%\'"

        if self.comboBoxSub.GetValue():
            strSubdivision = self.comboBoxSub.GetValue().upper()
            if flagOwner or flagStreet:
                queryString = queryString + " AND " + "DESC_ LIKE \'%" + strSubdivision + "%\'"
            else:
                queryString = "DESC_ LIKE \'%" + strSubdivision + "%\'"

        if self.txtMinVal.GetValue():
            numMinVal = long(self.txtMinVal.GetValue())
            queryString = queryString + " AND market > " + str(numMinVal)

        if self.txtMaxVal.GetValue():
            numMaxVal = long(self.txtMaxVal.GetValue())
            queryString = queryString + " AND market < " + str(numMaxVal)

        if not queryString:
            pythonaddins.MessageBox("Enter one or more search parameters", "Query Error", 0)
        else:
            self.lc.DeleteAllItems()
        
            with arcpy.da.SearchCursor("Kendall_Parcels.shp", ("PROP_ID","file_as_na", "situs_num" , "situs_st_1", "situs_st_2", "situs_city", "land_val", "imprv_val", "market"), queryString) as cursor:
                flag = False
                for row in cursor:
                    flag = True
                    pos = self.lc.InsertStringItem(0, str(row[0]))
                    self.lc.SetStringItem(pos,1,row[1])
                    self.lc.SetStringItem(pos,2,row[2] + " " + row[3] + " " + row[4])
                    self.lc.SetStringItem(pos,3,row[5])
                    self.lc.SetStringItem(pos,4,str(row[6]))
                    self.lc.SetStringItem(pos,5,str(row[7]))
                    self.lc.SetStringItem(pos,6,str(row[8]))

                if not flag:
                    pythonaddins.MessageBox("No records found", "Query Error", 0)
    

class NotebookParcel(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
    
        tabOwner = PageOwner(self)
        self.AddPage(tabOwner, "Search By Owner")

        tabAddress = PageAddress(self)
        self.AddPage(tabAddress, "Search by Address")

        tabID = PageID(self)
        self.AddPage(tabID, "Search by ID")

        tabAdvanced = PageAdvanced(self)
        self.AddPage(tabAdvanced, "Advanced Search")

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Search Parcels",size=(600,400),style=wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
              
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # Here we create a panel and a notebook on the panel
        panel = wx.Panel(self)

        arcpy.env.workspace = r"C:\ArcGIS_Blueprint_Python\data\Kendall"
 
        notebook = NotebookParcel(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
    
        panel.SetSizer(sizer)
        self.Layout()
    def OnClose(self, event):
        """Close the frame. Do not use destroy."""
        self.Show(False)
        # End OnClose event method
   #----------------------------------------------------------------------
#if __name__ == "__main__":
#    app = wx.App()
#    MainFrame().Show()
#    app.MainLoop()
