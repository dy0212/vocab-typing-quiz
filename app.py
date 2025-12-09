from flask import Flask, render_template, jsonify, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# =========================
# 1) 데이터
# =========================

# ---- 한영(뜻 -> 단어) ----
# 네가 이미 모아둔 단어 기준으로 자연스러운 한글 뜻 넣어둠.
KO_EN = [
    {"word": "prelude", "meaning": "전조, 서막"},
    {"word": "assertive", "meaning": "자기 주장이 분명한, 단호한"},
    {"word": "crusade", "meaning": "운동, 캠페인"},
    {"word": "inexplicable", "meaning": "설명할 수 없는"},
    {"word": "comply", "meaning": "따르다, 준수하다"},
    {"word": "obnoxious", "meaning": "불쾌하게 거슬리는"},
    {"word": "anomaly", "meaning": "이상 현상, 예외"},
    {"word": "subordinate", "meaning": "부하의, 하급의; 부하"},
    {"word": "deviate", "meaning": "벗어나다, 일탈하다"},
    {"word": "explicit", "meaning": "명확한, 분명히 드러낸"},
    {"word": "penetrate", "meaning": "관통하다, 침투하다"},
    {"word": "precipitation", "meaning": "강수(비·눈 등)"},
    {"word": "implication", "meaning": "함의, 암시, 영향"},
    {"word": "deferential", "meaning": "공손한, 존경을 표하는"},
    {"word": "mitigated", "meaning": "완화된, 경감된"},
    {"word": "nonchalant", "meaning": "태연한, 무심한"},
    {"word": "desperate", "meaning": "절박한, 필사적인"},
    {"word": "reckon", "meaning": "생각하다, 여기다, 추정하다"},
    {"word": "denounce", "meaning": "비난하다, 규탄하다"},
    {"word": "audit", "meaning": "감사; 꼼꼼한 점검"},
    {"word": "controversy", "meaning": "논란, 논쟁"},
    {"word": "aviation", "meaning": "항공(산업), 비행"},
    {"word": "oblivious", "meaning": "모르고 있는, 무심한"},
    {"word": "alternative", "meaning": "대안; 대체 가능한"},
    {"word": "malfunction", "meaning": "오작동하다; 오작동"},
    {"word": "consecutive", "meaning": "연속적인"},
    {"word": "catastrophe", "meaning": "대재앙, 참사"},
    {"word": "ethnic", "meaning": "민족의, 종족의"},
    {"word": "descent", "meaning": "하강; 혈통"},
    {"word": "terrain", "meaning": "지형"},
    {"word": "proximity", "meaning": "근접, 가까움"},
    {"word": "invariably", "meaning": "항상, 변함없이"},
    {"word": "perspective", "meaning": "관점, 시각"},
    {"word": "jurisdiction", "meaning": "관할권"},
    {"word": "cockpit", "meaning": "조종석"},
    {"word": "revoke", "meaning": "취소하다, 철회하다"},
    {"word": "erode", "meaning": "침식하다; 약화시키다"},
    {"word": "tenant", "meaning": "세입자, 임차인"},
    {"word": "peasant", "meaning": "소작농, 농민"},
    {"word": "oppressive", "meaning": "억압적인, 가혹한"},
    {"word": "proclivity", "meaning": "성향, 경향"},
    {"word": "equivalent", "meaning": "동등한, 상응하는"},
    {"word": "outperform", "meaning": "능가하다"},
    {"word": "correspond", "meaning": "일치하다, 대응하다"},
    {"word": "irrigate", "meaning": "관개하다, 물을 대다"},
    {"word": "intricate", "meaning": "복잡한, 정교한"},
    {"word": "hibernate", "meaning": "동면하다"},
    {"word": "idleness", "meaning": "게으름, 무위"},
    {"word": "vague", "meaning": "모호한"},
    {"word": "infinite", "meaning": "무한한"},
    {"word": "endeavor", "meaning": "노력; 시도하다"},
    {"word": "tedious", "meaning": "지루한, 장황한"},
    {"word": "stereotype", "meaning": "고정관념"},
    {"word": "abstract", "meaning": "추상적인"},
    {"word": "trivial", "meaning": "사소한"},
    {"word": "vertical", "meaning": "수직의"},
    {"word": "cultivate", "meaning": "경작하다; 함양하다"},
    {"word": "hierarchy", "meaning": "계층, 위계"},
    {"word": "disposition", "meaning": "성향, 기질"},
    {"word": "consequence", "meaning": "결과, 영향"},
    {"word": "collegiality", "meaning": "동료애, 협력적 분위기"},
    {"word": "postmortem", "meaning": "사후 검토, 사건 후 분석"},
    {"word": "evident", "meaning": "분명한, 명백한"},
    {"word": "devastating", "meaning": "파괴적인, 충격적인"},
    {"word": "freight", "meaning": "화물"},
    {"word": "subservient", "meaning": "종속적인, 비굴한"},
    {"word": "anonymous", "meaning": "익명의"},
    {"word": "advocate", "meaning": "옹호하다; 옹호자"},
    {"word": "predicament", "meaning": "곤경"},
    {"word": "ambiguity", "meaning": "모호함"},
    {"word": "distinctive", "meaning": "특징적인, 독특한"},
    {"word": "illusion", "meaning": "환상, 착각"},
    {"word": "plight", "meaning": "곤경, 어려운 처지"},
    {"word": "subtlety", "meaning": "미묘함, 섬세함"},
    {"word": "intimidating", "meaning": "위협적인, 주눅 들게 하는"},
    {"word": "identical", "meaning": "동일한"},
    {"word": "relentless", "meaning": "끈질긴, 가차없는"},
]

