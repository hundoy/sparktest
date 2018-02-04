#The list of lists
list_of_lists = [range(4), range(7)]

#flatten the lists
flattened_list = [y for x in list_of_lists for y in x]

print(flattened_list)

arr_str = ""
