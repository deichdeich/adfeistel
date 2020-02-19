# adfeistel
a simple python implementation of a feistel cipher

This implements a [Feistel cipher](https://en.wikipedia.org/wiki/Feistel_cipher).
It uses [BLAKE2](https://en.wikipedia.org/wiki/BLAKE_(hash_function)#BLAKE2) for hashing.

Here's an example of how to use it:
    import adfeistel as adf
    
    # make a feistel tree.  There will be one layer for every key you feed it.
    # keys must be in byte format.  This will create a 5-layer tree.
    tree = adf.feistel_tree([b'key1', b'key2', b'key3', b'key4',b'key5'])
    
    # use this tree to encrypt some data.  data is fed by splitting
    # up a string into "left" and "right" chunks, in a two-element list.
    data = ['the quick brown fox', 'jumped over the lazy dog']
    enc_data = tree.encrypt(data)

Now, the data looks like:
    
    > enc_data
    > [2610359756959841746523587404182352204913552772592159715175,
      4581578091725372066546928414116855508860183701314820371272362536470986268788830262663067028190021218995331144214932629665236000629857756153425214966934875]

To decrypt, do

    > tree.decrypt(enc_data)
    > ['the quick brown fox', 'jumped over the lazy dog']

To see what each layer is doing, include `verbose = True` at initialization of the tree.
