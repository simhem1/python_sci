# python_sci

Can you add some examples for how to use your implementation? 
I want to give password , let's say "foobar" into your algorithm , and i want to get encrypted password. Can you write here , how I can do this ?

## The DES algorithm takes a 64bit/8bytes-bitstring as input, operates on it and returns it, i.e. one has to split the plaintext message(here: "foobar") into 8byte pieces (padding if needed) with a proper encoding format, take it as
input for the algorithm and decode the output of the algorithm to get the ciphertext(here: encrypt("foobar")).
There are several modes of operation, one of them is the so-called ECB mode where the ciphertext is created as following: ciphertext = encrypt(plaintext[:64]) + encrypt(plaintext[64:128] + ...
(encrypting blockwise and concatenating the encrypted blocks). I think we should go for this mode as it is the easiest one when it comes to implementation even if it is not first choice under crypto aspects


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

##################### <br/>
I did not finish yet, a string to binary converter will be added today <br/>
Yesterday I focused on the internal DES structure <br/>
Btw please excuse that I am not that fast as you due to my lack of python experience  <br/>

<pre>
<h3>Check this url: https://github.com/edutilos6666/PythonSciStudentProject
i have committed my project here , you just commit your changes into your repository , i will copy these files, and add
them into encryption directory of my repository
</h3>
</pre>

