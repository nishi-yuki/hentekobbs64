import random
import itertools


# NUM  1     2     3     4     5     6     7     8
chrsets = (
    ("怪", "蝕", "真", "戯", "酔", "霊", "魔", "猛",
     "朔", "地", "迷", "儚", "偽", "嵬", "虚", "天"),
    ("亀", "馬", "猫", "象", "牛", "鶏", "鹿", "龍",
     "鵺", "駒", "兎", "狐", "鰐", "蛾", "獏", "蝗"),
)

names = tuple(itertools.product(*chrsets))


def get_name_count():
    return len(chrsets[0])*len(chrsets[1])


# def get_shuffled_nameids():
#     return random.sample(range(get_name_count()), get_name_count())


def get_name(nid):
    '''nidから名前を求める
    nidは 0 から始まる
    '''
    return names[nid]


def get_shuffled_names():
    all_name = ["".join(cs) for cs in itertools.product(*chrsets)]
    return random.sample(all_name, len(all_name))
