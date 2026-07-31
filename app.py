import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
import os
import hashlib
import csv
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u

# ============================================================
# CONFIG — edit this section to personalize everything
# ============================================================
CONFIG = {
    "her_name": "Rara",              # TODO: swap for her real name
    "his_name": "Talo",
    "her_city": "Tawau, Sabah",
    "his_city": "Sheikhupura, Punjab",
    "her_tz_offset": 8,              # Malaysia = UTC+8
    "his_tz_offset": 5,              # Pakistan = UTC+5
    "her_lat": 4.2449, "her_lon": 117.8998,   # Tawau, Sabah
    "his_lat": 31.7167, "his_lon": 73.9853,   # Sheikhupura, Punjab
    "relationship_start": "2025-11-13",       # TODO: set to your real start date
    "inside_jokes": [
        "the great sock debate of last winter",
        "that voice note that was 90% laughing",
        "the day the call dropped 6 times in a row",
        "the ongoing argument about who misses who more",
    ],
}

COUPLE_IMG = os.path.join(os.path.dirname(__file__), "assets", "couple.png")
RARA_IMG = os.path.join(os.path.dirname(__file__), "assets", "rara.png")
STARS_CSV = os.path.join(os.path.dirname(__file__), "assets", "stars.csv")

@st.cache_data
def load_star_catalog():
    stars = []
    with open(STARS_CSV) as f:
        for row in csv.DictReader(f):
            stars.append({
                "name": row["name"],
                "ra": float(row["ra_hours"]) * 15.0,  # hours -> degrees
                "dec": float(row["dec_deg"]),
                "mag": float(row["mag"]),
            })
    return stars

# ============================================================
# PAGE SETUP + STYLE
# ============================================================
st.set_page_config(page_title="Miles Apart", page_icon="🧭", layout="centered")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Quicksand:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Quicksand', sans-serif;
}}

