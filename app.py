import streamlit as st
from pathlib import Path

from data_loader import load_all_matches
from context import get_pre_match_context


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MatchIQ",
    page_icon="⚽",
    layout="wide"
)

# =========================================================
# LOAD CSS
# =========================================================

css = Path("style.css").read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background-color: #0C131B;
        color: #FFFFFF;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* =========================
       TEXT
       ========================= */

    h1, h2, h3, h4, p, label {
        color: #FFFFFF !important;
    }

    .muted {
        color: #AAB4C0;
    }

    /* =========================
       HERO
       ========================= */

    .hero {
        padding: 50px 20px 55px 20px;
    }

    .hero-tag {
        display: inline-block;
        color: #AAB4C0;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.08;
        font-weight: 800;
        max-width: 720px;
        margin-bottom: 22px;
    }

    .hero-description {
        color: #AAB4C0;
        font-size: 18px;
        line-height: 1.7;
        max-width: 650px;
        margin-bottom: 22px;
    }

    .hero-check {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 600;
    }

    /* =========================
       HERO PREVIEW
       ========================= */

    .hero-preview {
        background:
            linear-gradient(
                rgba(12, 19, 27, 0.45),
                rgba(12, 19, 27, 0.80)
            ),
            url("https://images.pexels.com/photos/399187/pexels-photo-399187.jpeg")
            center / cover no-repeat;

        min-height: 360px;
        border-radius: 20px;
        padding: 28px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .preview-tag {
        align-self: flex-start;
        background: rgba(22, 30, 42, 0.65);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: #94a3b8;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.8px;
        padding: 6px 14px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        gap: 6px;
        text-transform: uppercase;
    }

    .preview-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 600;
        letter-spacing: -0.3px;
        margin-bottom: 6px;
        line-height: 1.2;
    }

    .preview-subtitle {
        color: #D0D7DE;
        font-size: 16px;
    }

    /* =========================
       CONTAINER
       ========================= */

    .match-container {
        background-color: #121D28;
        border: 1px solid rgba(255,255,255,0.85);
        border-radius: 18px;
        padding: 30px;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    .section-number {
        color: #AAB4C0;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 25px;
    }

    /* =========================
       TEAM CARDS
       ========================= */

    .team-card {
        background-color: #0C131B;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 22px;
        text-align: center;
    }

    .team-name {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .stat-line {
        color: #AAB4C0;
        margin: 7px 0;
        font-size: 14px;
    }

    .stat-value {
        color: #FFFFFF;
        font-weight: 700;
    }

    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 46px;
        font-weight: 700;
    }

    /* =========================
       DATAFRAME
       ========================= */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: rgba(255,255,255,0.10);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

matches = load_all_matches()

matches["League"] = "La Liga"


# =========================================================
# HERO
# =========================================================

hero_col1, hero_col2 = st.columns(
    [1.05, 0.95],
    gap="large"
)

with hero_col1:

    st.markdown(
        """
        <div class="hero">
            <div class="hero-tag">
                THE FOOTBALL ANALYST'S TRAINING GROUND
            </div>
            <div class="hero-title">
                Can you think like a football analyst?
            </div>
            <div class="hero-description">
                Study the information available before kickoff.
                Make your prediction. Then discover what really happened.
            </div>
            <div class="hero-check">
                ✓ &nbsp; Real analysis. Historical matches. No betting.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with hero_col2:

    st.markdown(
        """
        <div class="hero-preview">
            <div class="preview-tag">
                ◷ &nbsp; BEFORE KICKOFF
            </div>
            <div>
                <div class="preview-title">
                    The result can wait.
                </div>
                <div class="preview-subtitle">
                    Your reasoning comes first.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 1. SELECT A MATCH
# =========================================================

st.markdown(
    """
    <div class="match-container">
        <div class="section-number">01</div>
        <div class="section-title">Select a Match</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MATCH SELECTORS
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)


# -------------------------
# League
# -------------------------

with col1:

    leagues = sorted(
        matches["League"].dropna().unique()
    )

    selected_league = st.selectbox(
        "League",
        leagues
    )


filtered = matches[
    matches["League"] == selected_league
]


# -------------------------
# Season
# -------------------------

with col2:

    seasons = sorted(
        filtered["Season"].dropna().unique(),
        reverse=True
    )

    selected_season = st.selectbox(
        "Season",
        seasons
    )


filtered = filtered[
    filtered["Season"] == selected_season
]


# -------------------------
# Date
# -------------------------

with col3:

    dates = sorted(
        filtered["Date"].dropna().unique()
    )

    selected_date = st.selectbox(
        "Date",
        dates,
        format_func=lambda x: x.strftime("%d/%m/%Y")
    )


filtered = filtered[
    filtered["Date"] == selected_date
]


# -------------------------
# Home Team
# -------------------------

with col4:

    home_teams = sorted(
        filtered["HomeTeam"].unique()
    )

    selected_home = st.selectbox(
        "Home Team",
        home_teams
    )


filtered = filtered[
    filtered["HomeTeam"] == selected_home
]


# -------------------------
# Away Team
# -------------------------

with col5:

    away_teams = sorted(
        filtered["AwayTeam"].unique()
    )

    selected_away = st.selectbox(
        "Away Team",
        away_teams
    )


# =========================================================
# GET SELECTED MATCH
# =========================================================

selected_match = filtered[
    filtered["AwayTeam"] == selected_away
]


selected_index = selected_match.index[0]


context = get_pre_match_context(
    matches,
    selected_index
)


match = context["match"]

home = context["home"]
away = context["away"]


# =========================================================
# 2. PRE-MATCH ANALYSIS
# =========================================================

st.markdown(
    """
    <div class="match-container">
        <div class="section-number">02</div>
        <div class="section-title">Pre-Match Analysis</div>
    """,
    unsafe_allow_html=True
)


match_col1, match_col2, match_col3 = st.columns(
    [2, 1, 2]
)


with match_col1:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-name">
                {home["team"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with match_col2:

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            height:100%;
            font-size:28px;
            font-weight:800;
        ">
            VS
        </div>
        """,
        unsafe_allow_html=True
    )


with match_col3:

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-name">
                {away["team"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.caption(
    f"Match date: {match['Date'].strftime('%d %B %Y')}"
)


# =========================================================
# RECENT FORM
# =========================================================

st.subheader("Recent Form")

form_col1, form_col2 = st.columns(2)


with form_col1:

    stats = home["stats"]

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-name">
                {home["team"]}
            </div>
            <div class="stat-line">
                Last 5:
                <span class="stat-value">
                    {stats["wins"]}W
                    {stats["draws"]}D
                    {stats["losses"]}L
                </span>
            </div>
            <div class="stat-line">
                Points:
                <span class="stat-value">
                    {stats["points"]} / 15
                </span>
            </div>
            <div class="stat-line">
                Goals scored:
                <span class="stat-value">
                    {stats["avg_goals_for"]} / game
                </span>
            </div>
            <div class="stat-line">
                Goals conceded:
                <span class="stat-value">
                    {stats["avg_goals_against"]} / game
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with form_col2:

    stats = away["stats"]

    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-name">
                {away["team"]}
            </div>
            <div class="stat-line">
                Last 5:
                <span class="stat-value">
                    {stats["wins"]}W
                    {stats["draws"]}D
                    {stats["losses"]}L
                </span>
            </div>
            <div class="stat-line">
                Points:
                <span class="stat-value">
                    {stats["points"]} / 15
                </span>
            </div>
            <div class="stat-line">
                Goals scored:
                <span class="stat-value">
                    {stats["avg_goals_for"]} / game
                </span>
            </div>
            <div class="stat-line">
                Goals conceded:
                <span class="stat-value">
                    {stats["avg_goals_against"]} / game
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# H2H
# =========================================================

st.subheader("Head-to-Head")

h2h = context["h2h"]

if h2h.empty:

    st.info("No previous meetings available.")

else:

    display_h2h = h2h[
        [
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "FTR"
        ]
    ].copy()

    display_h2h["Date"] = display_h2h[
        "Date"
    ].dt.strftime("%d/%m/%Y")

    display_h2h.columns = [
        "Date",
        "Home",
        "Away",
        "Home Goals",
        "Away Goals",
        "Result"
    ]

    st.dataframe(
        display_h2h,
        use_container_width=True,
        hide_index=True
    )


st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 3. YOUR PREDICTION
# =========================================================

st.markdown(
    """
    <div class="match-container">
        <div class="section-number">03</div>
        <div class="section-title">
            Your Prediction
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


prediction = st.radio(
    "What do you think will happen?",
    [
        f"{home['team']} Win",
        "Draw",
        f"{away['team']} Win"
    ],
    horizontal=True
)


if st.button(
    "🔒 Lock Prediction",
    use_container_width=True
):

    st.session_state["prediction"] = prediction
    st.session_state["locked"] = True


if st.session_state.get("locked", False):

    st.success(
        f"Prediction locked: "
        f"**{st.session_state['prediction']}**"
    )

    st.info(
        "Your prediction is locked. "
        "The actual result is hidden until you reveal it."
    )

    if st.button(
        "🎯 Reveal Result",
        use_container_width=True
    ):

        st.session_state["reveal"] = True


st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 4. RESULT
# =========================================================

if st.session_state.get("reveal", False):

    st.markdown(
        """
        <div class="match-container">

            <div class="section-number">04</div>

            <div class="section-title">
                Result
            </div>

        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:32px;
            font-weight:800;
            margin:30px 0;
        ">
            {match['HomeTeam']}
            &nbsp;
            {int(match['FTHG'])}
            -
            {int(match['FTAG'])}
            &nbsp;
            {match['AwayTeam']}
        </div>
        """,
        unsafe_allow_html=True
    )


    actual_result = match["FTR"]


    if actual_result == "H":

        result_text = f"{home['team']} Win"

    elif actual_result == "A":

        result_text = f"{away['team']} Win"

    else:

        result_text = "Draw"


    st.write(
        f"**Actual result:** {result_text}"
    )


    user_prediction = st.session_state["prediction"]


    if user_prediction == result_text:

        st.success(
            "✅ Correct prediction!"
        )

    else:

        st.error(
            f"❌ Incorrect prediction. "
            f"You predicted: {user_prediction}"
        )


    st.markdown("</div>", unsafe_allow_html=True)