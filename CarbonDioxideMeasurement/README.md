# Carbon Dioxide Measurement Study

This repository contains the code for the carbon dioxide measurement study. The FetchRadius.py script is for determining the fetch radius of the carbon dioxide plume based on the parameter $\Delta IME$, which represents the additional mass enhancement as the radius expands a differential amount from $r_{j-1}$ to $r_{j}$.  The fetch radius $r_{c}$ is defined as the radius where $\Delta IME$ reaches its minimum value. 

### Description

The inputs of this function include:

- $imevals$: the additional mass enhancement along the expansion of radius ($\Delta IME$)
- $minfetch$: the radius value where radius starts to expand ($r_{s}$)
- $maxfetch$: the radius value where radius stops expanding
- $ps$: pixel resolution, which is defined as the incremental radius ($\Delta r$)
