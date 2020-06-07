import os
import sys
import calendar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
from dateutil.parser import parse
from shutil import copy2

path = os.path.abspath(os.path.join(os.getcwd(),'projections'))

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

def is_date(string, fuzzy=False):
    
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def get_files(country_name):
    if not os.path.exists(f'predictions/{country_name.lower()}'):
        os.makedirs(f'predictions/{country_name.lower()}')

    if country_name.lower() in ['us','usa']:
        for i in os.listdir('projections'):
            if is_date(i):
                if os.path.exists(f'predictions/us/us_{i}.csv'):
                    continue
                else:
                    if 'predicted_total_deaths_mean' not in pd.read_csv(f'projections/{i}/US.csv').keys():
                        continue
                    else:
                        copy2(f'projections/{i}/US.csv', f'predictions/us/us_{i}.csv')
    else:
        for root, _, files in os.walk(path):
            if root.endswith('global'):
                for file in files:
                    if file.startswith(country_name):
                        if os.path.exists(f'predictions/{country_name.lower()}/{country_name.lower()}_{root[-17:-7]}.csv'):
                            continue
                        else:
                            copy2(os.path.join(root,file), f'predictions/{country_name.lower()}/{country_name.lower()}_{root[-17:-7]}.csv')

def plot_discrete(index, database, max_deaths, prediction, country_name):
    # discrete data changes the y limit often and that messes up the legend
    # so this (lim_data and max_y) are here to give some space on the top
    lim_data = max( clean_nan(database['discrete']) ) + ( max( clean_nan(database['discrete']))/ 2 )
    max_y = max(clean_nan(database['pred_discrete_upper'])) + max(clean_nan(database['pred_discrete_upper']))/2
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (14,6)
    plt.rcParams['figure.constrained_layout.use'] = True
    
    plt.plot(index, database['discrete'], label=f'real deaths {max_deaths}', linewidth=5, color = 'black')
    plt.plot(index, database['pred_discrete_low'],   label = f'pred deaths: {clean_nan(database["pred_cummulative_low"]  ) [-1]}')
    plt.plot(index, database['pred_discrete_mean'],  label = f'pred deaths: {clean_nan(database["pred_cummulative_mean"] ) [-1]}')
    plt.plot(index, database['pred_discrete_upper'], label = f'pred deaths: {clean_nan(database["pred_cummulative_upper"]) [-1]}')
    
    plt.fill_between(index, database['pred_discrete_low'], database['pred_discrete_upper'], color='b', alpha=.1)
    
    plt.title(f' predicted deaths for September: {sum(clean_nan(database["pred_discrete_mean"])) }', fontsize=25,pad=20)
    plt.suptitle(f'{country_name.upper()}_{calendar.month_name[int(prediction[-9:-7])]}-{prediction[-6:-4]}', fontsize=20,ha='left',va='top')
    plt.ylabel('Deaths for Covid19')
    plt.ylim(0, max(max_y,lim_data))
    plt.legend(fontsize=20,loc=0)
    plt.xlabel(f'Real deaths: {max_deaths}', fontsize = 20)
    
    plt.savefig(f'plots/{country_name}/discrete/{prediction[-14:-4]}.jpg')
    
def plot_cummulative(index, database, max_deaths, prediction, country_name):
    
    plt.close('all')
    plt.rcParams["figure.figsize"] = (15,6)
    
    plt.plot(index, database['cummulative'], label=f'real deaths {max_deaths}', linewidth=5, color = 'black')
    plt.plot(index, database['pred_cummulative_low'],   label = f'pred deaths: {clean_nan(database["pred_cummulative_low"]  ) [-1]}')
    plt.plot(index, database['pred_cummulative_mean'],  label = f'pred deaths: {clean_nan(database["pred_cummulative_mean"] ) [-1]}')
    plt.plot(index, database['pred_cummulative_upper'], label = f'pred deaths: {clean_nan(database["pred_cummulative_upper"]) [-1]}')
    
    plt.fill_between(index, database['pred_cummulative_low'], database['pred_cummulative_upper'], color='b', alpha=.1)
    
    plt.xlabel(f'Real deaths: {max_deaths}', fontsize = 20)
    plt.ylabel('Deaths for Covid19')
    plt.title(f' deaths for September: {max(clean_nan(database["pred_cummulative_mean"]))}', fontsize=25,pad=20)
    plt.suptitle(f'{country_name.upper()}_{calendar.month_name[int(prediction[-9:-7])]}-{prediction[-6:-4]}', fontsize=20,ha='left', va='top')
    plt.legend(fontsize=16,loc='upper left')

    
    plt.savefig(f'plots/{country_name}/cummulative/{prediction[-14:-4]}.jpg')

def process_data(index, cummulative, discrete, prediction, country_name):
    
    pred = pd.read_csv(f'predictions/{country_name}/{prediction}')
    pred['date'] = pd.to_datetime(pred.date)
    
    database = {
        
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
            database['cummulative'].append(cummulative[cummulative.date == date].deaths.values[0])
        except:
            database['cummulative'].append(np.nan)
        try:
            database['discrete'].append(discrete[discrete.date == date].deaths.values[0])
        except:
            database['discrete'].append(np.nan)
        try:
            database['pred_cummulative_low'].append(pred[pred.date == date].predicted_total_deaths_lower.values[0])
        except:
            database['pred_cummulative_low'].append(np.nan)
        try:
            database['pred_cummulative_mean'].append(pred[pred.date == date].predicted_total_deaths_mean.values[0])
        except:
            database['pred_cummulative_mean'].append(np.nan)
        try:
            database['pred_cummulative_upper'].append(pred[pred.date == date].predicted_total_deaths_upper.values[0])
        except:
            database['pred_cummulative_upper'].append(np.nan)
        try:
            database['pred_discrete_low'].append(pred[pred.date == date].predicted_deaths_lower.values[0])
        except:
            database['pred_discrete_low'].append(np.nan)
        try:
            database['pred_discrete_mean'].append(pred[pred.date == date].predicted_deaths_mean.values[0])
        except:
            database['pred_discrete_mean'].append(np.nan)
        try:
            database['pred_discrete_upper'].append(pred[pred.date == date].predicted_deaths_upper.values[0])
        except:
            database['pred_discrete_upper'].append(np.nan)
    
    
    
    plot_cummulative(index, database, max(clean_nan(cummulative.deaths)), prediction, country_name)

    plot_discrete(index, database, max(clean_nan(cummulative.deaths)), prediction, country_name)

def get_animation(country_name):

    country_name = country_name.lower()

    get_files(country_name)
        
    if not os.path.exists(f'plots/{country_name}/cummulative'):
        os.makedirs(f'plots/{country_name}/cummulative')
    if not os.path.exists(f'plots/{country_name}/discrete'):
        os.makedirs(f'plots/{country_name}/discrete')
    if not os.path.exists(f'results/{country_name}'):    
        os.makedirs(f'results/{country_name}')
    
    files_dir = os.listdir(f'predictions/{country_name}')
    
    oldest_file = min([pd.to_datetime(x[-14:-4]) for x in files_dir])
    newest_file = max([pd.to_datetime(x[-14:-4]) for x in files_dir])
    
    oldest_file= pd.read_csv(f'predictions/{country_name}/{country_name}_{str(oldest_file)[:10]}.csv')
    newest_file = pd.read_csv(f'predictions/{country_name}/{country_name}_{str(newest_file)[:10]}.csv')
        
    start_date = min(pd.to_datetime(oldest_file.date.copy()))
    end_date   = max(pd.to_datetime(newest_file.date.copy()))
    
    index = pd.date_range(start = start_date, end = end_date)
    
    cummulative = pd.DataFrame()
    cummulative['date'] = pd.to_datetime(newest_file.date.copy())
    cummulative['deaths']= newest_file.total_deaths
    cummulative = eliminate_negatives(cummulative)
    
    discrete = pd.DataFrame()
    discrete['date'] = pd.to_datetime(newest_file.date.copy())
    discrete['deaths']= newest_file.actual_deaths
    discrete = eliminate_negatives(discrete)
    
    for file in files_dir:
        process_data(index, cummulative, discrete, file, country_name)
        os.system('cls')
        print('##########')
        print(f'{file[-14:-4]} ready...')
    
    
    print('##########')
    print('Processing final animations...')
    # repeate last image so the final frame of the video lingers on
    pic_dates  = [x[:-4] for x in os.listdir(f'plots/{country_name}/cummulative')]
    max_date = str(max(pd.to_datetime(pic_dates)))[:10]
    
    for _ in range(50):
        copy2(f'plots/{country_name}/cummulative/{max_date}.jpg', f'plots/{country_name}/cummulative/{max_date}_{_}.jpg')
        copy2(f'plots/{country_name}/discrete/{max_date}.jpg', f'plots/{country_name}/discrete/{max_date}_{_}.jpg')
    
    cum_images = []
    
    for filename in os.listdir(f'plots/{country_name}/cummulative'):
        cum_images.append(imageio.imread(os.path.join(f'plots/{country_name}/cummulative',filename)))
    imageio.mimsave(f'results/{country_name}/cummulative_{country_name}.mp4', cum_images)
    print('##########')
    print('Cummulative animation ready...')

    dis_images = []
    
    for filename in os.listdir(f'plots/{country_name}/discrete'):
        dis_images.append(imageio.imread(os.path.join(f'plots/{country_name}/discrete',filename)))
    imageio.mimsave(f'results/{country_name}/discrete_{country_name}.mp4', dis_images)
    print('##########')
    print('Discrete animation ready...')
    print('##########')
    print(f'Animations ready, con be found on:\nresults/{country_name}')

def make_videos(country_name):
    #There is a warning on creating the final video with the defaul dimentions
    import warnings
    warnings.filterwarnings('ignore')
    
    # repeate last image so the final frame of the video lingers on
    pic_dates  = [x[:-4] for x in os.listdir(f'plots/{country_name}/cummulative')]
    max_date = str(max(pd.to_datetime(pic_dates)))[:10]
    
    for _ in range(50):
        copy2(f'plots/{country_name}/cummulative/{max_date}.jpg', f'plots/{country_name}/cummulative/{max_date}_{_}.jpg')
        copy2(f'plots/{country_name}/discrete/{max_date}.jpg', f'plots/{country_name}/discrete/{max_date}_{_}.jpg')
    
    cum_images = []
    
    for filename in os.listdir(f'plots/{country_name}/cummulative'):
        cum_images.append(imageio.imread(os.path.join(f'plots/{country_name}/cummulative',filename)))
    imageio.mimsave(f'results/{country_name}/cummulative_{country_name}.mp4', cum_images)
    print('##########')
    print('Cummulative animation ready...')
    
    dis_images = []
    
    for filename in os.listdir(f'plots/{country_name}/discrete'):
        dis_images.append(imageio.imread(os.path.join(f'plots/{country_name}/discrete',filename)))
    imageio.mimsave(f'results/{country_name}/discrete_{country_name}.mp4', dis_images)
    print('##########')
    print('Discrete animation ready...')
    print('##########')
    print(f'Animations ready, con be found on:\nresults/{country_name}')

def get_posible_countries():
    set_names = []
    for root, _, files in os.walk('projections'):
        if root.endswith('global'):
            for file in files:
                if file[0] not in '0123456789':
                    set_names.append(file[:-8])
    for name in set(set_names):
        print(name)

if __name__ == "__main__":
    if sys.argv[1] == 'names':
        get_posible_countries()
    else:
        try:
            get_animation(sys.argv[1])
        except:
            print(f"I don't understand the name of the country: {sys.argv[1]}\nposible names are: ")
            get_posible_countries()
            
    