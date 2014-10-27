import arcpy
import os
import sys

#TILELIST = [1...378] #there are 377 full tiles
#Script Variables
#TargetTable = r'C:\TEMP\thomas_hutton_gis\T_H_Submittal_2\20141002\20141002\AED.gdb\swStructure_TH'
TargetTable =[]
TargetTable.append("WK_Dickson\Submission_1\swStructure")
TargetTable.append("WK_Dickson\Submission_1\Storm Gravity Mains")
TargetTable.append("WK_Dickson\Submission_1\Storm Open Drains")
#####TargetTable.append("WK_Dickson\Submission_2\Storm Detention Areas")
TargetTable.append("WK_Dickson\Submission_1\swDetention") #smartass
counter=0 #starts counting at 0.  Don't forget.
#sanity check
with arcpy.da.SearchCursor(TargetTable[counter], ['FACILITYID']) as cursor:
    for row in cursor:
        if (len(row[0]) != 14):
            print "string at "+row[0]+" is the wrong length, stopping"
##            sys.exit("Short String")

List_of_Bad_Rows = []
        
with arcpy.da.UpdateCursor(TargetTable[counter], ['FACILITYID']) as cursor:
    for row in cursor:
#FOR STRUCTURES
        if (len(row[0]) != 14):
            print "string at "+row[0]+" is the wrong lenth, adding to the list"
            #sys.exit("Short String")
            List_of_Bad_Rows.append(row)
            next
        spam = row[0]
        print "raw myrow[0] is: "+spam
        firstpart = spam[0:2]
        secondpart = spam[3:6]
        thirdpart = spam[10:]
        row[0] = firstpart+secondpart+"S"+thirdpart
        print "fixed myrow[0] is: "+row[0]
        
        ###cursor.updateRow(row)
        del row
    del cursor

for row in List_of_Bad_Rows:
    print row


List_of_Bad_Rows = []

counter = 1 #Gravity Mains from Toole Submission 2 has From and To Manholes that need to be renumbered.
##sanity check this table....sometimes....

with arcpy.da.UpdateCursor(TargetTable[counter], ['FACILITYID','FROMMH','TOMH']) as cursor:
    for row in cursor:
##        if (len(row[0]) != 14) or (len(row[1]) != 14) or (len(row[2]) != 14):
            ##print "a malformed string escaped detection, it's either Row_1,2,or3: "+row[0]+":"+row[1]+":"+row[2]
            ##sys.exit("STOPPING JUST BECAUSE")
##            List_of_Bad_Rows.append(row)
        for column in [0,1,2]:
            if  (row[column] is not None) and (len(row[column]) == 14): 
                spam = row[column]
                print "raw myrow"+str(column)+" is: "+spam
                firstpart = spam[0:2]
                secondpart = spam[3:6]
                thirdpart = spam[10:]
                row[column] = firstpart+secondpart+"G"+thirdpart
                print "fixed myrow"+str(column)+" is: "+row[column]
            elif  (row[column] is not None) and (len(row[column]) == 15): 
                spam = row[column]
                print "raw myrow"+str(column)+" is: "+spam
                firstpart = spam[0:2]
                secondpart = spam[3:6]
                if spam[9:10] is " ":
                    thirdpart = spam[11:]
                else:
                    print "i dont know what to do here"
                row[column] = firstpart+secondpart+"G"+thirdpart
                print "fixed myrow"+str(column)+" is: "+row[column]
            else:
                List_of_Bad_Rows.append(row)
        cursor.updateRow(row)
        del row
    del cursor

arcpy.SelectLayerByAttribute_management(TargetTable[counter],"CLEAR_SELECTION")

for row in List_of_Bad_Rows:
    arcpy.SelectLayerByAttribute_management(TargetTable[counter],"ADD_TO_SELECTION","FACILITYID LIKE "+"\'"+row[0]+"\'")
    print row
    
