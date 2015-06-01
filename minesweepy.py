import string
import random

game_board = None
visible_board = None
num_mines = 10
width = 10
height = 10

def letters(begin='A', end='Z'):
    begin_ord = ord(begin)
    end_ord = ord(end)
    for number in xrange(begin_ord, end_ord+1):
        yield chr(number)

def generate_boards():
    global visible_board
    global game_board
    visible_board = [["*" for x in xrange(width)] for x in xrange(height)]
    game_board = [["_" for x in xrange(width)] for y in xrange(height)]

    local_num_mines = num_mines
    while local_num_mines > 0:
        for x in xrange(width):
            if local_num_mines == 0:
                break

            for y in xrange(height):
                if game_board[x][y] == 'X':
                    continue

                if local_num_mines == 0:
                    break

                add_mine = random.randint(0,99)
                if add_mine == 0:
                    game_board[x][y] = "X"
                    local_num_mines -= 1

    for x in xrange(width):
        for y in xrange(height):
            if game_board[x][y] == 'X':
                continue

            count = 0
            if x > 0:
                xval = x - 1
                if y > 0:
                    count += 1 if game_board[xval][y-1] == 'X' else 0
                if y < height - 1:
                    count += 1 if game_board[xval][y+1] == 'X' else 0
                count += 1 if game_board[xval][y] == 'X' else 0
            if x < width - 1:
                xval = x + 1
                if y > 0:
                    count += 1 if game_board[xval][y-1] == 'X' else 0
                if y < height - 1:
                    count += 1 if game_board[xval][y+1] == 'X' else 0
                count += 1 if game_board[xval][y] == 'X' else 0

            if y > 0:
                count += 1 if game_board[x][y-1] == 'X' else 0

            if y < height - 1:
                count += 1 if game_board[x][y+1] == 'X' else 0

            if count > 0:
                game_board[x][y] = count

def display_boards():
    #display_board(visible_board)
    #display_board(game_board)
    pass

def display_board(board):
    print "   ",
    for x in xrange(width):
        print x,
    print "\n",
    print "  ",
    print "-" * (width*2+1)
    for x in xrange(height):
        print "{} |".format(x),
        for c in board[x]:
            print c,
        print "| {}".format(x)
        if x < height - 1:
            print "  |",
            print " " * (width*2-1),
            print "|"
    print "  ",
    print "-" * (width*2+1)
    print "   ",
    for x in xrange(width):
        print x,
    print "\n"

def recursive_clear(board, y, x, checked):
    if (x,y) in checked:
        return
    checked.add((x,y))

    board[y][x] = game_board[y][x]
    if game_board[y][x] != '_':
        return

    if x > 0:
        xval = x-1
        if y > 0:
            recursive_clear(board, y-1, xval, checked)
        if y < height - 1:
            recursive_clear(board, y+1, xval, checked)

        recursive_clear(board, y, xval, checked)

    if x < width - 1:
        xval = x+1
        if y > 0:
            recursive_clear(board, y-1, xval, checked)
        if y < height - 1:
            recursive_clear(board, y+1, xval, checked)
        recursive_clear(board, y, xval, checked)

    if y > 0:
        recursive_clear(board, y-1, x, checked)
    if y < height - 1:
        recursive_clear(board, y+1, x, checked)

num_ord_diff = 48

def play_game():
    global visible_board
    while True:
        display_board(visible_board)

        x = ord(raw_input("Select horizontal [0-9]: ")) - num_ord_diff
        y = ord(raw_input("Select vertical [0-9]: ")) - num_ord_diff

        if not (0 <= x <= 9 and 0 <= y <= 9):
            print "Bad!"
            continue

        print "\n"

        if game_board[y][x] == 'X':
            print "You died!"
            display_board(game_board)
            break

        recursive_clear(visible_board, y, x, set())

        num_left = 0
        for w in xrange(width):
            for h in xrange(height):
                num_left += 1 if visible_board[h][w] == '*' else 0
        if num_left == num_mines:
            print "You won!"
            display_board(game_board)
            break

def main():
    generate_boards()
    #display_boards()
    play_game()


if __name__ == "__main__":
    main()
