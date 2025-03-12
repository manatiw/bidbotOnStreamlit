# check Streamlit Secrets ".streamlit/secrets.toml" to hide api key when deploy (gpt_key.txt is ignored by git)
import openai
import streamlit as sl


'''file_path = 'config/gpt_key.txt'
try:
    with open(file_path, 'r') as file:
        openai.api_key = file.read().strip('\n')

except FileNotFoundError:
    print(f"File not found at {file_path}")'''

oak = sl.secrets['OPENAI_API_KEY']
try:
    with oak:
        openai.api_key = oak

except FileNotFoundError:
    print(f"File not found at {file_path}")


def gpt_classification(prompt):
    try:
        response = openai.chat.completions.create(
            model='gpt-3.5-turbo',
            temperature=0.6,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classification AI that determines the relevance of Traditional Chinese bidding titles "
                        "to Molecular Devices' products, specifically plate readers and cell imaging systems.\n"
                        "Output ONLY a confidence score as an integer from 0 to 100, without any additional text or symbols.\n"
                        "If the title is highly relevant, output 100.\n"
                        "If the title is completely irrelevant, output 0.\n"
                        "Titles unrelated to biology will likely be irrelevant.\n\n"
                        "Examples:\n"
                        "- '流式細胞儀項目' → 80\n"
                        "- '超微量分光光度計壹台' → 80\n"
                        "- '化學試劑採購' → 30\n"
                        "- '數位病理影像教學管理系統*1式' → 0\n"
                        "- '螢光顯微鏡' → 70\n"
                        "- '分光光度計水質分析儀' → 70\n"
                        "- '多功能微盤分光光譜儀' → 100\n"
                        "- '基因定序採購' → 0\n\n"
                        "Output format:\n"
                        "Only provide a number between 0 and 100, with no explanation or symbols."
                    ),
                },
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and parse the response
        classification_score = response.choices[0].message.content.strip()
        percentage = int(classification_score)  # Convert to integer
        return percentage

    except openai.error.OpenAIError as e:
        print(f"AI chat error occurred: {e}")
        return None  # Return None in case of an error


if __name__ == "__main__":
    print(gpt_classification('高解析微區光譜儀'))
    print(gpt_classification('微盤光譜'))
    print(gpt_classification('細胞蛋白'))
