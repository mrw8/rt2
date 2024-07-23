from rt_core_v2.metadata_accessory import (
    TupleEventType,
    RtChangeReason,
    pretty_print_dict,
    description_dict,
)

print(TupleEventType.INSERT, "\t", pretty_print_dict[TupleEventType.INSERT])
print()

print(RtChangeReason.REALITY, "\t", pretty_print_dict[RtChangeReason.REALITY])
print()

print(
    RtChangeReason.R08,
    "\t",
    pretty_print_dict[RtChangeReason.R08],
    "\t",
    description_dict[RtChangeReason.R08],
)
print()
