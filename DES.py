#!/usr/bin/env python3
import numpy as np
from bitstring import *

# !!! only for test purpose !!!

# ciphertest = np.array([0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0,
#                        1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0,
#                        0, 1, 1, 0, 0, 0])
ciphertest = BitArray(bin='0110100000111000111101100111010000000010110011011111100100011000')

plaintest = BitArray(bin='1010100000101011000110001010100100001000111110100101111101101001')

key1test = BitArray(bin='1111000101001110011011111100011010010101101011110001111110110011')


# Input: plaintext = 64bit list

# #Permutation matrices##
# Create initial permutation matrix

ip = np.arange(64).reshape((8, 8))
for col in range(0, 8):
    for row in range(0, 8):
        ip[row][col] = (58-((row >= 4)*1)+2*(row-(4*(row >= 4))))-col*8
# Create final permutation matrix

ip_inv = np.arange(64).reshape((8, 8))

for col in range(0, 8):
    for row in range(0, 8):
        ip_inv[row][col] = (40+(col-(1*(col % 2 != 0)))*4)-(32*(col % 2 != 0))-row*1

# Create expansion permutation matrix
e = np.arange(48).reshape((8, 6))

for row in range(0, 8):
    for i in range(0, 6):
        e[row][i] = i+4*row
e[0][0] = 32
e[7][5] = 1

# f-function permutation matrix
p = np.array([[16, 7, 20, 21, 29, 12, 28, 17], [1, 15, 23, 26, 5, 18, 31, 10], [2, 8, 24, 14, 32, 27, 3, 9],
              [19, 13, 30, 6, 22, 11, 4, 25]])

# initial key permutation
pc_1 = np.array([[57, 49, 41, 33, 25, 17, 9, 1], [58, 50, 42, 34, 26, 18, 10, 2], [59, 51, 43, 25, 27, 19, 11, 3],
                 [60, 52, 44, 36, 63, 55, 47, 39], [31, 23, 15, 7, 62, 54, 46, 38], [30, 22, 14, 6, 62, 53, 45, 37],
                 [29, 21, 13, 5, 28, 20, 12, 4]])

# round key permutation
pc_2 = np.array([[14, 17, 11, 24, 1, 5, 3, 28], [15, 6, 21, 10, 23, 19, 12, 4], [26, 8, 16, 7, 27, 20, 13, 2],
                 [41, 52, 31, 37, 47, 55, 30, 40], [51, 45, 33, 48, 44, 49, 39, 56], [34, 53, 46, 42, 50, 36, 29, 32]])

# DES-S-Boxes

# S1

