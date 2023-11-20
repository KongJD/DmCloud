import pandas as pd
import pymysql


def comman(path="", table_name=""):
    df = pd.read_excel(path)
    cnx = pymysql.connect(user='siteusra', password='dm20210120',
                          host='192.168.100.10', database='DMCloudDb')

    df = df.where(df.notnull(), "")
    cols = df.columns
    # print(df["召回编号"].isnull().sum())
    # df["召回编号"].fillna("", inplace=True)

    cursor = cnx.cursor()
    for ind, row in df.iterrows():
        all = []
        for i in range(len(df.columns)):
            all.append(row[i])
        sql = f"INSERT INTO `{table_name}` (`" + "`, `".join(cols) + "`) VALUES (" + ", ".join(
            ["%s"] * len(cols)) + ")"
        cursor.execute(sql, tuple(all))

    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    # comman(path="../data/召回汇总-20231013.xlsx", table_name="baike_zhaohuiall")
    comman(path="../data/与召回相关风险.xlsx", table_name="baike_zhaohuirealtedrisk")
    # comman(path="../data/生物安全汇总-1010.xlsx", table_name="baike_biosafeall")
    # comman(path="../data/致病性-xlsx.xlsx", table_name="baike_zhidieases")
