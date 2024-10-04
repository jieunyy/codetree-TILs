from collections import deque

def inRange(x, y, large):
    return 0 <= x < large and 0 <= y < large

# fill
def fill(a, wall, idx, m, large):
    for j in range(large):
        for i in range(large-1, -1, -1):
            if a[i][j] == 0:
                a[i][j] = wall[idx]
                idx = (idx + 1) % m
    return a, idx

# bfs
def bfs(i, j, a, large):
    queue = deque([(i, j)])
    track = [(i, j)]
    visit = [[False]*large for _ in range(large)]
    visit[i][j] = True
    value = a[i][j]

    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    while queue:
        x, y = queue.popleft()
        for dir in range(4):
            nx, ny = x + dx[dir], y + dy[dir]
            if inRange(nx, ny, large) and not visit[nx][ny] and a[nx][ny] == value:
                visit[nx][ny] = True
                queue.append((nx, ny))
                track.append((nx, ny))
    
    if len(track) >= 3:
        for x, y in track:
            a[x][y] = 0
        return len(track)
    return 0

# rotate_subgrid
def rotate_subgrid(subgrid, cnt):
    for _ in range(cnt):
        # 90도 시계 방향 회전
        subgrid = [list(row) for row in zip(*subgrid[::-1])]
    return subgrid

# discover
def discover(array, wall, idx, m, large, small):
    best_score = -1
    best_rotation = None
    best_rot_cnt = None
    best_center = None
    best_grid = None

    # Iterate over all possible 3x3 subgrids
    for x in range(large - small + 1):
        for y in range(large - small + 1):
            original_subgrid = [row[y:y+small] for row in array[x:x+small]]
            for rot_cnt in [1, 2, 3]:  # 90, 180, 270 degrees
                rotated_subgrid = rotate_subgrid(original_subgrid, rot_cnt)
                # Create a copy of the grid to apply rotation
                new_grid = [row[:] for row in array]
                for i in range(small):
                    for j in range(small):
                        new_grid[x+i][y+j] = rotated_subgrid[i][j]
                
                # Now, perform BFS to find and remove connected components
                temp_grid = [row[:] for row in new_grid]
                total_score = 0
                temp_idx = idx
                while True:
                    score = 0
                    for i in range(large):
                        for j in range(large):
                            if temp_grid[i][j] != 0:
                                s = bfs(i, j, temp_grid, large)
                                score += s
                    if score == 0:
                        break
                    total_score += score
                    temp_grid, temp_idx = fill(temp_grid, wall, temp_idx, m, large)
                
                # Update the best rotation method
                if total_score > best_score:
                    best_score = total_score
                    best_rotation = (x, y)
                    best_rot_cnt = rot_cnt
                    best_grid = temp_grid
                elif total_score == best_score:
                    # 회전 각도가 더 작은 경우
                    if rot_cnt < best_rot_cnt:
                        best_rotation = (x, y)
                        best_rot_cnt = rot_cnt
                        best_grid = temp_grid
                    elif rot_cnt == best_rot_cnt:
                        # 중심 열이 작은 경우
                        if y < best_rotation[1]:
                            best_rotation = (x, y)
                            best_center = (x + 1, y + 1)
                            best_grid = temp_grid
                        elif y == best_rotation[1]:
                            # 중심 행이 작은 경우
                            if x < best_rotation[0]:
                                best_rotation = (x, y)
                                best_center = (x + 1, y + 1)
                                best_grid = temp_grid

    if best_score > 0:
        # Apply the best rotation to the original grid
        x, y = best_rotation
        original_subgrid = [row[y:y+small] for row in array[x:x+small]]
        rotated_subgrid = rotate_subgrid(original_subgrid, best_rot_cnt)
        for i in range(small):
            for j in range(small):
                array[x+i][y+j] = rotated_subgrid[i][j]
        # Remove connected components and fill
        total_score = 0
        while True:
            score = 0
            for i in range(large):
                for j in range(large):
                    if array[i][j] != 0:
                        s = bfs(i, j, array, large)
                        score += s
            if score == 0:
                break
            total_score += score
            array, idx = fill(array, wall, idx, m, large)
        return total_score
    else:
        return 0

# 입력 받기
k, m = map(int, input().split())  # 탐사 횟수, 벽면 유물 조각 개수
large = 5
small = 3

array = [list(map(int, input().split())) for _ in range(large)]
wall = list(map(int, input().split()))

result = []
idx = 0
for _ in range(k):
    score = discover(array, wall, idx, m, large, small)
    if score == 0:
        break
    result.append(score)

# 출력
print(' '.join(map(str, result)))