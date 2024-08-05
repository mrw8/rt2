import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from rt_core_v2.ids_codes.rui import Rui, TempRef
from rt_core_v2.metadata import TupleEventType, ValueEnum, RtChangeReason

"""Takes an set of enums and converts them into a dict with mapping entry:value"""


def enum_to_dict(entries: set):
    return {entry: entry.value for entry in entries}


"""Enum representing RUI statuses"""


class RuiStatus(ValueEnum):
    assigned = "A"
    reserved = "R"


"""Enum representing the tuple types"""


class TupleType(ValueEnum):
    A = "A"
    D = "D"
    F = "F"
    NtoDE = "NtoDE"
    NtoN = "NtoN"
    NtoR = "NtoR"
    NtoC = "NtoC"
    NtoLackR = "NtoR(-)"


"""Enum representing portions of reality types"""


class PorType(ValueEnum):
    singular = "+SU"
    non_singular = "-SU"


# TODO Move this into the classes, as it is not a semantically sound placement here
class TupleComponents(enum.Enum):
    ruit = "ruit"
    ruitn = "ruitn"
    type = "type"
    ar = "ar"
    ruia = "ruia"
    unique = "unique"
    t = "t"
    ruid = "ruid"
    event = "event"
    event_reason = "event_reason"
    td = "td"
    replacements = "replacements"
    ta = "ta"
    C = "C"
    polarity = "polarity"
    r = "r"
    p_list = "p"
    tr = "tr"
    inst = "inst"
    ruin = "ruin"
    ruir = "ruir"
    ruics = "ruics"
    code = "code"
    data = "data"
    ruidt = "ruidt"
    rui = "rui"

def Visitor():
    def visit(self, host):
        pass

@dataclass
class RtTuple(ABC):
    """Abstract Referent Tracking tuple that contains the information that all referent tracking tuples contain

    Attributes:
    rui -- The rui of this tuple
    type -- The id of the tuple component
    """

    tuple_type: ClassVar[TupleType] = None
    params: ClassVar[dict[TupleComponents, str]] = {**enum_to_dict({TupleComponents.rui, TupleComponents.type})}
    rui: Rui = field(default_factory=Rui)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    def accept(self, visitor: Visitor):
        return visitor.visit(self)
    
    @abstractmethod
    def get_attributes(self) -> dict:
        """Get the attributes of this tuplestring"""
        return {
            self.params[TupleComponents.rui]: self.rui,
            self.params[TupleComponents.type]: self.tuple_type,
        }

@dataclass
class ATuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a PoR

    Attributes:
    ar -- The status of ruin
    ruin -- The Rui that is being assigned for the first time
    ruia -- The Rui of the author of this ATuple
    unique -- Asserts whether this is a non-repeatable or repeatable portion of reality
    t -- The time of the creation of the ATuple
    """

    tuple_type: ClassVar[TupleType] = TupleType.A
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ar,
                TupleComponents.t,
                TupleComponents.ruia,
                TupleComponents.unique,
                TupleComponents.ruin,
            }
        ),
    }
    ruia: Rui = field(default_factory=Rui)
    ruin: Rui = field(default_factory=Rui)
    ar: RuiStatus = RuiStatus.assigned
    unique: PorType = PorType.singular
    t: TempRef = field(default_factory=TempRef)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.ruia]] = self.ruia
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.ar]] = self.ar
        attributes[self.params[TupleComponents.unique]] = self.unique
        attributes[self.params[TupleComponents.t]] = self.t
        return attributes

@dataclass
class DTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the instantation of other tuple types

    Attributes:
    ruit -- The ruit of another tuple that this tuple stores information about
    event -- The category of reason that caused the creation of tuple ruit
    event_reason -- The reason for the event above occuring
    td -- The time of this tuple's creation
    replacements -- Any tuples that ruit replaces
    """

    # D#< RUId, RUIT, t, ‘I’/E, R, S >

    tuple_type: ClassVar[TupleType] = TupleType.D
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ruid,
                TupleComponents.event,
                TupleComponents.event_reason,
                TupleComponents.t,
                TupleComponents.replacements,
                TupleComponents.ruit
            }
        ),
    }
    ruit: Rui = field(default_factory=Rui)
    ruid: Rui = field(default_factory=Rui)
    t: TempRef = field(default_factory=TempRef)
    event: TupleEventType = field(default_factory=TupleEventType.INSERT)
    event_reason: RtChangeReason = field(default_factory=RtChangeReason.REALITY)
    #TODO Make replacements a shallow copy
    replacements: list[Rui] = field(default_factory=list)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = {}
        attributes[self.params[TupleComponents.type]] = self.tuple_type.value
        attributes[self.params[TupleComponents.ruid]] = self.ruid
        attributes[self.params[TupleComponents.rui]] = self.rui
        attributes[self.params[TupleComponents.ruit]] = self.ruit
        attributes[self.params[TupleComponents.event]] = self.event.value
        attributes[self.params[TupleComponents.event_reason]] = self.event_reason.value
        attributes[self.params[TupleComponents.t]] = self.t
        attributes[self.params[TupleComponents.replacements]] = self.replacements
        return attributes

