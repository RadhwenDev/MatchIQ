import pandas as pd
import streamlit as st

from match_context import (
    inject_context_css,
    scroll_to_top,
    prepare_history,
    get_team_history,
    safe,
)
from team_utils import team_logo_html


# =========================================================
# CSS
# =========================================================

PREDICT_CSS = """
<style>
.pd-tag { color:#34d399; font-size:11px; letter-spacing:2px; font-weight:700; }
.pd-title { color:#fff; font-size:44px; font-weight:800; line-height:1.1; margin:6px 0 6px; }
.pd-sub { color:#94a3b8; font-size:18px; margin-bottom:22px; }

.pd-opt { background:#121d28; border:1px solid #1e293b; border-radius:14px;
          padding:20px; min-height:128px; position:relative; margin-bottom:8px; }
.pd-opt.sel { border:1.5px solid #79d1ad; background:rgba(121,209,173,.08); }
.pd-opt-h { color:#64748b; font-size:11px; letter-spacing:1px; font-weight:700; }
.pd-opt-n { color:#fff; font-size:22px; font-weight:700; margin:8px 0 4px; }
.pd-opt-d { color:#94a3b8; font-size:13px; }
.pd-check { position:absolute; top:14px; right:14px; width:24px; height:24px;
            border-radius:50%; background:#79d1ad; color:#0b0f17;
            display:flex; align-items:center; justify-content:center;
            font-weight:800; font-size:14px; }

.pd-card { background:#121d28; border:1px solid #1e293b; border-radius:14px;
           padding:22px; margin-bottom:16px; }
.pd-card-h { display:flex; justify-content:space-between; align-items:center; }
.pd-card-t { color:#fff; font-size:20px; font-weight:700; }
.pd-card-s { color:#64748b; font-size:12px; margin:3px 0 12px; }
.pd-optional { background:#1e293b; color:#94a3b8; font-size:11px;
               padding:3px 10px; border-radius:20px; }

.pd-ok { color:#34d399; font-size:13px; margin-top:6px; }
.pd-bad { color:#f5a0aa; font-size:13px; margin-top:6px; }

.pd-check-item { border-top:1px solid #1b2635; padding:12px 0; }
.pd-check-item:first-of-type { border-top:none; }
.pd-check-t { color:#fff; font-size:14px; font-weight:700; margin-bottom:3px; }
.pd-check-d { color:#94a3b8; font-size:13px; line-height:1.5; }

.pd-lock-note { color:#94a3b8; font-size:12px; line-height:1.5; margin-bottom:10px; }
.pd-summary { color:#fff; font-size:16px; font-weight:700; text-align:center; }
.pd-summary-s { color:#64748b; font-size:12px; text-align:center; margin-top:2px; }

.pd-footer { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
             padding:22px 0; margin-top:40px;
             border-top:1px solid rgba(255,255,255,.1);
             color:#94a3b8; font-size:14px; }
.pd-footer b { color:#fff; font-weight:500; }
.st-key-score_box {
    background: #121d28;
    border-color: #1e293b !important;
    border-radius: 14px;
}

@media (max-width:700px) { .pd-title { font-size:30px; } }
</style>
"""


# =========================================================
# CALLBACKS
# =========================================================

def _set_outcome(idx, code):
    st.session_state[f"pd_outcome_{idx}"] = code


def _lock(idx, code, score):
    st.session_state["prediction"] = code
    st.session_state["predicted_score"] = score
    st.session_state["prediction_locked_for"] = idx


def _go_context():
    st.session_state["analysis_step"] = 2


def _go_reveal():
    st.session_state["analysis_step"] = 4
    st.session_state["scroll_to_top"] = True


# =========================================================
# HELPERS
# =========================================================

def _is_consistent(code, hg, ag):
    if code == "H":
        return hg > ag
    if code == "A":
        return ag > hg
    return hg == ag


def _outcome_label(code):
    return {"H": "HOME WIN", "D": "DRAW", "A": "AWAY WIN"}[code]


def _summary_text(code, home, away, score):
    label = _outcome_label(code)
    if score is not None:
        return f"{label} · {home} {score[0]} — {score[1]} {away}"
    if code == "H":
        return f"{label} · {home}"
    if code == "A":
        return f"{label} · {away}"
    return label


def _record_text(rows):
    w = int((rows["Result"] == "W").sum())
    d = int((rows["Result"] == "D").sum())
    l = int((rows["Result"] == "L").sum())
    return w, d, l, int(rows["Points"].sum())


