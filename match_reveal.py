import pandas as pd
import streamlit as st

from match_context import inject_context_css, scroll_to_top, safe
from team_utils import team_logo_html


# =========================================================
# CSS
# =========================================================

REVEAL_CSS = """
<style>
.rv-card { background:#121d28; border:1px solid #1e293b; border-radius:20px;
           padding:34px 40px; margin-bottom:18px; }
.rv-tag { color:#79d1ad; font-size:11px; letter-spacing:2px; font-weight:700;
          text-align:center; }
.rv-title { color:#fff; font-size:40px; font-weight:800; text-align:center;
            margin:6px 0 22px; }
.rv-sides { display:grid; grid-template-columns:1fr 1fr; color:#64748b;
            font-size:11px; letter-spacing:1px; font-weight:700; }
.rv-sides div:last-child { text-align:right; }
.rv-line { display:grid; grid-template-columns:1fr auto 1fr; align-items:center;
           gap:20px; margin:10px 0 22px; }
.rv-team { display:flex; align-items:center; gap:14px; min-width:0; }
.rv-team.r { justify-content:flex-end; }
.rv-team-name { color:#fff; font-size:24px; font-weight:700; }
.rv-team .club-logo, .rv-team .club-fallback { width:56px; height:56px; flex-shrink:0; }
.rv-score { color:#fff; font-size:56px; font-weight:800; text-align:center; }
.rv-pillwrap { text-align:center; margin-bottom:10px; }
.rv-res { display:inline-block; font-size:13px; font-weight:700; padding:6px 16px;
          border-radius:20px; }
.rv-res.good { background:rgba(121,209,173,.14); color:#79d1ad;
               border:1px solid rgba(121,209,173,.4); }
.rv-res.bad { background:rgba(245,160,170,.12); color:#f5a0aa;
              border:1px solid rgba(245,160,170,.4); }
.rv-msg { color:#94a3b8; font-size:14px; text-align:center; margin-bottom:26px; }

.rv-cols { display:grid; grid-template-columns:repeat(3,1fr); gap:24px;
           border-top:1px solid #1b2635; padding-top:22px; }
.rv-col-h { color:#64748b; font-size:11px; letter-spacing:1.2px; font-weight:700;
            margin-bottom:8px; }
.rv-col-v { color:#fff; font-size:17px; font-weight:700; margin-bottom:4px; }
.rv-col-d { color:#94a3b8; font-size:13px; line-height:1.5; }

.rv-lesson { display:flex; gap:16px; background:#1a352f;
             border:1px solid rgba(121,209,173,.25); border-radius:16px;
             padding:22px 26px; margin-bottom:16px; }
.rv-lesson-i { font-size:26px; }
.rv-lesson-t { color:#fff; font-size:17px; font-weight:700; margin-bottom:6px; }
.rv-lesson-d { color:#94a3b8; font-size:14px; line-height:1.6; }
.rv-lesson-n { color:#64748b; font-size:12px; margin-top:10px; }

.rv-side { background:#121d28; border:1px solid #1e293b; border-radius:16px;
           padding:22px; margin-bottom:16px; }
.rv-side-t { color:#fff; font-size:18px; font-weight:700; }
.rv-side-s { color:#64748b; font-size:12px; margin:3px 0 16px; }
.rv-states { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:14px; }
.rv-state { background:#1b2635; color:#64748b; font-size:12px; padding:6px 14px;
            border-radius:20px; border:1px dashed #334155; }
.rv-state.on-good { background:rgba(121,209,173,.14); color:#79d1ad;
                    border:1px solid rgba(121,209,173,.5); }
.rv-state.on-bad { background:rgba(245,160,170,.12); color:#f5a0aa;
                   border:1px solid rgba(245,160,170,.5); }
.rv-side-d { color:#94a3b8; font-size:13px; line-height:1.5; }

.rv-bar-note { color:#94a3b8; font-size:14px; }
.rv-footer { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
             padding:22px 0; margin-top:40px;
             border-top:1px solid rgba(255,255,255,.1);
             color:#94a3b8; font-size:14px; }
.rv-footer b { color:#fff; font-weight:500; }

@media (max-width:700px) {
    .rv-card { padding:22px 18px; }
    .rv-title { font-size:28px; }
    .rv-score { font-size:34px; }
    .rv-team-name { font-size:16px; }
    .rv-team .club-logo, .rv-team .club-fallback { width:40px; height:40px; }
    .rv-cols { grid-template-columns:1fr; gap:18px; }
}
</style>
"""


# =========================================================
# HELPERS
# =========================================================

