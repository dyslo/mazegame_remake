import tkinter
import tkinter.font as tkFont
import random
import os
from datetime import datetime
#import winsound

filecount = len(os.listdir("./mazefile/"))
rnd = str(random.randrange(1,filecount+1))
fileName = 'maze' + rnd + '.txt'

with open('./mazefile/' + fileName, 'r') as file:
        maze = file.readline()
        maze = eval(''.join(maze)) #배열로 불러오기
#print(maze)

count = acquired = 3

while (count > 0):
    temp = random.randrange(0, len(maze))
    temp2 = random.randrange(0, len(maze[temp]))
    if (maze[temp][temp2] == 0):
        count -= 1
        maze[temp][temp2] = 4
        continue    
        
key = None
position = None

startPos = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 2]
endPos   = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 3]
starPos  = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 4]
stars = []

startPos_x = startPos[0][0]
startPos_y = startPos[0][1]

start_time = None
end_time = None

blockSize = 15
window = tkinter.Tk()
window.title("Maze Game")
window.geometry(str(len(maze) * blockSize)+ "x" + str(len(maze[0]) * blockSize) + "+" + "100+100")
window.resizable(False, False)

canvas = tkinter.Canvas(width=len(maze[0]) * blockSize, height=len(maze) * blockSize + 100)

def regenMaze():
    global maze, key, position, startPos, endPos, starPos, startPos_x, startPos_y, acquired, stars
    rnd = str(random.randrange(1,filecount))
    fileName = 'maze' + rnd + '.txt'

    with open('./mazefile/' + fileName, 'r') as file:
            maze = file.readline()
            maze = eval(''.join(maze)) #배열로 불러오기
    #print(maze)

    count = acquired = 3

    while (count > 0):
        temp = random.randrange(0, len(maze))
        temp2 = random.randrange(0, len(maze[temp]))
        if (maze[temp][temp2] == 0):
            count -= 1
            maze[temp][temp2] = 4
            continue

    key = None
    position = None

    startPos = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 2]
    endPos   = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 3]
    starPos  = [[j, i] for i in range(len(maze)) for j in range(len(maze[i])) if maze[i][j] == 4]
    stars = []

    startPos_x = startPos[0][0]
    startPos_y = startPos[0][1]

def drawmaze():
    global maze, position
    canvas.pack()
    regenMaze()
    for y in range(len(maze)):
        for x in range(len(maze)):
            if maze[y][x] == 1:
                wall = canvas.create_rectangle(x * blockSize, y * blockSize, x * blockSize + blockSize, y * blockSize + blockSize, fill="green", outline="green")
                canvas.tag_raise(wall)
            if maze[y][x] == 2:
                position = canvas.create_rectangle(x * blockSize, y * blockSize, x * blockSize + blockSize, y * blockSize + blockSize, fill="red", outline="red", tags="start")
                canvas.tag_raise(position)
            if maze[y][x] == 3:
                end = canvas.create_rectangle(x * blockSize, y * blockSize, x * blockSize + blockSize, y * blockSize + blockSize, fill="skyblue", outline="skyblue", tags="end")
                canvas.tag_lower(end)
            if maze[y][x] == 4:
                star = canvas.create_rectangle(x * blockSize, y * blockSize, x * blockSize + blockSize, y * blockSize + blockSize, fill="yellow", outline="yellow", tags=str(x)+"+"+str(y))
                canvas.tag_lower(star)

def startPage():
    frm_main  = tkinter.Frame(window, bd=1)
    def gameStart():
        global start_time
        drawmaze()
        frm_main.place_forget()
        start_time = datetime.now()
        window.bind("<Key>", keyEvent)
        
    lbl_title = tkinter.Label(frm_main, text="미로 게임", fg="black", font=tkFont.Font(size=30))
    lbl_start = tkinter.Button(frm_main, text="게임 시작", width=15, command=gameStart, padx=20)
    lbl_title.pack()
    lbl_start.pack()
    frm_main.place(relx=.5, rely=.5, anchor="c")

