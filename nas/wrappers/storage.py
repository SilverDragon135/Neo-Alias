from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import concat, range


class Storage:
    """
    Simplifies access to storage apis
    """
    ctx = GetContext()

    def load(self, key):
        """
        :param key:
        :returns value:
        """
        return Get(self.ctx, key)

    def save(self, key, value):
        """
        :param key:
        :param value:
        """
        Put(self.ctx, key, value)

    def delete(self, key):
        """
        :param key:
        """
        Delete(self.ctx, key)

    def deserialize_bytearray(self, data):
        """
        :param data:
        \n:returns deserialized data as array:
        \nDeserializes bytearray to array
        """
        # get length of length
        collection_length_length = data[0:1]

        # get length of collection
        collection_len = data[1:collection_length_length + 1]

        # create a new collection
        new_collection = list(length=collection_len)

        # trim the length data
        offset = 1 + collection_length_length

        for i in range(0, collection_len):

            # get the data length length
            itemlen_len = data[offset:offset + 1]

            # get the length of the data
            item_len = data[offset + 1:offset + 1 + itemlen_len]

            # get the data
            item = data[offset + 1 + itemlen_len: offset + 1 + itemlen_len + item_len]

            # store it in collection
            new_collection[i] = item

            offset = offset + item_len + itemlen_len + 1

        return new_collection

    def serialize_array(self, items):
        """
        :param items:
        \n:returns serialized items as bytearray:
        \nSerializes array to bytearray
        """
        # serialize the length of the list
        itemlength = self.serialize_var_length_item(items)

        output = itemlength

        # now go through and append all your stuff
        for item in items:

            # get the variable length of the item
            # to be serialized
            itemlen = self.serialize_var_length_item(item)

            # add that indicator
            output = concat(output, itemlen)

            # now add the item
            output = concat(output, item)

        # return the stuff
        return output

    def serialize_var_length_item(self, item):
        """
        :param item:
        \n:returns serialized var lenth item:
        \nserializes length of item
        """
        # get the length of your stuff
        stuff_len = len(item)

        # now we need to know how many bytes the length of the array
        # will take to store

        # for storing empty items in array we have to use zero byte
        if stuff_len == 0:
            byte_len = b'\x00'
        # this is one byte
        elif stuff_len <= 255:
            byte_len = b'\x01'
        # two byte
        elif stuff_len <= 65535:
            byte_len = b'\x02'
        # hopefully 4 byte
        else:
            byte_len = b'\x04'

        out = concat(byte_len, stuff_len)

        return out
