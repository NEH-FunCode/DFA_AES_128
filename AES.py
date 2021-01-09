from copy import copy

sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]

# s-box inverse

sboxInv = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]

# rcon table for key exapnsion

rcon = [
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb
]

statesize=16
column_length = 4
line_length = 4

# Input : state - a python list of size 16,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
#                 example : [0,11,247,3,47,58,63,70,78,29,140,101,12,123,114,150]
# Output : print the state
# Return : nothing
def printState(state):
    line = []
    for i in range(line_length):
        for j in range(column_length):
            line = line + [hex(state[i*4+j])]
        print line
        print '\n'
        line = []

# Input : l - a python state of size 16,
#                 with values in range (0, 255)
# Output : nothing
# Return : a list of size 16, with values in range (0, 255)
# Purpose : starting from a list, the state for the AES algorithm often
#           is interpreted as the following matrix :
#           [0,1,2,3
#            4,5,6,7
#            8,9,10,11
#            12,13,14,15]
# but sometimes the representation is :
#           [0,4,8,12
#            1,5,9,13
#            2,6,10,14
#            3,7,11,15]
# this function modifies the state from the first representation
# to the second one.
def list2state(l):
    length = len(l)
    s = [0] * length
    for i in range(4):
        for j in range(4):
            s[4*i+j] = l[i+4*j]
    return s

############ subBytes ############

# Input : state - a python list of size 16,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
# Output : nothing
# Return : nothing
# Purpose : preforms the AES sub-bytes transformation on the input state
def subBytes(state):
    for i in range(statesize):
        state[i] = sbox[state[i]]


# Input : state - a python list of size 16,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
# Output : nothing
# Return : nothing
# Purpose : preforms the inverse sub-bytes transformation on the input state
def subBytesInv(state):
    for i in range(statesize):
        state[i] = sboxInv[state[i]]


############ ShiftRows ############

# Input : word - a python list of size 4,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
# Output : nothing
# Return : the new word
# Purpose : perform a cyclic rotation of n elements to the left
def rotate(word, n):
    return word[n:]+word[0:n]

# Input : state - a python list of size 16,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
# Output : nothing
# Return : nothing
# Purpose : perform the AES shift rows on the input state
def shiftRows(state):
    for i in range(4):
        state[i*4:i*4+4] = rotate(state[i*4:i*4+4],i)


# Input : state - a python list of size 16,
#                 with values in range (0 (or 0x00 in hexa), 255 (0xFF))
# Output : nothing
# Return : nothing
# Purpose : perform the inverse AES shift rows on the input state
def shiftRowsInv(state):
    for i in range(4):
        state[i*4:i*4+4] = rotate(state[i*4:i*4+4],-i)

############ MixColumns ############

# Input : a - an integer
#         b - an integer
# Output : nothing
# Return : the result of the Galois multiplication between a and b
# Purpose : useful for the mixColumn transformation
def galoisMult(a, b):
    p=0
    hiBitSet=0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

# Input : col - a column of an AES state as a python list of size 4,
#                 with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : perform the mixColumn transformation of the AES on a column
def mixColumn(col):
    temp = copy(col)
    col[0] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
    col[1] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
    col[2] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
    col[3] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],3)

# Input : state - a state of the AES as a python list of size 16,
#                 with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : perform the mixColumn transformation of the AES on the full input state
def mixColumns(state):
    for i in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j*4+i])

        # apply mixColumn on our virtual column
        mixColumn(column)

        # transfer the new values back into the state table
        for j in range(4):
            state[j*4+i] = column[j]

# Input : column - a column of an AES state as a python list of size 4,
#                 with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : perform the inverse mixColumn transformation of the AES on a column
def mixColumnInv(column):
    temp = copy(column)
    column[0] = galoisMult(temp[0],14) ^ galoisMult(temp[3],9) ^ galoisMult(temp[2],13) ^ galoisMult(temp[1],11)
    column[1] = galoisMult(temp[1],14) ^ galoisMult(temp[0],9) ^ galoisMult(temp[3],13) ^ galoisMult(temp[2],11)
    column[2] = galoisMult(temp[2],14) ^ galoisMult(temp[1],9) ^ galoisMult(temp[0],13) ^ galoisMult(temp[3],11)
    column[3] = galoisMult(temp[3],14) ^ galoisMult(temp[2],9) ^ galoisMult(temp[1],13) ^ galoisMult(temp[0],11)

