# Import necessary libraries
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import ttest_ind, ttest_ind_from_stats
import matplotlib.pyplot as plt
import time
import os

# Sentinel-2 methane retrieval code from Varon et al. (2021)
import setup
import radtran as rt

# Change directory accordingly
root_path = '/S2Imagery/'


def gridretrieval_MBSP(d):
    # Load reflectance data 
    arr  = np.loadtxt(root_path + '/' + d + '/ref1_data_wB12.txt')
    arr2 = np.loadtxt(root_path + '/' + d + '/ref1_data_wB11.txt')
    
    arr[arr == np.nan] = 0
    arr2[arr2 == np.nan] = 0
    [nrow, ncol] = arr.shape
    for i in range(nrow):
        for j in range(ncol):
            if arr[i,j] == 0 or arr2[i,j] == 0:
                arr[i,j]  = 0
                arr2[i,j] = 0
            elif arr[i,j] == 1 or arr2[i,j] == 1:
                arr[i,j]  = 1
                arr2[i,j] = 1
    
    plt.imshow(arr, cmap='gray')
    plt.colorbar(label='reflectance')
    plt.show()

    plt.imshow(arr2, cmap='gray')
    plt.colorbar(label='reflectance')
    plt.show()
    
    # Calculate fractional change of reflectance $\delta$R
    x = arr.flatten()
    x = x[:, np.newaxis]
    y = arr2.flatten()
    c = np.linalg.lstsq(x, y, rcond=None)[0]
    frac_refl_data = (c*arr - arr2)/arr2
    
    # Column retrieval (mol/m^2)
    num_layers = 100
    targheight = 0
    obsheight = 100
    solarangle = 40
    obsangle = 0
    instrument = 'S2A'
    method = 'MBSP'
    retrieval = rt.retrieve(frac_refl_data, instrument, method, targheight, obsheight, solarangle, obsangle, num_layers=num_layers)

    # Export methane column enhancement $\delta$$\Omega$ (kg/m^2)
    retrievalmass = retrieval*0.016
    retrievalmass[np.isnan(retrievalmass)] = 0    # Nan value to 0
    
    plt.figure(figsize = (5,5))
    plt.imshow(retrievalmass, vmin=0, vmax=0.05)
    plt.colorbar(label='$\delta$$\Omega$ (kg/m2)')
    plt.title("Plume observation (" + d + ")")
    plt.show()

    return retrievalmass

def generateMasks(retrievalmass, qvalue):
    width = 3                # Set grid width
    hfwidth = (width-1)//2

    studyarea = retrievalmass
    q = np.nanquantile(studyarea, qvalue)

    [nrow, ncol] = studyarea.shape
    select = np.zeros((nrow, ncol))

    for i in range(nrow-width+1):
        for j in range(ncol-width+1):
            substudyarea = studyarea[i:i+width, j:j+width]
            m = np.nanmean(substudyarea)
            if m > q:
                select[i+hfwidth, j+hfwidth] = 1
    
    # Filtering to clean random errors
    # Median filtering
    width = 3               # Set grid width
    hfwidth = (width-1)//2

    for i in range(nrow-width+1):
        for j in range(ncol-width+1):
            subselect = select[i:i+width, j:j+width]
            median = np.median(subselect)
            select[i+hfwidth, j+hfwidth] = median

    # Gaussian filtering
    width = 5                # Set grid width
    hfwidth = (width-1)//2

    gaussian = np.array([[1,4,7,4,1], [4,16,26,16,4], [7,26,41,26,7], [4,16,26,16,4], [1,4,7,4,1]])
    gaussian = gaussian * 1/100

    # Add padding to inputs to keep output dimensions consistent with input
    pad = (width-1)//2
    select = np.pad(select, ((pad,pad), (pad,pad)), mode='constant', constant_values = (0,0))

    output = np.zeros((nrow, ncol))

    for i in range(nrow):
        for j in range(ncol):
            subselect = select[i:i+width, j:j+width]
            s = np.multiply(subselect, gaussian)
            output[i,j] = np.sum(s)

    [nrow_o, ncol_o] = output.shape

    th = 2.5
    output = np.where(output > th, 1, 0)
    mask = output
    return mask

