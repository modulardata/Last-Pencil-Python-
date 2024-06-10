import string
s1 = input()
s2 = input()
# s1 = "the string i want to capitalize"
# s2 = "the string i want to capitalize"

s1 = s1.capitalize()
s2 = string.capwords(s2, sep=' ')
print(s1)
print(s2)
