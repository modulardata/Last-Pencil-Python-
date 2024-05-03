n_pencils = int(input('How many pencils would you like to use:\n'))
player = str(input('Who will be the first (John, Jack):\n'))
print('|' * n_pencils)

turn = player

while n_pencils > 0:
    print(f'{turn}\'s turn: ', end='\n')
    taken = min(n_pencils, int(input()))
    n_pencils -= taken
    print('|' * n_pencils)
    if n_pencils == 0:
        # print(f'{turn} wins!')
        break
    if turn == 'John':
        turn = 'Jack'
    else:
        turn = 'John'

# if n_pencils == 0:
#     print(f'{turn} loses!')
