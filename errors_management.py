from AES import *
from random import randrange

############ Errors management ############

# Input : state - one intermediate state during the AES algorithm, at any time (not only at the beginning of a round),
#                 as a python list of size 16, with values in range (0, 255)
#         i - the state is interpreted as a matrix, this parameter in the line; an integer between 0 and 3
#         j - the state is interpreted as a matrix, this parameter in the column; an integer between 0 and 3
#         val - the value of the fault injected
# Output : nothing
# Return : nothing
# Purpose : set a fault in a state of the AES algorithm (for the attack to be successful, the fault has to be injected
# just before the mixColumns of the 9^th round of AES (the last round does not have a mixColumns)
def setError(state, i, j, val):
    state[i*line_length+j] = val

# Input : state - one intermediate state during the AES algorithm, at any time (not only at the beginning of a round),
#                 as a python list of size 16, with values in range (0, 255)
#         i - the state is interpreted as a matrix, this parameter in the line; an integer between 0 and 3
#         j - the state is interpreted as a matrix, this parameter in the column; an integer between 0 and 3
#         val - the value of the fault injected to be xored with the current value
# Output : nothing
# Return : nothing
# Purpose : set a fault in a state of the AES algorithm (for the attack to be successful, the fault has to be injected
# just before the mixColumns of the 9^th round of AES (the last round does not have a mixColumns)
def setErrorXOR(state, i, j, val):
    state[i*line_length+j] = state[i*line_length+j]^val

# Input : state - one intermediate state during the AES algorithm, at any time (not only at the beginning of a round),
#                 as a python list of size 16, with values in range (0, 255)
#         i - the state is interpreted as a matrix, this parameter in the line; an integer between 0 and 3
#         j - the state is interpreted as a matrix, this parameter in the column; an integer between 0 and 3
# Output : nothing
# Return : nothing
# Purpose : set a random fault in a state of the AES algorithm (for the attack to be successful, the fault has to be injected
# just before the mixColumns of the 9^th round of AES (the last round does not have a mixColumns)
def setErrorRdm(state, i, j):
    f = randrange(0,256,1)
    state[i*line_length+j] = f
    
# Input : plaintext - the plaintext to cipher
#                     as a python list of size 16, with values in range (0, 255)
#         mainkey - the main key of the AES algorithm
#         loc - the localisation of the error
# Output : nothing
# Return : the faulty ciphertext
# Purpose : set a fault on the state, just after the Shift Rows (so just before the Mix Columns) operation of the 9^th round
# the fault has the effect to inverse every bits of the byte targeted
def setFault(plaintext, mainkey, loc, numRounds=10):
    AES_but_last_2_rounds(plaintext, mainkey)
    subBytes(plaintext)
    shiftRows(plaintext)
    setErrorXOR(plaintext, loc/4, loc%4, 0xff)
    mixColumns(plaintext)
    expandedKey = expandKey(mainkey)
    roundKey = createRoundKey(expandedKey, numRounds-1)
    addRoundKey(plaintext, roundKey)
    subBytes(plaintext)
    shiftRows(plaintext)
    roundKey = createRoundKey(expandedKey, numRounds)
    addRoundKey(plaintext, roundKey)
    return plaintext

# Input : plaintext - the plaintext to cipher
#                     as a python list of size 16, with values in range (0, 255)
#         mainkey - the main key of the AES algorithm
#         loc - the localisation of the error
# Output : nothing
# Return : the faulty ciphertext
# Purpose : The same as the previous function, but the fault injected is randomly chosen
def setFaultRdm(plaintext, mainkey, loc, numRounds=10):
    AES_but_last_2_rounds(plaintext, mainkey)
    subBytes(plaintext)
    shiftRows(plaintext)
    setErrorRdm(plaintext, loc/4, loc%4)
    mixColumns(plaintext)
    expandedKey = expandKey(mainkey)
    roundKey = createRoundKey(expandedKey, numRounds-1)
    addRoundKey(plaintext, roundKey)
    subBytes(plaintext)
    shiftRows(plaintext)
    roundKey = createRoundKey(expandedKey, numRounds)
    addRoundKey(plaintext, roundKey)
    return plaintext

# Input : plaintext - the plaintext to cipher
#                     as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16, with values in range (0, 255)
#         loc - the localisation of the error, an integer between 0 and 15
# Output : nothing
# Return : the faulty ciphertext and the "normal" ciphertext, as two python lists of size 16, with values in range (0, 255)
# Purpose : this function computes and return a couple of ciphertexts : the normal and the faulty ciphertexts
# with the help of the previous function for the faulty one
def createCouple(plaintext, key, loc):
    plaincopy = copy(plaintext)
    faultedCiph = setFault(plaincopy, key, loc)
    realCiph = AES(plaintext, key)
    return realCiph, faultedCiph

# Input : plaintext - the plaintext to cipher
#                     as a python list of size 16, with values in range (0, 255)
#         key - the main key of the AES algorithm, as a python list of size 16, with values in range (0, 255)
#         loc - the localisation of the error, an integer between 0 and 15
# Output : nothing
# Return : the faulty ciphertext and the "normal" ciphertext, as two python lists of size 16, with values in range (0, 255)
# Purpose : The same as the previous function but with a random fault injected
def createCoupleWithRdm(plaintext, key, loc):
    plaincopy = copy(plaintext)
    faultedCiph = setFaultRdm(plaincopy, key, loc)
    realCiph = AES(plaintext, key)
    return realCiph, faultedCiph

# Input : C - the ciphertext
#             as a python list of size 16, with values in range (0, 255)
#         C_f - the faulty ciphertext
#               as a python list of size 16, with values in range (0, 255)
# Output : nothing
# Return : a list of size 4
# Purpose : this function returns the list of the 4 indices such as C[i] and C_f[i] are different
def nonZeroIndices(C, C_f):
    l = []
    for i in range(len(C)):
        if ((C[i] ^ C_f[i]) != 0x00):
            l = l + [i]
    return l
