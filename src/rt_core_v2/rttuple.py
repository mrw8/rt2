import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, override

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
    AR = "AR"
    AN = "AN"
    Dc = "Dc"
    Di = "Di"
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
    ruio = 'ruio'
    type = "type"
    ar = "ar"
    ruia = "ruia"
    unique = "unique"
    t = "t"
    ruid = "ruid"
    event = "event"
    event_reason = "event_reason"
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

class RtTupleVisitor(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
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

    def accept(self, visitor: RtTupleVisitor):
        return visitor.visit(self)

@dataclass
class ANTuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a PoR

    Attributes:
    ar -- The status of ruin
    ruin -- The Rui that is being assigned for the first time
    ruia -- The Rui of the author of this ANTuple
    unique -- Asserts whether this is a non-repeatable or repeatable portion of reality
    t -- The time of the creation of the ANTuple
    """

    tuple_type: ClassVar[TupleType] = TupleType.AN
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



#TODO Add ontology field
#TODO Figure out the process for inserting an ontology. Is it just an instance that has an ntode tuple linking to the website?
@dataclass
class ARTuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a PoR

    Attributes:
    ar -- The status of ruin
    ruin -- The Rui that is being assigned for the first time
    ruia -- The Rui of the author of this ARTuple
    unique -- Asserts whether this is a non-repeatable or repeatable portion of reality
    t -- The time of the creation of the ARTuple
    """

    tuple_type: ClassVar[TupleType] = TupleType.AR
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ar,
                TupleComponents.t,
                TupleComponents.ruia,
                TupleComponents.unique,
                TupleComponents.ruir,
                TupleComponents.ruio,
            }
        ),
    }
    ruia: Rui = field(default_factory=Rui)
    ruir: Rui = field(default_factory=Rui)
    ruio: Rui = field(default_factory=Rui)
    ar: RuiStatus = RuiStatus.assigned
    unique: PorType = PorType.singular
    t: TempRef = field(default_factory=TempRef)


@dataclass
class DiTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the instantation of other tuple types

    Attributes:
    ruit -- The ruit of another tuple that this tuple stores information about
    event -- The category of reason that caused the creation of tuple ruit
    event_reason -- The reason for the event above occuring
    td -- The time of this tuple's creation
    replacements -- Any tuples that ruit replaces
    """

    # D#< RUId, RUIT, t, ‘I’/E, R, S >

    tuple_type: ClassVar[TupleType] = TupleType.Di
    params: ClassVar[dict[TupleComponents, str]] = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ruid,
                TupleComponents.event_reason,
                TupleComponents.t,
                TupleComponents.ruit,
                TupleComponents.ruia,
                TupleComponents.ta,
            }
        ),
    }
    ruit: Rui = field(default_factory=Rui)
    ruid: Rui = field(default_factory=Rui)
    t: TempRef = field(default_factory=TempRef)
    event_reason: RtChangeReason = field(default_factory=RtChangeReason.REALITY)
    ruia: Rui = field(default_factory=Rui)
    ta: TempRef = field(default_factory=TempRef)


@dataclass
class DcTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the instantation of other tuple types

    Attributes:
    ruit -- The ruit of another tuple that this tuple stores information about
    event -- The category of reason that caused the creation of tuple ruit
    event_reason -- The reason for the event above occuring
    td -- The time of this tuple's creation
    replacements -- Any tuples that ruit replaces
    """

    # D#< RUId, RUIT, t, ‘I’/E, R, S >

    tuple_type: ClassVar[TupleType] = TupleType.Dc
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

"""Mapping from tuple id to the corresponding tuple class"""
type_to_class = {
    TupleType.AN: ANTuple,
    TupleType.AR: ARTuple,
    TupleType.Di: DiTuple,
    TupleType.Dc: DcTuple,
    TupleType.F: FTuple,
    TupleType.NtoDE: NtoDETuple,
    TupleType.NtoN: NtoNTuple,
    TupleType.NtoR: NtoRTuple,
    TupleType.NtoC: NtoCTuple,
    TupleType.NtoLackR: NtoLackRTuple,
}

