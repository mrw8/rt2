from enum import Enum

class TupleEventType(Enum):
	"""Each metadata or D tuple represents an action taken on another tuple, which can include 
	      (1) insertion of a tuple, (2) marking a tuple as being in error, or 
	      (3) retracting an assertion of being in error"""
	INSERT = 1
	INVALIDATE = 2
	REVALIDATE = 3


class RtChangeReason(Enum):
	"""For each event that a D tuple represents, what is the reason we are doing it?
	     These reasons include:
	       (1) change in belief
	       (2) change in reality
	       (3) change in relevance
	       (4) recognition of an error or mistake"""
	BELIEF = 4
	REALITY = 5
	RELEVANCE = 6
	MISTAKE = 7


class RtErrorCode(Enum):
	A1 = 8
	A2 = 9
	A3 = 10
	A4 = 11
	R01 = 12
	R02 = 13
	R03 = 14
	R04 = 15
	R05 = 16
	R06 = 17
	R07 = 18
	R08 = 19
	R09 = 20
	R10 = 21
	P1 = 22
	P2 = 23
	P3 = 24
	AM1 = 25
	AM2 = 26
	RM1 = 27
	RM2 = 28
	PM1 = 29
	PM2 = 30


pretty_print_dict = {
	TupleEventType.INSERT: "inserting",
	TupleEventType.INVALIDATE: "invalidating",
	TupleEventType.REVALIDATE: "revalidating",
	RtChangeReason.BELIEF: "change in belief",
	RtChangeReason.REALITY: "change in reality",
	RtChangeReason.RELEVANCE: "change in relevance",
	RtChangeReason.MISTAKE: "recognizing a mistake",
	RtErrorCode.A1: "The RUI does not refer",
	RtErrorCode.A2: "The RUI refers to two or more distinct portions of reality",
	RtErrorCode.A3: "The RUI is not the only RUI in the RTS that refers to this portion of reality",
	RtErrorCode.A4: "The RUI does not refer to the intended portion of reality",
	RtErrorCode.R01: "The relationship between the non-repeatable PoR referred to by ruin and the repeatable PoR referred to by ruir does not hold during the stated time period",
	RtErrorCode.R02: " The ruir parameter for the repeatable PoR does not refer to the intended PoR or it refers to no PoR at all",
	RtErrorCode.R03: "There is an A1 error in the corresponding A tuple; therefore the NtoRTuple tuple is nonsensical",
	RtErrorCode.R04: "The ruin parameter is subject to a mistake of type A2, and for at least one of the non-repeatable PoR referred to by it, the stated relationship does not hold",
	RtErrorCode.R05: "The ruin parameter is subject to a mistake of type A3, and the relationship between the non-repeatable PoR and the repeatable PoR does not hold during the stated time period",
	RtErrorCode.R06: "The ruin parameter is subject to a mistake of type A4, and the relationship between the non-repeatable PoR and the repeatable PoR does not hold during the stated time period",
	RtErrorCode.R07: "The ruin parameter is subject to a mistake of type A2, but for ALL the non-repeatable PoR that it refers to, the relationship with the repeatable PoR does not hold during the stated time period",
	RtErrorCode.R08: "The ruin parameter is subject to a mistake of type A3, but the relationship between the non-repeatable PoR it denotes and the repeatable PoR holds during the stated time period",
	RtErrorCode.R09: "The ruin parameter is subject to a mistake of type A4, but the relationship between the non-repeatable PoR it denotes and the repeatable PoR holds during the stated time period",
	RtErrorCode.R10: "There is no A-type error but the stated relationship between the non-repeatable PoR and the repeatable PoR is irrelevant",
	RtErrorCode.P1: "The relationship does not hold among the list of non-repeatable PoR denoted by the RUIs in P",
	RtErrorCode.P2: "One or more of the RUIs in P do not refer to the intended non-repeatable PoR or refer to no non-repeatable PoR at all",
	RtErrorCode.P3: "There is an A1 error in the corresponding A tuple; the NtoNTuple tuple is nonsensical",
	RtErrorCode.AM1: "The existence of a relevant non-repeatable PoR was previously not recognized",
	RtErrorCode.AM2: "The relevance of a non-repeatable PoR to the purpose of the RTS has not been acknowledged, despite knowledge of its existence",
	RtErrorCode.RM1: "The existence of relationship between a non-repeatable PoR and a repeatable PoR was previously not recognized",
	RtErrorCode.RM2: "The relevance of a relationship between a non-repeatable PoR and a repeatable PoR has not been acknowledged, despite knowledge of its existence",
	RtErrorCode.PM1: "The existence of a relationship among a group of non-repeatable PoR was previously not recognized",
	RtErrorCode.PM2: "The relevance of a relationship among a group of non-repeatable PoR has not been acknowledged, despite knowledge of its existence"
}