# ---- 영영(정의 -> 단어) ----
EN_EN = [
    {"word": "prelude", "definition": "something that comes before and leads to something else"},
    {"word": "assertive", "definition": "confident in behavior or style"},
    {"word": "crusade", "definition": "a major effort to change something"},
    {"word": "inexplicable", "definition": "not able to be explained or understood"},
    {"word": "comply", "definition": "to do what you are asked or ordered to do"},
    {"word": "obnoxious", "definition": "unpleasant in a way that offends or annoys"},
    {"word": "anomaly", "definition": "something that deviates from what is normal or expected"},
    {"word": "subordinate", "definition": "someone who has less power or authority"},
    {"word": "deviate", "definition": "to depart from usual or accepted standards"},
    {"word": "explicit", "definition": "very clear and complete, leaving no doubt"},
    {"word": "penetrate", "definition": "to go through or into something"},
    {"word": "precipitation", "definition": "water that falls to the ground as rain, snow, etc."},
    {"word": "implication", "definition": "a possible future effect or result"},
    {"word": "deferential", "definition": "showing respect or consideration"},
    {"word": "mitigated", "definition": "lessened, reduced, diminished"},
    {"word": "nonchalant", "definition": "relaxed and calm, not showing you care"},
    {"word": "desperate", "definition": "very bad or difficult to deal with"},
    {"word": "reckon", "definition": "to think or suppose something is true"},
    {"word": "denounce", "definition": "to publicly state something is bad or wrong"},
    {"word": "audit", "definition": "a careful check or review of something"},
    {"word": "controversy", "definition": "an argument involving many who strongly disagree"},
    {"word": "aviation", "definition": "the business or practice of flying airplanes"},
    {"word": "oblivious", "definition": "not conscious or aware of something"},
    {"word": "alternative", "definition": "offering or expressing a choice"},
    {"word": "malfunction", "definition": "to fail to function or work properly"},
    {"word": "consecutive", "definition": "following one after another in a series"},
    {"word": "catastrophe", "definition": "a disaster"},
    {"word": "ethnic", "definition": "relating to races or large groups with shared culture"},
    {"word": "descent", "definition": "the act of going from higher to lower place"},
    {"word": "terrain", "definition": "land of a particular kind"},
    {"word": "proximity", "definition": "the state of being near"},
    {"word": "invariably", "definition": "without fail"},
    {"word": "perspective", "definition": "a way of thinking about or understanding something"},
    {"word": "jurisdiction", "definition": "an area where a system of laws applies"},
    {"word": "cockpit", "definition": "the area where the pilot sits"},
    {"word": "revoke", "definition": "to officially cancel the power or effect"},
    {"word": "erode", "definition": "to gradually destroy or be destroyed by natural forces"},
    {"word": "tenant", "definition": "a person who pays to use another’s property"},
    {"word": "peasant", "definition": "a poor farmer with low social status"},
    {"word": "oppressive", "definition": "very cruel or unfair"},
    {"word": "proclivity", "definition": "a tendency or disposition"},
    {"word": "equivalent", "definition": "having the same value, use, or meaning"},
    {"word": "outperform", "definition": "to perform better than"},
    {"word": "correspond", "definition": "to be similar or equal to"},
    {"word": "irrigate", "definition": "to supply with water by artificial means"},
    {"word": "intricate", "definition": "very complicated or detailed"},
    {"word": "hibernate", "definition": "to spend the winter sleeping"},
    {"word": "idleness", "definition": "laziness"},
    {"word": "vague", "definition": "not clear in meaning"},
    {"word": "infinite", "definition": "having no limits"},
    {"word": "endeavor", "definition": "to seriously try to do something"},
    {"word": "tedious", "definition": "too long, slow, or dull"},
    {"word": "stereotype", "definition": "a fixed, oversimplified idea of a group"},
    {"word": "abstract", "definition": "relating to general ideas, not specific things"},
    {"word": "trivial", "definition": "insignificant, minor"},
    {"word": "vertical", "definition": "upright, perpendicular"},
    {"word": "cultivate", "definition": "to grow and care for"},
    {"word": "hierarchy", "definition": "a system of levels with different importance"},
    {"word": "disposition", "definition": "a person’s inherent qualities of mind and character"},
    {"word": "consequence", "definition": "something that happens as a result of an action"},
    {"word": "collegiality", "definition": "cooperation between colleagues"},
    {"word": "postmortem", "definition": "analysis after something has ended"},
    {"word": "evident", "definition": "obvious, apparent"},
    {"word": "devastating", "definition": "highly destructive or damaging"},
    {"word": "freight", "definition": "goods carried by ships, trains, trucks, airplanes"},
    {"word": "subservient", "definition": "less important than something or someone else"},
    {"word": "anonymous", "definition": "not named or identified"},
    {"word": "advocate", "definition": "to support or argue for a cause"},
    {"word": "predicament", "definition": "a difficult or unpleasant situation"},
    {"word": "ambiguity", "definition": "something without a single clear meaning"},
    {"word": "distinctive", "definition": "distinguishing or characteristic"},
    {"word": "illusion", "definition": "an incorrect idea or belief"},
    {"word": "plight", "definition": "a very bad or difficult situation"},
    {"word": "subtlety", "definition": "a small but important detail not obvious"},
    {"word": "intimidating", "definition": "having a frightening, overawing or threatening effect"},
    {"word": "identical", "definition": "exactly the same"},
    {"word": "relentless", "definition": "continuing without becoming weaker, less severe"},
]

