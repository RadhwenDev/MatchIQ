import html
import pandas as pd
import streamlit as st
from team_utils import TEAM_LOGOS, get_logo, get_initials, safe


def select_match(match_index: int) -> None:
    st.session_state["selected_match_index"] = match_index
    st.session_state["page_transition"] = True   



def format_match_date(value):
    return pd.Timestamp(value).strftime("%d %b %Y")


def reset_page():
    st.session_state["match_page"] = 1

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
        .club-fallback {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: #1e293b;
            color: #94a3b8;
            font-size: 22px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        }
        .club-name {
            color: #F8FAFC;
            font-weight: 700;
            font-size: .95rem;
            margin-top: 10px;
        }
        .club-role {
            color: #64748b;
            font-size: .65rem;
            letter-spacing: 1px;
        }
        .vs {
            color: #64748b;
            font-weight: 700;
            text-align: center;
            padding-top: 28px;
        }
        .empty-state {
            text-align: center;
            color: #94A3B8;
            padding: 40px 0;
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
    
def play_zoom_transition():
    """Zoom the current page in and fade it out."""
    st.markdown(
        """
        <style>
        [data-testid="stMainBlockContainer"],
        .block-container {
            animation: zoomOut 0.7s ease-in forwards;
            transform-origin: center center;
            pointer-events: none;
        }
        @keyframes zoomOut {
            0%   { transform: scale(1);    opacity: 1; filter: blur(0); }
            100% { transform: scale(1.25); opacity: 0; filter: blur(6px); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    inject_selection_css()
    
    

    if matches is None or matches.empty:
        st.error("No match data could be loaded.")
        return

    data = matches.copy()
    if "Playable" in data.columns:
        data = data[data["Playable"]].copy()
    
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
    # SEARCH AND FILTERS
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

        selected_team = st.selectbox(
            "🔎 Search by team",
            options=all_teams,
            index=None,
            placeholder="Type a club name: Barcelona, Real Madrid, Betis...",
            key="match_team_select",
            on_change=reset_page,
        ) or ""

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
                on_change=reset_page,
            )

        with filter_cols[1]:
            selected_season = st.selectbox(
                "Season",
                seasons,
                key="match_filter_season",
                on_change=reset_page,
            )

        filtered = data.copy()

        if selected_team:
            filtered = filtered[
                (filtered["HomeTeam"].astype(str) == selected_team)
                | (filtered["AwayTeam"].astype(str) == selected_team)
            ]

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

   