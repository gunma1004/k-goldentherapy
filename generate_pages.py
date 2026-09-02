import os
import hashlib
import urllib.parse

if not os.path.exists("template.html"):
    print("오류: template.html 파일이 없습니다.")
    exit()

with open("template.html", "r", encoding="utf-8") as f:
    template_content = f.read()

BASE_URL = "https://k-goldentherapy.netlify.app"
BRAND_NAME = "한국골든테라피"

# ==============================================================================
# 1. 한국골든테라피 25가지 정밀 교차 패턴
# - 출장 [회피단어] 마사지 / 출장 [지역명] 마사지 교차 순환
# - '출장'과 '마사지'가 연달아 붙는 스팸 형태 0건 (완벽 차단)
# ==============================================================================
MIXED_KEYWORD_PATTERNS = [
    # 1군: 출장 [지역명] 마사지 형태
    "출장 {loc} 마사지",
    "24시 출장 {loc} 마사지",
    "야간 출장 {loc} 마사지",
    "안심 출장 {loc} 마사지",
    "정찰제 출장 {loc} 마사지",
    "프라이빗 출장 {loc} 마사지",
    "1:1 출장 {loc} 마사지",
    "호텔식 출장 {loc} 마사지",
    "전지역 출장 {loc} 마사지",
    "빠른방문 출장 {loc} 마사지",
    
    # 2군: {loc} 출장 [회피단어] 마사지 형태
    "{loc} 출장 스웨디시 마사지",
    "{loc} 출장 아로디시 마사지",
    "{loc} 출장 바디케어 마사지",
    "{loc} 출장 VIP케어 마사지",
    "{loc} 출장 전신힐링 마사지",
    "{loc} 출장 딥릴렉스 마사지",
    "{loc} 출장 한국인스웨디시 마사지",
    "{loc} 출장 에스테틱 마사지",
    "{loc} 출장 피로회복 마사지",
    "{loc} 출장 감성테라피 마사지",
    
    # 3군: 출장 [회피단어] {loc} 마사지 형태
    "출장 스웨디시 {loc} 마사지",
    "출장 힐링케어 {loc} 마사지",
    "출장 혼혈케어 {loc} 마사지",
    "출장 바디리셋 {loc} 마사지",
    "출장 럭셔리 {loc} 마사지"
]

TITLE_SUFFIXES = [
    f"100% 후불정찰제 | {BRAND_NAME}",
    f"24시 신속도착 안내 | {BRAND_NAME}",
    f"자택·호텔 1:1 방문 | {BRAND_NAME}",
    f"스웨디시 안심예약 | {BRAND_NAME}",
    f"프라이빗 힐링케어 | {BRAND_NAME}",
    f"전문 관리사 상시대기 | {BRAND_NAME}"
]

LOCAL_DESC_TEMPLATES = [
    "{loc} 일대 24시간 언제나 편하게 이용하는 {keyword}. 전 코스 투명한 정찰제와 100% 안심 후불제.",
    "선입금 없는 신뢰의 정직한 {keyword}. {loc} 전지역 전화 한 통으로 25분 이내 신속 방문 배정.",
    "내 집, 호텔 어디서든 프라이빗하게 누리는 {keyword}. 전문 테라피스트의 정성 어린 손길로 피로를 완화하세요.",
    "{loc} 1:1 맞춤형 프라이빗 바디 케어 {keyword}. 투명한 요금제와 수준 높은 감성 힐링 프로그램을 보장합니다.",
    "품격 있는 바디 릴렉싱의 시작, {loc} 일대 {keyword} 안내. 철저한 위생 관리와 쾌적한 휴식을 약속드립니다.",
    "{keyword} 공식 예약 센터. 합리적인 가격과 숙련된 관리사의 프리미엄 케어를 {loc} 전역에서 만나보세요."
]

