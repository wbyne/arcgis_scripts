#from: http://mapthis.net/how-to/exporting-geodatabase-feature-attachments-python/
def main():
    pass
import arcpy
import os
 
#Script Variables
sourceAttachmentTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH__ATTACH_1'
targetOutputFolder = r'C:\TEMP\thomas_hutton_gis_T_H_Submittal_1\Attachment_Export'
filePathAttribute = 'FILE_PATH'

swStructTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH'
 
#Create a new column to contain the path to each exported file
if not filePathAttribute in arcpy.ListFields(sourceAttachmentTable):
    arcpy.AddField_management(sourceAttachmentTable, filePathAttribute, 'TEXT', '', '', 200)
 
#Update the new column with the export path for each attachment
    #had to change REL_OBJECTID to REL_GLOBALID
#with arcpy.da.UpdateCursor(sourceAttachmentTable, [filePathAttribute, 'REL_GLOBALID', 'ATT_NAME']) as cursor:
with arcpy.da.UpdateCursor(sourceAttachmentTable, [filePathAttribute, 'REL_GLOBALID']) as cursor:
    for row in cursor:
        searchclause = "GLOBALID = "+str(row[1])
        with arcpy.da.SearchCursor(swStructTable,['FACILITYID','GLOBALID'],where_clause = searchclause) as mysearchcursor:
            for searchrows in mysearchcursor:
                spam = searchrows[2]
                print spam
        row[0] = targetOutputFolder + os.sep + row[1]
        print row[0]
#        cursor.updateRow(row)
        del row
    del cursor
 
#Export attachments from attachment table
with arcpy.da.SearchCursor(sourceAttachmentTable, [filePathAttribute, 'DATA']) as cursor:
    for row in cursor:
        outPath = row[0]
        blobData = row[1]
        open(outPath, 'wb').write(blobData.tobytes())
        del row
    del cursor
 
 
if __name__ == '__main__':
    main()
