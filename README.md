# Community Parcels


## Features

Update Community Parcels

The Community Parcel solution will leverage the core ArcGIS Platform to help communities aggregate parcel information from authoritative sources in a simple and sustainable way and leverage this information in many workflows. 

This GitHub repository houses the data aggregation toolset used to update the community parcels (seamless set of parcels) feature service. 

This solutions makes use of [ArcRest] (https://github.com/Esri/ArcREST)

Toolset Include the following:

1. Map source parcel fields to the Community Parcel Schema - Leverage ArcGIS Parcel Management solution (can contribute seamlessly), Users can also contribute shapefiles, GDB feature classes (field mapping required)

2. Update the Community Parcels service - Truncate, delete parcels from existing service (based on FIPS code), Add authoritative parcel data from local source

3. Promote ongoing contributions - Run ad-hoc (quarterly, weekly, daily), Schedule nightly using a script 




## Instructions

### General Help
[New to Github? Get started here.](http://htmlpreview.github.com/?https://github.com/Esri/esri.github.com/blob/master/help/esri-getting-to-know-github.html)

## Requirements

* For editing and customizing the scripts - Notepad or a Python Editor
* Basic understanding of GeoProcessing with ArcGIS
* ArcGIS Desktop 10.2
 
## Resources

This script leverages the [agol-helper](https://github.com/Esri/agol-helper) python package to move information to and from hosted services


## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.


## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2014 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's
[LICENSE.txt](https://github.com/Esri/community-parcels-python/blob/master/License.txt) file.

[](Esri Tags: LocalGovernment CommunityParcels AGOL Python ArcGIS-Online)
[](Esri Language: Python)
