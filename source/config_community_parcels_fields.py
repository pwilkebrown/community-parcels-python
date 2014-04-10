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

def main(config_file,                   ##0

         localparcels = "",             ##1
         communityparcellocalcopy ="",  ##2
         CreateCurrent = True,          ##3
         localfips ="",                 ##4

         LowParcelID = "",              ##5-x
         ParcelID =  "",                ##6-x
         FloorDesignator = "",          ##7-x
         StatedArea = "",               ##8-x
         ConveyanceName = "",           ##9-x
         UseCode = "",                  ##10-x
         UseDescription = "",           ##11-x
         TaxUseDescription = "",        ##12-x
         Improved = "",                 ##13-x
         Owntype = "",                  ##14-x
         SiteAddress = "",              ##15-x
         Ownername1 = "",               ##16-x
         Ownername2 = "",               ##17-x
         PostalAddress = "",            ##18-x
         USPSBox = "",                  ##19-x
         State = "",                    ##20-x
         City = "",                     ##21-x
         Zip = "",                      ##22-x
         InternationalAddress = "",     ##23-x
         TaxableValue = "",             ##24-x
         SalePrice = "",                ##25-x
         SaleDate = "",                 ##26-x
         LocalFIPS = "",                ##27-x
         StateFIPS = "",                ##28-x
         GNISID = "",                   ##29-x
         LastEditor = "",               ##30-x
         LastUpdate = "",               ##31-x
         SHAPE_Length = "",             ##32-x
         SHAPE_Area = "",               ##33-x
         ImprovedValue = "",            ##34-x
         LandValue = "",                ##35-x
         AssessedValue = "",            ##36-x

         *args):

    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    # Add general parameters
    section = 'LOCAL_DATA'
    p_names = ['LOCALPARCELS','COMMUNITYPARCELSLOCALCOPY','CreateCurrent','localfips']
    p_vals  = [ localparcels,  communityparcellocalcopy,   CreateCurrent , localfips ]

    arcpy.AddMessage('Writing general parameters...')
    write_config(p_names, p_vals, config, section)


    #Add general publication parameters
    section = 'FIELD_MAPPER'
    p_names = ['LowParcelID','ParcelID','FloorDesignator','StatedArea','ConveyanceName', 'UseCode', 'UseDescription', 'TaxUseDescription', 'Improved', 'Owntype', 'SiteAddress', 'Ownername1', 'Ownername2', 'PostalAddress', 'USPSBox', 'State', 'City', 'Zip', 'InternationalAddress', 'TaxableValue','SalePrice', 'SaleDate', 'LocalFIPS', 'StateFIPS', 'GNISID', 'LastEditor','LastUpdate', 'ImprovedValue', 'LandValue', 'AssessedValue']
    p_vals  = [ LowParcelID , ParcelID ,  FloorDesignator, StatedArea , ConveyanceName ,  UseCode ,  UseDescription ,  TaxUseDescription ,  Improved ,  Owntype ,  SiteAddress ,  Ownername1 ,  Ownername2 ,  PostalAddress ,  USPSBox ,  State ,  City ,  Zip ,  InternationalAddress ,  TaxableValue , SalePrice ,  SaleDate ,  LocalFIPS ,  StateFIPS ,  GNISID ,  LastEditor , LastUpdate ,  ImprovedValue ,  LandValue ,  AssessedValue ]

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