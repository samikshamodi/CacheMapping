import math
import random
"""
Consider a cache of size 16 KB with block size 256 bytes. The size of main memory is 128 KB. 
Given:
Main memory size = 128 KB 
block_size=frame_size=line_size = 256 bytes
Cache memory size = 16 KB
Set size = 2 (for 2 way set associative mapping)
"""

"""
DIRECT MAPPING
Size of main memory = 128 KB = 2^7 * 2^10 bytes = 2^17 bytes. Therefore no of bits in physical address is 17 bits.
Block size = 256 bytes = 2^8 bytes. Therefore no of bits in word-offset is 8 bits.
Total number of lines in cache = Cache size / Line size = 16 KB / 256 bytes = 16 * 2^10 bytes / 256 bytes = 2^6 lines = 64 lines
Therefore no of bits in index = 6 bits
Number of bits in tag = Number of bits in physical address – (Number of bits in index + Number of bits in block offset)
= 17 bits – (6 bits + 8 bits) = 17 bits – 14 bits = 3 bits
Therefore no of bits in tag = 3 bits

<Main Memory Address - 17 bits> = |Tag - 3 bits | Index - 6 bits | Word-offset - 8 bits|
"""

""" 
FULLY ASSOCIATIVE MAPPING
Size of main memory = 128 KB = 2^7 * 2^10 bytes = 2^17 bytes. Therefore no of bits in physical address is 17 bits.
Block size = 256 bytes = 2^8 bytes. Therefore no of bits in word-offset is 8 bits.
Number of bits in tag = Number of bits in physical address – Number of bits in word-offset = 17 bits – 8 bits = 9 bits. 
Therefore no of bits in tag = 9 bits

<Main Memory Address - 17 bits> = |Tag - 9 bits | Word-offset - 8 bits|

Total number of lines in cache = Cache size / Line size = 16 KB / 256 bytes = 16 * 2^10 bytes / 256 bytes = 2^6 lines = 64 lines
Therfore no of lines in cache = 64
"""

"""
SET ASSOCIATIVE MAPPING
(For a 2 way set associative mapping)
Size of main memory = 128 KB = 2^7 * 2^10 bytes = 2^17 bytes. Therefore no of bits in physical address is 17 bits.
Block size = 256 bytes = 2^8 bytes. Therefore no of bits in word-offset is 8 bits.
Total number of lines in cache = Cache size / Line size = 16 KB / 256 bytes = 16 * 2^10 bytes / 256 bytes = 2^6 lines = 64 lines
Total number of sets in cache = Total number of lines in cache / Set size = 64 / 2 = 32 sets = 2^5 sets
Therefore no of bits in set = 5 bits
Number of bits in tag = Number of bits in physical address – (Number of bits in set number + Number of bits in block offset)
= 17 bits – (5 bits + 8 bits) = 17 bits – 13 bits = 4 bits

<Main Memory Address - 17 bits> = |Tag - 4 bits | Set - 5 bits | Word-offset - 8 bits|
"""
def direct_mapping():
    index_bits=int(math.log(cache_lines,2))
    print("index bits: ", index_bits)

    tag_bits=address_bits-index_bits-wordoffset_bits
    print("tag bits:", tag_bits)
 
    #data wordAdrr binAddr tag index offset hit/miss
    cache=[]
    for i in range(cache_lines):
        cache.append([0,0,0,0,0,0,0])
         

    ch="true"
    while(ch=="true"):
        command=input().split()  
        print(command)
        if(command[0]=="quit"):
            exit()

        if(command[0]=="printcache"):
            print(cache)

        if(command[0]=="read"):
            word_addr=int(command[1])  #address to be read in cache
            bin_addr=dec_to_bin(word_addr,address_bits)
            tag=bin_addr[:tag_bits]
            index=bin_addr[tag_bits:tag_bits+index_bits]
            offset=bin_addr[tag_bits+index_bits:]
            data=rand_byte()
            print(data,word_addr,bin_addr, tag, index, offset)
        
        if(command[0]=="write"):
            address=command[1]
            data=command[2]


def associative_mapping():
    tag_bits=address_bits-wordoffset_bits
    print("tag bits:", tag_bits)

def k_associative_mapping():
    set_size =int( input("Input set size: "))
    total_sets=cache_lines//set_size
    print("total sets: ", total_sets)

    set_bits=int(math.log(total_sets,2))
    print("set bits: ", set_bits)

    tag_bits=address_bits-set_bits-wordoffset_bits
    print("tag bits:",tag_bits)

def dec_to_bin(integer,width):
    """Returns a binary string representation of an integer value
    If integer is 15, width is 5. It returns 01111"""
    return "{0:0>{1}b}".format(integer, width)

def bin_to_dec(n): 
    return int(n,2) 


def rand_byte():
    """Returns a random byte between 0 to 255"""
    return random.randint(0,255)


"""
print("Input in power of 2 means that if you input 7, it would mean 2^7 bytes")
cache_size =int( input("Input cache size in power of 2 bytes: "))
block_size = int(input("Input block size in power of 2 bytes: "))
memory_size =int(input("Input main memory size in power of 2 bytes: "))"""

cache_size=2**14
block_size=2**8
memory_size=2**17

#Finding no of cache lines
cache_lines=cache_size//block_size
print("cache lines: ",cache_lines)

#Finding no of bits required in pyhsical address
address_bits=int(math.log(memory_size,2))
print("address bits:  ",address_bits)

#Finding no of bits in word-offset
wordoffset_bits=int(math.log(block_size,2))
print("word-offset bits: ",wordoffset_bits)

#Take user input to determine the type of mapping they want
#mapping=int(input(" Enter the desired number \n 0 for Direct Mapping \n 1 for Fully Associative Mapping \n 2 for Set Associative Mapping\n "))
mapping=0
if(mapping==0):
    direct_mapping()

if(mapping==1):
    associative_mapping()

if(mapping==2):
    k_associative_mapping()

    


