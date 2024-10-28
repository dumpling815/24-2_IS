# This file is storing all fundamental tools for project1.
import pandas as pd

def get_sbox_from_dataframe(df_sbox):
    # simple function to get 2-dimensional array value from dataframe
    result = []
    for i in range(0,16):
        result.append(df_sbox.iloc[i].tolist()[1:])
    return result

# simple functions for encryption
def r_shift(input,bits):
    zeros = '0' * bits
    result = zeros + input[:len(input)-bits]
    return result
def XOR(l,r,bits):
    # both l,r should be string
    return (bin(int(l,2) ^ int(r,2))[2:].zfill(bits))
def multiplication(in1,in2,bits):
    num1 = int(in1,2)
    num2 = int(in2,2)
    result = (num1 * num2) % (2**bits)
    result = bin(result)[2:].zfill(bits)
    return result
def inverse_mod(plaintext,m):
    p = int(plaintext,2)
    a1,a2,a3 = (1,0,m)
    b1,b2,b3 = (0,1,p)
    while 1 :
        if b3 == 0:
            return ValueError("We cannot find the inverse mod")
        elif b3 == 1:
            if b2 >= 0:
                return b2
            else:
                return m + b2
        q = a3 // b3
        t1,t2,t3 = (a1 - q*b1, a2 - q*b2, a3 - q*b3)
        a1,a2,a3 = (b1,b2,b3)
        b1,b2,b3 = (t1,t2,t3)
def addition(in1,in2,bits):
    num1 = int(in1,2)
    num2 = int(in2,2)
    result = (num1 + num2) % (2**16)
    result = bin(result)[2:].zfill(bits)
    return result
def inverse_add(input,bits):
    num1 = int(input,2)
    num2 = 2**bits
    result = (num2 - num1)
    result = bin(result)[2:].zfill(bits)
    return result

# Substitution & Permutation
def substitution(sbox,input):
    # note that input is 8 bits (string type)
    row = int(input[:4],2)
    column = int(input[4:],2)
    result = bin(sbox[row][column])[2:].zfill(8)
    # note that result is also 8 bits (string type)
    return result
def n_substitution(input,sboxes,n):
    result = ""
    for i in range(0,n):
        result += substitution(sboxes[i],input[i*8:(i+1)*8])
    return result
def permutation(df_permutation,input):
    # input should be 16 bits. (string type)
    result = ""
    permutation_list = list(df_permutation['Permutation Index'])
    for i in range(0,16):
        result += input[permutation_list[i]]
    # result is also 16 bits.
    return result    

# Encryption algorithm
def key_generation(val):
    # subkey6 is gained by analysis
    subk_1 = "1010011011001100"
    subk_3 = "0011100110011000"
    subk_6 = "01001011110111101000010111101100"
    subk_4 = r_shift(subk_3,2)
    subk_2 = "1001111101010000"
    subk_5 = "0000011010010100"
    return (subk_1,subk_2,subk_3,subk_4,subk_5,subk_6)
def encryption(plaintext,keys,df_permutation,sboxes):
    (subk_1, subk_2, subk_3, subk_4, subk_5, subk_6) = keys
    block = []
    for i in range(0,4):
        block.append(plaintext[i*16:(i+1)*16])
    block[3] = block[2] + block[3]
    # note that 4th block is 32bits
    block[0] = multiplication(block[0],subk_1,16)
    block[1] = permutation(df_permutation,block[1])
    block[2] = XOR(block[2],subk_4,16)
    block[3] = n_substitution(block[3],sboxes,4)

    
    ml1 = XOR(block[0],block[2],16)
    mr1 = XOR(block[1],block[3][16:],16)
    ml2 = multiplication(mr1,subk_2,16)
    mr2 = multiplication(ml1,subk_5,16)
    
    block[2] = n_substitution(block[2],sboxes,2)
    block[2] = permutation(df_permutation,block[2])
    block[2] = XOR(block[2],mr2,16)
    block[2] = addition(block[2],ml2,16)

    block[0] = XOR(block[0],subk_3,16)
    block[1] = XOR(block[1],block[2],16)
    block[3] = XOR(block[3],subk_6,32)

    del block[2]
    ciphertext = ''.join(block)
    return hex(int(ciphertext,2))[2:].zfill(16)