#from http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/
########-------------Load rasters in ArcGIS 10.1---------------
########  Information taken from various quality internet sources
#####     Copyright GPL 2013, as applicable, freely distributable.
#####     Wes Byne, wbyne@augustaga.gov
#####
#####   Please be sure that the project and data frame have a coordinate system defined, otherwise
#####   the selection of boundaries results in an uncertain output.
#####   Also, the curselection method on a ListBox still returns a list of strings, contrary
#####   to whatever the internet calls a bug or an intended feature.
#####   Happy GISing.

#import Tkinter as Tk
from Tkinter import *
from ttk import *
import arcpy
#import pythonaddins

########################################################################
class FindAsBuilts(object):
#class ToolClass10(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.config(width=750)
        self.root.title("Find As Builts or Aerials - BETA BUILD 5 June 2013")
        self.frameFind = Frame(parent)
        self.frameResults = Frame(parent,width=150)
        self.frameDetails = Frame(parent,width=150)
        self.frameLoad = Frame(parent)
        self.frameSave = Frame(parent)
        #self.grab_set()

#never did like the packer, always seemed too arbitrary....                
#        self.frameFind.pack()
#        self.frameResults.pack()
#        self.frameDetails.pack()
#        self.frameLoad.pack()
#        self.frameSave.pack()

        self.frameFind.grid(row=0, column=0,padx=3,pady=3)
        self.frameResults.grid(row = 0, column = 1,padx=3,pady=3)
        self.frameDetails.grid(row = 0, column = 2,padx=3,pady=3)
        self.frameLoad.grid(row = 1, column = 2,padx=3,pady=3)
        self.frameSave.grid(row = 2, column = 2,padx=3,pady=3)

        lblFind = Label(self.frameFind, text="Search by:")
        self.BtnFindPnt = Button(self.frameFind, text="Point",command=self.selectMidPoint)
        self.BtnFindPoly = Button(self.frameFind, text="Poly", command=self.selectRectangle)
        self.BtnReset = Button(self.frameFind, text="Reset", command=self.search_reset)
        lblFind.grid(row=0,column=0,sticky=W)
        self.BtnFindPnt.grid(row=2,column=0)
        self.BtnFindPoly.grid(row=3,column=0)
        self.BtnReset.grid(row=4,column=0)

        self.ListRes = []
        lblResults = Label(self.frameResults, text="Results:")
#        btn2 = Button(self.frameResults, text="Open Frame", command=self.openFrame)
        scrollResults = Scrollbar(self.frameResults)
        self.listBoxResults = Listbox(self.frameResults, yscrollcommand=scrollResults.set, width=60)
        self.listBoxResults.bind('<<ListboxSelect>>', self.parseListResults)
        scrollResults.config(command=self.listBoxResults.yview)
#        scrollResults.pack(side=right,fill=Y)
        lblResults.grid(row=0,column=0,sticky=W)
        scrollResults.grid(row=1,column=1,sticky=NS)
        self.listBoxResults.grid(row=1,column=0)
        #self.listBoxResults.insert(END, "my big fat list entry 1")
        #self.listBoxResults.insert(0, "my big fat list entry 2")
        #self.listBoxResults.insert(0, "my big fat list entry 3")

        lblDetails = Label(self.frameDetails, text="Details:")
        scrollDetails = Scrollbar(self.frameDetails)
        self.listBoxDetails = Listbox(self.frameDetails, yscrollcommand=scrollDetails.set,width=60)
        #accidentally set yscrollcommand to scrollResults.set and it activated the scrollbar,
        #but of course there was no data in it.
        scrollDetails.config(command=self.listBoxDetails.yview)
#        scrollResults.pack(side=right,fill=Y)
        lblDetails.grid(row=0,column=0,sticky=W)
        scrollDetails.grid(row=1,column=1,sticky=NS)
        self.listBoxDetails.grid(row=1,column=0)


        lblLoad1 = Label(self.frameLoad, text="Load:")
        lblLoad2 = Label(self.frameLoad, text="Map: ")
        lblLoad3 = Label(self.frameLoad, text="Support Docs:")
        btnMap = Button(self.frameLoad, text="Map", command=self.loadInMap)
        btnPdf = Button(self.frameLoad, text="Paper", command=self.loadInPaper)
        btnDocs = Button(self.frameLoad, text="PDF", command=self.openFrame)
        lblLoad1.grid(row=0,column=0,sticky=W)
        lblLoad2.grid(row=1,column=0,sticky=W)
        lblLoad3.grid(row=1,column=2,sticky=E)
        btnMap.grid(row=2,column=0,sticky=W)
        btnPdf.grid(row=2,column=1,sticky=W)
        btnDocs.grid(row=2,column=2,sticky=E)

        self.aer_96_path="C:\\mnt\\gis\\raster\\aerials\\"
#        self.aer_96_path="\\\\augnas005\\ortho\\BlackWhite1997Orthos\\"
        self.aer_02_path="C:\\mnt\\gis\\raster\\aerials\\"
        self.aer_07_path="\\\\augnas005\\ortho\\GARICH10-GeoTIFFs\\"
        self.rec_aud_path_map="C:\\mnt\project_archives\\rectified\\aud\\"
        self.rec_aed_path_map="C:\\mnt\project_archives\\rectified\\aed\\"            
        self.rec_aud_path_paper="C:\\mnt\project_archives\\printable\\aud\\"
        self.rec_aed_path_paper="C:\\mnt\project_archives\\printable\\aed\\"            
        
        
        btnSettings = Button(self.frameSave, text="Settings", command=self.setSettings)
        btnSettings.grid(row=0,column=0)

