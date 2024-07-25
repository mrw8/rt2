from rt_core_v2.ids_codes.rui import Rui, TempRef
from rt_core_v2.rttuple import (
    ATuple,
    DTuple,
    FTuple,
    NtoNTuple,
    NtoRTuple,
    NtoCTuple,
    NtoDETuple,
    NtoLackRTuple,
    TupleType,
    PorType,
    RuiStatus,
    TupleComponents
)

from rt_core_v2.metadata import TupleEventType, RtChangeReason
from rt_core_v2.factory import insert_rttuple

ruip = Rui()
ruia = Rui()
ruit = Rui()
ruid = Rui()
ruics = Rui()
ruir = Rui()
ruin = Rui()
ruidt = Rui()

unique = PorType.non_singular
ar = RuiStatus.assigned
time_1 = TempRef()
event = TupleEventType.INSERT
reason = RtChangeReason.BELIEF
replacements = [ruin, ruidt, ruin]
polarity = False
relation = "part of"
p_list = [ruid, ruin]
time_relation = "at"
code = "code insert"
inst = "instance of"
data = "data insert"


#TODO Fill out tests for tuple factory usage
def test_atuple_factory():
    a = ATuple(ruit, ruia, ruip, ar, unique, time_1)
    # a_args = {TupleComponents.ruit:ruit, TupleComponents.ruit:ruia, TupleComponents.ruit:ruip, TupleComponents.ruit:ar, TupleComponents.ruit:unique, TupleComponents.ruit:time_1}
    # a_fac, d_fac = insert_rttuple({:ruit, :ruia, :ruip, :ar, :unique, :time_1}, TupleType.ATuple)
# def test_dtuple_factory():

# def test_ftuple_factory():

# def test_ntodetuple_factory():

# def test_ntontuple_factory():

# def test_ntortuple_factory():

# def test_ntoctuple_factory():

# def test_ntolackrtuple_factory():

