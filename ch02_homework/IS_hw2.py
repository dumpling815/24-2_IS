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
#Actual main function of hw2. Decrypting Vigenere cipher by brute force
def decrypt_vigenere_bruteforce(targetString,length):
    # Assume that targetString is set of alphabets.(Uppercase)
    #trial = 0
    # Because the hint was given (Plaintext starts with 'A'), we can easily infer that first character of key should be 'F'
    trial = 5*pow(26,2)
    char_arr = string_to_ascii_arr(targetString)
    #while(trial <= pow(26,length)):
    while(trial <= 5*pow(26,2) + 675):
        key = inference_key_bruteforce(length,trial)
        key_extended = key * (len(targetString) // len(key)) + key[0:(len(targetString) % len(key))]
        key_arr = string_to_ascii_arr(list(key_extended))
        res_arr = ascii_minus(char_arr, key_arr)
        res = ascii_arr_to_string(res_arr)
        trial += 1
        print("trial : {}\tkey : {}\tResult : {}".format(trial,key,res))
        

    

#
#
def inference_key_bruteforce(length,trial):
    # Hint was given : the plaintext starts with 'A'
    # Total 26^length keys are possible.
    key_arr = [0] * length
    trial_copy = copy.copy(trial)
    for i in range(length-1,-1,-1):
        denominator = pow(26,i)
        key_arr[length -1 - i] = trial_copy // denominator
        trial_copy -= trial_copy // denominator * denominator
    res = ascii_arr_to_string(key_arr)
    return res




#----------------------------------------
# key + target
def ascii_minus(char_arr, key_arr):
    res_arr = copy.copy(char_arr)
    for i in range(0,len(char_arr)):
        res_arr[i] -= key_arr[i]
        res_arr[i] %= 26
    
    return res_arr


#----------------------------------------
#Changing String variable to arr that contains each ascii code
def string_to_ascii_arr(string):
    arr = []
    for char in string:
        arr.append(ord(char) - 65)
    return arr

#-----------------------------------------
#Reverse of upon function. (changing arr that contains each character's ascii code to string)
def ascii_arr_to_string(arr):
    string_arr = []
    for i in range(0,len(arr)):
        arr[i] += 65
    for ascii in arr:
        string_arr.append(chr(ascii))
    return ''.join(string_arr)


def main():
    decrypt_vigenere_bruteforce(targetString_2,3)
if __name__ == '__main__':
    main()