def _num(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(v) else v


def _outcome_of(hg, ag):
    if hg > ag:
        return "H"
    if ag > hg:
        return "A"
    return "D"


def _outcome_text(code, home, away):
    if code == "H":
        return f"{home} win"
    if code == "A":
        return f"{away} win"
    return "Draw"


def _go_learn():
    st.session_state["analysis_step"] = 5
    st.session_state["scroll_to_top"] = True


def _go_predict():
    st.session_state["analysis_step"] = 3


# =========================================================
# MAIN PAGE
# =========================================================

def render_match_reveal(matches, selected_index):
    inject_context_css()
    st.markdown(REVEAL_CSS, unsafe_allow_html=True)

    if st.session_state.pop("scroll_to_top", False):
        scroll_to_top()

    if selected_index is None or selected_index not in matches.index:
        st.warning("Select a match first.")
        return

    idx = int(selected_index)
    target = matches.loc[idx]
    home = target["HomeTeam"]
    away = target["AwayTeam"]

    hg, ag = _num(target.get("FTHG")), _num(target.get("FTAG"))
    if hg is None or ag is None:
        st.warning("The actual score is unavailable for this fixture.")
        return
    hg, ag = int(hg), int(ag)

    code = st.session_state.get("prediction")
    locked = st.session_state.get("prediction_locked_for") == idx

    if code is None or not locked:
        st.warning("No locked prediction was found for this match.")
        st.button("← Back to Prediction", on_click=_go_predict)
        return

    pred_score = st.session_state.get("predicted_score")

    # ---------- evaluation (two independent checks) ----------
    actual = _outcome_of(hg, ag)
    correct = code == actual
    exact = pred_score is not None and tuple(pred_score) == (hg, ag)

    st.session_state["actual_result"] = actual
    st.session_state["actual_score"] = (hg, ag)

    if pred_score is None:
        score_status = "not submitted"
    elif exact:
        score_status = "matched"
    else:
        score_status = "not matched"

    if correct:
        res_html = '<span class="rv-res good">✔ Correct</span>'
        msg = ("Your outcome matched. Now check whether the reasoning "
               "behind it was sound.")
        lesson_d = ("You called the outcome. A correct call can still come "
                    "from weak reasoning, so look at which signals really "
                    "supported it and which ones you ignored.")
    else:
        res_html = '<span class="rv-res bad">✖ Incorrect</span>'
        msg = ("An unexpected outcome. A useful opportunity to revisit "
               "the evidence.")
        lesson_d = ("You identified some real signals in the pre-match data. "
                    "Now look at the counter-evidence and learn how to weigh "
                    "it more carefully next time.")

    pred_line = (
        f"Predicted score: {home} {pred_score[0]} — {pred_score[1]} {away}"
        if pred_score is not None
        else "No exact score submitted"
    )

    # =====================================================
    # ROW 1: the result card (full width)
    # =====================================================
    st.markdown(
        '<div class="rv-card">'
        '<div class="rv-tag">RESULT REVEALED</div>'
        '<div class="rv-title">Full Time</div>'
        '<div class="rv-sides"><div>HOME TEAM</div><div>AWAY TEAM</div></div>'
        '<div class="rv-line">'
        '<div class="rv-team">'
        f'{team_logo_html(home)}'
        f'<span class="rv-team-name">{safe(home)}</span></div>'
        f'<div class="rv-score">{hg} — {ag}</div>'
        '<div class="rv-team r">'
        f'<span class="rv-team-name">{safe(away)}</span>'
        f'{team_logo_html(away)}</div>'
        '</div>'
        f'<div class="rv-pillwrap">{res_html}</div>'
        f'<div class="rv-msg">{safe(msg)}</div>'
        '<div class="rv-cols">'
        '<div><div class="rv-col-h">YOUR PREDICTION</div>'
        f'<div class="rv-col-v">{safe(_outcome_text(code, home, away))}</div>'
        f'<div class="rv-col-d">{safe(pred_line)}</div></div>'
        '<div><div class="rv-col-h">ACTUAL RESULT</div>'
        f'<div class="rv-col-v">{safe(_outcome_text(actual, home, away))}</div>'
        f'<div class="rv-col-d">Revealed score: {safe(home)} {hg} — {ag} '
        f'{safe(away)}</div></div>'
        '<div><div class="rv-col-h">SEPARATE LEARNING CHECKS</div>'
        f'<div class="rv-col-v">Outcome: {"correct" if correct else "incorrect"}'
        f' / Exact score: {score_status}</div>'
        '<div class="rv-col-d">Reasoning quality: review next, '
        'not scored by luck.</div></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # ROW 2: lesson (left) | feedback states (right)
    # =====================================================
    left, right = st.columns([2.2, 1], gap="large")

    with left:
        st.markdown(
            '<div class="rv-lesson"><div class="rv-lesson-i">💡</div><div>'
            '<div class="rv-lesson-t">A result isn’t the same thing as '
            'good reasoning.</div>'
            f'<div class="rv-lesson-d">{safe(lesson_d)}</div>'
            '<div class="rv-lesson-n">This is a real historical result from '
            'the dataset, shown for learning purposes.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )

    with right:
        c_cls = " on-good" if correct else ""
        e_cls = " on-good" if exact else ""
        i_cls = "" if correct else " on-bad"

        st.markdown(
            '<div class="rv-side">'
            '<div class="rv-side-t">Feedback states</div>'
            '<div class="rv-side-s">Your attempt is highlighted · '
            'the others are inactive examples</div>'
            '<div class="rv-states">'
            f'<span class="rv-state{c_cls}">Correct Prediction</span>'
            f'<span class="rv-state{e_cls}">Exact Score!</span>'
            f'<span class="rv-state{i_cls}">Incorrect</span>'
            '</div>'
            '<div class="rv-side-d">A correct outcome and a matching exact '
            'score are evaluated independently.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    # =====================================================
    # BOTTOM BAR
    # =====================================================
    with st.container(border=True):
        b1, b2 = st.columns([3, 1.4], gap="medium")

        with b1:
            st.markdown(
                '<div class="rv-bar-note">The next step uses pre-match '
                'indicators — not hindsight disguised as certainty.</div>',
                unsafe_allow_html=True,
            )

        with b2:
            st.button(
                "Explore the explanation ➔",
                type="primary",
                use_container_width=True,
                on_click=_go_learn,
            )

    st.markdown(
        '<div class="rv-footer">'
        '<span><b>MatchIQ</b> &nbsp;/&nbsp; An independent football learning lab</span>'
        '<span>Study evidence. Make a decision. Learn from the outcome.</span>'
        '</div>',
        unsafe_allow_html=True,
    )