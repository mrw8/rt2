import json

from rt_core_v2.ids_codes.Rui import Rui
from rt_core_v2.rttuple import ATuple, DTuple
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

    Atuple = ATuple(ruit, ruia, ruip)
    ATuple_formated = format_rttuples(Atuple)
    expected_1 = f"{{\"ruip\": \"{ruip}\", \"ruia\": \"{ruia}\", \"ruit\": \"{ruit}\", \"type\": \"{Atuple.tuple_type}\", \"unique\": \"{Atuple.unique}\", \"ar\": \"{Atuple.ar}\", \"t\": \"{Atuple.t}\"}}"
    print("Expected:  \n" + expected_1)
    print("Processed:  \n" + ATuple_formated)
    assert(ordered(json.loads(ATuple_formated)) == ordered(json.loads(expected_1)))

    d = DTuple()
    
    # FTuple = FTuple()


