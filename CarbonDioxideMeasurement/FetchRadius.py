import numpy as np

def FetchRadius(imevals, minfetch, maxfetch, ps):
    rad_min = int(np.ceil(minfetch/ps))
    rad_max = int(np.ceil(maxfetch/ps))
    
    # Smooth imevals by taking the average of three adjacent values
    fm_min_ps = rad_min
    imevals_sm = np.zeros(len(imevals[fm_min_ps - 1 : len(imevals) - fm_min_ps]))
    imevals_sm[0] = imevals[fm_min_ps - 1]
    imevals_sm[-1] = imevals[len(imevals) - fm_min_ps - 1]
    for i in range(1, len(imevals_sm) - 1):
        imevals_sm[i] = (imevals[fm_min_ps + i - 2] + imevals[fm_min_ps + i - 1] + imevals[fm_min_ps + i])/3
    
    # Find the fetch radius at which the min imevals is achieved
    ime_minval = min(imevals_sm)
    ime_minind = np.where(imevals_sm == ime_minval)[0][0] + fm_min_ps - 1
    fetch_radius_output = ps * ime_minind + minfetch
    print('fetch radius output: ' + str(fetch_radius_output))

    return fetch_radius_output

