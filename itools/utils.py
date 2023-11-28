import string

import pandas as pd
import os
import time
import random

from DmCloud.settings import random_path, save_fasta_path


class Utils:

    def read_qc_stats(self, qc_path):
        df = pd.read_csv(qc_path, sep="\t")
        result = {k: v[0] for k, v in df.to_dict().items()}
        return result


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class RandomNumber:

    def generate_path(self, path):
        now = int(round(time.time() * 1000))
        shift_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(now / 1000))
        rand = random.randint(1, 1000000)
        dir = "-".join([shift_time, generate_random_letters(), str(rand)])
        dir_path = os.path.join(path, dir)
        return dir_path, dir

    def save_fasta_path(self):
        now = int(round(time.time() * 1000))
        shift_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(now / 1000))
        rand = random.randint(1, 1000000)
        dir = "-".join([shift_time, generate_random_letters(), str(rand)])
        dir_path = os.path.join(save_fasta_path, dir)
        return dir_path, dir


def generate_random_letters():
    letters = string.ascii_lowercase + string.ascii_uppercase[:26]
    random_letters = random.sample(letters, 6)
    return "".join(random_letters)
