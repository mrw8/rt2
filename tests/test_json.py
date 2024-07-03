import json

from rt_core_v2.ids_codes.Rui import Rui
from rt_core_v2.rttuple import Atuple
from rt_core_v2.rttuple_formatter import format_rttuples

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    

def test_json():
    ruip = Rui()
    ruia = Rui()
    ruit= Rui()

    atuple = Atuple(ruip, ruia, ruit)
    atuple_formated = format_rttuples(atuple)
    expected_1 = f"{{\"ruip\": \"{ruip}\", \"ruia\": \"{ruia}\", \"ruit\": \"{ruit}\", \"type\": \"{atuple.tuple_type}\", \"unique\": \"{atuple.unique}\", \"ar\": \"{atuple.ar}\", \"t\": \"{atuple.t}\"}}"
    print("Expected:  \n" + expected_1)
    print("Processed:  \n" + atuple_formated)
    assert(ordered(json.loads(atuple_formated)) == ordered(json.loads(expected_1)))

    # dtuple = Dtuple()

    # ftuple = Ftuple()


