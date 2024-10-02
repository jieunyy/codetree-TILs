# (x, y)가 보드 내의 좌표인지 확인하는 함수입니다.
def is_inrange(x, y):
    return 1 <= x and x <= n and 1 <= y and y <= n

n, m, p, c, d = map(int, input().split())
rr, rc = tuple(map(int, input().split()))

santa_count = [0 for _ in range(p + 1)]
santas = [(0, 0) for _ in range(p + 1)]
board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
down = [0 for _ in range(p + 1)]
is_live = [False for _ in range(p + 1)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board[rr][rc] = -1

for _ in range(p):
    id, x, y = tuple(map(int, input().split()))
    santas[id] = (x, y)
    board[santas[id][0]][santas[id][1]] = id
    is_live[id] = True

for t in range(1, m + 1):
    closestX, closestY, closestIdx = 10000, 10000, 0

    # 살아있는 산타들 중 루돌프에 가장 가까운 산타를 찾습니다.
    for i in range(1, p + 1):
        if not is_live[i]:
            continue

        currentBest = ((closestX - rr) ** 2 + (closestY - rc) ** 2, (-closestX, -closestY))
        currentValue = ((santas[i][0] - rr) ** 2 + (santas[i][1] - rc) ** 2, (-santas[i][0], -santas[i][1]))

        if currentValue < currentBest:
            closestX, closestY = santas[i]
            closestIdx = i

    # 가장 가까운 산타의 방향으로 루돌프가 이동합니다.
    if closestIdx:
        prevRudolf = (rr, rc)
        moveX = 0
        if closestX > rr:
            moveX = 1
        elif closestX < rr:
            moveX = -1

        moveY = 0
        if closestY > rc:
            moveY = 1
        elif closestY < rc:
            moveY = -1

        rr, rc = (rr + moveX, rc + moveY)
        board[prevRudolf[0]][prevRudolf[1]] = 0

    # 루돌프의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
    if rr == closestX and rc == closestY:
        firstX = closestX + moveX * c
        firstY = closestY + moveY * c
        lastX, lastY = firstX, firstY

        down[closestIdx] = t + 1

        # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
        while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
            lastX += moveX
            lastY += moveY

        # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해,
        # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY

            if not is_inrange(beforeX, beforeY):
                break

            idx = board[beforeX][beforeY]

            if not is_inrange(lastX, lastY):
                is_live[idx] = False
            else:
                board[lastX][lastY] = board[beforeX][beforeY]
                santas[idx] = (lastX, lastY)

            lastX, lastY = beforeX, beforeY

        santa_count[closestIdx] += c
        santas[closestIdx] = (firstX, firstY)
        if is_inrange(firstX, firstY):
            board[firstX][firstY] = closestIdx
        else:
            is_live[closestIdx] = False

    board[rr][rc] = -1;

    # 각 산타들은 루돌프와 가장 가까운 방향으로 한칸 이동합니다.
    for i in range(1, p + 1):
        if not is_live[i] or down[i] >= t:
            continue

        minDist = (santas[i][0] - rr) ** 2 + (santas[i][1] - rc) ** 2
        moveDir = -1

        for dir in range(4):
            nx = santas[i][0] + dx[dir]
            ny = santas[i][1] + dy[dir]

            if not is_inrange(nx, ny) or board[nx][ny] > 0:
                continue

            dist = (nx - rr) ** 2 + (ny - rc) ** 2
            if dist < minDist:
                minDist = dist
                moveDir = dir

        if moveDir != -1:
            nx = santas[i][0] + dx[moveDir]
            ny = santas[i][1] + dy[moveDir]

            # 산타의 이동으로 충돌한 경우, 산타를 이동시키고 처리를 합니다.
            if nx == rr and ny == rc:
                down[i] = t + 1

                moveX = -dx[moveDir]
                moveY = -dy[moveDir]

                firstX = nx + moveX * d
                firstY = ny + moveY * d
                lastX, lastY = firstX, firstY

                if d == 1:
                    santa_count[i] += d
                else:
                    # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
                    while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY

                    # 연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작해,
                    # 순차적으로 보드판에 있는 산타를 한칸씩 이동시킵니다.
                    while lastX != firstX or lastY != firstY:
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY

                        if not is_inrange(beforeX, beforeY):
                            break

                        idx = board[beforeX][beforeY]

                        if not is_inrange(lastX, lastY):
                            is_live[idx] = False
                        else:
                            board[lastX][lastY] = board[beforeX][beforeY]
                            santas[idx] = (lastX, lastY)

                        lastX, lastY = beforeX, beforeY

                    santa_count[i] += d
                    board[santas[i][0]][santas[i][1]] = 0
                    santas[i] = (firstX, firstY)
                    if is_inrange(firstX, firstY):
                        board[firstX][firstY] = i
                    else:
                        is_live[i] = False
            else:
                board[santas[i][0]][santas[i][1]] = 0
                santas[i] = (nx, ny)
                board[nx][ny] = i

    # 라운드가 끝나고 탈락하지 않은 산타들의 점수를 1 증가시킵니다.
    for i in range(1, p + 1):
        if is_live[i]:
            santa_count[i] += 1

# 결과를 출력합니다.
for i in range(1, p + 1):
    print(santa_count[i], end=" ")