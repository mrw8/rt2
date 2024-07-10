import json
import enum
from io import StringIO
from uuid import UUID

from rt_core_v2.rttuple import TupleComponents, TupleType, type_to_class, RuiStatus, PorType
from rt_core_v2.ids_codes.Rui import Rui, TempRef
from rt_core_v2.metadata_accessory import TupleEventType, RtChangeReason

def rttuple_to_json(input_rttuples):
    """Converts either a list or an RtTuple to a json object"""
    return json.dumps(input_rttuples.get_str_attributes(), default=lambda o: o.toJSON() if hasattr(o, 'toJSON') else str(o))

"""Enum mapping formats to functions to convert RtTuples into the format"""
class RtTupleFormat(enum.Enum):
    json_format = rttuple_to_json

def format_rttuples(tuples, format: RtTupleFormat=RtTupleFormat.json_format, stream=StringIO):
    """Convert the rttuple to the specified format"""
    return format(tuples)

"""Function collection for mapping"""
class JsonEntryConverter():

    @staticmethod
    def str_to_rui(x):
        return Rui(UUID(x))
    
    @staticmethod
    def str_to_temp(x):
        return TempRef(Rui(UUID(x)))
    
    @staticmethod
    def lst_to_ruis(x):
        return [Rui(UUID(entry)) for entry in x]
    
    @staticmethod
    def str_to_str(x):
        return x

json_entry_converter = {
    TupleComponents.ruit: JsonEntryConverter.RtChangeReason.str_to_rui,
    TupleComponents.ruip: RtChangeReason.str_to_rui,
    TupleComponents.ruia: RtChangeReason.str_to_rui,
    TupleComponents.ruid: RtChangeReason.str_to_rui,
    TupleComponents.ruin: RtChangeReason.str_to_rui,
    TupleComponents.ruir: RtChangeReason.str_to_rui,
    TupleComponents.ruics: RtChangeReason.str_to_rui,
    TupleComponents.ruins: RtChangeReason.str_to_rui,
    TupleComponents.ruidt: RtChangeReason.str_to_rui,
    TupleComponents.t: RtChangeReason.str_to_temp,
    TupleComponents.td: RtChangeReason.str_to_temp,
    TupleComponents.ta: RtChangeReason.str_to_temp,
    TupleComponents.tr: RtChangeReason.str_to_temp,
    TupleComponents.ar: lambda x: RuiStatus(x),
    TupleComponents.unique: lambda x: PorType(x),
    TupleComponents.event: lambda x: TupleEventType(x),
    #TODO Figure out type of event_reason
    TupleComponents.event_reason: lambda x: RtChangeReason(x),
    TupleComponents.replacements: RtChangeReason.lst_to_ruis,
    TupleComponents.p_list: RtChangeReason.lst_to_ruis,
    TupleComponents.C: lambda x: float(x),
    TupleComponents.polarity: lambda x: bool(x),
    TupleComponents.r: RtChangeReason.str_to_str,
    #TODO Figure out type of rT, inst, code, data
    TupleComponents.rT: RtChangeReason.str_to_str,
    TupleComponents.inst: RtChangeReason.str_to_str,
    TupleComponents.code: RtChangeReason.str_to_str,
    TupleComponents.data: RtChangeReason.str_to_str,
    TupleComponents.type: lambda x: TupleType(x)
}

def json_to_rttuple(tuple_json):
    """Map a json to an rttuple"""
    tuple_dict = json.loads(tuple_json)
    for key, value in tuple_dict.items():
        try:
            entry = TupleComponents(key)
            entry[key] = json_entry_converter[entry](value)
        except ValueError: 
            #TODO Log error
            tuple_dict = None
            return None
    return type_to_class[tuple_dict[TupleComponents.type]](**tuple_dict)


            


    return type_to_class[TupleType(tuple_dict[TupleComponents.type])](**tuple_dict)
