import json

from rt_core_v2.ids_codes.Rui import Rui, TempRef
from rt_core_v2.rttuple import ATuple, DTuple, FTuple, NtoNTuple, NtoRTuple, NtoCTuple
from rt_core_v2.rttuple_formatter import format_rttuples
from rt_core_v2.metadata_accessory import TupleEventType, RtChangeReason

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    
ruip = Rui()
ruia = Rui()
ruit= Rui()
ruid = Rui()
ruics = Rui()
ruir = Rui()
ruin = Rui()
time_1 = TempRef()
event = TupleEventType.INSERT
reason = RtChangeReason.BELIEF
replacements = []
polarity = False
relation = "part of"
p_list = [ruid]
time_relation = "at"
code = "1234"
inst = "instance of"

def compare(formatted, expected):
    return ordered(json.loads(formatted)) == ordered(json.loads(expected))

def test_atuple_json():
    a = ATuple(ruit, ruia, ruip)
    formatted_a = format_rttuples(a)
    expected_a = f"{{\"ruip\": \"{ruip}\", \"ruia\": \"{ruia}\", \"ruit\": \"{ruit}\", \"type\": \"{a.tuple_type}\", \"unique\": \"{a.unique}\", \"ar\": \"{a.ar}\", \"t\": \"{a.t}\"}}"
    print("Atuple Expected:  \n" + expected_a)
    print("Atuple Processed:  \n" + formatted_a)
    assert compare(formatted_a, expected_a)

def test_dtuple_json():
    d = DTuple(ruid, ruit, time_1, TupleEventType.INSERT, RtChangeReason.BELIEF, replacements)
    formatted_d = format_rttuples(d)
    expected_d = f"{{\"type\": \"{d.tuple_type}\", \"ruid\": \"{ruid}\", \"ruit\": \"{ruit}\", \"t\": \"{time_1}\", \"event\": \"{event}\", \"event_reason\": \"{reason}\", \"replacements\": \"{replacements}\"}}"
    print("Dtuple Expected:  \n" + expected_d)
    print("Dtuple Processed:  \n" + formatted_d)
    assert compare(formatted_d, expected_d)

def test_ftuple_json():
    C = 0.753
    f = FTuple(ruid, ruit, time_1, ruia, C)
    formatted_f = format_rttuples(f)
    expected_f = f"{{\"type\": \"{f.tuple_type}\", \"ruid\": \"{ruid}\", \"ruit\": \"{ruit}\", \"ta\": \"{time_1}\", \"ruia\": \"{ruia}\", \"C\": \"{C}\"}}"
    print("Ftuple Expected:  \n" + expected_f)
    print("Ftuple Processed:  \n" + formatted_f)

    assert compare(formatted_f, expected_f)

def test_nton_json():
    nton = NtoNTuple(ruit, polarity, relation, p_list, time_relation, time_1)
    formatted_nton = format_rttuples(nton)
    expected_nton = f"{{\"type\": \"{nton.tuple_type}\", \"ruit\": \"{ruit}\", \"polarity\": \"{polarity}\", \"r\": \"{relation}\", \"p_list\": [\"{ruid.uuid}\"], \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\"}}"

    print("Ntontuple Expected:  \n" + expected_nton)
    print("Ntontuple Processed:  \n" + formatted_nton)

    assert compare(formatted_nton, expected_nton)

def test_ntor_json():
    ntor = NtoRTuple(ruit, polarity, inst, ruin, ruir, time_relation, time_1)
    formatted_ntor = format_rttuples(ntor)
    expected_ntor = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntor.tuple_type}\", \"polarity\": \"{polarity}\", \"inst\": \"{inst}\", \"ruir\": \"{ruir}\", \"ruin\": \"{ruin}\", \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\"}}"

    print("Ntortuple Expected:  \n" + expected_ntor)
    print("Ntonrtuple Processed:  \n" + formatted_ntor)

    assert compare(formatted_ntor, expected_ntor)

def test_ntoc_json():
    ntoc = NtoCTuple(ruit, polarity, relation, ruics, ruip, code, time_relation, time_1)
    formatted_ntoc = format_rttuples(ntoc)
    expected_ntoc = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntoc.tuple_type}\", \"polarity\": \"{polarity}\", \"r\": \"{relation}\", \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\", \"ruics\": \"{ruics}\", \"ruip\": \"{ruip}\", \"code\": \"{code}\"}}"

    print("Ntoctuple Expected:  \n" + expected_ntoc)
    print("Ntoctuple Processed:  \n" + formatted_ntoc)

    assert compare(formatted_ntoc, expected_ntoc)
