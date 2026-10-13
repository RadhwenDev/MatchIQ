import streamlit as st


# =========================================================
# CSS
# =========================================================

NAV_CSS = """
<style>
.nb-brand { display:flex; align-items:center; gap:14px; }
.nb-logo { width:48px; height:48px; border-radius:12px; background:#12332b;
           border:1px solid #1f5a49; display:flex; align-items:center;
           justify-content:center; flex-shrink:0; }
.nb-name { color:#fff; font-size:26px; font-weight:400; line-height:1.1; }
.nb-name b { color:#79d1ad; font-weight:400; }
.nb-tag { color:#94a3b8; font-size:11px; letter-spacing:.3px; margin-top:2px; }
.nb-right { display:flex; align-items:center; justify-content:flex-end; gap:10px;
            color:#94a3b8; font-size:15px; }
.nb-line { border-bottom:1px solid #1b2635; margin:6px 0 26px; }

/* nav buttons look like text links */
[class*="st-key-nav_"] button {
    background:transparent !important;
    border:none !important;
    border-bottom:2px solid transparent !important;
    border-radius:0 !important;
    box-shadow:none !important;
    padding:6px 4px !important;
    min-height:0 !important;
}
[class*="st-key-nav_"] button p {
    color:#94a3b8 !important;
    font-size:17px !important;
    font-weight:600 !important;
}
[class*="st-key-nav_"] button:hover p { color:#ffffff !important; }

@media (max-width:700px) {
    .nb-tag, .nb-right { display:none; }
}
</style>
"""

LOGO_SVG = (
    '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<rect x="3" y="15" width="3" height="8" rx="1" fill="#79d1ad"/>'
    '<rect x="8" y="12" width="3" height="11" rx="1" fill="#79d1ad"/>'
    '<rect x="13" y="14" width="3" height="9" rx="1" fill="#79d1ad"/>'
    '<rect x="18" y="9" width="3" height="14" rx="1" fill="#79d1ad"/>'
    '<path d="M3 11 L9 6 L14 9 L22 2" stroke="#79d1ad" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


# =========================================================
# CALLBACKS
# =========================================================

def _go(view):
    st.session_state["view"] = view
    if view is not None:
        st.session_state["scroll_to_top"] = True


# =========================================================
# NAVBAR
# =========================================================

def render_navbar(active):
    """active: None (Play), "history" or "about"."""
    active_key = {"history": "nav_history", "about": "nav_about"}.get(
        active, "nav_play"
    )

    st.markdown(
        NAV_CSS
        + "<style>"
        f".st-key-{active_key} button {{ border-bottom:2px solid #79d1ad !important; }}"
        f".st-key-{active_key} button p {{ color:#ffffff !important; }}"
        "</style>",
        unsafe_allow_html=True,
    )

    brand, nav, tag = st.columns([2.2, 3, 2.2], vertical_alignment="center")

    with brand:
        st.markdown(
            '<div class="nb-brand">'
            f'<div class="nb-logo">{LOGO_SVG}</div>'
            '<div><div class="nb-name">Match<b>IQ</b></div>'
            '<div class="nb-tag">Think Before the Whistle.</div></div></div>',
            unsafe_allow_html=True,
        )

    with nav:
        _, c1, c2, c3, _ = st.columns([0.6, 1, 1, 1, 0.6], gap="small")
        with c1:
            st.button("Play", key="nav_play", on_click=_go, args=(None,))
        with c2:
            st.button("History", key="nav_history", on_click=_go, args=("history",))
        with c3:
            st.button("About", key="nav_about", on_click=_go, args=("about",))

    with tag:
        st.markdown(
            '<div class="nb-right"><span>🎓</span>'
            '<span>Football intelligence, not betting</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="nb-line"></div>', unsafe_allow_html=True)


# =========================================================
# ABOUT PAGE (simple)
# =========================================================

def render_about():
    st.markdown(
        """
        <div style="max-width:820px;margin:10px auto 40px;">
        <div style="color:#79d1ad;font-size:12px;letter-spacing:1.5px;font-weight:600;">
        ABOUT</div>
        <div style="color:#fff;font-size:44px;line-height:1.1;margin:10px 0 16px;">
        An independent football learning lab</div>
        <div style="color:#94a3b8;font-size:17px;line-height:1.7;">
        MatchIQ trains the way you reason about football. You study the
        information available before kickoff, commit to a prediction, then
        discover what really happened and why.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 3, 1])

    with mid:
        st.markdown("##### How it works")
        st.markdown(
            "1. **Select a match** from La Liga 2022/23 to 2025/26.\n"
            "2. **Study the context**: form, venue record, league table, "
            "recovery and head-to-head, using only data from before kickoff.\n"
            "3. **Predict** the outcome, and optionally the exact score.\n"
            "4. **Reveal** the result. Outcome and exact score are checked "
            "separately.\n"
            "5. **Learn**: see what you got right, what you missed, and the "
            "actual match statistics."
        )

        st.markdown("##### The data")
        st.markdown(
            "Match results and statistics come from football-data.co.uk. "
            "Segunda División and the 2021/22 season are used only as "
            "history, so promoted teams still have form to show. "
            "Everything shown before your prediction is computed from "
            "matches played strictly before that date."
        )

        st.markdown("##### What it is not")
        st.markdown(
            "- Not a betting tool and not a tipster. It measures decisions, "
            "not financial outcomes.\n"
            "- Not a complete picture: injuries, line-ups, and cup or "
            "European fixtures are not in the data.\n"
            "- Not certainty. Indicators support reasoning; they do not "
            "explain causes."
        )