import pandas as pd
def r_shift(input,bits):
    zeros = '0' * bits
    result = zeros + input[:len(input)-bits]
    return result
def XOR(l,r,bits):
    # both l,r should be string
    return (bin(int(l,2) ^ int(r,2))[2:].zfill(bits))
def permutation(df_permutation,input):
    # input should be 16 bits. (string type)
    result = ""
    permutation_list = list(df_permutation['Permutation Index'])
    for i in range(0,16):
        result += input[permutation_list[i]]
    # result is also 16 bits.
    return result
def get_sbox_from_dataframe(df_sbox):
    # simple function to get 2-dimensional array value from dataframe
    result = []
    for i in range(0,16):
        result.append(df_sbox.iloc[i].tolist()[1:])
    return result
def substitution(sbox,input):
    # note that input is 8 bits (string type)
    row = int(input[:4],2)
    column = int(input[4:],2)
    result = bin(sbox[row][column])[2:].zfill(8)
    # note that result is also 8 bits (string type)
    return result
def multiplication(in1,in2,bits):
    num1 = int(in1,2)
    num2 = int(in2,2)
    result = (num1 * num2) % (2**16)
    result = bin(result)[2:].zfill(bits)
    return result
def addition(in1,in2,bits):
    num1 = int(in1,2)
    num2 = int(in2,2)
    result = (num1 + num2) % (2**16)
    result = bin(result)[2:].zfill(bits)
    return result
def key_generation(val):
    # subkey6 is gained by analysis
    subk_1 = "1010011011001100"
    subk_3 = "0011100110011000"
    subk_6 = "01001011110111101000010111101100"
    subk_4 = r_shift(subk_3,2)

    binary = bin(val)[2:].zfill(32)
    subk_2 = binary[:16]
    subk_5 = binary[16:]
    return (subk_1,subk_2,subk_3,subk_4,subk_5,subk_6)
def n_substitution(input,sboxes,n):
    result = ""
    for i in range(0,n):
        result += substitution(sboxes[i],input[i*8:(i+1)*8])
    return result
def subtraction(in1,in2,bits):
    num1 = int(in1,2)
    num2 = int(in2,2)
    result = (num1 - num2) % (2**16)
    result = bin(result)[2:].zfill(bits)
    return result


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

# we found these values by getting subkey 1,3,4,6
ml1 = "1101101111110000"
mr1 = "1001101111010110"
block_2_after_permutation = "0001110000010000"

plaintext_list = [bin(int(given_pairs[i][0],16))[2:].zfill(64) for i in range(0,4)]
ciphertext_list = [bin(int(given_pairs[i][1],16))[2:].zfill(64) for i in range(0,4)]