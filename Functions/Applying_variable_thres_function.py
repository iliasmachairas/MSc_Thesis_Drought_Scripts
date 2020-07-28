#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import numpy as np
import pandas as pd

def df_droughts_var_T(df,column,threshold,column2, removed_period):  #variable threshold
    #The function loses 1 time step in case it starts with a drought
    # Removed_period arguement is just an integer number, not a string neither a pd.Timedelta
    """
    df: dataframe
    column: the column name (string) of the df which contains groundwater level information (e.g. 'GW')
    threshold: the threshold time series for identification of drought occurrence
    removed_duration: drought events whose duration is lower or equal than that are removed (the arguement type is integer expressing the time steps, e.g. for 2 days, it is 2)

    Outputs
    droughts: is a df with four columns: drought onset, drought end, drought maximum deviation from the threshold, and drought duration

    Prints:
    - Drought durations before removing minor droughts
    - Onset of drought events after removing minor droughts
    - End of drought events after removing minor droughts
    - Drought durations after removing minor droughts
    """
    # The steps are the same as the fixed trheshold approach  (the only difference is that T is a time series and not a fixed number)
    j_max=int(len(df)/2)

    # Initializing the array where drought deviation for all time steps for each drought event are stored
    # One filled-in row in G array contains the deficit of a drought event for its time steps
    G=np.zeros((j_max,df.shape[0]))
    k=0
    T=threshold
    onset=np.zeros(j_max)
    end=np.zeros(j_max)

    # loop in order to identify drought events for the whole time series
    for i in range(1,df.shape[0]-1):
        # for 1 time step drought event
        if (df[column][i]<T.iloc[i][column2]) & (df[column][i-1]>=T.iloc[i-1][column2]) & (df[column][i+1]>=T.iloc[i+1][column2]):
            start=i
            onset[k]=start
            end[k]=i
            G[k,i-start]=T.iloc[i][column2]-df[column][i]
            k+=1
        # onset of non 1 time step drought event
        elif (df[column][i]<T.iloc[i][column2]) & (df[column][i-1]>=T.iloc[i-1][column2]):
            start=i
            onset[k]=start
            G[k,i-start]=T.iloc[i][column2]-df[column][i]
        # end of non 1 time step drought event
        elif (df[column][i]<T.iloc[i][column2]) & (df[column][i+1]>=T.iloc[i+1][column2]):
            # start for 1-time step drought event which started before
            # the start of time series 
            if i==1:
                start=i      
            G[k,i-start]=T.iloc[i][column2]-df[column][i]
            end[k]=i
            k+=1
        # rest time steps of non 1 time step drought event
        elif (df[column][i]<T.iloc[i][column2]):
            if i==1:
                # when a time series starts with a drought event and its duration
                # is more than 1 time step
                start=1
                G[k,i-start]=T.iloc[i][column2]-df[column][i]
            elif i==df.shape[0]-2:
                # when a time series ends with a drought event
                G[k,i-start]=T.iloc[i][column2]-df[column][i]
                G[k,(i-start+1)]=T.iloc[i+1][column2]-df[column][(i+1)]
                end[k]=i+1
                k+=1
            else:
                # normal intermediate time step 
                G[k,i-start]=T.iloc[i][column2]-df[column][i]
    
    # Reducing the size of G array

    # Max of elements per row
    maxim_rows=np.max((G!=0).sum(axis=1))
    # Max of elements per column
    maxim_columns=np.max((G!=0).sum(axis=0))
    G_final=G[:k,:maxim_rows]

    # Estimating maximum deviation for each drought event
    maximum=np.zeros(k)
    for i in range(k):
        maximum[i]=np.max(G_final[i])

    # Estimating the duration for each drought event
    durations=(G_final!=0).sum(axis=1)
    print(durations)
    # Reducing the size of the arrays
    onset_clear=onset[:k]
    end_clear=end[:k]
    
    # Filtering out minor drought events
    # The drought events with duration less than removed_duration will be deleted
    durations_clear_2=durations[np.where(durations>removed_period)]
    onset_clear_2 = onset_clear[np.where(durations>removed_period)]
    end_clear_2=end_clear[np.where(durations>removed_period)]
    maximum_clear_2= maximum[np.where(durations>removed_period)]
    print('onset_clear_2:',onset_clear_2)
    print('end_clear_2:', end_clear_2)
    print('durations_clear_2',durations_clear_2)

    droughts=pd.DataFrame(index=np.arange(len(onset_clear_2)), data={'onset': onset_clear_2, 'end':end_clear_2, "duration":durations_clear_2, "maximum":maximum_clear_2})

    return droughts