# Input : state - a state of the AES as a python list of size 16,
#                 with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : perform the mixColumn inverse transformation of the AES on the full input state
def mixColumnsInv(state):
    for i in range(4):
        column = []
        # create the column by taking the same item out of each "virtual" row
        for j in range(4):
            column.append(state[j*4+i])

        # apply mixColumn on our virtual column
        mixColumnInv(column)

        # transfer the new values back into the state table
        for j in range(4):
            state[j*4+i] = column[j]
            

############ AddRoundKey ############

# Input : state - a state of the AES as a python list of size 16,
#                 with values in range (0, 255)
#         roundKey - the AES round key as a python list of size 16,
#                    with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : perform the AddRoundKey transformation of the AES on the input state,
# by XOR-ing each byte of the roundKey with the state
# no need of a specific function for the inverse transformation of ARK,
# the inverse operation of XOR being XOR itself
def addRoundKey(state, roundKey):
    for i in range(statesize):
        state[i] = state[i] ^ roundKey[i]

############ KeyExpansion ############

# Input : word - a python list of size 4,
#                with values in range (0, 255)
#         i - an integer between 0 and the length value of the rcon table
# Output : nothing
# Return : nothing
# Purpose : this function is a part of the KeyExpansion operation of the AES
def keyScheduleCore(word, i):
    word = rotate(word, 1)
    newWord = []
    for byte in word:
        newWord.append(sbox[byte])
    newWord[0] = newWord[0]^rcon[i]
    return newWord

# Input : cipherKey - the main key of the AES algorithm, as a python list of size 16,
#                     with values in range (0, 255)
# Output : nothing
# Return : the 11 round keys of the AES 128 as a python list of size 11*16 = 176
# (the round 0 consists of a simple XOR with the main key,
# therefore the main key is at the beginning of the returned list)
# Purpose : this function performs the KeyExpansion operation of the AES
def expandKey(cipherKey):
    cipherKeySize = len(cipherKey)
    assert cipherKeySize == 16
    # container for expanded key
    expandedKey = []
    currentSize = 0
    rconIter = 1
    # temporary list to store 4 bytes
    t = [0,0,0,0]

    #copy the first 16 bytes of the cipher key to the expanded key
    for i in range(cipherKeySize):
        expandedKey.append(cipherKey[i])
    currentSize += cipherKeySize

    # generate the remaining bytes until we get a total key size of 176
    while (currentSize < 176):
        # assign previous 4 bytes to the temporary storage t
        t = expandedKey[currentSize-4:currentSize]
        if ((currentSize % cipherKeySize) == 0):
            t = keyScheduleCore(t, rconIter)
            rconIter += 1
        for m in range(4):
            expandedKey.append(((expandedKey[currentSize - cipherKeySize]) ^ (t[m])))
            currentSize += 1
            
    return expandedKey

# Input : expandedKey - the expanded key of the AES algorithm, as a python list of size 176,
#                       with values in range (0, 255)
#         n - the round number (from 0 to 10)
# Output : nothing
# Return : the key of the round number n
# Purpose : see above
def createRoundKey(expandedKey, n):
    return expandedKey[(n*16):(n*16+16)]
        
# Input : lastk - the last round key, as a python list of size 16,
#                 with values in range (0, 255)
# Output : nothing
# Return : the main key of the AES algorithm
# Purpose : find the main key from the retrieved last round key
def find_main_key_from_last_key(lastk):
    ind = 43
    w = [0,0,0,0]
    tmp = [0,0,0,0]
    mainK = [-1 for i in range(16)]
    keys = [[-1 for i in range(4)] for j in range(44)]
    for i in range(4, 0, -1):
        for j in range((i-1)*4, i*4, 1):
            keys[ind][j-(i-1)*4] = lastk[j]
        ind = ind - 1
    for i in range(39,-1,-1):
        w = keys[i+3]
        for j in range(4):
            keys[i][j] = keys[i+4][j] ^ w[j]
        if ((i % 4) == 0):
            tmp[0] = sbox[w[1]] ^ rcon[i/4 + 1]
            tmp[1] = sbox[w[2]] 
            tmp[2] = sbox[w[3]] 
            tmp[3] = sbox[w[0]] 
            for j in range(4):
                keys[i][j] = keys[i+4][j] ^ tmp[j]
    k = 0
    for i in range(4):
        for j in range(4):
            mainK[k] = keys[i][j]
            k = k+1
    return mainK
        

############ One Round of AES ############

# Input : state - one intermediate state at the beginning of a round during the whole AES algorithm,
#                 as a python list of size 16, with values in range (0, 255)
#         roundKey - the key associated with the round to compute, as a python list of size 16,
#                    with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : compute one round of the AES with the associated round key
def aesRound(state, roundKey):
    subBytes(state)
    shiftRows(state)
    mixColumns(state)
    addRoundKey(state, roundKey)


