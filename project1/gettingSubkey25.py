import pandas as pd
from tools import *

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

subk_1 = "1010011011001100"
subk_3 = "0011100110011000"
subk_6 = "01001011110111101000010111101100"
subk_4 = r_shift(subk_3,2)
breakall = False
for i in range(58176,mod):
    for j in range(0,mod):
        subk_2 = bin(i)[2:].zfill(16)
        subk_5 = bin(j)[2:].zfill(16)
        keys = (subk_1,subk_2,subk_3,subk_4,subk_5,subk_6)
        fin_res = True
        for k in range(0,len(plaintext_list)):
            plaintext = plaintext_list[k]
            ciphertext = ciphertext_list[k]
            res = encryption(plaintext,keys,df_permutation,sboxes)
            cipher_hex = hex(int(ciphertext,2))[2:].zfill(16)
            if res != cipher_hex:
                fin_res = False
                break
            else :
                continue
        if fin_res == True:
            print("Success!!")
            print(f"subkey2 : {hex(int(subk_2,2))[2:].zfill(4)}")
            print(f"subkey5 : {hex(int(subk_5,2))[2:].zfill(4)}")
            breakall = True
            break
    if breakall == True:
        break
    

        





