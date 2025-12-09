from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# 지금까지 번역한 단어 목록
WORDS = [
    {"word": "prelude", "meaning": "전조, 서막, 시작"},
    {"word": "assertive", "meaning": "자기 주장이 분명한, 당당한"},
    {"word": "crusade", "meaning": "운동, 캠페인"},
    {"word": "comply", "meaning": "따르다, 준수하다"},
    {"word": "obnoxious", "meaning": "불쾌하게 거슬리는, 밉상인"},
    {"word": "anomaly", "meaning": "이상 현상, 예외"},
    {"word": "deviate", "meaning": "벗어나다, 일탈하다"},

    {"word": "inexplicable", "meaning": "설명할 수 없는, 이해가 안 되는"},
    {"word": "subordinate", "meaning": "부하의, 하급의; 부하"},
    {"word": "explicit", "meaning": "명확한, 분명히 드러낸"},

    {"word": "penetrate", "meaning": "관통하다, 침투하다"},
    {"word": "precipitation", "meaning": "강수(비·눈 등), 침전"},
    {"word": "implication", "meaning": "함의, 암시, 영향"},
    {"word": "deferential", "meaning": "공손한, 존경을 표하는"},
    {"word": "mitigated", "meaning": "완화된, 경감된"},
    {"word": "nonchalant", "meaning": "태연한, 무심한"},
    {"word": "desperate", "meaning": "절박한, 필사적인"},
    {"word": "reckon", "meaning": "생각하다, 여기다, 추정하다"},
    {"word": "denounce", "meaning": "비난하다, 규탄하다"},
    {"word": "audit", "meaning": "꼼꼼한 점검/검토; 감사"},

    {"word": "controversy", "meaning": "논란, 논쟁"},
    {"word": "aviation", "meaning": "항공(산업), 비행"},
    {"word": "oblivious", "meaning": "모르고 있는, 무심한"},
    {"word": "alternative", "meaning": "대안, 대체 가능한"},
    {"word": "malfunction", "meaning": "오작동, 기능 장애"},
    {"word": "consecutive", "meaning": "연속적인"},
    {"word": "catastrophe", "meaning": "대재앙, 참사"},
    {"word": "ethnic", "meaning": "민족의, 민족 관련"},
    {"word": "descent", "meaning": "하강, 내려감; 혈통, 가계"},
    {"word": "terrain", "meaning": "지형, 지세"},

    {"word": "proximity", "meaning": "근접, 가까움"},
    {"word": "invariably", "meaning": "항상, 변함없이"},
    {"word": "perspective", "meaning": "관점, 시각"},
    {"word": "jurisdiction", "meaning": "관할권, 사법권"},
    {"word": "cockpit", "meaning": "조종석"},
    {"word": "revoke", "meaning": "취소하다, 철회하다"},
    {"word": "erode", "meaning": "침식하다, 약화시키다"},
    {"word": "tenant", "meaning": "세입자, 임차인"},
    {"word": "peasant", "meaning": "소작농, 농민"},
    {"word": "oppressive", "meaning": "억압적인, 가혹한"},
    {"word": "proclivity", "meaning": "성향, 경향"},
    {"word": "equivalent", "meaning": "동등한, 상응하는; 동등한 것"},
    {"word": "outperform", "meaning": "능가하다, 더 좋은 성과를 내다"},
    {"word": "correspond", "meaning": "일치하다, 대응하다; 편지를 주고받다"},
    {"word": "irrigate", "meaning": "관개하다, 물을 대다"},
    {"word": "intricate", "meaning": "복잡한, 정교한"},
    {"word": "hibernate", "meaning": "동면하다"},
    {"word": "idleness", "meaning": "게으름, 무위"},
    {"word": "vague", "meaning": "모호한, 애매한"},
    {"word": "infinite", "meaning": "무한한"},
    {"word": "endeavor", "meaning": "노력; 시도하다"},
    {"word": "tedious", "meaning": "지루한, 장황한"},
    {"word": "stereotype", "meaning": "고정관념"},
    {"word": "abstract", "meaning": "추상적인; 초록(요약)"},
    {"word": "trivial", "meaning": "사소한, 하찮은"},
    {"word": "vertical", "meaning": "수직의"},
    {"word": "cultivate", "meaning": "경작하다; 기르다, 함양하다"},
    {"word": "hierarchy", "meaning": "계층, 위계"},
    {"word": "disposition", "meaning": "성향, 기질; 처분"},
    {"word": "consequence", "meaning": "결과, 영향"},
    {"word": "collegiality", "meaning": "동료애, 협력적 분위기"},
    {"word": "postmortem", "meaning": "사후 검토, 사건 후 분석"},
    {"word": "evident", "meaning": "분명한, 명백한"},
    {"word": "devastating", "meaning": "파괴적인, 충격적인"},
    {"word": "freight", "meaning": "화물, 화물 운송"},
    {"word": "subservient", "meaning": "비굴한, 종속적인"},
    {"word": "anonymous", "meaning": "익명의"},
    {"word": "advocate", "meaning": "옹호하다; 옹호자"},
    {"word": "predicament", "meaning": "곤경, 난처한 상황"},
    {"word": "ambiguity", "meaning": "모호함, 애매성"},
    {"word": "distinctive", "meaning": "독특한, 특징적인"},
    {"word": "illusion", "meaning": "환상, 착각"},
    {"word": "plight", "meaning": "곤경, 어려운 처지"},
    {"word": "subtlety", "meaning": "미묘함, 섬세함"},
    {"word": "intimidating", "meaning": "위협적인, 주눅 들게 하는"},
    {"word": "identical", "meaning": "동일한"},
    {"word": "relentless", "meaning": "끈질긴, 가차없는"},
]

@app.route("/")
def index():
    return render_template("index.html", total=len(WORDS))

@app.route("/api/next")
def next_word():
    item = random.choice(WORDS)
    # 정답은 클라이언트에 보내지 않음
    return jsonify({"meaning": item["meaning"]})

@app.route("/api/check", methods=["POST"])
def check():
    data = request.get_json(force=True)
    meaning = (data.get("meaning") or "").strip()
    answer = (data.get("answer") or "").strip()

    # meaning으로 원본 단어 찾기(뜻이 중복될 가능성 낮다고 가정)
    candidates = [w for w in WORDS if w["meaning"] == meaning]
    if not candidates:
        return jsonify({"ok": False, "error": "Meaning not found"}), 400

    correct_word = candidates[0]["word"]

    normalized_answer = answer.lower()
    normalized_correct = correct_word.lower()

    is_correct = normalized_answer == normalized_correct

    return jsonify({
        "correct": is_correct,
        "correct_word": correct_word
    })

if __name__ == "__main__":
    app.run(debug=True)
