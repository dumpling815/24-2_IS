"""
Information Security Chapter2 Homework
Each strings are encrypted by Shift Cipher, Vigenere Cipher, Shift + Vigenere
"""
import copy
targetString_1 = "VDKBNLDSNBNLOTSDQRDBTQHSX"
targetString_2 = "FFJFSFPYRUSBZLCFMFBIEIMFFZR"
targetString_3 = "YJZAGBATXHVAEVHCZXSOTAIXWZWS"

# All the code below that includes 'ascii' means it is leveraging ascii code, not directly means each character's ascii.
# That is, we will use ascii to get index of alphabets (A : get 0 by ascii of A - 65)

#---------------------------------------
#Actual main function of hw1. Decrypting Shift cipher by brute force
def decrypt_shift_bruteforce(targetString):
    # Assume that targetString is set of alphabets.(Uppercase)
    char_arr = string_to_ascii_arr(targetString)
    # Shifting 0 or 26 is meaningless.
    for i in range(1,26):
        # We should not change char_arr. -> Use copy package in function 'ascii_plus'
        # Because if not, the shifting will be accumulated.
        res_arr = ascii_minus(char_arr,i)
        res = ascii_arr_to_string(res_arr)
        print("Shift(Key) : {}\t\tResult : {}".format(i,res))

#----------------------------------------
#Shifting Ascii by 'num' parameter
def ascii_minus(char_arr, num):
    # Because char_arr is 1-dimensional list(array), there is no difference of result between shallow copy and deep copy
    res_arr = copy.copy(char_arr)
    for i in range(0,len(char_arr)):
        res_arr[i] -= num
        res_arr[i] %= 26
    return res_arr

#----------------------------------------
#Changing String variable to arr that contains each (ascii code - 65) (0~25 scale)
def string_to_ascii_arr(string):
    arr = []
    for char in string:
        arr.append(ord(char) - 65)
    return arr

#-----------------------------------------
#Reverse of upon function. (changing arr to string)
def ascii_arr_to_string(arr):
    string_arr = []
    for i in range(0,len(arr)):
        arr[i] += 65
    for ascii in arr:
        string_arr.append(chr(ascii))
    return ''.join(string_arr)

def main():
    decrypt_shift_bruteforce(targetString_1)

if __name__ == '__main__':
    main()