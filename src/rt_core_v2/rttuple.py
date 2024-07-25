import enum
from abc import ABC, abstractmethod

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
    type = "type"
    ar = "ar"
    ruip = "ruip"
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


class RtTuple(ABC):
    """Abstract Referent Tracking tuple that contains the information that all referent tracking tuples contain

    Attributes:
    ruit -- The rui of this tuple
    type -- The id of the tuple component
    """

    tuple_type = None
    params = {**enum_to_dict({TupleComponents.ruit, TupleComponents.type})}

    def __init__(self, rui: Rui = None):
        self._rui = rui if rui else Rui()

    @property
    def ruit(self):
        """Get the rui identifying this RtTuple"""
        return self._rui

    @ruit.setter
    def ruit(self, ruit):
        """Set the rui identifying this RtTuple"""
        self._rui = ruit

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    @abstractmethod
    def get_attributes(self) -> dict:
        """Get the attributes of this tuplestring"""
        return {
            self.params[TupleComponents.ruit]: self._rui,
            self.params[TupleComponents.type]: self.tuple_type,
        }


class ATuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a PoR

    Attributes:
    ar -- The status of ruip
    ruip -- The Rui that is being assigned for the first time
    ruia -- The Rui of the author of this ATuple
    unique -- Asserts whether this is a non-repeatable or repeatable portion of reality
    t -- The time of the creation of the ATuple
    """

    params = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ar,
                TupleComponents.t,
                TupleComponents.ruia,
                TupleComponents.unique,
                TupleComponents.ruip,
            }
        ),
    }
    tuple_type = TupleType.A

    def __init__(
        self,
        ruit: Rui = None,
        ruia: Rui = None,
        ruip: Rui = None,
        ar: RuiStatus = RuiStatus.assigned,
        unique: PorType = PorType.singular,
        t: TempRef = None,
    ):
        super().__init__(ruit)
        self.ar = ar

        # If we don't get an author Rui for the tuple, then autogenerate one,
        # unless we don't get a Ruip either, in which case set it to the
        # autogenerated Ruip.
        # This means that the default behavior is that if neither Ruia nor Ruip
        # are provided, we are assuming some entity is assigning a Ruip to
        # itself, and thus should be equal
        self.ruia = ruia if ruia else (Rui() if ruip else (ruip := Rui()))
        self.ruip = ruip if ruip else Rui()
        self.unique = unique
        self.t = t if t else TempRef()

    def is_assigned(self):
        """Returns whether this tuple is an assignment or not"""
        return self.ar is RuiStatus.assigned

    def is_reserved(self):
        """Returns whether this tuple is a reservation or not"""
        return self.ar is RuiStatus.reserved

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.ruia]] = self.ruia
        attributes[self.params[TupleComponents.ruip]] = self.ruip
        attributes[self.params[TupleComponents.ar]] = self.ar
        attributes[self.params[TupleComponents.unique]] = self.unique
        attributes[self.params[TupleComponents.t]] = self.t
        return attributes


class DTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the instantation of other tuple types

    Attributes:
    ruit_ref -- The ruit of another tuple that this tuple stores information about
    event -- The category of reason that caused the creation of tuple ruit_ref
    event_reason -- The reason for the event above occuring
    td -- The time of this tuple's creation
    replacements -- Any tuples that will be replaced by ruit (if there are any)
    """

    # D#< RUId, RUIT, t, ‘I’/E, R, S >

    tuple_type = TupleType.D
    params = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ruid,
                TupleComponents.event,
                TupleComponents.event_reason,
                TupleComponents.t,
                TupleComponents.replacements,
            }
        ),
    }

    def __init__(
        self,
        ruit: Rui,
        t: TempRef,
        event: TupleEventType,
        event_reason: RtChangeReason,
        ruid: Rui = None,
        replacements: list[Rui] = None,
    ):
        super().__init__(ruid)
        self.ruit_ref = ruit
        self.event = event
        self.event_reason = event_reason
        self.td = t if t else TempRef()
        self.replacements = replacements.copy() if replacements else []

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = {}
        attributes[self.params[TupleComponents.type]] = self.tuple_type.value
        attributes[self.params[TupleComponents.ruid]] = self.ruid
        attributes[self.params[TupleComponents.ruit]] = self.ruit_ref
        attributes[self.params[TupleComponents.event]] = self.event.value
        attributes[self.params[TupleComponents.event_reason]] = self.event_reason.value
        attributes[self.params[TupleComponents.t]] = self.td
        attributes[self.params[TupleComponents.replacements]] = self.replacements
        return attributes

    @property
    def ruid(self):
        return self.ruit

    @ruid.setter
    def ruid(self, ruid):
        self.ruit = ruid


class FTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the confidence level in another tuple's assertions

    Attributes:
    ruid -- The ruid of this tuple
    ruia -- The ruid of the author making the assertion
    ruit_ref -- The ruid of the tuple refered to by this tuple's confidence assertion.
    ta -- The time instance of the confidence assertion.
    C -- The level of confidence from 0.00-1.00 in the assertion.
    """

    # F#< RUId, ta, RUIa, RUIT, C >

    tuple_type = TupleType.F
    params = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.ruid,
                TupleComponents.ruia,
                TupleComponents.ta,
                TupleComponents.C,
            }
        ),
    }

    def __init__(
        self,
        ruid: Rui = None,
        ruit: Rui = None,
        ta: TempRef = None,
        ruia: Rui = None,
        C: float = 1.0,
    ):
        super().__init__(ruid)
        self.ruit_ref = ruit if ruit else Rui()
        self.ruia = ruia if ruia else Rui()
        self.ta = ta
        self.C = C

    def get_attributes(self):
        """Get the attributes of this tuple"""
        attributes = {}
        attributes[self.params[TupleComponents.type]] = self.tuple_type.value
        attributes[self.params[TupleComponents.ruid]] = self.ruid
        attributes[self.params[TupleComponents.ruit]] = self.ruit_ref
        attributes[self.params[TupleComponents.ruia]] = self.ruia
        attributes[self.params[TupleComponents.ta]] = self.ta
        attributes[self.params[TupleComponents.C]] = self.C

        return attributes

    @property
    def ruid(self):
        return self.ruit

    @ruid.setter
    def ruid(self, ruid):
        self.ruit = ruid


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
    tuple_type = TupleType.NtoN
    params = {
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

    def __init__(
        self,
        ruit: Rui = None,
        polarity: bool = True,
        r: str = "",
        p: list[Rui] = None,
        tr: TempRef = None,
    ):
        super().__init__(ruit)
        self.polarity = polarity
        self.relation = r
        self.p_list = p.copy() if p else []
        self.time = tr

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.r]] = self.relation
        attributes[self.params[TupleComponents.p_list]] = self.p_list
        attributes[self.params[TupleComponents.tr]] = self.time
        return attributes


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

    tuple_type = TupleType.NtoR
    params = {
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

    def __init__(
        self,
        ruit: Rui = None,
        polarity: bool = True,
        inst: str = "",
        ruin: Rui = None,
        ruir: Rui = None,
        tr: TempRef = None,
    ):
        super().__init__(ruit)
        self.polarity = polarity
        self.inst = inst
        self.ruin = ruin if ruin else Rui()
        self.ruir = ruir if ruir else Rui()
        self.time = tr

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.inst]] = self.inst
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.ruir]] = self.ruir
        attributes[self.params[TupleComponents.tr]] = self.time
        return attributes


# TODO Use concepts
class NtoCTuple(RtTuple):
    """Tuple type that annotates a non-repeatable portion of reality with a "concept" code from a
    concept-based system

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    relation -- The relationship between the non-repeatable PoR and the concept
    ruics -- The Rui of the concept class the concept for the relation is from
    ruip -- The Rui of the non-repeatable PoR in the relation
    code -- The code for the concept within the concept class referred to by Ruics
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoC#< ‘+’/‘-’, r, RUIcs, RUIp, code, tr >

    tuple_type = TupleType.NtoC
    params = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.polarity,
                TupleComponents.r,
                TupleComponents.ruics,
                TupleComponents.ruip,
                TupleComponents.code,
                TupleComponents.tr,
            }
        ),
    }

    # TODO Change code to be bytecode
    # TODO Make creating a tempref create an underlying time instance
    def __init__(
        self,
        ruit: Rui = None,
        polarity: bool = True,
        r: str = "",
        ruics: Rui = None,
        ruip: Rui = None,
        code: str = "",
        tr: TempRef = None,
    ):
        super().__init__(ruit)
        self.polarity = polarity
        self.reason = r
        self.ruics = ruics if ruics else Rui()
        self.ruip = ruip if ruip else Rui()
        self.code = code
        self.time = tr

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.r]] = self.reason
        attributes[self.params[TupleComponents.ruics]] = self.ruics
        attributes[self.params[TupleComponents.ruip]] = self.ruip
        attributes[self.params[TupleComponents.code]] = self.code
        attributes[self.params[TupleComponents.tr]] = self.time
        return attributes


