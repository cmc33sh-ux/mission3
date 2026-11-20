import json
import time

DATA_FILE = "data.json"
EPSILON = 1e-9
REPEAT = 10

# 라벨 정규화표: 파일의 표기(+, x, cross)를 표준 라벨(Cross, X)로 바꾼다.
label_map = {"+": "Cross", "cross": "Cross", "x": "X"}


def normalize_label(value):
    # 표기를 표준 라벨로 바꾼다. 모르는 표기면 None 을 돌려준다.
    return label_map.get(str(value).strip().lower())


def mac(pattern, filter_):
    # 같은 위치끼리 곱해서 모두 더한다 (외부 라이브러리 없이 반복문으로 구현).
    score = 0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_[i][j]
    return score


def judge(s_cross, s_x):
    # epsilon 기반 비교: 차이가 epsilon 보다 작으면 동점으로 본다.
    if abs(s_cross - s_x) < EPSILON:
        return "UNDECIDED"
    if s_cross > s_x:
        return "Cross"
    return "X"


def measure(pattern, filter_):
    # MAC 연산 구간만 REPEAT 번 재서 평균 시간(ms)을 돌려준다 (입출력 시간은 제외).
    total = 0.0
    for _ in range(REPEAT):
        start = time.perf_counter()
        mac(pattern, filter_)
        total += time.perf_counter() - start
    return total / REPEAT * 1000


def print_performance(samples):
    # samples: [(크기 N, 패턴, 필터), ...]
    print("크기(N×N)   평균 시간(ms)   연산 횟수(N²)")
    for n, pattern, filter_ in samples:
        ms = measure(pattern, filter_)
        print(f"{n}×{n:<8} {ms:<15.6f} {n * n}")


# ---------- 모드 1: 사용자 입력 (3×3) ----------

def read_matrix(name, n=3):
    print(f"{name}: {n}줄을 입력하세요 (줄마다 숫자 {n}개를 공백으로 구분)")
    matrix = []
    while len(matrix) < n:
        line = input(f"  {len(matrix) + 1}번째 줄: ")
        parts = line.split()
        if len(parts) != n:
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
            continue
        try:
            row = [float(p) for p in parts]
        except ValueError:
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
            continue
        matrix.append(row)
    return matrix


def run_mode1():
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")
    print("필터 A, B 저장 완료")
    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    ms = measure(pattern, filter_a)

    if abs(score_a - score_b) < EPSILON:
        result = "판정 불가"
    elif score_a > score_b:
        result = "A"
    else:
        result = "B"

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간: {ms:.6f} ms")
    print(f"판정: {result}")
    print()
    print("[성능 분석 (3×3)]")
    print_performance([(3, pattern, filter_a)])


# ---------- 모드 2: data.json 분석 ----------

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: {DATA_FILE} 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError as e:
        print(f"오류: {DATA_FILE} 형식이 올바르지 않습니다. ({e})")
    return None


def is_square(matrix, n):
    # n×n 숫자 판인지 확인한다.
    if not isinstance(matrix, list) or len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
        for v in row:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                return False
    return True


def get_size(key):
    # "size_13_2" 에서 13 을 꺼낸다. 형식이 틀리면 None.
    parts = key.split("_")
    if len(parts) != 3 or parts[0] != "size" or not parts[1].isdigit():
        return None
    return int(parts[1])


def build_filters(group):
    # {"cross": 판, "x": 판} 의 이름표를 표준 라벨로 바꾼다.
    filters = {}
    for name, matrix in group.items():
        label = normalize_label(name)
        if label is not None:
            filters[label] = matrix
    return filters


def run_mode2():
    data = load_data()
    if data is None:
        return
    if "filters" not in data or "patterns" not in data:
        print("오류: filters 또는 patterns 항목이 없습니다.")
        return

    total = 0
    passed = 0
    failed = 0
    fail_list = []

    print("[케이스별 판정]")
    for key, case in data["patterns"].items():
        total += 1
        reason = None

        n = get_size(key)
        if n is None:
            reason = "키 형식 오류"
        elif f"size_{n}" not in data["filters"]:
            reason = f"size_{n} 필터가 없음"
        else:
            filters = build_filters(data["filters"][f"size_{n}"])
            if "Cross" not in filters or "X" not in filters:
                reason = "필터 라벨(Cross/X) 부족"
            elif not is_square(filters["Cross"], n) or not is_square(filters["X"], n):
                reason = "필터 크기 불일치"
            elif "input" not in case or not is_square(case["input"], n):
                reason = "패턴 크기 불일치"
            elif normalize_label(case.get("expected")) is None:
                reason = "expected 라벨 오류"

        if reason is not None:
            failed += 1
            fail_list.append((key, reason))
            print(f"{key}: FAIL ({reason})")
            continue

        expected = normalize_label(case["expected"])
        s_cross = mac(case["input"], filters["Cross"])
        s_x = mac(case["input"], filters["X"])
        result = judge(s_cross, s_x)

        if result == expected:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"
            fail_list.append((key, f"판정 {result}, 정답 {expected}"))
        print(f"{key}: Cross {s_cross:.4f} / X {s_x:.4f} -> {result} (expected {expected}) {status}")

    print()
    print("[성능 분석]")
    samples = [(3, DEFAULT_3[0], DEFAULT_3[1])]
    for size_key in data["filters"]:
        n = get_size(size_key + "_0")
        filters = build_filters(data["filters"][size_key])
        if n is not None and "Cross" in filters and is_square(filters["Cross"], n):
            samples.append((n, filters["Cross"], filters["Cross"]))
    print_performance(sorted(samples, key=lambda s: s[0]))

    print()
    print("[결과 요약]")
    print("전체", total, "통과", passed, "실패", failed)
    if fail_list:
        print("실패 케이스:")
        for key, reason in fail_list:
            print(f"  - {key}: {reason}")


# 성능 표의 3×3 용 기본 판 (십자가 모양)
DEFAULT_3 = (
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
)


def main():
    while True:
        print("=== Mini NPU 시뮬레이터 ===")
        print("1. 사용자 입력 (3×3)")
        print("2. data.json 분석")
        choice = input("모드를 선택하세요 (1/2): ").strip()
        if choice == "1":
            run_mode1()
            return
        if choice == "2":
            run_mode2()
            return
        print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()