def NormalizeObservation(d, maxthd):
    retrievalmass = gridretrieval_MBSP(d)
    retrievalmass = retrievalmass[25:55, 25:55]
    retrievalmass[np.isnan(retrievalmass)] = 0
    
    # Remove extreme values with lower bound 0 and upper bound maxthd
    retrievalmass[retrievalmass > maxthd] = maxthd
    retrievalmass[retrievalmass < 0] = 0
    
    # Normalize
    norm = np.linalg.norm(retrievalmass)
    retrievalmass = retrievalmass/norm
    
    # Remove extremes again
    retrievalmass[retrievalmass > maxthd] = maxthd
    retrievalmass[retrievalmass < 0] = 0
    
    return retrievalmass

def MBPDRetrieval(ind, n_cds, maxthd, q, totallist):
    # Target Date
    d2 = totallist[ind]
    retrievalmass_td = NormalizeObservation(d2, maxthd)
    
    # Comparison dates
    [nrow, ncol] = retrievalmass_td.shape
    former = np.zeros((nrow, ncol))
    comlist = totallist[ind-n_cds:ind]    # Comparison dates: continuous n_cds dates
    for j in range(n_cds):
        d1 = comlist[j]
        retrievalmass_cd = NormalizeObservation(d1, maxthd)
        former += retrievalmass_cd
    former = former/n_cds
    
    # Export and show MBMP subtraction results
    diff = retrievalmass_td - former    
    plt.imshow(diff, cmap='viridis', vmin=0, vmax=0.05)
    plt.title('MBPD plume observation ('+ d2 + ')')
    plt.colorbar()
    plt.show()
    
    # Export and show plume mask
    retrievalmask = generateMasks(diff, q)
    plt.imshow(retrievalmask, cmap='viridis', vmin=0, vmax=1)
    plt.title('MBPD plume mask ('+ d2 + ')')
    plt.colorbar()
    plt.show()
    
    return retrievalmask

def EmissionRate(ind, n_cds, maxthd, q, totallist, windlist):
    # Target Date
    d2 = totallist[ind]
    retrievalmass_td = gridretrieval_MBSP(d2)
  
    # Comparison date
    [nrow, ncol] = retrievalmass_td.shape
    former = np.zeros((nrow, ncol))
    comlist = totallist[ind-n_cds:ind]
    for j in range(n_cds):
        d1 = comlist[j]
        retrievalmass_cd = gridretrieval_MBSP(d1)
        former += retrievalmass_cd
    former = former/n_cds
    
    # MBMP subtraction
    diff = retrievalmass_td - former
    diff[diff < 0] = 0
    
    # Generate plume mask by MBPD retrieval
    retrievalmask = MBPDRetrieval_test(ind, n_cds, maxthd, q, totallist)
    
    # Calculate emission source rate (kg/s) by IME
    wind10 = windlist[ind]
    wind = 0.33*wind10 + 0.45
    totalmass = 0    # unit: kg/m2, with each grid 20*20 m2
    count = 0        # total counts of grids with plume
    for j in range(nrow):
        for k in range(ncol):
            if retrievalmask[j, k] == 1:
                totalmass += diff[j, k]
                count += 1

    length = np.sqrt(count*400)        # plume length scale: sqrt of plume area (m)
    rate = 0
    if length == 0:
        rate = 0
    else:
        rate = totalmass*wind*400/length   # unit: kg/s
    return rate

def main():
    
    totallist = ["date1", "date2", "date3"]  # Replace with actual date list
    windlist = [10, 15, 20]  # Replace with actual wind speed list
    n_cds = 3
    maxthd = 0.01
    q = 0.9

    retrievalmask = MBPDRetrieval(ind, n_cds, maxthd, q, totallist)
    rate = EmissionRate(ind, n_cds, maxthd, q, totallist, windlist)
    print(f"Emission rate for {totallist[ind]}: {rate} kg/s")

if __name__ == "__main__":
    main()