def _counter_case(code, home, away, home_hist, away_hist):
    """One sentence that challenges the selected outcome."""
    if code is None:
        return "Select an outcome to see the counter-case."

    if code == "H":
        rows = away_hist[away_hist["AwayTeam"] == away].head(5)
        if rows.empty:
            return f"No previous away fixtures found for {away}."
        w, d, l, pts = _record_text(rows)
        return (f"{away} took {pts} points from their last {len(rows)} "
                f"away fixtures: {w}W · {d}D · {l}L.")

    if code == "A":
        rows = home_hist[home_hist["HomeTeam"] == home].head(5)
        if rows.empty:
            return f"No previous home fixtures found for {home}."
        w, d, l, pts = _record_text(rows)
        return (f"{home} took {pts} points from their last {len(rows)} "
                f"home fixtures: {w}W · {d}D · {l}L.")

    h5, a5 = home_hist.head(5), away_hist.head(5)
    hd = int((h5["Result"] == "D").sum()) if not h5.empty else 0
    ad = int((a5["Result"] == "D").sum()) if not a5.empty else 0
    return (f"Draws in the last 5 fixtures: {home} {hd}, {away} {ad}. "
            "Ask whether either side usually finds a winner.")


def _rest_days(team_hist, target_date):
    if team_hist.empty:
        return None
    last = team_hist["Date"].iloc[0]  # sorted newest first
    return int((target_date.normalize() - last.normalize()).days)


def _opt_card(code, header, name, desc, selected):
    check = '<div class="pd-check">✓</div>' if selected else ""
    return (
        f'<div class="pd-opt{" sel" if selected else ""}">'
        f"{check}"
        f'<div class="pd-opt-h">{safe(header)}</div>'
        f'<div class="pd-opt-n">{safe(name)}</div>'
        f'<div class="pd-opt-d">{safe(desc)}</div>'
        "</div>"
    )


# =========================================================
# MAIN PAGE
# =========================================================

