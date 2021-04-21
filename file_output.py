

# with open("nary_problems/try1.csp", "w") as file:
        
#     file.write("Add " +  "a word" + "\n")
#     file.write("Add a word2")

# a = [(1,2,3,4),(1,2,3,4),(1,2,3,4)]

# def modify_tuple(ori_tuple: tuple, offsets: list):
#     temp = list(ori_tuple)
#     for index, offset in enumerate(offsets):
#         temp[index] = ori_tuple[index + offset]
#     return tuple(temp)

# b = [('c1','b','d'),('c2','b','d'),('c3','b','d'),('c4','b','d')]
# print(set(map(lambda x :modify_tuple(x, [1,-1, 0]), b)))
# print(set([modify_tuple(x, [1,-1, 0]) for x in b]))

import itertools
test = "num"
if test == "s":
    print(set(itertools.permutations(['w'], 1)))  
    print(set(itertools.permutations(['w','w','s'], 2)))
    print(set(itertools.permutations(['w','w','w', 's', 's'], 3)))
    print(set(itertools.permutations(['w','w','w','w', 's', 's', 's'], 4)))   
elif test == "m":
    print(set(itertools.permutations(['w', 'p'], 2)))
    print("____________________________________________________")
    print(set(itertools.permutations(['w','w', 'p', 'p'], 3)))# w至少1个最多2个，p至少1个最多2个，s最多1个，
    print(set(itertools.permutations(['w', 'p', 's'], 3)))
    print("____________________________________________________")
    print(set(itertools.permutations(['w','w','w', 'p', 'p','p'], 4)))
    print(set(itertools.permutations(['w','p','s','s'], 4)))
    print(set(itertools.permutations(['w','p','p','s'], 4)))
    print(set(itertools.permutations(['w','w','p','s'], 4)))
else:
    print(set(itertools.permutations(['w','p','p','s','s','s','s'], 4)))