import os
import pandas as pd
import numpy as np
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
                    
def get_cummulative(data_dir):
    data = pd.read_csv(data_dir, encoding='ANSI')
    cummulative = []
    raw = data.loc[data['nombre'] == 'Nacional']

    for i in raw.values[0][3:]:
        if len(cummulative) == 0:
            cummulative.append(i)
        else:
            cummulative.append(i+cummulative[-1])
    new_data = pd.DataFrame()
    new_data['dates'] = pd.to_datetime(raw.columns[3:],dayfirst=True)
    new_data['deaths']= np.array(cummulative)
    new_data.set_index('dates',drop=True)
    return new_data
def get_discrete(data_dir):
    data = pd.read_csv(data_dir, encoding='ANSI')
        
    new_data = pd.DataFrame()
    new_data['dates'] = pd.to_datetime(data.columns[3:],dayfirst=True)
    new_data['deaths']= data.loc[data['nombre'] == 'Nacional'].values[0][3:]
    new_data = new_data.set_index('dates',drop=True)
    
    return new_data

def process_plot(index, cummulative, discrete, pred):

    database = {
        'index':index,
        'cummulative': [],
        'discrete': [],
        'pred_cummulative_low':[],
        'pred_cummulative_mean':[],
        'pred_cummulative_upper':[],
        'pred_discrete_low': [],
        'pred_discrete_mean':[],
        'pred_discrete_upper':[],
    }
    
    for date in index:
        try:
            database['cummulative'].append(cummulative[cummulative['dates'] == date].deaths.values[0])
        except:
            database['cummulative'].append(np.nan)
        try:
            database['discrete'].append(discrete[discrete.index == date].deaths.values[0])
        except:
            database['discrete'].append(np.nan)
        try:
            database['pred_cummulative_low'].append(pred[pred.index == date].predicted_total_deaths_lower.values[0])
        except:
            database['pred_cummulative_low'].append(np.nan)
        try:
            database['pred_cummulative_mean'].append(pred[pred.index == date].predicted_total_deaths_mean.values[0])
        except:
            database['pred_cummulative_mean'].append(np.nan)
        try:
            database['pred_cummulative_upper'].append(pred[pred.index == date].predicted_total_deaths_upper.values[0])
        except:
            database['pred_cummulative_upper'].append(np.nan)
        try:
            database['pred_discrete_low'].append(pred[pred.index == date].predicted_deaths_lower.values[0])
        except:
            database['pred_discrete_low'].append(np.nan)
        try:
            database['pred_discrete_mean'].append(pred[pred.index == date].predicted_deaths_mean.values[0])
        except:
            database['pred_discrete_mean'].append(np.nan)
        try:
            database['pred_discrete_upper'].append(pred[pred.index == date].predicted_deaths_upper.values[0])
        except:
            database['pred_discrete_upper'].append(np.nan)
            
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)
    plt.rcParams['figure.constrained_layout.use'] = True
    
    plt.plot(database['index'],database['discrete'], label=f'real deaths {max(cummulative.deaths)}', linewidth=5, color = 'black')
    plt.plot(database['index'],database['pred_discrete_low'],   label = f'pred deaths: {database["pred_cummulative_low"][-1]}')
    plt.plot(database['index'],database['pred_discrete_mean'],  label = f'pred deaths: {database["pred_cummulative_mean"][-1]}')
    plt.plot(database['index'],database['pred_discrete_upper'], label = f'pred deaths: {database["pred_cummulative_upper"][-1]}')
    
    plt.fill_between(database['index'], database['pred_discrete_low'], database['pred_discrete_upper'], color='b', alpha=.1)
    
    plt.title(f' predicted deaths for September: {sum(database["pred_discrete_mean"]) }', fontsize=25,pad=20)
    plt.suptitle(f'{calendar.month_name[int(prediction[-9:-7])]}-{prediction[-6:-4]}', fontsize=20,ha='left',va='top')
    plt.ylabel('Deaths for Covid19')
    plt.legend(fontsize=20,loc='upper left')
    plt.xlabel(f'Real deaths: {max(cummulative.deaths)}', fontsize = 20)
    
    plt.savefig(f'imgs/{country_name}/discrete/{prediction[-9:-4]}.jpg')
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)
    plt.plot(database['index'],database['cummulative'], label=f'real deaths {max(cummulative.deaths)}', linewidth=5, color = 'black')
    plt.plot(database['index'],database['pred_cummulative_low'],   label = f'pred deaths: {database["pred_cummulative_low"][-1]}')
    plt.plot(database['index'],database['pred_cummulative_mean'],  label = f'pred deaths: {database["pred_cummulative_mean"][-1]}')
    plt.plot(database['index'],database['pred_cummulative_upper'], label = f'pred deaths: {database["pred_cummulative_upper"][-1]}')
    
    plt.fill_between(database['index'], database['pred_cummulative_low'], database['pred_cummulative_upper'], color='b', alpha=.1)
    
    plt.xlabel(f'Real deaths: {max(cummulative.deaths)}', fontsize = 20)
    plt.ylabel('Deaths for Covid19')
    plt.title(f' predicted deaths: {database["pred_cummulative_mean"][-1]}', fontsize=25,pad=20)
    plt.suptitle(f'{calendar.month_name[int(prediction[-9:-7])]}-{prediction[-6:-4]}', fontsize=20,ha='left', va='top')
    plt.legend(fontsize=16,loc='upper left')

    
    plt.savefig(f'imgs/{country_name}/cummulative/{prediction[-9:-4]}.jpg')

def get_animation(country_name):
    
    get_files(country_name)
        
    if not os.path.exists(f'imgs/{country_name}/cummulative'):
        os.makedirs(f'imgs/{country_name}/cummulative')
    if not os.path.exists(f'imgs/{country_name}/discrete'):
        os.makedirs(f'imgs/{country_name}/discrete')
    
    files_dir = os.listdir(f'predictions/{country_name}')
    
    oldest_file = min([pd.to_datetime(x[-14:-4]) for x in files_dir])
    newest_file = max([pd.to_datetime(x[-14:-4]) for x in files_dir])
    
    oldest_file= pd.read_csv(f'predictions/{country_name}/{country_name}_{str(oldest_file)[:10]}.csv')
    newest_file = pd.read_csv(f'predictions/{country_name}/{country_name}_{str(newest_file)[:10]}.csv')
        
    start_date = min(pd.to_datetime(oldest_file.date.copy()))
    end_date   = max(pd.to_datetime(newest_file.date.copy()))
    
    index = pd.date_range(start = start_date, end = end_date)
    
    cummulative = pd.DataFrame()
    cummulative['dates'] = pd.to_datetime(newest_file.date.copy())
    cummulative['deaths']= newest_file.total_deaths
    
    discrete = pd.DataFrame()
    discrete['dates'] = pd.to_datetime(newest_file.date.copy())
    discrete['deaths']= newest_file.actual_deaths
    
    for file in files_dir:
        process_plot(index, cummulative, discrete, pd.read_csv(f'predictions/{country_name}/{file}'))
    
    images = []
    for filename in os.listdir('imgs/cummulative'):
        images.append(imageio.imread(os.path.join('imgs/cummulative',filename)))
    
    imageio.mimsave('cummulative.mp4', images)

