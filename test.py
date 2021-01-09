from AES import *
from DFA import *
from errors_management import *
from time import clock

# This function takes a function as input, executes it and times it

def time_fun(func):
    t1 = clock()
    func()
    t2 = clock()
    print "This function has been executed in "+str(t2-t1)+" secondes"

# This function reads into a .txt file (do not write explicitly the extension in the file name !)
# in which the python lists are sorted like :
# List 1
# List 2
# ...
# with the lists being normal ciphertexts / faulty ciphertexts
# see the "input_example" file in the directory for more details

def get_input_from_file(path):
    lists = []
    s = ""
    input_file = open(path, "r")
    for line in input_file.readlines():
        l = []
        length = len(line)
        i = 0
        while (i < length):
            if (line[i] == ','):
                i = i+1
                while (line[i] != ',' and line[i] != '[' and line[i] != ']' and line[i] != '\n'):
                    s = s + line[i]
                    i = i+1
                s = s.replace(' ','')
                s_int = int(s)
                l = l + [s_int]
                s = ""
            elif (line[i] != '[' and line[i] != ']' and line[i] != ' ' and line[i] != '\n'):
                while (line[i] != ',' and line[i] != '[' and line[i] != ']' and line[i] != '\n'):
                    s = s + line[i]
                    i = i+1
                s = s.replace(' ','')
                s_int = int(s)
                l = l + [s_int]
                s = ""
            else:
                i = i+1
        lists = lists + [l]
    input_file.close()
    return lists

# This function retrieves 4 bytes of the last round key
# from two different plaintexts ciphered with the same key
# with the same fault value injected (at the same location)
# Note : it would have worked with two different fault values too

def test_two_diff_plain():
    plaintext = [i for i in range(16)]
    plaintext2 = [16-i-1 for i in range(16)]
    mainK = [0xfe for k in range(16)]
    print "the round key to find is :"
    print createRoundKey(expandKey(mainK), 10)
    location = 0 # first column : C differs from C* at bytes 0,7,10,13
    C, C_f = createCouple(plaintext, mainK, location)
    print "the first ciphertext and the faulty ciphertext associated with are :"
    print C
    print C_f
    D, D_f = createCouple(plaintext2, mainK, location)
    print "the second ciphertext and the faulty ciphertext associated with are :"
    print D
    print D_f

    pcc = preComputationsColumns()
    nZ = nonZeroIndices(C, C_f)
    print "the ciphertexts / faulty ciphertexts differ at indices :"
    print nZ

    H = resolveKeyTwoFirstBytes(C, C_f, D, D_f, nZ, pcc)
    H3 = extendHypKey3rdByte(C, C_f, D, D_f, H, nZ, pcc)
    H4 = extendHypKey4thByte(C, C_f, D, D_f, H3, nZ, pcc)
    
    partialKey = [-1 for i in range(16)]

    partialKey[nZ[0]] = H4[0]
    partialKey[nZ[1]] = H4[1]
    partialKey[nZ[2]] = H4[2]
    partialKey[nZ[3]] = H4[3]

    print "The retrieved partial key is (-1 stands for unknown values) :"
    print partialKey



# This function retrieves 4 bytes of the last round key
# from two different plaintexts ciphered with the same key
# with the same fault value injected (at the same location, but other than at indice 0)
# Note : it would have worked with two different fault values too

def test_other_loc_with_resolve_fun():
    plaintext1 = [i for i in range(16)]
    plaintext2 = [16-j-1 for j in range(16)]
    mainK = [0xfe for k in range(16)]
    print "the round key to find is :"
    print createRoundKey(expandKey(mainK), 10)
    location = 2 # third column : C differs from C* at bytes 2,5,8,15
    C, C_f = createCouple(plaintext1, mainK, location)
    print "the first ciphertext and the faulty ciphertext associated with are :"
    print C
    print C_f
    D, D_f = createCouple(plaintext2, mainK, location)
    print "the second ciphertext and the faulty ciphertext associated with are :"
    print D
    print D_f

    PK = resolve(C, C_f, D, D_f)

    print "The retrieved partial key is (-1 stands for unknown values) :"
    print PK


