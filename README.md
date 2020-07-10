#  Cache Mapping
It is a program that simulates the 3 different types of cache mapping techniques namely - direct, fullt associative and n-way set associative. I wrote this program in my second semester at IIITD for my course Computer Organization.

## Usage
- The program is written in Python 3.6.9
- Clone this reposiotry to your desktop
- Open the terminal and navigate to the directory where the files are saved.
- Run level1.py (for level 1 cache) using the following command
```
python3 level1.py
```
- Run level2.py (for level 2 cache) using the following command
```
python3 level2.py
```
- Then enter the input as instructed

## Details
- The word length of the machine is 32 bits by default (so you can just press enter and move on during input) or you can decide it.
- The size of each memory word is 1 byte. 
- All the inputs have to be in the power of 2. 
- The write policy used is Write Through (WT) and the replacement policy used is Least Recently Used (LRU). 
- The address is input in decimal (base 10).

## Input
- Cache Lines - in the power of 2
- Block Size - in the power of 2 bytes
- Address Bits - 32 bits by default but can be 16,32,64 bits based on user discretion
-Set Size - is n in the power of 2 for n-way set associative mapping
- Mapping
  - 0 - Direct
  - 1 - Associative
  - 2 - N-way Set Associative
