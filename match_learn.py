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
from team_utils import team_logo_html


# =========================================================
# CSS
# =========================================================

LEARN_CSS = """
<style>
.ln-tag { color:#79d1ad; font-size:11px; letter-spacing:2px; font-weight:700; }
.ln-title { color:#fff; font-size:40px; font-weight:800; margin:6px 0 14px; }
.ln-strip { display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:26px; }
.ln-res { font-size:13px; font-weight:700; padding:6px 16px; border-radius:20px; }
.ln-res.good { background:rgba(121,209,173,.14); color:#79d1ad; border:1px solid rgba(121,209,173,.4); }
.ln-res.bad { background:rgba(245,160,170,.12); color:#f5a0aa; border:1px solid rgba(245,160,170,.4); }
.ln-strip-t { color:#94a3b8; font-size:14px; }

.ln-card { background:#121d28; border:1px solid #1e293b; border-radius:16px;
           padding:24px 26px; }
.ln-card-h { font-size:12px; letter-spacing:1.5px; font-weight:700; margin-bottom:6px; }
.ln-card-h.good { color:#79d1ad; }
.ln-card-h.warn { color:#f5cf72; }
.ln-card-h + .ln-item { border-top:none; }
.ln-item { border-top:1px solid #1b2635; padding:16px 0 6px; }
.ln-item-t { color:#fff; font-size:16px; font-weight:700; margin-bottom:8px; }
.ln-ic { margin-right:8px; }
.ln-ic.good { color:#79d1ad; }
.ln-ic.warn { color:#f5cf72; }
.ln-item-l { color:#64748b; font-size:10px; letter-spacing:1px; font-weight:700;
             text-transform:uppercase; margin-bottom:6px; }
.ln-pill { display:inline-block; background:#1b2635; color:#e2e8f0; font-size:13px;
           font-weight:600; padding:6px 12px; border-radius:10px; margin-bottom:8px; }
.ln-item-d { color:#94a3b8; font-size:13px; line-height:1.55; }
.ln-empty { color:#64748b; font-size:13px; padding:16px 0 6px; }

.ln-h2h { display:flex; gap:14px; background:#121d28; border:1px solid #1e293b;
          border-radius:16px; padding:20px 26px; margin:16px 0; }
.ln-h2h-i { font-size:20px; }
.ln-h2h-t { color:#fff; font-size:15px; font-weight:700; margin-bottom:4px; }
.ln-h2h-d { color:#94a3b8; font-size:13px; line-height:1.5; }

.ln-lesson { background:rgba(121,209,173,.06); border:1px solid rgba(121,209,173,.25);
             border-radius:16px; padding:26px 30px; margin-bottom:16px; }
.ln-lesson-h { color:#79d1ad; font-size:12px; letter-spacing:1.5px; font-weight:700;
               margin-bottom:10px; }
.ln-lesson-t { color:#fff; font-size:22px; font-weight:700; line-height:1.35; margin-bottom:10px; }
.ln-lesson-d { color:#94a3b8; font-size:14px; line-height:1.6; }

.ln-checks { display:grid; grid-template-columns:1fr 1fr; gap:28px;
             background:#121d28; border:1px solid #1e293b; border-radius:16px;
             padding:24px 28px; margin-bottom:20px; }
.ln-check-t { color:#fff; font-size:15px; font-weight:700; margin-bottom:6px; }
.ln-check-d { color:#94a3b8; font-size:13px; line-height:1.55; }

.ln-footer { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
             padding:22px 0; margin-top:40px;
             border-top:1px solid rgba(255,255,255,.1);
             color:#94a3b8; font-size:14px; }
.ln-footer b { color:#fff; font-weight:500; }

@media (max-width:700px) {
    .ln-title { font-size:28px; }
    .ln-checks { grid-template-columns:1fr; gap:18px; }
}
</style>
"""


# =========================================================
# CALLBACKS
# =========================================================

def _choose_another():
    for k in list(st.session_state.keys()):
        if k.startswith(("pd_", "_pd_")):
            del st.session_state[k]
    for k in ("prediction", "predicted_score", "prediction_locked_for",
              "actual_result", "actual_score", "learning_reflection"):
        st.session_state.pop(k, None)
    st.session_state["match_selection_confirmed"] = False
    st.session_state["selected_match_index"] = None
    st.session_state["analysis_step"] = 1


