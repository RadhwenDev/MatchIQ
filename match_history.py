import streamlit as st

from match_context import inject_context_css, scroll_to_top, safe
from match_learn import _choose_another


# =========================================================
# STORAGE (session only)
# =========================================================

def record_attempt(attempt_id, idx, home, away, date_str, season, league,
                   pred, pred_score, actual, actual_score):
    """Save one completed attempt. Called once, when the result is revealed."""
    if attempt_id is None:
        return

    history = st.session_state.setdefault("history", [])
    if any(h["attempt"] == attempt_id for h in history):
        return

    history.append({
        "attempt": attempt_id,
        "idx": int(idx),
        "home": str(home),
        "away": str(away),
        "date": str(date_str),
        "season": str(season),
        "league": str(league),
        "pred": pred,
        "pred_score": tuple(pred_score) if pred_score is not None else None,
        "actual": actual,
        "actual_score": tuple(actual_score),
        "correct": pred == actual,
        "exact": pred_score is not None and tuple(pred_score) == tuple(actual_score),
    })


# =========================================================
# CSS
# =========================================================

HISTORY_CSS = """
<style>
.hs-top { display:flex; justify-content:space-between; align-items:flex-start;
          flex-wrap:wrap; gap:16px; margin-bottom:22px; }
.hs-tag { color:#79d1ad; font-size:12px; letter-spacing:1.5px; font-weight:600; }
.hs-title { color:#fff; font-size:48px; font-weight:400; line-height:1.1; margin:10px 0 12px; }
.hs-sub { color:#94a3b8; font-size:17px; }
.hs-pillbox { text-align:right; }
.hs-pill { display:inline-block; background:#1e293b; color:#cbd5e1; font-size:13px;
           font-weight:600; padding:8px 16px; border-radius:20px; }
.hs-pill-s { color:#94a3b8; font-size:12px; margin-top:10px; }

.hs-stats { display:grid; grid-template-columns:repeat(5,1fr); gap:20px; margin-bottom:22px; }
.hs-stat { background:#121d28; border:1px solid #263545; border-radius:18px; padding:26px 28px; }
.hs-stat-l { color:#cbd5e1; font-size:16px; }
.hs-stat-v { color:#fff; font-size:48px; font-weight:400; margin:14px 0 18px; line-height:1; }
.hs-stat-v.g { color:#79d1ad; }
.hs-stat-d { color:#94a3b8; font-size:13px; }

.hs-card { background:#121d28; border:1px solid #1e293b; border-radius:18px;
           padding:28px 30px; margin-bottom:16px; }
.hs-card.green { background:#14352d; border-color:rgba(121,209,173,.45); }
.hs-card-t { color:#fff; font-size:22px; font-weight:700; }
.hs-card-s { color:#94a3b8; font-size:14px; margin:6px 0 18px; }
.hs-foot { color:#94a3b8; font-size:13px; border-top:1px solid #1b2635;
           padding-top:16px; margin-top:6px; line-height:1.5; }

.hs-big { display:flex; align-items:baseline; gap:16px; margin:26px 0 22px; }
.hs-big-v { color:#fff; font-size:72px; font-weight:700; line-height:1; }
.hs-big-l { color:#cbd5e1; font-size:18px; }
.hs-split { display:flex; gap:3px; height:20px; margin-bottom:22px; }
.hs-split .c { background:#79d1ad; border-radius:6px; }
.hs-split .i { background:#8093b0; border-radius:6px; }
.hs-cnt { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }
.hs-cnt-l { color:#cbd5e1; font-size:15px; }
.hs-cnt-v { color:#fff; font-size:32px; font-weight:600; margin-top:6px; }
.hs-dot { display:inline-block; width:9px; height:9px; border-radius:3px; margin-right:8px; }
.hs-dot.c { background:#79d1ad; }
.hs-dot.i { background:#8093b0; }
.hs-note { color:#94a3b8; font-size:14px; line-height:1.6; }

.hs-type { display:grid; grid-template-columns:110px 1fr 70px 70px; align-items:center;
           gap:16px; margin:16px 0; }
.hs-type-n { color:#fff; font-size:17px; }
.hs-track { height:6px; background:#1b2635; border-radius:6px; }
.hs-fill { height:100%; background:#79d1ad; border-radius:6px; }
.hs-type-c { color:#94a3b8; font-size:15px; }
.hs-type-p { color:#fff; font-size:15px; font-weight:700; text-align:right; }

.hs-focus-h { color:#fff; font-size:20px; font-weight:700; margin-bottom:22px; }
.hs-focus-t { color:#fff; font-size:26px; font-weight:400; margin-bottom:18px; }
.hs-focus-d { color:#cbd5e1; font-size:15px; line-height:1.65; margin-bottom:24px; }
.hs-focus-f { color:#94a3b8; font-size:13px; }

.hs-levels { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin:20px 0 26px; }
.hs-level { background:#0f1822; border:1px solid #263545; border-radius:12px; padding:22px; }
.hs-level.cur { background:#14352d; border-color:rgba(121,209,173,.6); }
.hs-level-s { color:#94a3b8; font-size:12px; }
.hs-level-n { color:#fff; font-size:22px; font-weight:700; margin:10px 0 8px; }
.hs-level-d { color:#94a3b8; font-size:13px; }
.hs-prog { display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:30px; }
.hs-prog-l, .hs-prog-r { color:#94a3b8; font-size:14px; }
.hs-prog-bar { height:6px; background:#1b2635; border-radius:6px; }
.hs-prog-fill { height:100%; background:#79d1ad; border-radius:6px; }

.hs-empty { background:#121d28; border:1px dashed #334155; border-radius:18px;
            padding:50px 30px; text-align:center; margin-bottom:20px; }
.hs-empty-t { color:#fff; font-size:22px; font-weight:700; margin-bottom:8px; }
.hs-empty-d { color:#94a3b8; font-size:15px; }

.hs-bottom-t { color:#94a3b8; font-size:15px; padding-top:8px; }
.hs-footer { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
             padding:22px 0; margin-top:40px;
             border-top:1px solid rgba(255,255,255,.1);
             color:#94a3b8; font-size:14px; }
.hs-footer b { color:#fff; font-weight:500; }

@media (max-width:900px) {
    .hs-stats { grid-template-columns:repeat(2,1fr); }
    .hs-levels { grid-template-columns:1fr 1fr; }
    .hs-prog { grid-template-columns:1fr; gap:10px; }
    .hs-title { font-size:34px; }
}
</style>
"""


