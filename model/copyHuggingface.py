pipe = pipeline("text-classification", model = 'manatiw/test-trainer-imbalanced1.0')

def predict(value):
  prediction = pipe(value)
  correlation = prediction[0]['label']
  score = prediction[0]['score']
  if correlation == 'negative':
    pos_score = (1 - score)
  else:
    pos_score = score
  return pos_score


merged_tender_df['score'] = merged_tender_df['title'].apply(predict)
merged_award_df['score'] = merged_award_df['title'].apply(predict)



#backup prompt
messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a classification AI that determines the relevance of Traditional Chinese bidding titles "
                        "to Molecular Devices' products, specifically plate readers and cell imaging systems.\n"
                        "Output a confidence score in from 0 to 100%, where:\n"
                        "- 100% means 'highly relevant'\n"
                        "- 0% means 'completely irrelevant'\n"
                        "- Titles unrelated to biology will be likely irrelevent\n\n"
                        "Examples:\n"
                        "- '流式細胞儀項目' → 80%\n"
                        "- '超微量分光光度計壹台' → 80%\n"
                        "- '化學試劑採購' → 30%\n"
                        "- '數位病理影像教學管理系統*1式' → 0%\n"
                        "- '螢光顯微鏡' → 70%\n"
                        "- '分光光度計水質分析儀' → 70%\n"
                        "- '多功能微盤分光光譜儀' → 100%\n"
                        "- '基因定序採購' → 0%"
                    ),},
            {"role": "user", "content": prompt}
            ]