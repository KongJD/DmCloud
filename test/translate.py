import re
import requests
from hashlib import md5
import random
from bs4 import BeautifulSoup
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

text = """Description of A. utsteinense sp. nov.

Abditibacterium utsteinense (ut.stein.en’se. N.L. neut. adj. referring to Utsteinen, the location in Antarctica where the first strain was isolated).

The following properties are additional to those given for the genus. Cells are spherical to ovoid, 0.6–1.0 × 0.65–1.3 μm in size. Colonies are circular, smooth and pink with a red center on PH-5 medium. Growth occurs between 1 and 45 °C, with 15–18 °C as optimum. The pH range for growth is 6.5–8.0 with an optimum around 7.0–7.5. NaCl is not required for growth. The following substrates support stable growth on solid PH-5 medium: d-glucose, sucrose, sodium pyruvate, sodium succinate and sodium acetate. Susceptible to the antibiotics quinupristin/dalfopristin, linezolid, netilmicin, gentamicin, kanamycin, streptomycin, amikacin, clindamycin and minocycline (concentrations are given in Table S1). Antibiotics that are tolerated are listed in Table S1. Major cellular fatty acids are 16:1 ω7c/15 iso 2OH, 18:1 ω7c and 16:0 3OH. A full overview of all fatty acids can be found in Table S7. The DNA G + C content of the type strain is 54.27%.
Type strain, LMG 29911T (R-68213T = DSM 105287T), was isolated from a terrestrial sample taken in the proximity of the Belgian Princess Elisabeth Station, Utsteinen, East Antarctica.
Description of Abditibacterium gen. nov.
Abditibacterium (ab.di.ti.bac.te’ri.um. L. adj. abditus, remote, secluded; -i- connecting vowel; L. neut. n. bacterium, a small rod; N. L. neut. n. Abditibacterium, a small rod hiding in remote places).
Strictly aerobic, obligate oligotrophic heterotrophic bacteria. No photosynthetic growth is observed. Cells are free-living, stain Gram-negative and divide by binary fission. Non-motile and non-sporulating. Oxidase negative and catalase positive. Major cellular fatty acids are 16:1 ω7c/15 iso 2OH, 18:1 ω7c and 16:0 3OH.
Type species is A. utsteinense
https://www.sciencedirect.com/science/article/pii/S0723202018300341?via%3Dihub"""


def filter_text(text):
    com = []
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
        com.append(url)
        text = text.replace(url, "")
    text = text.strip().replace("\n", "")
    return text, ";".join(com)


def tranlate(query):
    appid = '20231018001851043'
    appkey = 'NXmxEjGrqz3UdpOdoUfZ'
    from_lang = 'en'
    to_lang = 'zh'
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    return result['trans_result'][0]["dst"]


def tiltle(urls_str):
    urls = urls_str.split(";")
    if urls:
        titles = []
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }
        for url in urls:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                pattern = re.compile(r"articleName\s*:\s*'([^']+)'")
                script = soup.find('script', text=pattern)
                tit = pattern.search(script.text).group(1)
                titles.append(tit)
            except:
                try:
                    tit = soup.find("div", {'class': "metadata_title"})
                    titles.append(tit.text)
                except:
                    print(f'{url} problem')
                    titles.append('')
        return ";".join(list(set(titles)))
    return ""


def database():
    df = pd.read_excel("../data/datatables.xlsx")
    df[['pro', 'urls']] = df['source'].astype(str).apply(lambda x: pd.Series(filter_text(x)))
    # df['titles'] = df["urls"].astype(str).apply(lambda x: tiltle(x) if x else "")
    for ind, row in df.iterrows():
        urls = row['urls']
        text = row['pro']
        if urls:
            try:
                df.loc[ind, "titles"] = tiltle(urls)
            except:
                df.loc[ind, "titles"] = ""
        else:
            df.loc[ind, "titles"] = ""
        if text:
            try:
                df.loc[ind, "translate"] = tranlate(text)
            except:
                df.loc[ind, "translate"] = "not translate success "
        else:
            df.loc[ind, "translate"] = ""
    df.drop("pro", axis=1)
    df.to_excel("data.xlsx", index=False)


if __name__ == '__main__':
    # text, urls = filter_text(text)
    # print(urls)
    text = """Description of Paraburkholderia haematera sp. nov.
Paraburkholderia haematera sp. nov. (hae.ma.te’ra. Gr. adj. haemateros, blood-thirsty; N.L. fem. adj. haematera, blood-thirsty; because of its hemolytic behavior on horse blood agar).
Cells are non-motile, rod-shaped, approximately 1 µm long and 0.5 µm wide. After incubation on NAB at 28 °C for three days, colonies have a diameter of 1 mm and are circular, opaque and beige. They are flat or slightly raised and have an entire edge and a smooth surface. Strain LMG 31837T optimally grows on NAB and TSA between 15 and 28 °C in aerobic conditions, but does not grow in anaerobic conditions on NAB, TSA or TSA supplemented with 10 mM KNO3. No growth at 4, 37, 40 and 45 °C. Growth in the presence of 0% and 1% NaCl, but not 2% or more. Growth at pH 6.0 and 7.0, but not at 4.0, 5.0, 8.0 or 9.0. Growth on MacConkey and Drigalski agar and no growth on cetrimide agar. Growth on Tween 20, 40, 60 and 80 agar base and hydrolysis of all Tweens after 7 days of incubation. Hemolysis on horse blood agar but no DNase activity and hydrolysis of"""
    res = tranlate(text)
    print(res)
    # title(urls)
    # database()
