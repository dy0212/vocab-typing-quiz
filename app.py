from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# =========================
# KO -> EN (뜻 보고 단어 쓰기)
# =========================
KO_EN = [
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
    {"word": "oblivious", "meaning": "(무엇을) 모르고 있는, 무심한"},
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
    {"word": "correspond", "meaning": "일치하다, 대응하다"},
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
    {"word": "disposition", "meaning": "성향, 기질"},
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

# =========================
# EN -> EN (definition 보고 단어 쓰기)
# 너가 준 영영풀이 반영
# =========================
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

# =========================
# Example blank filling
# 너가 준 예문 기반으로 정리
# (문장 속 {단어/변형} -> ____ 처리)
# 이상한 섞임/없는 예문은 제외
# =========================
EXAMPLES = [
    {"word": "prelude", "sentence": "If it were not the ____ to a tragedy, their back-and-forth would resemble an Abbott and Costello comedy routine."},
    {"word": "assertive", "sentence": "Every major airline now has what is called \"Crew Resource Management,\" known as CRM, and it's designed to teach junior crew members how to communicate clearly and ____."},
    {"word": "crusade", "sentence": "Combating mitigation has become one of the great ____ in commercial aviation in the past fifteen years."},
    {"word": "inexplicable", "sentence": "But what happened with Avianca was just so strangely ____ that it sparked a huge outcry in the industry."},
    {"word": "comply", "sentence": "Ratwatte couldn't ____ with the request of the air controller."},
    {"word": "obnoxious", "sentence": "This is not because Ratwatte has an ____ personality, or has an enormous ego."},
    {"word": "anomaly", "sentence": "Mitigation explains one of the great ____ of plane crashes."},
    {"word": "subordinate", "sentence": "Klotz sees himself as a ____."},
    {"word": "deviate", "sentence": "Which direction would you like to ____?"},
    {"word": "explicit", "sentence": "That's the most direct and ____ way of making a point imaginable."},
    {"word": "penetrate", "sentence": "You want to ensure that your aircraft will not ____ this area."},
    {"word": "precipitation", "sentence": "You encounter moderate turbulence and ____."},
    {"word": "implication", "sentence": "He had to weigh the risk of damaging his plane against the ____ of Helsinki versus Moscow."},
    {"word": "deferential", "sentence": "We mitigate when we're being ____ to authority."},
    {"word": "mitigated", "sentence": "The term used by linguists to describe this is ____: downplaying or sugarcoating meaning."},
    {"word": "nonchalant", "sentence": "This may involve being ____ or even indirect."},
    {"word": "desperate", "sentence": "He was tired and hungry and ever so ____ to go home."},
    {"word": "reckon", "sentence": "He had said \"I guess so\" and \"I ____\" and \"that might\"."},
    {"word": "denounce", "sentence": "To judge that someone is being insensitive is to implicitly ____ that person."},
    {"word": "audit", "sentence": "They ____ the tapes and present them to the pilots for review."},
    {"word": "controversy", "sentence": "He is in the forefront of the ____ over how to make sure the benefits of this cultural diversity are realized in the cockpit."},
    {"word": "aviation", "sentence": "That is why ____ is now so safe."},
    {"word": "oblivious", "sentence": "He's not entirely ____ of his legal obligations to the passengers."},
    {"word": "alternative", "sentence": "There was an ____ pattern for using the land in response to demographic change."},
    {"word": "malfunction", "sentence": "No one can figure out what is happening in time to prevent the ____ from blowing up the reactor."},
    {"word": "consecutive", "sentence": "It was the second ____ night the crew had pulled duty."},
    {"word": "catastrophe", "sentence": "It is the same small set of human errors that cause the ____."},
    {"word": "ethnic", "sentence": "The ____ Theory of Plane Crashes."},
    {"word": "terrain", "sentence": "We'll look at the weather and the ____ and the airport conditions."},
    {"word": "proximity", "sentence": "The final approach is demanding because of the ____ to the ground."},
    {"word": "invariably", "sentence": "He could ____ look back to the early days of the pilot's career and see the same kinds of errors."},
    {"word": "perspective", "sentence": "We were to have a completely different ____ on how the world works."},
    {"word": "jurisdiction", "sentence": "Aviation ____ was given to the Ministry of Construction and Transportation."},
    {"word": "cockpit", "sentence": "What they did in that ____ makes no sense at all through the lens of Western pilot culture."},
    {"word": "revoke", "sentence": "They were considering ____ the company's overflight and landing privileges."},
    {"word": "erode", "sentence": "Management was trying to ____ their authority."},
    {"word": "tenant", "sentence": "The first three storeys were typically given over to showrooms and the downstairs ____."},
    {"word": "peasant", "sentence": "The life of a rice farmer was different from the life of a European tenant ____."},
    {"word": "oppressive", "sentence": "China and Japan never developed that kind of ____ feudal system."},
    {"word": "proclivity", "sentence": "Not about an airline with a ____ for crashing but about one that transformed its image."},
    {"word": "equivalent", "sentence": "Their lives are also—in an odd way—entirely ____."},
    {"word": "outperform", "sentence": "The Korean economy had managed to ____ its rivals."},
    {"word": "correspond", "sentence": "Differences that ____ perfectly to Helmreich's findings."},
    {"word": "irrigate", "sentence": "Make sure the soil is properly ____."},
    {"word": "hibernate", "sentence": "Trees go through cycles of growth and dormancy, ____ in the winter and exploding in the spring."},
    {"word": "idleness", "sentence": "The peasant could indulge in ____ and festivities."},
    {"word": "vague", "sentence": "Few parents would have been so ____ about their calendars."},
    {"word": "infinite", "sentence": "The ____ improbability of successful lives."},
    {"word": "endeavor", "sentence": "Success is a purposeful ____ that we make in concert with others."},
    {"word": "tedious", "sentence": "The subject is ____ and technical."},
    {"word": "stereotype", "sentence": "He is a living argument against the ____ that Jews are good with numbers."},
    {"word": "abstract", "sentence": "They had a lively interest in the ____ questions of their field."},
    {"word": "trivial", "sentence": "This was not just a ____ scientific observation."},
    {"word": "vertical", "sentence": "Organizations could be horizontal or ____."},
    {"word": "cultivate", "sentence": "Rice farmers had to ____ a single field for more than half of the year."},
    {"word": "hierarchy", "sentence": "Power distance is concerned with attitudes toward ____."},
    {"word": "consequence", "sentence": "Showing more or less respect has real, practical ____."},
    {"word": "postmortem", "sentence": "Consultants examined the company in the ____."},
    {"word": "evident", "sentence": "The crash made it ____."},
    {"word": "devastating", "sentence": "The consequences were ____."},
    {"word": "freight", "sentence": "Cargo and ____ would be turned away."},
    {"word": "subservient", "sentence": "Systems based on the idea of hierarchy and ____ work ethic."},
    {"word": "anonymous", "sentence": "A voice to students whose opinions had been marginalized or ____."},
    {"word": "advocate", "sentence": "He became these children's ____."},
    {"word": "predicament", "sentence": "How that single mother manages to lift herself out of her ____."},
    {"word": "ambiguity", "sentence": "Routines remove the possibility of error and ____."},
    {"word": "distinctive", "sentence": "These are the ____ qualities of successful people."},
    {"word": "illusion", "sentence": "When we strip away the ____ of innate talent."},
    {"word": "plight", "sentence": "He has tried and failed to communicate his ____."},
    {"word": "subtlety", "sentence": "____ of requests—how much attention each party must pay to the other."},
    {"word": "intimidating", "sentence": "New York ATC can be very, very ____."},
    {"word": "identical", "sentence": "If you compare the two rankings, they are ____."},
    {"word": "relentless", "sentence": "The same ____ , intricate pattern of agriculture."},
]

MODES = {
    "ko": {"label": "한영", "prompt_key": "meaning", "data": KO_EN},
    "en": {"label": "영영", "prompt_key": "definition", "data": EN_EN},
    "ex": {"label": "예문", "prompt_key": "sentence", "data": EXAMPLES},
}


@app.route("/")
def index():
    counts = {k: len(v["data"]) for k, v in MODES.items()}
    return render_template("index.html", counts=counts)


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

    item = random.choice(data_list)
    return jsonify({
        "mode": mode,
        "label": MODES[mode]["label"],
        "prompt_key": prompt_key,
        "prompt": item[prompt_key],
        "empty": False
    })


@app.route("/api/check", methods=["POST"])
def api_check():
    payload = request.get_json(force=True)

    mode = (payload.get("mode") or "ko").strip()
    prompt = (payload.get("prompt") or "").strip()
    answer = (payload.get("answer") or "").strip()

    if mode not in MODES:
        return jsonify({"ok": False, "error": "Invalid mode"}), 400

    data_list = MODES[mode]["data"]
    prompt_key = MODES[mode]["prompt_key"]

    if not data_list:
        return jsonify({"ok": False, "error": "Empty mode data"}), 400

    candidates = [w for w in data_list if (w.get(prompt_key) or "").strip() == prompt]
    if not candidates:
        return jsonify({"ok": False, "error": "Prompt not found"}), 400

    correct_word = candidates[0]["word"]
    is_correct = answer.lower() == correct_word.lower()

    return jsonify({
        "correct": is_correct,
        "correct_word": correct_word
    })


if __name__ == "__main__":
    app.run(debug=True)
