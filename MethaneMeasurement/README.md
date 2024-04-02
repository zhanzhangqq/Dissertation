# Methane Measurement Study

This repository contains the code and scripts for the methane measurement study: S2Download.java and MBPD.py. The former Java script is for dowloading Sentinel-2 satellite imagery from Google Earth Engine. The latter Python script is for methane retrieval from Sentinel-2 satellite data and subsequent calculation of emission rates based on the retrieved concentration enhancements. The retrieval process involves multi-band-single-pass (MBSP) and multi-band-multi-pass-multi-comparison-date (MBPD) methods. The MBSP method is under license of GHGSAT Inc. More information of this study can be found in the following publication: https://doi.org/10.5194/amt-15-7155-2022.

## S2Download.java

### Description

The `S2Download.java` is a Java script for downloading Sentinel-2 satellite imagery from Google Earth Engine.

### Usage

Run the codes in Google Earth Engine to download imagery.


## MBPD.py

### Description

The `MBPD.py` is a Python script for the multi-band-multi-pass-multi-comparison-date (MBPD) methane retrieval and quantification algorithm from Sentinel-2 imagery. It does methane retrieval and calculates emission rates based on the retrieved concentration enhancements.

### Prerequisites

- Python 3
- NumPy
- Pandas
- Matplotlib
- SciPy
- PIL

The MBSP method is from Varon et al. (2021):

Varon et al. (2021) Atmos. Meas. Tech., 14, 2771–2785, 2021

https://doi.org/10.5194/amt-14-2771-2021

This method is under license of GHGSAT Inc.


### Usage

1. Clone the repository:

```bash
git clone https://github.com/zhanzhangqq/Dissertation.git
cd MethaneMeasurement
```

2. Modify the script as needed, adjusting file paths and parameters.

3. Run the script:

```bash
python MBPD.py
```

### Functionality

#### Methane Retrieval (MBSP)

The `gridretrieval_MBSP` function retrieves methane concentration enhancements based on Sentinel-2 reflectance data. The results are visualized.

#### Plume Mask Generation

The `generateMasks` function generates binary plume masks based on the retrieved concentration enhancements. The `qvalue` parameter controls the threshold during mask generation.

#### Normalization

The `NormalizeObservation` function performs extreme value removal and normalization to the retrieved concentration enhancements.

#### Methane Retrieval (MBPD)

The `MBPDRetrieval` function implements multi-band-multi-pass-multi-comparison-date (MBPD) retrieval. It visualizes the subtraction results and generates plume masks.

#### Emission Rate Calculation

The `EmissionRate` function calculates the emission source rate (kg/s) based on retrieved concentration enhancements, wind speed, and plume characteristics.

## Citation
Please cite the following reference if you find this project useful for your research or work:

Zhang, Z., Sherwin, E. D., Varon, D. J., & Brandt, A. R. (2022). Detecting and quantifying methane emissions from oil and gas production: algorithm development with ground-truth calibration based on Sentinel-2 satellite imagery. Atmospheric Measurement Techniques, 15(23): 7155-7169.

```bibtex
@article{Zhang2022Detecting,
author = {Zhang, Z. and Sherwin, E. D. and Varon, D. J. and Brandt, A. R.},
title = {Detecting and quantifying methane emissions from oil and gas production: algorithm development with ground-truth calibration based on {Sentinel-2} satellite imagery},
journal = {Atmospheric Measurement Techniques},
volume = {15},
number = {23},
pages = {7155--7169},
year = {2022},
doi = {10.5194/amt-15-7155-2022},
url = {https://amt.copernicus.org/articles/15/7155/2022/}
}
```
