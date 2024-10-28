# this file is to get 32bits Subkey6 by analysis.
# I will use the property of XOR to get Subkey6
import pandas as pd
from tools import *

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

# x is s-boxed plaintext that I computed with my hand
x = "6e2b89c2"
x = bin(int(x,16))[2:].zfill(32)


for i in range(0,4):
    plaintext = given_pairs[i][0]
    ciphertext = given_pairs[i][1]
    plain_R = plaintext[len(plaintext)//2:]
    cipher_R = ciphertext[len(ciphertext)//2:]
    plain_R = bin(int(plain_R,16))[2:].zfill(32)
    cipher_R = bin(int(cipher_R,16))[2:].zfill(32)

    # First, checking my s-boxes are doing well.
    plain_R = n_substitution(plain_R,sboxes,4)
    print(f"plain_R after sbox :\t {plain_R}\t{hex(int(plain_R,2))}")
    print(f"My result :\t\t {x}\t{hex(int(x,2))}")
    if plain_R == x :
        print("S-boxes are doing well")


    # The property of XOR is that XOR's inverse is itself
    # That is, if a XOR b = c, a XOR c = b
    subk_6 = XOR(plain_R,cipher_R,32)
    subk_6_hex = hex(int(subk_6,2))

    if ( cipher_R == XOR(plain_R,subk_6,32)):
        print("We finally get Subkey6")
        print(f"Subkey6 : \t {subk_6_hex}")
        print(f"{hex(int(XOR(plain_R,subk_6,32),2))}")
