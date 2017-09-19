# python_sci

Can you add some examples for how to use your implementation? 
I want to give password , let's say "foobar" into your algorithm , and i want to get encrypted password. Can you write here , how I can do this ? 


Btw I have completed my part , i have to only comment my code and i am waiting for your code in order to create login page. And maybe i will create some extra apps into this , in order to get 100% :) 


And your code does not run : 
1) # initPermutation: 
text = "foobar"
initPermutation(text)


# output 
Traceback (most recent call last):
  File "/home/edutilos/PycharmProjects/PythonSciStudentProject/encryption/DES.py", line 143, in <module>
    initPermutation(text)
  File "/home/edutilos/PycharmProjects/PythonSciStudentProject/encryption/DES.py", line 87, in initPermutation
    print(plaintext[IP_1d[i]])
TypeError: string indices must be integers



################################################################
2) # finalPermutation: 
text = "foobar"
finalPermutation(text)


# output 
Traceback (most recent call last):
  File "/home/edutilos/PycharmProjects/PythonSciStudentProject/encryption/DES.py", line 143, in <module>
    finalPermutation(text)
  File "/home/edutilos/PycharmProjects/PythonSciStudentProject/encryption/DES.py", line 98, in finalPermutation
    ciphertext[i] = input[IP_inv_1d[i]]
TypeError: string indices must be integers
