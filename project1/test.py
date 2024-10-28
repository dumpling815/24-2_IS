# main file for the Information Security Project 1
# This project is to find keys when the plain-ciphertext pairs are given.
# Which means we are going to execute "known plaintext attack!"

# key consists of 6 sub keys 6th key is 32 bits, and remaining keys are all 16bits

# import pandas for get data from csv file as dataframe
import pandas as pd
from tools import *

def encryption_test(plaintext,keys,df_permutation,sboxes):
    (subk_1, subk_2, subk_3, subk_4, subk_5, subk_6) = keys
    block = []
    for i in range(0,4):
        block.append(plaintext[i*16:(i+1)*16])
    block[3] = block[2] + block[3]
    # note that 4th block is 32bits
    block[0] = multiplication(block[0],subk_1,16)
    print(f"block_0 after multiplication: {hex(int(block[0],2))}")
    block[1] = permutation(df_permutation,block[1])
    print(f"block_1 after permutation: {hex(int(block[1],2))}")
    block[2] = XOR(block[2],subk_4,16)
    print(f"block_2 after xor: {hex(int(block[2],2))}")
    block[3] = n_substitution(block[3],sboxes,4)
    print(f"block_3 after substitution: {hex(int(block[3],2))}")

    
    ml1 = XOR(block[0],block[2],16)
    print(f"ml1: {hex(int(ml1,2))}")
    mr1 = XOR(block[1],block[3][16:],16)
    print(f"mr1: {hex(int(mr1,2))}")
    ml2 = multiplication(mr1,subk_2,16)
    print(f"ml2: {hex(int(ml2,2))}")
    mr2 = multiplication(ml1,subk_5,16)
    print(f"mr2: {hex(int(mr2,2))}")
    
    block[2] = n_substitution(block[2],sboxes,2)
    print(f"block_2 after substitution: {hex(int(block[2],2))}")
    block[2] = permutation(df_permutation,block[2])
    print(f"block_2 after permutation: {hex(int(block[2],2))}")
    block[2] = XOR(block[2],mr2,16)
    print(f"block_2 XOR mr2 : {hex(int(block[2],2))}")
    block[2] = addition(block[2],ml2,16)
    print(f"block_2 after addition: {hex(int(block[2],2))}")

    block[0] = XOR(block[0],subk_3,16)
    block[1] = XOR(block[1],block[2],16)
    block[3] = XOR(block[3],subk_6,32)

    del block[2]
    ciphertext = ''.join(block)
    print(f"final result : {hex(int(ciphertext,2))[2:].zfill(16)}")
    return hex(int(ciphertext,2))[2:].zfill(16)
# -------------Actual Main Function.-------------------------------------------------
# Reading CSV files
df_permutation = pd.read_csv('permutation.csv')
# sb is all 2-dimensional list.
sb1 = get_sbox_from_dataframe(pd.read_csv('s_box_1.csv'))
sb2 = get_sbox_from_dataframe(pd.read_csv('s_box_2.csv'))
sb3 = get_sbox_from_dataframe(pd.read_csv('s_box_3.csv'))
sb4 = get_sbox_from_dataframe(pd.read_csv('s_box_4.csv'))
sboxes = [sb1,sb2,sb3,sb4]
given_pairs = [("f9d062082456050b","c858f63425f50c2e"), \
               ("7092fb542ee18ac3","59c0fa662d2e161c"), \
               ("dd600212d1e83384","91187fa91caa99cd"), \
               ("b5438b700072ee1d","dafc53d022e7d0ab")]
plaintext_list = [bin(int(given_pairs[i][0],16))[2:].zfill(64) for i in range(0,4)]
ciphertext_list = [bin(int(given_pairs[i][1],16))[2:].zfill(64) for i in range(0,4)]

print("Starting Encryption ...")
print("-----------------------")
keys = key_generation()
count = 0
for i in range(0,len(plaintext_list)):
    plaintext = plaintext_list[i]
    ciphertext = ciphertext_list[i]
    result = encryption_test(plaintext,keys,df_permutation,sboxes)
    print(f"my result: {result}")
    hex_cipher = hex(int(ciphertext,2))[2:].zfill(16)
    print(f"ciphertext: {hex_cipher}")
    if hex_cipher == result:
        print("Correct")
        count += 1
    print("----------------------------------------")
if count == 4:
    print("Project 1 successfully doned")