#----------------------------------------------------------------------
    def setSettings(self):
        """"""
        import os.path
        import tkMessageBox
        self.hide()
        otherFrame = Toplevel()
        otherFrame.geometry("600x250")
        otherFrame.title("SettingsFrame")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Button(otherFrame, text="Close", command=handler)
#        btn.pack()
        lblSet0 = Label(otherFrame, text="c:\\workspace\\load_rasters\\src\\load_raster.cfg")
        lblSet1 = Label(otherFrame, text="Aerials 96:")
        lblSet2 = Label(otherFrame, text="Aerials 02:")
        lblSet3 = Label(otherFrame, text="Aerials 07:")
        lblSet4 = Label(otherFrame, text="Rectifed aud:")
        lblSet5 = Label(otherFrame, text="Rectified aed:")
        lblSet6 = Label(otherFrame, text="Printable aud:")
        lblSet7 = Label(otherFrame, text="Printable aed:")

        lblSet0.grid(row=0, column=0)
        lblSet1.grid(row=1, column=0)
        lblSet2.grid(row=2, column=0)
        lblSet3.grid(row=3, column=0)
        lblSet4.grid(row=4, column=0)
        lblSet5.grid(row=5, column=0)
        lblSet6.grid(row=6, column=0)
        lblSet7.grid(row=7, column=0)
        
        btn.grid(row=10, column=4)
#        lblSet1.pack()
#        lblLoad9.grid(row=0,column=0,sticky=W)
        entrywidth=55
        Entry1 = Entry(otherFrame,width=entrywidth)
        Entry2 = Entry(otherFrame)
        Entry3 = Entry(otherFrame)
        Entry4 = Entry(otherFrame)
        Entry5 = Entry(otherFrame)
        Entry6 = Entry(otherFrame)
        Entry7 = Entry(otherFrame)
        Entry1.grid(row=1, column=1,columnspan=4,sticky=W+E)
        Entry2.grid(row=2, column=1,columnspan=4,sticky=W+E)
        Entry3.grid(row=3, column=1,columnspan=4,sticky=W+E)
        Entry4.grid(row=4, column=1,columnspan=4,sticky=W+E)
        Entry5.grid(row=5, column=1,columnspan=4,sticky=W+E)
        Entry6.grid(row=6, column=1,columnspan=4,sticky=W+E)
        Entry7.grid(row=7, column=1,columnspan=4,sticky=W+E)
# initialize Entry widgets
 
        path = "c:\\workspace\\load_rasters\\src\\load_raster.cfg"
        if os.path.isfile(path):
                path = path + ".sid"  # need to check for img and jp2 formats....
                print path + "oh sid"
        else:
            tkMessageBox.showinfo("Gratuitous Information Box:", "Config file not found, using defaults.")
            print "Using defaults for paths."
            self.aer_96_path = "\\\\augnas005\\ortho\\BlackWhite1997Orthos\\"
            self.aer_02_path = "C:\\mnt\\gis\\raster\\aerials\\"
            self.aer_07_path = "\\\\augnas005\\ortho\\GARICH10-GeoTIFFs\\"
            self.rec_aud_path_map = "C:\\mnt\project_archives\\rectified\\aud\\"
            self.rec_aed_path_map = "C:\\mnt\project_archives\\rectified\\aed\\"            
            self.rec_aud_path_paper = "C:\\mnt\project_archives\\printable\\aud\\"
            self.rec_aed_path_paper = "C:\\mnt\project_archives\\printable\\aed\\"            
            Entry1.insert(0, self.aer_96_path)
            Entry2.insert(0, self.aer_02_path)
            Entry3.insert(0, self.aer_07_path)
            Entry4.insert(0, self.rec_aud_path_map)
            Entry5.insert(0, self.rec_aed_path_map)
            Entry6.insert(0, self.rec_aud_path_paper)
            Entry7.insert(0, self.rec_aed_path_paper) 






    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()

    #---------------------
    def populate_found(self):
        """"""
#arcpy.RefreshActiveView()
#        print xmid,ymid
#        self.listBoxDetails.insert(END, xmid)
#        self.listBoxDetails.insert(END, ymid)
        if arcpy.Exists("c:/temp/resultsview1"):
            arcpy.Delete_management("c:/temp/resultsview1")
        if arcpy.Exists("c:/temp/resultsview2"):
            arcpy.Delete_management("c:/temp/resultsview2")

        mytable1 = "c:/temp/resultsview1"
        arcpy.MakeTableView_management("aerial_tile",mytable1)
        myfields1=arcpy.ListFields(mytable1)
        mytable2 = "c:/temp/resultsview2"
        arcpy.MakeTableView_management("ibounds",mytable2)
        myfields2=arcpy.ListFields(mytable2)
        
        self.ListRes=[]
        self.listBoxResults.insert(END, "----------AERIALS-----------")
        self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Title Here","Year Here","Null","Null",0,0))
        
        myfields1 = ["TILENUM"]
        with arcpy.da.SearchCursor(mytable1,myfields1) as cursor:
                 for row in cursor:
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Flyover","Year Here","Null",row[0],0,0))
                     self.listBoxDetails.insert(END, row[0])
                     self.listBoxResults.insert(END, row[0])
        self.listBoxResults.insert(END, "----------SCANS-----------")
        self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Scans","Title Here","Year Here","Null","Null",0,0))

        myfields2 = ["CONTRACTOR","SETTITLE","DRAWING_DA","ENGINEEERI","FILENAME","CD","GEO_CD"]
        with arcpy.da.SearchCursor(mytable2,myfields2) as cursor:
                 for row in cursor:
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                     self.listBoxDetails.insert(END, row[1])
                     self.listBoxResults.insert(END, row[1])
                     
