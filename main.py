import math
import random
import os

#It is for a 32 bit system
  #TODO handle invalid address input part
  #TODO mention arraylist size limitation when taking address. 32 bits address ka data pura nhi store kar payga
  #TODO Assume that the size of each memory word is 1 byte. 

def direct_mapping():
    index_bits=int(math.log(cache_lines,2))
    print("index bits: ", index_bits)

    tag_bits=address_bits-index_bits-offset_bits
    print("tag bits:", tag_bits)
 
    #  wordAdrr binAddr tag index offset hit/miss
    valid=[0]*cache_lines   #table column
    tag=['-']*cache_lines   #table column
    data=[0]*cache_lines    #table column #decimal
    dirty=[0]*cache_lines   #table column

    print("\n-----------------------------------------------------------------------")
    print("                          CACHE TABLE")
    print("-----------------------------------------------------------------------")
    print("Index\tValid\tTag\t\tData(Decimal)\t\tDirty Bit")
    for i in range(cache_lines):
        print(" ",i,"\t ",valid[i],"\t",tag[i],"\t\t    ",data[i],"\t\t\t   ",dirty[i])


    def direct_table():
        print("\n-----------------------------------------------------------------------")
        print("                          CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines):
            print(i,"\t",valid[i],"\t",tag[i],"\t",data[i],"\t",dirty[i])

    def update_table():
        tag[dec_index]=bin_tag  
        if(dec_address==0):
            dec_block_no=0
        else:
            dec_block_no=dec_address//block_size
        
        if(hit_flag==False and (command[0]=="read" or command[0]=="READ")):
            print("BLOCK "+ str(dec_block_no) + " with offset 0 to "+str(block_size-1) +" is transferred to cache at index",dec_index)
        
        if(hit_flag==False and (command[0]=="write" or command[0]=="WRITE")):
            print("BLOCK "+ str(dec_block_no) + " with offset 0 to "+str(block_size-1) +" is transferred to cache at index",dec_index)
            print("Content is updated based on Write Policy")

        data[dec_index]="BLOCK "+ str(dec_block_no)
        direct_table()
    

    
    #os.system('clear')

    ch="true"
    hit_flag=False
    while(ch=="true"):
        hit_flag=False  #True if cache hit. False if cache miss
        command=input().split()  
        #os.system('clear')
        print("\n\n\n")
        if(command[0]=="quit" or command[0]=="QUIT"):
            exit()

        if(command[0]=="read" or command[0]=="READ"):
            dec_address=int(command[1])   #Format of read instruction is "read address"  
            if(dec_address>=2**address_bits):
                print("Invalid address")
                continue
            print("read",dec_address)
            print("Address bits:",address_bits)
            print()
            print("Instruction Breakdown")
            print("Tag(",tag_bits,"bits )\t\tIndex(",index_bits,"bits )\t\tOffset(",offset_bits,"bits )")

            """Determining the binary string for tag, index and offset by converting input address to a binary string"""
            bin_address=dec_to_bin(dec_address,address_bits)    #input address is being converted to a binary string
            bin_tag=bin_address[:tag_bits]      #in binary
            bin_index=bin_address[tag_bits:tag_bits+index_bits] #in binary
            bin_offset=bin_address[tag_bits+index_bits:]    #in binary
            print(bin_tag,"\t",bin_index,"\t\t", bin_offset)
            dec_index=bin_to_dec(bin_index) #in decimal
            print("Index in decimal: ",dec_index )
            print()

            if(valid[dec_index]==0):   
                hit_flag=False #cache miss
                print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                valid[dec_index]=1  #Make the valid bit as  1
                update_table()
               
            
            elif(valid[dec_index]==1):
                if(bin_tag == tag[dec_index]):
                    hit_flag=True   #cache hit
                    print("Cache HIT!")
                    update_table()
                else:
                    hit_flag=False #cache miss
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    print("Address",dec_address,"will replace the block at index", dec_index)
                    update_table()

     
        if(command[0]=="write" or command[0]=="WRITE"):
            if(len(command)<3):
                print("Invalid input")
                continue
            dec_address=int(command[1])
            dec_data=int(command[2])

            if(dec_address>=2**address_bits):
                print("Invalid address")
                continue

            print("write ",dec_address,dec_data)
            print("Address bits:",address_bits)
            print()
            print("Instruction Breakdown")
            print("Tag(",tag_bits,"bits )\t\tIndex(",index_bits,"bits )\t\tOffset(",offset_bits,"bits )")

            """Determining the binary string for tag, index and offset by converting input address to a binary string"""
            bin_address=dec_to_bin(dec_address,address_bits)    #input address is being converted to a binary string
            bin_tag=bin_address[:tag_bits]      #in binary
            bin_index=bin_address[tag_bits:tag_bits+index_bits] #in binary
            bin_offset=bin_address[tag_bits+index_bits:]    #in binary
            print(bin_tag,"\t",bin_index,"\t\t", bin_offset)
            dec_index=bin_to_dec(bin_index) #in decimal
            print("Index in decimal: ",dec_index )
            print()

            if(valid[dec_index]==0):   
                hit_flag=False #cache miss
                print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                valid[dec_index]=1  #Make the valid bit as  1
                update_table()
               
            
            elif(valid[dec_index]==1):
                if(bin_tag == tag[dec_index]):
                    hit_flag=True   #cache hit
                    print("Cache HIT!")
                    print("Content is updated based on Write Policy")
                    update_table()
                else:
                    hit_flag=False #cache miss
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    print("Address",dec_address,"will replace the block at index", dec_index)
                    update_table()



def associative_mapping():
    tag_bits=address_bits-offset_bits
    print("tag bits:", tag_bits)

    #  wordAdrr binAddr tag index offset hit/miss
    valid=[0]*cache_lines   #table column
    tag=['-']*cache_lines   #table column
    data=[0]*cache_lines    #table column #decimal
    dirty=[0]*cache_lines   #table column

    print("\n-----------------------------------------------------------------------")
    print("                          CACHE TABLE")
    print("-----------------------------------------------------------------------")
    print("Index\tValid\tTag\t\tData(Decimal)\t\tDirty Bit")
    for i in range(cache_lines):
        print(" ",i,"\t ",valid[i],"\t",tag[i],"\t\t    ",data[i],"\t\t\t   ",dirty[i])


    def associative_table():
        print("\n-----------------------------------------------------------------------")
        print("                          CACHE TABLE")
        print("-----------------------------------------------------------------------")
        print("Index\tValid\t\tTag\t\tData(Decimal)\tDirty Bit")
        for i in range(cache_lines):
            print(i,"\t",valid[i],"\t",tag[i],"\t",data[i],"\t",dirty[i])
        print("lru: ",lru)

    def update_table():
        tag[dec_index]=bin_tag  
        if(dec_address==0):
            dec_block_no=0
        else:
            dec_block_no=dec_address//block_size
        
        if(hit_flag==False and (command[0]=="read" or command[0]=="READ")):
            print("BLOCK "+ str(dec_block_no) + " with offset 0 to "+str(block_size-1) +" is transferred to cache at index",dec_index)
        
        if(hit_flag==False and (command[0]=="write" or command[0]=="WRITE")):
            print("BLOCK "+ str(dec_block_no) + " with offset 0 to "+str(block_size-1) +" is transferred to cache at index",dec_index)
            print("Content is updated based on Write Policy")

        try:
            lru.remove(dec_index)
        except:
            pass
        lru.append(dec_index)
        data[dec_index]="BLOCK "+ str(dec_block_no)
        associative_table()
    

    
    ch="true"
    hit_flag=False
    cl_cnt=0
    lru=[]  #stores least recently used index in the cache table. The rightmost is the MOST recently used. 0th one is lru
    while(ch=="true"):
        hit_flag=False  #True if cache hit. False if cache miss
        command=input().split()  
        #os.system('clear')
        print("\n\n\n")
        if(command[0]=="quit" or command[0]=="QUIT"):
            exit()

        if(command[0]=="read" or command[0]=="READ"):
            dec_address=int(command[1])   #Format of read instruction is "read address"  
            if(dec_address>=2**address_bits):
                print("Invalid address")
                continue
            print("read",dec_address)
            print("Address bits:",address_bits)
            print()
            print("Instruction Breakdown")
            print("Tag(",tag_bits,"bits )\t\tOffset(",offset_bits,"bits )")

            #Determining the binary string for tag, index and offset by converting input address to a binary string
            bin_address=dec_to_bin(dec_address,address_bits)    #input address is being converted to a binary string
            bin_tag=bin_address[:tag_bits]      #in binary
            bin_offset=bin_address[tag_bits:]    #in binary
            print(bin_tag,"\t\t", bin_offset)
            print()

            if bin_tag in tag:  #Cache hit
                hit_flag=True
                dec_index=tag.index(bin_tag)
                print("Cache HIT! at index", dec_index)
                update_table()

            
            if(cl_cnt<cache_lines): #cache lines are not all filled yet. So we start filling in order from index 0              
                if bin_tag not in tag:  #Cache miss
                    hit_flag=False
                    dec_index=cl_cnt
                    cl_cnt+=1
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    valid[dec_index]=1  #Make the valid bit as  1
                    update_table()
            
            if(cl_cnt>=cache_lines):   #all cache lines are filled. Now in case of a miss we need to through stuff out
                if bin_tag not in tag: #Cache miss
                    hit_flag=False
                    dec_index=lru.pop(0)
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    valid[dec_index]=1  #Make the valid bit as  1
                    update_table()

     
        if(command[0]=="write" or command[0]=="WRITE"):
            if(len(command)<3):
                print("Invalid input")
                continue
            dec_address=int(command[1])
            dec_data=int(command[2])

            if(dec_address>=2**address_bits):
                print("Invalid address")
                continue

            print("read",dec_address)
            print("Address bits:",address_bits)
            print()
            print("Instruction Breakdown")
            print("Tag(",tag_bits,"bits )\t\tOffset(",offset_bits,"bits )")

            #Determining the binary string for tag, index and offset by converting input address to a binary string
            bin_address=dec_to_bin(dec_address,address_bits)    #input address is being converted to a binary string
            bin_tag=bin_address[:tag_bits]      #in binary
            bin_offset=bin_address[tag_bits:]    #in binary
            print(bin_tag,"\t\t", bin_offset)
            print()

            if bin_tag in tag:  #Cache hit
                hit_flag=True
                dec_index=tag.index(bin_tag)
                print("Cache HIT! at index", dec_index)
                print("Content is updated based on Write Policy")
                update_table()

            
            if(cl_cnt<cache_lines): #cache lines are not all filled yet. So we start filling in order from index 0              
                if bin_tag not in tag:  #Cache miss
                    hit_flag=False
                    dec_index=cl_cnt
                    cl_cnt+=1
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    valid[dec_index]=1  #Make the valid bit as  1
                    update_table()
            
            if(cl_cnt>=cache_lines):   #all cache lines are filled. Now in case of a miss we need to through stuff out
                if bin_tag not in tag: #Cache miss
                    hit_flag=False
                    dec_index=lru.pop(0)
                    print("Cache MISS!! - Address not found\nCache table is updated accordingly")
                    print("Address",dec_address,"will replace the block at index", dec_index)
                    valid[dec_index]=1  #Make the valid bit as  1
                    update_table()
            

def k_associative_mapping():
    set_size =int( input("Input set size: "))
    total_sets=cache_lines//set_size
    print("total sets: ", total_sets)

    set_bits=int(math.log(total_sets,2))
    print("set bits: ", set_bits)

    tag_bits=address_bits-set_bits-offset_bits
    print("tag bits:",tag_bits)

def dec_to_bin(integer,width):
    return "{0:0>{1}b}".format(integer, width)

def bin_to_dec(n): 
    return int(n,2) 

#cache_lines =int( input("Input cache lines in power of 2: "))
#block_size = int(input("Input block size in power of 2 bytes: "))


cache_lines=4
block_size=4
address_bits=11

"""
block_size=64
cache_lines=128
address_bits=32"""


print("cache lines: ",cache_lines)
print("address bits: ",address_bits)

#Finding no of bits in offset
offset_bits=int(math.log(block_size,2))
print("offset bits: ",offset_bits)

#Take user input to determine the type of mapping they want
#mapping=int(input(" Enter the desired number \n 0 for Direct Mapping \n 1 for Fully Associative Mapping \n 2 for Set Associative Mapping\n "))
mapping=1
if(mapping==0):
    direct_mapping()

if(mapping==1):
    associative_mapping()

if(mapping==2):
    k_associative_mapping()

    