############ Full AES ############

# Input : state - the input plaintext to cipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16,
#               with values in range (0, 255)
# Output : nothing
# Return : the final ciphertext
# Purpose : compute the whole AES algorithm
def AES(state, key, numRounds=10):
    expandedKey = expandKey(key)
    roundKey = createRoundKey(expandedKey, 0)
    addRoundKey(state, roundKey)
    for i in range(1, numRounds):
        roundKey = createRoundKey(expandedKey, i)
        aesRound(state, roundKey)
    # final round : no MixColumns
    roundKey = createRoundKey(expandedKey, numRounds)
    subBytes(state)
    shiftRows(state)
    addRoundKey(state, roundKey)
    return state

# Input : state - the input plaintext to cipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16,
#               with values in range (0, 255)
# Output : nothing
# Return : the final ciphertext
# Purpose : compute the whole AES algorithm,
# but with the input plaintext being interpreted differently (see list2state function)
def AES_other_POV(state, key, numRounds=10):
    state = list2state(state)
    expandedKey = expandKey(key)
    roundKey = list2state(createRoundKey(expandedKey, 0))
    addRoundKey(state, roundKey)
    for i in range(1, numRounds):
        roundKey = list2state(createRoundKey(expandedKey, i))
        aesRound_no_graphic(state, roundKey)
    # final round : no MixColumns
    roundKey = list2state(createRoundKey(expandedKey, numRounds))
    subBytes(state)
    shiftRows(state)
    addRoundKey(state, roundKey)
    return state

############ Full AES inverse ############

# Input : state - the input ciphertext to decipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16,
#               with values in range (0, 255)
# Output : nothing
# Return : the initial plaintext
# Purpose : compute the whole AES inverse algorithm
def AESInv(state, key, numRounds=10):
    expandedKey = expandKey(key)
    roundKey = createRoundKey(expandedKey, numRounds)
    addRoundKey(state, roundKey)
    shiftRowsInv(state)
    subBytesInv(state)
    for i in range(numRounds-1, 0, -1):
        roundKey = createRoundKey(expandedKey, i)
        aesRoundInv_no_graphic(state, roundKey)
    roundKey = createRoundKey(expandedKey, 0)
    addRoundKey(state, roundKey)
    return state

############ AES without last round inverse ############

# Input : state - the input ciphertext to decipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16,
#               with values in range (0, 255)
# Output : nothing
# Return : the initial plaintext
# Purpose : compute the whole AES inverse algorithm
def AES_but_last_roundInv(state, key, numRounds=10):
    expandedKey = expandKey(key)
    for i in range(numRounds-1, 0, -1):
        roundKey = createRoundKey(expandedKey, i)
        aesRoundInv(state, roundKey)
    roundKey = createRoundKey(expandedKey, 0)
    addRoundKey(state, roundKey)
    champ_state.config(text = state2str(state, is_hex))
    
############ AES inverse round ############

# Input : state - one intermediate state at the end of a round during the whole AES algorithm,
#                 as a python list of size 16, with values in range (0, 255)
#         roundKey - the key associated with the round to inverse, as a python list of size 16,
#                    with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : compute one inverse round of the AES with the associated round key
def aesRoundInv(state, roundKey):
    addRoundKey(state, roundKey)
    mixColumnsInv(state)
    shiftRowsInv(state)
    subBytesInv(state)
    
############ AES without last round ############

# Input : state - the plaintext to cipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key, as a python list of size 16,
#                    with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : compute the AES algorithm but last round
def AES_but_last_round(state, key, numRounds=10):
    expandedKey = expandKey(key)
    roundKey = createRoundKey(expandedKey, 0)
    addRoundKey(state, roundKey)
    for i in range(1, numRounds):
        roundKey = createRoundKey(expandedKey, i)
        aesRound(state, roundKey)

# Input : state - the plaintext to cipher,
#                 as a python list of size 16, with values in range (0, 255)
#         key - the main key, as a python list of size 16,
#                    with values in range (0, 255)
# Output : nothing
# Return : nothing
# Purpose : compute the AES algorithm but last two rounds
def AES_but_last_2_rounds(state, key, numRounds=10):
    expandedKey = expandKey(key)
    roundKey = createRoundKey(expandedKey, 0)
    addRoundKey(state, roundKey)
    for i in range(1, numRounds-1):
        roundKey = createRoundKey(expandedKey, i)
        aesRound(state, roundKey)