# We use NtoDE instead of NtoI, and we use an instance for the identifying descriptor
# or IdD associated with:
# (1) and NtoRTuple tuple that says what type of IdD it is,
# (2) an NtoNTuple tuple to relate the name to what the IdD denotes, and
# (3) an NtoDE tuple to hold the actual written (or "string") form of the IdD.
# Note that an IdD can be a name, identifier, etc.
# TODO Figure out if data should be a string or generic data
class NtoDETuple(RtTuple):
    """Tuple type that creates a connection between a non-repeatable portion of reality and a piece of data

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    ruin -- The Rui of the tuple that the data is atrributed to
    data -- The data in the relationship
    ruidt -- An Rui containing the data type of data
    """

    # NtoDE#< '+/-', r, ruin, data, ruidt>

    tuple_type = TupleType.NtoDE
    params = {
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

    def __init__(
        self,
        ruit: Rui = None,
        polarity: bool = True,
        ruin: Rui = None,
        data="",
        ruidt: Rui = None,
    ):
        super().__init__(ruit)
        self.polarity = polarity
        self.ruin = ruin if ruin else Rui()
        self.data = data
        self.ruidt = ruidt if ruidt else Rui()

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.polarity]] = self.polarity
        attributes[self.params[TupleComponents.ruin]] = self.ruin
        attributes[self.params[TupleComponents.data]] = self.data
        attributes[self.params[TupleComponents.ruidt]] = self.ruidt
        return attributes


class NtoLackRTuple(RtTuple):
    """Tuple type that asserts that a repeatable portion of reality in a does not have a specified relationship with a non-repeateble portion of reality

    Attribtues:
    relation -- A relationship between a non-repeatable portion of reality and a repeatable portion of reality
    ruip -- The rui of the repeatable portion of reality that the non-repeatable does not have the relation to
    ruir -- The rui of the non-repeatable portion fo reality that does not have relation to the POR refered to buy ruip
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoRTuple(-) -tuple NtoRTuple(-)#< r, RUIp, RUIr, rT/‘-’, tr/‘-’ >

    tuple_type = TupleType.NtoLackR
    params = {
        **RtTuple.params,
        **enum_to_dict(
            {
                TupleComponents.r,
                TupleComponents.ruip,
                TupleComponents.ruir,
                TupleComponents.tr,
            }
        ),
    }

    def __init__(
        self,
        ruit: Rui = None,
        r: str = "",
        ruip: Rui = None,
        ruir: Rui = None,
        tr: TempRef = None,
    ):
        super().__init__(ruit)
        self.relation = r
        self.ruip = ruip if ruip else Rui()
        self.ruir = ruir if ruir else Rui()
        self.time = tr

    def get_attributes(self):
        """Get the attributes of this tuplestring"""
        attributes = super().get_attributes()
        attributes[self.params[TupleComponents.r]] = self.relation
        attributes[self.params[TupleComponents.ruip]] = self.ruip
        attributes[self.params[TupleComponents.ruir]] = self.ruir
        attributes[self.params[TupleComponents.tr]] = self.time
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
