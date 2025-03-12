# check Streamlit Secrets ".streamlit/secrets.toml" to hide api key when deploy (gpt_key.txt is ignored by git)
import openai


file_path = 'config/gpt_key.txt'
try:
    with open(file_path, 'r') as file:
        openai.api_key = file.read().strip('\n')

except FileNotFoundError:
    print(f"File not found at {file_path}")



def gpt_classification(prompt):
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        temperature = 0.7,
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

    )
    percentage = int(response.choices[0].message.content.strip().rstrip('%'))
    return percentage

#def predict(title):



if __name__ == "__main__":
    print(gpt_classification('高解析微區光譜儀'))