import streamlit as st
from datetime import date, time, datetime, timedelta
import swisseph as swe
import pandas as pd
import calendar

st.set_page_config(page_title="Astro Life AI", page_icon="🔮", layout="wide")

SIGNS_EN = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
SIGNS_NE = ["मेष", "वृष", "मिथुन", "कर्कट", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुम्भ", "मीन"]
PLANETS = [
    ("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS),
    ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER), ("Venus", swe.VENUS),
    ("Saturn", swe.SATURN), ("Rahu", swe.MEAN_NODE)
]
LANGS = ["हिंदी", "नेपाली", "English"]

TEXT = {
"हिंदी": {
"title":"🔮 Astro Life AI", "subtitle":"जन्मकुंडली • करियर • पैसा • प्रेम • विवाह • जीवन के चरण • वर्षफल 2027",
"inputs":"जन्म विवरण", "name":"नाम (वैकल्पिक)", "dob":"जन्म तारीख", "tob":"जन्म समय (स्थानीय)", "lat":"अक्षांश (Latitude)", "lon":"देशांतर (Longitude)", "tz":"UTC से समय अंतर (नेपाल: 5.75)", "calculate":"कुंडली और रिपोर्ट बनाएं",
"overview":"आपकी ज्योतिष रिपोर्ट", "birth":"जन्म कुंडली के ग्रह", "annual":"🔮 वर्षफल 2027", "month":"महीना-दर-महीना रोडमैप", "career":"करियर और नौकरी", "money":"पैसा और वित्त", "love":"प्रेम और संबंध", "marriage":"विवाह", "health":"स्वास्थ्य", "life":"जीवन के महत्वपूर्ण चरण",
"disclaimer":"यह पारंपरिक ज्योतिष पर आधारित सामान्य व्याख्या है, निश्चित भविष्यवाणी नहीं। स्वास्थ्य संबंधी निर्णय के लिए डॉक्टर और वित्त/करियर संबंधी निर्णय के लिए वास्तविक जानकारी व विशेषज्ञ सलाह को प्राथमिकता दें।",
"no":"पहले जन्म विवरण भरकर रिपोर्ट बनाएं।", "lagna":"लग्न", "moon":"चंद्र राशि", "sun":"सूर्य राशि", "house":"भाव", "sign":"राशि", "planet":"ग्रह", "position":"डिग्री",
"career_text":"करियर में परिणाम कौशल, अनुभव, आवेदन और अवसरों पर निर्भर करते हैं। कुंडली को आत्मचिंतन के संकेत की तरह लें; नियमित आवेदन, CV सुधार और इंटरव्यू अभ्यास पर ध्यान दें।",
"money_text":"आय और बचत के लिए बजट, आपातकालीन बचत और जोखिम समझना अधिक उपयोगी है। ज्योतिष के आधार पर निवेश या कर्ज का निर्णय अकेले न लें।",
"love_text":"रिश्ते में स्पष्ट बातचीत, सम्मान, भरोसा और दोनों की सहमति सबसे महत्वपूर्ण हैं। ज्योतिष को संबंध का अंतिम फैसला न बनाएं।",
"marriage_text":"विवाह का सही समय केवल कुंडली से निश्चित नहीं किया जा सकता। आपसी समझ, तैयारी, सहमति और जीवन की परिस्थितियां भी महत्वपूर्ण हैं।",
"health_text":"कुंडली बीमारी का निदान या भविष्य में बीमारी की विश्वसनीय भविष्यवाणी नहीं कर सकती। लक्षण हों तो योग्य स्वास्थ्यकर्मी से संपर्क करें।",
"life_text":"महत्वपूर्ण जीवन चरणों को निश्चित घटना न समझें। लक्ष्यों को 3–6 महीने के छोटे चरणों में बांटें और प्रगति की समीक्षा करें।",
"annual_intro":"यह 2027 के प्रत्येक महीने के मध्य में ग्रहों की राशि देखकर बनाया गया सामान्य ज्योतिषीय कैलेंडर है; यह पारंपरिक सटीक ताजिक वर्षफल कुंडली का विकल्प नहीं है।",
"good":"योजना, सीखने और नियमित प्रयास पर ध्यान दें।", "care":"बड़े निर्णय से पहले तथ्यों की जांच करें और जल्दबाजी से बचें."
},
"नेपाली": {
"title":"🔮 Astro Life AI", "subtitle":"जन्मकुण्डली • करियर • पैसा • प्रेम • विवाह • जीवनका चरण • वर्षफल २०२७",
"inputs":"जन्म विवरण", "name":"नाम (ऐच्छिक)", "dob":"जन्म मिति", "tob":"जन्म समय (स्थानीय)", "lat":"अक्षांश (Latitude)", "lon":"देशान्तर (Longitude)", "tz":"UTC बाट समय अन्तर (नेपाल: 5.75)", "calculate":"कुण्डली र रिपोर्ट बनाउनुहोस्",
"overview":"तपाईंको ज्योतिष रिपोर्ट", "birth":"जन्मकुण्डलीका ग्रह", "annual":"🔮 वर्षफल २०२७", "month":"महिना अनुसार रोडम्याप", "career":"करियर र जागिर", "money":"पैसा र वित्त", "love":"प्रेम र सम्बन्ध", "marriage":"विवाह", "health":"स्वास्थ्य", "life":"जीवनका महत्वपूर्ण चरण",
"disclaimer":"यो परम्परागत ज्योतिषमा आधारित सामान्य व्याख्या हो, निश्चित भविष्यवाणी होइन। स्वास्थ्यका लागि चिकित्सक र वित्त/करियरका निर्णयका लागि वास्तविक जानकारी तथा विशेषज्ञ सल्लाहलाई प्राथमिकता दिनुहोस्।",
"no":"पहिले जन्म विवरण भरेर रिपोर्ट बनाउनुहोस्।", "lagna":"लग्न", "moon":"चन्द्र राशि", "sun":"सूर्य राशि", "house":"भाव", "sign":"राशि", "planet":"ग्रह", "position":"डिग्री",
"career_text":"करियरका नतिजा सीप, अनुभव, आवेदन र अवसरमा निर्भर हुन्छन्। नियमित आवेदन, CV सुधार र अन्तर्वार्ता अभ्यासमा ध्यान दिनुहोस्।",
"money_text":"आय र बचतका लागि बजेट, आपतकालीन बचत र जोखिम बुझ्नु उपयोगी हुन्छ। ज्योतिषका आधारमा मात्र लगानी वा ऋणको निर्णय नगर्नुहोस्।",
"love_text":"सम्बन्धमा स्पष्ट संवाद, सम्मान, विश्वास र दुवैको सहमति महत्वपूर्ण हुन्छ। ज्योतिषलाई सम्बन्धको अन्तिम निर्णय नबनाउनुहोस्।",
"marriage_text":"विवाहको समय कुण्डलीबाट निश्चित गर्न सकिँदैन। आपसी समझदारी, तयारी, सहमति र परिस्थितिहरू पनि महत्वपूर्ण छन्।",
"health_text":"कुण्डलीले रोगको निदान वा भविष्यमा रोग लाग्ने विश्वसनीय भविष्यवाणी गर्न सक्दैन। लक्षण भए स्वास्थ्यकर्मीसँग सम्पर्क गर्नुहोस्।",
"life_text":"जीवनका चरणलाई निश्चित घटना नमान्नुहोस्। लक्ष्यलाई ३–६ महिनाका साना चरणमा बाँडेर प्रगति समीक्षा गर्नुहोस्।",
"annual_intro":"यो २०२७ का प्रत्येक महिनाको मध्यमा ग्रहको राशि हेरेर बनाइएको सामान्य ज्योतिषीय क्यालेन्डर हो; यो परम्परागत सटीक ताजिक वर्षफल कुण्डलीको विकल्प होइन।",
"good":"योजना, सिकाइ र निरन्तर प्रयासमा ध्यान दिनुहोस्।", "care":"ठूला निर्णयअघि तथ्य जाँच्नुहोस् र हतार नगर्नुहोस्."
},
"English": {
"title":"🔮 Astro Life AI", "subtitle":"Birth chart • Career • Money • Love • Marriage • Life phases • Varshphal 2027",
"inputs":"Birth details", "name":"Name (optional)", "dob":"Date of birth", "tob":"Birth time (local)", "lat":"Latitude", "lon":"Longitude", "tz":"UTC offset (Nepal: 5.75)", "calculate":"Calculate chart and report",
"overview":"Your astrology report", "birth":"Birth chart planets", "annual":"🔮 Varshphal 2027", "month":"Month-by-month roadmap", "career":"Career & job", "money":"Money & finance", "love":"Love & relationships", "marriage":"Marriage", "health":"Health", "life":"Important life phases",
"disclaimer":"This is a general interpretation of traditional astrology, not a certain prediction. For health decisions consult a qualified clinician; for financial and career decisions prioritize real-world information and expert advice.",
"no":"Enter birth details and generate the report first.", "lagna":"Ascendant", "moon":"Moon sign", "sun":"Sun sign", "house":"House", "sign":"Sign", "planet":"Planet", "position":"Position",
"career_text":"Career outcomes depend on skills, experience, applications and opportunities. Use astrology for reflection; prioritize regular applications, CV improvements and interview practice.",
"money_text":"Budgeting, emergency savings and understanding risk are more useful for financial stability. Do not make investment or borrowing decisions based on astrology alone.",
"love_text":"Clear communication, respect, trust and mutual consent matter most in relationships. Do not treat astrology as the final verdict on a relationship.",
"marriage_text":"A marriage date cannot be determined reliably from a chart alone. Compatibility, readiness, consent and life circumstances matter too.",
"health_text":"A birth chart cannot diagnose disease or reliably predict future illness. Contact a qualified health professional if you have symptoms.",
"life_text":"Treat life phases as reflection prompts, not guaranteed events. Break goals into 3–6 month steps and review progress.",
"annual_intro":"This is a general astrology calendar based on planetary signs around the middle of each month in 2027; it is not a substitute for a precisely calculated traditional Tajika annual chart.",
"good":"Focus on planning, learning and consistent effort.", "care":"Verify facts and avoid rushing major decisions."
}
}

def sign_index(longitude):
    return int((longitude % 360) // 30)

def sign_name(idx, lang):
    arr = SIGNS_HI if lang == "हिंदी" else SIGNS_NE if lang == "नेपाली" else SIGNS_EN
    return arr[idx % 12]

def local_to_jd(birth_date, birth_time, utc_offset):
    local_dt = datetime.combine(birth_date, birth_time)
    utc_dt = local_dt - timedelta(hours=float(utc_offset))
    hour = utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour)

def calc_chart(birth_date, birth_time, lat, lon, utc_offset):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = local_to_jd(birth_date, birth_time, utc_offset)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    positions = {}
    for name, body in PLANETS:
        xx, ret = swe.calc_ut(jd, body, flags)
        positions[name] = xx[0] % 360
    # Mean Rahu is used; Ketu is always opposite Rahu.
    positions["Ketu"] = (positions["Rahu"] + 180) % 360
    cusps, ascmc = swe.houses_ex(jd, float(lat), float(lon), b'P', swe.FLG_SIDEREAL)
    asc = ascmc[0] % 360
    return jd, asc, positions

def house_from_sign(planet_sign, asc_sign):
    return ((planet_sign - asc_sign) % 12) + 1

def month_transits(year, lang, asc_sign):
    rows = []
    for m in range(1, 13):
        # Noon on the 15th, using the user's entered UTC offset is not necessary for sign-level overview.
        jd = swe.julday(year, m, 15, 12.0)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        data = {}
        for name, body in [("Jupiter", swe.JUPITER), ("Saturn", swe.SATURN), ("Rahu", swe.MEAN_NODE)]:
            xx, ret = swe.calc_ut(jd, body, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
            sidx = sign_index(xx[0])
            data[name] = f"{sign_name(sidx, lang)} (H{house_from_sign(sidx, asc_sign)})"
        rows.append({"Month": calendar.month_name[m], "Jupiter": data["Jupiter"], "Saturn": data["Saturn"], "Rahu": data["Rahu"]})
    return pd.DataFrame(rows)

def sign_house_theme(house, lang):
    hi = {
        1:"स्व-छवि, ऊर्जा और व्यक्तिगत दिशा", 2:"बचत, परिवार और संसाधन", 3:"कौशल, संवाद और प्रयास",
        4:"घर, परिवार और स्थिरता", 5:"रचनात्मकता, पढ़ाई और प्रेम", 6:"दिनचर्या, सेवा और चुनौतियाँ",
        7:"साझेदारी और संबंध", 8:"बदलाव, साझा संसाधन और गहन सीख", 9:"उच्च शिक्षा, यात्रा और विश्वास",
        10:"करियर, जिम्मेदारी और प्रतिष्ठा", 11:"लक्ष्य, नेटवर्क और लाभ", 12:"खर्च, विश्राम और विदेश"
    }
    ne = {
        1:"आत्मछवि, ऊर्जा र व्यक्तिगत दिशा", 2:"बचत, परिवार र स्रोत", 3:"सीप, संवाद र प्रयास",
        4:"घर, परिवार र स्थिरता", 5:"सिर्जनशीलता, पढाइ र प्रेम", 6:"दिनचर्या, सेवा र चुनौती",
        7:"साझेदारी र सम्बन्ध", 8:"परिवर्तन, साझा स्रोत र गहिरो सिकाइ", 9:"उच्च शिक्षा, यात्रा र विश्वास",
        10:"करियर, जिम्मेवारी र प्रतिष्ठा", 11:"लक्ष्य, सञ्जाल र लाभ", 12:"खर्च, आराम र विदेश"
    }
    en = {
        1:"identity, energy and personal direction", 2:"savings, family and resources", 3:"skills, communication and effort",
        4:"home, family and stability", 5:"creativity, study and romance", 6:"routine, service and challenges",
        7:"partnerships and relationships", 8:"change, shared resources and deeper learning", 9:"higher learning, travel and beliefs",
        10:"career, responsibility and reputation", 11:"goals, networks and gains", 12:"expenses, rest and foreign places"
    }
    return (hi if lang == "हिंदी" else ne if lang == "नेपाली" else en)[house]

def annual_summary(df, lang):
    months = df["Month"].tolist()
    out = []
    for i, row in df.iterrows():
        # Keep the month-by-month text as reflective planning guidance, not a deterministic prediction.
        month = row["Month"]
        if lang == "हिंदी":
            msg = f"**{month}:** गुरु {row['Jupiter']}, शनि {row['Saturn']}, राहु {row['Rahu']}। सीखने, काम और पैसों के फैसलों को वास्तविक परिस्थितियों के साथ मिलाकर देखें। {TEXT[lang]['good']}"
        elif lang == "नेपाली":
            msg = f"**{month}:** गुरु {row['Jupiter']}, शनि {row['Saturn']}, राहु {row['Rahu']}। पढाइ, काम र पैसाका निर्णयलाई वास्तविक परिस्थितिसँग मिलाएर हेर्नुहोस्। {TEXT[lang]['good']}"
        else:
            msg = f"**{month}:** Jupiter {row['Jupiter']}, Saturn {row['Saturn']}, Rahu {row['Rahu']}. Compare study, work and money decisions with real circumstances. {TEXT[lang]['good']}"
        out.append(msg)
    return out

st.title("🔮 Astro Life AI")
lang = st.selectbox("Language / भाषा / भाषा", LANGS, index=0)
T = TEXT[lang]
st.caption(T["subtitle"])
st.info(T["disclaimer"])

with st.sidebar:
    st.header(T["inputs"])
    person_name = st.text_input(T["name"])
    birth_date = st.date_input(T["dob"], value=date(2000, 4, 15), min_value=date(1900, 1, 1), max_value=date.today())
    birth_time = st.time_input(T["tob"], value=time(1, 0))
    latitude = st.number_input(T["lat"], value=27.6966, min_value=-90.0, max_value=90.0, format="%.4f")
    longitude = st.number_input(T["lon"], value=82.4861, min_value=-180.0, max_value=180.0, format="%.4f")
    utc_offset = st.number_input(T["tz"], value=5.75, min_value=-12.0, max_value=14.0, step=0.25)
    st.caption("Ghorahi, Nepal defaults: 27.6966° N, 82.4861° E, UTC+5:45.")
    submitted = st.button(T["calculate"], type="primary", use_container_width=True)

if submitted:
    try:
        jd, asc, positions = calc_chart(birth_date, birth_time, latitude, longitude, utc_offset)
        asc_sign = sign_index(asc)
        moon_sign = sign_index(positions["Moon"])
        sun_sign = sign_index(positions["Sun"])
        st.session_state["report"] = {
            "name": person_name, "date": birth_date, "time": birth_time, "asc": asc,
            "asc_sign": asc_sign, "positions": positions, "moon_sign": moon_sign,
            "sun_sign": sun_sign, "lat": latitude, "lon": longitude, "tz": utc_offset
        }
    except Exception as exc:
        st.error(f"Calculation error: {exc}")
        st.stop()

if "report" not in st.session_state:
    st.write(T["no"])
    st.markdown("### Features")
    st.markdown("- Birth chart and planetary signs\n- Career, money, love, marriage, health and life-stage reflection\n- Varshphal 2027 month-by-month transit calendar\n- Hindi, Nepali and English interface")
    st.stop()

r = st.session_state["report"]
positions = r["positions"]
asc_sign = r["asc_sign"]
st.header(T["overview"])
if r["name"]:
    st.write(f"**{r['name']}**")
c1, c2, c3 = st.columns(3)
c1.metric(T["lagna"], sign_name(asc_sign, lang))
c2.metric(T["moon"], sign_name(r["moon_sign"], lang))
c3.metric(T["sun"], sign_name(r["sun_sign"], lang))
st.caption(f"{r['date'].strftime('%d %B %Y')} • {r['time'].strftime('%H:%M')} • Lat {r['lat']}, Lon {r['lon']} • UTC {r['tz']:+g}")

st.subheader(T["birth"])
planet_rows = []
for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
    idx = sign_index(positions[p])
    planet_rows.append({
        T["planet"]: p,
        T["sign"]: sign_name(idx, lang),
        T["house"]: house_from_sign(idx, asc_sign),
        T["position"]: f"{positions[p] % 30:.2f}°"
    })
st.dataframe(pd.DataFrame(planet_rows), use_container_width=True, hide_index=True)

st.subheader(T["life"])
st.write(f"{T['life_text']}")
st.write(f"**{T['house']} 10:** {sign_house_theme(10, lang)}.")
st.write(f"**{T['house']} 2:** {sign_house_theme(2, lang)}.")
st.write(f"**{T['house']} 7:** {sign_house_theme(7, lang)}.")
st.write(f"**{T['house']} 12:** {sign_house_theme(12, lang)}.")

with st.expander(T["career"], expanded=True):
    st.write(T["career_text"])
    st.write(f"Traditional chart theme: {sign_house_theme(10, lang)}; foreign-place theme: {sign_house_theme(12, lang)}.")
with st.expander(T["money"]):
    st.write(T["money_text"])
    st.write(f"Traditional chart theme: {sign_house_theme(2, lang)} and {sign_house_theme(11, lang)}.")
with st.expander(T["love"]):
    st.write(T["love_text"])
    st.write(f"Traditional chart theme: {sign_house_theme(5, lang)} and {sign_house_theme(7, lang)}.")
with st.expander(T["marriage"]):
    st.write(T["marriage_text"])
    st.write(f"Traditional chart theme: {sign_house_theme(7, lang)}.")
with st.expander(T["health"]):
    st.write(T["health_text"])
    st.write("Use this section for reflection on routine and wellbeing only—not for diagnosis or treatment.")

st.header(T["annual"])
st.write(T["annual_intro"])
annual_df = month_transits(2027, lang, asc_sign)
st.dataframe(annual_df, use_container_width=True, hide_index=True)
st.subheader(T["month"])
for item in annual_summary(annual_df, lang):
    st.markdown(item)

st.divider()
st.caption("Astro Life AI • Free starter edition • Calculations use Swiss Ephemeris with Lahiri sidereal zodiac. Interpretations are educational and not professional advice.")
