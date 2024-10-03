from collections import deque

# 범위 내 위치
def is_in(x, y, board):
    global r, c
    return (1<=(x-1) and (x+1)<=r+3 and 1<=(y-1) and (y+1)<=c and not board[x-1][y] and not board[x][y-1] and not board[x][y] and not board[x][y+1] and not board[x+1][y])

# 골렘 픽스, 정령 점수
def bfs(x, y, d, turn, board, is_exit):
    global r, c
    queue = deque([x, y, d])
    visit = [[False]*(c+1) for _ in range(r+4)]

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    while queue:
        x, y, d = queue.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            turn
            if (is_in(nx, ny, board) and board[nx][ny]==turn and not visit[nx][ny]) or (board[nx][ny]!=turn and is_exit[nx][ny]==true):
                turn = board[nx][ny]
                queue.append((nx, ny))
        
        # 아무 곳도 갈 수 없으면 이게 최종
        return x


# 전체 흐름
def move_golem(x, y, d, turn, board, is_exit):
    # 남쪽
    if is_in(x+1, y, board):
        move_golem(x+1, y, d, turn, board, is_exit)

    # 서쪽, 방향
    elif is_in(x+1, y-1, board):
        d = (d+3)%4
        move_golem(x+1, y-1, d, turn, board, is_exit)

    # 동쪽, 방향
    elif is_in(x+1, y+1, board):
        if d-1 > 0:
            d = (d-1)%4
        else:
            d = (d-1)%4 + 4
        move_golem(x, y, d, turn, board, is_exit)  
    
    return x, y, d


def magic(x, y, d, turn, board, is_exit):
    x, y, d = move_golem(x, y, d, turn, board, is_exit)

    if not is_in(x, y, board): 
        return 0

    # 영역 내에 있고, 더이상 이동할 수 없으면 픽스
    else:
        board[x-1][y] = turn
        board[x][y-1] = turn
        board[x][y] = turn
        board[x][y+1] = turn
        board[x+1][y] = turn

    res = bfs(x, y, d, turn, board, is_exit)
    return (res-3)

# 입력
r, c, k = map(int, input().split())

golem = deque([])
for _ in range(k):
    ci, d = map(int, input().split())
    golem.append((1, ci, d)) # 1-based x y d

result = 0
board = [[0]*(c+1) for _ in range(r+4)] # 1-based
is_exit = [[False]*(c+1) for _ in range(r+4)]

for i in range(k):
    x, y, d = golem.popleft()
    result += magic(x, y, d, i, board, is_exit)

# 출력
print(result)