#        mylist = ["1","2","3","4"]
#        for row in mylist: #ListRes: #python book p 154 @ top, list iteration
#             self.listBoxResults.insert(END, mylist[row])

        self.BtnFindPnt.config(state=DISABLED)
        self.BtnFindPoly.config(state=DISABLED)
        
        #clean up the table view, apparently it is case sensitive
        arcpy.Delete_management("c:/temp/resultsview1")
        arcpy.Delete_management("c:/temp/resultsview2")
        return self.ListRes

    #----------------------------------------------------------------------
    def search_reset(self):
        """"""
        self.listBoxResults.delete(0,END)
        self.BtnFindPnt.config(state=NORMAL)
        self.listBoxDetails.delete(0,END)
        self.BtnFindPoly.config(state=NORMAL)
        self.ListRes=[]
        
    #----------------------------------------------------------------------
#http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def parseListResults(self,evt):
        """"""
        self.listBoxDetails.delete(0,END)
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)
        localResult = self.ListRes[index]
        print localResult
        mysplit=[]
        mysplit = localResult.split('|')
#        mysplit= [localResult.split('|')[0] for i in localResult]
        self.listBoxDetails.insert(END, "CONTRACTOR: " + mysplit[0])
        self.listBoxDetails.insert(END, "SET_TITLE: " + mysplit[1])
        self.listBoxDetails.insert(END, "DRAWING_DATE: " + mysplit[2])
        self.listBoxDetails.insert(END, "ENGINEER: " + mysplit[3])
        self.listBoxDetails.insert(END, "FILENAME: " + mysplit[4])
        self.listBoxDetails.insert(END, "CD: " + mysplit[5])
        self.listBoxDetails.insert(END, "GEO_CD: " + mysplit[6])
#"CONTRACTOR","SETTITLE","DRAWING_DA","ENGINEEERI","FILENAME","GEO_CD"            
        
    #----------------------------------------------------------------------
    def loadInMap(self):
        """"""
#        arcpy.MakeRasterLayer_management("c:/workspace/image.tif", "rdlayer", "#", "feature.shp", "1")                
        #arcpy.MakeRasterLayer_management("//augnas005/ortho/GARICH10-GeoTIFFs/003-4.tif","weslry")
#through trial and error, old school forward slashing..... me gusta
        import tkMessageBox
        import os.path #for checking for sid/img/jp2 format below
        print "spam"
        #tkMessageBox.showinfo("Got Here","Spamalot")
        print "spam, spam"
        
        myresult = self.listBoxResults.curselection()
        if not myresult: #an empty data structure is false in python
            tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
            return 0
        myresult = map(int, myresult)
#        localResult = self.ListRes[index]
        print myresult
        print myresult[0] 
        print "spam, spam, spam, " 
        print "spam, spam, spam, spam"
        mysplit=[]
        print self.ListRes[myresult[0]]
        mysplit = self.ListRes[myresult[0]].split('|')
        #look for someone who selects in the Details and then hits load
        if mysplit[0]=="Aerials" or mysplit[0] == "Scans":
            if mysplit[1] == "Title Here":
                tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
                return 0
        if mysplit[0]==None:
            tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
            return 0
        
        if mysplit[0] == "Aerials":
            if mysplit[2] == "1996" :
