from AES import *
from errors_management import nonZeroIndices
# Input : nothing
# Output : nothing
# Return : the result of the computations as a list of dimension 2 : [1020][4]
# Purpose : compute a list of all possible differences between normal and faulty ciphertexts, at the output of the 9th round
# i.e. the 1020 columns of MixColumn(x), where x is a column with hamming weight of 1
def preComputationsColumns():
    preComp = []
    for i in range(1,256,1): # the fault value injected
        for j in range(4): # the location
            col = [0 for k in range(4)]
            col[j % 4] = i
            mixColumn(col)
            preComp = preComp + [col]
    return preComp

# Input : C - a normal ciphertext
#             as a python list of size 16, with values in range (0, 255)
#         C_f - the faulty ciphertext associated with C
#         D - a normal ciphertext
#         D_f - the faulty ciphertext associate with D
# Note : these four ciphertexts / faulty ciphertexts have to be ciphered with the same key
# Output : nothing
# Return : a list of dimension 2 being the list of hypothesis of two bytes
# of the last round key : [n][2] with n the number of hypothesis
def resolveKeyTwoFirstBytes(C, C_f, D, D_f, nZ, pcc):
    possible_values = []
    hyp = []
    for i in range(256):
        for l in range(256):
            CDelta0 = sboxInv[C[nZ[0]]^i] ^ sboxInv[C_f[nZ[0]]^i]
            CDelta1 = sboxInv[C[nZ[1]]^l] ^ sboxInv[C_f[nZ[1]]^l]
            for j in range(len(pcc)):
                if (pcc[j][0] == CDelta0 and pcc[j][1] == CDelta1):
                    DDelta0 = sboxInv[D[nZ[0]]^i] ^ sboxInv[D_f[nZ[0]]^i]
                    DDelta1 = sboxInv[D[nZ[1]]^l] ^ sboxInv[D_f[nZ[1]]^l]
                    for m in range(len(pcc)):
                        if (pcc[m][0] == DDelta0 and pcc[m][1] == DDelta1):
                            hyp = hyp + [i]
                            hyp = hyp + [l]
                            possible_values = possible_values + [hyp]
                            hyp = []
    return possible_values

# Input : C - a normal ciphertext
#             as a python list of size 16, with values in range (0, 255)
#         C_f - the faulty ciphertext associated with C
#         D - a normal ciphertext
# Note : these four ciphertexts / faulty ciphertexts have to be ciphered with the same key
#         D_f - the faulty ciphertext associate with D
#         keys_hyp - the hypothesis that could be two bytes of the last round key, computed by the previous function
# Output : nothing
# Return : a reduced list of dimension 2 being the list of hypothesis
# of three bytes of the last round key : [n][3] with n the number of hypothesis
def extendHypKey3rdByte(C, C_f, D, D_f, keys_hyp, nZ, pcc):
    possible_values = []
    for i in range(256):
        for j in range(len(keys_hyp)):
            new_hyp_key = keys_hyp[j] + [i]
            CDelta0 = sboxInv[C[nZ[0]]^new_hyp_key[0]] ^ sboxInv[C_f[nZ[0]]^new_hyp_key[0]]
            CDelta1 = sboxInv[C[nZ[1]]^new_hyp_key[1]] ^ sboxInv[C_f[nZ[1]]^new_hyp_key[1]]
            CDelta2 = sboxInv[C[nZ[2]]^new_hyp_key[2]] ^ sboxInv[C_f[nZ[2]]^new_hyp_key[2]]
            for k in range(len(pcc)):
                if (pcc[k][0] == CDelta0 and pcc[k][1] == CDelta1 and pcc[k][2] == CDelta2):
                    DDelta0 = sboxInv[D[nZ[0]]^new_hyp_key[0]] ^ sboxInv[D_f[nZ[0]]^new_hyp_key[0]]
                    DDelta1 = sboxInv[D[nZ[1]]^new_hyp_key[1]] ^ sboxInv[D_f[nZ[1]]^new_hyp_key[1]]
                    DDelta2 = sboxInv[D[nZ[2]]^new_hyp_key[2]] ^ sboxInv[D_f[nZ[2]]^new_hyp_key[2]]
                    for m in range(len(pcc)):
                        if (pcc[m][0] == DDelta0 and pcc[m][1] == DDelta1 and pcc[m][2] == DDelta2):
                            possible_values = possible_values + [new_hyp_key]
    return possible_values

