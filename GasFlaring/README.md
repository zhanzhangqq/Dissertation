# Gas Flairng Study

## Overview

This repository contains the code and scripts for the gas flaring study: Well2Field.py and FlareMatch.py. These scripts are designed to perform geospatial analysis on field and flare datasets, providing insights into the relationships between wells and fields and allocating flare volumes associated with specific fields.

## Well2Field.py

### Description

The `Well2Field.py` script focuses on the spatial conversion from wells to fields. It performs operations such as loading well data, converting it to a GeoDataFrame, generating well buffers, and dissolving well buffers based on the associated field.

### Prerequisites

- Python 3.x
- Pandas
- Geopandas
- Fiona
- Shapely
- Pyproj
- Rtree
- Contextily

### Usage

1. Clone the repository:

```bash
git clone https://github.com/zhanzhangqq/Dissertation.git
cd GasFlaring
```

2. Modify the script as needed, adjusting file paths and parameters.

3. Run the script:

```bash
python Well2Field.py
```

4. View the results in the console or further analyze the generated GeoDataFrames.


## FlareMatch.py

### Description

The `FlareMatch.py` script focuses on matching flares to specific geographic fields. It loads flare data, allocates flare volumes of the flares within fields to the fields, generates field buffers, and allocates flare volumes of the flares within field buffers to the fields.

### Prerequisites

- Python 3.x
- Pandas
- Geopandas
- Fiona
- Shapely
- Pyproj
- Rtree
- Contextily

### Usage

1. Clone the repository:

```bash
git clone https://github.com/zhanzhangqq/Dissertation.git
cd GasFlaring
```

2. Modify the script as needed, adjusting file paths and parameters.

3. Run the script:

```bash
python FlareMatch.py
```

4. View the results in the console or further analyze the generated GeoDataFrames.
