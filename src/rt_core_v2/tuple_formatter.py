import json

from rttuple import RtTuple

def rttuple_to_json(input_rttuple: RtTuple):
    return json.dumps(input_rttuple.get_str_attributes())