from rtt_meta.metadata_accessory import TupleEventType, RtChangeReason, RtErrorCode, pretty_print_dict, description_dict

print(TupleEventType.INSERT, "\t", pretty_print_dict[TupleEventType.INSERT])
print()

print(RtChangeReason.REALITY, "\t", pretty_print_dict[RtChangeReason.REALITY])
print()

print(RtErrorCode.R08, '\t', pretty_print_dict[RtErrorCode.R08], '\t', description_dict[RtErrorCode.R08])
print()
