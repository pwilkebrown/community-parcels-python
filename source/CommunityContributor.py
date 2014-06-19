"""
    @author:
    @contact:
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014

"""
import arcpy
import sys, os, datetime
import ConfigParser
from os.path import dirname, join, exists, splitext, isfile

from arcpy import env
from arcrest.agol import layer

logFileName ='.\\logs\\ParcelUpdate.log'
##configFilePath =  '.\\configs\\UpdateCommunityParcels.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def main(config_file, *args):

    # Set overwrite output option to True
    arcpy.env.overwriteOutput = True

    if isfile(config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)

    else:
        print "INI file not found."
        sys.exit()

# Config File

    username = config.get( 'AGOL', 'user')
    password = config.get('AGOL', 'pass')
    LocalParcels = config.get('LOCAL_DATA', 'localparcels')
    CommunityParcelsLocalCopy = config.get('LOCAL_DATA', 'communityparcelslocalcopy')
    createCurrent = config.get('LOCAL_DATA', 'createcurrent')
    reportCurrentURL = config.get('FS_INFO', 'featureserviceurl')
    deleteSQL = config.get('FS_INFO', 'deletesql')
    countycityname = config.get ('LOCAL_DATA','localfips')
    LowParcelID = config.get ('FIELD_MAPPER', 'lowparcelid')
    ParcelID = config.get ('FIELD_MAPPER', 'parcelid')
    FloorDesignator = config.get ('FIELD_MAPPER', 'floordesignator')
    StatedArea = config.get ('FIELD_MAPPER', 'statedarea')
    ConveyanceName = config.get ('FIELD_MAPPER', 'conveyancename')
    UseCode = config.get ('FIELD_MAPPER', 'usecode')
    UseDescription = config.get ('FIELD_MAPPER', 'usedescription')
    TaxUseDescription = config.get ('FIELD_MAPPER', 'taxusedescription')
    Improved = config.get ('FIELD_MAPPER', 'improved')
    Owntype = config.get ('FIELD_MAPPER', 'owntype')
    SiteAddress = config.get ('FIELD_MAPPER', 'siteaddress')
    Ownername1 = config.get ('FIELD_MAPPER', 'ownername1')
    Ownername2 = config.get ('FIELD_MAPPER', 'ownername2')
    PostalAddress = config.get ('FIELD_MAPPER', 'postaladdress')
    USPSBox = config.get ('FIELD_MAPPER', 'uspsbox')
    State = config.get ('FIELD_MAPPER', 'state')
    City = config.get ('FIELD_MAPPER', 'city')
    Zip = config.get ('FIELD_MAPPER', 'zip')
    InternationalAddress = config.get ('FIELD_MAPPER', 'internationaladdress')
    TaxableValue = config.get ('FIELD_MAPPER', 'taxablevalue')
    SalePrice = config.get ('FIELD_MAPPER', 'saleprice')
    SaleDate = config.get ('FIELD_MAPPER', 'saledate')
    LocalFIPS = config.get ('FIELD_MAPPER', 'localfips')
    StateFIPS = config.get ('FIELD_MAPPER', 'statefips')
    GNISID = config.get ('FIELD_MAPPER', 'gnisid')
    LastEditor = config.get ('FIELD_MAPPER', 'lasteditor')
    LastUpdate = config.get ('FIELD_MAPPER', 'lastupdate')
    ##SHAPE_Length = config.get ('FIELD_MAPPER', 'SHAPE_Length')
    ##SHAPE_Area = config.get ('FIELD_MAPPER', 'SHAPE_Area')
    ImprovedValue = config.get ('FIELD_MAPPER', 'improvedvalue')
    LandValue = config.get ('FIELD_MAPPER', 'landvalue')
    AssessedValue = config.get ('FIELD_MAPPER', 'assessedvalue')


    print "Loading Configuration File"
    arcpy.AddMessage("Loading Configuration File")


    if arcpy.Exists(LocalParcels) == False:
        print "Please specify a input parcel feature class (LocalParcels=) in the configuration file, exiting"
        arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
        sys.exit()


    if CommunityParcelsLocalCopy == "":
        print "Please specify a input community parcel layer (CommunityParcelsLocalCopy=) in the configuration file, exiting"
        arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
        sys.exit()


    if username == "":
        print "Please specify a ArcGIS Online Username (username =)in the configuration file, exiting"
        arcpy.AddMessage(username)
        sys.exit()


    if password == "":
        print "Please specify a ArcGIS Online password (password =)in the configuration file, exiting"
        arcpy.AddMessage(password)
        sys.exit()


    if deleteSQL == "":
        print "Please specify a SQL query (DELETESQL= LOCALFIPS ='jurisdiction') in the configuration file, exiting"
        arcpy.AddMessage("Please specify a SQL query (DELETESQL= LOCALFIPS ='jurisdiction') in the configuration file, exiting")
        sys.exit()


    fs = layer.FeatureLayer(url=reportCurrentURL,username=username,password=password)
    if fs == None:
        print "Cannot find or connect to service, make sure service is accessible"
        arcpy.AddMessage("Cannot find or connect to service, make sure service is accessible")
        sys.exit()


    # Update Current service if used - see the services helper in the agolhelper folder


    if createCurrent == "True":
        fs.url = reportCurrentURL


    # Delete existing dataset that matches the community parcel schema
        arcpy.management.TruncateTable(CommunityParcelsLocalCopy)
        print "Cleaning up local parcel data"


    # Append new parcels into the community parcels schema, field map your data into the community schema.  Add local data field names after the "#" in the list.
    # For example, for STATEAREA "STATEAREA" true true false 50 Text 0 0 ,First,#,LocalParcels,TotalAcres,-1,-1;  The local Parcels field name from STATEDAREA (community parcels schema) is TotalAcres.


        common_vars = "true true false 50 Text 0 0, First, #"


        if LowParcelID == "":
            new_field = """LOWPARCELID 'Low Parcel Identification Number' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """LOWPARCELID 'Low Parcel Identification Number' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, LowParcelID)
        field_map = "{}".format(new_field)




        if ParcelID =="":
            new_field = """PARCELID 'Parcel Identification Number' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PARCELID 'Parcel Identification Number' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, ParcelID)


        field_map = "{}; {}".format(field_map, new_field)




        if FloorDesignator =="":
            new_field = """FLOORDESIG 'Floor Designator' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """FLOORDESIG 'Floor Designator' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, FloorDesignator)


        field_map = "{}; {}".format(field_map, new_field)




        if StatedArea =="":
            new_field = """STATEAREA 'Stated Area' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """STATEAREA 'Stated Area' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, StatedArea)


        field_map = "{}; {}".format(field_map, new_field)




        if ConveyanceName =="":
            new_field = """CNVYNAME 'Sub or Condo Name' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """CNVYNAME 'Sub or Condo Name' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, ConveyanceName)


        field_map = "{}; {}".format(field_map, new_field)




        if UseCode =="":
            new_field = """USEDCD 'Parcel Use Code' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """USEDCD 'Parcel Use Code' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, UseCode)


        field_map = "{}; {}".format(field_map, new_field)


        if UseDescription =="":
            new_field = """USEDSCRP 'Parcel Use Description' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """USEDSCRP 'Parcel Use Description' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, UseDescription)


        field_map = "{}; {}".format(field_map, new_field)




        if TaxUseDescription =="":
            new_field = """CVTTXDSCRP 'Tax District Description' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """CVTTXDSCRP 'Tax District Description' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, TaxUseDescription)


        field_map = "{}; {}".format(field_map, new_field)




        if Improved =="":
            new_field = """IMPROVED 'Improved Structure' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """IMPROVED 'Improved Structure' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, Improved)


        field_map = "{}; {}".format(field_map, new_field)




        if Owntype =="":
            new_field = """OWNTYPE 'Owner Type' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """OWNTYPE 'Owner Type' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, Owntype)


        field_map = "{}; {}".format(field_map, new_field)




        if SiteAddress =="":
            new_field = """SITEADRESS 'Physical Address' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """SITEADRESS 'Physical Address' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, SiteAddress)


        field_map = "{}; {}".format(field_map, new_field)




        if Ownername1 =="":
            new_field = """OWNERNME1 'First Owner Name' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """OWNERNME1 'First Owner Name' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, Ownername1)


        field_map = "{}; {}".format(field_map, new_field)




        if Ownername2 =="":
            new_field = """OWNERNME2 'Second Owner Name' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """OWNERNME2 'Second Owner Name' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, Ownername2)


        field_map = "{}; {}".format(field_map, new_field)


        if PostalAddress =="":
            new_field = """PSTLADRESS 'Mailing Address' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PSTLADRESS 'Mailing Address' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, PostalAddress)


        field_map = "{}; {}".format(field_map, new_field)




        if USPSBox =="":
            new_field = """USPSBOX 'US Postal Box Number' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """USPSBOX 'US Postal Box Number' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, USPSBox)


        field_map = "{}; {}".format(field_map, new_field)




        if City =="":
            new_field = """PSTLCITY 'City' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PSTLCITY 'City' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, City)


        field_map = "{}; {}".format(field_map, new_field)




        if State =="":
            new_field = """PSTLSTATE'State' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PSTLSTATE 'State' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, State)


        field_map = "{}; {}".format(field_map, new_field)




        if Zip =="":
            new_field = """PSTLZIP 'Zip Code' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PSTLZIP 'Zip Code' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, Zip)


        field_map = "{}; {}".format(field_map, new_field)




        if InternationalAddress =="":
            new_field = """PSTLINTER 'International Postal Address' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """PSTLINTER 'International Postal Address' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, InternationalAddress)


        field_map = "{}; {}".format(field_map, new_field)




        if TaxableValue =="":
            new_field = """CNTTXBLVAL 'Current Taxable Value' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """CNTTXBLVAL 'Current Taxable Value' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, TaxableValue)


        field_map = "{}; {}".format(field_map, new_field)




        if SalePrice =="":
            new_field = """SALEPRICE 'Last Sale Price' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """SALEPRICE 'Last Sale Price' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, SalePrice)


        field_map = "{}; {}".format(field_map, new_field)




        if SaleDate =="":
            new_field = """SALEDATE 'Last Sale Date' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """SALEDATE 'Last Sale Date' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, SaleDate)


        field_map = "{}; {}".format(field_map, new_field)




        if LocalFIPS =="":
            new_field = """LOCALFIPS 'Local FIPS Code' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """LOCALFIPS 'Local FIPS Code' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, LocalFIPS)


        field_map = "{}; {}".format(field_map, new_field)




        if StateFIPS =="":
            new_field = """STCOFIPS 'State FIPS Code' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """STCOFIPS 'State FIPS Code' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, StateFIPS)


        field_map = "{}; {}".format(field_map, new_field)




        if ImprovedValue =="":
            new_field = """IMPVALUE 'Improved Structure Value' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """IMPVALUE 'Improved Structure Value' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, ImprovedValue)


        field_map = "{}; {}".format(field_map, new_field)




        if LandValue =="":
            new_field = """LNDVALUE 'Land Value' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """LNDVALUE 'Land Value' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, LandValue)


        field_map = "{}; {}".format(field_map, new_field)


        if AssessedValue =="":
            new_field = """CNTASSDVAL 'Current Assessed Value' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """CNTASSDVAL 'Current Assessed Value' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, AssessedValue)


        field_map = "{}; {}".format(field_map, new_field)


        if GNISID =="":
            new_field = """GNISID 'Geographic Names Information System Code' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """GNISID 'Geographic Names Information System Code' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, GNISID)


        field_map = "{}; {}".format(field_map, new_field)


        if LastEditor =="":
            new_field = """LASTEDITOR 'Last Editor' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """LASTEDITOR 'Last Editor' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, LastEditor)


        field_map = "{}; {}".format(field_map, new_field)




        if LastUpdate =="":
            new_field = """LASTUPDATE 'Last Update' true true false 50 Text 0 0, First, #"""


        else:
            new_field = """LASTUPDATE 'Last Update' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, LastUpdate)


        field_map = "{}; {}".format(field_map, new_field)


##        if SHAPE_Length =="":
##            new_field = """SHAPE_Length 'SHAPE_Length' true true false 50 Text 0 0, First, #"""
##
##
##        else:
##            new_field = """SHAPE_Length 'SHAPE_Length' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, SHAPE_Length)
##
##
##        field_map = "{}; {}".format(field_map, new_field)
##
##
##
##
##        if SHAPE_Area =="":
##            new_field = """SHAPE_Area 'SHAPE_Area' true true false 50 Text 0 0, First, #"""
##
##
##        else:
##            new_field = """SHAPE_Area 'SHAPE_Area' {}, {}, {}, -1, -1""".format(common_vars, LocalParcels, SHAPE_Area)
##
##
##        field_map = "{}; {}".format(field_map, new_field)




        arcpy.Append_management(LocalParcels, CommunityParcelsLocalCopy, "NO_TEST", field_map)


        print "Mapping Local Parcel data to Community Parcel Schema"
        print "Community Parcel Update to ArcGIS Online Started, please be patient"
        arcpy.AddMessage("Mapping Local Parcel data to Community Parcel Schema")
        arcpy.AddMessage("Community Parcel Update to ArcGIS Online Started, please be patient")


    #Calculate Last Editor Field
        calc0 = '"{0}"'.format(username)
        arcpy.CalculateField_management(CommunityParcelsLocalCopy, "LASTEDITOR", calc0)
        print "Calculating Last Editor"
        arcpy.AddMessage("Calculating Last Editor")


    # Calculate the Last Update field


        arcpy.CalculateField_management(CommunityParcelsLocalCopy, "LASTUPDATE", "time.strftime(\"%m/%d/%Y\")", "PYTHON", "")
        print "Calculating Last Update "
        arcpy.AddMessage("Calculating Last Update")


    # Calculate the LOCALFIPS to the County/City Name
        calc = '"{0}"'.format(countycityname)
        arcpy.CalculateField_management(CommunityParcelsLocalCopy, "LOCALFIPS", calc, "VB", "")
        print "Set FIPS Code information"
        arcpy.AddMessage("Calculating 'FIPS' Code Information")



    #Calculate improved information
        arcpy.CalculateField_management(CommunityParcelsLocalCopy, "IMPROVED", "improve", "VB", "Dim improve\\nIf [IMPVALUE] > 1 Then\\nimprove = \"YES\"\\n\\nelse\\nimprove = \"NO\"\\n\\nend if\\n")
        print "Calculating Improved Structure information"
        arcpy.AddMessage("Calculating Improved Structure information")
        print "Truncating Parcels from Feature Service"
        arcpy.AddMessage("Truncating Parcels from Feature Service")


        try:
                value1 = fs.query(where=deleteSQL, returnIDsOnly=True)
                myids=value1 ['objectIds']


                minId = min(myids)
                i = 0
                maxId = max(myids)


                print minId
                print maxId
                chunkSize = 1000


                while (i <= len(myids)):
                    #print myids[i:i+1000]
                    oids = ",".join(str(e) for e in myids[i:i+chunkSize])
                    print oids
                    if oids == '':
                        continue
                    else:
                        fs.deleteFeatures(objectIds=oids)
                    i+=chunkSize
                    print i
                    print "Completed: {0:2f}%".format( i/ float(len(myids))*100)
                    arcpy.AddMessage("Deleted: {0:2f}%".format ( i/ float(len(myids))*100))


        except:
            pass


        print "Community Parcels upload Started"
        arcpy.AddMessage("Community Parcels upload started, please be patient.  For future consideration, please run tool during non-peak internet usage")
        fs.addFeatures(CommunityParcelsLocalCopy)


if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)