# =========================================================
# CALLBACKS
# =========================================================

def _close_history():
    st.session_state["view"] = None
    st.session_state["scroll_to_top"] = True


def _new_match():
    _choose_another()
    st.session_state["view"] = None


# =========================================================
# CALCULATIONS
# =========================================================

LEVELS = [
    ("Beginner", "Build the habit", 0, 0),
    ("Analyst", "10 attempts", 10, 0),
    ("Advanced Analyst", "50 attempts + 70% accuracy", 50, 70),
    ("Elite Analyst", "100 attempts + 80% accuracy", 100, 80),
]

TYPE_LABELS = {"H": "Home win", "D": "Draw", "A": "Away win"}
TYPE_PLURAL = {"H": "Home wins", "D": "Draws", "A": "Away wins"}

FOCUS = {
    "D": ("Spot the case for a draw.",
          "Practice identifying balanced chance creation, low-scoring form "
          "and strong defensive venue records."),
    "H": ("Test the home-win assumption.",
          "Practice checking whether the home advantage is real: compare "
          "venue form and recovery time before trusting reputation."),
    "A": ("Back the visitors with evidence.",
          "Practice weighing away form and defensive venue records against "
          "the pull of home advantage."),
}


def _pct(p):
    s = f"{p:.1f}"
    return (s[:-2] if s.endswith(".0") else s) + "%"


def _streak(history):
    streak = 0
    for h in reversed(history):
        if h["correct"]:
            streak += 1
        else:
            break
    return streak


