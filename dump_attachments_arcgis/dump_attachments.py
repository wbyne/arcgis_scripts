#from: http://mapthis.net/how-to/exporting-geodatabase-feature-attachments-python/
def main():
    pass
import arcpy
import os
 
#Script Variables
sourceAttachmentTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH__ATTACH_1'
targetOutputFolder = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\Attachment_Export'
filePathAttribute = 'FILE_PATH_2'

swStructTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH'
 
#Create a new column to contain the path to each exported file
if not filePathAttribute in arcpy.ListFields(sourceAttachmentTable):
    arcpy.AddField_management(sourceAttachmentTable, filePathAttribute, 'TEXT', '', '', 200)
 
#Update the new column with the export path for each attachment
    #had to change REL_OBJECTID to REL_GLOBALID
#with arcpy.da.UpdateCursor(sourceAttachmentTable, [filePathAttribute, 'REL_GLOBALID', 'ATT_NAME']) as cursor:
with arcpy.da.UpdateCursor(sourceAttachmentTable, [filePathAttribute, 'REL_GLOBALID']) as cursor:
    for row in cursor:
        searchclause = r"GlobalID = "+"\'"+row[1]+"\'"
        #strings: wes = "{spam}", a=wes[0] (is {), b=wes[-1](is }), c = wes[1:-1] (is spam).  if you specify the final value, it is
        #  NOT inclusive.  First value is inclusive, otherwise addition might add the same value twice (pythoncentral.io/cutting-and-slicing-strings-in-python)
        #with arcpy.da.SearchCursor(swStructTable,"*",where_clause = r'''GlobalID LIKE \'\{00360D27-6FEF-4BF9-986D-1F881C66292F\}\'''') as mysearchcursor:
#searchclause = "GLOBALID = "+"""+str(row[1])+"""
        with arcpy.da.SearchCursor(swStructTable,['FACILITYID','GLOBALID'],where_clause = searchclause) as mysearchcursor:
            for searchrows in mysearchcursor:
                spam = searchrows[0]
                print spam
        row[0] = targetOutputFolder + os.sep + spam
#        row[0] = targetOutputFolder + os.sep + row[1]
        print row[0]
        cursor.updateRow(row)
        del row
    del cursor
 
#Export attachments from attachment table
with arcpy.da.SearchCursor(sourceAttachmentTable, [filePathAttribute, 'DATA']) as cursor:
    for row in cursor:
        counter = 0
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        outPath = row[0]+"."+alphabet[counter] #should be name.a for the first entry
        while (os.path.exists(outPath+".jpg")):
            counter = counter + 1
            if (outPath[-1] == alphabet[counter-1]): #outPath already has an 'a','b','c' extension
                outPath = outPath[0:-2]+"."+alphabet[counter]
#            else:
# shouldn't need anymore since we're requiring the name to start with 'a' outPath = outPath+"."+alphabet[counter]
        outPath = outPath+".jpg"
        blobData = row[1]
        open(outPath, 'wb').write(blobData.tobytes())
        del row
    del cursor
 
 
if __name__ == '__main__':
    main()