def render_match_prediction(matches, selected_index):
    inject_context_css()
    st.markdown(PREDICT_CSS, unsafe_allow_html=True)

    if selected_index is None or selected_index not in matches.index:
        st.warning("Select a match first.")
        return

    idx = int(selected_index)

    # scroll to the top once when arriving on this page
    if st.session_state.get("_pd_scrolled_for") != idx:
        scroll_to_top()
        st.session_state["_pd_scrolled_for"] = idx

    target = matches.loc[idx]
    home = target["HomeTeam"]
    away = target["AwayTeam"]
    league = target.get("League", "La Liga")
    season = target.get("Season", "")

    target_date = pd.to_datetime(target["Date"], errors="coerce", dayfirst=True)
    date_str = target_date.strftime("%d %B %Y") if pd.notna(target_date) else ""

    # ---------- header ----------
    st.markdown(
        '<div class="match-header-top">'
        f'<div class="breadcrumb">{safe(league)} &nbsp;/&nbsp; {safe(date_str)}'
        f' &nbsp;/&nbsp; {safe(season)}</div>'
        '<div class="header-badges">'
        '<span class="badge-pill">Illustrative training scenario</span>'
        '<span class="badge-pill-green">🛡️ Pre-match</span>'
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

    # ---------- already locked ----------
    if st.session_state.get("prediction_locked_for") == idx:
        code = st.session_state.get("prediction")
        score = st.session_state.get("predicted_score")
        st.markdown(
            '<div class="pd-card">'
            '<div class="pd-tag">PREDICTION LOCKED</div>'
            f'<div class="pd-title" style="font-size:30px">'
            f'{safe(_summary_text(code, home, away, score))}</div>'
            '<div class="pd-sub" style="font-size:15px;margin-bottom:0">'
            'This attempt can no longer be changed. '
            'The result is still hidden until you reveal it.</div></div>',
            unsafe_allow_html=True,
        )
        st.button(
            "Reveal the result →",
            type="primary",
            use_container_width=True,
            on_click=_go_reveal,
        )
        return

    # ---------- history for the side checks ----------
    history = prepare_history(matches, target)
    home_hist = get_team_history(history, home)
    away_hist = get_team_history(history, away)

    code = st.session_state.get(f"pd_outcome_{idx}")

    # ---------- title ----------
    st.markdown(
        '<div class="pd-tag">YOUR ANALYSIS. YOUR DECISION.</div>'
        '<div class="pd-title">Think Before The Whistle.</div>'
        '<div class="pd-sub">What do you think will happen?</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1], gap="large")

    # =====================================================
    # LEFT: outcome + exact score
    # =====================================================
    with left:
        options = [
            ("H", "HOME WIN", home, "The home team takes the three points."),
            ("D", "DRAW", "Level at full time",
             "Neither side finds the winning edge."),
            ("A", "AWAY WIN", away, "The visitors take the three points."),
        ]

        cols = st.columns(3, gap="medium")
        for col, (opt_code, header, name, desc) in zip(cols, options):
            with col:
                selected = code == opt_code
                st.markdown(
                    _opt_card(opt_code, header, name, desc, selected),
                    unsafe_allow_html=True,
                )
                st.button(
                    "✓ Selected" if selected else "Select",
                    key=f"pd_btn_{idx}_{opt_code}",
                    type="primary" if selected else "secondary",
                    use_container_width=True,
                    on_click=_set_outcome,
                    args=(idx, opt_code),
                )

        st.write("")

        score = None
        consistent = True

        with st.container(border=True, key="score_box"):
            st.markdown(
                '<div class="pd-card-h"><div class="pd-card-t">'
                'Predict the exact score</div>'
                '<span class="pd-optional">Optional</span></div>'
                '<div class="pd-card-s">A more specific hypothesis. Exact-score '
                'accuracy is tracked separately from outcome accuracy.</div>',
                unsafe_allow_html=True,
            )

            use_score = st.checkbox(
                "I want to predict the exact score",
                key=f"pd_use_score_{idx}",
            )

            if use_score:
                c1, c2 = st.columns(2)
                with c1:
                    hg = st.number_input(
                        f"Home goals · {home}", min_value=0, max_value=20,
                        value=0, step=1, key=f"pd_hg_{idx}",
                    )
                with c2:
                    ag = st.number_input(
                        f"Away goals · {away}", min_value=0, max_value=20,
                        value=0, step=1, key=f"pd_ag_{idx}",
                    )
                score = (int(hg), int(ag))

                if code is None:
                    st.markdown(
                        '<div class="pd-bad">Select an outcome first.</div>',
                        unsafe_allow_html=True,
                    )
                    consistent = False
                elif _is_consistent(code, score[0], score[1]):
                    label = {"H": "Home win", "D": "Draw", "A": "Away win"}[code]
                    st.markdown(
                        '<div class="pd-ok">Your exact score is consistent with '
                        f'your selected outcome: {label}.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<div class="pd-bad">Your exact score does not match '
                        'your selected outcome. Adjust one of them.</div>',
                        unsafe_allow_html=True,
                    )
                    consistent = False

    # =====================================================
    # RIGHT: before you commit
    # =====================================================
    with right:
        hd = _rest_days(home_hist, target_date)
        ad = _rest_days(away_hist, target_date)

        def rest(team, d):
            return f"{team}: not available." if d is None else f"{team}: {d} rest days."

        st.markdown(
            '<div class="pd-card">'
            '<div class="pd-card-t">Before you commit</div>'
            '<div class="pd-card-s">A quick check of your analytical process</div>'
            '<div class="pd-check-item">'
            '<div class="pd-check-t">Consider the counter-case</div>'
            f'<div class="pd-check-d">'
            f'{safe(_counter_case(code, home, away, home_hist, away_hist))}'
            '</div></div>'
            '<div class="pd-check-item">'
            '<div class="pd-check-t">Check the recovery window</div>'
            f'<div class="pd-check-d">{safe(rest(home, hd))} '
            f'{safe(rest(away, ad))}</div></div>'
            '<div class="pd-check-item">'
            '<div class="pd-check-t">Separate evidence from certainty</div>'
            '<div class="pd-check-d">Stronger averages support a view, '
            'not a guaranteed outcome.</div></div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # =====================================================
    # BOTTOM BAR: lock
    # =====================================================
    with st.container(border=True):
        st.markdown(
            '<div class="pd-lock-note"><b style="color:#fff">Locking is '
            'irreversible for this attempt.</b> You cannot change your outcome '
            'or exact score after locking, and the result stays hidden until '
            'you choose to reveal it.</div>',
            unsafe_allow_html=True,
        )

        b1, b2, b3 = st.columns([1.2, 2.6, 1.3], gap="medium")

        with b1:
            st.button(
                "Review pre-match data",
                use_container_width=True,
                on_click=_go_context,
            )

        with b2:
            summary = (
                _summary_text(code, home, away, score)
                if code is not None
                else "No outcome selected yet"
            )
            st.markdown(
                f'<div class="pd-summary">{safe(summary)}</div>'
                '<div class="pd-summary-s">No result or actual-match stats '
                'shown yet.</div>',
                unsafe_allow_html=True,
            )

        with b3:
            st.button(
                "🔒 Lock Prediction",
                type="primary",
                use_container_width=True,
                disabled=(code is None or not consistent),
                on_click=_lock,
                args=(idx, code, score),
            )

    st.markdown(
        '<div class="pd-footer">'
        '<span><b>MatchIQ</b> &nbsp;/&nbsp; An independent football learning lab</span>'
        '<span>Study evidence. Make a decision. Learn from the outcome.</span>'
        '</div>',
        unsafe_allow_html=True,
    )