# This function retrieves 4 bytes of the last round key
# from the same plaintext ciphered twice with the same key
# but with a different fault value injected (at the same location)

def test_same_plain_ciphered_twice():
    plaintext = [i for i in range(16)]
    mainK = [0xfe for k in range(16)]
    print "the round key to find is :"
    print createRoundKey(expandKey(mainK), 10)
    location = 0 # first column : C differs from C* at bytes 0,7,10,13
    C, C_f = createCoupleWithRdm(plaintext, mainK, location)
    print "the first ciphertext and the faulty ciphertext associated with are :"
    print C
    print C_f
    # we have to re-initialize the plaintext because the last function modified it
    plaintext = [i for i in range(16)]
    D, D_f = createCoupleWithRdm(plaintext, mainK, location)
    print "the second ciphertext and the faulty ciphertext associated with are :"
    print D
    print D_f

    pcc = preComputationsColumns()
    nZ = nonZeroIndices(C, C_f)
    print "the ciphertexts / faulty ciphertexts differ at indices :"
    print nZ

    H = resolveKeyTwoFirstBytes(C, C_f, D, D_f, nZ, pcc)
    H3 = extendHypKey3rdByte(C, C_f, D, D_f, H, nZ, pcc)
    H4 = extendHypKey4thByte(C, C_f, D, D_f, H3, nZ, pcc)

    partialKey = [-1 for i in range(16)]

    partialKey[nZ[0]] = H4[0]
    partialKey[nZ[1]] = H4[1]
    partialKey[nZ[2]] = H4[2]
    partialKey[nZ[3]] = H4[3]

    print "The retrieved partial key is (-1 stands for unknown values) :"
    print partialKey

# This function retrieves 16 bytes of the last round key (therefore, the whole last round key)
# from eight different plaintexts ciphered with the same key
# with the same fault value injected (at the same location)
# Note : it would have worked with two different fault values too

def test_retrieve_whole_round_key():
    mainK = [0xfa for k in range(16)]
    print "the round key to find is : "
    print createRoundKey(expandKey(mainK), 10)
    plaintext1 = [i for i in range(16)]
    plaintext2 = [16-j-1 for j in range(16)]
    plaintext3 = [i+1 for i in range(16)]
    plaintext4 = [16-j for j in range(16)]
    plaintext5 = [i+2 for i in range(16)]
    plaintext6 = [16-j+4 for j in range(16)]
    plaintext7 = [i+3 for i in range(16)]
    plaintext8 = [16-j+5 for j in range(16)]
    loc = 0
    C, C_f = createCouple(plaintext1, mainK, loc)
    D, D_f = createCouple(plaintext2, mainK, loc)
    E, E_f = createCouple(plaintext3, mainK, loc+1)
    F, F_f = createCouple(plaintext4, mainK, loc+1)
    G, G_f = createCouple(plaintext5, mainK, loc+2)
    H, H_f = createCouple(plaintext6, mainK, loc+2)
    I, I_f = createCouple(plaintext7, mainK, loc+3)
    J, J_f = createCouple(plaintext8, mainK, loc+3)

    L = []
    L = L + [C] + [C_f] + [D] + [D_f] + [E] + [E_f] + [F] + [F_f]+ [G] + [G_f] + [H] + [H_f] + [I] + [I_f] + [J] + [J_f]
    R10 = retrieveKey(L)
    print "The retrieved partial key is (-1 stands for unknown values) :"
    print R10


def test_input_in_file():
    mainK = [0xfa for k in range(16)]
    print "The main key is :"
    print mainK
    print "The round key to find is : "
    print createRoundKey(expandKey(mainK), 10)
    L = get_input_from_file("V:\pole_crypto\Dev\PME\JeanGrey-master\DFA_AES_128_Python\input_example.txt")
    R10 = retrieveKey(L)
    if (R10 == 0): # not a valid input file
        return 0
    print "The retrieved round key is :"
    print R10

    for i in range(len(R10)):
        if (R10[i] == -1):
            print "Only a subset of the last round key has been retrieved ; can't find the main key !"
            print "The partial retrieved round key is (-1 stands for unknown value): "
            print R10
            return 0
    
    MK = find_main_key_from_last_key(R10)
    print "The retrieved main key is :"
    print MK

