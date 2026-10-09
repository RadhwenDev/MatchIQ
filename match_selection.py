import html
import pandas as pd
import streamlit as st


def select_match(match_index: int) -> None:
    st.session_state["selected_match_index"] = match_index
    st.session_state["match_selection_confirmed"] = True
    st.session_state["analysis_step"] = 2

# =========================================================
# MATCHIQ — MATCH CENTER
# =========================================================

TEAM_LOGOS = {
    # Clubs present across multiple seasons
    "Barcelona": "https://crests.football-data.org/81.png",
    "Real Madrid": "https://crests.football-data.org/86.png",
    "Ath Madrid": "https://crests.football-data.org/78.png",
    "Atletico Madrid": "https://crests.football-data.org/78.png",
    "Ath Bilbao": "https://crests.football-data.org/77.png",
    "Athletic Bilbao": "https://crests.football-data.org/77.png",
    "Betis": "https://crests.football-data.org/90.png",
    "Real Betis": "https://crests.football-data.org/90.png",
    "Sociedad": "https://crests.football-data.org/92.png",
    "Real Sociedad": "https://crests.football-data.org/92.png",
    "Sevilla": "https://crests.football-data.org/559.png",
    "Valencia": "https://crests.football-data.org/95.png",
    "Villarreal": "https://crests.football-data.org/94.png",
    "Celta": "https://crests.football-data.org/558.png",
    "Getafe": "https://crests.football-data.org/82.png",
    "Osasuna": "https://crests.football-data.org/79.png",
    "Mallorca": "https://crests.football-data.org/89.png",
    "Vallecano": "https://crests.football-data.org/87.png",
    "Rayo Vallecano": "https://crests.football-data.org/87.png",

    # Clubs appearing in some of the four seasons
    "Alaves": "https://crests.football-data.org/263.png",
    "Almería": "https://crests.football-data.org/267.png",
    "Almeria": "https://crests.football-data.org/267.png",
    "Cadiz": "https://crests.football-data.org/264.png",
    "Cádiz": "https://crests.football-data.org/264.png",
    "Elche": "https://crests.football-data.org/285.png",
    "Espanol": "https://crests.football-data.org/80.png",
    "Espanyol": "https://crests.football-data.org/80.png",
    "Girona": "https://crests.football-data.org/298.png",
    "Granada": "https://crests.football-data.org/83.png",
    "Las Palmas": "https://crests.football-data.org/275.png",
    "Leganes": "https://crests.football-data.org/745.png",
    "Leganés": "https://crests.football-data.org/745.png",
    "Levante": "https://crests.football-data.org/88.png",
    "Valladolid": "https://crests.football-data.org/250.png",
    "Oviedo": "https://www.footylogos.com/logos/real-oviedo",
}

def get_logo(team):
    return TEAM_LOGOS.get(str(team), "")


def get_initials(team):
    words = str(team).strip().split()

    if not words:
        return "FC"

    if len(words) == 1:
        return words[0][:2].upper()

    return (words[0][0] + words[-1][0]).upper()

def format_match_date(value):
    return pd.Timestamp(value).strftime("%d %b %Y")


