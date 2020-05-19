# Bonus Assignment
# Samiksha Modi
# Roll No 2019331

import math
import random
import os

# It is for a 32 bit system by default


def associative_mapping():
    tag_bits = address_bits-offset_bits
    print("tag bits:", tag_bits)

    #  wordAdrr binAddr tag index offset hit/miss
    valid = [0]*cache_lines  # table column
    tag = ['-']*cache_lines  # table column
    data = [0]*cache_lines  # table column #decimal
    dirty = [0]*cache_lines  # table column

    print("\n-----------------------------------------------------------------------")
    print("                    LEVEL 1 CACHE TABLE")
    print("-----------------------------------------------------------------------")
    print("Index\tValid\tTag\t\tData(Decimal)\t\tDirty Bit")
    for i in range(cache_lines):
        print(" ", i, "\t ", valid[i], "\t", tag[i],
              "\t\t    ", data[i], "\t\t\t   ", dirty[i])

    def associative_table():
        print("\n-----------------------------------------------------------------------")
        print("                LEVEL 1 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines):
            print(i, "\t", valid[i], "\t", tag[i],
                  "\t", data[i], "\t", dirty[i])
        print("lru: ", lru)

    def update_table():
        tag[dec_index] = bin_tag
        if(dec_address == 0):
            dec_block_no = 0
        else:
            dec_block_no = dec_address//block_size

        if(hit_flag == False and (command[0] == "read" or command[0] == "READ")):
            print("\nBLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 1 at index", dec_index)

        if(hit_flag == False and (command[0] == "write" or command[0] == "WRITE")):
            print("\nBLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 1 at index", dec_index)
            print("Content is updated based on Write Policy")

        try:
            lru.remove(dec_index)
        except:
            pass
        lru.append(dec_index)
        data[dec_index] = "BLOCK " + str(dec_block_no)
        associative_table()

    ch = "true"
    hit_flag = False
    cl_cnt = 0
    lru = []  # stores least recently used index in the cache table. The rightmost is the MOST recently used. 0th one is lru
    while(ch == "true"):
        hit_flag = False  # True if cache hit. False if cache miss
        command = input().split()
        # os.system('clear')
        print("\n\n\n")
        if(command[0] == "quit" or command[0] == "QUIT"):
            exit()

        if(command[0] == "read" or command[0] == "READ"):
            # Format of read instruction is "read address"
            dec_address = int(command[1])
            if(dec_address >= 2**address_bits):
                print("Invalid address")
                continue
            print("read", dec_address)
            print("Address bits:", address_bits)
            print()
            print("Instruction Breakdown Level 1")
            print("Tag(", tag_bits, "bits )\t\tOffset(", offset_bits, "bits )")

            # Determining the binary string for tag, index and offset by converting input address to a binary string
            # input address is being converted to a binary string
            bin_address = dec_to_bin(dec_address, address_bits)
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_offset = bin_address[tag_bits:]  # in binary
            print(bin_tag, "\t\t", bin_offset)
            print()

            if bin_tag in tag:  # Cache hit
                hit_flag = True
                dec_index = tag.index(bin_tag)
                print("Cache HIT at Level 1! at index", dec_index)
                update_table()

            # cache lines are not all filled yet. So we start filling in order from index 0
            if(cl_cnt < cache_lines):
                if bin_tag not in tag:  # Cache miss
                    hit_flag = False
                    dec_index = cl_cnt
                    cl_cnt += 1
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    valid[dec_index] = 1  # Make the valid bit as  1
                    update_table()

            # all cache lines are filled. Now in case of a miss we need to through stuff out
            if(cl_cnt >= cache_lines):
                if bin_tag not in tag:  # Cache miss
                    hit_flag = False
                    dec_index = lru.pop(0)
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    print("\nAddress", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
                    valid[dec_index] = 1  # Make the valid bit as  1
                    update_table()

        if(command[0] == "write" or command[0] == "WRITE"):
            if(len(command) < 3):
                print("Invalid input")
                continue
            dec_address = int(command[1])
            dec_data = int(command[2])

            if(dec_address >= 2**address_bits):
                print("Invalid address")
                continue

            print("read", dec_address)
            print("Address bits:", address_bits)
            print()
            print("Instruction Breakdown Level 1")
            print("Tag(", tag_bits, "bits )\t\tOffset(", offset_bits, "bits )")

            # Determining the binary string for tag, index and offset by converting input address to a binary string
            # input address is being converted to a binary string
            bin_address = dec_to_bin(dec_address, address_bits)
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_offset = bin_address[tag_bits:]  # in binary
            print(bin_tag, "\t\t", bin_offset)
            print()

            if bin_tag in tag:  # Cache hit
                hit_flag = True
                dec_index = tag.index(bin_tag)
                print("Cache HIT at Level 1! at index", dec_index)
                print("Content is updated based on Write Policy")
                update_table()

            # cache lines are not all filled yet. So we start filling in order from index 0
            if(cl_cnt < cache_lines):
                if bin_tag not in tag:  # Cache miss
                    hit_flag = False
                    dec_index = cl_cnt
                    cl_cnt += 1
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    valid[dec_index] = 1  # Make the valid bit as  1
                    update_table()

            # all cache lines are filled. Now in case of a miss we need to through stuff out
            if(cl_cnt >= cache_lines):
                if bin_tag not in tag:  # Cache miss
                    hit_flag = False
                    dec_index = lru.pop(0)
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    print("Address", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
                    valid[dec_index] = 1  # Make the valid bit as  1
                    update_table()


def level2(dec_address):
    global valid2
    global tag2
    global data2
    global dirty2
    global lru2
    global cl_cnt2
    tag_bits = address_bits-offset_bits
    #print("tag bits:", tag_bits)

    def associative_table():
        print("\n-----------------------------------------------------------------------")
        print("               LEVEL 2 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines2):
            print(i, "\t", valid2[i], "\t", tag2[i],
                  "\t", data2[i], "\t", dirty2[i])
        print("lru: ", lru2)

    def update_table():
        tag2[dec_index] = bin_tag
        if(dec_address == 0):
            dec_block_no = 0
        else:
            dec_block_no = dec_address//block_size

        if(hit_flag == False):
            print("BLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 2 at index", dec_index)

        try:
            lru2.remove(dec_index)
        except:
            pass
        lru2.append(dec_index)
        data2[dec_index] = "BLOCK " + str(dec_block_no)
        associative_table()

    #print("Address bits:", address_bits)
    print()
    print("Instruction Breakdown Level 2")
    print("Tag(", tag_bits, "bits )\t\tOffset(", offset_bits, "bits )")

    # Determining the binary string for tag, index and offset by converting input address to a binary string
    # input address is being converted to a binary string
    bin_address = dec_to_bin(dec_address, address_bits)
    bin_tag = bin_address[:tag_bits]  # in binary
    bin_offset = bin_address[tag_bits:]  # in binary
    print(bin_tag, "\t\t", bin_offset)
    print()

    if bin_tag in tag2:  # Cache hit
        hit_flag = True
        dec_index = tag2.index(bin_tag)
        print("Cache HIT at Level 2! at index", dec_index)
        update_table()

    # cache lines are not all filled yet. So we start filling in order from index 0
    if(cl_cnt2 < cache_lines2):
        if bin_tag not in tag2:  # Cache miss
            hit_flag = False
            dec_index = cl_cnt2
            cl_cnt2 += 1
            print(
                "Cache MISS at Level 2!! - Address not found\nBoth caches are updated accordingly")
            valid2[dec_index] = 1  # Make the valid bit as  1
            update_table()

    # all cache lines are filled. Now in case of a miss we need to throw stuff out
    if(cl_cnt2 >= cache_lines2):
        if bin_tag not in tag2:  # Cache miss
            hit_flag = False
            dec_index = lru2.pop(0)
            print(
                "Cache MISS at Level 2!! - Address not found\nBoth caches are updated accordingly")
            print("Address", dec_address,
                  "will replace the block at index", dec_index, "in Level 2")
            valid2[dec_index] = 1  # Make the valid bit as  1
            update_table()


def dec_to_bin(integer, width):
    return "{0:0>{1}b}".format(integer, width)


def bin_to_dec(n):
    return int(n, 2)


cache_lines = int(input("Input cache lines in level 1 in power of 2: "))
block_size = int(input("Input block size in power of 2 bytes: "))

try:
    address_bits = int(
        input("Input no of bits in memory address in power of 2: "))
except:
    address_bits = 32

"""
cache_lines = 8
block_size = 4
address_bits = 11"""

cache_lines2 = cache_lines*2  # Level 2

print("cache lines level 1: ", cache_lines)
print('cache lines level 2: ', cache_lines2)
print("address bits: ", address_bits)

valid2 = [0]*cache_lines2  # table column
tag2 = ['-']*cache_lines2  # table column
data2 = [0]*cache_lines2  # table column
dirty2 = [0]*cache_lines2  # table column
lru2 = []
cl_cnt2 = 0


# Finding no of bits in offset
offset_bits = int(math.log(block_size, 2))
print("offset bits: ", offset_bits)
associative_mapping()