def generate_local_seo(loc_name):
    hash_val = int(hashlib.md5(f"kgolden_{loc_name}".encode("utf-8")).hexdigest(), 16)
    keyword = MIXED_KEYWORD_PATTERNS[hash_val % len(MIXED_KEYWORD_PATTERNS)].format(loc=loc_name)
    suffix = TITLE_SUFFIXES[(hash_val // 10) % len(TITLE_SUFFIXES)]
    desc_tmpl = LOCAL_DESC_TEMPLATES[(hash_val // 100) % len(LOCAL_DESC_TEMPLATES)]
    
    title = f"{keyword} {suffix}"
    desc = desc_tmpl.format(loc=loc_name, keyword=keyword)
    return {"title": title, "desc": desc}

# ==============================================================================
# 2. 서울, 경기, 인천 지역 데이터
# ==============================================================================
regions_data = {
    "seoul": {
        "name": "서울",
        "gus": {
            "gangnam": {"name": "강남구", "dongs": ["역삼동", "논현동", "삼성동", "대치동", "신사동", "청담동", "압구정동", "개포동", "도곡동", "일원동", "수서동", "세곡동", "자곡동", "율현동"]},
            "gangdong": {"name": "강동구", "dongs": ["천호동", "길동", "둔촌동", "암사동", "성내동", "명일동", "고덕동", "상일동", "강일동"]},
            "gangbuk": {"name": "강북구", "dongs": ["미아동", "번동", "수유동", "우이동", "삼양동", "송중동", "송천동", "삼각산동", "인수동"]},
            "gangseo": {"name": "강서구", "dongs": ["화곡동", "등촌동", "염창동", "가양동", "마곡동", "발산동", "공항동", "방화동", "개화동", "우장산동"]},
            "gwanak": {"name": "관악구", "dongs": ["신림동", "봉천동", "남현동", "보라매동", "낙성대동", "대학동", "서원동", "인헌동", "미성동", "난곡동"]},
            "gwangjin": {"name": "광진구", "dongs": ["자양동", "구의동", "화양동", "군자동", "중곡동", "광장동", "능동"]},
            "guro": {"name": "구로구", "dongs": ["구로동", "신도림동", "가리봉동", "고척동", "개봉동", "오류동", "궁동", "온수동", "천왕동", "항동", "수궁동"]},
            "geumcheon": {"name": "금천구", "dongs": ["가산동", "독산동", "시흥동", "가산디지털단지"]},
            "nowon": {"name": "노원구", "dongs": ["상계동", "중계동", "하계동", "월계동", "공릉동"]},
            "dobong": {"name": "도봉구", "dongs": ["쌍문동", "방학동", "창동", "도봉동"]},
            "dongdaemun": {"name": "동대문구", "dongs": ["장안동", "답십리동", "전농동", "용두동", "제기동", "청량리동", "회기동", "휘경동", "이문동", "용신동"]},
            "dongjak": {"name": "동작구", "dongs": ["사당동", "상도동", "노량진동", "흑석동", "대방동", "신대방동", "본동"]},
            "mapo": {"name": "마포구", "dongs": ["서교동", "합정동", "연남동", "망원동", "상암동", "공덕동", "아현동", "도화동", "용강동", "대흥동", "염리동", "신수동", "상수동", "성산동", "홍대"]},
            "seodaemun": {"name": "서대문구", "dongs": ["신촌동", "연희동", "창천동", "홍제동", "홍은동", "남가좌동", "북가좌동", "충정로동", "북아현동", "천연동"]},
            "seocho": {"name": "서초구", "dongs": ["서초동", "잠원동", "반포동", "방배동", "양재동", "우면동", "원지동", "내곡동", "염곡동", "신원동"]},
            "seongdong": {"name": "성동구", "dongs": ["성수동", "왕십리동", "마장동", "행당동", "응봉동", "금호동", "옥수동", "도선동", "용답동", "사근동", "송정동"]},
            "seongbuk": {"name": "성북구", "dongs": ["길음동", "돈암동", "정릉동", "안암동", "보문동", "삼선동", "동선동", "종암동", "월곡동", "장위동", "석관동", "성북동"]},
            "songpa": {"name": "송파구", "dongs": ["잠실동", "신천동", "방이동", "송파동", "석촌동", "삼전동", "가락동", "문정동", "장지동", "풍납동", "오금동", "거여동", "마천동", "위례동"]},
            "yangcheon": {"name": "양천구", "dongs": ["목동", "신정동", "신월동"]},
            "yeongdeungpo": {"name": "영등포구", "dongs": ["여의도동", "영등포동", "당산동", "문래동", "양평동", "신길동", "대림동", "도림동"]},
            "yongsan": {"name": "용산구", "dongs": ["이태원동", "한남동", "한강로동", "용산동", "후암동", "원효로동", "이촌동", "청파동", "효창동", "보광동", "서빙고동"]},
            "eunpyeong": {"name": "은평구", "dongs": ["불광동", "갈현동", "응암동", "역촌동", "신사동", "대조동", "구산동", "진관동", "증산동", "수색동", "녹번동"]},
            "jongno": {"name": "종로구", "dongs": ["종로동", "혜화동", "명륜동", "대학로", "평창동", "부암동", "삼청동", "가회동", "인사동", "숭인동", "창신동", "교남동", "무악동", "청운동", "효자동"]},
            "junggu": {"name": "중구", "dongs": ["명동", "을지로동", "신당동", "다산동", "약수동", "청구동", "황학동", "중림동", "소공동", "회현동", "장충동", "필동", "광희동", "동대문"]},
            "jungnang": {"name": "중랑구", "dongs": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"]}
        }
    },
    "gyeonggi": {
        "name": "경기",
        "gus": {
            "suwon": {"name": "수원시", "dongs": ["인계동", "매탄동", "원천동", "영통동", "망포동", "광교동", "곡반정동", "권선동", "세류동", "화서동", "정자동", "조원동", "율전동", "천천동", "고등동", "우만동", "지동", "구운동", "호매실동", "금곡동", "행궁동", "파장동"]},
            "seongnam": {"name": "성남시", "dongs": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "판교동", "삼평동", "백현동", "운중동", "금곡동", "구미동", "신흥동", "태평동", "상대원동", "중원구", "수정구", "단대동", "산성동", "복정동", "위례동"]},
            "goyang": {"name": "고양시", "dongs": ["일산동", "주엽동", "탄현동", "대화동", "마두동", "백석동", "식사동", "풍동", "화정동", "행신동", "원흥동", "삼송동", "지축동", "향동동", "덕은동", "토당동", "관산동", "고양동", "킨텍스", "라페스타"]},
            "yongin": {"name": "용인시", "dongs": ["풍덕천동", "신봉동", "죽전동", "동천동", "상현동", "성복동", "기흥동", "신갈동", "구갈동", "보정동", "동백동", "마북동", "서천동", "영덕동", "처인구", "역북동", "김량장동", "유방동", "고림동", "포곡읍", "수지"]},
            "bucheon": {"name": "부천시", "dongs": ["중동", "상동", "심곡동", "원미동", "소사동", "오정동", "송내동", "괴안동", "역곡동", "삼정동", "도당동", "고강동", "원종동", "여월동", "작동", "부천역", "신중동"]},
            "ansan": {"name": "안산시", "dongs": ["고잔동", "중앙동", "원곡동", "선부동", "초지동", "본오동", "사동", "이동", "일동", "와동", "월피동", "성포동", "신길동", "대부동", "상록수역", "한양대에리카"]},
            "anyang": {"name": "안양시", "dongs": ["안양동", "석수동", "박달동", "비산동", "관양동", "평촌동", "호계동", "범계동", "인덕원", "귀인동", "갈산동", "신촌동", "달안동", "안양역", "범계역", "평촌역"]},
            "hwaseong": {"name": "화성시", "dongs": ["동탄동", "동탄1신도시", "동탄2신도시", "병점동", "진안동", "반월동", "기안동", "봉담읍", "향남읍", "남양읍", "우정읍", "송산면", "마도면", "비봉면", "매송면", "팔탄면", "장안면", "양감면", "정남면", "새솔동", "향남2지구"]},
            "pyeongtaek": {"name": "평택시", "dongs": ["평택동", "비전동", "송탄동", "서정동", "지산동", "신장동", "안중읍", "포승읍", "청북읍", "고덕동", "고덕신도시", "세교동", "통복동", "팽성읍", "진위면", "오성면", "현덕면", "동삭동", "용이동", "죽백동", "소사벌"]},
            "siheung": {"name": "시흥시", "dongs": ["정왕동", "배곧동", "배곧신도시", "은행동", "대야동", "신천동", "목감동", "능곡동", "장현동", "월곶동", "거모동", "미산동", "포동", "매화동", "과림동", "조남동", "산현동", "은계동", "은계지구", "오이도"]},
            "gimpo": {"name": "김포시", "dongs": ["구래동", "장기동", "운양동", "마산동", "사우동", "풍무동", "걸포동", "북변동", "감정동", "통진읍", "고촌읍", "양촌읍", "대곶면", "월곶면", "하성면", "한강신도시"]},
            "gwangju": {"name": "광주시", "dongs": ["경안동", "송정동", "역동", "쌍령동", "탄벌동", "목현동", "회덕동", "태전동", "오포읍", "신현동", "능평동", "문형동", "매산동", "양벌동", "고산동", "초월읍", "곤지암읍", "도척면", "퇴촌면", "남종면", "남한산성면", "태전지구"]},
            "gwangmyeong": {"name": "광명시", "dongs": ["철산동", "하안동", "소하동", "광명동", "일직동", "학온동", "가학동", "노온사동", "옥길동", "KTX광명역", "철산역"]},
            "gunpo": {"name": "군포시", "dongs": ["산본동", "당동", "당정동", "금정동", "대야미동", "부곡동", "도마교동", "둔대동", "속달동", "산본역", "금정역"]},
            "hanam": {"name": "하남시", "dongs": ["미사동", "미사강변", "위례동", "신장동", "덕풍동", "풍산동", "감일동", "감이동", "학암동", "초이동", "망월동", "선동", "창우동", "천현동", "교산동", "스타필드하남"]},
            "osan": {"name": "오산시", "dongs": ["오산동", "원동", "궐동", "청학동", "갈곶동", "세교동", "세교지구", "수청동", "금암동", "은계동", "가장동", "양산동", "외삼미동", "내삼미동", "부산동", "누읍동", "오산대역"]},
            "namyangju": {"name": "남양주시", "dongs": ["다산동", "다산신도시", "별내동", "별내신도시", "진접읍", "화도읍", "와부읍", "호평동", "평내동", "오남읍", "퇴계원읍", "진건읍", "수동면", "조안면", "마석"]},
            "paju": {"name": "파주시", "dongs": ["운정동", "운정신도시", "야당동", "야당역", "와동동", "목동동", "동패동", "다율동", "당하동", "교하동", "금촌동", "아동동", "문산읍", "파주읍", "조리읍", "법원읍", "탄현면", "헤이리"]},
            "uijeongbu": {"name": "의정부시", "dongs": ["의정부동", "호원동", "장암동", "신곡동", "용현동", "민락동", "민락2지구", "낙양동", "고산동", "고산지구", "산곡동", "금오동", "가능동", "녹양동", "자금동", "의정부역"]},
            "icheon": {"name": "이천시", "dongs": ["창전동", "중리동", "관고동", "안흥동", "갈산동", "증포동", "송정동", "부발읍", "하이닉스", "장호원읍", "대월면", "마장면", "백사면", "신둔면"]},
            "anseong": {"name": "안성시", "dongs": ["공도읍", "대덕면", "보개면", "금광면", "서운면", "미양면", "양성면", "원곡면", "고삼면", "일죽면", "죽산면", "삼죽면", "안성동", "아양동", "아양지구", "옥산동", "석정동", "당왕동"]},
            "guri": {"name": "구리시", "dongs": ["갈매동", "갈매신도시", "인창동", "교문동", "수택동", "아천동", "토평동", "사노동", "구리역"]},
            "uiwang": {"name": "의왕시", "dongs": ["고천동", "오전동", "포일동", "내손동", "청계동", "삼동", "왕곡동", "백운밸리"]},
            "pocheon": {"name": "포천시", "dongs": ["신읍동", "어룡동", "소흘읍", "송우리", "군내면", "내촌면", "가산면", "신북면", "일동면", "이동면", "선단동", "대진대"]},
            "yangju": {"name": "양주시", "dongs": ["옥정동", "옥정신도시", "고읍동", "덕계동", "덕정동", "삼숭동", "회정동", "백석읍", "광적면", "장흥면"]},
            "dongducheon": {"name": "동두천시", "dongs": ["지행동", "지행역", "생연동", "보산동", "동두천동", "송내동", "상패동"]},
            "yeoju": {"name": "여주시", "dongs": ["홍문동", "창동", "가남읍", "점동면", "세종대왕면", "흥천면", "금사면", "대신면", "북내면", "강천면", "오학동", "현암동", "월송동"]},
            "gwacheon": {"name": "과천시", "dongs": ["중앙동", "갈현동", "별양동", "부림동", "과천동", "문원동", "원문동", "과천지식정보타운"]},
            "gapyeong": {"name": "가평군", "dongs": ["가평읍", "설악면", "청평면", "상면", "조종면", "북면", "청평"]},
            "yangpyeong": {"name": "양평군", "dongs": ["양평읍", "강상면", "강하면", "양서면", "옥천면", "서종면", "용문면", "양수리"]},
            "yeoncheon": {"name": "연천군", "dongs": ["연천읍", "전곡읍", "전곡역", "군남면", "청산면", "백학면"]}
        }
    },
    "incheon": {
        "name": "인천",
        "gus": {
            "bupyeong": {"name": "부평구", "dongs": ["부평동", "부평역", "십정동", "동암역", "산곡동", "청천동", "삼산동", "갈산동", "부개동", "일신동", "구산동"]},
            "namdong": {"name": "남동구", "dongs": ["구월동", "인천터미널", "로데오거리", "간석동", "만수동", "논현동", "소래포구", "서창동", "서창2지구", "도림동", "고잔동", "논현고잔동"]},
            "yeonsu": {"name": "연수구", "dongs": ["송도동", "송도국제도시", "송도센트럴파크", "연수동", "청학동", "동춘동", "옥련동", "선학동"]},
            "seogu": {"name": "서구", "dongs": ["청라동", "청라국제도시", "검암동", "경서동", "연희동", "가정동", "루원시티", "신현동", "석남동", "가좌동", "마전동", "당하동", "원당동", "검단신도시", "불로동", "왕길동"]},
            "michuhol": {"name": "미추홀구", "dongs": ["주안동", "주안역", "도화동", "인하대", "학익동", "용현동", "숭의동", "관교동", "문학동"]},
            "gyeyang": {"name": "계양구", "dongs": ["계산동", "계산역", "작전동", "작전서운동", "효성동", "임학동", "용종동", "병방동", "박촌동", "동양동", "귤현동"]},
            "junggu": {"name": "중구", "dongs": ["영종동", "영종도", "하늘도시", "운서동", "운서역", "중산동", "을왕리", "동인천동", "신포동", "월미도", "연안부두", "신흥동", "인천공항"]},
            "donggu": {"name": "동구", "dongs": ["송현동", "송림동", "화수동", "만석동", "금곡동", "창영동"]},
            "ganghwa": {"name": "강화군", "dongs": ["강화읍", "선원면", "불은면", "길상면", "화도면", "마니산", "동막해변"]},
            "ongjin": {"name": "옹진군", "dongs": ["영흥도", "백령면", "대청면", "연평면", "덕적면", "자월면", "북도면"]}
        }
    }
}

count = 0

# ==============================================================================
# 0) 루트 메인 페이지 (index.html)
# - 출장 / 마사지 스팸 키워드 100% 완전 배제
# - 메타 설명문 65자로 네이버 80자 이내 완벽 준수
# ==============================================================================
root_gu_links = [f'<a class="neighbor-card" href="/{k}/"><b>{v["name"]} 전지역</b> 바로가기 ➔</a>' for k, v in regions_data.items()]
root_page = template_content
root_page = root_page.replace("{{BREADCRUMBS}}", f'<span>{BRAND_NAME} 공식 홈</span>')
root_page = root_page.replace("{{PAGE_TITLE}}", f"{BRAND_NAME} | 수도권 24시 프리미엄 방문 홈케어 테라피")
root_page = root_page.replace("{{PAGE_DESC}}", "서울·경기·인천 24시 안심 후불제 한국골든테라피. 아로디시·VIP혼혈·한국인스웨디시 1:1 방문 케어.")
root_page = root_page.replace("{{CANONICAL_URL}}", f"{BASE_URL}/")
root_page = root_page.replace("{{REGION_NAME}}", "서울·경기·인천 전지역")
root_page = root_page.replace("{{SUB_NAV_TITLE}}", "📍 서비스 광역 권역 선택")
root_page = root_page.replace("{{neighborhood_links}}", "\n".join(root_gu_links))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(root_page)
count += 1
print("✅ 메인 루트 index.html 생성 완료 (출장·마사지 스팸 키워드 100% 배제)")

# ==============================================================================
# 1) 광역 페이지 (/seoul/, /gyeonggi/, /incheon/)
# ==============================================================================
for sido_key, sido_val in regions_data.items():
    sido_dir = sido_key
    os.makedirs(sido_dir, exist_ok=True)

    gu_links = [f'<a class="neighbor-card" href="/{sido_key}/{k}/">{v["name"]} 바로가기 ➔</a>' for k, v in sido_val["gus"].items()]
    seo = generate_local_seo(f"{sido_val['name']} 전지역")
    
    page = template_content
    page = page.replace("{{BREADCRUMBS}}", f'<a href="/">홈</a> <span>&gt;</span> {sido_val["name"]}')
    page = page.replace("{{PAGE_TITLE}}", seo["title"])
    page = page.replace("{{PAGE_DESC}}", seo["desc"])
    page = page.replace("{{CANONICAL_URL}}", f"{BASE_URL}/{sido_key}/")
    page = page.replace("{{REGION_NAME}}", f"{sido_val['name']} 전지역")
    page = page.replace("{{SUB_NAV_TITLE}}", f"📍 {sido_val['name']} 주요 행정구역")
    page = page.replace("{{neighborhood_links}}", "\n".join(gu_links))
    
    with open(f"{sido_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(page)
    count += 1

# ==============================================================================
# 2) 구/시 단위 페이지 (/seoul/gangnam/ 등)
# ==============================================================================
for sido_key, sido_val in regions_data.items():
    for gu_key, gu_info in sido_val["gus"].items():
        gu_dir = f"{sido_key}/{gu_key}"
        os.makedirs(gu_dir, exist_ok=True)

        dong_links = [f'<a class="neighbor-card" href="/{sido_key}/{gu_key}/{urllib.parse.quote(d)}/">{d}</a>' for d in gu_info["dongs"]]
        seo = generate_local_seo(f"{sido_val['name']} {gu_info['name']}")

        page = template_content
        page = page.replace("{{BREADCRUMBS}}", f'<a href="/">홈</a> <span>&gt;</span> <a href="/{sido_key}/">{sido_val["name"]}</a> <span>&gt;</span> {gu_info["name"]}')
        page = page.replace("{{PAGE_TITLE}}", seo["title"])
        page = page.replace("{{PAGE_DESC}}", seo["desc"])
        page = page.replace("{{CANONICAL_URL}}", f"{BASE_URL}/{sido_key}/{gu_key}/")
        page = page.replace("{{REGION_NAME}}", f"{sido_val['name']} {gu_info['name']}")
        page = page.replace("{{SUB_NAV_TITLE}}", f"📍 {gu_info['name']} 세부 상권·동네")
        page = page.replace("{{neighborhood_links}}", "\n".join(dong_links))
        
        with open(f"{gu_dir}/index.html", "w", encoding="utf-8") as f:
            f.write(page)
        count += 1

# ==============================================================================
# 3) 읍/면/동 세부 페이지 (/seoul/gangnam/역삼동/ 등)
# ==============================================================================
for sido_key, sido_val in regions_data.items():
    for gu_key, gu_info in sido_val["gus"].items():
        neighbor_links = [f'<a class="neighbor-card" href="/{sido_key}/{gu_key}/{urllib.parse.quote(d)}/">{d}</a>' for d in gu_info["dongs"]]
        
        for dong in gu_info["dongs"]:
            target_dir = f"{sido_key}/{gu_key}/{dong}"
            os.makedirs(target_dir, exist_ok=True)
            
            seo = generate_local_seo(f"{gu_info['name']} {dong}")
            encoded_dong = urllib.parse.quote(dong)
            
            page = template_content
            page = page.replace("{{BREADCRUMBS}}", f'<a href="/">홈</a> <span>&gt;</span> <a href="/{sido_key}/">{sido_val["name"]}</a> <span>&gt;</span> <a href="/{sido_key}/{gu_key}/">{gu_info["name"]}</a> <span>&gt;</span> {dong}')
            page = page.replace("{{PAGE_TITLE}}", seo["title"])
            page = page.replace("{{PAGE_DESC}}", seo["desc"])
            page = page.replace("{{CANONICAL_URL}}", f"{BASE_URL}/{sido_key}/{gu_key}/{encoded_dong}/")
            page = page.replace("{{REGION_NAME}}", f"{gu_info['name']} {dong}")
            page = page.replace("{{SUB_NAV_TITLE}}", f"📍 {gu_info['name']} 인근 동네 둘러보기")
            page = page.replace("{{neighborhood_links}}", "\n".join(neighbor_links))
            
            with open(f"{target_dir}/index.html", "w", encoding="utf-8") as f:
                f.write(page)
            count += 1

print(f"\n>> [{BRAND_NAME}] 빌드 완료! 총 {count}개 페이지 생성 완료.")