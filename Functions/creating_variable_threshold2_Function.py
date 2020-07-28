#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime


# In[2]:


def Plotting_Var_Thres(df1, col1, df_thres, col2):
    import plotly.graph_objects as go

    xx1=go.Scatter(x=df1.index, y=df1[col1], name='timeseries')
    xx2=go.Scatter(x=df_thres.index, y=df_thres[col2], name='threshold')

    fig=go.Figure([xx1, xx2])
    fig.show()


# In[3]:

def creating_variable_threshold2(df, column, percentile):
    """
    df: dataframe
    column: the column name (string) of the df which contains groundwater level information (e.g. 'GW')
    percentile: the percentile for the calulation of trheshold [%]

    Output:
    sel_thres: the initial monthly variable threshold without applying moving average
    perntl_months_df_MA: monthly variable threshold after applying moving average
    The moving average has a span of 20 days
    """
   
    df['month']=df.index.month
    start=df.iloc[0].name.year
    end = df.iloc[-1].name.year
    # dif_years= int(pd.Timedelta(end - start)/pd.Timedelta('365 days'))
    
    # Creating an array where each row contains all values took place in a specific month
    monthly_val = [[] for i in range(12)]
    
    month_ar=[]
    for i in range(12):
        monthly_val[i].append(df[df.month==(i+1)][column].values)
          
    for i in range(12):
        month_ar.append(list(monthly_val[i][0]))

    # Converting the 0 values to np.Nan    
    maxl = max(map(len, month_ar))
    month_ar_2=np.asarray([i + [np.NaN]*(maxl-len(i)) for i in month_ar], dtype='float')
             
    # Convering the array to df
    import calendar
    month_names=list(calendar.month_name) # Attention the 0_index includes a zero value
    monthly_val_df = pd.DataFrame(index=month_names[1:], data=month_ar_2)
       
    # Finding the percentiles
    perntl_months=np.zeros(12)
    for i in range(12):
        perntl_months[i] = np.nanpercentile(monthly_val_df.loc[calendar.month_name[(i+1)],:], percentile)

    # Creating a df where monthly percentiles of one year are repeated (daily scale)
    # perntl_months is repeated in ts_thres for 11 years which is more than what we need
    # It is clipped subsequently based on the input groundwater level data
    ranges=pd.date_range(start='01-01-2010', end='01-01-2021', freq='D')
    
    ts_thres= np.zeros(len(ranges))
    for i in range(len(ranges)):
        for j in range(12):
            if ranges[i].month == (j+1):
                ts_thres[i]=perntl_months[j]
    
    ts_thres_df= pd.DataFrame(index=ranges, data=ts_thres, columns=['thres'])
    
    d1=df.iloc[0].name #first day of input data
    d2=df.iloc[-1].name #last day of input data

    # selecting timeseries of monthly variable threshold based on input data (daily time_step)
    sel_thres= ts_thres_df.loc[(ts_thres_df.index>=pd.Timestamp(d1).tz_localize(None)) & (ts_thres_df.index<=pd.Timestamp(d2).tz_localize(None))].copy()
    
    # Applying moving average
    threshold_daily_df_rol = sel_thres.thres.rolling(20).mean()
    threshold_daily_df_rol.dropna(inplace=True)
    perntl_months_df_MA=pd.DataFrame()
    perntl_months_df_MA['thres']= threshold_daily_df_rol
    
    # plotting
    Plotting_Var_Thres(df, column, perntl_months_df_MA, 'thres')
    
    return sel_thres, perntl_months_df_MA


# In[ ]:




