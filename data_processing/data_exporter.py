import pytz
from datetime import datetime


def save_dataframes_as_csv(*dataframes):
    today_str = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%m%d%Y')

    for df in dataframes:    
        file_name = df.__class__.__name__
        df.to_csv(f'{today_str}_{file_name}.csv', index=False, encoding='utf-8-sig')