def keyEvent(e):
    try:
        global key, startPos_x, startPos_y, count, end_time, acquired
        key = e.keysym
        if key == "Up" and maze[startPos_y-1][startPos_x] != 1:
            startPos_y -= 1
            canvas.move("start", 0, -blockSize)
        if key == "Down" and maze[startPos_y+1][startPos_x] != 1:
            startPos_y += 1
            canvas.move("start", 0, blockSize)
        if key == "Left" and maze[startPos_y][startPos_x-1] != 1:
            startPos_x -= 1
            canvas.move("start", -blockSize, 0)
        if key == "Right" and maze[startPos_y][startPos_x+1] != 1:
            startPos_x += 1
            canvas.move("start", blockSize, 0)
        if [startPos_x, startPos_y] in starPos:
            #canvas.create_rectangle(startPos_x * blockSize, startPos_y * blockSize, startPos_x * blockSize + blockSize, startPos_y * blockSize + blockSize, fill="white", outline="white")
            #winsound.Playsound("coin.mp3")
            canvas.delete(str(startPos_x)+"+"+str(startPos_y))
            starPos.remove([startPos_x, startPos_y])
            acquired -= 1
            #print("star acquired")
        if [startPos_x, startPos_y] == endPos[0]:
            if acquired == 0:
                canvas.delete("end")
                endPage()
            else:
                return
    except IndexError:
        #print("out of range error")
        return
       
def endPage():
    global window
    canvas.pack_forget()
    canvas.delete("all")
    window.unbind("<Key>")
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    #print(elapsed_time)
    with open('rank.txt', 'a') as file:
        file.write(str(elapsed_time) + "\n")

    def returnPage():
        global end_time
        end_time = None
        frm_end.place_forget()
        startPage()

    def rankPage():
        global end_time
        end_time = None
        frm_end.place_forget()
        rank()

    frm_end = tkinter.Frame(window, bd=1)
    lbl_title = tkinter.Label(frm_end, text="게임 끝", fg="black", font=tkFont.Font(size=30))
    lbl_elapsed_time = tkinter.Label(frm_end, text=str(elapsed_time), fg="black", font=tkFont.Font(size=15))
    lbl_ranking = tkinter.Button(frm_end, text="순위 보기", command=rankPage, width=15, padx=20)
    lbl_return = tkinter.Button(frm_end, text="게임 시작", command=returnPage,width=15, padx=20)
    lbl_title.pack()
    lbl_elapsed_time.pack()
    lbl_return.pack()
    lbl_ranking.pack()
    frm_end.place(relx=.5, rely=.5, anchor="c")

def rank():
    def returnPage():
        frm_rank.place_forget()
        startPage()

    with open('rank.txt', 'r') as file:
        top5 = file.readlines()
    frm_rank = tkinter.Frame(window, bd=1)
    lbl_title = tkinter.Label(frm_rank, text="TOP 5 순위", fg="black", font=tkFont.Font(size=30))
    lbl_return = tkinter.Button(frm_rank, text="시작 화면", command=returnPage, width=15, padx=20)
    lbl_title.pack(side="left")
    top5 = sorted(top5)
    if len(top5) > 5:
        l = 5
    else:
        l = len(top5)

    if len(top5) == 0:
        r = tkinter.Label(frm_rank, text="표시할 순위가 없습니다.", fg="black", anchor="center", height=2, font=tkFont.Font(size=15))
        r.pack()
    else:
        for i in range(0, l):
            r = tkinter.Label(frm_rank, text=str(i+1) + " - " + top5[i], fg="black", anchor="center", height=2, font=tkFont.Font(size=15))
            r.pack()
    #print(top5)
    lbl_return.pack()
    frm_rank.place(relx=.5, rely=.5, anchor="c")

startPage()
#print(stars)
window.mainloop()
