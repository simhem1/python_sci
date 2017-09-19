#!/usr/bin/env python3
import numpy as np

#Input: plaintext = 64bit list

##Permutation matrices##
#Create initial permutation matrix

IP = np.zeros((8,8))
for col in range(0, 8):
    for row in range(0, 8):
        IP[row][col]=(58-((row>=4)*1)+2*((row-(4*(row>=4)))))-col*8
#Create final permutation matrix

IP_inv = np.zeros((8,8))

for col in range(0, 8):
    for row in range(0, 8):
           IP_inv[row][col] = (40+(col-(1*(col%2!=0)))*4)-(32*(col%2!=0))-row*1

#Create expansion permutation matrix
E = np.zeros((8,6))

for row in range(0, 8):
    for i in range(0, 6):
        E[row][i]=i+4*row
E[0][0]=32
E[7][5]=1

#f-function permutation matrix
P = np.array([[16,7,20,21,29,12,28,17],[1,15,23,26,5,18,31,10], [2,8,24,14,32,27,3,9], [19,13,30,6,22,11,4,25]])

#initial key permutation
PC_1 = np.array([[57,49,41,33,25,17,9,1], [58,50,42,34,26,18,10,2], [59,51,43,25,27,19,11,3], [60,52,44,36,63,55,47,39], [31,23,15,7,62,54,46,38], [30,22,14,6,62,53,45,37], [29,21,13,5,28,20,12,4]])

#round key permutation
PC_2 = np.array([[14,17,11,24,1,5,3,28], [15,6,21,10,23,19,12,4], [26,8,16,7,27,20,13,2], [41,52,31,37,47,55,30,40], [51,45,33,48,44,49,39,56], [34,53,46,42,50,36,29,32]])

##DES-S-Boxes##

#S1

Sbox_1 = np.array([[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7], [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8], [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]])

#S2

Sbox_2 = np.array([[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10], [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5], [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15], [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]])

#S3

Sbox_3 = np.array([[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8], [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1], [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7], [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]])

#S4

Sbox_4 = np.array([[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15], [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9], [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4], [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]])

#S5

Sbox_5 = np.array([[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9], [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6], [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14], [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]])

#S6

Sbox_6  = np.array([[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11], [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8], [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6], [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]])

#S7

Sbox_7  = np.array([[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1], [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6], [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2], [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]])

#S8

Sbox_8 = np.array([[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7], [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2], [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8], [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]])



#print(IP)
#print(IP_inv)
#print(E)
#print(np.array(P))
#print(np.array(Sbox_1))

# initial permutation

def initPermutation(plaintext):
    plaintext_initpermutated = np.zeros((1,64))
    IP_1d=IP.flatten()
    for i in range(0,64):
        plaintext_initpermutated[i]  = plaintext[IP_1d[i]]
    print(plaintext_initpermutated)
    return plaintext_initpermutated

# final permutation

def finalPermutation(input):
    ciphertext = np.zeros((1,64))
    IP_inv_1d=IP_inv.flatten()
    for i in range(0,64):
        ciphertext[i] = input[IP_inv_1d[i]]
    print(ciphertext)
    return ciphertext

# expansion permutation
# Input:32bit Output:48bit

def expansionPermutation(input):
    expanded_input = np.zeros((1,48))
    E_1d = E.flatten()
    for i in range(0,48):
        expanded_input[i] = input[E_1d[i]]
    print(expanded_input)
    return expanded_input


##Key Schedule##

#initial key permutation

def initialKeyPermutation(key):
    initPermutatedKey = np.zeros((1,56))
    PC_1_1d = PC_1.flatten()
    for i in range(0,56):
        initPermutatedKey[i] = key[PC_1_1d[i]]
    print(initPermutatedKey)
    return initPermutatedKey

#round key permutation


def RoundKeyPermutation(roundkey):
    permutatedRoundKey = np.zeros((1,48))
    PC_2_1d = PC_2.flatten()
    for i in range(0,48):
        initPermutatedKey[i] = key[PC_2_1d[i]]
    print(permutatedRoundKey)
    return permutatedRoundKey