#                path="//augnas005/ortho/BlackWhite1997Orthos/"
#                path="E:/mnt/raid/data/maps/Augusta/raster/aerials/"
                path=self.aer_96_path
                tsplit = mysplit[4]
                #tsplit[-4:] #remove the file extension
                print int(tsplit[:-2])
                if int(tsplit[:-2]) >= 300:
                    if os.path.isfile(path+"do300-377\\"+tsplit+".sid"):
                        path=path+"do300-377\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do300-377\\"+tsplit[:-2]+".sid"):
                        path=path+"do300-377\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) >= 200:
                    if os.path.isfile(path+"do200-299\\"+tsplit+".sid"):
                        path=path+"do200-299\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do200-299\\"+tsplit[:-2]+".sid"):
                        path=path+"do200-299\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) >= 150:
                    if os.path.isfile(path+"do150-199\\"+tsplit+".sid"):
                        path=path+"do150-199\\"+tsplit+".sid"
                    elif os.path.isfile(path+"do150-199\\"+tsplit[:-2]+".sid"):
                        path=path+"do150-199\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 100:
                    if os.path.isfile(path+"do100-149\\"+tsplit+".sid"):
                        path=path+"do100-149\\"+tsplit+".sid"
                    if os.path.isfile(path+"do100-149\\"+tsplit[:-2]+".sid"):
                        path=path+"do100-149\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 50:
                    if os.path.isfile(path+"do050-099\\"+tsplit+".sid"):
                        path=path+"do050-099\\"+tsplit+".sid"
                    if os.path.isfile(path+"do050-099\\"+tsplit[:-2]+".sid"):
                        path=path+"do050-099\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 00:
                    if os.path.isfile(path+"do001-049\\"+tsplit+".sid"):
                        path=path+"do001-049\\"+tsplit+".sid"
                    if os.path.isfile(path+"do001-049\\"+tsplit[:-2]+".sid"):
                        path=path+"do001-049\\"+tsplit[:-2]+".sid"
                else:
                    print "error with path:" + path
                print path + " (1996)"
            elif mysplit[2] == "2002":
                path=self.aer_02_path
                tsplit = mysplit[4]
                #tsplit[-4:] #remove the file extension
                print int(tsplit[:-2])
                if int(tsplit[:-2]) > 300:
                    if os.path.isfile(path+"do300-377\\"+tsplit+".sid"):
                        path=path+"do300-377\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do300-377\\"+tsplit[:-2]+".sid"):
                        path=path+"do300-377\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) > 200:
                    if os.path.isfile(path+"do200-299\\"+tsplit+".sid"):
                        path=path+"do200-299\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do200-299\\"+tsplit[:-2]+".sid"):
                        path=path+"do200-299\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) > 150:
                    if os.path.isfile(path+"do150-199\\"+tsplit+".sid"):
                        path=path+"do150-199\\"+tsplit+".sid"
                    elif os.path.isfile(path+"do150-199\\"+tsplit[:-2]+".sid"):
                        path=path+"do150-199\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 100:
                    if os.path.isfile(path+"do100-149\\"+tsplit+".sid"):
                        path=path+"do100-149\\"+tsplit+".sid"
                    if os.path.isfile(path+"do100-149\\"+tsplit[:-2]+".sid"):
                        path=path+"do100-149\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 50:
                    if os.path.isfile(path+"do050-099\\"+tsplit+".sid"):
                        path=path+"do050-099\\"+tsplit+".sid"
                    if os.path.isfile(path+"do050-099\\"+tsplit[:-2]+".sid"):
                        path=path+"do050-099\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 00:
                    if os.path.isfile(path+"do001-049\\"+tsplit+".sid"):
                        path=path+"do001-049\\"+tsplit+".sid"
                    if os.path.isfile(path+"do001-049\\"+tsplit[:-2]+".sid"):
                        path=path+"do001-049\\"+tsplit[:-2]+".sid"
                else:
                    print "error with path:" + path
                print path + " (2002)"
            elif mysplit[2] == "2007":
                #don't know if this is right or not, but for now it's A-Okay.
                tsplit = mysplit[4]
                #not on aerials....tsplit[-4:] #remove the file extension
#                path="//augnas005/ortho/GARICH10-GeoTIFFs/"+tsplit+".tif"
                path=self.aer_07_path
                if os.path.isfile(path+tsplit+".tif"):
                    path=path+tsplit+".tif"
                elif os.path.isfile(path+tsplit[:-2]+".tif"):
                    path=path+tsplit[:-2]+".tif"
                else:
                    print "error with path: " +path    
                print path + " (2007)"
        else: #Record Drawings
            tsplit = mysplit[4]
            ttsplit = tsplit[:-4] #remove the file extension
            print "here" + ttsplit
            path=self.rec_aud_path_map
            path=path+mysplit[6]+"\\"+tsplit[:-4]
            pathaed=self.rec_aed_path_map
            pathaed=pathaed+mysplit[6]+"\\"+tsplit[:-4]
            if os.path.isfile(path+".sid"):
                path=path+".sid" #need to check for img and jp2 formats....
                print path + "oh sid"
            elif os.path.isfile(pathaed+".sid"):
                path=pathaed+".sid" #need to check for img and jp2 formats....
                print path + "oh sid"
            elif os.path.isfile(path+".img"):
                path=path+".img" #need to check for img and jp2 formats....
                print path + "oh img"
            elif os.path.isfile(pathaed+".img"):
                path=pathaed+".img" #need to check for img and jp2 formats....
                print path + "oh img"
            elif os.path.isfile(path+".jp2"):
                path=path+".jp2" #need to check for img and jp2 formats....
                print path + "oh jp2"
            elif os.path.isfile(pathaed+".jp2"):
                path=pathaed+".jp2" #need to check for img and jp2 formats....
                print path + "oh jp2"
            elif os.path.isfile(path+".jpeg"):
                path=path+".jpeg" #need to check for img and jp2 formats....
                print path + "oh jpeg"
            elif os.path.isfile(pathaed+".jpeg"):
                path=pathaed+".jpeg" #need to check for img and jp2 formats....
                print path + "oh jpeg"
            elif os.path.isfile(path+".jpg"):
                path=path+".jpg" #need to check for img and jp2 formats....
                print path + "oh jpg"
            elif os.path.isfile(pathaed+".jpg"):
                path=pathaed+".jpg" #need to check for img and jp2 formats....
                print path + "oh jpg"

            else:
                tkMessageBox.showinfo("Well that seems to be it","That file doesn't exist")
                
            print path
            
        if mysplit[0] == "Aerials":
            weslyr=str(tsplit) +":"+ str(mysplit[2]) #tsplit[:-2]
        else:
            weslyr=tsplit[:-4]
            
        arcpy.MakeRasterLayer_management(path,weslyr)
            
                
                
  #----------------------------------------------------------------------
    def loadInPaper(self):
        """"""