@dataclass
class FTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the confidence level in another tuple's assertions

    Attributes:
    ruid -- The ruid of this tuple
    ruia -- The ruid of the author making the assertion
    ruitn -- The ruid of the tuple refered to by this tuple's confidence assertion.
    ta -- The time instance of the confidence assertion.
    C -- The level of confidence from 0.00-1.00 in the assertion.
    """

    # F#< RUId, ta, RUIa, RUITN, C >

    tuple_type: ClassVar[TupleType] = TupleType.F
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ruid,
                TupleComponents.ta,
                TupleComponents.C,
                TupleComponents.ruitn,
            }
        ),
    }
    ruid: Rui = field(default_factory=Rui)
    ruitn: Rui = field(default_factory=Rui)
    ta: TempRef = field(default_factory=TempRef)
    C: float = 1.0

    def get_attributes(self):
        """Get the attributes of this tuple"""
        attributes = {}
        attributes[self.params[TupleComponents.type]] = self.tuple_type.value
        attributes[self.params[TupleComponents.ruid]] = self.ruid
        attributes[self.params[TupleComponents.ruitn]] = self.ruitn
        attributes[self.params[TupleComponents.ta]] = self.ta
        attributes[self.params[TupleComponents.C]] = self.C
        attributes[self.params[TupleComponents.rui]] = self.rui

        return attributes

@dataclass
class NtoNTuple(RtTuple):
    """Tuple type that relates two or more non-repeatable portions of reality to one another

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    relation -- A relation between the non-repeatable portions of reality in p_list
    p_list -- A list of non-repeatable portions of reality that have the relationship described
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoNTuple#< ‘+’/‘-’, r, P, tr/‘-’ >
    tuple_type: ClassVar[TupleType] = TupleType.NtoN
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.polarity,
                TupleComponents.r,
                TupleComponents.p_list,
                TupleComponents.tr,
            }
        ),
    }
    polarity: bool = True
    r: str = ""
    #TODO Make a copy of p
    p: list[Rui] = field(default_factory=[])
    tr: TempRef = field(default_factory=TempRef)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.r]] = self.r
        attributes[self.params[TupleComponents.p_list]] = self.p
        attributes[self.params[TupleComponents.tr]] = self.tr
        return attributes

