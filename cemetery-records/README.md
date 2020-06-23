# Burial Records
## Burial Records Aggregator

### Goal 
Scrape the Town of Chapel Hill burial records pages to create a single dataset
### Purpose 

Provide a single source for all town public cemetery burial data
### Methodology 
html scraping

### Data Source
[Town of Chapel Hill Cemeteries](https://www.townofchapelhill.org/town-hall/departments-services/parks-recreation/cemeteries)
### Output 
cemetery_data.csv

### Transformations
Select Last Name, First Name, Year Deceased, Section, Lot

### Constraints
Users the lxml library via ```pip install lxml```
