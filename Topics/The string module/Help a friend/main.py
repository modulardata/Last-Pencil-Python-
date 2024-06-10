import string
name = input()
adjective: str = input()
template = string.Template("Hi, $name! You look $adjective today! You're doing great!")
compliment = template.substitute(name=name, adjective=adjective)
print(compliment)