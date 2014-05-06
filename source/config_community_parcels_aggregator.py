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

def main(config_file,                   ##0

         communityparcellocalcopy ="",  ##1
         localparcels ="",              ##2
         CreateCurrent = True,          ##3
         localfips ="",                 ##4

         FEATURESERVICEURL ="",         ##5
         DELETESQL ="",                 ##6

         USER = "",                     ##7
         PASS = "",                     ##8

         *args):

    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    # Add general parameters
    section = 'LOCAL_DATA'
    p_names = ['COMMUNITYPARCELSLOCALCOPY', 'localparcels', 'CreateCurrent','localfips']
    p_vals  = [ communityparcellocalcopy,  localparcels, CreateCurrent , localfips ]

    arcpy.AddMessage('Writing general parameters...')
    write_config(p_names, p_vals, config, section)


    # Add parameters for creating features from XY values
    section = 'FS_INFO'
    p_names = ['FEATURESERVICEURL','DELETESQL']
    p_vals  = [ FEATURESERVICEURL,  DELETESQL ]

    arcpy.AddMessage('Writing parameters for Feature Service...')
    write_config(p_names, p_vals, config, section)


    # Add parameters for creating features from addresses
    section = 'AGOL'
    p_names = ['USER','PASS']
    p_vals  = [ USER , PASS ]

    arcpy.AddMessage('Writing username and password...')
    write_config(p_names, p_vals, config, section)


    # Save configuration to file
    cfgpath = dirname(realpath(__file__))
    cfgfile = join(cfgpath, "{}".format(config_file))

    with open(cfgfile, "w") as cfg:
        arcpy.AddMessage('Saving configuration "{}"...'.format(cfgfile))
        config.write(cfg)

    arcpy.AddMessage('Done.')

if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)
