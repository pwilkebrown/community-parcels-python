"""
    @author:
    @contact:
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

from os.path import dirname, join, realpath
import arcpy
import ConfigParser

#C:\EsriApplications\Community Parcels\CommunityParcels\source\configs\test.ini

def write_config(names, vals, config, section):

    config.add_section(section)

    i = 0
    while i < len(names):
        if vals[i] == "#" or vals[i] == "":
            vals[i] = ''
        config.set(section, names[i], vals[i])
        i += 1

def main(config_file,                   #0

         localparcels = "",             #1
         communityparcellocalcopy ="",  #2
         CreateCurrent = True,          #3
         localfips ="",                 #4

         LowParcelID = "",              #5
         ParcelID =  "",                #6
         FloorDesignator = "",          #7
         StatedArea = "",               #8
         ConveyanceName = "",           #9
         UseCode = "",                  #10
         UseDescription = "",           #11
         TaxUseDescription = "",        #12
         Improved = "",                 #13
         Owntype = "",                  #14
         SiteAddress = "",              #15
         Ownername1 = "",               #16
         Ownername2 = "",               #17
         PostalAddress = "",            #18
         USPSBox = "",                  #19
         State = "",                    #20
         City = "",                     #21
         Zip = "",                      #22
         InternationalAddress = "",     #23
         TaxableValue = "",             #24
         SalePrice = "",                #25
         SaleDate = "",                 #26
         LocalFIPS = "",                #27
         StateFIPS = "",                #28
         GNISID = "",                   #29
         LastEditor = "",               #30
         LastUpdate = "",               #31
         SHAPE_Length = "",             #32
         SHAPE_Area = "",               #33
         ImprovedValue = "",            #34
         LandValue = "",                #35
         AssessedValue = "",            #36

         *args):

    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    # Add general parameters
    section = 'LOCAL_DATA'
    p_names = ['LOCALPARCELS',
                'COMMUNITYPARCELSLOCALCOPY',
                'CreateCurrent',
                'localfips']

    p_vals  = [ localparcels,
                communityparcellocalcopy,
                CreateCurrent ,
                localfips ]

    arcpy.AddMessage('Writing general parameters...')
    write_config(p_names, p_vals, config, section)


    #Add general publication parameters
    section = 'FIELD_MAPPER'
    p_names = ['LowParcelID',
                'ParcelID',
                'FloorDesignator',
                'StatedArea',
                'ConveyanceName',
                'UseCode',
                'UseDescription',
                'TaxUseDescription',
                'Improved',
                'Owntype',
                'SiteAddress',
                'Ownername1',
                'Ownername2',
                'PostalAddress',
                'USPSBox',
                'State',
                'City',
                'Zip',
                'InternationalAddress',
                'TaxableValue',
                'SalePrice',
                'SaleDate',
                'LocalFIPS',
                'StateFIPS',
                'GNISID',
                'LastEditor',
                'LastUpdate',
                'ImprovedValue',
                'LandValue',
                'AssessedValue']

    p_vals  = [ LowParcelID ,
                ParcelID ,
                FloorDesignator,
                StatedArea ,
                ConveyanceName ,
                UseCode ,
                UseDescription ,
                TaxUseDescription ,
                Improved ,
                Owntype ,
                SiteAddress ,
                Ownername1 ,
                Ownername2 ,
                PostalAddress ,
                USPSBox ,
                State ,
                City ,
                Zip ,
                InternationalAddress ,
                TaxableValue ,
                SalePrice ,
                SaleDate ,
                LocalFIPS ,
                StateFIPS ,
                GNISID ,
                LastEditor ,
                LastUpdate ,
                ImprovedValue ,
                LandValue ,
                AssessedValue ]

    arcpy.AddMessage('Writing general publication configuration parameters...')
    write_config(p_names, p_vals, config, section)


    # Save configuration to file
    cfgpath = dirname(realpath(__file__))
    cfgfile = join(cfgpath, "{}.ini".format(config_file))

    with open(cfgfile, "w") as cfg:
        arcpy.AddMessage('Saving configuration "{}"...'.format(cfgfile))
        config.write(cfg)

    arcpy.AddMessage('Done.')

if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)
