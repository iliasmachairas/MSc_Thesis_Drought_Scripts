#!/usr/bin/env python
# coding: utf-8

# In[1]:


def pooling(df, col_start, col_end, col_max, col_dur, thres):
    """
    The following arguements are used:
    df: DataFrame, 
    col_start: df column contains the time step each drought event started
    col_end: df column contains the time step each drought event ended
    The start and end of droughts are measured from the same reference point (start of time series)
    col_max: df column represents the deficit (maximum deviation from the threshold) for each drought event
    col_dur: df column represents the duration of each drought event
    thres: the threshold value for pooling in days; droughts time difference (onset of drought i - end of drought i-1)
    lower or equal than the provided by the user are merged)      
    Attention: all the column names need to be provided as strings.

    Output
    droughts_merged: A df which contains: onset step, end step, deficit, and duration of each pooled drought event
    """
    import numpy as np
    import pandas as pd
    
    start = df[col_start].values
    end   = df[col_end].values
    max_dev = df[col_max].values
    duration = df[col_dur].values
    
    # Estimating the gap between events in time steps (days)
    dists = start[1:] - end[:-1]
    # Mask events to merge 
    m = dists > thres
    # First and last indices of each merged group
    first_indices = np.flatnonzero(np.r_[True, m])
    last_indices = np.r_[first_indices[1:], len(start)] - 1
    
    #Results
    merged_start    = start[first_indices]
    merged_end      = end[last_indices]
    merged_maximum = np.maximum.reduceat(max_dev, first_indices)
    merged_duration = np.add.reduceat(duration, first_indices)
    
    combined_ar = np.array([merged_start, merged_end, merged_maximum, merged_duration])
    combined_ar_T = combined_ar.T.copy()
    droughts_merged = pd.DataFrame(data=combined_ar_T, columns=['onset','end','deficit','duration'])
        
    return droughts_merged