# ---- 예문(빈칸 -> 형태 정답) ----
# 규칙:
# - answer가 있으면 예문 모드에서 그 형태만 정답
# - answer가 없으면 word가 정답
EXAMPLES = [
    {
        "word": "prelude",
        "sentence": "If it were not the ____ to a tragedy, their back-and-forth would resemble a comedy routine."
    },
    {
        "word": "assertive",
        "answer": "assertively",
        "sentence": "The program teaches junior crew members how to communicate clearly and ____."
    },
    {
        "word": "crusade",
        "answer": "crusades",
        "sentence": "Combating mitigation has become one of the great ____ in commercial aviation."
    },
    {
        "word": "inexplicable",
        "sentence": "What happened was so strangely ____ that it sparked a huge outcry."
    },
    {
        "word": "comply",
        "sentence": "He couldn't ____ with the request of the air controller."
    },
    {
        "word": "obnoxious",
        "sentence": "This is not because he has an ____ personality."
    },
    {
        "word": "anomaly",
        "answer": "anomalies",
        "sentence": "Mitigation explains one of the great ____ of plane crashes."
    },
    {
        "word": "subordinate",
        "sentence": "He sees himself as a ____."
    },
    {
        "word": "deviate",
        "sentence": "Which direction would you like to ____?"
    },
    {
        "word": "explicit",
        "sentence": "That's the most direct and ____ way of making a point."
    },
    {
        "word": "penetrate",
        "sentence": "Ensure that your aircraft will not ____ this area."
    },
    {
        "word": "precipitation",
        "sentence": "You encounter moderate turbulence and ____."
    },
    {
        "word": "implication",
        "answer": "implications",
        "sentence": "He had to weigh the risk against the ____ of his decision."
    },
    {
        "word": "deferential",
        "sentence": "We mitigate when we're being ____ to authority."
    },
    {
        "word": "mitigated",
        "sentence": "His wording was highly ____ and indirect."
    },
    {
        "word": "nonchalant",
        "sentence": "This may involve being apologetic or ____."
    },
    {
        "word": "desperate",
        "sentence": "He was ever so ____ to go home."
    },
    {
        "word": "reckon",
        "sentence": "He said, \"I ____ that might be enough.\""
    },
    {
        "word": "denounce",
        "sentence": "To judge someone as overly aggressive is to implicitly ____ that person."
    },
    {
        "word": "audit",
        "answer": "audit",
        "sentence": "They ____ the tapes and present them to the pilots for review."
    },
    {
        "word": "controversy",
        "sentence": "He is in the forefront of the ____ over safety culture."
    },
    {
        "word": "aviation",
        "sentence": "That is why ____ is now so safe."
    },
    {
        "word": "oblivious",
        "sentence": "He wasn't entirely ____ of his legal obligations."
    },
    {
        "word": "alternative",
        "sentence": "There was an ____ pattern for using the land."
    },
    {
        "word": "malfunction",
        "sentence": "They tried to prevent the ____ from escalating."
    },
    {
        "word": "consecutive",
        "sentence": "It was the second ____ night the crew had pulled duty."
    },
    {
        "word": "catastrophe",
        "sentence": "Small human errors can cause a ____."
    },
    {
        "word": "ethnic",
        "sentence": "The ____ theory highlights cultural differences."
    },
    {
        "word": "descent",
        "answer": "descended",
        "sentence": "They are ____ from generations of rice farmers."
    },
    {
        "word": "terrain",
        "sentence": "Investigators considered the weather and the ____."
    },
    {
        "word": "proximity",
        "sentence": "The final approach is demanding because of the ____ to the ground."
    },
    {
        "word": "invariably",
        "sentence": "He could ____ trace the errors to early training."
    },
    {
        "word": "perspective",
        "sentence": "We may have a completely different ____ on how the world works."
    },
    {
        "word": "jurisdiction",
        "sentence": "Aviation ____ was reassigned after the accident."
    },
    {
        "word": "cockpit",
        "sentence": "What happened in that ____ raised serious questions."
    },
    {
        "word": "revoke",
        "answer": "revoking",
        "sentence": "They were considering ____ the company's privileges."
    },
    {
        "word": "erode",
        "sentence": "The policy threatened to ____ their authority."
    },
    {
        "word": "tenant",
        "sentence": "The downstairs ____ paid rent to use the space."
    },
    {
        "word": "peasant",
        "sentence": "The European tenant ____ lived under harsh landlords."
    },
    {
        "word": "oppressive",
        "sentence": "They never developed that kind of ____ feudal system."
    },
    {
        "word": "proclivity",
        "sentence": "The airline was once seen as having a ____ for accidents."
    },
    {
        "word": "equivalent",
        "sentence": "Their stories are extraordinary, yet in a way ____."
    },
    {
        "word": "outperform",
        "sentence": "The economy managed to ____ its rivals."
    },
    {
        "word": "correspond",
        "answer": "corresponded",
        "sentence": "The findings ____ perfectly with later research."
    },
    {
        "word": "irrigate",
        "answer": "irrigated",
        "sentence": "The soil must be properly ____."
    },
    # intricate는 예문이 원문에서 비어있던 느낌이라 제외
    {
        "word": "hibernate",
        "answer": "hibernating",
        "sentence": "Trees are dormant in winter, ____ until spring."
    },
    {
        "word": "idleness",
        "sentence": "They could indulge in ____ and festivities."
    },
    {
        "word": "vague",
        "sentence": "Few parents would be so ____ about their calendars."
    },
    {
        "word": "infinite",
        "sentence": "He spoke of the ____ improbability of success."
    },
    {
        "word": "endeavor",
        "sentence": "Success is a purposeful ____ made with others."
    },
    {
        "word": "tedious",
        "sentence": "The subject is ____ and technical."
    },
    {
        "word": "stereotype",
        "sentence": "He is an argument against the ____."
    },
    {
        "word": "abstract",
        "sentence": "They were interested in ____ questions of the field."
    },
    {
        "word": "trivial",
        "sentence": "This was not a ____ observation."
    },
    {
        "word": "vertical",
        "sentence": "Organizations can be horizontal or ____."
    },
    {
        "word": "cultivate",
        "sentence": "Farmers had to ____ a single field for months."
    },
    {
        "word": "hierarchy",
        "sentence": "Power distance reflects attitudes toward ____."
    },
    {
        "word": "disposition",
        "sentence": "Culture shapes temperament and ____."
    },
    {
        "word": "consequence",
        "answer": "consequences",
        "sentence": "These choices have real, practical ____."
    },
    {
        "word": "collegiality",
        "sentence": "A healthy team needs trust and ____."
    },
    {
        "word": "postmortem",
        "sentence": "The company conducted a ____ after the incident."
    },
    {
        "word": "evident",
        "sentence": "A clear pattern became ____."
    },
    {
        "word": "devastating",
        "sentence": "The results were ____."
    },
    {
        "word": "freight",
        "sentence": "Cargo and ____ were turned away."
    },
    {
        "word": "subservient",
        "sentence": "He remained ____ to senior authority."
    },
    {
        "word": "anonymous",
        "sentence": "The writer wished to remain ____."
    },
    {
        "word": "advocate",
        "sentence": "He became the children's ____."
    },
    {
        "word": "predicament",
        "sentence": "She struggled to escape her ____."
    },
    {
        "word": "ambiguity",
        "sentence": "Routines remove error and ____."
    },
    {
        "word": "distinctive",
        "sentence": "These are the ____ qualities of success."
    },
    {
        "word": "illusion",
        "sentence": "We must strip away the ____ of innate talent."
    },
    {
        "word": "plight",
        "sentence": "He tried to explain his ____ to the controller."
    },
    {
        "word": "subtlety",
        "sentence": "The ____ of the request was easy to miss."
    },
    {
        "word": "intimidating",
        "sentence": "For newcomers, the environment can be ____."
    },
    {
        "word": "identical",
        "sentence": "The two rankings were ____."
    },
    {
        "word": "relentless",
        "sentence": "They worked in a ____ pattern year after year."
    },
]


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
    session[ukey] = list(range(len(data_list)))
    random.shuffle(session[ukey])

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

    # ✅ 1회전 우선
    if session[ukey]:
        qid = session[ukey].pop()
    else:
        # ✅ 1회전 끝난 후에만 오답 복습
        if session[wkey]:
            qid = session[wkey].pop(0)  # queue 방식
        else:
            # ✅ 오답도 다 끝나면 1회전 리셋
            _reset_unseen(mode)
            qid = session[ukey].pop()

    item = data_list[qid]

    return jsonify({
        "mode": mode,
        "label": MODES[mode]["label"],
        "prompt_key": prompt_key,
        "prompt": item[prompt_key],
        "qid": qid,
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
        _init_mode_state(mode)
        wkey = _wrong_key(mode)
        if qid not in session[wkey]:
            session[wkey].append(qid)

    return jsonify({
        "correct": is_correct,
        "correct_word": correct_word
    })

# =========================
# 5) 실행
# =========================

if __name__ == "__main__":
    app.run(debug=True)
