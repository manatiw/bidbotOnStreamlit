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