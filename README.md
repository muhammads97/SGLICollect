<h3 align="center">SGLICollect</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](/COPYING.txt)

</div>

---

<p align="center"> SGLICollect is an open-source software for searching, downloading and reading SGLI/GCOM-C products from both GPORTAL and JASMES. 
    <br> 
    Acknowledgment: This project was developed as part of my master's degree at Kyoto University of Advanced Science, under the Remote Sensing Laboratory. 
    <br> 
    This project is built for research purposes to collect and extract data.
    <br> 
    The research contributes towards my master's degree, under the supervision of Professor Salem Ibrahim Salem.
    <br> 
</p>

## Installation

This section explains how to download and set up SGLICollect for various environments (The GUI version of SGLICollect is currently under construction)

### Stand-alone installation (Linux and MacOS only)

1. Download the bash installer:
`curl -L -o SGLICollect_installer.sh https://raw.githubusercontent.com/muhammads97/SGLICollect/main/installer.sh`

2. Run the installer:
`sh SGLICollect_installer.sh`

3. Add SGLICollect to the system path

Now you can use SGLICollect as follows:
`SGLICollect --version`

### Conda python installation

To use SGLICollect inside a conda environment please follow the instructions in this section

1. Clone this repo:
`git clone https://github.com/muhammads97/SGLICollect.git`
2. Install the conda environment:
`conda env create -f environment.yml`
3. Activate the conda environment:
`conda activate SGLICollect`
4. Validate installation:
`python <path to SGLICollect> --version`

## Usage

The SGLICollect can be used in two modes:
1. Single-entry processing
2. Bulk processing using CSV

The services provided in each mode are as follows:
1. Search (using latitude, longitude, and date)
2. Download (using product URL)
3. Extract (using product directory, latitude, and longitude)

All the parameters for these services are set using the `config.json` file

To run the SGLICollect, set the parameters needed in `config.json` and run:
for the stand-alone version:
`SGLICollect -c <path to config.json>`
for the conda python installation:
`python <path to SGLICollect> -c <path to config.json>`