def inject_selection_css():
    st.markdown(
        """
        <style>
        .hero-title {
            font-size: 52px;
            line-height: 1.08;
            font-weight: 800;
            max-width: 720px;
            margin-bottom: 22px;
        }
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
        .hero-desc {
            color: #AAB4C0;
            font-size: 18px;
            line-height: 1.7;
            max-width: 650px;
            margin-bottom: 22px;
        }
        .hero-tag {
            display: inline-block;
            color: #64ae92;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 18px;
        }
        .hero-check {
            color: #FFFFFF;
            font-size: 15px;
            font-weight: 600;
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
        .clock-icon {
            font-size: 12px;
            opacity: 0.8;
        }
        .preview-text-block {
            margin-bottom: 8px;
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
            color: #94a3b8;
            font-size: 14px;
            font-weight: 400;
            letter-spacing: 0.2px;
        }
                .stat-card {
            background: #121C27;
            border: 1px solid #263545;
            border-radius: 15px;
            padding: 18px;
        }

        .stat-label {
            color: #94A3B8;
            font-size: .69rem;
            letter-spacing: 1px;
            font-weight: 750;
        }

        .stat-value {
            color: #F8FAFC;
            font-size: 1.65rem;
            font-weight: 850;
            margin-top: 7px;
        }
        .section-title {
            color: #F8FAFC;
            font-size: 1.3rem;
            font-weight: 800;
            margin-top: 12px;
        }

        .section-subtitle {
            color: #94A3B8;
            font-size: .88rem;
            margin-bottom: 18px;
        }

                .match-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 22px;
        }

        .competition-label {
            color: #94A3B8;
            font-size: .72rem;
            font-weight: 750;
            letter-spacing: .8px;
        }
        
        .date-label {
            color: #CBD5E1;
            background: #1D2C3B;
            padding: 6px 9px;
            border-radius: 8px;
            font-size: .72rem;
        }

        .club {
            text-align: center;
            min-width: 0;
        }

        .club-logo {
            width: 72px;
            height: 72px;
            object-fit: contain;
            display: block;
            margin: 0 auto;
        }

        .custom-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0px;
            margin-top: 60px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .footer-left {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 400;
        }

        .footer-left .brand-name {
            color: #ffffff;
            font-weight: 500;
        }

        .footer-right {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 400;
        }
        
        .features-grid {
            display: flex;
            justify-content: space-between;
            gap: 30px;
            margin-top: 50px;
            margin-bottom: 40px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .feature-item {
            flex: 1;
        }

        .feature-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }

        .feature-icon {
            color: #34d399; 
            font-size: 20px;
        }

        .feature-title {
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
        }

        .feature-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.5;
        }

        .banner-quote {
            text-align: center;
            color: #34d399; 
            font-size: 18px;
            font-weight: 500;
            margin-top: 40px;
            margin-bottom: 30px;
            letter-spacing: 0.3px;
        }
        
        </style>
        """,
        unsafe_allow_html=True
        )

def safe(value):
    """Escape text before inserting it into HTML."""
    return html.escape(str(value), quote=True)


def render_team(team, role):
    logo = get_logo(team)
    team_name = safe(team)

    if logo:
        image_html = f"""<img class="club-logo" src="{safe(logo)}" alt="{team_name}" onerror=" this.style.display='none'; this.nextElementSibling.style.display='flex';"> <div class="club-fallback" style="display:none"> {safe(get_initials(team))}</div>"""
    else:
        image_html = f"""
            <div class="club-fallback">
                {safe(get_initials(team))}
            </div>
        """

    st.markdown(
        f"""<div class="club">{image_html}<div class="club-name">{team_name}</div><div class="club-role">{role}</div></div>""",
        unsafe_allow_html=True
    )


def render_match_selection(matches):
    """
    Display searchable match cards.
    Return the original dataframe index when the user clicks Analyse Match.
    """


