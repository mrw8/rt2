import json

from rttuple import *
from tuple_formatter import rttuple_to_json

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    

def test_json():
    a = Rui()

    x = Rui()
    y = Atuple(x)

    q = Rui()
    z = Atuple(q, ruia=a, unique="+SU", ar='R')

    print(rttuple_to_json(z))