#        arcpy.MakeRasterLayer_management("c:/workspace/image.tif", "rdlayer", "#", "feature.shp", "1")                
        #arcpy.MakeRasterLayer_management("//augnas005/ortho/GARICH10-GeoTIFFs/003-4.tif","weslry")
#through trial and error, old school forward slashing..... me gusta
        import tkMessageBox
        from subprocess import Popen
        import os 
        myresult = self.listBoxResults.curselection()
        if not myresult: #an empty data structure is false in python
            tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
            return 0
        myresult2 = map(int, myresult)
#        localResult = self.ListRes[index]
        mysplit=[]
        mysplit = self.ListRes[myresult2[0]].split('|')
        #look for someone who selects in the Details and then hits load
        if mysplit[0]=="Aerials" or mysplit[0] == "Scans":
            if mysplit[1] == "Title Here":
                tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
                return 0
        if mysplit[0]==None:
            tkMessageBox.showinfo("Error", "Please select a Aerial or Drawing to Load")
            return 0
        
        if mysplit[0] == "Aerials":
            if mysplit[2] == "1996" :
#                path="//augnas005/ortho/BlackWhite1997Orthos/"
#                path="E:/mnt/raid/data/maps/Augusta/raster/aerials/"
                path=self.aer_96_path
                tsplit = mysplit[4]
                #tsplit[-4:] #remove the file extension
                print int(tsplit[:-2])
                if int(tsplit[:-2]) >= 300:
                    if os.path.isfile(path+"do300-377\\"+tsplit+".sid"):
                        path=path+"do300-377\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do300-377\\"+tsplit[:-2]+".sid"):
                        path=path+"do300-377\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) >= 200:
                    if os.path.isfile(path+"do200-299\\"+tsplit+".sid"):
                        path=path+"do200-299\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do200-299\\"+tsplit[:-2]+".sid"):
                        path=path+"do200-299\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) >= 150:
                    if os.path.isfile(path+"do150-199\\"+tsplit+".sid"):
                        path=path+"do150-199\\"+tsplit+".sid"
                    elif os.path.isfile(path+"do150-199\\"+tsplit[:-2]+".sid"):
                        path=path+"do150-199\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 100:
                    if os.path.isfile(path+"do100-149\\"+tsplit+".sid"):
                        path=path+"do100-149\\"+tsplit+".sid"
                    if os.path.isfile(path+"do100-149\\"+tsplit[:-2]+".sid"):
                        path=path+"do100-149\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 50:
                    if os.path.isfile(path+"do050-099\\"+tsplit+".sid"):
                        path=path+"do050-099\\"+tsplit+".sid"
                    if os.path.isfile(path+"do050-099\\"+tsplit[:-2]+".sid"):
                        path=path+"do050-099\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) >= 00:
                    if os.path.isfile(path+"do001-049\\"+tsplit+".sid"):
                        path=path+"do001-049\\"+tsplit+".sid"
                    if os.path.isfile(path+"do001-049\\"+tsplit[:-2]+".sid"):
                        path=path+"do001-049\\"+tsplit[:-2]+".sid"
                else:
                    print "error with path:" + path
                print path + " (1996)"
            elif mysplit[2] == "2002":
                path=self.aer_02_path
                tsplit = mysplit[4]
                #tsplit[-4:] #remove the file extension
                print int(tsplit[:-2])
                if int(tsplit[:-2]) > 300:
                    if os.path.isfile(path+"do300-377\\"+tsplit+".sid"):
                        path=path+"do300-377\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do300-377\\"+tsplit[:-2]+".sid"):
                        path=path+"do300-377\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) > 200:
                    if os.path.isfile(path+"do200-299\\"+tsplit+".sid"):
                        path=path+"do200-299\\"+tsplit +".sid"
                    elif os.path.isfile(path+"do200-299\\"+tsplit[:-2]+".sid"):
                        path=path+"do200-299\\"+tsplit[:-2] +".sid"
                elif int(tsplit[:-2]) > 150:
                    if os.path.isfile(path+"do150-199\\"+tsplit+".sid"):
                        path=path+"do150-199\\"+tsplit+".sid"
                    elif os.path.isfile(path+"do150-199\\"+tsplit[:-2]+".sid"):
                        path=path+"do150-199\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 100:
                    if os.path.isfile(path+"do100-149\\"+tsplit+".sid"):
                        path=path+"do100-149\\"+tsplit+".sid"
                    if os.path.isfile(path+"do100-149\\"+tsplit[:-2]+".sid"):
                        path=path+"do100-149\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 50:
                    if os.path.isfile(path+"do050-099\\"+tsplit+".sid"):
                        path=path+"do050-099\\"+tsplit+".sid"
                    if os.path.isfile(path+"do050-099\\"+tsplit[:-2]+".sid"):
                        path=path+"do050-099\\"+tsplit[:-2]+".sid"
                elif int(tsplit[:-2]) > 00:
                    if os.path.isfile(path+"do001-049\\"+tsplit+".sid"):
                        path=path+"do001-049\\"+tsplit+".sid"
                    if os.path.isfile(path+"do001-049\\"+tsplit[:-2]+".sid"):
                        path=path+"do001-049\\"+tsplit[:-2]+".sid"
                else:
                    print "error with path:" + path
                print path + " (2002)"
            elif mysplit[2] == "2007":
                #don't know if this is right or not, but for now it's A-Okay.
                tsplit = mysplit[4]
                #not on aerials....tsplit[-4:] #remove the file extension