def _checkpoints(history):
    n = len(history)
    step = max(1, n // 5)
    ks = list(range(step, n + 1, step))
    if ks[-1] != n:
        ks.append(n)
    return [(k, sum(1 for h in history[:k] if h["correct"])) for k in ks]


def _by_type(history):
    rows = []
    for code in ("H", "D", "A"):
        items = [h for h in history if h["pred"] == code]
        if items:
            c = sum(1 for h in items if h["correct"])
            rows.append((code, c, len(items), c / len(items) * 100))
    rows.sort(key=lambda r: (r[3], -r[2]))
    return rows


def _level_index(n, acc):
    cur = 0
    for i, (_, _, att, acc_min) in enumerate(LEVELS):
        if n >= att and acc >= acc_min:
            cur = i
    return cur


# =========================================================
# HTML BUILDERS
# =========================================================

def _chart_svg(cps):
    w, h = 800, 320
    left, right, top, bottom = 56, 770, 20, 260
    x0, x1 = left + 40, right - 40

    kmin, kmax = cps[0][0], cps[-1][0]

    def X(k):
        if kmax == kmin:
            return (x0 + x1) / 2
        return x0 + (k - kmin) / (kmax - kmin) * (x1 - x0)

    def Y(p):
        return bottom - (p / 100) * (bottom - top)

    pts = [(X(k), Y(c / k * 100), c / k * 100) for k, c in cps]

    svg = [f'<svg viewBox="0 0 {w} {h}" width="100%" '
           'xmlns="http://www.w3.org/2000/svg" role="img" '
           'aria-label="Prediction accuracy over time">']

    for p in (0, 25, 50, 75, 100):
        y = Y(p)
        svg.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" '
                   'stroke="#1b2635" stroke-width="1"/>')
        svg.append(f'<text x="{left - 10}" y="{y + 4:.1f}" fill="#64748b" '
                   f'font-size="12" text-anchor="end">{p}%</text>')

    area = f"{pts[0][0]:.1f},{bottom} " + " ".join(
        f"{x:.1f},{y:.1f}" for x, y, _ in pts) + f" {pts[-1][0]:.1f},{bottom}"
    svg.append(f'<polygon points="{area}" fill="rgba(111,211,168,0.08)"/>')

    line = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)
    svg.append(f'<polyline points="{line}" fill="none" stroke="#6fd3a8" '
               'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')

    for x, y, _ in pts:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#6fd3a8"/>')

    for k, _ in cps:
        svg.append(f'<text x="{X(k):.1f}" y="{bottom + 22}" fill="#64748b" '
                   f'font-size="12" text-anchor="middle">{k}</text>')

    lx, ly, lp = pts[-1]
    bx = min(max(lx - 26, left), right - 52)
    svg.append(f'<rect x="{bx:.1f}" y="{ly - 40:.1f}" width="52" height="24" rx="6" '
               'fill="rgba(111,211,168,0.15)" stroke="rgba(111,211,168,0.4)"/>')
    svg.append(f'<text x="{bx + 26:.1f}" y="{ly - 23:.1f}" fill="#6fd3a8" '
               f'font-size="13" font-weight="700" text-anchor="middle">'
               f'{lp:.0f}%</text>')

    svg.append(f'<text x="{(left + right) / 2}" y="{h - 8}" fill="#64748b" '
               'font-size="12" text-anchor="middle">Completed predictions · '
               'cumulative outcome accuracy</text>')
    svg.append("</svg>")
    return "".join(svg)


def _stat(label, value, desc, green=False):
    cls = " g" if green else ""
    return (
        '<div class="hs-stat">'
        f'<div class="hs-stat-l">{safe(label)}</div>'
        f'<div class="hs-stat-v{cls}">{safe(value)}</div>'
        f'<div class="hs-stat-d">{safe(desc)}</div></div>'
    )


# =========================================================
# MAIN PAGE
# =========================================================

