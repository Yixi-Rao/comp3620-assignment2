

# with open("nary_problems/try1.csp", "w") as file:
        
#     file.write("Add " +  "a word" + "\n")
#     file.write("Add a word2")

a = [(1,2,3,4),(1,2,3,4),(1,2,3,4)]

def modify_tuple(ori_tuple: tuple, offsets: list):
    temp = list(ori_tuple)
    for index, offset in enumerate(offsets):
        temp[index] = ori_tuple[index + offset]
    return tuple(temp)

b = [('c1','b','d'),('c2','b','d'),('c3','b','d'),('c4','b','d')]
print(set(map(lambda x :modify_tuple(x, [1,-1, 0]), b)))
# print(set([modify_tuple(x, [1,-1, 0]) for x in b]))