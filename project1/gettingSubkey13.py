# this file is to get 16bits Subkey1 and Subkey3 by analysis.
# I will use meet in the middle attack which is used to break double-DES
# First, I will found middle value with brute force attack
# then, I will use middle value to infer Subkey1 & 3
from tools import *

def find_subkey13(plaintext_list, ciphertext_list, mod=2**16):
    # following two lists are about the candidate of subkeys.
    # So, I will push all of candidate in the list, and check if there is duplicated 
    # key over 4 known pairs.
    # That is, if same subkey candidate is duplicated with # of 4, that is real subkey
    subk_poss = []
    plaintext = plaintext_list[0][:16]
    ciphertext = ciphertext_list[0][:16]
    # because impossible to find inverse everytime because given modular is 2 ^ 16
    # I changed the method to find subkey 1 by brute force (mid -> subkey1)
    for subk_1 in range(0,mod):
        subk_1 = bin(subk_1)[2:].zfill(16)
        mid = multiplication(plaintext,subk_1,16)
        subk_3 = XOR(mid,ciphertext,16)
        subk_poss.append((subk_1,subk_3))
 
    rmv = []
    for i in range(1,len(plaintext_list)):
        plaintext = plaintext_list[i][:16]
        ciphertext = ciphertext_list[i][:16]
        for j in range(0,mod):
            subk_1, subk_3 = subk_poss[j]
            mid = multiplication(plaintext,subk_1,16)
            test_res = XOR(mid,subk_3,16)
            if test_res != ciphertext:
                rmv.append((subk_1,subk_3))
    list(set(rmv))
    for i in rmv:
        if i in subk_poss:
            subk_poss.remove(i)
    subk_1_res, subk_3_res = subk_poss[0]
    return (subk_1_res,subk_3_res)

# Actual main of getting subkey13 ------------------------------------------
given_pairs = [("f9d062082456050b","c858f63425f50c2e"), \
               ("7092fb542ee18ac3","59c0fa662d2e161c"), \
               ("dd600212d1e83384","91187fa91caa99cd"), \
               ("b5438b700072ee1d","dafc53d022e7d0ab")]

plaintext_list = [bin(int(given_pairs[i][0],16))[2:].zfill(64) for i in range(0,4)]
ciphertext_list = [bin(int(given_pairs[i][1],16))[2:].zfill(64) for i in range(0,4)]


subk_1, subk_3 = find_subkey13(plaintext_list,ciphertext_list,2**16)

print(f"subk_1 : {subk_1}\nsubk_3 : {subk_3}")
print("--------------------------------------")
for i in range(1,len(plaintext_list)):
    mid = multiplication(plaintext_list[i][:16],subk_1,16)
    res = XOR(mid,subk_3,16)
    print(f"result = {hex(int(res,2))}")
    cipher = bin(int(given_pairs[i][1],16))[2:].zfill(64)[:16]
    print(f"cipher = {hex(int(cipher,2))}")
    if res != cipher:
        print("Try again")
    elif i == len(plaintext_list)-1:
        print("Success")



# 처음에는 inverse를 사용하려고 하였으나, plain-cipher 쌍의 key중에서 block1에 속하는 숫자들 중 홀수가 없음
# 따라서, 역원을 구하지 못했고, subkey 1을 bruteforce로 유추 (subkey 3은 subkey1에 deterministic)
# O(2^16)의 시간복잡도로 해결가능