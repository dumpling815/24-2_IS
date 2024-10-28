import DES_my

# ======================================================== Making Answer
from Crypto.Cipher import DES
from binascii import unhexlify, hexlify

# 평문과 키를 16진수 문자열로 제공
plaintext = "02468aceeca86420"
key = "0f1571c947d9e859"

# 평문과 키를 바이트로 변환
plaintext_bytes = unhexlify(plaintext)
key_bytes = unhexlify(key)

# DES 암호화 객체 생성 (ECB 모드 사용)
cipher = DES.new(key_bytes, DES.MODE_ECB)

# 암호화 수행
ciphertext_bytes = cipher.encrypt(plaintext_bytes)

# 암호문을 16진수 문자열로 변환하여 출력
answer = hexlify(ciphertext_bytes).decode()
# ======================================================== Making Answer


# Starting Actual Main Function

# input_str, key_str are both 64bit. (Of course, we will use 56bit key. Explain in  key_generation.)
input_str = "02468aceeca86420"
key_str = "0f1571c947d9e859"

# Because input is hex value string, we need to convert them into 64bit binary value 
# zfill helps to maintain 64bit length, [2:] is to remove "0b" value. because result of bin function is actually string class
input = bin(int(input_str,16))[2:].zfill(64)
key_original = bin(int(key_str,16))[2:].zfill(64)
# As a result, input & key variables are both length 64 string. (looks like "01101011...")

input_permut = DES_my.initial_permutation(input)
key_i = DES_my.initial_key_permutation(key_original)
# key_i is 56bit binary (string type)
L = input_permut[:32]
R = input_permut[32:]
# L,R are still string type (length:32)

print("L0 : {}\t\tR0 : {}".format(hex(int(L,2))[2:].zfill(8),hex(int(R,2))[2:].zfill(8)))
print("Starting round---------------------------")

for round in range(0,16):
    L_i = L
    key_i, key_pc2 = DES_my.key_generation(key_i,round)    # this key_generation returns 48-length bit key for each round(string type)
    # key_pc2 is now 48bit binary (string type)
    # key_i is 56bit for key_generation.
    L = R
    R = (DES_my.XOR(L_i,DES_my.Round(R,key_pc2),32))
    print("Round : {}\t\tKey : {}\nL : {}\t\tR : {}".format(round+1,hex(int(key_pc2,2))[2:].zfill(12),hex(int(L,2))[2:].zfill(8),hex(int(R,2))[2:].zfill(8) ))
    print("-------------------------------------------")

# Last Swap!
swap = L
L = R
R = swap

# IP^-1
final = L + R
ciphertext = hex(int(DES_my.inverse_initial_permutation(final),2))[2:]

print("My DES Ciphertext : {}".format(ciphertext))
print(f"Answer: {answer}")
print("------------------------------------------")
if answer != ciphertext:
    print("Wrong!! try again")
else:
    print("Correct!! Well done!!")
print("------------------------------------------")

