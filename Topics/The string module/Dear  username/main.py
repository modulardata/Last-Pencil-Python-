import string

username = input()
message = string.Template("Dear $u! It was really nice to meet you. Hopefully, you have a nice day! See you soon, $u!")
print(message.substitute(u=username))
