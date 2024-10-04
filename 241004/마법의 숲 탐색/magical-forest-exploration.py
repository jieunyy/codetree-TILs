from collections import deque

# 방향 정의: 0=북, 1=동, 2=남, 3=서
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

# 글로벌 변수 초기화
R, C, K = 0, 0, 0
A = []          # 숲의 격자 [0..R+2][0..C-1]
isExit = []     # 출구 여부 저장
answer = 0      # 최종 정령 위치의 행 번호 합산

# (y, x)가 숲의 범위 안에 있는지 확인하는 함수
def inRange(y, x):
    return 3 <= y < R + 3 and 0 <= x < C

# 숲에 있는 특정 골렘을 제거하는 함수 (resetMap)
def resetMap():
    for i in range(R + 3):
        for j in range(C):
            A[i][j] = 0
            isExit[i][j] = False

# 골렘의 중심이 y, x에 위치할 수 있는지 확인하는 함수
def canGo(y, x):
    # 중앙 셀이 숲 안에 있는지 확인
    if not inRange(y, x):
        return False
    
    # y + 1과 x + 1, x - 1이 격자 내에 있는지 추가로 확인
    if (y + 1 >= R + 3) or (x + 1 >= C) or (x - 1 < 0):
        return False
    
    # 골렘의 중심과 북, 동, 남, 서 방향 셀들이 비어 있는지 확인
    if (A[y - 1][x] != 0 or A[y][x - 1] != 0 or A[y][x] != 0 or
        A[y][x + 1] != 0 or A[y + 1][x] != 0):
        return False
    return True

# 정령의 최종 위치를 찾는 BFS 함수
def bfs(y, x, turn):
    global R, C
    queue = deque([(y, x)])
    visit = [[False] * C for _ in range(R + 3)]
    visit[y][x] = True
    max_row = y  # 가장 남쪽 행 번호 초기화

    while queue:
        current_y, current_x = queue.popleft()
        max_row = max(max_row, current_y)

        for i in range(4):
            ny = current_y + dy[i]
            nx = current_x + dx[i]

            if inRange(ny, nx) and not visit[ny][nx]:
                # 현재 셀이 같은 골렘에 속하거나, 출구를 통해 다른 골렘으로 이동 가능한지 확인
                if (A[ny][nx] == turn and canGo(ny, nx)) or (A[ny][nx] != 0 and isExit[current_y][current_x]):
                    visit[ny][nx] = True
                    queue.append((ny, nx))
    return max_row

# 골렘을 이동시키는 함수
def move_golem(y, x, d, turn):
    while True:
        # 1. 남쪽으로 이동 시도
        ny, nx = y + 1, x
        if ny < R + 3 and 0 <= nx < C and canGo(ny, nx):
            y, x = ny, nx
            continue

        # 2. 서쪽으로 회전하며 이동 시도 (반시계 방향 회전)
        ny, nx = y + 1, x - 1
        if ny < R + 3 and 0 <= nx < C and canGo(ny, nx):
            d = (d + 3) % 4  # 반시계 방향 회전
            y, x = ny, nx
            continue

        # 3. 동쪽으로 회전하며 이동 시도 (시계 방향 회전)
        ny, nx = y + 1, x + 1
        if ny < R + 3 and 0 <= nx < C and canGo(ny, nx):
            d = (d + 1) % 4  # 시계 방향 회전
            y, x = ny, nx
            continue

        # 더 이상 이동할 수 없으면 종료
        break

    return y, x, d

# 골렘을 배치하고 정령의 최종 위치를 계산하는 함수
def magic(y, x, d, turn):
    global answer
    y, x, d = move_golem(y, x, d, turn)

    # 중앙 셀이 숲 안에 있는지 확인
    if not inRange(y, x):
        # 해당 골렘만 스킵하고 점수를 추가하지 않음
        resetMap()  # 격자 초기화
        return

    # 중앙 셀이 숲 안에 있고, 주변 셀이 비어있는지 다시 확인
    if not canGo(y, x):
        resetMap()  # 격자 초기화
        return

    # 골렘을 격자에 고정
    A[y][x] = turn
    if x - 1 >= 0:
        A[y][x - 1] = turn
    if x + 1 < C:
        A[y][x + 1] = turn
    if y - 1 >= 0:
        A[y - 1][x] = turn
    if y + 1 < R + 3:
        A[y + 1][x] = turn

    # 출구 방향에 따른 위치 설정
    exit_dir = d
    exit_y = y + dy[exit_dir]
    exit_x = x + dx[exit_dir]
    if inRange(exit_y, exit_x):
        isExit[exit_y][exit_x] = True

    # 정령의 최종 위치 계산 via BFS
    res = bfs(y, x, turn)
    # 초기 3개의 추가 행을 보정하여 정렬
    score = res - 2  # 초기 3개의 추가 행을 고려하여 수정
    answer += score

    

    # 골렘 정착 후 격자 초기화
    resetMap()

# 메인 함수
def main():
    global R, C, K, A, isExit, answer
    R, C, K = map(int, input().split())
    # 초기화: 숲의 격자와 출구 배열 설정
    A = [[0] * C for _ in range(R + 3)]
    isExit = [[False] * C for _ in range(R + 3)]

    for turn in range(1, K + 1):
        ci, d = map(int, input().split())
        y = 3  # 골렘의 초기 y좌표: 상단에 3개의 추가 행을 고려
        x = ci - 1  # 골렘의 초기 x좌표: 0-based 인덱싱
        magic(y, x, d, turn)

    print(answer-1)

if __name__ == "__main__":
    main()