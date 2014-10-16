import arcpy
import os


#TILELIST = [1...378] #there are 377 full tiles
#Script Variables
#TargetTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH'
##TargetTable = "swStructure_TH"
TargetTable = "Storm Gravity Mains"
#targetOutputFolder = r'C:\TEMP\thomas_hutton_gis_T_H_Submittal_1\Attachment_Export'
#filePathAttribute = 'FILE_PATH'

for tile in range(69,112): #378
    tile_select = "TILE = "+str(tile)
#    tile_select = "TILE LIKE "+"'%"+tile+"%'"
    arcpy.SelectLayerByAttribute_management("aerial_tile","New_Selection",tile_select)
    arcpy.SelectLayerByLocation_management("swStructure_TH","HAVE_THEIR_CENTER_IN","aerial_tile")
    feature_no = 0
    with arcpy.da.UpdateCursor(TargetTable, ['FACILITYID','tile_no']) as cursor:
        for row in cursor:
            if (tile > 100):
                tilestr = str(tile)
            elif (tile > 10):
                tilestr = "0"+str(tile)
            else:
                tilestr = "00"+str(tile)
# FOR STRUCTURES            row[0] = "RY"+tilestr+"S"+str(feature_no).zfill(4)
            row[0] = "RY"+tilestr+"G"+str(feature_no).zfill(4)
            #zfill from stackexchange site on how to pad strings with zeros
            row[1] = tilestr
            feature_no=feature_no+1
            cursor.updateRow(row)
            del row
        del cursor
