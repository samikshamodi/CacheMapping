# Bonus Assignment
# Samiksha Modi
# Roll No 2019331

import math
import random
import os

# It is for a 32 bit system by default


def k_associative_mapping():
    index_bits = int(math.log(total_sets, 2))
    print("set bits: ", index_bits)
    if(index_bits == 0):
        print("Invalid Configuration")
        print("Set bits is 0. Fully Associative Mapping Suggested")
        exit()

    tag_bits = address_bits-index_bits-offset_bits
    print("tag bits:", tag_bits)

    #  wordAdrr binAddr tag index offset hit/miss
    valid = [0]*(total_sets)  # table column
    tag = ['-']*(total_sets)  # table column
    data = [0]*(total_sets)  # table column
    dirty = [0]*(total_sets)  # table column
    lru = [0]*(total_sets)
    for i in range(total_sets):
        valid[i] = [0]*set_size
        tag[i] = ['-']*set_size
        data[i] = [0]*set_size
        dirty[i] = [0]*set_size
        # stores least recently used index in the cache table. The rightmost is the MOST recently used. 0th one is lru
        lru[i] = []*set_size

    print("\n-----------------------------------------------------------------------")
    print("                  LEVEL 1 CACHE TABLE")
    print("-----------------------------------------------------------------------")
    print("Index\tValid\tTag\t\tData(Decimal)\t\tDirty Bit")
    for i in range(total_sets):
        for j in range(set_size):
            print(" ", i, "\t ", valid[i][j], "\t", tag[i][j], "\t\t    ", data[i][j],
                  "\t\t\t   ", dirty[i][j])

    def k_associative_table():
        print("\n-----------------------------------------------------------------------")
        print("               LEVEL 1 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(total_sets):
            for j in range(set_size):
                print(" ", i, "\t ", valid[i][j], "\t", tag[i][j], "\t\t    ", data[i][j],
                      "\t\t\t   ", dirty[i][j])
        print("lru:", lru)

    def update_table():
        tag[dec_index][way_index] = bin_tag
        if(dec_address == 0):
            dec_block_no = 0
        else:
            dec_block_no = dec_address//block_size

        if(hit_flag == False and (command[0] == "read" or command[0] == "READ")):
            print("BLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 1 at index", dec_index)

        if(hit_flag == False and (command[0] == "write" or command[0] == "WRITE")):
            print("BLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 1 at index", dec_index)
            print("Content is updated based on Write Policy")

        try:
            lru[dec_index].remove(way_index)
        except:
            pass
        lru[dec_index].append(way_index)
        data[dec_index][way_index] = "BLOCK " + str(dec_block_no)
        k_associative_table()

    def find_in_list(lst, s):
        list_no = 0
        pos = 0
        for x in range(0, len(lst)):
            try:
                pos = lst[x].index(s)
                break
            except:
                pass
        return pos
    ch = "true"
    hit_flag = False
    way_cnt = [0]*total_sets
    way_index = 0
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

            # Determining the binary string for tag, index and offset by converting input address to a binary string
            # input address is being converted to a binary string
            bin_address = dec_to_bin(dec_address, address_bits)
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
            bin_offset = bin_address[tag_bits+index_bits:]  # in binary
            print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
            dec_index = bin_to_dec(bin_index)  # in decimal
            print("Index in decimal: ", dec_index)
            print()

            if bin_tag in tag[dec_index]:  # Cache hit
                hit_flag = True
                # way_index=tag[dec_index].find(bin_tag)
                way_index = find_in_list(tag, bin_tag)
                print("Cache HIT at Level 1! at index", dec_index)
                update_table()

            # if all the 4 sets are not filled at a particular index
            if(way_cnt[dec_index] < set_size):
                if(bin_tag not in tag[dec_index]):  # Cache miss
                    hit_flag = False
                    way_index = way_cnt[dec_index]
                    way_cnt[dec_index] += 1
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearhing in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    valid[dec_index][way_index] = 1  # Make valid bit as 1
                    update_table()

            if(way_cnt[dec_index] >= set_size):  # All the 4 ways have been filled
                if bin_tag not in tag[dec_index]:  # Cache miss
                    hit_flag = False
                    way_index = lru[dec_index].pop(0)
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 1
                    level2(dec_address)
                    print("Address", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
                    valid[dec_index][way_index] = 1  # Make valid bit as 1
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
            print("Tag(", tag_bits, "bits )\t\tIndex(", index_bits,
                  "bits )\t\tOffset(", offset_bits, "bits )")

            # Determining the binary string for tag, index and offset by converting input address to a binary string
            # input address is being converted to a binary string
            bin_address = dec_to_bin(dec_address, address_bits)
            bin_tag = bin_address[:tag_bits]  # in binary
            bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
            bin_offset = bin_address[tag_bits+index_bits:]  # in binary
            print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
            dec_index = bin_to_dec(bin_index)  # in decimal
            print("Index in decimal: ", dec_index)
            print()

            if bin_tag in tag[dec_index]:  # Cache hit
                hit_flag = True
                # way_index=tag[dec_index].find(bin_tag)
                way_index = find_in_list(tag, bin_tag)
                print("Cache HIT at Level 1! at index", dec_index)
                print("Content is updated based on Write Policy")
                update_table()

            # if all the 4 sets are not filled at a particular index
            if(way_cnt[dec_index] < set_size):
                if(bin_tag not in tag[dec_index]):  # Cache miss
                    hit_flag = False
                    way_index = way_cnt[dec_index]
                    way_cnt[dec_index] += 1
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    valid[dec_index][way_index] = 1  # Make valid bit as 1
                    update_table()

            if(way_cnt[dec_index] >= set_size):  # All the 4 ways have been filled
                if bin_tag not in tag[dec_index]:  # Cache miss
                    hit_flag = False
                    way_index = lru[dec_index].pop(0)
                    print(
                        "Cache MISS at Level 1!! - Address not found\nSearching in Level 2")  # TODO goto level 2
                    level2(dec_address)
                    print("Address", dec_address,
                          "will replace the block at index", dec_index, "in Level 1")
                    valid[dec_index][way_index] = 1  # Make valid bit as 1
                    update_table()


def level2(dec_address):
    global valid2
    global tag2
    global data2
    global dirty2
    global lru2
    global way_cnt2
    global way_index2

    index_bits = int(math.log(total_sets2, 2))
    tag_bits = address_bits-index_bits-offset_bits

    def k_associative_table():
        print("\n-----------------------------------------------------------------------")
        print("               LEVEL 2 CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(total_sets2):
            for j in range(set_size):
                print(" ", i, "\t ", valid2[i][j], "\t", tag2[i][j], "\t\t    ", data2[i][j],
                      "\t\t\t   ", dirty2[i][j])
        print("lru:", lru2)

    def update_table():
        tag2[dec_index][way_index2] = bin_tag
        if(dec_address == 0):
            dec_block_no = 0
        else:
            dec_block_no = dec_address//block_size

        if(hit_flag == False):
            print("BLOCK " + str(dec_block_no) + " with offset 0 to " +
                  str(block_size-1) + " is transferred to cache Level 2 at index", dec_index)

        try:
            lru2[dec_index].remove(way_index2)
        except:
            pass
        lru2[dec_index].append(way_index2)
        data2[dec_index][way_index2] = "BLOCK " + str(dec_block_no)
        k_associative_table()

    def find_in_list(lst, s):
        list_no = 0
        pos = 0
        for x in range(0, len(lst)):
            try:
                pos = lst[x].index(s)
                break
            except:
                pass
        return pos

    #print("Address bits:", address_bits)
    print()
    print("Instruction Breakdown Level 2")
    print("Tag(", tag_bits, "bits )\t\tIndex(", index_bits,
          "bits )\t\tOffset(", offset_bits, "bits )")

    # Determining the binary string for tag, index and offset by converting input address to a binary string
    # input address is being converted to a binary string
    bin_address = dec_to_bin(dec_address, address_bits)
    bin_tag = bin_address[:tag_bits]  # in binary
    bin_index = bin_address[tag_bits:tag_bits+index_bits]  # in binary
    bin_offset = bin_address[tag_bits+index_bits:]  # in binary
    print(bin_tag, "\t", bin_index, "\t\t", bin_offset)
    dec_index = bin_to_dec(bin_index)  # in decimal
    print("Index in decimal: ", dec_index)
    print()

    if bin_tag in tag2[dec_index]:  # Cache hit
        hit_flag = True
        # way_index=tag[dec_index].find(bin_tag)
        way_index2 = find_in_list(tag2, bin_tag)
        print("Cache HIT at Level 2! at index", dec_index)
        update_table()

    # if all the 4 sets are not filled at a particular index
    if(way_cnt2[dec_index] < set_size):
        if(bin_tag not in tag2[dec_index]):  # Cache miss
            hit_flag = False
            way_index2 = way_cnt2[dec_index]
            way_cnt2[dec_index] += 1
            print(
                "Cache MISS at Level 2!! - Address not found\nBoth caches are updated accordingly")
            valid2[dec_index][way_index2] = 1  # Make valid bit as 1
            update_table()

    if(way_cnt2[dec_index] >= set_size):  # All the 4 ways have been filled
        if bin_tag not in tag2[dec_index]:  # Cache miss
            hit_flag = False
            way_index2 = lru2[dec_index].pop(0)
            print(
                "Cache MISS at Level 2!! - Address not found\nBoth caches are updated accordingly")
            print("Address", dec_address,
                  "will replace the block at index", dec_index, "in Level 2")
            valid2[dec_index][way_index2] = 1  # Make valid bit as 1
            update_table()


def dec_to_bin(integer, width):
    return "{0:0>{1}b}".format(integer, width)


def bin_to_dec(n):
    return int(n, 2)


cache_lines = int(input("Input cache lines in power of 2: "))
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

set_size = int(input("Input set size: "))
total_sets = cache_lines//set_size
print("total sets: ", total_sets)

cache_lines2 = cache_lines*2  # Level 2
total_sets2 = cache_lines2//set_size

print("cache lines level 1: ", cache_lines)
print('cache lines level 2: ', cache_lines2)
print("address bits: ", address_bits)

valid2 = [0]*(total_sets2)  # table column
tag2 = ['-']*(total_sets2)  # table column
data2 = [0]*(total_sets2)  # table column
dirty2 = [0]*(total_sets2)  # table column
lru2 = [0]*(total_sets2)
for i in range(total_sets2):
    valid2[i] = [0]*set_size
    tag2[i] = ['-']*set_size
    data2[i] = [0]*set_size
    dirty2[i] = [0]*set_size
    # stores least recently used index in the cache table. The rightmost is the MOST recently used. 0th one is lru
    lru2[i] = []*set_size
way_cnt2 = [0]*total_sets2
way_index2 = 0


# Finding no of bits in offset
offset_bits = int(math.log(block_size, 2))
print("offset bits: ", offset_bits)
k_associative_mapping()
