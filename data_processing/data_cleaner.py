import pandas as pd

def delete_duplicates(merged_tender_df, merged_award_df):
    for df in [merged_tender_df, merged_award_df]:
        # Compute missing values count
        df['missing_values_count'] = df.isnull().sum(axis=1) + df.apply(lambda x: x == '', axis=1).sum(axis=1)
        # Sort by all required columns at once
        df.sort_values(by=['date', 'job_number', 'missing_values_count'], inplace=True)
        # Drop duplicates
        df.drop_duplicates(subset=['date', 'job_number'], keep='first', inplace=True)
        # Drop the extra column
        df.drop(columns=['missing_values_count'], inplace=True)





