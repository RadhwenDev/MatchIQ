import pandas as pd
import streamlit as st

from match_context import (
    inject_context_css,
    scroll_to_top,
    prepare_history,
    get_team_history,
    safe,
    _team_series,
    _mean,
)
from match_learn import _choose_another
from team_utils import team_logo_html


# =========================================================
# CSS
# =========================================================

STATS_CSS = """
<style>
.sx-tag { color:#79d1ad; font-size:11px; letter-spacing:2px; font-weight:700; }
.sx-title { color:#fff; font-size:40px; font-weight:800; margin:6px 0 6px; }
.sx-sub { color:#94a3b8; font-size:15px; margin-bottom:20px; }

.sx-bar { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap;
          gap:14px; background:#121d28; border:1px solid #1e293b; border-radius:16px;
          padding:18px 24px; margin-bottom:12px; }
.sx-bar-l { display:flex; align-items:center; gap:18px; flex-wrap:wrap; }
.sx-ft { background:rgba(121,209,173,.14); color:#79d1ad; font-size:12px; font-weight:700;
         padding:5px 14px; border-radius:20px; border:1px solid rgba(121,209,173,.4); }
.sx-bar-team { color:#fff; font-size:20px; font-weight:700; }
.sx-bar-score { color:#fff; font-size:34px; font-weight:800; }
.sx-bar-ht { color:#64748b; font-size:12px; }
.sx-bar-note { color:#64748b; font-size:12px; }

.sx-notice { background:#0d281e; border:1px solid #144734; border-radius:10px;
             padding:12px 18px; color:#94a3b8; font-size:13px; margin-bottom:22px; }

.sx-card { background:#121d28; border:1px solid #1e293b; border-radius:16px;
           padding:24px 26px; margin-bottom:16px; }
.sx-card-t { color:#fff; font-size:19px; font-weight:700; }
.sx-card-s { color:#64748b; font-size:12px; margin:3px 0 14px; }
.sx-legend { display:flex; justify-content:space-between; color:#fff; font-size:14px;
             font-weight:700; margin-bottom:6px; }
.sx-dot { display:inline-block; width:9px; height:9px; border-radius:3px; margin:0 8px; }
.sx-dot.h { background:#6fd3a8; margin-left:0; }
.sx-dot.a { background:#8093b0; margin-right:0; }

.sx-row { padding:12px 0 8px; }
.sx-row-top { display:grid; grid-template-columns:70px 1fr 70px; align-items:center; }
.sx-v { color:#cbd5e1; font-size:18px; font-weight:700; }
.sx-v.r { text-align:right; }
.sx-l { text-align:center; color:#94a3b8; font-size:13px; }
.sx-card.plain .sx-row { border-top:1px solid #1b2635; padding:12px 0; }

/* chance creation: bars grow from the center to each side */
.sx-card.chance .sx-v { font-weight:400; }
.sx-split { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px; }
.sx-half { height:6px; background:#1b2635; border-radius:6px; display:flex; }
.sx-half.l { justify-content:flex-end; }
.sx-half .fill { height:100%; border-radius:6px; }
.sx-half.l .fill { background:#6fd3a8; }
.sx-half.r .fill { background:#8093b0; }

.sx-note { color:#64748b; font-size:12px; margin-top:14px; line-height:1.5; }

.sx-fin { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.sx-fin-team { color:#94a3b8; font-size:13px; }
.sx-fin-pct { color:#fff; font-size:32px; font-weight:800; margin:4px 0 2px; }
.sx-fin-d { color:#64748b; font-size:12px; }

.sx-insight { background:rgba(121,209,173,.07); border:1px solid rgba(121,209,173,.3);
              border-radius:16px; padding:24px 28px; margin-bottom:16px; }
.sx-insight-t { color:#79d1ad; font-size:20px; font-weight:800; margin-bottom:8px; }
.sx-insight-d { color:#cbd5e1; font-size:14px; line-height:1.65; }

.sx-cmp { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }
.sx-cmp-box { background:#121d28; border:1px solid #1e293b; border-radius:16px;
              padding:22px 26px; }
.sx-cmp-h { color:#64748b; font-size:11px; letter-spacing:1.2px; font-weight:700;
            margin-bottom:10px; }
.sx-cmp-h.after { color:#79d1ad; }
.sx-cmp-v { color:#fff; font-size:18px; font-weight:700; margin-bottom:4px; }
.sx-cmp-d { color:#64748b; font-size:12px; }

.sx-footer { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
             padding:22px 0; margin-top:40px;
             border-top:1px solid rgba(255,255,255,.1);
             color:#94a3b8; font-size:14px; }
.sx-footer b { color:#fff; font-weight:500; }

@media (max-width:700px) {
    .sx-title { font-size:28px; }
    .sx-cmp { grid-template-columns:1fr; }
}
</style>
"""