Configuration options:
1. `operations`: an array of the operations that will be performed, the available options are: `search`, `download`, and `extract`.
2. `args`: an object containing the arguments to be used for these operations:
    - `product`      : satellite product, please refer to the [list of products](#list-of-products).
    - `latitude`     : used for a single-entry mode.
    - `longitude`    : used for a single-entry mode.
    - `date`         : used for a single-entry mode.
    - `csv`          : a path to a CSV file for bulk processing mode. (This will override the parameters provided for single-entry mode), refer to [CSV file format](#csv-file-format).
    - `api`          : `GPORTAL` or `JASMES` (Default: `GPORTAL`).
    - `download_dir` : Download directory (for both single-entry and bulk-processing). If not provided, the files will be downloaded in the temp directory and they will be deleted once the processing ends.
    - `cred`         : path to JSON file containing account and password (refer to [Credentials file](#credentials-file)).
    - `product_dir`  : directory of all products used for the extraction step for bulk-processing mode.
    - `product_path` : path for a single product to extract from, used in the single-entry mode.
    - `no_repeat`    : `true` or `false`. Used for search and download, if the entry already exists in the CSV or the file is already downloaded the operation will be skipped. (default: false)


### List of products

#### GPortal
1. `L1B`: Level 1 B SGLI product from GPortal.
2. `L2P`: Level 2 Water Quality Products from GPortal.
3. `L2R`: Level 2 Remote Sensing Reflectance from GPortal.

#### JASMES
1. `NWLR_380`: Water leaving radiance at 380 nm.
2. `NWLR_412`: Water leaving radiance at 412 nm.
3. `NWLR_443`: Water leaving radiance at 443 nm.
4. `NWLR_490`: Water leaving radiance at 490 nm.
5. `NWLR_530`: Water leaving radiance at 530 nm.
6. `NWLR_565`: Water leaving radiance at 565 nm.
7. `NWLR_670`: Water leaving radiance at 670 nm.
8. `CDOM`   : Colored Dissolved Organic Matter.               
9. `CHLA`   : Chlorophyll-a concentration.          
10. `TSM`    : Total Suspended Matter.         
11. `SST`    : Sea Surface Temperature.          

### Credentials file

a Json file containing `account` and `password` for GPortal or JASMES
Example:
```
{
    "account": "username",
    "password": "password"
}
```

### CSV file format

#### For Search:

1. date
2. lat
3. lon

##### Search output:

1. Output columns for GPORTAL:
    - identifier
    - file_status
    - resolution
    - download_url
    - preview_url
    - cloud_coverage (%)
2. Output columns for JASMES:
    - ftp_path
    - file_name
    - file_size
    - box_id

#### For Download:

1. download_url (GPortal)/ftp_path (JASMES)

##### Download output:

No updates to the CSV, the files will be downloaded either in the specified download_dir or in the temp folder.

#### For Extract:

1. identifier (GPortal)/ file_name (JASMES)
2. lat
3. lon

##### Extract output (GPORTAL):

1. L1B:
    - Rt11: Reflectance at band 11  
    - Rt10: Reflectance at band 10  
    - Rt09: Reflectance at band 09  
    - Rt08: Reflectance at band 08  
    - Rt07: Reflectance at band 07  
    - Rt06: Reflectance at band 06  
    - Rt05: Reflectance at band 05  
    - Rt04: Reflectance at band 04  
    - Rt03: Reflectance at band 03  
    - Rt02: Reflectance at band 02   
    - Rt01: Reflectance at band 01
    - Lt11: Radiance at band 11
    - Lt10: Radiance at band 10
    - Lt09: Radiance at band 09
    - Lt08: Radiance at band 08
    - Lt07: Radiance at band 07
    - Lt06: Radiance at band 06
    - Lt05: Radiance at band 05
    - Lt04: Radiance at band 04
    - Lt03: Radiance at band 03
    - Lt02: Radiance at band 02
    - Lt01: Radiance at band 01
    - land: percentage of land in the pixel
2. L2R:
    - Rrs_670: Remote sensing reflectance at wavelength 670 nm
    - Rrs_565: Remote sensing reflectance at wavelength 565 nm
    - Rrs_530: Remote sensing reflectance at wavelength 530 nm
    - Rrs_490: Remote sensing reflectance at wavelength 490 nm
    - Rrs_443: Remote sensing reflectance at wavelength 443 nm
    - Rrs_412: Remote sensing reflectance at wavelength 412 nm
    - Rrs_380: Remote sensing reflectance at wavelength 380 nm
3. L2P:
    - Chla      : Chlorophyll-a concentration using JAXA's Standard Chla Algorithm for GPortal (mg/m3)
    - aCDOM_412 : absorption of Colored Dissolved Organic Matter at wavelength 412 nm (1/m)
    - TSM       : Total Suspended Matter (g/m3)


##### Extract output (JASMES):

The output column is the same as the product name.

### Example usage (single-entry)

`config.json` :
```
{
  "operations": ["search", "download", "extract"],
  "args": {
    "product": "L2R",
    "latitude": 44.853750035714505,
    "longitude": 138.32875040812206,
    "date": "2023/11/21",
    "download_dir": "~/Downloads/",
    "api": "GPORTAL",
    "cred": "./cred.json"
  }
}
```
Note: in this example, product_path doesn't need to be set because after the download finishes the product_path will be calculated automatically.

### Example usage (bulk-processing)

`config.json` :
```
{
  "operations": ["search", "download", "extract"],
  "args": {
    "product": "L2R",
    "csv": "./test.csv"
    "no_repeat": true,
    "download_dir": "~/Downloads/",
    "product_dir": "~/Downloads/",
    "api": "GPORTAL",
    "cred": "./cred.json"
  }
}
```