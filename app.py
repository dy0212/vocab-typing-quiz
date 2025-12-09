from flask import Flask, render_template, jsonify, request, session
import random
import os

# ✅ 데이터는 별도 파일로 분리
from data import KO_EN, EN_EN, EXAMPLES


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# =========================
# 1) 모드 설정
# =========================

MODES = {
    "ko": {"label": "한영", "prompt_key": "meaning", "data": KO_EN},
    "en": {"label": "영영", "prompt_key": "definition", "data": EN_EN},
    "ex": {"label": "예문", "prompt_key": "sentence", "data": EXAMPLES},
}

# =========================
# 2) 세션 상태 헬퍼
# =========================

def _unseen_key(mode): return f"unseen_{mode}"
def _wrong_key(mode): return f"wrong_{mode}"

def _init_mode_state(mode):
    """모드별 1회전/오답 큐 초기화"""
    ukey = _unseen_key(mode)
    wkey = _wrong_key(mode)

    data_list = MODES[mode]["data"]

    if ukey not in session:
        session[ukey] = list(range(len(data_list)))
        random.shuffle(session[ukey])

    if wkey not in session:
        session[wkey] = []

def _reset_unseen(mode):
    """1회전 리셋"""
    ukey = _unseen_key(mode)
    data_list = MODES[mode]["data"]
    new_list = list(range(len(data_list)))
    random.shuffle(new_list)
    session[ukey] = new_list

def _get_item_by_qid(mode, qid):
    data_list = MODES[mode]["data"]
    if qid is None or qid < 0 or qid >= len(data_list):
        return None
    return data_list[qid]

# =========================
# 3) 페이지
# =========================

@app.route("/")
def index():
    counts = {k: len(v["data"]) for k, v in MODES.items()}
    return render_template("index.html", counts=counts)

# =========================
# 4) API
# =========================

@app.route("/api/next")
def api_next():
    mode = (request.args.get("mode") or "ko").strip()
    if mode not in MODES:
        mode = "ko"

    data_list = MODES[mode]["data"]
    prompt_key = MODES[mode]["prompt_key"]

    if not data_list:
        return jsonify({
            "mode": mode,
            "label": MODES[mode]["label"],
            "prompt_key": prompt_key,
            "prompt": "(이 모드 데이터가 비어 있어요)",
            "empty": True
        })

    _init_mode_state(mode)
    ukey = _unseen_key(mode)
    wkey = _wrong_key(mode)

    # ✅ 세션 리스트는 복사 → 수정 → 재할당 (반복 버그 방지)
    unseen = list(session.get(ukey, []))
    wrong = list(session.get(wkey, []))

    # ✅ 라운드 종료 신호:
    # 1회전 끝 + 오답 복습도 끝
    if not unseen and not wrong:
        # 새 라운드 준비
        unseen = list(range(len(data_list)))
        random.shuffle(unseen)
        wrong = []

        session[ukey] = unseen
        session[wkey] = wrong

        return jsonify({
            "mode": mode,
            "label": MODES[mode]["label"],
            "prompt_key": prompt_key,
            "completed": True,
            "empty": False
        })

    # ✅ 1회전 우선
    if unseen:
        qid = unseen.pop()
    else:
        qid = wrong.pop(0)

    session[ukey] = unseen
    session[wkey] = wrong

    item = data_list[qid]

    return jsonify({
        "mode": mode,
        "label": MODES[mode]["label"],
        "prompt_key": prompt_key,
        "prompt": item[prompt_key],
        "qid": qid,
        "completed": False,
        "empty": False
    })


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json(force=True)

    mode = (data.get("mode") or "ko").strip()
    answer = (data.get("answer") or "").strip().lower()
    qid = data.get("qid")

    if mode not in MODES:
        return jsonify({"ok": False, "error": "Invalid mode"}), 400

    data_list = MODES[mode]["data"]
    if not data_list:
        return jsonify({"ok": False, "error": "Empty mode data"}), 400

    try:
        qid = int(qid)
    except:
        return jsonify({"ok": False, "error": "Invalid qid"}), 400

    item = _get_item_by_qid(mode, qid)
    if not item:
        return jsonify({"ok": False, "error": "Item not found"}), 400

    _init_mode_state(mode)
    wkey = _wrong_key(mode)
    wrong = list(session.get(wkey, []))

    # ✅ 예문 모드: answer가 있으면 그 형태만 정답
    if mode == "ex":
        expected = (item.get("answer") or item["word"]).strip().lower()
        correct_word = item.get("answer") or item["word"]
        is_correct = (answer == expected)
    else:
        correct_word = item["word"]
        is_correct = (answer == correct_word.lower())

    # ✅ 틀리면 오답 큐에 추가(중복 방지)
    if not is_correct:
        if qid not in wrong:
            wrong.append(qid)
        session[wkey] = wrong

    return jsonify({
        "correct": is_correct,
        "correct_word": correct_word
    })


# =========================
# 5) 실행
# =========================

if __name__ == "__main__":
    app.run(debug=True)
