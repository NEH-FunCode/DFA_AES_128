This program works with Python 2.7.

This program implements a differential fault analysis attack on AES 128. The attack in explained in the following paper :

https://www.researchgate.net/publication/221291688_A_Differential_Fault_Attack_Technique_against_SPN_Structures_with_Application_to_the_AES_and_Khazad

(See chapter 3 in particular).

Its aim is to retrieve the main key of AES 128 if enough couples valid ciphertext / faulty ciphertexts have been computed. 8 couples minimum are necessary to retrieve the full main key.
The program takes a file (see input_example.txt) as parameter, with valid ciphertexts / faulty ciphertexts (Python lists), as follow :

Valid ciphertext 1
Corresponding faulty ciphertext 1
Valid ciphertext 2
Corresponding faulty ciphertext 2
...
Valid ciphertext n
Corresponding faulty ciphertext n

See test file, function : "test_input_in_file" ; set the input file in function "get_input_from_file" (for now it is "input_example.txt").
You can either modify the path, or the example file.

Then the program calls "test_input_in_file" in the main by default.
If the program manages to get the last tour key in full, the function to retrieve the main key is called.

The file "input_example2" only has n couples from which it is possible to retrieve 12 bytes (the key is 16 bytes long) of the last key tour.
The file "input_example3" has an illegal number of lists (not a multiple of 4) and so generates an error.
