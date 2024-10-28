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
#Actual main function of hw3.
def decrypt_twostep_bruteforce(targetString,length):
    # Assume that targetString is set of alphabets.(Uppercase)
    # Vigenere cipher key's first letter is given 'T' by hint, so we will start trial = 19*pow(26,2)
    # In this code, trial means the time of guess only for vigenere key, not for shift cipher
    trial = 19*pow(26,2)
    char_arr = string_to_ascii_arr(targetString)
    mid_arr = [None] * 26
    #while(trial <= pow(26,length)):
    while(trial <= 19*pow(26,2) + 675):
        key = inference_key_bruteforce(length,trial)
        key_extended = key * (len(targetString) // len(key)) + key[0:(len(targetString) % len(key))]
        key_arr = string_to_ascii_arr(list(key_extended))
        for i in range(0,26):
            # mid_arr is the 2 dimensional list that contains the possible decryption of step 2, shift cipher
            mid_arr[i] = ascii_minus(char_arr,i)
            #print(mid_arr[i])
            res_arr = vigenere_minus(mid_arr[i],key_arr)
            #print("Vigenere Key : {}\t Shift Key : {}\tResult : {}".format(key,i,res))
            if res_arr[3] == res_arr[6] == res_arr[10] == res_arr[13] == res_arr[21]:
               #print("4th:{}\t7th:{}\t11th:{}\t14th:{}\t22th:{}".format(res_arr[3],res_arr[6],res_arr[10],res_arr[13],res_arr[21]))
               res = ascii_arr_to_string(res_arr)
               print("Vigenere Key : {}\t Shift Key : {}\t\tResult : {}".format(key,i,res))
        trial += 1
        

#----------------------------------------
# We can infer much easily because of Hint in the homework, but I wrote more general module that infers key by Bruteforce
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
#Shifting Ascii by 'num' parameter
def ascii_minus(char_arr, num):
    # Because char_arr is 1-dimensional list(array), there is no difference of result between shallow copy and deep copy
    res_arr = copy.copy(char_arr)
    for i in range(0,len(char_arr)):
        res_arr[i] -= num
        res_arr[i] %= 26
    return res_arr

#----------------------------------------
# target - target
def vigenere_minus(char_arr, key_arr):
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
    decrypt_twostep_bruteforce(targetString_3,3)

if __name__ == '__main__':
    main()