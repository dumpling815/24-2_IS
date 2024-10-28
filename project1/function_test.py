import pandas as pd
from tools import *
# simple functions for encryption
df_permutation = pd.read_csv('permutation.csv')
# sb is all 2-dimensional list. key value is 'C0' ~ 'C15'
sb1 = get_sbox_from_dataframe(pd.read_csv('s_box_1.csv'))
sb2 = get_sbox_from_dataframe(pd.read_csv('s_box_2.csv'))
sb3 = get_sbox_from_dataframe(pd.read_csv('s_box_3.csv'))
sb4 = get_sbox_from_dataframe(pd.read_csv('s_box_4.csv'))
sboxes = [sb1,sb2,sb3,sb4]

given_pairs = [("f9d062082456050b","c858f63425f50c2e"), \
               ("7092fb542ee18ac3","59c0fa662d2e161c"), \
               ("dd600212d1e83384","91187fa91caa99cd"), \
               ("b5438b700072ee1d","dafc53d022e7d0ab")]

inv = inverse_mod("1111",2**4)
print(bin(inverse_mod("1111",2**4))[2:].zfill(4))
res = multiplication((bin(inverse_mod("1111",2**4))[2:].zfill(4)),multiplication("1111","0010",4),4)
print(res)

count = 0 
subk_3 = "0011100110011000"
subk_4 = "0000111001100110"
if subk_4 == r_shift(subk_3,2):
    print("r_shift doing well..")
    count += 1
if "0011011111111110" == XOR(subk_3,subk_4,16):
    print("XOR doing well..")
    count += 1
if "0101110011000100" == permutation(df_permutation, subk_3):
    print("permutation doing well..")
    count += 1
if "01101110001010111000100111000010" == n_substitution("00100100010101100000010100001011",sboxes,4):
    print("s-boxes doing well..")
    count += 1
if subk_3 == addition(inverse_add(subk_4,16),addition(subk_3,subk_4,16),16):
    print("addition, inverse add doing well..")
    count += 1
if "0010" == multiplication((bin(inverse_mod("1111",2**4))[2:].zfill(4)),multiplication("1111","0010",4),4):
    print("multiplication, inverse mod doing well..")
    count += 1

if count == 6:
    print("All doing well !!")