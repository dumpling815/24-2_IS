# main file for the Information Security Project 1
# This project is to find keys when the plain-ciphertext pairs are given.
# Which means we are going to execute "known plaintext attack!"

# key consists of 6 sub keys 6th key is 32 bits, and remaining keys are all 16bits

# import pandas for get data from csv file as dataframe
import pandas as pd
from tools import *
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
    result = encryption(plaintext,keys,df_permutation,sboxes)
    print(f"my result: {result}")
    hex_cipher = hex(int(ciphertext,2))[2:].zfill(16)
    print(f"ciphertext: {hex_cipher}")
    if hex_cipher == result:
        print("Correct")
        count += 1
    print("----------------------------------------")
if count == 4:
    print("Project 1 successfully doned")