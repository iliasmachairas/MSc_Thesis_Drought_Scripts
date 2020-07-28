#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def Moving_Window_daily(df, column, percentile, window):
    """
    df: dataframe
    column: the column name (string) of the df which contains groundwater level information (e.g. 'GW')
    percentile: the percentile for the calulation of trheshold [%]
    time window: the size of moving window in days; please give even numbers, otherwise it may not work

    Output
    df_perc: the Moving Window daily percentile threshold time series
    """
    dates=[]
    perc_table = np.zeros(df.shape[0]-window)
    half_window = int(window/2)
    
    for i in range(half_window,(df.shape[0]-half_window)):
        window_df = df.iloc[i - half_window : i + half_window].copy()
        dates.append(df.iloc[i].name)
        calc_perc = np.nanpercentile(window_df[column],percentile)
        perc_table[i-int(window/2)] = calc_perc
        
    df_perc = pd.DataFrame(index=dates, data = perc_table, columns=['thres'])
    return df_perc


# In[3]:


def Clip_GW_series_based_on_thres_func_d_MA(df_GW, df_thres):
    """Attention: Both dfs need to have as index timestamp"""
    start_thres = df_thres.iloc[0].name
    end_thres = df_thres.iloc[-1].name
    data_clipped = df_GW.loc[start_thres:end_thres].copy()
    return data_clipped

