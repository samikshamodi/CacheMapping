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
- Set Size - is n in the power of 2 for n-way set associative mapping
- Mapping
  - 0 - Direct
  - 1 - Associative
  - 2 - N-way Set Associative
  
## Commands
- read address
- write address data
- quit - to exit the program
After every valid command, the entire cache will be printed. In case of a MISS, it will print
address not found and will update the cache table with the new dataset. In case of a replacement,
it will also print the address by which the block will be replaced.

## Logic
Cache HIT - When requested data is found in the cache
Cache MISS - When requested data is not found in the cache
Caches are of 3 types
- Direct Mapped Cache
- Fully Associative Cache
- Set Associative Cache

Write Policy - Write Through (Hence Dirty Bit is always 0)

Replacement Policy - LRU (Least Recently Used)

### Direct Mapped Cache
Definitions <br>
Tag - distinguishes one cache memory block from another <br>
Index - identifies the cache block <br>
Offset - points to desired data in the cache block <br>

Instruction Breakdown <br>
Each of the address of read or write instruction is broken into three parts: Tag, Index and Offset

Tag bits = Address bits - Index bits - Offset bits <br>
Index bits = log​ 2​ (No of Cache Lines) <br>
Offset bits = log​ 2​ (Block Size in bytes)

The requested address is converted to binary and is broken down into tag, index and
offset. Then the cache table with the corresponding index is examined. If valid bit of the index is
0, cache miss is obtained. Else tag bit of the requested address is compared with tag bit in cache table. If tag is a match then cache hit is obtained else cache miss is obtained. When cache miss
occurs the cache table will be updated with the new dataset.

### Fully Associative Cache
Definitions <br>
Tag - distinguishes one cache memory block from another <br>
Offset - points to desired data in the cache block <br>

Instruction Breakdown <br>
Each of the address of read or write instruction is broken into two parts: Tag and Offset

Tag bits = Address bits - Offset bits <br>
Offset bits = log​ 2​ (Block Size in bytes)

The requested address is converted to binary and is broken down into tag and offset. The
requested tag is then searched in the cache. If the tag matches with one of the entries in the cache
table, cache hit is obtained. Else, cache miss obtained. When cache miss occurs the cache table
will be updated with the new dataset. If the cache is full then it will place the new dataset at the
least recently used block in the cache. The lru array has the least recently used cache block at 0th index and it’s most recently used cache block at the last index. Everytime a particular cache
block is accessed it is removed from the lru array and placed at the last index in the array.

### N-way Set Associative Cache
N-way set associative cache combines the idea of direct mapped cache and fully associative
cache. It has direct mapped principle to an index, yet fully associative concept within the index.
An index contains N blocks of way.

Definitions <br>
Tag - distinguishes one cache memory block from another <br>
Index - identifies the cache block <br>
Offset - points to desired data in the cache block <br>

Instruction Breakdown <br>
Each of the address of read or write instruction is broken into three parts: Tag, Index and Offset <br>

Total sets = No of Cache Lines/Set Size <br>
Tag bits = Address bits - Index bits - Offset bits <br>
Index bits = log​ 2​ (Total sets) <br>
Offset bits = log​ 2​ (Block Size in bytes)