#                path="//augnas005/ortho/GARICH10-GeoTIFFs/"+tsplit+".tif"
                path=self.aer_07_path
                if os.path.isfile(path+tsplit+".tif"):
                    path=path+tsplit+".tif"
                elif os.path.isfile(path+tsplit[:-2]+".tif"):
                    path=path+tsplit[:-2]+".tif"
                else:
                    print "error with path: " +path    
                print path + " (2007)"
        else: #Record Drawings
            tsplit = mysplit[4]
            ttsplit = tsplit[:-4] #remove the file extension
            print "here" + ttsplit
            path=self.rec_aud_path_paper
            path=path+mysplit[5]+"\\"+tsplit[:-4]
            pathaed=self.rec_aed_path_paper
            pathaed=pathaed+mysplit[5]+"\\"+tsplit[:-4]
            if os.path.isfile(path+".sid"):
                path=path+".sid" #need to check for img and jp2 formats....
                print path + "oh sid"
            elif os.path.isfile(pathaed+".sid"):
                path=pathaed+".sid" #need to check for img and jp2 formats....
                print path + "oh sid"
            elif os.path.isfile(path+".img"):
                path=path+".img" #need to check for img and jp2 formats....
                print path + "oh img"
            elif os.path.isfile(pathaed+".img"):
                path=pathaed+".img" #need to check for img and jp2 formats....
                print path + "oh img"
            elif os.path.isfile(path+".jp2"):
                path=path+".jp2" #need to check for img and jp2 formats....
                print path + "oh jp2"
            elif os.path.isfile(pathaed+".jp2"):
                path=pathaed+".jp2" #need to check for img and jp2 formats....
                print path + "oh jp2"
            elif os.path.isfile(path+".jpeg"):
                path=path+".jpeg" #need to check for img and jp2 formats....
                print path + "oh jpeg"
            elif os.path.isfile(pathaed+".jpeg"):
                path=pathaed+".jpeg" #need to check for img and jp2 formats....
                print path + "oh jpeg"
            elif os.path.isfile(path+".jpg"):
                path=path+".jpg" #need to check for img and jp2 formats....
                print path + "oh jpg"
            elif os.path.isfile(pathaed+".jpg"):
                path=pathaed+".jpg" #need to check for img and jp2 formats....
                print path + "oh jpg"
            else:
                tkMessageBox.showinfo("Well that seems to be it","That file doesn't exist")
                
            print path+" lost?"
        if os.path.isfile(path):
            print "file found....loading"
            print path
#            args1 = ("cmd /c start"+"|"+"title"+"|"+path) #also works, but only for jpgs/tifs, NOT sids, WHEN launched from ArcGIS.....typical.
            print "here 1"
            if (mysplit[0]=="Aerials"):
                args2 = ("c:\\workspace\\load_rasters\\src\\pythons_little_helper.bat Aerials " + path)
            else:
                 args2 = ("c:\\workspace\\load_rasters\\src\\pythons_little_helper.bat Record " + path)
                 
            print ("args2: "+args2+" path: "+path+"\n")
#           args3 = ("start"+"|"+"title"+"|"+path)
#            pid1=Popen(args1, shell=True, stdin=None, stdout=None, stderr=None,close_fds=True)
            print "here 2"
            pid2=Popen(args2, shell=False, stdin=None, stdout=None, stderr=None,close_fds=True)
#            pid3=Popen(args3, shell=True, stdin=None, stdout=None, stderr=None,close_fds=True)
            print "here 3, args, path: " + args2 + ":" + path
        else:
            tkMessageBox.showinfo("Well that seems to be it","That file doesn't exist. Please check your number and try again.")

#        print "here 4"
#        arg_local = ("C:\\Users\\wb11262\\AppData\\Local\\Apps\\2.0\\96C46K2N.D2B\\KZD8KQRW.5VV\\liza...app_a514fd0e4caeee8b_0005.0005_54b8632c5decc743\\GeoViewer.exe "+path)
#        print "here 5"
#        pidwes = Popen(arg_local,shell=False, stdin=None, stdout=None, stderr=None,close_fds=True)
#        print "spiffy"
#        arg_local2 = ("c:\\workspace\\load_rasters\\src\\pythons_little_helper.bat " + path)
#        pidwes = Popen(arg_local2,shell=False, stdin=None, stdout=None, stderr=None,close_fds=True)
 #       print "double-spiffy"
                
        
    #----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        otherFrame = Toplevel()
        otherFrame.geometry("400x300")
        otherFrame.title("otherFrame")
        handler = lambda: self.onCloseOtherFrame(otherFrame)
        btn = Button(otherFrame, text="Close", command=handler)
        btn.pack()
        