def render_match_selection(matches):
    inject_selection_css()
    
    

    if matches is None or matches.empty:
        st.error("No match data could be loaded.")
        return

    data = matches.copy()
    
    required = ["Date", "HomeTeam", "AwayTeam"]
    missing = [col for col in required if col not in data.columns]

    if missing:
        st.error("Missing columns: " + ", ".join(missing))
        return None

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce",
        dayfirst=True,
    )


    if "League" not in data.columns:
        data["League"] = "La Liga"

    data = data.dropna(
        subset=["Date", "HomeTeam", "AwayTeam"]
    ).copy()

    if data.empty:
        st.error("No valid matches are available.")
        return
    
    if "League" not in data.columns:
        data["League"] = "La Liga"

    if "Season" not in data.columns:
        data["Season"] = "All seasons"

    data["League"] = data["League"].fillna("Unknown")
    data["Season"] = data["Season"].fillna("Unknown")
    
    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------
    
    col1, col2 = st.columns([1.3, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="hero-tag">THE FOOTBALL ANALYST'S TRAINING GROUND</div>
        <div class="hero-title">Can you think like a football analyst?</div>
        <div class="hero-desc">
            Study the information available before kickoff. Make your prediction. 
            Then discover what really happened.
        </div>
        <div class="hero-check">
            <span>🛡️</span> Real analysis. Historical matches. No betting.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(
        """
        <div class="hero-preview">
            <div class="preview-tag">
                <span class="clock-icon">🕒</span> BEFORE KICKOFF
            </div>
            <div class="preview-text-block">
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
    
    st.write("\n")
    
    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    stats = [
        ("MATCHES", f"{len(data):,}"),
        (
            "TEAMS",
            f"{len(set(data['HomeTeam'].astype(str)) | set(data['AwayTeam'].astype(str))):,}",
        ),
        ("SEASONS", f"{data['Season'].nunique():,}"),
        ("COMPETITIONS", f"{data['League'].nunique():,}"),
    ]

    stat_cols = st.columns(4)

    for col, (label, value) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    # -----------------------------------------------------
    # SEARCH AND FILTERS — LIVE CLUB SUGGESTIONS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Search the match library</div>'
        '<div class="section-subtitle">'
        'Type a club name to see suggestions instantly.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        all_teams = sorted(
            set(data["HomeTeam"].dropna().astype(str))
            | set(data["AwayTeam"].dropna().astype(str))
        )
        
        search_text = st.text_input(
            "🔎 Search by team",
            placeholder="Try Barcelona, Real Madrid, Betis...",
            key="match_search",
        ).strip()

        # Suggestions update automatically on every rerun while typing.
        suggestions = []

        if search_text:
            suggestions = [
                team for team in all_teams
                if search_text.casefold() in team.casefold()
            ][:8]

        if suggestions:
            st.caption("CLUB SUGGESTIONS")

            suggestion_cols = st.columns(min(4, len(suggestions)))

            for i, team in enumerate(suggestions):
                with suggestion_cols[i % len(suggestion_cols)]:
                    if st.button(
                        f"⚽ {team}",
                        key=f"suggest_team_{i}_{team}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_search_team"] = team
                        st.rerun()

        elif search_text:
            st.caption("No clubs found. Try another spelling.")

        selected_team = st.session_state.get("selected_search_team", "")

        if selected_team:
            st.info(f"Selected club: {selected_team}")

            if st.button("Clear selected club", key="clear_selected_club"):
                st.session_state["selected_search_team"] = ""
                st.rerun()

        filter_cols = st.columns(2)

        competitions = ["All competitions"] + sorted(
            data["League"].astype(str).unique().tolist()
        )

        seasons = ["All seasons"] + sorted(
            data["Season"].astype(str).unique().tolist(),
            reverse=True,
        )

        with filter_cols[0]:
            selected_league = st.selectbox(
                "Competition",
                competitions,
                key="match_filter_league",
            )

        with filter_cols[1]:
            selected_season = st.selectbox(
                "Season",
                seasons,
                key="match_filter_season",
            )

        filtered = data.copy()

        # A selected club takes priority over the text being typed.
        active_search = selected_team if selected_team else search_text

        if active_search:
            query = active_search.casefold()

            home_matches = filtered["HomeTeam"].astype(str).str.casefold().str.contains(
                query, regex=False
            )
            away_matches = filtered["AwayTeam"].astype(str).str.casefold().str.contains(
                query, regex=False
            )

            filtered = filtered[home_matches | away_matches]

        if selected_league != "All competitions":
            filtered = filtered[
                filtered["League"].astype(str) == selected_league
            ]

        if selected_season != "All seasons":
            filtered = filtered[
                filtered["Season"].astype(str) == selected_season
            ]

        st.caption(f"{len(filtered):,} matching fixture(s)")

    # -----------------------------------------------------
    # MATCH RESULTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Available fixtures</div>'
        '<div class="section-subtitle">'
        'Choose a match and click Analyse Match to continue.'
        '</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.markdown(
            """
            <div class="empty-state">
                <h3>No matches found</h3>
                Try another team name, competition or season.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return None

    # Show latest dates first; the actual result is not rendered here.
    filtered = filtered.sort_values("Date", ascending=False)

    # Pagination: avoid rendering hundreds of cards at once.
    page_size = 12
    total_pages = max(1, (len(filtered) + page_size - 1) // page_size)

    if st.session_state.get("match_page", 1) > total_pages:
        st.session_state["match_page"] = 1

    page = st.session_state.get("match_page", 1)

    if total_pages > 1:
        page_cols = st.columns([1, 2, 1])

        with page_cols[0]:
            if st.button(
                "← Previous",
                disabled=(page <= 1),
                key="match_prev_page",
            ):
                st.session_state["match_page"] = page - 1
                st.rerun()

        with page_cols[1]:
            st.markdown(
                f"<div style='text-align:center;padding-top:8px;color:#94A3B8'>"
                f"Page {page} of {total_pages}</div>",
                unsafe_allow_html=True,
            )

        with page_cols[2]:
            if st.button(
                "Next →",
                disabled=(page >= total_pages),
                key="match_next_page",
            ):
                st.session_state["match_page"] = page + 1
                st.rerun()

    start = (page - 1) * page_size
    page_matches = filtered.iloc[start:start + page_size]

    # Two cards per row on desktop.
    rows = list(page_matches.iterrows())

    for i in range(0, len(rows), 2):
        card_cols = st.columns(2)

        for j in range(2):
            if i + j >= len(rows):
                break

            original_index, match = rows[i + j]

            home = str(match["HomeTeam"])
            away = str(match["AwayTeam"])
            league = str(match["League"])
            season = str(match["Season"])
            date_label = format_match_date(match["Date"])

            with card_cols[j]:
                with st.container(border=True):

                    st.markdown(
                        f"""
                        <div class="match-card-top">
                            <div class="competition-label">
                                {safe(league)} · {safe(season)}
                            </div>
                            <div class="date-label">
                                {safe(date_label)}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    home_col, vs_col, away_col = st.columns([4, 1, 4])

                    with home_col:
                        render_team(home, "HOME")

                    with vs_col:
                        st.markdown(
                            '<div class="vs">VS</div>',
                            unsafe_allow_html=True,
                        )

                    with away_col:
                        render_team(away, "AWAY")

                    st.write("")

                    st.button(
                        "Analyse Match →",
                        key=f"analyse_match_{original_index}",
                        use_container_width=True,
                        on_click=select_match,
                        args=(int(original_index),),
)


    st.markdown(
        """
        <div class="features-grid">
            <div class="feature-item">
                <div class="feature-header">
                    <span class="feature-icon">🔍</span>
                    <span class="feature-title">Study the evidence</span>
                </div>
                <div class="feature-desc">
                    Compare form, chances, venue performance and context &mdash; before the result influences you.
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-header">
                    <span class="feature-icon">🔒</span>
                    <span class="feature-title">Commit to a decision</span>
                </div>
                <div class="feature-desc">
                    Choose an outcome and an optional exact score. Your prediction is locked before the reveal.
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-header">
                    <span class="feature-icon">💡</span>
                    <span class="feature-title">Learn, not just guess</span>
                </div>
                <div class="feature-desc">
                    Review what you noticed, what you missed and how to build a stronger analytical process.
                </div>
            </div>
        </div>
        <div class="banner-quote">
            Before the whistle, you have information. Your job is to turn information into a decision.
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="custom-footer">
            <div class="footer-left">
                <span class="brand-name">MatchIQ</span> &nbsp;/&nbsp; An independent football learning lab
            </div>
            <div class="footer-right">
                Study evidence. Make a decision. Learn from the outcome.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Keep a previous selection available while browsing.
    return st.session_state.get("selected_match_index")

   