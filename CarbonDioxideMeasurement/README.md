# Carbon Dioxide Measurement Study

This repository contains the code for the carbon dioxide measurement study. The FetchRadius.py script is for determining the fetch radius of the carbon dioxide plume based on the parameter $\Delta IME$, which represents the additional mass enhancement as the radius expands a differential amount from $r_{j-1}$ to $r_{j}$.  The fetch radius $r_{c}$ is defined as the radius where $\Delta IME$ reaches its minimum value. More information of this study can be found in the following publication: https://doi.org/10.1029/2023GL105755.

## Description

The inputs of this function include:

- $imevals$: the additional mass enhancement along the expansion of radius ($\Delta IME$)
- $minfetch$: the radius value where radius starts to expand ($r_{s}$)
- $maxfetch$: the radius value where radius stops expanding
- $ps$: pixel resolution, which is defined as the incremental radius ($\Delta r$)

## Citation

Please cite the following publication if you find this project useful for your research or work:

Zhang, Z., Cusworth, D. H., Ayasse, A. K., Sherwin, E. D., & Brandt, A. R. (2023). Measuring carbon dioxide emissions from liquefied natural gas (LNG) terminals with imaging spectroscopy. Geophysical Research Letters, 50, e2023GL105755.

```bibtex
@article{Zhang2023Measuring,
author = {Zhang, Zhan and Cusworth, Daniel H. and Ayasse, Alana K. and Sherwin, Evan D. and Brandt, Adam R.},
title = {Measuring Carbon Dioxide Emissions From Liquefied Natural Gas (LNG) Terminals With Imaging Spectroscopy},
journal = {Geophysical Research Letters},
volume = {50},
number = {23},
pages = {e2023GL105755},
year = {2023},
doi = {https://doi.org/10.1029/2023GL105755},
url = {https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2023GL105755}
}
```
