import re
import pandas as pd

class PccG0vMerger:
    def __init__(self, pcc_tender_df, pcc_award_df, g0v_tender_df, g0v_award_df):
        self.pcc_tender_df = pcc_tender_df
        self.pcc_award_df = pcc_award_df
        self.g0v_tender_df = g0v_tender_df
        self.g0v_award_df = g0v_award_df



    def remove_spaces_around_chinese(self, text):
        '''
        #test this
        txt = "正立螢光電動顯微觀察系統 如CARL ZEISS AXIO IMAGER M2 或同等品以上 詳規範 共1ST"
        remove_spaces_around_chinese(txt)
        '''
        # Define a pattern to match Chinese characters
        chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]')

        # Split the text by spaces
        parts = text.split()

        # Remove spaces around Chinese characters
        cleaned_parts = []
        for part in parts:

            if cleaned_parts and chinese_char_pattern.search(part):
                cleaned_parts[-1] += part

            elif cleaned_parts and chinese_char_pattern.search(cleaned_parts[-1][-1]):
                    # Append English parts without space if previous part was Chinese
                cleaned_parts[-1] += part

            else:
                cleaned_parts.append(part)

        # Join the cleaned parts with spaces
        cleaned_text = ' '.join(cleaned_parts)

        return cleaned_text

 
    def clean_g0v_titles_in_df(self, df):
        if 'title' in df.columns:
            df['title'] = df['title'].apply(self.remove_spaces_around_chinese)
        return df 



    def run_merger(self):
        g0v_tender_df = self.clean_g0v_titles_in_df(self.g0v_tender_df)
        g0v_award_df = self.clean_g0v_titles_in_df(self.g0v_award_df)


        #Check empty dataframe
        empty_tender_df = pd.DataFrame(columns=self.pcc_tender_df.columns)
        empty_award_df = pd.DataFrame(columns=self.pcc_award_df.columns)
        g0v_tender_df = g0v_tender_df if not g0v_tender_df.empty else empty_tender_df
        g0v_award_df = g0v_award_df if not g0v_award_df.empty else empty_award_df

        # Outer merge gov and g0v data
        merged_tender_df = self.pcc_tender_df.merge(g0v_tender_df, on=['date', 'title','keyword', 'job_number', '機關名稱', '領投開標:截止投標', 'url'], how='outer')
        merged_award_df = self.pcc_award_df.merge(g0v_award_df, on=['date', 'title', 'keyword', 'type', 'job_number', '機關名稱', 'url'], how='outer')

        return merged_tender_df, merged_award_df
    