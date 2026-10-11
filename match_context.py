import html

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from team_utils import team_logo_html

# =========================================================
# CSS
# =========================================================

def inject_context_css():
    st.markdown(
        """
        <style>
        .context-card {
            background: #111d32;
            border: 1px solid #263650;
            padding: 18px;
            border-radius: 14px;
            min-height: 95px;
        }
        .context-label {
            color: #94a3b8;
            font-size: 12px;
            margin-bottom: 8px;
        }
        .context-value {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 750;
            overflow-wrap: anywhere;
        }
        .form-card {
            background: #111d32;
            border: 1px solid #263650;
            padding: 18px;
            border-radius: 16px;
            margin-bottom: 10px;
        }
        .team-block-logo {
            flex-direction: row;
            align-items: center;
            gap: 14px;
        }
        .club-fallback {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #1e293b;
            color: #94a3b8;
            font-size: 20px;
            font-weight: 700;
            align-items: center;
            justify-content: center;
            display: flex;
        }
        .club-logo {
            width: 64px;
            height: 64px;
            object-fit: contain;
            display: block;
        }
        .form-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .form-team-name {
            color: #f8fafc;
            font-size: 19px;
            font-weight: 750;
        }
        .form-label {
            color: #94a3b8;
            font-size: 10px;
            letter-spacing: 1px;
        }
        .form-results {
            display: flex;
            gap: 7px;
            margin: 18px 0;
        }
        .form-badge {
            width: 30px;
            height: 30px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 800;
        }
        .form-w { background: #17382f; color: #6fd3a8; }
        .form-d { background: #3b321b; color: #f5cf72; }
        .form-l { background: #40242b; color: #f5a0aa; }
        .form-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }
        .form-stat {
            background: #0d1728;
            border-radius: 10px;
            padding: 12px 8px;
            text-align: center;
        }
        .form-stat-value {
            color: #f8fafc;
            font-size: 22px;
            font-weight: 750;
        }
        .form-stat-label {
            color: #94a3b8;
            font-size: 10px;
            margin-top: 4px;
        }
        .form-card-note {
            color: #94a3b8;
            font-size: 11px;
            margin-top: 15px;
        }
         .stApp {
            background-color: #0b0f17;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .match-header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        @media (max-width: 700px) {
            .club-logo, .club-fallback { width: 44px; height: 44px; }
            .team-title { font-size: 24px; }
        }

        .breadcrumb {
            color: #94a3b8;
            font-size: 13px;
        }

        .header-badges {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .badge-pill {
            background: #1e293b;
            color: #94a3b8;
            font-size: 12px;
            padding: 5px 12px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .badge-pill-green {
            background: rgba(16, 185, 129, 0.1);
            color: #34d399;
            font-size: 12px;
            padding: 5px 12px;
            border-radius: 20px;
            border: 1px solid rgba(52, 211, 153, 0.2);
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .teams-section {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 30px;
        }

        .teams-display {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .team-text {
            display: flex;
            flex-direction: column;
        }
        .team-block {
            display: flex;
            flex-direction: column;
        }

        .team-label {
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
        }

        .team-title {
            color: #ffffff;
            font-size: 38px;
            font-weight: 700;
            line-height: 1;
        }

        .vs-text {
            color: #64748b;
            font-size: 14px;
            font-weight: 600;
            margin: 0 10px;
            align-self: center;
        }

        .sub-notice {
            color: #94a3b8;
            font-size: 12px;
            text-align: right;
            max-width: 320px;
            line-height: 1.4;
        }

        .section-title {
            font-size: 11px;
            color: #34d399;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .alert-banner {
            background-color: #0d281e;
            border: 1px solid #144734;
            border-radius: 8px;
            padding: 14px 18px;
            color: #94a3b8;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 30px;
        }

        .team-card {
            background-color: #111822;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 24px;
            color: #f8fafc;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .card-team-name {
            font-size: 22px;
            font-weight: 700;
            margin: 0;
            color: #ffffff;
        }

        .recent-form-title {
            font-size: 11px;
            color: #64748b;
            letter-spacing: 0.8px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .card-body {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .form-badges {
            display: flex;
            gap: 8px;
        }

        .badge {
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
        }

        .stats-container {
            display: flex;
            gap: 28px;
            text-align: center;
        }

        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            line-height: 1;
        }

        .stat-label {
            font-size: 10px;
            color: #64748b;
            letter-spacing: 0.5px;
            margin-top: 6px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .card-footer {
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #1e293b;
            padding-top: 14px;
        }
        .form-card {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 24px;
            color: #f8fafc;
        }
        .form-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .form-team-name {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
        }
        .form-label {
            color: #64748b;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .form-card-body {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .form-results {
            display: flex;
            gap: 8px;
            margin: 0;
        }
        .form-badge {
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 600;
        }
        .form-w { background: #064e3b; color: #34d399; }
        .form-d { background: #1e293b; color: #94a3b8; }
        .badge-l { background-color: #35272a; color: #d5a4a1; }

        .form-stats {
            display: flex;
            gap: 28px;
            text-align: center;
        }
        .form-stat {
            background: transparent;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-stat-value {
            color: #ffffff;
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
        }
        .form-stat-label {
            color: #64748b;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-top: 6px;
        }
        .form-card-note {
            color: #64748b;
            font-size: 12px;
            border-top: 1px solid #1e293b;
            padding-top: 14px;
            margin-top: 0;
        }
        [data-testid="stMainBlockContainer"],
        .block-container {
            animation: pageEnter 0.6s ease-out;
        }
        @keyframes pageEnter {
            from { opacity: 0; transform: scale(0.94); }
            to   { opacity: 1; transform: scale(1); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HELPERS
# =========================================================
def scroll_to_top():
    """Reset the scroll position to the top of the page."""
    components.html(
        """
        <script>
        const doc = window.parent.document;

        function goTop() {
            const targets = [
                doc.querySelector('[data-testid="stMain"]'),
                doc.querySelector('section.main'),
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.documentElement,
                doc.body,
            ];
            targets.forEach(el => {
                if (el) el.scrollTop = 0;
            });
            window.parent.scrollTo(0, 0);
        }

        goTop();
        setTimeout(goTop, 50);
        setTimeout(goTop, 250);
        </script>
        """,
        height=0,
    )
def safe(value):
    return html.escape(str(value))


def render_metric(label, value):
    st.markdown(
        f"""
        <div class="context-card">
            <div class="context-label">{safe(label)}</div>
            <div class="context-value">{safe(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def prepare_history(matches, target):
    """
    Only use matches played strictly before the selected fixture date.
    All matches on the selected date are excluded to prevent leakage.
    """
    data = matches.copy()

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce", dayfirst=True
    )

    target_date = pd.to_datetime(
        target.get("Date"), errors="coerce", dayfirst=True
    )

    if pd.isna(target_date):
        return data.iloc[0:0].copy()

    for column in ["HomeTeam", "AwayTeam", "FTHG", "FTAG"]:
        if column not in data.columns:
            data[column] = pd.NA

    data["FTHG"] = pd.to_numeric(data["FTHG"], errors="coerce")
    data["FTAG"] = pd.to_numeric(data["FTAG"], errors="coerce")

    history = data[
        data["Date"].notna()
        & (data["Date"].dt.normalize() < target_date.normalize())
    ].copy()

    return history.dropna(subset=["FTHG", "FTAG"])


def get_team_history(history, team):
    home = history[history["HomeTeam"] == team].copy()
    away = history[history["AwayTeam"] == team].copy()

    home["GF"] = home["FTHG"]
    home["GA"] = home["FTAG"]

    away["GF"] = away["FTAG"]
    away["GA"] = away["FTHG"]

    team_history = pd.concat([home, away], ignore_index=True)

    if team_history.empty:
        return team_history

    team_history["Points"] = (
        (team_history["GF"] > team_history["GA"]).astype(int) * 3
        + (team_history["GF"] == team_history["GA"]).astype(int)
    )

    team_history["Result"] = "D"
    team_history.loc[team_history["GF"] > team_history["GA"], "Result"] = "W"
    team_history.loc[team_history["GF"] < team_history["GA"], "Result"] = "L"

    sort_columns = ["Date"]
    ascending = [False]

    if "Time" in team_history.columns:
        sort_columns.append("Time")
        ascending.append(False)

    return team_history.sort_values(
        sort_columns,
        ascending=ascending,
        na_position="last",
    )


def render_form_card(team, team_history):
    recent = team_history.head(5).copy()

    if recent.empty:
        st.markdown(f"### {safe(team)}")
        st.info("No previous matches found for this team.")
        return

    results_html = "".join(
        f'<span class="form-badge form-{result.lower()}">'
        f'{safe(result)}</span>'
        for result in recent["Result"]
    )

    points = int(recent["Points"].sum())
    goals_for = int(recent["GF"].sum())
    goals_against = int(recent["GA"].sum())

    st.markdown(
        f"""
        <div class="form-card">
            <div class="form-card-header">
                <div class="form-team-name">{safe(team)}</div>
                <div class="form-label">RECENT FORM · LAST {len(recent)}</div>
            </div>
            <div class="form-card-body">
                <div class="form-results">{results_html}</div>
                <div class="form-stats">
                    <div class="form-stat">
                        <div class="form-stat-value">{points}</div>
                        <div class="form-stat-label">POINTS</div>
                    </div>
                    <div class="form-stat">
                        <div class="form-stat-value">{goals_for}</div>
                        <div class="form-stat-label">SCORED</div>
                    </div>
                    <div class="form-stat">
                        <div class="form-stat-value">{goals_against}</div>
                        <div class="form-stat-label">CONCEDED</div>
                    </div>
                </div>
            </div>
            <div class="form-card-note">
                Oldest → newest · matches before the selected fixture
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_head_to_head(history, home_team, away_team):
    st.subheader("Previous head-to-head matches")

    h2h = history[
        (
            (history["HomeTeam"] == home_team)
            & (history["AwayTeam"] == away_team)
        )
        | (
            (history["HomeTeam"] == away_team)
            & (history["AwayTeam"] == home_team)
        )
    ].sort_values("Date", ascending=False).head(5)

    if h2h.empty:
        st.info("No previous head-to-head matches found in the dataset.")
        return

    display = h2h[
        ["Date", "HomeTeam", "FTHG", "FTAG", "AwayTeam"]
    ].copy()

    display["Date"] = display["Date"].dt.strftime("%d %b %Y")
    display.columns = [
        "Date", "Home team", "Home goals", "Away goals", "Away team"
    ]

    display["Home goals"] = display["Home goals"].astype(int)
    display["Away goals"] = display["Away goals"].astype(int)

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
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

# =========================================================
# MAIN CONTEXT PAGE
# =========================================================

def render_match_context(matches, selected_index):
    inject_context_css()
    if st.session_state.pop("scroll_to_top", False):
        scroll_to_top()
    if selected_index is None:
        st.warning("Select a match first.")
        return

    if selected_index not in matches.index:
        st.error("The selected match could not be found.")
        return

    target = matches.loc[selected_index]

    home_team = target["HomeTeam"]
    away_team = target["AwayTeam"]

    history = prepare_history(matches, target)

    home_history = get_team_history(history, home_team)
    away_history = get_team_history(history, away_team)

    target_date = pd.to_datetime(
        target["Date"], errors="coerce", dayfirst=True
    )
    
    date_str = target_date.strftime('%d %B %Y') if pd.notna(target_date) else ""

    home_logo = team_logo_html(home_team)
    away_logo = team_logo_html(away_team)

    st.markdown(f"""
    <div class="match-header-top">
        <div class="breadcrumb">Pre-Match Analysis &nbsp;/&nbsp; {date_str}</div>
        <div class="header-badges">
            <span class="badge-pill">Illustrative training scenario</span>
            <span class="badge-pill-green">🛡️ Pre-match</span>
        </div>
    </div>
    <div class="teams-section">
        <div class="teams-display">
            <div class="team-block team-block-logo">
                {home_logo}
                <div class="team-text">
                    <span class="team-label">HOME TEAM</span>
                    <span class="team-title">{safe(home_team)}</span>
                </div>
            </div>
            <span class="vs-text">VS</span>
            <div class="team-block team-block-logo">
                {away_logo}
                <div class="team-text">
                    <span class="team-label">AWAY TEAM</span>
                    <span class="team-title">{safe(away_team)}</span>
                </div>
            </div>
        </div>
        <div class="sub-notice">
            Travel back to before kickoff. The selected match's result and post-match statistics are hidden during this stage.
        </div>
    </div>
    <div class="section-title">PRE-MATCH INFORMATION</div>
    <div class="alert-banner">
        <span>🛡️</span> Only information available before kickoff is shown.
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        render_form_card(home_team, home_history)

    with right:
        render_form_card(away_team, away_history)

    st.divider()
    render_head_to_head(history, home_team, away_team)

    st.divider()

    back_col, next_col = st.columns(2)

    with back_col:
        if st.button("← Choose another match", use_container_width=True):
            st.session_state["match_selection_confirmed"] = False
            st.session_state["selected_match_index"] = None
            st.session_state["analysis_step"] = 1
            st.session_state.pop("prediction", None)
            st.rerun()

    with next_col:
        if st.button(
            "Continue to Prediction →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["analysis_step"] = 3
            st.session_state["prediction_ready"] = False
            st.rerun()