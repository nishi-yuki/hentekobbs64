import random
import itertools


# NUM  1     2     3     4     5     6     7     8
chrsets = (
    ("怪", "蝕", "真", "戯", "酔", "霊", "魔", "猛"),
    ("亀", "馬", "猫", "象", "牛", "鶏", "鹿", "龍"),
)


def make_namelist():
    all_name = ["".join(cs) for cs in itertools.product(*chrsets)]
    return random.sample(all_name, len(all_name))