# Input : C - a normal ciphertext
#             as a python list of size 16, with values in range (0, 255)
#         C_f - the faulty ciphertext associated with C
#         D - a normal ciphertext
#         D_f - the faulty ciphertext associate with D
# Note : these four ciphertexts / faulty ciphertexts have to be ciphered with the same key
#         keys_hyp - the hypothesis that could be two bytes of the last round key, computed by the previous function
# Output : nothing
# Return : a reduced list of dimension 2 being the list of hypothesis of four bytes of the last round key : [n][4] with n the number of hypothesis,
# n should be equal to 1 here. We normally find here 4 bytes
# of the last round key
def extendHypKey4thByte(C, C_f, D, D_f, keys_hyp, nZ, pcc):
    possible_values = []
    for i in range(256):
        for j in range(len(keys_hyp)):
            new_hyp_key = keys_hyp[j] + [i]
            CDelta0 = sboxInv[C[nZ[0]]^new_hyp_key[0]] ^ sboxInv[C_f[nZ[0]]^new_hyp_key[0]]
            CDelta1 = sboxInv[C[nZ[1]]^new_hyp_key[1]] ^ sboxInv[C_f[nZ[1]]^new_hyp_key[1]]
            CDelta2 = sboxInv[C[nZ[2]]^new_hyp_key[2]] ^ sboxInv[C_f[nZ[2]]^new_hyp_key[2]]
            CDelta3 = sboxInv[C[nZ[3]]^new_hyp_key[3]] ^ sboxInv[C_f[nZ[3]]^new_hyp_key[3]]
            for k in range(len(pcc)):
                if (pcc[k][0] == CDelta0 and pcc[k][1] == CDelta1 and pcc[k][2] == CDelta2 and pcc[k][3] == CDelta3):
                    DDelta0 = sboxInv[D[nZ[0]]^new_hyp_key[0]] ^ sboxInv[D_f[nZ[0]]^new_hyp_key[0]]
                    DDelta1 = sboxInv[D[nZ[1]]^new_hyp_key[1]] ^ sboxInv[D_f[nZ[1]]^new_hyp_key[1]]
                    DDelta2 = sboxInv[D[nZ[2]]^new_hyp_key[2]] ^ sboxInv[D_f[nZ[2]]^new_hyp_key[2]]
                    DDelta3 = sboxInv[D[nZ[3]]^new_hyp_key[3]] ^ sboxInv[D_f[nZ[3]]^new_hyp_key[3]]
                    for m in range(len(pcc)):
                        if (pcc[m][0] == DDelta0 and pcc[m][1] == DDelta1 and pcc[m][2] == DDelta2 and pcc[m][3] == DDelta3):
                            possible_values = possible_values + new_hyp_key
    return possible_values

# Input : C - a normal ciphertext
#             as a python list of size 16, with values in range (0, 255)
#         C_f - the faulty ciphertext associated with C
#         D - a normal ciphertext
#         D_f - the faulty ciphertext associate with D
#         PK - the last round key partially retrieved, or equal to 16 "-1" if this function is called for the first time 
# Output : nothing
# Return : a reduced list of dimension 2 being the list of hypothesis of four bytes of the last round key : [n][4] with n the number of hypothesis,
# n should be equal to 1 here. We normally find here 4 bytes
# of the last round key
def resolve(C, C_f, D, D_f, partialKey = [-1 for i in range(16)]):
    pcc = preComputationsColumns()
    
    nZ = nonZeroIndices(C, C_f)
    #print "the ciphertexts / faulty ciphertexts differ at indices :"
    #print nZ
    print "Trying to find the round key ..."
    H = resolveKeyTwoFirstBytes(C, C_f, D, D_f, nZ, pcc)
    H3 = extendHypKey3rdByte(C, C_f, D, D_f, H, nZ, pcc)
    H4 = extendHypKey4thByte(C, C_f, D, D_f, H3, nZ, pcc)

    partialKey[nZ[0]] = H4[0]
    partialKey[nZ[1]] = H4[1]
    partialKey[nZ[2]] = H4[2]
    partialKey[nZ[3]] = H4[3]

    return partialKey
    
# Input : L - a dimension 1 list of ciphertexts / faulty ciphertexts, multiple of 4, ciphered with the same key, ordered two by two,
# with the two first couples having the same fault location on their faulty ciphertexts,
# idem for the two next couples, and so on ...
# example -> [A, A_f, B, B_f, C, C_f, D, D_f, ...] with A_f and B_f having the same fault location, idem for C_f and D_f.
# See the "main" file for a most detailed example.
# Output : nothing
# Return : The last round key, in full in enough ciphertexts / faulty ciphertexts have been given in input,
# or only some bytes of the key, if the user does not have enough pairs.
def retrieveKey(L):
    if ((len(L) % 4) != 0):
        print "The input list must be a multiple of 4 to ensure a single solution for the round key !"
        print "Remove the extra (useless) list(s) in the file to have a multiple of 4 and launch the program again !"
        return 0
    i = 0
    while (i < len(L)):
        PK = resolve(L[i], L[i+1], L[i+2], L[i+3])
        i += 4
    return PK
