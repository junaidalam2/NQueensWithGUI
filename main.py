from tkinter import *
from tkinter import messagebox
import time


root = Tk()
root.title("N-Queens")
root.resizable(False, False)
p1 = PhotoImage(file='queen.png')
root.iconphoto(False, p1)

label_squares = []
animation_refresh_seconds = 0.20
board_size = 0
adjusted_board_size = board_size


# restart application
def restart():
    global board_size, label_squares, board_size_entry, frame2

    # clear board
    for i in range(board_size):
        for j in range(board_size):
            label_squares[i][j]['text'] = ''

    # reset scalar to 0
    board_size_entry['from_'] = 0
    board_size_entry['to'] = 0
    board_size_entry['from_'] = 1
    board_size_entry['to'] = 20

    # destroy and reinitialize frame2 (game board)
    frame2.destroy()
    frame2 = Frame(root)
    frame2.grid(row=0, column=1)

    submit_button['state'] = NORMAL
    board_size = 0
    label_squares = []


frame = Frame(root)

# frame 1 - user input
frame1 = Frame(root, bg='#0861a6')
frame1.grid(row=0, column=0, sticky='n')

# fame 2 - game board
frame2 = Frame(root)
frame2.grid(row=0, column=1, rowspan=2, sticky='n')


# Frame 1: User input for board length, and reset, submit and exit buttons --------------------------------------------

label0 = Label(frame1, text='Select the length of the board:', bg='#a5cbe8')
label0.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

board_size_entry = Scale(frame1, from_=1, to=20, orient=HORIZONTAL, bg='#a5cbe8')
board_size_entry.grid(row=2, column=0, padx=20, pady=10, columnspan=2)


# function that calls other functions
def main():
    global board_size, label_squares

    submit_button['state'] = DISABLED  # submit button disabled until reset button clicked
    board_size = int(board_size_entry.get())  # input board size

    # create a 2-d array of labels: name convention 'l + row number + column number'
    label_squares = [['l' + str(i) + str(j) for i in range(board_size)] for j in range(board_size)]

    generate_board()
    backtrack(label_squares, 0)  # solver function
    messagebox.showinfo(title=None, message=f'Finished Placing {adjusted_board_size} {"Queens" if adjusted_board_size > 1 else "Queen"}!')


submit_button = Button(frame1, text='Submit', command=main, bg='#a5cbe8')
submit_button.grid(row=3, column=0, padx=20, pady=10, columnspan=2)

reset_button = Button(frame1, text='Reset', command=restart)
reset_button.grid(row=4, column=0, sticky='w')


# exit application
def exit_application():
    root.destroy()


exit_button = Button(frame1, text='Exit', command=exit_application)
exit_button.grid(row=4, column=1, sticky='e')


# determine color for each square
def tile_color(row, column, dark_col, light_col):
    # alternate color
    bg_color = dark_col
    if (row % 2 == 0 and column % 2 == 0) or (row % 2 == 1 and column % 2 == 1):
        bg_color = light_col

    return bg_color


# Frame 2: Game board --------------------------------------------------------------------------------------------------

# create the board
def generate_board():
    global board_size

    # create labels within a grid
    for i in range(board_size):
        for j in range(board_size):

            dark_color = '#0861a6'
            light_color = '#a5cbe8'

            bg_color = tile_color(i, j, dark_color, light_color)

            height = 3
            width = 3
            label_squares[i][j] = Label(frame2, text='', borderwidth=0.5, relief='sunken', bg=bg_color, fg='#1f252e', font=('Goudy Stout', 10), height=height, width=width)
            label_squares[i][j].grid(row=i, column=j)


# check for conflicts between queens
def no_conflict(bo, row, col):
    # for specified row, check columns
    for j in range(len(bo)):
        if bo[row][j]['text'] == 'Q' and col != j:
            return False

    # for specified col, check rows
    for i in range(len(bo)):
        if bo[i][col]['text'] == 'Q' and row != i:
            return False

    # check downward to the right diagonals
    for i in range(min(len(bo) - row, len(bo) - col)):
        if bo[row + i][col + i]['text'] == 'Q' and row != row + i:
            return False

    # check upward to the right diagonals
    for i in range(min(row + 1, len(bo) - col)):
        if bo[row - i][col + i]['text'] == 'Q' and row != row + i:
            return True

    # check downward to the left diagonals
    for i in range(min(len(bo) - row, col + 1)):
        if bo[row + i][col - i]['text'] == 'Q' and row != row + i:
            return False

    # check upward to the left diagonals
    for i in range(min(row + 1, col + 1)):
        if bo[row - i][col - i]['text'] == 'Q' and row != row + i:
            return False

    return True


# solver function that uses backtracking
def backtrack(bo, c):
    global adjusted_board_size

    empty_dark_color = '#0861a6'
    empty_light_color = '#a5cbe8'
    occupied_dark_color = '#58d5db'
    occupied_light_color = '#aaf6fa'

    # if board size is 2 or 3, only n - 1 queens can fit on the board
    if len(bo) == 2 or len(bo) == 3:
        adjusted_board_size = len(bo) - 1
    else:
        adjusted_board_size = len(bo)

    if c >= adjusted_board_size:
        return True

    for row in range(len(bo)):
        if no_conflict(bo, row, c):  # subject cell to checker (of conflicts)
            root.update()
            time.sleep(animation_refresh_seconds)
            bo[row][c]['text'] = 'Q'  # if clear checker, place queen in that cell
            label_squares[row][c]['bg'] = tile_color(row, c, occupied_dark_color, occupied_light_color)

            if backtrack(bo, c + 1):  # if clear checker, move to next cell
                return True
            else:
                root.update()
                time.sleep(animation_refresh_seconds)
                bo[row][c]['text'] = ''  # if no solution, step back
                label_squares[row][c]['bg'] = tile_color(row, c, empty_dark_color, empty_light_color)

    return False


root.mainloop()
