# Bonus Assignment
# Samiksha Modi
# Roll No 2019331

import math
import random
import os


def direct_mapping():
    index_bits = int(math.log(cache_lines, 2))
    print("index bits level 1: ", index_bits)

    tag_bits = address_bits-index_bits-offset_bits
    print("tag bits level 1:", tag_bits)

    #  wordAdrr binAddr tag index offset hit/miss
    valid = [0]*cache_lines  # table column
    tag = ['-']*cache_lines  # table column
    data = [0]*cache_lines  # table column #decimal
    dirty = [0]*cache_lines  # table column

    print("\n-----------------------------------------------------------------------")
    print("                     LEVEL 1 CACHE TABLE")
    print("-----------------------------------------------------------------------")
    print("Index\tValid\tTag\t\tData(Decimal)\t\tDirty Bit")
    for i in range(cache_lines):
        print(" ", i, "\t ", valid[i], "\t", tag[i],
              "\t\t    ", data[i], "\t\t\t   ", dirty[i])

    def direct_table():
        print("\n-----------------------------------------------------------------------")
        print("                  LEVEL 1 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines):
            print(i, "\t", valid[i], "\t", tag[i],
                  "\t", data[i], "\t", dirty[i])

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

        data[dec_index] = "BLOCK " + str(dec_block_no)
        direct_table()

    # os.system('clear')

    ch = "true"
    hit_flag = False
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
            print("Tag(", tag_bits, "bits )\t\tIndex(", index_bits,
                  "bits )\t\tOffset(", offset_bits, "bits )")

            """Determining the binary string for tag, index and offset by converting input address to a binary string"""
            bin_address = dec_to_bin(
                dec_address, address_bits)  # input address is being converted to a binary string
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
            bin_offset = bin_address[tag_bits+index_bits:]  # in binary
            print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
            dec_index = bin_to_dec(bin_index)  # in decimal
            print("Index in decimal: ", dec_index)
            print()

            if(valid[dec_index] == 0):
                hit_flag = False  # cache miss
                print(
                    "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                level2(dec_address)
                valid[dec_index] = 1  # Make the valid bit as  1
                update_table()

            # gotta throw stuff out in case of a miss
            elif(valid[dec_index] == 1):
                if(bin_tag == tag[dec_index]):
                    hit_flag = True  # cache hit
                    print("Cache HIT at Level 1!")
                    update_table()
                else:
                    hit_flag = False  # cache miss
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    print("\nAddress", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
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

            print("write ", dec_address, dec_data)
            print("Address bits:", address_bits)
            print()
            print("Instruction Breakdown Level 1")
            print("Tag(", tag_bits, "bits )\t\tIndex(", index_bits,
                  "bits )\t\tOffset(", offset_bits, "bits )")

            """Determining the binary string for tag, index and offset by converting input address to a binary string"""
            bin_address = dec_to_bin(
                dec_address, address_bits)  # input address is being converted to a binary string
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
            bin_offset = bin_address[tag_bits+index_bits:]  # in binary
            print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
            dec_index = bin_to_dec(bin_index)  # in decimal
            print("Index in decimal: ", dec_index)
            print()

            if(valid[dec_index] == 0):
                hit_flag = False  # cache miss
                print(
                    "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                level2(dec_address)
                valid[dec_index] = 1  # Make the valid bit as  1
                update_table()

            elif(valid[dec_index] == 1):
                if(bin_tag == tag[dec_index]):
                    hit_flag = True  # cache hit
                    print("Cache HIT at Level 1!")
                    print("Content is updated based on Write Policy")
                    update_table()
                else:
                    hit_flag = False  # cache miss
                    print(
                        "Cache MISS!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    print("\nAddress", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
                    update_table()


def level2(dec_address):
    global valid2
    global tag2
    global data2
    global dirty2

    index_bits = int(math.log(cache_lines2, 2))
    #print("index bits level 2: ", index_bits)

    tag_bits = address_bits-index_bits-offset_bits
    #print("tag bits level 2:", tag_bits)

    def direct_table():
        print("\n-----------------------------------------------------------------------")
        print("                  LEVEL 2 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines2):
            print(i, "\t", valid2[i], "\t", tag2[i],
                  "\t", data2[i], "\t", dirty2[i])

    def update_table():
        tag2[dec_index] = bin_tag
        if(dec_address == 0):
            dec_block_no = 0
        else:
            dec_block_no = dec_address//block_size

        if(hit_flag == False):
            print("BLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 2 at index", dec_index)

        data2[dec_index] = "BLOCK " + str(dec_block_no)
        direct_table()

    #print("Address bits:", address_bits)
    print()
    print("Instruction Breakdown Level 2")
    print("Tag(", tag_bits, "bits )\t\tIndex(", index_bits,
          "bits )\t\tOffset(", offset_bits, "bits )")

    """Determining the binary string for tag, index and offset by converting input address to a binary string"""
    bin_address = dec_to_bin(
        dec_address, address_bits)  # input address is being converted to a binary string
    bin_tag = bin_address[:tag_bits]  # in binary
    bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
    bin_offset = bin_address[tag_bits+index_bits:]  # in binary
    print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
    dec_index = bin_to_dec(bin_index)  # in decimal
    print("Index in decimal: ", dec_index)
    print()

    if(valid2[dec_index] == 0):
        hit_flag = False  # cache miss
        print(
            "Cache MISS at Level 2!! - Address not found\nBoth caches are updated accordingly")
        valid2[dec_index] = 1  # Make the valid bit as  1
        update_table()

    elif(valid2[dec_index] == 1):
        if(bin_tag == tag2[dec_index]):
            hit_flag = True  # cache hit
            print("Cache HIT at Level 2! Data is loaded to Cache Level 1")
            update_table()
        else:
            hit_flag = False  # cache miss
            print(
                "Cache MISS at Level 2!! - Address not found\nBoth cache are updated accordingly")
            print("Address", dec_address,
                  "will replace the block at index", dec_index, "in Level 2")
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

"""cache_lines = 8
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


# Finding no of bits in offset
offset_bits = int(math.log(block_size, 2))
print("offset bits: ", offset_bits)
direct_mapping()
