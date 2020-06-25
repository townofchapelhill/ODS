# building-permit-automation
## Scripts to automate and enhance the LAMA query dataset for building permits

### Purpose
Create a workflow to add 2d geographic data to the permits file 

### Methodology 
The permits.csv file is created by a LAMA query multiple times per hour. The file is uploaded directly to the ODS FTP site. This file does not include a 2d geographic coordinate for mapping.

The Address file is created by an ODS call to the Town ArcGIS system to generate a list of all addresses within town limits. This file is downloaded from the chapelhillopendata.org site to a work area for intermediate processing.

The Powershell script ```download_csv.ps1``` downloads the address file from ODS to use as the input to the PIN lookup table.

The Powershell script ```address_to_PIN_lookup.ps1``` de-duplicates PIN entries and creates the ```PIN_lookup_sorted.csv``` file.

```open_data_ftp_download``` retrieves the current ```permits.csv``` file for input.

```update_permits``` creates the new ```building_permits.csv``` file, which is processed by ODS for the Building Permits dataset.

### Data Sources
#### ODS - [Addresses](https://www.chapelhillopendata.org/explore/dataset/addresses) file

#### ODS FTP site - permits.csv file

### Outputs
#### staging directory - building_permits.csv


### Transformations
#### address.csv to pin_lookup_sorted.csv
#### permits.csv to building_permits.csv

### Constraints