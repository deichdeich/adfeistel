import hashlib

class feistel_layer(object):
    def __init__(self, hashkey, verbose = False):
        self.hashkey = hashkey
        self.verbose = verbose
        self.is_str = False

    def encrypt(self, leftright):
        
        left, right = leftright
        
        if self.verbose:
            print(f'\t Left input: {left}', flush = True)
            print(f'\t Right input: {right}', flush = True)
        
        # convert stings to decimals
        if type(left) and type(right) is str:
            self.is_str = True
            left = str_to_dec(left)
            right = str_to_dec(right)

        # get a new hash instance
        h = hashlib.blake2b(key = self.hashkey)
        
        # hash the right side
        right_bytes = int_to_bytes(right)
        h.update(right_bytes)

        # xor the right hash with the left side
        righthash = int.from_bytes(h.digest(), 'big')
        newright = left ^ righthash

        if self.verbose:
            print(f'\t Left output: {right}', flush = True)
            print(f'\t Right output: {newright}\n', flush = True)
        
        return([right, newright])


class feistel_tree(object):
    def __init__(self, keys, verbose = False):
        self.nlayers = len(keys)
        self.keys = keys
        self.verbose = verbose
        self.treelist = self.make_tree()

    """ make_tree adds a new feistel layer for every key in the key list
    """
    def make_tree(self):
        treelist = []
        for layer in range(self.nlayers):
            key = self.keys[layer]
            treelist.append(feistel_layer(key, self.verbose))
        return(treelist)

    """ encrypt runs through the list of layers, piping the output of one into
    the input of the next. the order parameter is for reversing the order of the
    list, which you want to do when decrypting
    """
    def encrypt(self, leftright, order = 1):
        current_lr = leftright
        for layer in self.treelist[::order]:
            idx = self.treelist.index(layer)
            if self.verbose: print(f'Layer {idx}, key = {self.keys[idx]}:', flush=True)
            current_lr = layer.encrypt(current_lr)
        return(current_lr)

    """ decrypt just calls encrypt but in reverse order
    """
    def decrypt(self, leftright, is_str = True):
        rightleft = leftright[::-1]
        orig = self.encrypt(rightleft, order=-1)[::-1]
        if is_str:
            orig = [dec_to_str(i) for i in orig]
        return(orig)


def str_to_dec(string):
    string_bytes = bytes(string, 'utf8')
    string_int = int.from_bytes(string_bytes, 'big')
    return(string_int)

def dec_to_str(decimal):
    length = len(str(decimal))
    byte_number = (length - 1)/2 - 1 if length%2 else (length/2) -1
    binary_array = decimal.to_bytes(int(byte_number), 'big')
    ascii_txt = binary_array.decode('utf8')
    return(ascii_txt)

def int_to_bytes(ingr):
    length = len(str(ingr))
    return(ingr.to_bytes(int(length),'big'))