.stApp {{
    background: linear-gradient(180deg, #FBEEE0 0%, #F5DCC8 100%);
}}

/* Targeted overrides — fix Streamlit's own widget text colors without
   clobbering our intentional accent colors elsewhere */
section[data-testid="stSidebar"] * {{
    color: #5B4636 !important;
}}
[data-testid="stWidgetLabel"] p {{
    color: #5B4636 !important;
}}
[data-testid="stCaptionContainer"] * {{
    color: #7A6852 !important;
}}
[data-testid="stMarkdownContainer"] p {{
    color: #5B4636;
}}

h1, h2, h3 {{
    font-family: 'Fredoka', sans-serif !important;
    color: #5B4636 !important;
}}

section[data-testid="stSidebar"] {{
    background: #EFE0CC;
    border-right: 2px solid #D9C3A3;
}}

.mile-card {{
    background: #FFF8EE;
    border: 2px solid #D9C3A3;
    border-radius: 18px;
    padding: 1.3rem 1.6rem;
    box-shadow: 0 4px 14px rgba(90, 70, 50, 0.08);
    margin-bottom: 1rem;
    color: #5B4636 !important;
}}
.mile-card, .mile-card p, .mile-card b, .mile-card i {{
    color: #5B4636 !important;
}}

.ticket-header {{
    background: #8CA080;
    color: #FFF8EE !important;
    padding: 0.6rem 1rem;
    border-radius: 12px 12px 0 0;
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.masthead {{
    text-align: center;
    border-bottom: 4px double #5B4636;
    border-top: 4px double #5B4636;
    padding: 0.6rem 0;
    margin-bottom: 0.8rem;
    color: #5B4636 !important;
}}
.masthead p {{
    color: #5B4636 !important;
}}

.masthead h1 {{
    font-size: 2.6rem;
    letter-spacing: 2px;
    margin: 0;
}}

.stButton>button {{
    background: #8CA080;
    color: white;
    border-radius: 999px;
    border: none;
    padding: 0.5rem 1.4rem;
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
}}
.stButton>button:hover {{
    background: #718A66;
    color: white;
}}

.scroll-frame {{
    background: #FFF8EE;
    border: 2px dashed #D9C3A3;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAV
# ============================================================
st.sidebar.image(RARA_IMG, width='stretch')
st.sidebar.markdown(f"### {CONFIG['his_city'].split(',')[0]} ↔ {CONFIG['her_city'].split(',')[0]}")
page = st.sidebar.radio(
    "Wander around",
    ["🏡 Home", "✨ Same Sky", "🗺️ If We Were In The Same City", "📰 The Talo Times", "📮 Complaint Box"],
    label_visibility="collapsed",
)

NAME = CONFIG["her_name"]

# ============================================================
# HOME
# ============================================================
if page == "🏡 Home":
    st.markdown(f"<h1 style='text-align:center;'>for {NAME} 🌷</h1>", unsafe_allow_html=True)
    st.image(COUPLE_IMG, width='stretch')
    st.markdown(f"""
    <div class="mile-card" style="text-align:center;">
    No occasion today. No anniversary, no excuse. Just a small world I built
    because {CONFIG['his_city'].split(',')[0]} and {CONFIG['her_city'].split(',')[0]} are far apart
    and I wanted you to have something that isn't.<br><br>
    Look around — there's a complaint box, a shared sky, an imagined city where
    we're never actually apart, and a newspaper that's only ever about us.
    </div>
    """, unsafe_allow_html=True)

    start = datetime.date.fromisoformat(CONFIG["relationship_start"])
    days = (datetime.date.today() - start).days
    st.markdown(f"""
    <div class="mile-card" style="text-align:center;">
    <div style="font-size:2.2rem; font-family:'Fredoka',sans-serif; color:#8CA080; font-weight:700;">{days:,}</div>
    <div style="color:#5B4636;">one of the best days of my lifee, you are soo amazingg, i love you sooo muchh.</div>
    <div style="font-size:0.85rem; margin-top:0.4rem; color:#7A6852;">
    that's roughly {days*24:,} hours, {days//7:,} weeks, and {days:,} days and i missed you moree than these numbers</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# COMPLAINT BOX
# ============================================================
elif page == "📮 Complaint Box":
    st.markdown("<h2>📮 Official Complaint Box</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="mile-card">
    <b>MILES APART INC.</b> — Customer Relations (Long Distance Division)<br>
    File a complaint about missing {CONFIG['his_name']}. Response guaranteed to be dramatic,
    overly formal, and completely unqualified to fix anything.
    </div>
    """, unsafe_allow_html=True)

    complaint = st.text_area("Describe your complaint:", placeholder="e.g. He hasn't called in 4 whole hours, this is unacceptable")

    TEMPLATES = [
        """Dear {name},

We regret to inform you that the Complaints Department has reviewed your case
(Ticket #{ticket}) and found the accused, one {his_name} of {his_city}, guilty
on all counts. In his defense, he submitted only the phrase "I was thinking
about her the whole time," which the tribunal found emotionally compelling
but legally irrelevant.

As compensation, he has been sentenced to: missing you exactly as much as
you miss him, for the rest of the day, with no possibility of parole.

We apologize for the {his_city}-{her_city} distance. It was not in the
original agreement and management is looking into it.

Sincerely,
The Department of Feelings""",

        """URGENT MEMO — Case #{ticket}

Subject: Alleged failure to be physically present

Findings: {his_name} has been formally charged with being 3,000+ km away
during a moment you needed him closer. He does not deny the charge. He
simply has no defense, no excuse, and no ability to teleport (yet — R&D
is working on it, ETA: as soon as the visa comes through).

Recommended remedy: one (1) extra-long voice note, one (1) embarrassing
admission of how much he actually misses you, and a formal promise that
the distance is temporary and the plan is not.

Filed under: things he'd fix in a heartbeat if he could.""",

        """NOTICE OF APOLOGY — Ref: {ticket}

We acknowledge receipt of your complaint and confirm it has been escalated
to the highest possible authority: {his_name} himself, who read it twice,
felt terrible, and would like the record to show he is, in fact, always
thinking about you, even during the boring hours.

Compensation package: unlimited attention upon return of signal, priority
handling on all future calls, and a written guarantee that {his_city} is
only a placeholder address until it isn't.

Status: RESOLVED WITH LOVE.""",
    ]

    if st.button("Submit Complaint"):
        ticket = f"MA-{random.randint(1000,9999)}"
        template = random.choice(TEMPLATES)
        letter = template.format(
            name=NAME, his_name=CONFIG["his_name"], his_city=CONFIG["his_city"].split(",")[0],
            her_city=CONFIG["her_city"].split(",")[0], ticket=ticket
        )
        st.markdown(f"""<div class="ticket-header">TICKET {ticket} — STATUS: RESOLVED WITH LOVE</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="mile-card" style="white-space:pre-wrap; border-top:none; border-radius:0 0 18px 18px;">{letter}</div>""", unsafe_allow_html=True)

# ============================================================
# SAME SKY (constellation)
# ============================================================
elif page == "✨ Same Sky":
    st.markdown("<h2>✨ Same Sky, Different Distance</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="mile-card">
    Pick a date and a time of night. These are real bright stars, plotted
    with real astronomy (astropy) for exactly what's above the horizon in
    {CONFIG['his_city'].split(',')[0]} and {CONFIG['her_city'].split(',')[0]} at that moment —
    not random dots. Since {CONFIG['her_city'].split(',')[0]} sits so close to the equator,
    it actually gets a bigger slice of sky than {CONFIG['his_city'].split(',')[0]} does —
    stars neither of you can see from up north.
    </div>
    """, unsafe_allow_html=True)

    col_d, col_t = st.columns(2)
    with col_d:
        picked_date = st.date_input("Pick a date", datetime.date.today())
    with col_t:
        picked_time = st.time_input("Pick a time (local to each city)", datetime.time(21, 0))

    def moon_phase(date):
        diff = date - datetime.date(2001, 1, 1)
        days = diff.days
        lunations = 0.20439731 + (days * 0.03386319269)
        phase_index = round((lunations % 1) * 8) % 8
        phases = ["New Moon 🌑", "Waxing Crescent 🌒", "First Quarter 🌓", "Waxing Gibbous 🌔",
                   "Full Moon 🌕", "Waning Gibbous 🌖", "Last Quarter 🌗", "Waning Crescent 🌘"]
        return phases[phase_index]

    def real_sky(lat, lon, tz_offset, date, time_, color):
        # Convert local city time -> UTC for the astronomy calculation
        local_dt = datetime.datetime.combine(date, time_)
        utc_dt = local_dt - datetime.timedelta(hours=tz_offset)
        t = Time(utc_dt)
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=100 * u.m)
        frame = AltAz(obstime=t, location=loc)

        stars = load_star_catalog()
        ras = np.array([s["ra"] for s in stars])
        decs = np.array([s["dec"] for s in stars])
        mags = np.array([s["mag"] for s in stars])
        names = [s["name"] for s in stars]

        coords = SkyCoord(ra=ras * u.deg, dec=decs * u.deg)
        altaz = coords.transform_to(frame)
        alt = altaz.alt.deg
        az = altaz.az.deg

        visible = alt > 0
        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={"projection": "polar"})
        fig.patch.set_alpha(0)
        ax.set_facecolor((0, 0, 0, 0))
        theta = np.radians(az[visible])
        r = 90 - alt[visible]  # zenith at center, horizon at edge
        sizes = (2.0 - mags[visible]).clip(min=0.3) * 25
        ax.scatter(theta, r, s=sizes, color=color, alpha=0.95, edgecolors="none")

        # label the brightest 4 visible stars
        vis_idx = np.where(visible)[0]
        order = vis_idx[np.argsort(mags[vis_idx])][:4]
        for i in order:
            ax.annotate(names[i], (np.radians(az[i]), 90 - alt[i]),
                        color=color, fontsize=7, alpha=0.9, ha="center")

        ax.set_ylim(0, 90)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(alpha=0.15, color=color)
        ax.spines['polar'].set_alpha(0.2)
        return fig, int(visible.sum())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{CONFIG['his_city'].split(',')[0]} sky**")
        fig1, n1 = real_sky(CONFIG["his_lat"], CONFIG["his_lon"], CONFIG["his_tz_offset"],
                             picked_date, picked_time, "#5B4636")
        st.pyplot(fig1, width='stretch')
        st.caption(f"{n1} bright stars above the horizon right now")
    with col2:
        st.markdown(f"**{CONFIG['her_city'].split(',')[0]} sky**")
        fig2, n2 = real_sky(CONFIG["her_lat"], CONFIG["her_lon"], CONFIG["her_tz_offset"],
                             picked_date, picked_time, "#8CA080")
        st.pyplot(fig2, width='stretch')
        st.caption(f"{n2} bright stars above the horizon right now")

    st.markdown(f"""
    <div class="mile-card" style="text-align:center;">
    🌙 That night's real moon phase: <b>{moon_phase(picked_date)}</b> — exactly the same one over both of you.<br>
    🕐 Clocks are {CONFIG['her_tz_offset'] - CONFIG['his_tz_offset']} hours apart:
    {CONFIG['her_city'].split(',')[0]} is ahead of {CONFIG['his_city'].split(',')[0]}.
    </div>
    """, unsafe_allow_html=True)
    st.caption("Star positions use real coordinates for ~40 of the sky's brightest stars — "
               "a simplified but genuine chart, not a full observatory-grade catalog.")

# ============================================================
# WHERE'S TALO RIGHT NOW
# ============================================================
elif page == "🗺️ If We Were In The Same City":
    st.markdown("<h2>🗺️ If We Were In The Same City</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="mile-card">
    Not real yet. But it will be. Pick a place in {CONFIG['his_city'].split(',')[0]}
    and imagine a very ordinary day together there — the kind of ordinary
    that feels extraordinary when you're doing it with the person you miss.
    </div>
    """, unsafe_allow_html=True)

    # Real Sheikhupura-area spots with Wikimedia Commons photographs.
    # The photos below are CC BY-SA licensed; attribution is shown under the image.
    SPOTS = {
        "🏰 Sheikhupura Fort": {
            "story": (
                "Talo insists on giving Rara the full tour even though he only remembers "
                "about half the history. Rara catches every confident mistake. They walk "
                "slowly through the old walls, stop for photos, and argue over which one "
                "looks better. Neither wants to leave first."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Sheikhupura_Fort_White_Haveli.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Sheikhupura_Fort_White_Haveli.jpg",
            "credit": "Photo: Omarjhawarian — Wikimedia Commons, CC BY-SA 3.0",
        },
        "🌿 Hiran Minar": {
            "story": (
                "Golden hour. A long walk beside the water. Talo says the view is the "
                "reason they came, but Rara knows he mostly wanted somewhere quiet enough "
                "to sit beside her without checking the time. They take one photo, then "
                "forget about the camera."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Hiran_Minar%2C_Sheikhupura.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Hiran_Minaar,_Sheikhupura.jpg",
            "credit": "Photo: Taeja — Wikimedia Commons, CC BY-SA 4.0",
        },
        "🌸 Shrine of Waris Shah": {
            "story": (
                "A quieter afternoon in Jandiala Sher Khan. They walk through the garden, "
                "talk about old stories and poetry, and then sit somewhere peaceful. "
                "Rara gets unexpectedly sentimental. Talo pretends not to notice because "
                "he is absolutely going to tease her about it later."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Shrine_of_Waris_Shah.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Shrine_of_Waris_Shah.jpg",
            "credit": "Photo: Nawab Afridi — Wikimedia Commons, CC BY-SA 4.0",
        },
        "🏏 Sheikhupura Stadium": {
            "story": (
                "Talo claims this is going to be a quick stop. It is not. One discussion "
                "about cricket becomes a full debate, followed by snacks, people-watching, "
                "and Rara making fun of how seriously he takes the score. A very normal "
                "day. Exactly the point."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/8/88/%22International_Cricket_Stadium_Sheikhupura-Jun_2017.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:%22International_Cricket_Stadium_Sheikhupura-Jun_2017.jpg",
            "credit": "Photo: Basit Nadeem — Wikimedia Commons, CC BY-SA 4.0",
        },

        "🕌 Badshahi Mosque, Lahore": {
            "story": (
                "They finally get to walk through the same courtyard instead of talking "
                "about it over a phone screen. Rara looks up at the domes. Talo looks at "
                "her first. They take too many photos and still somehow forget the one "
                "photo they both wanted."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Badshahi_Mosque_in_Lahore_panoramic_view.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Badshahi_Mosque_in_Lahore_panoramic_view.jpg",
            "credit": "Photo: Marsmux — Wikimedia Commons, CC BY-SA 4.0",
        },
        "🏯 Lahore Fort": {
            "story": (
                "Talo walks into guide mode immediately. Rara lets him have exactly five "
                "minutes before correcting something. They wander through the fort, stop "
                "for a quiet view, and spend half the afternoon pretending they are not "
                "already tired."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Lahore_Fort%2C_Lahore..jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Lahore_Fort,_Lahore..jpg",
            "credit": "Photo: Kamran Aslam — Wikimedia Commons, CC BY-SA 4.0",
        },
        "🗼 Minar-e-Pakistan": {
            "story": (
                "A late-afternoon walk through the park. They sit somewhere with the "
                "tower in the distance and talk about absolutely nothing important. "
                "Talo insists they need one dramatic couple photo. Rara eventually gives in."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/6/69/Minar-E-Pakistan%2C_Lahore.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Minar-E-Pakistan,_Lahore.jpg",
            "credit": "Photo: NainaR — Wikimedia Commons, CC BY-SA 4.0",
        },
        "🌺 Shalimar Gardens": {
            "story": (
                "They slow down here on purpose. Rara wants to see every fountain and "
                "garden level. Talo keeps saying he is not tired while absolutely looking "
                "for the next place to sit. Eventually they find a quiet corner and stay."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/c/c6/Shalimar_Gardens_%28Lahore%29_1.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Shalimar_Gardens_(Lahore)_1.jpg",
            "credit": "Photo: Guilhem Vellut — Wikimedia Commons, CC BY 2.0",
        },
        "🫖 Rooftop chai at Cuckoo's Den": {
            "story": (
                "This is the tea one. Rooftop, evening air, Badshahi Mosque glowing "
                "right in front of them. No video call. No 'can you hear me?' No frozen "
                "screen. Just two cups of chai, one ridiculous amount of staring at the "
                "mosque, and Rara quietly saying, 'I wish we could do this every week.'"
            ),
            "image": "assets/rooftop_chai.png",
            "source": "https://www.instagram.com/p/DTtB7nxCKDs/",
            "credit": "Photo provided by you from Instagram (@butt_karahi_bbq)",
        },

        "🌳 The park bench": {
            "story": (
                "They sit down for ten minutes and stay for two hours. Talo opens his "
                "phone to show her something and forgets what it was. They just talk. "
                "No big plan. No occasion. Just finally being in the same place."
            ),
            "image": "https://upload.wikimedia.org/wikipedia/commons/5/58/Bagh-e-Jinnah_Lahore_Pakistan.jpg",
            "source": "https://commons.wikimedia.org/wiki/File:Bagh-e-Jinnah_Lahore_Pakistan.jpg",
            "credit": "Photo: Amnagondal — Wikimedia Commons, CC BY-SA 4.0",
        },
    }

    cols = st.columns(2)
    for i, spot in enumerate(SPOTS.keys()):
        with cols[i % 2]:
            if st.button(spot, key=f"spot_{i}", width='stretch'):
                st.session_state["picked_spot"] = spot

    picked = st.session_state.get("picked_spot", list(SPOTS.keys())[0])
    selected = SPOTS[picked]

    st.markdown(f"""
    <div class="mile-card" style="text-align:center; margin-top:1rem;">
    <h3 style="margin-top:0;">{picked}</h3>
    <i>{selected["story"]}</i>
    </div>
    """, unsafe_allow_html=True)

    st.image(selected["image"], width="stretch")
    st.caption(selected["credit"])
    st.markdown(
        f"[View the original photo on Wikimedia Commons]({selected['source']})"
    )

# ============================================================
# THE TALO TIMES
# ============================================================
elif page == "📰 The Talo Times":
    st.markdown("""<div class="masthead"><h1>THE TALO TIMES</h1>
    <p style="margin:0; letter-spacing:1px;">"All the news that's fit to feel"</p></div>""", unsafe_allow_html=True)
    st.caption(datetime.date.today().strftime("%A, %B %d, %Y") + f" · {CONFIG['his_city']} EDITION · FREE (priceless, actually)")

    HEADLINES = [
        ("LOCAL MAN WALKS EXTRA MILE, LITERALLY, TO PROVE LOVE",
         f"Sources confirm {CONFIG['his_name']} of {CONFIG['his_city'].split(',')[0]} continues to close the {CONFIG['her_tz_offset']-CONFIG['his_tz_offset']}-hour time gap nightly, "
         f"at great personal cost to his sleep schedule. Experts call it 'unnecessary.' {CONFIG['his_name']} calls it 'Tuesday.'"),
        (f"BREAKING: {NAME.upper()} STILL THE MAIN ATTRACTION IN {CONFIG['his_city'].split(',')[0].upper()}",
         f"Despite being {CONFIG['her_city'].split(',')[0]} residents' business, {NAME}'s daily calls remain the most anticipated event on the {CONFIG['his_city'].split(',')[0]} calendar, beating even lunch."),
        ("MAN CLAIMS DISTANCE 'JUST A NUMBER,' PROVIDES NO MATH TO BACK THIS UP",
         f"Local sources confirm {CONFIG['his_name']} has never once done the actual kilometre calculation, on the grounds that it would 'ruin the vibe.'"),
        ("SHY WOMAN IN TAWAU GOES QUIET MID-CALL, INVESTIGATION FINDS NOTHING WRONG AT ALL",
         f"After brief panic, sources close to {CONFIG['his_name']} confirm the silence was, in fact, extremely cute and not a problem whatsoever."),
    ]

    main = random.choice(HEADLINES)
    st.markdown(f"""
    <div class="mile-card">
    <h3>{main[0]}</h3>
    <p>{main[1]}</p>
    </div>
    """, unsafe_allow_html=True)

    others = [h for h in HEADLINES if h != main]
    random.shuffle(others)
    cols = st.columns(2)
    for c, h in zip(cols, others[:2]):
        with c:
            st.markdown(f"""<div class="mile-card"><b>{h[0]}</b><p style="font-size:0.85rem;">{h[1]}</p></div>""", unsafe_allow_html=True)

    st.caption("Refresh the page for a new front page. Editorial standards: none. Editorial love: unlimited.")

    if CONFIG["inside_jokes"]:
        st.markdown(f"""<div class="mile-card"><b>Also in this issue:</b> {random.choice(CONFIG['inside_jokes'])}</div>""", unsafe_allow_html=True)

