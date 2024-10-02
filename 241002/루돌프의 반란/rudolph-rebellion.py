from collections import deque

# 산타 상호작용 함수
def santa_match(pn, sr, sc, sy, sx, santas, n):
    tmp = deque(santas)
    result = deque()

    while tmp:
        n, r, c = tmp.popleft()
        if r == sr and c == sc:  # 산타가 동일한 좌표에 있는 경우
            # 산타를 밀어내기
            r += sy
            c += sx
            if 1 <= r <= n and 1 <= c <= n:
                result.append((n, r, c))  # 갱신된 좌표 추가
            sr, sc = r, c
        else:
            result.append((n, r, c))

    return result

# 산타 이동 함수
def move_s(rr, rc, santas, down, santa_count, d, n, turn):
    for i in range(len(santas)):
        pn, sr, sc = santas.popleft()
        if down[pn] > turn:  # 기절 상태인 경우
            santas.append((pn, sr, sc))
            continue

        sx, sy = 0, 0
        # 산타가 루돌프에게 가까워지는 방향으로 이동
        move_candidates = []
        for i in range(4):
            nr, nc = sr + sdy[i], sc + sdx[i]
            if 1 <= nr <= n and 1 <= nc <= n and all(nr != x or nc != y for _, x, y in santas):
                dist_before = (sr - rr) ** 2 + (sc - rc) ** 2
                dist_after = (nr - rr) ** 2 + (nc - rc) ** 2
                if dist_after < dist_before:  # 루돌프에게 가까워지는 경우만 이동 후보로 추가
                    move_candidates.append((dist_after, sdy[i], sdx[i]))

        # 상우하좌 우선순위에 따라 이동
        if move_candidates:
            _, sy, sx = min(move_candidates)
            sr, sc = sr + sy, sc + sx

        # 산타가 루돌프와 충돌한 경우
        if sr == rr and sc == rc:
            santa_count[pn] += d  # 산타가 힘만큼 점수 얻음
            # 산타가 충돌로 인해 밀려남
            sr -= sy * d
            sc -= sx * d

            # 이동한 좌표가 격자 안에 있을 때만 기절 처리
            if 1 <= sr <= n and 1 <= sc <= n:
                down[pn] = turn + 1  # 현재 턴에서 +1 턴까지 기절
                santas = santa_match(pn, sr, sc, sy, sx, santas, n)  # 산타 상호작용 처리

        santas.append((pn, sr, sc))  # 리스트에 다시 추가

    return santas

# 루돌프 이동 함수
def move_r(rr, rc, santas, down, santa_count, c, rdy, rdx, n):
    # 가장 가까운 산타 찾기 (우선순위: 거리 -> r 좌표 -> c 좌표)
    min_dis = float('inf')
    min_spn, msr, msc = 0, 0, 0

    for i in range(len(santas)):
        pn, sr, sc = santas.popleft()
        if down[pn] == 0:  # 기절해있지 않은 산타만 탐색
            dist = (sr - rr) ** 2 + (sc - rc) ** 2
            if (dist < min_dis or
                (dist == min_dis and sr > msr) or
                (dist == min_dis and sr == msr and sc > msc)):  # 우선순위: 거리 -> r 좌표 -> c 좌표
                min_dis = dist
                min_spn = pn
                msr, msc = sr, sc
        santas.append((pn, sr, sc))

    # 가장 가까운 산타를 향해 이동
    min_dis = float('inf')
    min_i = 0
    for i in range(8):
        nr, nc = rr + rdy[i], rc + rdx[i]
        if 1 <= nr <= n and 1 <= nc <= n:
            dist = (msr - nr) ** 2 + (msc - nc) ** 2  # 새로운 위치 기준 거리 계산
            if dist < min_dis:
                min_dis = dist
                min_i = i

    rr, rc = rr + rdy[min_i], rc + rdx[min_i]  # 루돌프 전진

    # 루돌프와 산타가 충돌한 경우
    if msr == rr and msc == rc:
        santa_count[min_spn] += c  # 산타 힘만큼 점수 얻음
        # 충돌 방향 설정 (sy, sx)
        sy = 1 if msr < rr else -1 if msr > rr else 0
        sx = 1 if msc < rc else -1 if msc > rc else 0

        msr -= sy * c  # 산타가 충돌로 인해 밀려남
        msc -= sx * c

        # 유효한 좌표로 이동 시 기절 처리
        if 1 <= msr <= n and 1 <= msc <= n:
            down[min_spn] = 1  # 산타 기절 처리
            santas = santa_match(min_spn, msr, msc, sy, sx, santas, n)  # 산타 상호작용 처리

    return rr, rc, santas

# 산타 이동 및 루돌프 이동 방향
sdx = [0, 1, 0, -1]
sdy = [-1, 0, 1, 0]
rdy = [1, 1, 1, 0, 0, -1, -1, -1]
rdx = [1, 0, -1, 1, -1, 1, 0, -1]

# 입력 및 초기화
n, m, p, c, d = map(int, input().split())
rr, rc = map(int, input().split())
santas = deque([tuple(map(int, input().split())) for _ in range(p)])

down = [0] * (p + 1)  # 기절 여부
santa_count = [0] * (p + 1)  # 산타 점수

# 각 턴마다 루돌프와 산타의 움직임 처리
for turn in range(m):
    rr, rc, santas = move_r(rr, rc, santas, down, santa_count, c, rdy, rdx, n)
    if len(santas) == 0:
        break

    santas = move_s(rr, rc, santas, down, santa_count, d, n, turn)

    # 산타가 살아남은 경우 점수 추가
    for i in range(len(santas)):
        pn, sr, sc = santas.popleft()
        if down[pn] <= turn:  # 기절 상태가 아닌 경우
            santa_count[pn] += 1
        santas.append((pn, sr, sc))

    # 기절 상태 초기화 (턴 + 2 까지 기절 유지)
    for i in range(1, p + 1):
        if down[i] == turn + 1:
            down[i] = 0  # 기절 해제

# 결과 출력
print(" ".join(map(str, santa_count[1:])))