def render_match_history():
    inject_context_css()
    st.markdown(HISTORY_CSS, unsafe_allow_html=True)

    if st.session_state.pop("scroll_to_top", False):
        scroll_to_top()

    history = st.session_state.get("history", [])
    n = len(history)

    # ---------- header ----------
    st.markdown(
        '<div class="hs-top"><div>'
        '<div class="hs-tag">PERFORMANCE / LEARNING</div>'
        '<div class="hs-title">Your analyst journey</div>'
        '<div class="hs-sub">Build better judgment one match at a time. '
        'Measure decisions, not financial outcomes.</div></div>'
        '<div class="hs-pillbox"><span class="hs-pill">Saved for this session</span>'
        '<div class="hs-pill-s">Your learning record · kept until you close '
        'or refresh the page</div></div></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("match_selection_confirmed"):
        st.button("← Back to my match", on_click=_close_history)

    # ---------- empty state ----------
    if n == 0:
        st.markdown(
            '<div class="hs-empty">'
            '<div class="hs-empty-t">No completed attempts yet</div>'
            '<div class="hs-empty-d">Lock a prediction and reveal the result. '
            'Your first attempt will appear here.</div></div>',
            unsafe_allow_html=True,
        )
        st.button("Choose a match →", type="primary", on_click=_new_match)
        return

    correct = sum(1 for h in history if h["correct"])
    exact = sum(1 for h in history if h["exact"])
    acc = correct / n * 100
    streak = _streak(history)

    # ---------- stat cards ----------
    st.markdown(
        '<div class="hs-stats">'
        + _stat("Predictions", n, "Completed learning attempts")
        + _stat("Correct", correct, "Correct match outcomes")
        + _stat("Accuracy", f"{acc:.0f}%", f"{correct} correct out of {n}", green=True)
        + _stat("Exact Scores", exact, "A separate accuracy measure")
        + _stat("Current Streak", streak, "Consecutive correct outcomes")
        + '</div>',
        unsafe_allow_html=True,
    )

    # ---------- chart | correct vs incorrect ----------
    c1, c2 = st.columns([1.5, 1], gap="large")

    with c1:
        if n >= 2:
            cps = _checkpoints(history)
            chart = _chart_svg(cps)
            foot = ("Checkpoints: "
                    + " · ".join(f"{c}/{k}" for k, c in cps)
                    + f" correct. A small sample, not a measure of certainty.")
            sub = f"Outcome accuracy · {len(cps)} completed-prediction checkpoints"
        else:
            chart = ('<div class="hs-note" style="padding:60px 0;text-align:center">'
                     'Complete a second prediction to see your trend.</div>')
            foot = "A single attempt is not a trend."
            sub = "Outcome accuracy · cumulative"

        st.markdown(
            '<div class="hs-card">'
            '<div class="hs-card-t">Prediction accuracy over time</div>'
            f'<div class="hs-card-s">{safe(sub)}</div>'
            f'{chart}<div class="hs-foot">{safe(foot)}</div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        inc = n - correct
        note = (f"{exact} exact-score match{'es are' if exact != 1 else ' is'} "
                f"included within the {correct} correct outcomes, not added to them.")
        st.markdown(
            '<div class="hs-card">'
            '<div class="hs-card-t">Correct vs incorrect</div>'
            f'<div class="hs-card-s">{n} completed predictions · outcomes only</div>'
            '<div class="hs-big">'
            f'<span class="hs-big-v">{acc:.0f}%</span>'
            '<span class="hs-big-l">correct outcomes</span></div>'
            '<div class="hs-split">'
            f'<div class="c" style="flex:{correct}"></div>'
            f'<div class="i" style="flex:{inc}"></div></div>'
            '<div class="hs-cnt">'
            '<div><div class="hs-cnt-l"><i class="hs-dot c"></i>Correct</div>'
            f'<div class="hs-cnt-v">{correct}</div></div>'
            '<div><div class="hs-cnt-l"><i class="hs-dot i"></i>Incorrect</div>'
            f'<div class="hs-cnt-v">{inc}</div></div></div>'
            f'<div class="hs-note">{safe(note)}</div></div>',
            unsafe_allow_html=True,
        )

    # ---------- difficult types | practice focus ----------
    types = _by_type(history)
    d1, d2 = st.columns([1.5, 1], gap="large")

    with d1:
        rows = "".join(
            '<div class="hs-type">'
            f'<div class="hs-type-n">{TYPE_LABELS[code]}</div>'
            f'<div class="hs-track"><div class="hs-fill" style="width:{p:.0f}%"></div></div>'
            f'<div class="hs-type-c">{c} / {t}</div>'
            f'<div class="hs-type-p">{_pct(p)}</div></div>'
            for code, c, t, p in types
        )
        st.markdown(
            '<div class="hs-card">'
            '<div class="hs-card-t">Most difficult prediction types</div>'
            '<div class="hs-card-s">Grouped by the outcome you predicted · '
            'ranked from lowest accuracy</div>'
            f'{rows}'
            '<div class="hs-note" style="font-size:13px">Correct / attempts · '
            f'totals: {correct} / {n} · small categories can fluctuate '
            'sharply.</div></div>',
            unsafe_allow_html=True,
        )

    with d2:
        code, c, t, p = types[0]
        if p >= 100:
            f_title = "Keep challenging yourself."
            f_text = ("Every prediction type has gone well so far. Keep "
                      "checking the counter-case before you lock.")
        else:
            f_title, tip = FOCUS[code]
            f_text = (f"{TYPE_PLURAL[code]} are your most difficult type: "
                      f"{c} correct from {t}. {tip}")
        st.markdown(
            '<div class="hs-card green">'
            '<div class="hs-focus-h">◎ &nbsp;Your next practice focus</div>'
            f'<div class="hs-focus-t">{safe(f_title)}</div>'
            f'<div class="hs-focus-d">{safe(f_text)}</div>'
            '<div class="hs-focus-f">Better reasoning first. Accuracy follows '
            'over time.</div></div>',
            unsafe_allow_html=True,
        )

    # ---------- analyst profile ----------
    cur = _level_index(n, acc)
    cards = ""
    for i, (name, req, _, _) in enumerate(LEVELS):
        if i < cur:
            status, desc = "Completed", req
        elif i == cur:
            status, desc = "Current", "Your current level"
        elif i == cur + 1:
            status, desc = "Next milestone", req
        else:
            status, desc = "Future milestone", req
        cls = " cur" if i == cur else ""
        cards += (
            f'<div class="hs-level{cls}">'
            f'<div class="hs-level-s">{status}</div>'
            f'<div class="hs-level-n">{safe(name)}</div>'
            f'<div class="hs-level-d">{safe(desc)}</div></div>'
        )

    if cur < len(LEVELS) - 1:
        _, _, next_att, next_acc = LEVELS[cur + 1]
        prog = min(n / next_att, 1) * 100
        left_txt = f"{n} / {next_att} attempts toward your next profile review"
        right_txt = (f"Accuracy: {acc:.0f}% / {next_acc}% target · no betting results"
                     if next_acc else f"Accuracy: {acc:.0f}% · no betting results")
    else:
        prog = 100
        left_txt = "Top level reached"
        right_txt = f"Accuracy: {acc:.0f}% · no betting results"

    st.markdown(
        '<div class="hs-card">'
        '<div class="hs-card-t">Analyst Profile</div>'
        '<div class="hs-card-s">Progression is based only on prediction and '
        'analytical performance</div>'
        f'<div class="hs-levels">{cards}</div>'
        '<div class="hs-prog">'
        f'<div class="hs-prog-l">{safe(left_txt)}</div>'
        f'<div class="hs-prog-bar"><div class="hs-prog-fill" style="width:{prog:.0f}%"></div></div>'
        f'<div class="hs-prog-r">{safe(right_txt)}</div></div></div>',
        unsafe_allow_html=True,
    )

    # ---------- bottom ----------
    b1, b2 = st.columns([4, 1.3], gap="medium")
    with b1:
        st.markdown(
            '<div class="hs-bottom-t">Your record is kept for this session. '
            'The core training journey continues with your next match.</div>',
            unsafe_allow_html=True,
        )
    with b2:
        st.button(
            "Choose another match →",
            type="primary",
            use_container_width=True,
            on_click=_new_match,
        )

    st.markdown(
        '<div class="hs-footer">'
        '<span><b>MatchIQ</b> &nbsp;/&nbsp; An independent football learning lab</span>'
        '<span>Study evidence. Make a decision. Learn from the outcome.</span>'
        '</div>',
        unsafe_allow_html=True,
    )