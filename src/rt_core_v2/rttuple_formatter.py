import json
import enum

def rttuple_to_json(input_rttuples):
    """Converts either a list or an RtTuple to a json object"""
    return json.dumps(input_rttuples.get_str_attributes())

"""Enum mapping formats to functions to convert RtTuples into the format"""
class RtTupleFormat(enum.Enum):
    json_format = rttuple_to_json

def format_rttuples(tuples, format: RtTupleFormat=RtTupleFormat.json_format):
    """Convert the rttuple to the specified format"""
    return format(tuples)


# def tuple_to_rttuple(input_json):
#     """Converts the input JSON string into an rttuple if it exists"""

