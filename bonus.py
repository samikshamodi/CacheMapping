
# Take user input to determine the type of mapping they want
mapping = int(input(
    " Enter the desired number \n 0 for Direct Mapping \n 1 for Fully Associative Mapping \n 2 for Set Associative Mapping\n "))
if(mapping==0):
    import direct
if mapping==1:
    import associative
if mapping==2:
    import kassociative