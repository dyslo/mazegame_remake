# Source: https://blog.naver.com/repeater1384/222067091195

import random

class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(self.dir)

    def get_cur_pos(self):
        return self.x, self.y
    
    def get_next_pos(self):
        return self.dir.pop()

def generateMaze(size):
    mazeRoom = [[Room(x,y) for x in range(size)] for y in range(size)]
    mazeBase = [[1 for _ in range(size*2+1)] for _ in range(size*2+1)]

    visited = []

    def make(cRoom):
        cx, cy = cRoom.get_cur_pos()
        visited.append((cx, cy))
        mazeBase[cy*2+1][cx*2+1] = 0
        while cRoom.dir:
            nx, ny = cRoom.get_next_pos()
            if 0 <= nx < size and 0 <= ny < size:
                if (nx, ny) not in visited:
                    mazeBase[cy+ny+1][cx+nx+1] = 0
                    make(mazeRoom[ny][nx])
    
    make(mazeRoom[0][0])
    
    # 입구/출구 생성, 2: 입구, 3: 출구
    def generateHole():
        ent_drct = random.randint(1,2) #1: 상, 2: 좌
        ext_drct = random.randint(3,4) #3: 하, 4: 우
        mazeSize_x = len(mazeBase[0])
        mazeSize_y = len(mazeBase)

        if ent_drct == 1:
            while True:
                temp = random.randint(1, mazeSize_x)
                if (mazeBase[1][temp-1] == 1):
                    continue
                else:
                    mazeBase[0][temp-1] = 2
                    break
        elif ent_drct == 2:
            while True:
                temp = random.randint(1, mazeSize_y)
                if (mazeBase[temp-1][1] == 1):
                    continue
                else:
                    mazeBase[temp-1][0] = 2
                    break
        
        if ext_drct == 3:
            while True:
                temp = random.randint(1, mazeSize_x)
                if (mazeBase[mazeSize_x-2][temp-1] == 1):
                    continue
                else:
                    mazeBase[mazeSize_x-1][temp-1] = 3
                    break
        elif ext_drct == 4:
            while True:
                temp = random.randint(1, mazeSize_y)
                if (mazeBase[temp-1][mazeSize_y-2] == 1):
                    continue
                else:
                    mazeBase[temp-1][mazeSize_y-1] = 3
                
    generateHole()

    return mazeBase

x = generateMaze(13)
file = open('/Users/dyslo/Library/Mobile Documents/com~apple~CloudDocs/Study/대학 2학년/컴프실/미로찾기/mazefile/maze2.txt', 'w')

print(x)
file.write(str(x))
file.close()