# =========================================================
# CALLBACKS
# =========================================================

def _back_learn():
    st.session_state["analysis_step"] = 5
    st.session_state["scroll_to_top"] = True


# =========================================================
# HELPERS
# =========================================================

def _num(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(v) else v


def _int_or_none(value):
    v = _num(value)
    return None if v is None else int(v)


def _fmt(value, decimals=0, suffix=""):
    return "–" if value is None else f"{value:.{decimals}f}{suffix}"


def _xg_est(shots, on_target):
    """Rough shot-based estimate. Not a real xG model."""
    if shots is None or on_target is None:
        return None
    return on_target * 0.30 + max(shots - on_target, 0) * 0.04


def _row(label, left, right, decimals=0, suffix="", bar=True):
    bar_html = ""
    if bar:
        lv, rv = left or 0, right or 0
        total = lv + rv
        lp = lv / total * 100 if total > 0 else 0
        rp = rv / total * 100 if total > 0 else 0
        bar_html = (
            '<div class="sx-split">'
            '<div class="sx-half l">'
            f'<div class="fill" style="width:{lp:.1f}%"></div></div>'
            '<div class="sx-half r">'
            f'<div class="fill" style="width:{rp:.1f}%"></div></div>'
            '</div>'
        )

    return (
        '<div class="sx-row">'
        '<div class="sx-row-top">'
        f'<div class="sx-v">{_fmt(left, decimals, suffix)}</div>'
        f'<div class="sx-l">{safe(label)}</div>'
        f'<div class="sx-v r">{_fmt(right, decimals, suffix)}</div>'
        '</div>'
        f'{bar_html}'
        '</div>'
    )


def _legend(home, away):
    return (
        '<div class="sx-legend">'
        f'<span><i class="sx-dot h"></i>{safe(home)}</span>'
        f'<span>{safe(away)}<i class="sx-dot a"></i></span></div>'
    )


def _card(title, subtitle, body, note="", cls=""):
    note_html = f'<div class="sx-note">{safe(note)}</div>' if note else ""
    return (
        f'<div class="sx-card {cls}">'
        f'<div class="sx-card-t">{safe(title)}</div>'
        f'<div class="sx-card-s">{safe(subtitle)}</div>'
        f'{body}{note_html}</div>'
    )


def _fin_block(team, goals, shots):
    if shots is None or goals is None:
        pct, detail = "–", "Not available"
    elif shots == 0:
        pct, detail = "–", f"{goals} goals / 0 shots"
    else:
        pct = f"{goals / shots * 100:.0f}%"
        detail = f"{goals} goals / {shots} shots"
    return (
        '<div>'
        f'<div class="sx-fin-team">{safe(team)}</div>'
        f'<div class="sx-fin-pct">{pct}</div>'
        f'<div class="sx-fin-d">{safe(detail)}</div>'
        '</div>'
    )


def _insight(home, away, hg, ag, hs, as_, hst, ast):
    """Title and text comparing shot volume with the real outcome."""
    if hs is None or as_ is None:
        return ("Match numbers",
                "Shot data is not available for this fixture, so the match "
                "cannot be compared with the pre-match averages.")

    leader = home if hs > as_ else away if as_ > hs else None
    winner = home if hg > ag else away if ag > hg else None
    shots = {home: hs, away: as_}
    sot = {home: hst, away: ast}
    goals = {home: hg, away: ag}

    closing = ("These stats describe the match; they do not prove what "
               "caused the result.")

    if leader and winner and leader != winner:
        other_shots = shots[winner]
        if sot[winner] is not None:
            detail = (f"{winner} put {sot[winner]} of {other_shots} shots on "
                      f"target and scored {goals[winner]}")
        else:
            detail = f"{winner} scored {goals[winner]} from {other_shots} shots"
        return (
            "More shots. A different outcome.",
            f"{leader} had more shots ({shots[leader]} to {other_shots}), "
            f"but {detail}. The {hg}–{ag} score shows why volume alone cannot "
            f"tell the whole story. {closing}",
        )

    if leader and winner and leader == winner:
        return (
            "Volume and result agreed.",
            f"{leader} led on shots ({shots[leader]} to "
            f"{min(hs, as_)}) and won {hg}–{ag}. Even so, shots are only one "
            f"view of the match, and a good process can still lose. {closing}",
        )

    if leader and not winner:
        return (
            "Level on the scoreboard.",
            f"{leader} had more shots ({max(hs, as_)} to {min(hs, as_)}), "
            f"but the match ended {hg}–{ag}. Shot volume does not always turn "
            f"into goals. {closing}",
        )

    if winner:
        return (
            "Equal shots, one winner.",
            f"Both sides had {hs} shots, yet {winner} won {hg}–{ag}. "
            f"Efficiency, not volume, separated them. {closing}",
        )

    return (
        "Even on every count.",
        f"Both sides had {hs} shots and the match ended {hg}–{ag}. {closing}",
    )


# =========================================================
# MAIN PAGE
# =========================================================

def render_match_stats(matches, selected_index):
    inject_context_css()
    st.markdown(STATS_CSS, unsafe_allow_html=True)

    if st.session_state.pop("scroll_to_top", False):
        scroll_to_top()

    if selected_index is None or selected_index not in matches.index:
        st.warning("Select a match first.")
        return

    idx = int(selected_index)

    # never show actual-match stats before the prediction is locked
    if st.session_state.get("prediction_locked_for") != idx:
        st.warning("Lock a prediction and reveal the result first.")
        return

    target = matches.loc[idx]
    home = target["HomeTeam"]
    away = target["AwayTeam"]
    league = target.get("League", "La Liga")
    season = target.get("Season", "")

    hg, ag = _int_or_none(target.get("FTHG")), _int_or_none(target.get("FTAG"))
    if hg is None or ag is None:
        st.warning("The actual score is unavailable for this fixture.")
        return

    target_date = pd.to_datetime(target["Date"], errors="coerce", dayfirst=True)
    date_str = target_date.strftime("%d %B %Y") if pd.notna(target_date) else ""

    # ---------- actual-match numbers (this fixture only) ----------
    hs, as_ = _int_or_none(target.get("HS")), _int_or_none(target.get("AS"))
    hst, ast = _int_or_none(target.get("HST")), _int_or_none(target.get("AST"))
    hc, ac = _int_or_none(target.get("HC")), _int_or_none(target.get("AC"))
    hf, af = _int_or_none(target.get("HF")), _int_or_none(target.get("AF"))
    hy, ay = _int_or_none(target.get("HY")), _int_or_none(target.get("AY"))
    hr, ar = _int_or_none(target.get("HR")), _int_or_none(target.get("AR"))
    hth, hta = _int_or_none(target.get("HTHG")), _int_or_none(target.get("HTAG"))

    # optional columns: only present if you add an external source
    hposs, aposs = _num(target.get("HPoss")), _num(target.get("APoss"))
    hxg_real, axg_real = _num(target.get("HxG")), _num(target.get("AxG"))

    # ---------- pre-match averages (for the final comparison) ----------
    history = prepare_history(matches, target)
    h5 = get_team_history(history, home).head(5)
    a5 = get_team_history(history, away).head(5)
    avg_h = _mean(_team_series(h5, home, "HS", "AS"))
    avg_a = _mean(_team_series(a5, away, "HS", "AS"))

    # ---------- header ----------
    st.markdown(
        '<div class="match-header-top">'
        f'<div class="breadcrumb">{safe(league)} &nbsp;/&nbsp; {safe(date_str)}'
        f' &nbsp;/&nbsp; {safe(season)}</div>'
        '<div class="header-badges">'
        '<span class="badge-pill">Illustrative training scenario</span>'
        '<span class="badge-pill-green">🟢 Revealed · post-match</span>'
        '</div></div>'
        '<div class="teams-section"><div class="teams-display">'
        '<div class="team-block team-block-logo">'
        f'{team_logo_html(home)}'
        '<div class="team-text"><span class="team-label">HOME TEAM</span>'
        f'<span class="team-title">{safe(home)}</span></div></div>'
        '<span class="vs-text">VS</span>'
        '<div class="team-block team-block-logo">'
        f'{team_logo_html(away)}'
        '<div class="team-text"><span class="team-label">AWAY TEAM</span>'
        f'<span class="team-title">{safe(away)}</span></div></div>'
        '</div>'
        '<div class="sub-notice">Historical match data. '
        'A safe space to practice your reasoning.</div></div>',
        unsafe_allow_html=True,
    )

    # ---------- title + full time bar ----------
    ht_html = (
        f'<span class="sx-bar-ht">Half-time {hth} — {hta}</span>'
        if hth is not None and hta is not None else ""
    )

    has_poss = hposs is not None and aposs is not None
    has_xg = hxg_real is not None and axg_real is not None

    if has_poss and has_xg:
        notice_tail = ""
    elif has_xg:
        notice_tail = " Possession is not available for this match."
    else:
        notice_tail = (" xG is estimated from shots, and possession is not "
                       "available in this dataset.")

    st.markdown(
        '<div class="sx-tag">POST-MATCH ANALYSIS</div>'
        '<div class="sx-title">What actually happened?</div>'
        '<div class="sx-sub">The revealed match, viewed separately from the '
        'information you had before kickoff.</div>'
        '<div class="sx-bar"><div class="sx-bar-l">'
        '<span class="sx-ft">Full Time</span>'
        f'<span class="sx-bar-team">{safe(home)}</span>'
        f'<span class="sx-bar-score">{hg} — {ag}</span>'
        f'<span class="sx-bar-team">{safe(away)}</span>'
        f'{ht_html}</div>'
        '<span class="sx-bar-note">Actual-match numbers · selected fixture '
        'only</span></div>'
        '<div class="sx-notice">👁 Available only after result reveal. These '
        'are the real numbers of this match, not pre-match averages.'
        f'{safe(notice_tail)}</div>',
        unsafe_allow_html=True,
    )

    # ---------- cards ----------
    left, right = st.columns([1.2, 1], gap="large")

    # LEFT: the only card with split bars
    with left:
        body = _legend(home, away)

        if has_poss:
            body += _row("Possession", hposs, aposs, suffix="%")

        body += _row("Shots", hs, as_)
        body += _row("Shots on target", hst, ast)
        body += _row("Corners", hc, ac)

        if has_xg:
            body += _row("xG", hxg_real, axg_real, decimals=2)
            note = ("xG is an estimate of chance quality, not a prediction "
                    "of the final score.")
        else:
            body += _row("xG (est.)", _xg_est(hs, hst), _xg_est(as_, ast),
                         decimals=2)
            note = ("xG (est.) is a rough estimate from shots (0.30 per shot "
                    "on target, 0.04 per other shot), not a real xG model.")
            if not has_poss:
                note += " Possession is not available in this dataset."

        if hth is not None and hta is not None:
            body += _row("Half-time goals", hth, hta)

        st.markdown(
            _card(
                "Ball control & chance creation" if has_poss
                else "Chance creation",
                f"{home} | {away} · actual-match data",
                body,
                note,
                cls="chance",
            ),
            unsafe_allow_html=True,
        )

    # RIGHT: plain numbers, no bars
    with right:
        disc = _legend(home, away)
        disc += _row("Fouls", hf, af, bar=False)
        disc += _row("Yellow cards", hy, ay, bar=False)
        disc += _row("Red cards", hr, ar, bar=False)
        st.markdown(
            _card("Discipline", "Actual-match totals", disc, cls="plain"),
            unsafe_allow_html=True,
        )

        fin = (
            '<div class="sx-fin">'
            f'{_fin_block(home, hg, hs)}'
            f'{_fin_block(away, ag, as_)}'
            '</div>'
        )
        st.markdown(
            _card("Finishing efficiency", "Goals as a share of shots", fin),
            unsafe_allow_html=True,
        )

    # ---------- insight ----------
    title, text = _insight(home, away, hg, ag, hs, as_, hst, ast)
    st.markdown(
        '<div class="sx-insight">'
        f'<div class="sx-insight-t">{safe(title)}</div>'
        f'<div class="sx-insight-d">{safe(text)}</div></div>',
        unsafe_allow_html=True,
    )

    # ---------- before vs after ----------
    st.markdown(
        '<div class="sx-cmp">'
        '<div class="sx-cmp-box">'
        '<div class="sx-cmp-h">BEFORE KICKOFF · HISTORICAL AVERAGES</div>'
        f'<div class="sx-cmp-v">Average shots: {safe(home)} {_fmt(avg_h, 1)} | '
        f'{safe(away)} {_fmt(avg_a, 1)}</div>'
        '<div class="sx-cmp-d">Last 5 prior fixtures · available during your '
        'prediction</div></div>'
        '<div class="sx-cmp-box">'
        '<div class="sx-cmp-h after">AFTER REVEAL · THIS MATCH ONLY</div>'
        f'<div class="sx-cmp-v">Actual shots: {safe(home)} {_fmt(hs)} | '
        f'{safe(away)} {_fmt(as_)}</div>'
        '<div class="sx-cmp-d">Selected fixture · never shown before you lock '
        'and reveal</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- buttons ----------
    b1, _, b3 = st.columns([1.3, 2.4, 1.5], gap="medium")

    with b1:
        st.button(
            "← Back to the explanation",
            use_container_width=True,
            on_click=_back_learn,
        )

    with b3:
        st.button(
            "Analyze another match ➔",
            type="primary",
            use_container_width=True,
            on_click=_choose_another,
        )

    st.markdown(
        '<div class="sx-footer">'
        '<span><b>MatchIQ</b> &nbsp;/&nbsp; An independent football learning lab</span>'
        '<span>Study evidence. Make a decision. Learn from the outcome.</span>'
        '</div>',
        unsafe_allow_html=True,
    )