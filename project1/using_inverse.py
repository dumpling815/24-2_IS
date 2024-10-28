import pandas as pd
from tools import *
def partial_encrypt(subk_1,subk_2,subk_4,subk_5,plaintext,ciphertext,sboxes,df_permutation):
    block = []
    for i in range(0,4):
        block.append(plaintext[i*16:(i+1)*16])
    block[3] = block[2] + block[3]

    mid_l = multiplication(block[0],subk_1,16)
    mid_r = n_substitution(block[3],sboxes,4)[16:]

    block_1_after_permutation = permutation(df_permutation,block[1])
    block_2_after_permutation = permutation(df_permutation,n_substitution(block[2],sboxes,2))

    ml1 = XOR(mid_l,XOR(block[2],subk_4,16),16)
    mr1 = XOR(block_1_after_permutation,mid_r,16)

    ml2 = multiplication(mr1,subk_2,16)
    mr2 = multiplication(ml1,subk_5,16)

    ur = XOR(block_2_after_permutation,mr2,16)
    ul = addition(ml2,ur,16)
    res = XOR(block_1_after_permutation,ul,16)

    if res != ciphertext[16:32]:
        #print("failed...........")
        #print(f"res: {hex(int(res,2))}")
        #print(f"cipher: {hex(int(ciphertext[16:32],2))}")
        return False
    else:
        #print("success..........")
        #print(f"subkey2: {hex(int(subk_2,2))}")
        #print(f"subkey5: {hex(int(subk_5,2))}")
        #print(f"res: {hex(int(res,2))}")
        #print(f"cipher: {hex(int(ciphertext[16:32],2))}")
        return True

# -------------Actual Main Function.-------------------------------------------------
# Reading CSV files
df_permutation = pd.read_csv('permutation.csv')
# sb is all 2-dimensional list. key value is 'C0' ~ 'C15'
sb1 = get_sbox_from_dataframe(pd.read_csv('s_box_1.csv'))
sb2 = get_sbox_from_dataframe(pd.read_csv('s_box_2.csv'))
sb3 = get_sbox_from_dataframe(pd.read_csv('s_box_3.csv'))
sb4 = get_sbox_from_dataframe(pd.read_csv('s_box_4.csv'))
sboxes = [sb1,sb2,sb3,sb4]

mod = 2**16
given_pairs = [("f9d062082456050b","c858f63425f50c2e"), \
               ("7092fb542ee18ac3","59c0fa662d2e161c"), \
               ("dd600212d1e83384","91187fa91caa99cd"), \
               ("b5438b700072ee1d","dafc53d022e7d0ab")]
plaintext_list = [bin(int(given_pairs[i][0],16))[2:].zfill(64) for i in range(0,4)]
ciphertext_list = [bin(int(given_pairs[i][1],16))[2:].zfill(64) for i in range(0,4)]

# inverse를 사용할 수 있을 만한 두 번째 pair 사용할것. 3번째 block이 2ee1로 홀수, subkey4와 xor후에도 홀수,
plaintext = plaintext_list[1]
ciphertext = ciphertext_list[1]

subk_1 = "1010011011001100"
subk_3 = "0011100110011000"
subk_6 = "01001011110111101000010111101100"
subk_4 = r_shift(subk_3,2)

block = []
for i in range(0,4):
    block.append(plaintext[i*16:(i+1)*16])
block[3] = block[2] + block[3]

mid_l = multiplication(block[0],subk_1,16)
mid_r = n_substitution(block[3],sboxes,4)[16:]
block_1_after_permutation = permutation(df_permutation,block[1])
block_2_after_permutation = permutation(df_permutation,n_substitution(block[2],sboxes,2))


ml1 = XOR(mid_l,XOR(block[2],subk_4,16),16)
mr1 = XOR(block_1_after_permutation,mid_r,16)
# ml1 is odd!! so we can get the inverse of ml1
# that is, when we get subkey2, subkey 5 is given deterministically
ml1_inv = inverse_mod(ml1,mod)
ml1_inv = bin(ml1_inv)[2:].zfill(16)
ul = XOR(ciphertext[16:32],block_1_after_permutation,16)



for i in range(0,mod):
    subk_2 = bin(i)[2:].zfill(16)
    ml2 = multiplication(mr1,subk_2,16)
    ur = addition(inverse_add(ml2,16),ul,16)
    if addition(ml2,ur,16) != ul:
        print("Inverse add gone wrong")
    mr2 = XOR(ur,block_2_after_permutation,16)
    subk_5 = multiplication(ml1_inv,mr2,16)
    if False == partial_encrypt(subk_1,subk_2,subk_4,subk_5,plaintext_list[1],ciphertext_list[1],sboxes,df_permutation):
        print("partial ecnrypt is wrong")

subk_poss = []
# First, use brute force to get subkey2.
for i in range(0,mod):
    subk_2 = bin(i)[2:].zfill(16)
    ml2 = multiplication(mr1,subk_2,16)
    ur = addition(inverse_add(ml2,16),ul,16)
    if addition(ml2,ur,16) != ul:
        print("Inverse add gone wrong")
    mr2 = XOR(ur,block_2_after_permutation,16)
    subk_5 = multiplication(ml1_inv,mr2,16)
    #print(f"subkey2 : {hex(int(subk_2,2))}")
    #print(f"subkey5 : {hex(int(subk_5,2))}")
    if "0000000000000001" != multiplication(ml1,ml1_inv,16):
        print("Inverse mod gone wrong..")
        break
    keys = (subk_1, subk_2, subk_3, subk_4, subk_5, subk_6)
    put = True
    for j in range(0,4):
        if j == 1:
            continue
        if hex(int(ciphertext_list[j],2))[2:].zfill(16) == encryption(plaintext_list[j],keys,df_permutation,sboxes):
            print(encryption(plaintext_list[j],keys,df_permutation,sboxes))
            print(subk_2,subk_5)
            continue
        else:
            #print(encryption(plaintext_list[j],keys,df_permutation,sboxes))
            put = False
            break
        """if j == 1: # because we used second pair to find subkeys
            if partial_encrypt(subk_1,subk_2,subk_4,subk_5,plaintext_list[j],ciphertext_list[j],sboxes,df_permutation):
                continue
        else:
            if partial_encrypt(subk_1,subk_2,subk_4,subk_5,plaintext_list[j],ciphertext_list[j],sboxes,df_permutation):
                continue
            else:
                put = False
                break"""
    if put:
        subk_poss.append((subk_2,subk_5))
        break

print(subk_poss)