@dataclass
class NtoRTuple(RtTuple):
    """Tuple type that relates a non-repeatable portion of reality to a repeatable portion of reality

    Attribtues:
    polarity -- Boolean describing whether the relation is as stated or negated
    inst -- The instantiation relationship between the non-repeatable PoR an the repeatable PoR
    ruin -- The Rui of the non-repeatable PoR in the relation
    ruir -- The Rui of the repeatable Por in the relation
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoRTuple#< ‘+’/‘-’, inst, RUIn, RUIr, tr/‘-’ >

    tuple_type: ClassVar[TupleType] = TupleType.NtoR
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.polarity,
                TupleComponents.inst,
                TupleComponents.ruin,
                TupleComponents.ruir,
                TupleComponents.tr,
            }
        ),
    }
    polarity: bool = True
    inst: str = ""
    ruin: Rui = field(default_factory=Rui)
    ruir: Rui = field(default_factory=Rui)
    tr: TempRef = field(default_factory=TempRef)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.inst]] = self.inst
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.ruir]] = self.ruir
        attributes[self.params[TupleComponents.tr]] = self.tr
        return attributes


# TODO Use concepts
@dataclass
class NtoCTuple(RtTuple):
    """Tuple type that annotates a non-repeatable portion of reality with a "concept" code from a
    concept-based system

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    relation -- The relationship between the non-repeatable PoR and the concept
    ruics -- The Rui of the concept class the concept for the relation is from
    ruin -- The Rui of the non-repeatable PoR in the relation
    code -- The code for the concept within the concept class referred to by Ruics
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoC#< ‘+’/‘-’, r, RUIcs, ruin, code, tr >

    tuple_type: ClassVar[TupleType] = TupleType.NtoC
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.polarity,
                TupleComponents.r,
                TupleComponents.ruics,
                TupleComponents.ruin,
                TupleComponents.code,
                TupleComponents.tr,
            }
        ),
    }
    polarity: bool = True
    r: str = ""
    ruics: Rui = field(default_factory=Rui)
    ruin: Rui = field(default_factory=Rui)
    code: str = ""
    tr: TempRef = field(default_factory=TempRef)
    # TODO Make creating a tempref create an underlying time instance

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.r]] = self.r
        attributes[self.params[TupleComponents.ruics]] = self.ruics
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.code]] = self.code
        attributes[self.params[TupleComponents.tr]] = self.tr
        return attributes


# We use NtoDE instead of NtoI, and we use an instance for the identifying descriptor
# or IdD associated with:
# (1) and NtoRTuple tuple that says what type of IdD it is,
# (2) an NtoNTuple tuple to relate the name to what the IdD denotes, and
# (3) an NtoDE tuple to hold the actual written (or "string") form of the IdD.
# Note that an IdD can be a name, identifier, etc.
# TODO Figure out if data should be a string or generic data
@dataclass
class NtoDETuple(RtTuple):
    """Tuple type that creates a connection between a non-repeatable portion of reality and a piece of data

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    ruin -- The Rui of the tuple that the data is atrributed to
    data -- The data in the relationship
    ruidt -- An Rui containing the data type of data
    """

    # NtoDE#< '+/-', r, ruin, data, ruidt>

    tuple_type: ClassVar[TupleType] = TupleType.NtoDE
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.polarity,
                TupleComponents.ruin,
                TupleComponents.data,
                TupleComponents.ruidt,
            }
        ),
    }
    polarity: bool = True
    ruin: Rui = field(default_factory=Rui)
    data: str =""
    ruidt: Rui = field(default_factory=Rui)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.data]] = self.data
        attributes[self.params[TupleComponents.ruidt]] = self.ruidt
        return attributes

@dataclass
class NtoLackRTuple(RtTuple):
    """Tuple type that asserts that a repeatable portion of reality in a does not have a specified relationship with a non-repeateble portion of reality

    Attribtues:
    relation -- A relationship between a non-repeatable portion of reality and a repeatable portion of reality
    ruin -- The rui of the repeatable portion of reality that the non-repeatable does not have the relation to
    ruir -- The rui of the non-repeatable portion fo reality that does not have relation to the POR refered to buy ruin
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoRTuple(-) -tuple NtoRTuple(-)#< r, ruin, RUIr, rT/‘-’, tr/‘-’ >

    tuple_type: ClassVar[TupleType] = TupleType.NtoLackR
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.r,
                TupleComponents.ruin,
                TupleComponents.ruir,
                TupleComponents.tr,
            }
        ),
    }
    r: str = ""
    ruin: Rui = field(default_factory=Rui)
    ruir: Rui = field(default_factory=Rui)
    tr: TempRef = field(default_factory=TempRef)

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.r]] = self.r
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.ruir]] = self.ruir
        attributes[self.params[TupleComponents.tr]] = self.tr
        return attributes


"""Mapping from tuple id to the corresponding tuple class"""
type_to_class = {
    TupleType.A: ATuple,
    TupleType.D: DTuple,
    TupleType.F: FTuple,
    TupleType.NtoDE: NtoDETuple,
    TupleType.NtoN: NtoNTuple,
    TupleType.NtoR: NtoRTuple,
    TupleType.NtoC: NtoCTuple,
    TupleType.NtoLackR: NtoLackRTuple,
}