description_dict = {
	TupleEventType.INSERT: "inserting a tuple into the referent tracking system",
	TupleEventType.INVALIDATE: "invalidating an existing tuple in the referent tracking system as incorporating a mistake",
	TupleEventType.REVALIDATE: "revalidating an existing tuple in the system, which was previously invalidated, and that invalidation was itself a mistake",
	RtChangeReason.BELIEF: "the entity making this update to the system had a change in belief about what is true of reality and is making this update to reflect its change in belief.",
	RtChangeReason.REALITY: "the entity making this update to the system recognized that reality has changed and is making this update to reflect new reality",
	RtChangeReason.RELEVANCE: "the entity making this update to the system changed what it deems relevant to the purposes of the system and is making this update to reflect this change in relevance",
	RtChangeReason.MISTAKE: "the entity making this update recognized a mistake and is updating the system to correct it",
	RtErrorCode.A1: "The RUI that denotes the primary referent of the tuple, typically the ruip parameter, does not refer to any existing entity in reality after all",
	RtErrorCode.A2: "The RUI that denotes the primary referent of the tuple, typically the ruip parameter, refers to two or more numerically distinct portions of reality",
	RtErrorCode.A3: "The RUI that denotes the primary referent of the tuple, typically the ruip parameter, is not the only RUI in the RTS that refers to this portion of reality and the adjudication is to retire and replace it",
	RtErrorCode.A4: "The RUI that denotes the primary referent of the tuple, typically the ruip parameter, does not refer to the portion of reality that was intended but instead refers to some other portion of reality",
	RtErrorCode.R01: "The relationship between the non-repeatable portion of reality referred to by ruin and the repeatable portion of reality referred to by ruir does not hold during the stated time period",
	RtErrorCode.R02: "The ruir parameter for the repeatable portion of reality does not refer to the intended portion of reality or it refers to no portion of reality at all",
	RtErrorCode.R03: "There is an A1 error in the corresponding A tuple (the ruin parameter does not refer to any PoR at all); therefore the NtoRTuple tuple is nonsensical",
	RtErrorCode.R04: "The ruin parameter is subject to a mistake of type A2 and for at least one of the non-repeatable portions of reality referred to by it, the stated relationship to the repeatable portion of reality (denoted by ruir) does not hold",
	RtErrorCode.R05: "The ruin parameter is subject to a mistake of type A3, and the relationship between the non-repeatable portion of reality (denoted by ruin) and the repeatable portion of reality (denoted by ruir) does not hold during the stated time period",
	RtErrorCode.R06: "The ruin parameter is subject to a mistake of type A4, and the relationship between the non-repeatable portion of reality (dentoed by ruin) and the repeatable portion of reality (denoted by ruir) does not hold during the stated time period",
	RtErrorCode.R07: "The ruin parameter is subject to a mistake of type A2, but for ALL the non-repeatable portions of reality that it refers to, the relationship with the repeatable portion of reality (denoted by ruir) does not hold during the stated time period",
	RtErrorCode.R08: "The ruin parameter is subject to a mistake of type A3, but the relationship between the non-repeatable portion of reality it denotes and the repeatable portion of reality (denoted by ruir) holds during the stated time period",
	RtErrorCode.R09: "The ruin parameter is subject to a mistake of type A4, but the relationship between the non-repeatable portion of reality it denotes and the repeatable portion of reality (denoted by ruir) holds during the stated time period",
	RtErrorCode.R10: "There is no A-type error but the stated relationship between the non-repeatable portion of reality and the repeatable portion of reality is irrelevant to the purpose of the system",
	RtErrorCode.P1: "The stated relationship does not hold among the list of non-repeatable portions of reality denoted by the set of RUIs in the P parameter",
	RtErrorCode.P2: "One or more of the RUIs in the set P do not refer to the intended non-repeatable portion of reality or refer to no non-repeatable portion of reality at all",
	RtErrorCode.P3: "There is an A1 error in the corresponding A tuple (one or more of the RUIs in P does not refer at all); therefore the NtoNTuple tuple is nonsensical",
	RtErrorCode.AM1: "The existence of a relevant non-repeatable portion of reality was previously not recognized",
	RtErrorCode.AM2: "The relevance of a non-repeatable PoR to the purpose of the RTS has not been acknowledged, despite knowing of its existence",
	RtErrorCode.RM1: "The existence of relationship between a non-repeatable portion of reality and a repeatable portion of reality was previously not recognized",
	RtErrorCode.RM2: "The relevance of a relationship between a non-repeatable portion of reality and a repeatable portion of reality has not been acknowledged, despite knowledge of its existence",
	RtErrorCode.PM1: "The existence of a relationship among a group of non-repeatable portions of reality was previously not recognized",
	RtErrorCode.PM2: "The relevance of a relationship among a group of non-repeatable PoR has not been acknowledged, despite knowledge of its existence"
}
