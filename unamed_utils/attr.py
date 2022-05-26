from hexbytes import HexBytes
from web3.datastructures import AttributeDict

# Example AttributeDict methods
# ['__abstractmethods__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__orig_bases__', '__parameters__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_apply_if_mapping', '_is_protocol', '_repr_pretty_', 'address', 'args', 'blockHash', 'blockNumber', 'event', 'get', 'items', 'keys', 'logIndex', 'recursive', 'transactionHash', 'transactionIndex', 'values']

# Example 0xOG event entry
# AttributeDict({'args': AttributeDict({'from': '0x0000000000000000000000000000000000000000', 'to': '0x0676d673A2a0A13fe37A3EC7812A8cCC571cA07B', 'tokenId': 319}), 'event': 'Transfer', 'logIndex': 1, 'transactionIndex': 0, 'transactionHash': HexBytes('0x9ff5473cb9fb0ebf6acad36bb2bc2778e7b67fc275cc77e0b31dfd958869ab1f'), 'address': '0x5b7622DED96511639DdC12C86eb2703331cA2c78', 'blockHash': HexBytes('0x5f7d35c160af254affbd4286dd8329af257792554dac9bc494dd8f4765dd393f'), 'blockNumber': 14651691})


# Event data from web3 py is in AttributeDict format
# This method is needed for transforming AttributeDict to Python Native Dict so it can be json-serialized
# From 0xOG examples, it does these things
#   - Recursively transform AttributeDict to Dict
#   - encode HexBytes in hex str so it is readable
#   - MORE to be coming if needed
def attr_dict_to_dic(attr_dict):
    res = {}
    for (k, v) in attr_dict.items():
        (res_k, res_v) = (k, v)
        if isinstance(v, AttributeDict):
            res_v = attr_dict_to_dic(v)

        if isinstance(k, HexBytes):
            res_k = k.hex()
        if isinstance(v, HexBytes):
            res_v = v.hex()

        res[res_k] = res_v

    return res