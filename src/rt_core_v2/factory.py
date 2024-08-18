from rt_core_v2.rttuple import TupleType, DTuple, type_to_class
from rt_core_v2.metadata import RtChangeReason, TupleEventType


def insert_rttuple(tuple_arguments: dict, type: TupleType):
   return rttuple_factory(dict, type, TupleEventType.INSERT, RtChangeReason.BELIEF)


# TODO Create testing that creates every tuple type using this functions
def rttuple_factory(tuple_arguments: dict, type: TupleType, event: TupleEventType, event_reason: RtChangeReason):
    # DTuples should only be created in tandem with another tuple
    if type is TupleType.D:
        return None
    try:
        concrete_tuple = type_to_class[type](**tuple_arguments)
        meta_tuple = DTuple(
            concrete_tuple.ruit,
            concrete_tuple.t,
            event, 
            event_reason
        )
    except TypeError:
        # TODO Log error where tuple has incorrect arguments
        print(f"Incorrect arguments passed for tuple of type {type}")
        return None

    return concrete_tuple, meta_tuple
