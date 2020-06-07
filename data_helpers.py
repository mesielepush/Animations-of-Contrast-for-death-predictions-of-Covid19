import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
from shutil import copy2

path = os.path.abspath(os.path.join(os.getcwd(),'projections'))

def get_files(country_name):
    if not os.path.exists(f'predictions/{country_name}'):
        os.makedirs(f'predictions/{country_name}')
    for root, _, files in os.walk(path):
        if root.endswith('global'):
            for file in files:
                if file.startswith(country_name):
                    if os.path.exists(f'predictions/{country_name}/{country_name}_{root[-17:-7]}.csv'):
                        continue
                    else:
                        copy2(os.path.join(root,file), f'predictions/{country_name}/{country_name}_{root[-17:-7]}.csv') 
                    
def clean_nan(array):
    if type(array) == list:
        array = np.asarray(array) 
    not_nan_array = ~ np.isnan(array)
    return array[not_nan_array]

def eliminate_negatives(df):
    for key in df.keys():
        try:
            df[key] = [x if x >0 else np.nan for x in df[key]]
        except:
            pass
    return df