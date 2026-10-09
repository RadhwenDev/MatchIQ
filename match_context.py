import html

import pandas as pd
import streamlit as st


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
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HELPERS
# =========================================================

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
                <div class="form-label">LAST {len(recent)} MATCHES</div>
            </div>
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


# =========================================================
# MAIN CONTEXT PAGE
# =========================================================

def render_match_context(matches, selected_index):
    inject_context_css()

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

    st.title("Pre-Match Analysis")
    st.caption(
        "Travel back to before kickoff. The selected match's result "
        "and post-match statistics are hidden during this stage."
    )

    if pd.notna(target_date):
        st.markdown(
            f"**{home_team} vs {away_team}** · "
            f"{target_date.strftime('%d %B %Y')}"
        )
    else:
        st.markdown(f"**{home_team} vs {away_team}**")

    st.divider()

    if history.empty:
        st.warning(
            "No completed matches before this fixture were found. "
            "Try a later fixture or load earlier seasons."
        )
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            render_metric("Historical matches", len(history))

        with col2:
            seasons_count = (
                history["Season"].nunique()
                if "Season" in history.columns
                else "Unknown"
            )
            render_metric("Historical seasons", seasons_count)

        with col3:
            first_date = history["Date"].min()
            render_metric(
                "History available from",
                first_date.strftime("%d %b %Y")
                if pd.notna(first_date)
                else "Unknown",
            )

        last_date = history["Date"].max()
        if pd.notna(last_date):
            st.caption(
                f"Historical data available through "
                f"{last_date.strftime('%d %b %Y')}. "
                "Matches on the selected fixture's date are excluded."
            )

    st.divider()
    st.subheader("Team form before kickoff")

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