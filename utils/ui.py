import html
import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --cream: #fff7ea;
            --soft-peach: #f7ded2;
            --peach: #f4c7b7;
            --orange: #f26a21;
            --dark-orange: #c94d12;
            --ink: #18120f;
            --muted: #6f625b;
            --line: #d8bfae;
            --card: #fffaf1;
            --white: #ffffff;
            --danger: #a73616;
            --success: #678b48;
            --shadow: rgba(83, 45, 27, 0.12);
        }

        /* ---------- GLOBAL APP BACKGROUND ---------- */
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(242, 106, 33, 0.10), transparent 28%),
                linear-gradient(135deg, #f7ded2 0%, #fff7ea 45%, #f4c7b7 100%);
            color: var(--ink);
        }

        html, body, [class*="css"] {
            font-family: Georgia, "Times New Roman", serif;
        }

        .main .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* ---------- GLOBAL TEXT ---------- */
        h1, h2, h3, h4, h5, h6,
        p, label, span, div {
            color: var(--ink);
        }

        h1 {
            font-size: 3.2rem !important;
            line-height: 1.05 !important;
            font-weight: 400 !important;
            letter-spacing: -1.2px;
            color: var(--ink) !important;
        }

        h2, h3 {
            color: var(--ink) !important;
            font-weight: 500 !important;
        }

        /* ---------- SIDEBAR ---------- */
        [data-testid="stSidebar"] {
            background: #fff7ea !important;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] * {
            color: var(--ink) !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-family: Georgia, "Times New Roman", serif;
        }

        div[role="radiogroup"] label {
            background: transparent !important;
            border-radius: 999px !important;
            padding: 0.45rem 0.7rem !important;
            margin-bottom: 0.2rem !important;
        }

        div[role="radiogroup"] label:hover {
            background: rgba(242, 106, 33, 0.12) !important;
        }

        div[role="radiogroup"] label p {
            color: var(--ink) !important;
        }

        /* ---------- TOP STRIP ---------- */
        .top-strip {
            background: #fffaf1;
            border: 1px solid var(--line);
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: Arial, sans-serif;
            font-size: 0.72rem;
            letter-spacing: 0.18rem;
            text-transform: uppercase;
            box-shadow: 0 10px 30px rgba(83, 45, 27, 0.08);
        }

        .brand-mark {
            font-size: 2rem;
            color: var(--orange) !important;
            font-family: Georgia, "Times New Roman", serif;
            letter-spacing: 0.08rem;
        }

        /* ---------- HERO ---------- */
        .hero-card {
            background: linear-gradient(
                90deg,
                #fff7ea 0%,
                #fffaf1 58%,
                #f26a21 58%,
                #f26a21 100%
            );
            border: 1px solid var(--line);
            box-shadow: 0 22px 45px rgba(83, 45, 27, 0.12);
            border-radius: 2px;
            padding: 2.2rem;
            margin-bottom: 1.4rem;
        }

        .hero-kicker {
            font-family: Arial, sans-serif;
            font-size: 0.68rem;
            letter-spacing: 0.28rem;
            text-transform: uppercase;
            color: var(--muted) !important;
            margin-bottom: 0.8rem;
            font-weight: 700;
        }

        .hero-title {
            font-size: 3.4rem;
            line-height: 1.02;
            color: var(--ink) !important;
            max-width: 760px;
            font-weight: 400;
        }

        .hero-subtitle {
            font-family: Arial, sans-serif;
            font-size: 0.92rem;
            line-height: 1.7;
            color: var(--muted) !important;
            margin-top: 1rem;
            max-width: 720px;
        }

        /* ---------- CARDS ---------- */
        .soft-card {
            background: rgba(255, 250, 241, 0.94);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.4rem;
            box-shadow: 0 14px 35px rgba(83, 45, 27, 0.10);
            margin-bottom: 1rem;
        }

        .metric-card-custom {
            background: #fffaf1;
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.25rem;
            min-height: 124px;
            box-shadow: 0 12px 28px rgba(83, 45, 27, 0.10);
            position: relative;
            overflow: hidden;
        }

        .metric-card-custom::after {
            content: "";
            width: 70px;
            height: 70px;
            background: rgba(242, 106, 33, 0.16);
            position: absolute;
            right: -20px;
            top: -20px;
            border-radius: 999px;
        }

        .metric-label {
            font-family: Arial, sans-serif;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.16rem;
            color: var(--muted) !important;
            margin-bottom: 0.6rem;
        }

        .metric-value-custom {
            font-size: 2rem;
            color: var(--ink) !important;
            line-height: 1.1;
            font-weight: 500;
        }

        .metric-note {
            font-family: Arial, sans-serif;
            font-size: 0.82rem;
            color: var(--muted) !important;
            margin-top: 0.5rem;
        }

        .section-title {
            font-family: Arial, sans-serif;
            font-size: 0.78rem;
            letter-spacing: 0.2rem;
            text-transform: uppercase;
            color: var(--dark-orange) !important;
            font-weight: 800;
            margin: 1.4rem 0 0.8rem 0;
        }

        /* ---------- ALERT CARDS ---------- */
        .alert-card {
            border-radius: 16px;
            padding: 1rem 1.1rem;
            border: 1px solid var(--line);
            background: #fffaf1;
            box-shadow: 0 10px 28px rgba(83, 45, 27, 0.08);
            margin-bottom: 0.8rem;
        }

        .alert-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--ink) !important;
            margin-bottom: 0.35rem;
        }

        .alert-body {
            font-family: Arial, sans-serif;
            color: var(--muted) !important;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .danger {
            border-left: 7px solid #a73616;
        }

        .warning {
            border-left: 7px solid #f26a21;
        }

        .success {
            border-left: 7px solid #678b48;
        }

        .info {
            border-left: 7px solid #9d7d61;
        }

        /* =========================================================
           BUTTON FIX — NORMAL SIZE
        ========================================================= */
        .stButton > button,
        .stFormSubmitButton > button,
        button[kind="primary"],
        button[kind="secondary"] {
            background-color: #18120f !important;
            color: #fff7ea !important;
            border: 1px solid #18120f !important;
            border-radius: 999px !important;

            min-height: 38px !important;
            height: auto !important;
            width: auto !important;
            max-width: 100% !important;

            padding: 0.48rem 1.05rem !important;

            font-family: Arial, sans-serif !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06rem !important;
            text-transform: uppercase !important;

            line-height: 1.1 !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }

        .stButton > button p,
        .stButton > button span,
        .stFormSubmitButton > button p,
        .stFormSubmitButton > button span,
        button[kind="primary"] p,
        button[kind="primary"] span,
        button[kind="secondary"] p,
        button[kind="secondary"] span {
            color: #fff7ea !important;
            font-family: Arial, sans-serif !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06rem !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
            border: 1px solid #f26a21 !important;
            transform: translateY(-1px);
        }

        .stButton > button:hover p,
        .stButton > button:hover span,
        .stFormSubmitButton > button:hover p,
        .stFormSubmitButton > button:hover span,
        button[kind="primary"]:hover p,
        button[kind="primary"]:hover span,
        button[kind="secondary"]:hover p,
        button[kind="secondary"]:hover span {
            color: #fff7ea !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .stButton > button:focus,
        .stFormSubmitButton > button:focus,
        button[kind="primary"]:focus,
        button[kind="secondary"]:focus {
            background-color: #18120f !important;
            color: #fff7ea !important;
            border: 1px solid #18120f !important;
            box-shadow: 0 0 0 3px rgba(242, 106, 33, 0.22) !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: auto !important;
            min-width: 110px !important;
            max-width: 180px !important;
            min-height: 36px !important;
            padding: 0.45rem 1rem !important;
            font-size: 0.76rem !important;
        }

        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            font-size: 0.76rem !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* ---------- DOWNLOAD BUTTON FIX ---------- */
        .stDownloadButton > button {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
            border: 1px solid #f26a21 !important;
            border-radius: 999px !important;

            min-height: 38px !important;
            width: auto !important;
            max-width: 100% !important;

            padding: 0.48rem 1.05rem !important;
            font-family: Arial, sans-serif !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06rem !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
        }

        .stDownloadButton > button p,
        .stDownloadButton > button span {
            color: #fff7ea !important;
            font-family: Arial, sans-serif !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06rem !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .stDownloadButton > button:hover {
            background-color: #18120f !important;
            color: #fff7ea !important;
            border: 1px solid #18120f !important;
        }

        /* =========================================================
           INPUT FIELD FIX — THIS FIXES INVISIBLE CURSOR
        ========================================================= */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            caret-color: #f26a21 !important;
            border: 1px solid #d8bfae !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            caret-color: #f26a21 !important;
            border: 1px solid #f26a21 !important;
            box-shadow: 0 0 0 3px rgba(242, 106, 33, 0.16) !important;
            outline: none !important;
        }

        .stTextInput input::selection,
        .stTextArea textarea::selection,
        .stNumberInput input::selection,
        .stDateInput input::selection {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder,
        .stDateInput input::placeholder {
            color: #8a7668 !important;
        }

        input,
        textarea {
            caret-color: #f26a21 !important;
        }

        /* =========================================================
           SELECTBOX + MULTISELECT FIX
        ========================================================= */
        div[data-baseweb="select"] > div {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            border: 1px solid #d8bfae !important;
            border-radius: 12px !important;
            min-height: 44px !important;
            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:hover {
            border: 1px solid #f26a21 !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #18120f !important;
        }

        div[data-baseweb="select"] input {
            color: #18120f !important;
            caret-color: #f26a21 !important;
        }

        div[data-baseweb="select"] svg {
            color: #18120f !important;
            fill: #18120f !important;
        }

        div[data-baseweb="popover"] {
            background-color: #fffaf1 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        ul[role="listbox"] {
            background-color: #fffaf1 !important;
            border: 1px solid #d8bfae !important;
            border-radius: 12px !important;
        }

        li[role="option"] {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            font-family: Arial, sans-serif !important;
        }

        li[role="option"] * {
            color: #18120f !important;
        }

        li[role="option"]:hover {
            background-color: #f7ded2 !important;
            color: #18120f !important;
        }

        li[aria-selected="true"] {
            background-color: #f4c7b7 !important;
            color: #18120f !important;
        }

        div[data-baseweb="tag"] {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
            border-radius: 999px !important;
        }

        div[data-baseweb="tag"] span {
            color: #fff7ea !important;
        }

        div[data-baseweb="tag"] svg {
            fill: #fff7ea !important;
            color: #fff7ea !important;
        }

        /* =========================================================
           DATE PICKER / CALENDAR FIX
           This fixes the black unreadable calendar popup.
        ========================================================= */

        div[data-baseweb="calendar"],
        div[data-baseweb="calendar"] *,
        div[data-baseweb="calendar"] div {
            font-family: Arial, sans-serif !important;
        }

        div[data-baseweb="calendar"] {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            border: 1px solid #d8bfae !important;
            border-radius: 16px !important;
            box-shadow: 0 18px 45px rgba(83, 45, 27, 0.22) !important;
            overflow: hidden !important;
        }

        div[data-baseweb="calendar"] > div {
            background-color: #fffaf1 !important;
            color: #18120f !important;
        }

        div[data-baseweb="calendar"] button {
            background-color: transparent !important;
            color: #18120f !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 999px !important;
            min-height: 34px !important;
            padding: 0.25rem 0.5rem !important;
            font-family: Arial, sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="calendar"] button:hover {
            background-color: #f7ded2 !important;
            color: #18120f !important;
        }

        div[data-baseweb="calendar"] button[aria-selected="true"],
        div[data-baseweb="calendar"] button[aria-current="date"] {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
        }

        div[data-baseweb="calendar"] button[disabled],
        div[data-baseweb="calendar"] button[aria-disabled="true"] {
            color: #b8a696 !important;
            opacity: 0.55 !important;
        }

        div[data-baseweb="calendar"] svg {
            color: #18120f !important;
            fill: #18120f !important;
        }

        div[data-baseweb="calendar"] [role="gridcell"],
        div[data-baseweb="calendar"] [role="columnheader"],
        div[data-baseweb="calendar"] [role="row"],
        div[data-baseweb="calendar"] [role="grid"],
        div[data-baseweb="calendar"] [role="button"] {
            background-color: #fffaf1 !important;
            color: #18120f !important;
        }

        div[data-baseweb="calendar"] [role="columnheader"] {
            color: #6f625b !important;
            font-weight: 700 !important;
        }

        div[data-baseweb="calendar"] [aria-selected="true"] {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
        }

        div[data-baseweb="calendar"] [aria-selected="true"] * {
            color: #fff7ea !important;
        }

        div[data-baseweb="calendar"] [aria-current="date"] {
            border: 2px solid #f26a21 !important;
        }

        div[data-baseweb="calendar"] [aria-current="date"] * {
            color: #18120f !important;
        }

        div[data-baseweb="calendar"] [aria-selected="true"][aria-current="date"] * {
            color: #fff7ea !important;
        }

        /* Extra fallback for Streamlit/BaseWeb calendar class changes */
        [class*="Calendar"],
        [class*="calendar"] {
            background-color: #fffaf1 !important;
            color: #18120f !important;
        }

        [class*="Calendar"] button,
        [class*="calendar"] button {
            color: #18120f !important;
        }

        [class*="Calendar"] button[aria-selected="true"],
        [class*="calendar"] button[aria-selected="true"] {
            background-color: #f26a21 !important;
            color: #fff7ea !important;
        }

        /* =========================================================
           CHECKBOX FIX
        ========================================================= */
        .stCheckbox label,
        .stCheckbox label span,
        .stCheckbox label p {
            color: #18120f !important;
            font-family: Arial, sans-serif !important;
        }

        /* =========================================================
           TABS FIX
        ========================================================= */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #fffaf1 !important;
            border: 1px solid #d8bfae !important;
            border-radius: 999px !important;
            color: #18120f !important;
            padding: 0.5rem 1rem !important;
            font-family: Arial, sans-serif !important;
            font-weight: 700 !important;
            min-height: 36px !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #18120f !important;
            color: #fff7ea !important;
            border: 1px solid #18120f !important;
        }

        .stTabs [aria-selected="true"] * {
            color: #fff7ea !important;
        }

        /* =========================================================
           EXPANDER FIX
        ========================================================= */
        .streamlit-expanderHeader {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            border-radius: 12px !important;
            border: 1px solid #d8bfae !important;
            font-family: Arial, sans-serif !important;
            font-weight: 700 !important;
        }

        .streamlit-expanderHeader * {
            color: #18120f !important;
        }

        div[data-testid="stExpander"] {
            background-color: rgba(255, 250, 241, 0.74) !important;
            border: 1px solid #d8bfae !important;
            border-radius: 14px !important;
        }

        /* =========================================================
           CONTAINER / FORM FIX
        ========================================================= */
        div[data-testid="stForm"] {
            background-color: rgba(255, 250, 241, 0.80) !important;
            border: 1px solid #d8bfae !important;
            border-radius: 18px !important;
            padding: 1rem !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(255, 250, 241, 0.82) !important;
            border-color: #d8bfae !important;
            border-radius: 18px !important;
        }

        /* =========================================================
           DATAFRAME / TABLE FIX
        ========================================================= */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: #fffaf1 !important;
            border-radius: 16px !important;
            border: 1px solid var(--line) !important;
            overflow: hidden !important;
        }

        [data-testid="stTable"] table {
            background-color: #fffaf1 !important;
            color: #18120f !important;
        }

        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            color: #18120f !important;
            background-color: #fffaf1 !important;
            border-color: #d8bfae !important;
        }

        /* ---------- STREAMLIT ALERTS ---------- */
        div[data-testid="stAlert"] {
            background-color: #fffaf1 !important;
            color: #18120f !important;
            border-radius: 14px !important;
            border: 1px solid #d8bfae !important;
        }

        div[data-testid="stAlert"] * {
            color: #18120f !important;
        }

        /* ---------- HORIZONTAL RULE ---------- */
        hr {
            border-color: var(--line) !important;
        }

        /* ---------- MARKDOWN ---------- */
        .stMarkdown,
        .stMarkdown p,
        .stMarkdown span,
        .stMarkdown li {
            color: #18120f !important;
        }

        /* ---------- CAPTION ---------- */
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] * {
            color: #6f625b !important;
        }

        /* ---------- DEFAULT METRIC FIX ---------- */
        [data-testid="stMetric"] {
            background-color: #fffaf1 !important;
            border: 1px solid #d8bfae !important;
            border-radius: 16px !important;
            padding: 1rem !important;
        }

        [data-testid="stMetric"] * {
            color: #18120f !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def top_bar(
    left="Expense Tracker",
    center="Personal Finance Studio",
    right="Track. Analyze. Control."
):
    st.markdown(
        f"""
        <div class="top-strip">
            <div>{html.escape(str(left))}</div>
            <div class="brand-mark">{html.escape(str(center))}</div>
            <div>{html.escape(str(right))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def page_hero(kicker, title, subtitle=""):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-kicker">{html.escape(str(kicker))}</div>
            <div class="hero-title">{html.escape(str(title))}</div>
            <div class="hero-subtitle">{html.escape(str(subtitle))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title):
    st.markdown(
        f"""<div class="section-title">{html.escape(str(title))}</div>""",
        unsafe_allow_html=True
    )


def metric_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card-custom">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value-custom">{html.escape(str(value))}</div>
            <div class="metric-note">{html.escape(str(note))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def alert_card(title, message, level="info"):
    allowed = {"danger", "warning", "success", "info"}
    level = level if level in allowed else "info"

    st.markdown(
        f"""
        <div class="alert-card {level}">
            <div class="alert-title">{html.escape(str(title))}</div>
            <div class="alert-body">{html.escape(str(message))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )