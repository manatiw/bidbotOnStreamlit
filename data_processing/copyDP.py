
# Delete Duplicates(drop
merged_tender_df['missing_values_count'] = merged_tender_df.isnull().sum(axis=1) + merged_tender_df.apply(lambda x: x == '', axis=1).sum(axis=1)
merged_award_df['missing_values_count'] = merged_award_df.isnull().sum(axis=1) + merged_award_df.apply(lambda x: x == '', axis=1).sum(axis=1)
merged_tender_df = merged_tender_df.sort_values(by=['date', 'job_number', 'missing_values_count'])
merged_award_df = merged_award_df.sort_values(by=['date', 'job_number', 'missing_values_count'])
cleaned_tender_df = merged_tender_df.drop_duplicates(subset=['date', 'job_number'], keep='first')
cleaned_award_df = merged_award_df.drop_duplicates(subset=['date', 'job_number'], keep='first')
cleaned_tender_df = cleaned_tender_df.drop(columns=['missing_values_count'])
cleaned_award_df = cleaned_award_df.drop(columns=['missing_values_count'])




# Apply threshold
merged_tender_df = merged_tender_df[merged_tender_df['score'] >= CLASSIFICATION_THRESHOLD]
merged_award_df = merged_award_df[merged_award_df['score'] >= CLASSIFICATION_THRESHOLD]

#merged_tender_df.replace('', pd.NA, inplace=True)
#merged_tender_df['date'] = merged_tender_df['date'].astype(str)
#merged_tender_df['job_number'] = merged_tender_df['job_number'].astype(str)
#merged_tender_df['date'] = merged_tender_df['date'].str.strip()
#merged_tender_df['job_number'] = merged_tender_df['job_number'].str.strip()


tz = pytz.timezone('Asia/Taipei')
today_str = datetime.now(tz).strftime('%m%d%Y')
cleaned_tender_df.to_csv(f'{today_str}newTender.csv', index=False, encoding='utf-8-sig')
cleaned_award_df.to_csv(f'{today_str}newAward.csv', index=False, encoding='utf-8-sig')