def _go_stats():
    st.session_state["analysis_step"] = 6
    st.session_state["scroll_to_top"] = True


# =========================================================
# SMALL HELPERS
# =========================================================

def _num(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(v) else v


def _outcome_of(hg, ag):
    return "H" if hg > ag else "A" if ag > hg else "D"


def _outcome_text(code, home, away):
    if code == "H":
        return f"{home} win"
    if code == "A":
        return f"{away} win"
    return "Draw"


def _join(items):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _rest_days(team_hist, target_date):
    if team_hist.empty:
        return None
    last = team_hist["Date"].iloc[0]  # sorted newest first
    return int((target_date.normalize() - last.normalize()).days)


def _record(rows):
    w = int((rows["Result"] == "W").sum())
    d = int((rows["Result"] == "D").sum())
    l = int((rows["Result"] == "L").sum())
    return w, d, l, int(rows["Points"].sum())


# =========================================================
# INDICATORS (all computed from pre-match history only)
# =========================================================

def _ind_form(home, away, hh, ah):
    h5, a5 = hh.head(5), ah.head(5)
    if h5.empty or a5.empty:
        return None
    hp, ap = int(h5["Points"].sum()), int(a5["Points"].sum())
    diff = hp - ap
    favors = "H" if diff >= 2 else "A" if diff <= -2 else None
    fav, other = (home, away) if favors == "H" else (away, home)
    fp, op = (hp, ap) if favors == "H" else (ap, hp)
    base = f"{fav} took {fp} points from the last 5 against {op} for {other}."
    return {
        "short": "recent form",
        "favors": favors,
        "label": "Overall form · last 5 fixtures",
        "pill": f"{home} {hp} points / {away} {ap} points",
        "title": f"{fav} had stronger recent form",
        "body_right": base + " This was a reasonable signal to consider.",
        "body_missed": base + " Recent form deserved more weight.",
        "bal_title": "Recent form was level",
        "bal_body": "Neither side had a clear points edge over the last 5 fixtures.",
    }


def _ind_chances(home, away, hh, ah):
    h5, a5 = hh.head(5), ah.head(5)
    hs = _mean(_team_series(h5, home, "HS", "AS"))
    as_ = _mean(_team_series(a5, away, "HS", "AS"))
    hst = _mean(_team_series(h5, home, "HST", "AST"))
    ast = _mean(_team_series(a5, away, "HST", "AST"))
    if None in (hs, as_, hst, ast):
        return None
    diff = hst - ast
    favors = "H" if diff >= 1.0 else "A" if diff <= -1.0 else None
    fav = home if favors == "H" else away
    fsot, osot = (hst, ast) if favors == "H" else (ast, hst)
    base = f"{fav} averaged {fsot:.1f} shots on target versus {osot:.1f}."
    return {
        "short": "chance creation",
        "favors": favors,
        "label": "Pre-match per-fixture averages · last 5",
        "pill": (f"Shots: {hs:.1f} vs {as_:.1f} / "
                 f"On target: {hst:.1f} vs {ast:.1f}"),
        "title": f"{fav} created more chances recently",
        "body_right": base + " Chance creation supported your view, "
                             "without guaranteeing finishing.",
        "body_missed": base + " Chance creation pointed the other way.",
        "bal_title": "Chance creation was similar",
        "bal_body": "Shots on target were close between the two sides.",
    }


def _ind_venue(home, away, hh, ah):
    hv = hh[hh["HomeTeam"] == home].head(5)
    av = ah[ah["AwayTeam"] == away].head(5)
    if len(hv) < 3 or len(av) < 3:
        return None

    hw, hd, hl, hp = _record(hv)
    aw, ad, al, ap = _record(av)
    hpm, apm = hp / len(hv), ap / len(av)
    hga, aga = float(hv["GA"].mean()), float(av["GA"].mean())

    edge = (hpm - apm) + (aga - hga)
    favors = "H" if edge >= 0.4 else "A" if edge <= -0.4 else None

    if favors == "A":
        pill = f"{away} away: {aw}W · {ad}D · {al}L / {ap} points"
        base = (f"{away} conceded {aga:.1f} goals per away fixture, "
                f"versus {hga:.1f} for {home} at home.")
        title = f"{away} had strong away form"
    elif favors == "H":
        pill = f"{home} home: {hw}W · {hd}D · {hl}L / {hp} points"
        base = (f"{home} conceded {hga:.1f} goals per home fixture, "
                f"versus {aga:.1f} for {away} away.")
        title = f"{home} had strong home form"
    else:
        pill = f"{home} home {hp} points / {away} away {ap} points"
        base = ""
        title = ""

    return {
        "short": "venue form",
        "favors": favors,
        "label": "Venue form · separate last-5 windows",
        "pill": pill,
        "title": title,
        "body_right": base + " Venue form supported your view.",
        "body_missed": base + " Venue-specific form deserved more weight.",
        "bal_title": "Venue form was similar",
        "bal_body": "Home and away records were close.",
    }


def _ind_recovery(home, away, hh, ah, target_date):
    hd, ad = _rest_days(hh, target_date), _rest_days(ah, target_date)
    if hd is None or ad is None or hd > 30 or ad > 30:
        return None
    diff = hd - ad
    favors = "H" if diff >= 2 else "A" if diff <= -2 else None
    rested, tired = (home, away) if favors == "H" else (away, home)
    base = f"{rested} had a {abs(diff)}-day recovery advantage."
    return {
        "short": "rest advantage",
        "favors": favors,
        "label": "Recovery window · since the previous fixture",
        "pill": f"{home} {hd} days / {away} {ad} days",
        "title": f"{tired} had fewer rest days",
        "body_right": base + " Rest is relevant context, not proof that "
                             "fatigue changes the result.",
        "body_missed": base + " Rest is relevant context, not proof that "
                              "fatigue caused the result.",
        "bal_title": "Recovery time was similar",
        "bal_body": "Both teams had a comparable rest window.",
    }


def _split(code, indicators):
    right, missed = [], []
    for ind in indicators:
        f = ind["favors"]
        if code == "D":
            (right if f is None else missed).append(ind)
        elif f is None:
            continue
        elif f == code:
            right.append(ind)
        else:
            missed.append(ind)
    return right, missed


def _item_html(ind, kind):
    if kind == "right":
        if ind["favors"] is None:
            title, body = ind["bal_title"], ind["bal_body"]
        else:
            title, body = ind["title"], ind["body_right"]
        icon, cls = "✓", "good"
    else:
        title, body = ind["title"], ind["body_missed"]
        icon, cls = "⚠️", "warn"

    return (
        '<div class="ln-item">'
        f'<div class="ln-item-t"><span class="ln-ic {cls}">{icon}</span>{safe(title)}</div>'
        f'<div class="ln-item-l">{safe(ind["label"])}</div>'
        f'<div class="ln-pill">{safe(ind["pill"])}</div>'
        f'<div class="ln-item-d">{safe(body)}</div>'
        '</div>'
    )


def _column_html(title_html, cls, items, kind, empty_text):
    body = (
        "".join(_item_html(i, kind) for i in items)
        if items
        else f'<div class="ln-empty">{safe(empty_text)}</div>'
    )
    return (
        '<div class="ln-card">'
        f'<div class="ln-card-h {cls}">{title_html}</div>'
        f'{body}</div>'
    )


# =========================================================
# TEXTS
# =========================================================

def _lesson_title(code, right, missed):
    if code == "D":
        if missed:
            return (f"Some indicators had a clear edge "
                    f"({_join(i['short'] for i in missed[:2])}), "
                    "which made a draw harder to defend.")
        return ("The indicators were balanced, which fits a draw call, "
                "but draws remain the hardest outcome to predict.")
    if right and missed:
        return (f"{_join(i['short'] for i in right[:2]).capitalize()} supported "
                f"your view, but {_join(i['short'] for i in missed[:2])} "
                "deserved more weight.")
    if right:
        return ("The indicators mostly agreed with your view. "
                "Football still carries a lot of randomness.")
    if missed:
        return ("Most indicators pointed against your pick. Weigh the "
                "counter-case before you commit next time.")
    return ("The indicators were close to balanced. Low-signal matches are "
            "hard to call, whatever the outcome.")


def _accuracy_text(correct, exact, has_score):
    if correct and exact:
        return ("Your selected winner and exact score both matched. That is a "
                "factual check of this attempt, not proof of skill.")
    if correct:
        extra = ("the exact score missed" if has_score
                 else "no exact score was submitted")
        return (f"Your selected winner matched, but {extra}. That is a "
                "factual check of this attempt, not a judgment of your "
                "overall ability.")
    what = "selected winner and exact score" if has_score else "selected winner"
    return (f"Your {what} missed. That is a factual check of this attempt, "
            "not a judgment of your overall ability.")


def _reasoning_text(right, missed):
    if right and missed:
        return (f"Next time, balance {_join(i['short'] for i in right[:2])} "
                f"with {_join(i['short'] for i in missed[:2])}. Confidence in "
                "reasoning is separate from being correct.")
    return ("Next time, always check the counter-case before locking. "
            "Confidence in reasoning is separate from being correct.")


# =========================================================
# MAIN PAGE
# =========================================================

def render_match_learn(matches, selected_index):
    inject_context_css()
    st.markdown(LEARN_CSS, unsafe_allow_html=True)

    if st.session_state.pop("scroll_to_top", False):
        scroll_to_top()

    if selected_index is None or selected_index not in matches.index:
        st.warning("Select a match first.")
        return

    idx = int(selected_index)
    target = matches.loc[idx]
    home = target["HomeTeam"]
    away = target["AwayTeam"]
    league = target.get("League", "La Liga")
    season = target.get("Season", "")

    hg, ag = _num(target.get("FTHG")), _num(target.get("FTAG"))
    code = st.session_state.get("prediction")
    locked = st.session_state.get("prediction_locked_for") == idx

    if hg is None or ag is None or code is None or not locked:
        st.warning("No locked prediction was found for this match.")
        return

    hg, ag = int(hg), int(ag)
    pred_score = st.session_state.get("predicted_score")

    actual = _outcome_of(hg, ag)
    correct = code == actual
    exact = pred_score is not None and tuple(pred_score) == (hg, ag)
    has_score = pred_score is not None

    target_date = pd.to_datetime(target["Date"], errors="coerce", dayfirst=True)
    date_str = target_date.strftime("%d %B %Y") if pd.notna(target_date) else ""

    # ---------- pre-match evidence (no leakage) ----------
    history = prepare_history(matches, target)
    hh = get_team_history(history, home)
    ah = get_team_history(history, away)

    indicators = [
        i for i in (
            _ind_form(home, away, hh, ah),
            _ind_chances(home, away, hh, ah),
            _ind_venue(home, away, hh, ah),
            _ind_recovery(home, away, hh, ah, target_date),
        ) if i is not None
    ]
    right, missed = _split(code, indicators)

    # head-to-head
    mask = (
        ((history["HomeTeam"] == home) & (history["AwayTeam"] == away))
        | ((history["HomeTeam"] == away) & (history["AwayTeam"] == home))
    )
    h2h = history[mask].sort_values("Date", ascending=False).head(5)

    # ---------- header ----------
    st.markdown(
        '<div class="match-header-top">'
        f'<div class="breadcrumb">{safe(league)} &nbsp;/&nbsp; {safe(date_str)}'
        f' &nbsp;/&nbsp; {safe(season)}</div>'
        '<div class="header-badges">'
        '<span class="badge-pill">Illustrative training scenario</span>'
        '<span class="badge-pill-green">👁 Revealed · learning review</span>'
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

    # ---------- title + result strip ----------
    if actual == "H":
        won = f"{home} won {hg} — {ag}"
    elif actual == "A":
        won = f"{away} won {hg} — {ag}"
    else:
        won = f"Draw {hg} — {ag}"

    score_status = (
        "not submitted" if not has_score
        else "matched" if exact else "not matched"
    )
    res_cls = "good" if correct else "bad"
    res_txt = "Correct" if correct else "Incorrect"

    st.markdown(
        '<div class="ln-tag">REVISIT THE EVIDENCE, NOT JUST THE SCORE</div>'
        '<div class="ln-title">Why was your prediction right or wrong?</div>'
        '<div class="ln-strip">'
        f'<span class="ln-res {res_cls}">{res_txt}</span>'
        f'<span class="ln-strip-t">You predicted '
        f'{safe(_outcome_text(code, home, away))} · {safe(won)} · '
        f'Exact score {score_status}</span></div>',
        unsafe_allow_html=True,
    )

    # ---------- right / missed ----------
    c1, c2 = st.columns(2, gap="large")

    if code == "D":
        right_empty = "No indicator was clearly balanced."
        missed_empty = "No indicator clearly pointed to a winner."
    else:
        right_empty = "No indicator clearly supported your pick."
        missed_empty = "No indicator clearly pointed the other way."

    with c1:
        st.markdown(
            _column_html("WHAT YOU GOT RIGHT ✓", "good", right, "right", right_empty),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            _column_html("WHAT YOU MISSED ⚠️", "warn", missed, "missed", missed_empty),
            unsafe_allow_html=True,
        )

    # ---------- head-to-head strip ----------
    if h2h.empty:
        h2h_t = "No previous meeting in the data"
        h2h_d = ("These two clubs have not met since 2021/22, so there is no "
                 "head-to-head to weigh.")
    else:
        hw = aw = dw = 0
        for _, m in h2h.iterrows():
            if m["HomeTeam"] == home:
                f, a = m["FTHG"], m["FTAG"]
            else:
                f, a = m["FTAG"], m["FTHG"]
            hw += f > a
            aw += f < a
            dw += f == a
        if hw > aw:
            h2h_t = f"Previous meetings favored {home} — but were not a guarantee."
        elif aw > hw:
            h2h_t = f"Previous meetings favored {away} — but were not a guarantee."
        else:
            h2h_t = "Previous meetings were evenly split."
        h2h_d = (f"Previous {len(h2h)}: {home} {int(hw)} wins · "
                 f"{away} {int(aw)} wins · {int(dw)} draws. The selected "
                 "match is excluded. Do not mistake a small historical "
                 "sample for certainty.")

    st.markdown(
        '<div class="ln-h2h"><div class="ln-h2h-i">🕒</div><div>'
        f'<div class="ln-h2h-t">{safe(h2h_t)}</div>'
        f'<div class="ln-h2h-d">{safe(h2h_d)}</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # ---------- key lesson ----------
    st.markdown(
        '<div class="ln-lesson">'
        '<div class="ln-lesson-h">💡 KEY LESSON</div>'
        f'<div class="ln-lesson-t">{safe(_lesson_title(code, right, missed))}</div>'
        '<div class="ln-lesson-d">These are factors to weigh before kickoff, '
        f'not verified causes of the {hg}–{ag} outcome. Indicators support '
        'reasoning rather than deterministically explain causation. '
        'Injuries, line-ups and cup or European fixtures are not in this data.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # ---------- two checks ----------
    st.markdown(
        '<div class="ln-checks">'
        '<div><div class="ln-check-t">Outcome accuracy checks the decision.</div>'
        f'<div class="ln-check-d">{safe(_accuracy_text(correct, exact, has_score))}</div></div>'
        '<div><div class="ln-check-t">Reasoning quality checks the process.</div>'
        f'<div class="ln-check-d">{safe(_reasoning_text(right, missed))}</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------- buttons ----------
    b1, _, b3 = st.columns([1.3, 2.4, 1.5], gap="medium")

    with b1:
        st.button(
            "← Choose another match",
            use_container_width=True,
            on_click=_choose_another,
        )

    with b3:
        st.button(
            "View actual match stats 📊",
            type="primary",
            use_container_width=True,
            on_click=_go_stats,
        )

    st.markdown(
        '<div class="ln-footer">'
        '<span><b>MatchIQ</b> &nbsp;/&nbsp; An independent football learning lab</span>'
        '<span>Study evidence. Make a decision. Learn from the outcome.</span>'
        '</div>',
        unsafe_allow_html=True,
    )