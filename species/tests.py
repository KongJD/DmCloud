import pandas as pd

df = pd.read_excel("../data/data.xlsx")

df1 = pd.read_excel("../data/genus_info.xlsx")

df["shu"] = df["species"].apply(lambda x: x.split(" ")[0])

all1 = list(set(df["shu"]))
all2 = list(set(df1["latin_name"]))

res = []
for m in all1:
    if m not in all2 and m:
        res.append(m)

print(len(res))

with open("../data/add.txt", mode="w") as f:
    for t in res:
        f.write(f"{t}\n")