class AttributesVisitor(RtTupleVisitor):
    """
    Visitor that converts a tuple's representation to a dictionary 
    mapping the TupleComponent entry type to the value of the entry
    """
    def __init__(self):
        super().__init__()

    @override
    def visit(self, host:RtTuple):
        attributes = {}
        attributes = {
            host.params[TupleComponents.rui]: host.rui,
            host.params[TupleComponents.type]: host.tuple_type,
        }
        match host.tuple_type:
            case TupleType.AN:
                attributes |= self.visit_an(host)
            case TupleType.AR:
                attributes |= self.visit_ar(host)
            case TupleType.Di:
                attributes |= self.visit_di(host)
            case TupleType.Dc:
                attributes |= self.visit_dc(host)
            case TupleType.F:
                attributes |= self.visit_f(host)
            case TupleType.NtoN:
                attributes |= self.visit_nton(host)
            case TupleType.NtoR:
                attributes |= self.visit_ntor(host)
            case TupleType.NtoC:
                attributes |= self.visit_ntoc(host)
            case TupleType.NtoDE:
                attributes |= self.visit_ntode(host)
            case TupleType.NtoLackR:
                attributes |= self.visit_ntolackr(host)
        return attributes

    def visit_an(self, host:ANTuple):
        attributes = {}
        attributes[host.params[TupleComponents.ruia]] = host.ruia
        attributes[host.params[TupleComponents.ruin]] = host.ruin
        attributes[host.params[TupleComponents.ar]] = host.ar
        attributes[host.params[TupleComponents.unique]] = host.unique
        attributes[host.params[TupleComponents.t]] = host.t
        return attributes
    
    def visit_ar(self, host:ARTuple):
        attributes = {}
        attributes[host.params[TupleComponents.ruia]] = host.ruia
        attributes[host.params[TupleComponents.ruir]] = host.ruir
        attributes[host.params[TupleComponents.ruio]] = host.ruio
        attributes[host.params[TupleComponents.ar]] = host.ar
        attributes[host.params[TupleComponents.unique]] = host.unique
        attributes[host.params[TupleComponents.t]] = host.t
        return attributes

    def visit_di(self, host:DiTuple):
        attributes = {}
        attributes[host.params[TupleComponents.ruid]] = host.ruid
        attributes[host.params[TupleComponents.ruit]] = host.ruit
        attributes[host.params[TupleComponents.event_reason]] = host.event_reason.value
        attributes[host.params[TupleComponents.t]] = host.t
        attributes[host.params[TupleComponents.ruia]] = host.ruia
        attributes[host.params[TupleComponents.ta]] = host.ta
        return attributes


    def visit_dc(self, host:DcTuple):
        attributes = {}
        attributes[host.params[TupleComponents.ruid]] = host.ruid
        attributes[host.params[TupleComponents.ruit]] = host.ruit
        attributes[host.params[TupleComponents.event]] = host.event.value
        attributes[host.params[TupleComponents.event_reason]] = host.event_reason.value
        attributes[host.params[TupleComponents.t]] = host.t
        attributes[host.params[TupleComponents.replacements]] = host.replacements
        return attributes

    def visit_f(self, host:FTuple):
        attributes = {}
        attributes[host.params[TupleComponents.ruid]] = host.ruid
        attributes[host.params[TupleComponents.ruitn]] = host.ruitn
        attributes[host.params[TupleComponents.ta]] = host.ta
        attributes[host.params[TupleComponents.C]] = host.C
        return attributes

    def visit_nton(self, host:NtoNTuple):
        attributes = {}
        attributes[host.params[TupleComponents.polarity]] = host.polarity
        attributes[host.params[TupleComponents.r]] = host.r
        attributes[host.params[TupleComponents.p_list]] = host.p
        attributes[host.params[TupleComponents.tr]] = host.tr
        return attributes

    def visit_ntor(self, host:NtoRTuple):
        attributes = {}
        attributes[host.params[TupleComponents.polarity]] = host.polarity
        attributes[host.params[TupleComponents.inst]] = host.inst
        attributes[host.params[TupleComponents.ruin]] = host.ruin
        attributes[host.params[TupleComponents.ruir]] = host.ruir
        attributes[host.params[TupleComponents.tr]] = host.tr
        return attributes

    def visit_ntoc(self, host:NtoCTuple):
        attributes = {}
        attributes[host.params[TupleComponents.polarity]] = host.polarity
        attributes[host.params[TupleComponents.r]] = host.r
        attributes[host.params[TupleComponents.ruics]] = host.ruics
        attributes[host.params[TupleComponents.ruin]] = host.ruin
        attributes[host.params[TupleComponents.code]] = host.code
        attributes[host.params[TupleComponents.tr]] = host.tr
        return attributes

    def visit_ntode(self, host:NtoDETuple):
        attributes = {}
        attributes[host.params[TupleComponents.polarity]] = host.polarity
        attributes[host.params[TupleComponents.ruin]] = host.ruin
        attributes[host.params[TupleComponents.data]] = host.data
        attributes[host.params[TupleComponents.ruidt]] = host.ruidt
        return attributes

    def visit_ntolackr(self, host:NtoLackRTuple):
        attributes = {}
        attributes[host.params[TupleComponents.r]] = host.r
        attributes[host.params[TupleComponents.ruin]] = host.ruin
        attributes[host.params[TupleComponents.ruir]] = host.ruir
        attributes[host.params[TupleComponents.tr]] = host.tr
        return attributes
