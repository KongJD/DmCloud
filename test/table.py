import pandas as pd
import re


def filter_text(text):
    com = []
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
        com.append(url)
        text = text.replace(url, "")
    lines = text.split("\n")
    filter_lines = [line for line in lines if not line.startswith("Description of")]
    all_text = "".join(filter_lines)
    pattern = r"DOI:\s\d+\.\d+\/\S+"
    result = re.sub(pattern, "", all_text)
    pattern1 = r"DOI :\s\d+\.\d+\/\S+"
    result1 = re.sub(pattern1, "", result)
    return result1, ";".join(com)


df = pd.read_excel("../data/verified用户source（1925）.xlsx")


df[['sou', 'urls']] = df['source'].astype(str).apply(lambda x: pd.Series(filter_text(x)))

df_tran = df[["uniqueID", "sou"]]
df['len'] = df["sou"].apply(lambda x: len(x))
print(df["len"])
print(df["len"].sum())
df_tran.to_csv('need_translate.txt', sep="\t", index=False)

"""
| Kosakonia cowanii         | 2      |
| Kosakonia oryzae          | 2      |
| Kosakonia oryzendophytica | 2      |
| Kosakonia sacchari        | 2      |
| Kosakonia cowanii         | 2      |
| Kosakonia oryzae          | 2      |
| Kosakonia oryzendophytica | 2      |
| Kosakonia sacchari        | 2      |
| Kosakonia cowanii         | 1      |
| Kosakonia oryzae          | 1      |
| Kosakonia oryzendophytica | 1      |
| Kosakonia sacchari        | 1      |
| Kosakonia radicincitans   | 1      |
| Kosakonia quasisacchari   | 1      |
| Kosakonia pseudosacchari  | 1      |
| Kosakonia oryziphila      | 1      |
| Kosakonia arachidis       | 1 

"""
