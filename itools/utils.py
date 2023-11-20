import pandas as pd
import os
import time
import random

all_path = "/public/Users/kongjind/pipeline/geneidentitytools/random"


class Utils:

    def read_qc_stats(self, qc_path):
        df = pd.read_csv(qc_path, sep="\t")
        result = {k: v[0] for k, v in df.to_dict().items()}
        return result


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class RandomNumber:

    def generate_path(self):
        now = int(round(time.time() * 1000))
        shift_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(now / 1000))
        rand = random.randint(1, 1000000)
        dir = "-".join([shift_time, str(rand)])
        dir_path = os.path.join(all_path, dir)
        return dir_path, dir
