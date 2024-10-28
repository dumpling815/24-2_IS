# for DES round testing.
# note that this code is only for testing, so the code may be inefficient.

def initial_permutation(input):
    # input is length-64 string.
    # It's actual value is for 64bit binary
    permut = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
    result = []
    for i in range(0,64):
        result.append(input[permut[i]-1])
    result = ''.join(result)
    # return value is also length-64 string.
    return result

def permutation(input):
    permut = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
    result = []
    for i in range(0,32):
        result.append(input[permut[i]-1])
    result = ''.join(result)
    return result

def initial_key_permutation(key_original):
    pc_1_l = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36]
    pc_1_r = [63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
    key_l = []
    key_r = []
    # input key is 64-length binary (in string type)
    # this for is split the key in to two left, right and permute it by pc_1_l and pc_1_r each.
    # Also this for naturally discard every 8th bit of the input key.
    # As a result, key_l and key_r are both 28bits -> We made 56bit key
    # computing pc_1
    # key_l, key_r are both list that contains each bit of left right key
    for i in range(0,28):
        key_l.append(key_original[pc_1_l[i]-1])
        key_r.append(key_original[pc_1_r[i]-1])
    result = key_l + key_r
    result = ''.join(result)
    return result

def key_generation(key,round):
    pc_2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
    round_rotate = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    key_pc2 = []
    rot = round_rotate[round]
    key_l = key[:28]
    key_r = key[28:]

    key_l_rot = rotating(key_l,rot)
    key_r_rot = rotating(key_r,rot)


    key_before_pc_2 = key_l_rot + key_r_rot
    # at this moment, key_before_pc_2 is 56-length list

    for i in range(0,48):
        key_pc2.append(key_before_pc_2[pc_2[i]-1])
    key_pc2 = ''.join(key_pc2)
    key_pc2 = bin(int(key_pc2,2))[2:].zfill(48)

    return ( ''.join(key_before_pc_2), key_pc2)

def rotating(string_to_rotate, rot):
    # simple left-rotating function for list.
    """
    arr = list(str)
    length = len(arr)
    mid = arr[0:rot]
    residual = length - rot
    for i in range(rot,rot+residual):
        arr[i-rot] = arr[i]
    
    for i in range(0,len(mid)):
        arr[i+residual] = mid[i]
    """
    arr = list(string_to_rotate)
    L = arr[rot:]
    R = arr[:rot]
    res = L+R
    return res

def E_table(input):
    # 32bit string -> 48bit string
    E = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
    result = []
    for i in range(0,48):
        result.append(input[E[i]-1])
    result = ''.join(result)
    return result

def s_boxes(input):
    #input : 48 bit
    # S1 S-box
    S1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ]
    # S2 S-box
    S2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
    # S3 S-box
    S3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ]
    # S4 S-box
    S4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ]
    # S5 S-box
    S5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]
    # S6 S-box
    S6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]
    # S7 S-box
    S7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]
    # S8 S-box
    S8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2,1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
    boxes = [S1,S2,S3,S4,S5,S6,S7,S8]
    start_index = [i * 6 for i in range(0,8)] #0,6,12,...,42
    result = ""
    for i in range(0,8):
        # 현재 input 47bit
        target = input[start_index[i]:(start_index[i]+6)]

        row = int(target[0] + target[5],2)
        column = int(target[1:5],2)
        res = bin(boxes[i][row][column])[2:].zfill(4)
        result += res
    return result

def P_table(input):
    p = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
    result = []
    for i in range(0,32):
        result.append(input[p[i]-1])
    result = ''.join(result)
    return result

def Round(R,key):
    # R & key are both string type
    # E_table makes R 32bit -> 48bit (string type)
    expanded_R = E_table(R)
    xor_res = XOR(expanded_R,key,48)
    sbox_res = s_boxes(xor_res)
    result = P_table(sbox_res)
    return result

def XOR(l,r,bit):
    # both l,r should be string
    return (bin(int(l,2) ^ int(r,2))[2:].zfill(bit))

def inverse_initial_permutation(final):
    inverse_ip = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
    result = []
    for i in range(0,64):
        result.append(final[inverse_ip[i]-1])
    result = ''.join(result)
    return result
# def show_64bit_key(key_48)