sbox_1 = np.array([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                   [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                   [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                   [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])

# S2

sbox_2 = np.array([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                   [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                   [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                   [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])

# S3

sbox_3 = np.array([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                   [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                   [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                   [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])

# S4

sbox_4 = np.array([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                   [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                   [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                   [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])

# S5

sbox_5 = np.array([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                   [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                   [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                   [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])

# S6

sbox_6 = np.array([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                   [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                   [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                   [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])

# S7

sbox_7 = np.array([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                   [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                   [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                   [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])

# S8

sbox_8 = np.array([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                   [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                   [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                   [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])


# ENCRYPTION

# functions used for encryption

# initial permutation

def init_permutation(plaintext):
    # noinspection SpellCheckingInspection
    plaintext_initpermutated = BitArray(64)
    ip_1d = ip.flatten()
    for i in range(0, 64):
        plaintext_initpermutated[i] = plaintext[ip_1d[i]-1]
    return plaintext_initpermutated


def final_permutation(output_of_last_round):      # final permutation

    ciphertext = BitArray(64)
    ip_inv_1d = ip_inv.flatten()
    for i in range(0, 64):
        ciphertext[i] = output_of_last_round[ip_inv_1d[i]]
    #print(ciphertext)
    return ciphertext


def expansion_permutation(input_r_1):    # expansion permutation Input:32bit Output:48bit
    expanded_input = BitArray(48)
    e_1d = e.flatten()
    for i in range(0, 48):
        expanded_input[i] = input_r_1[e_1d[i]-1]
    #print(expanded_input)
    return expanded_input


def f_function_permutation(concatenated_sbox_output):     # f-function permutation
    output = BitArray(32)
    p_1d = p.flatten()
    for i in range(0, 32):
        output[i] = concatenated_sbox_output[p_1d[i]]
    print(output)
    return output


def sbox_substitution(input_sbox, sbox):            # sbox substitution function

    msb = BitArray(uint=int(input_sbox[0]), length=1)

    lsb = BitArray(uint=int(input_sbox[-1]), length=1)
    row = (msb + lsb).uint

    input_1 = BitArray(uint=int(input_sbox[1]), length=1)
    input_2 = BitArray(uint=int(input_sbox[2]), length=1)
    input_3 = BitArray(uint=int(input_sbox[3]), length=1)
    input_4 = BitArray(uint=int(input_sbox[4]), length=1)
    col = (input_1 + input_2 + input_3 + input_4).uint


    if sbox == 1:
        return BitArray(uint=int(sbox_1[row][col]), length=4).bin
    elif sbox == 2:
        return BitArray(uint=int(sbox_2[row][col]), length=4).bin
    elif sbox == 3:
        return BitArray(uint=int(sbox_3[row][col]), length=4).bin
    elif sbox == 4:
        return BitArray(uint=int(sbox_4[row][col]), length=4).bin
    elif sbox == 5:
        return BitArray(uint=int(sbox_5[row][col]), length=4).bin
    elif sbox == 6:
        return BitArray(uint=int(sbox_6[row][col]), length=4).bin
    elif sbox == 7:
        return BitArray(uint=int(sbox_7[row][col]), length=4).bin
    elif sbox == 8:
        return BitArray(uint=int(sbox_8[row][col]), length=4).bin


def f_function(righthalf, k_i, current_round):               # fFunction
    expanded_righthalf = expansion_permutation(righthalf)
    temp = expanded_righthalf ^ k_i
    input_sbox = [[], [], [], [], [], [], [], []]
    input_sbox[0] = temp[0:6]
    input_sbox[1] = temp[6:12]
    input_sbox[2] = temp[12:18]
    input_sbox[3] = temp[18:24]
    input_sbox[4] = temp[24:30]
    input_sbox[5] = temp[30:36]
    input_sbox[6] = temp[36:42]
    input_sbox[7] = temp[42:]


    output_sbox = [[], [], [], [], [], [], [], []]
    for i in range(0, 8):
        output_sbox[i] = sbox_substitution(input_sbox[i], current_round)
        print(output_sbox[i])
    # # print(type(output_sbox[i]))
    #     if len(output_sbox[i]) != 4:
    #         while len(output_sbox[i]) < 4:
    #             BitArray(output_sbox[i]).prepend('0b0')

    pre_permuted_result = BitArray(32)
    pre_permuted_result[:4] = output_sbox[0]
    pre_permuted_result[4:8] = output_sbox[1]
    pre_permuted_result[8:12] = output_sbox[2]
    pre_permuted_result[12:16] = output_sbox[3]
    pre_permuted_result[16:20] = output_sbox[4]
    pre_permuted_result[20:24] = output_sbox[5]
    pre_permuted_result[24:28] = output_sbox[6]
    pre_permuted_result[28:] = output_sbox[7]

    print(pre_permuted_result)
    print(len(pre_permuted_result))
    result = f_function_permutation(pre_permuted_result)
    return result


def initial_key_permutation(key):     # initial key permutation
    init_permutated_key = BitArray(56)
    pc_1_1d = pc_1.flatten()
    for i in range(0, 56):
        init_permutated_key.overwrite(key[pc_1_1d[i]], i)
    #print(init_permutated_key)
    return init_permutated_key


def round_key_permutation(roundkey_in):  # round key permutation

    roundkey = BitArray(56)
    roundkey = roundkey_in
    permutated_roundkey = BitArray(48)
    pc_2_1d = pc_2.flatten()
    for i in range(0, 48):
        permutated_roundkey[i]=roundkey[pc_2_1d[i]-1]
    # print(permutated_roundkey)
    return permutated_roundkey

# entire DES Key Schedule


def keyschedule(key):
    key = BitArray(initial_key_permutation(key))
    c = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    d = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(0, 17):
        c[i] = BitArray(28)
        d[i] = BitArray(28)
    roundkeys = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(0,16):
        roundkeys[i] = BitArray(28)
    c[0] = key[:int(len(key)/2)]
    d[0] = key[int(len(key)/2):]
    for i in range(1, 16):
        if i == 1 or i == 2 or i == 9 or i == 16:
            c[i] = c[i-1] << 1
            d[i] = d[i-1] << 1
            roundkeys[i] = round_key_permutation(c[i] + d[i])

        else:
            c[i] = c[i-1] << 2
            d[i] = d[i-1] << 2
            roundkeys[i] = round_key_permutation(c[i] + d[i])
    return roundkeys


def encrypt(plaintext, key):    # DES encryption function
    roundkeys = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(0,16):
        roundkeys[i] = BitArray(48)

    lefthalf = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(0,17):
        lefthalf[i] = BitArray(32)

    righthalf = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(0,17):
        righthalf[i] = BitArray(32)

    roundkeys = keyschedule(key)
    lefthalf[0] = init_permutation(plaintext)[:32]
    righthalf[0] = init_permutation(plaintext)[32:]
    for i in range(1, 16):
        lefthalf[i] = righthalf[i-1]
        righthalf[i] = lefthalf[i-1] ^ f_function(righthalf[i-1], roundkeys[i], i)
    ciphertext = final_permutation(righthalf[16] + lefthalf[16])

    return ciphertext


def parse_plaintext(plaintext):     # plaintext parser      # TODO: complete this

    char_list = list(plaintext)
    ascii_list = []
    for i in range(0, len(char_list)):
        ascii_list[i] = char_list[i].encode(encoding='ascii')
    #print(ascii_list)
    # bin_list = []
    # for i in range(0, len(ascii_list)):
    #     for j in range()
    #     bin_list[i] =

# TODO: ciphertext parser:  def parse_ciphertext(ciphertext):


def reverse_keyschedule(key):   # calculates roundkeys for decryption

    key = initial_key_permutation(key)
    c_decrypt = []
    d_decrypt = []
    roundkeys_decryption = []
    c_decrypt[16] = key[:int((len(key)/2))]
    d_decrypt[16] = key[int((len(key)/2)):]
    for i in range(1, 16):
        if i == 2 or i == 9 or i == 15:  # TODO: check indices
            c_decrypt[i] = np.right_shift(c_decrypt[i-1], 1)
            d_decrypt[i] = np.right_shift(d_decrypt[i-1], 1)
            roundkeys_decryption[i] = round_key_permutation(np.append(c_decrypt[i], d_decrypt[i]))

        else:                           # TODO: check indices
            c_decrypt[i] = np.right_shift(c_decrypt[i-1], 2)
            d_decrypt[i] = np.right_shift(d_decrypt[i-1], 2)
            roundkeys_decryption[i] = round_key_permutation(np.append(c_decrypt[i], d_decrypt[i]))
    return roundkeys_decryption


def decrypt(ciphertext, key):
    roundkeys_decryption = keyschedule(key)
    lefthalf_decryption = []
    righthalf_decryption = []
    lefthalf_decryption[0] = init_permutation(ciphertext)[:int((len(key)/2))]
    righthalf_decryption[0] = init_permutation(ciphertext)[int((len(key)/2)):]
    for i in range(1, 17):
        lefthalf_decryption[i] = righthalf_decryption[i-1]
        righthalf_decryption[i] = lefthalf_decryption[i-1] ^ f_function(righthalf_decryption[i-1],
                                                                        roundkeys_decryption[i], i)
    plaintext = final_permutation(np.append(righthalf_decryption[16], lefthalf_decryption[16]))
    return plaintext


def triple_des_ede_encryption(plaintext, key):
    key1 = key
    key2 = BitArray(64)
    key3 = BitArray(64)
    for i in range(0, len(key)):
        if key1[i] == 0:
            key2[i] = 1
        else:
            key2[i] = 0
    for i in range(0, len(key)):
        key3[i] = key2[i]

    ciphertext = encrypt(decrypt(encrypt(plaintext, key1), key2), key3)
    return ciphertext


def triple_des_ded_decryption(ciphertext, key):

    key1 = key
    key2 = BitArray(64)
    key3 = BitArray(64)
    #print(key3)
    # for i in range(0, 63):
    #     if key1[i] == 0:
    #         key2[i] = 1
    #     else:
    #         key2[i] = 0
    # for j in range(0, len(key)-1):
    #    key3[i] = key2[i]

    # plaintext = decrypt(encrypt(decrypt(ciphertext, key3), key2), key1)
    # return plaintext


ciphertext2 = triple_des_ede_encryption(plaintest, key1test)

print(ciphertext2)



















