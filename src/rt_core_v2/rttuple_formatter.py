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
    TupleComponents.ruit: JsonEntryConverter.str_to_rui,
    TupleComponents.ruip: JsonEntryConverter.str_to_rui,
    TupleComponents.ruia: JsonEntryConverter.str_to_rui,
    TupleComponents.ruid: JsonEntryConverter.str_to_rui,
    TupleComponents.ruin: JsonEntryConverter.str_to_rui,
    TupleComponents.ruir: JsonEntryConverter.str_to_rui,
    TupleComponents.ruics: JsonEntryConverter.str_to_rui,
    TupleComponents.ruins: JsonEntryConverter.str_to_rui,
    TupleComponents.ruidt: JsonEntryConverter.str_to_rui,
    TupleComponents.t: JsonEntryConverter.str_to_temp,
    TupleComponents.td: JsonEntryConverter.str_to_temp,
    TupleComponents.ta: JsonEntryConverter.str_to_temp,
    TupleComponents.tr: JsonEntryConverter.str_to_temp,
    TupleComponents.ar: lambda x: RuiStatus(x),
    TupleComponents.unique: lambda x: PorType(x),
    TupleComponents.event: lambda x: TupleEventType(x),
    #TODO Figure out type of event_reason
    TupleComponents.event_reason: lambda x: RtChangeReason(x),
    TupleComponents.replacements: JsonEntryConverter.lst_to_ruis,
    TupleComponents.p_list: JsonEntryConverter.lst_to_ruis,
    TupleComponents.C: lambda x: float(x),
    TupleComponents.polarity: lambda x: bool(x),
    TupleComponents.r: JsonEntryConverter.str_to_str,
    #TODO Figure out type of rT, inst, code, data
    TupleComponents.rT: JsonEntryConverter.str_to_str,
    TupleComponents.inst: JsonEntryConverter.str_to_str,
    TupleComponents.code: JsonEntryConverter.str_to_str,
    TupleComponents.data: JsonEntryConverter.str_to_str,
    TupleComponents.type: lambda x: TupleType(x)
}

def json_to_rttuple(tuple_json):
    """Map a json to an rttuple"""
    tuple_dict = json.loads(tuple_json)
    for key, value in tuple_dict.items():
        try:
            entry = TupleComponents(key)
            tuple_dict[key] = json_entry_converter[entry](value)
        except ValueError: 
            #TODO Log error
            tuple_dict = None
            return None
    tuple_class = type_to_class[tuple_dict[TupleComponents.type.value]]
    del tuple_dict[TupleComponents.type.value]
    return tuple_class(**tuple_dict)


            


    return type_to_class[TupleType(tuple_dict[TupleComponents.type])](**tuple_dict)
