import html

import pandas as pd
import numpy as np
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
        .footer-left .brand-name {
            color: #ffffff;
            font-weight: 500;
        }

        .footer-right {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 400;
        }
        .form-card {
            background: #121d28;
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
        .form-seg { opacity: 0.55; border: 1px dashed #64748b; }
        [data-testid="stBaseButton-primary"] {
            background-color: #79d1ad !important;
            border-color: #79d1ad !important;
            color: #0b0f17 !important;
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
        f'<span class="form-badge form-{r.lower()}'
        f'{" form-seg" if div == 2 else ""}" '
        f'title="{"Segunda" if div == 2 else "La Liga"}">{safe(r)}</span>'
        for r, div in zip(
            recent["Result"],
            recent["Division"] if "Division" in recent.columns else [1] * len(recent),
        )
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


# =========================================================
# SECTIONS CSS
# =========================================================

SECTIONS_CSS = """
<style>
.mx-card { background:#121d28; border:1px solid #1e293b; border-radius:14px; padding:22px; margin-bottom:16px; }
.mx-title { color:#fff; font-size:20px; font-weight:700; }
.mx-sub { color:#64748b; font-size:12px; margin:3px 0 16px; }
.mx-note { color:#64748b; font-size:11px; margin-top:12px; line-height:1.5; }
.mx-muted { color:#64748b; font-size:13px; }
.mx-teams { display:grid; grid-template-columns:1fr 1fr; margin-bottom:10px; }
.mx-teams div { color:#fff; font-weight:700; font-size:15px; }
.mx-teams div:last-child { text-align:right; }
.mx-dot { display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:8px; }
.mx-cmp { display:grid; grid-template-columns:70px 1fr 70px; align-items:center; padding:9px 0; border-top:1px solid #1b2635; }
.mx-v { color:#cbd5e1; font-size:17px; font-weight:700; }
.mx-v.r { text-align:right; }
.mx-v.best { color:#34d399; }
.mx-l { text-align:center; color:#94a3b8; font-size:12px; }
.mx-venue { background:#111822; border:1px solid #1e293b; border-radius:10px; padding:12px 14px; margin-top:10px; }
.mx-venue-h { color:#64748b; font-size:10px; letter-spacing:.8px; text-transform:uppercase; }
.mx-venue-v { color:#fff; font-size:16px; font-weight:700; margin:4px 0 2px; }
.mx-venue-s { color:#94a3b8; font-size:12px; }
.mx-badge { display:inline-block; background:#1e293b; color:#94a3b8; font-size:11px; padding:4px 10px; border-radius:20px; margin-bottom:12px; }
.mx-tiles { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:12px; }
.mx-tile { background:#111822; border:1px solid #1e293b; border-radius:10px; padding:14px 8px; text-align:center; }
.mx-tile b { display:block; color:#fff; font-size:28px; line-height:1.1; }
.mx-tile span { color:#94a3b8; font-size:12px; }
.mx-odds { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.mx-odd { background:#111822; border:1px solid #1e293b; border-radius:10px; padding:14px 8px; text-align:center; }
.mx-odd b { display:block; color:#fff; font-size:24px; }
.mx-odd span { color:#94a3b8; font-size:12px; }
.mx-rest { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.mx-rest div { background:#111822; border:1px solid #1e293b; border-radius:10px; padding:14px; }
.mx-rest b { color:#fff; font-size:26px; }
.mx-rest span { display:block; color:#94a3b8; font-size:12px; margin-bottom:4px; }
</style>
"""

ODDS_SETS = [
    ("PSH", "PSD", "PSA"),
    ("B365H", "B365D", "B365A"),
    ("AvgH", "AvgD", "AvgA"),
]


# =========================================================
# SMALL HELPERS
# =========================================================

def _num(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(v) else v


def _fmt(value, decimals=1):
    return "–" if value is None else f"{value:.{decimals}f}"


def _mean(series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    return float(s.mean()) if len(s) else None


def _team_series(df, team, home_col, away_col):
    """A team's own value of a stat in every row, wherever it played."""
    if df.empty or home_col not in df.columns or away_col not in df.columns:
        return pd.Series(dtype=float)
    vals = np.where(df["HomeTeam"] == team, df[home_col], df[away_col])
    return pd.Series(vals, index=df.index)


def _card(title, subtitle, body, note=""):
    note_html = f'<div class="mx-note">{safe(note)}</div>' if note else ""
    return (
        '<div class="mx-card">'
        f'<div class="mx-title">{safe(title)}</div>'
        f'<div class="mx-sub">{safe(subtitle)}</div>'
        f'{body}{note_html}</div>'
    )


def _cmp_row(label, left, right, higher_better=True, decimals=1):
    cl = cr = ""
    if left is not None and right is not None and left != right:
        if (left > right) == higher_better:
            cl = " best"
        else:
            cr = " best"
    return (
        '<div class="mx-cmp">'
        f'<div class="mx-v{cl}">{_fmt(left, decimals)}</div>'
        f'<div class="mx-l">{safe(label)}</div>'
        f'<div class="mx-v r{cr}">{_fmt(right, decimals)}</div>'
        '</div>'
    )


def _info_row(label, left, right):
    return (
        '<div class="mx-cmp">'
        f'<div class="mx-v">{safe(left)}</div>'
        f'<div class="mx-l">{safe(label)}</div>'
        f'<div class="mx-v r">{safe(right)}</div>'
        '</div>'
    )


def _team_goals(match, team):
    if match["HomeTeam"] == team:
        return match["FTHG"], match["FTAG"]
    return match["FTAG"], match["FTHG"]


def _match_odds(match):
    """Opening 1X2 odds: Pinnacle, then Bet365, then market average."""
    for h, d, a in ODDS_SETS:
        vals = [_num(match.get(h)), _num(match.get(d)), _num(match.get(a))]
        if all(v is not None for v in vals):
            return vals
    return None


# =========================================================
# 1) PERFORMANCE COMPARISON
# =========================================================

def _venue_block(label, rows, venue_text):
    if rows.empty:
        return (
            '<div class="mx-venue">'
            f'<div class="mx-venue-h">{safe(label)}</div>'
            '<div class="mx-muted">Not available</div></div>'
        )
    w = int((rows["Result"] == "W").sum())
    d = int((rows["Result"] == "D").sum())
    l = int((rows["Result"] == "L").sum())
    pts = int(rows["Points"].sum())
    conceded = _mean(rows["GA"])
    return (
        '<div class="mx-venue">'
        f'<div class="mx-venue-h">{safe(label)} · last {len(rows)} {safe(venue_text)}</div>'
        f'<div class="mx-venue-v">{w}W · {d}D · {l}L / {pts} points</div>'
        f'<div class="mx-venue-s">{_fmt(conceded)} goals conceded per match</div>'
        '</div>'
    )


def perf_card_html(home_team, away_team, home_history, away_history):
    h5, a5 = home_history.head(5), away_history.head(5)

    metrics = [
        ("Average goals scored", _mean(h5["GF"]), _mean(a5["GF"]), True),
        ("Average goals conceded", _mean(h5["GA"]), _mean(a5["GA"]), False),
        ("Average shots",
         _mean(_team_series(h5, home_team, "HS", "AS")),
         _mean(_team_series(a5, away_team, "HS", "AS")), True),
        ("Average shots on target",
         _mean(_team_series(h5, home_team, "HST", "AST")),
         _mean(_team_series(a5, away_team, "HST", "AST")), True),
        ("Average corners",
         _mean(_team_series(h5, home_team, "HC", "AC")),
         _mean(_team_series(a5, away_team, "HC", "AC")), True),
        ("Average fouls",
         _mean(_team_series(h5, home_team, "HF", "AF")),
         _mean(_team_series(a5, away_team, "HF", "AF")), False),
    ]

    body = (
        '<div class="mx-teams">'
        f'<div><span class="mx-dot" style="background:#34d399"></span>{safe(home_team)}</div>'
        f'<div>{safe(away_team)}<span class="mx-dot" style="background:#60a5fa;margin:0 0 0 8px"></span></div>'
        '</div>'
    )
    body += "".join(_cmp_row(label, l, r, hb) for label, l, r, hb in metrics)

    home_venue = home_history[home_history["HomeTeam"] == home_team].head(5)
    away_venue = away_history[away_history["AwayTeam"] == away_team].head(5)

    body += _venue_block(f"{home_team}", home_venue, "home fixtures")
    body += _venue_block(f"{away_team}", away_venue, "away fixtures")

    return _card(
        "Performance comparison",
        "Per-match averages · last 5 fixtures (La Liga and Segunda)",
        body,
        "Venue windows are separate from overall form. "
        "Green marks the better value in each row.",
    )


# =========================================================
# 2) LEAGUE CONTEXT
# =========================================================

def league_table(history, target):
    """Table of the target's season, built from matches before the date."""
    df = history
    if "Season" in df.columns:
        df = df[df["Season"] == target.get("Season")]
    if "Division" in df.columns:
        df = df[df["Division"] == 1]
    if df.empty:
        return None

    home = pd.DataFrame({"Team": df["HomeTeam"], "GF": df["FTHG"], "GA": df["FTAG"]})
    away = pd.DataFrame({"Team": df["AwayTeam"], "GF": df["FTAG"], "GA": df["FTHG"]})
    t = pd.concat([home, away], ignore_index=True)
    t["Pts"] = np.where(t["GF"] > t["GA"], 3, np.where(t["GF"] == t["GA"], 1, 0))

    table = t.groupby("Team").agg(
        P=("Pts", "size"), Pts=("Pts", "sum"),
        GF=("GF", "sum"), GA=("GA", "sum"),
    )
    table["GD"] = table["GF"] - table["GA"]
    table = table.sort_values(["Pts", "GD", "GF"], ascending=False)
    table["Pos"] = range(1, len(table) + 1)
    return table


def league_card_html(table, home_team, away_team):
    if table is None or (home_team not in table.index and away_team not in table.index):
        body = (
            '<div class="mx-badge">Not available</div>'
            '<div class="mx-venue-v">Season opening fixture</div>'
            '<div class="mx-muted">No prior league table: neither team has '
            'played a La Liga match this season yet.</div>'
        )
        return _card("League context", "Table snapshot before the selected match", body)

    def get(team, col, fmt):
        if team not in table.index:
            return "Not available"
        v = table.loc[team, col]
        return fmt(v)

    rows = ""
    rows += _info_row("Position", get(home_team, "Pos", lambda v: f"{int(v)}"),
                      get(away_team, "Pos", lambda v: f"{int(v)}"))
    rows += _info_row("Points", get(home_team, "Pts", lambda v: f"{int(v)}"),
                      get(away_team, "Pts", lambda v: f"{int(v)}"))
    rows += _info_row("Goal difference", get(home_team, "GD", lambda v: f"{int(v):+d}"),
                      get(away_team, "GD", lambda v: f"{int(v):+d}"))
    rows += _info_row("Matches played", get(home_team, "P", lambda v: f"{int(v)}"),
                      get(away_team, "P", lambda v: f"{int(v)}"))

    body = (
        '<div class="mx-teams">'
        f'<div>{safe(home_team)}</div><div>{safe(away_team)}</div></div>'
        + rows
    )
    return _card(
        "League context",
        "Table snapshot before the selected match",
        body,
        "Ranked by points, goal difference, then goals scored "
        "(official tie-breakers may differ).",
    )


# =========================================================
# 3) RECOVERY WINDOW
# =========================================================

def _rest_days(team_history, target_date):
    if team_history.empty:
        return None
    last = team_history["Date"].iloc[0]          # sorted newest first
    return int((target_date.normalize() - last.normalize()).days)


def recovery_card_html(home_team, away_team, home_history, away_history, target_date):
    hd = _rest_days(home_history, target_date)
    ad = _rest_days(away_history, target_date)

    def cell(team, days):
        value = "Not available" if days is None else f"<b>{days}</b> days"
        return f'<div><span>{safe(team)}</span>{value}</div>'

    note = "Counts every fixture in the data (La Liga and Segunda). No cup or European fixtures."
    if any(d is not None and d > 30 for d in (hd, ad)):
        note = "A gap above 30 days is the summer break. " + note

    return _card(
        "Recovery window",
        "Days since each team's previous fixture",
        f'<div class="mx-rest">{cell(home_team, hd)}{cell(away_team, ad)}</div>',
        note,
    )


# =========================================================
# 4) HEAD TO HEAD
# =========================================================

def _pair(m, a, b):
    x, y = _num(m.get(a)), _num(m.get(b))
    return "–" if x is None or y is None else f"{int(x)}–{int(y)}"


def h2h_card_html(h2h, home_team, away_team):
    if h2h.empty:
        body = (
            '<div class="mx-badge">No previous meeting</div>'
            '<div class="mx-muted">These two clubs have not met in the '
            'available data (2021/22 onwards).</div>'
        )
        return _card("Head-to-head", "Previous meetings only · selected match excluded", body)

    hw = dw = aw = 0
    for _, m in h2h.iterrows():
        hg, ag = _team_goals(m, home_team)
        hw += hg > ag
        aw += hg < ag
        dw += hg == ag

    if hw > aw:
        verdict = f"Previous meetings favored {home_team}."
    elif aw > hw:
        verdict = f"Previous meetings favored {away_team}."
    else:
        verdict = "Previous meetings were evenly split."

    body = (
        '<div class="mx-tiles">'
        f'<div class="mx-tile"><b>{int(hw)}</b><span>{safe(home_team)} wins</span></div>'
        f'<div class="mx-tile"><b>{int(dw)}</b><span>Draws</span></div>'
        f'<div class="mx-tile"><b>{int(aw)}</b><span>{safe(away_team)} wins</span></div>'
        '</div>'
    )

    note = f"{verdict} History is context, not a guarantee."
    if len(h2h) < 3:
        note += " Small sample: treat with caution."
    if "Division" in h2h.columns and (h2h["Division"] == 2).any():
        note += " Segunda meetings are weaker evidence."

    return _card(
        "Head-to-head",
        f"Previous {len(h2h)} meeting(s) only · selected match excluded",
        body,
        note,
    )


def h2h_table(h2h):
    rows = []
    for _, m in h2h.iterrows():
        is_seg = _num(m.get("Division")) == 2
        rows.append({
            "Date": pd.Timestamp(m["Date"]).strftime("%d %b %Y"),
            "Competition": "Segunda" if is_seg else "La Liga",
            "Home": m["HomeTeam"],
            "Score": f'{int(m["FTHG"])}–{int(m["FTAG"])}',
            "Away": m["AwayTeam"],
            "Half-time": _pair(m, "HTHG", "HTAG"),
            "Shots": _pair(m, "HS", "AS"),
            "On target": _pair(m, "HST", "AST"),
            "Corners": _pair(m, "HC", "AC"),
            "Fouls": _pair(m, "HF", "AF"),
            "Yellows": _pair(m, "HY", "AY"),
            "Reds": _pair(m, "HR", "AR"),
        })
    return pd.DataFrame(rows)


# =========================================================
# 5) MARKET EXPECTATION
# =========================================================

def market_card_html(target):
    odds = _match_odds(target)
    if odds is None:
        body = '<div class="mx-muted">Not available for this match.</div>'
    else:
        body = (
            '<div class="mx-odds">'
            f'<div class="mx-odd"><b>{odds[0]:.2f}</b><span>Home</span></div>'
            f'<div class="mx-odd"><b>{odds[1]:.2f}</b><span>Draw</span></div>'
            f'<div class="mx-odd"><b>{odds[2]:.2f}</b><span>Away</span></div>'
            '</div>'
        )
    return _card(
        "Market Expectation",
        "Optional analytical reference · pre-match only",
        body,
        "Based on pre-match bookmaker odds. This is an analytical reference, "
        "not a betting recommendation.",
    )


# =========================================================
# MAIN CONTEXT PAGE
# =========================================================

def render_match_context(matches, selected_index):
    inject_context_css()
    st.markdown(SECTIONS_CSS, unsafe_allow_html=True)

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

    target_date = pd.to_datetime(target["Date"], errors="coerce", dayfirst=True)
    date_str = target_date.strftime("%d %B %Y") if pd.notna(target_date) else ""

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
        
    st.write("")

    table = league_table(history, target)

    mask = (
        ((history["HomeTeam"] == home_team) & (history["AwayTeam"] == away_team))
        | ((history["HomeTeam"] == away_team) & (history["AwayTeam"] == home_team))
    )
    h2h = history[mask].sort_values("Date", ascending=False).head(5)

    # ---- row 1: performance | league + recovery ----
    left, right = st.columns([1.5, 1], gap="large")

    with left:
        st.markdown(
            perf_card_html(home_team, away_team, home_history, away_history),
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(league_card_html(table, home_team, away_team), unsafe_allow_html=True)
        st.markdown(
            recovery_card_html(home_team, away_team, home_history, away_history, target_date),
            unsafe_allow_html=True,
        )

    # ---- row 2: head-to-head | market expectation ----
    left, right = st.columns([1.5, 1], gap="large")

    with left:
        st.markdown(h2h_card_html(h2h, home_team, away_team), unsafe_allow_html=True)
        if not h2h.empty:
            with st.expander("Meeting-by-meeting details"):
                st.dataframe(h2h_table(h2h), hide_index=True, use_container_width=True)

    with right:
        show_market = st.checkbox(
            "Show market expectation (optional)",
            key="show_market_expectation",
        )
        if show_market:
            st.markdown(market_card_html(target), unsafe_allow_html=True)

    st.markdown(
        '<div style="color:#ffffff; font-weight:600; font-size:16px; margin-bottom:2px;">'
        'Enough evidence to form a view?'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "These illustrative indicators support reasoning. "
        "They cannot determine the result."
    )
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
            "Make your Prediction →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["analysis_step"] = 3
            st.session_state["prediction_ready"] = False
            st.rerun()
            
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