#        self.listBoxResults.insert(0, "my big fat list entry 4")
 
    #----------------------------------------------------------------------
    def onCloseOtherFrame(self, otherFrame):
        """"""
        otherFrame.destroy()
        self.show()
 
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()
 
####################
    #from http://forums.arcgis.com/threads/82210-arcpy.mapping-SelectLayerByLocation_management?p=289479#post289479
#    def onRectangle(self, rectangle_geometry):
    def selectRectangle(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
#        ext = rectangle_geometry
        ext = df.extent
        thepoly = arcpy.Polygon(arcpy.Array([ext.lowerLeft, ext.lowerRight, ext.upperRight,  ext.upperLeft]),df.spatialReference)

#        for lyr in arcpy.mapping.ListLayers(mxd):
#            arcpy.AddMessage(lyr.name + " first layer found")
#            if lyr.name=="mylayer":
#                dlyr = lyr
# need to check and make sure both of these exist at some point
#        arcpy.SelectLayerByLocation_management("ibounds", "INTERSECT", thepoly, "", "NEW_SELECTION")
        arcpy.SelectLayerByAttribute_management("ibounds","CLEAR_SELECTION")
        arcpy.SelectLayerByLocation_management("ibounds", "INTERSECT", thepoly, "", "ADD_TO_SELECTION")

        #arcpy.RefreshActiveView() #makes it flash too much
#http://resources.arcgis.com/en/help/main/10.1/index.html#//018v0000004p000000        
        if arcpy.Exists("c:/temp/resultsview"):
            arcpy.Delete_management("c:/temp/resultsview")

        mytable = "c:/temp/resultsview"
        arcpy.MakeTableView_management("ibounds",mytable)
        myfields=arcpy.ListFields(mytable)
        self.ListRes=[]
        myfields = ["CONTRACTOR","SETTITLE","DRAWING_DA","ENGINEEERI","FILENAME","CD","GEO_CD"]
        with arcpy.da.SearchCursor(mytable,myfields) as cursor:
                 for row in cursor:
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                     self.listBoxDetails.insert(END, row[1])
                     self.listBoxResults.insert(END, row[1])
                     
#        mylist = ["1","2","3","4"]
#        for row in mylist: #ListRes: #python book p 154 @ top, list iteration
#             self.listBoxResults.insert(END, mylist[row])

        self.BtnFindPoly.config(state=DISABLED)
        self.BtnFindPnt.config(state=DISABLED)
        self.show()
        
        #clean up the table view, apparently it is case sensitive
        arcpy.Delete_management("c:/temp/resultsview")
        return self.ListRes
        
#----------------------------------
# from http://gis.stackexchange.com/questions/49713/select-and-copy-features-in-arcmap-using-python-add-in-tool
#    def onMouseDownMap(self, x, y, button, shift):
#        import arcpy
    def selectMidPoint(self):
        import tkMessageBox
#        mxd = arcpy.mapping.MapDocument("C:/Users/wb11262/Documents/ArcGIS/default_project.mxd")  #used from calls outside the python window
        mxd = arcpy.mapping.MapDocument("CURRENT") #apparently, if you're using the "current" option, it can get the extents (next function), otherwise you need to save? See next line...fwb29May13
#        arcpy.env.workspace = "C:/mnt/gis/gis/"
#        arcpy.MakeFeatureLayer_management("aerial_tile.shp", "aerial_tile_tmp")
#        arcpy.MakeFeatureLayer_management("ibounds.shp", "ibounds_tmp")
        df=arcpy.mapping.ListDataFrames(mxd)[0] #have to call this each time to get the new dataframe description ##have to save before using this from outside the interface.
        wesextent = df.extent
        xmid = (wesextent.XMax+wesextent.XMin)/2
        ymid = (wesextent.YMax+wesextent.YMin)/2
        pointGeom = arcpy.PointGeometry(arcpy.Point(xmid, ymid), mxd.activeDataFrame.spatialReference)
        searchdistance=0.01
#        tkMessageBox.showinfo("Got Here",xmid+" and "+ymid)
        xypoint = str(xmid) + " , " + str(ymid)
        tkMessageBox.showinfo("Got Here ", xypoint)

#        searchdistance = getSearchDistanceInches(mxd.activeDataFrame.scale)
#        lyr = arcpy.mapping.ListLayers(mxd)[0] # assumes you want to select features from 1st layer in TOC
#        arcpy.SelectLayerByLocation_management(lyr, "INTERSECT", pointGeom, "%d INCHES" % searchdistance)
# need to check and make sure both of these exist at some point
#        arcpy.SelectLayerByLocation_management("1996 Aerial Photography Grid", "INTERSECT", pointGeom, "%d INCHES" % searchdistance, "NEW_SELECTION")
#        arcpy.SelectLayerByLocation_management("2002 Aerial Photography Grid", "INTERSECT", pointGeom, "%d INCHES" % searchdistance, "ADD_TO_SELECTION")
# 96, 02, 07 grids are identical, but 07 has more quads out in the county.  96 data has quad-0 if it's a large tile, ergo...
#  using these breaks the selection if the loadInMap fails.....hmmmm
#       arcpy.SelectLayerByLocation_management("2007 Aerial Photography Grid", "INTERSECT", pointGeom, "%d INCHES" % searchdistance, "NEW_SELECTION")
#        arcpy.SelectLayerByLocation_management("Record Drawings", "INTERSECT", pointGeom, "%d INCHES" % searchdistance, "ADD_TO_SELECTION")
###-------------if you don't have the projection set properly, then the selection will produce some unusual results.
#        arcpy.SelectLayerByLocation_management("aerial_tile", "INTERSECT", pointGeom, "%d INCHES" % searchdistance, "NEW_SELECTION")
#        arcpy.MakeFeatureLayer_management(aerial_tile,outLyr)
        arcpy.SelectLayerByAttribute_management("aerial_tile","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("ibounds","CLEAR_SELECTION")
        arcpy.SelectLayerByLocation_management("aerial_tile", "CONTAINS", pointGeom, "%d INCHES" % searchdistance,  "NEW_SELECTION")
        arcpy.SelectLayerByLocation_management("ibounds", "CONTAINS", pointGeom, "%d INCHES" % searchdistance, "ADD_TO_SELECTION")
##INTERSECT isn't supposed to care about searchdistance.  Contains does, but I lowered the amount from 5 to 0.01 above.
#### it lowered the results found form 571 to 8, which seems more appropriate.  It may be the switch to Contains, or the distance.
        ### I've also seen where it appears that previously made selections might muck up the new selection process even through the first item
        ###  says "NEW_SELECTION"
        #populate_found()
#        return
    
        #arcpy.RefreshActiveView()
#        print xmid,ymid
#        self.listBoxDetails.insert(END, xmid)
#        self.listBoxDetails.insert(END, ymid)
        if arcpy.Exists("c:/temp/resultsview1"):
            arcpy.Delete_management("c:/temp/resultsview1")
        if arcpy.Exists("c:/temp/resultsview2"):
            arcpy.Delete_management("c:/temp/resultsview2")
#        if arcpy.Exists("c:/temp/resultsview3"):
#            arcpy.Delete_management("c:/temp/resultsview3")
#        if arcpy.Exists("c:/temp/resultsview4"):
#            arcpy.Delete_management("c:/temp/resultsview4")

        mytable1 = "c:/temp/resultsview1"
#        arcpy.MakeTableView_management("2007 Aerial Photography Grid",mytable1)
        arcpy.MakeTableView_management("aerial_tile",mytable1)
        myfields1=arcpy.ListFields(mytable1)
        mytable2 = "c:/temp/resultsview2"
#        arcpy.MakeTableView_management("Record Drawings",mytable2)
        arcpy.MakeTableView_management("ibounds",mytable2)
        myfields2=arcpy.ListFields(mytable2)
        
        self.ListRes=[]
        self.listBoxResults.insert(END, "----------AERIALS-----------")
        self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Title Here","Year Here","Null","Null",0,0))
        
#        myfields1 = ["TILE","QUAD","FILE_"]
        myfields1 = ["TILENUM","QUAD"]
        with arcpy.da.SearchCursor(mytable1,myfields1) as cursor:
                 for row in cursor:
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Flyover","1996","Null",row[0],0,0))
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Flyover","2002","Null",row[0],0,0))
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Aerials","Flyover","2007","Null",row[0],0,0))
                     self.listBoxDetails.insert(END, row[0])
                     self.listBoxResults.insert(END, row[0])
                     self.listBoxResults.insert(END, row[0])
                     self.listBoxResults.insert(END, row[0])
                     
        self.listBoxResults.insert(END, "-----RECORD DRAWINGS-----")
        self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format("Scans","Title Here","Year Here","Null","Null",0,0))

        myfields2 = ["CONTRACTOR","SETTITLE","DRAWING_DA","ENGINEEERI","FILENAME","CD","GEO_CD"]
        with arcpy.da.SearchCursor(mytable2,myfields2) as cursor:
                 for row in cursor:
                     self.ListRes.append("{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                     self.listBoxDetails.insert(END, row[1])
                     self.listBoxResults.insert(END, row[1])
                     
#        mylist = ["1","2","3","4"]
#        for row in mylist: #ListRes: #python book p 154 @ top, list iteration
#             self.listBoxResults.insert(END, mylist[row])

        self.BtnFindPnt.config(state=DISABLED)
        self.BtnFindPoly.config(state=DISABLED)
        
        #clean up the table view, apparently it is case sensitive
        arcpy.Delete_management("c:/temp/resultsview1")
        arcpy.Delete_management("c:/temp/resultsview2")
        return self.ListRes
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    root.geometry("880x300")
    app = FindAsBuilts(root)
#    app = ToolClass10(root)
    root.mainloop()

#----------------------
# from http://gis.stackexchange.com/questions/31684/how-do-i-retrieve-start-and-end-point-coordinates-with-python-arcpy

#import arcpy
#infc = arcpy.GetParameterAsText(0)

# Enter for loop for each feature
#
#for row in arcpy.da.SearchCursor(infc, ["OID@", "SHAPE@"]):
    # Print the current line ID

#    print("Feature {0}:".format(row[0]))

    #Set start point
#    startpt = row[1].firstPoint

    #Set Start coordinates
#    startx = startpt.X
#    starty = startpt.Y

    #Set end point
#    endpt = row[1].lastPoint

    #Set End coordinates
#    endx = endpt.X
#    endy = endpt.Y

