"""
S&C Media Inc. — AI Strategy Generator (Web App)
=================================================
Streamlit frontend + Groq API backend.
Deploy free at share.streamlit.io
"""

import io
import json
import os
import tempfile
import time
from pathlib import Path

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="S&C Media | AI Strategy Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:   #0D1B2A;
    --steel:  #1B2D40;
    --gold:   #C9A84C;
    --gold2:  #E8C96A;
    --smoke:  #F4F1EC;
    --muted:  #8A9BAD;
    --white:  #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--smoke);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* Top bar */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 2rem;
    background: var(--steel);
    border-bottom: 1px solid rgba(201,168,76,0.3);
    border-radius: 12px;
    margin-bottom: 2rem;
}
.brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--gold);
    letter-spacing: 0.03em;
}
.brand span { color: var(--smoke); }
.tagline {
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Section headers */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.5rem;
}

/* Cards */
.card {
    background: var(--steel);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Streamlit input overrides */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: var(--smoke) !important;
    border-radius: 8px !important;
}
.stTextInput > label, .stTextArea > label,
.stSelectbox > label, .stFileUploader > label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--gold2)) !important;
    color: var(--navy) !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }

/* Secondary button */
.stButton > button {
    background: rgba(255,255,255,0.06) !important;
    color: var(--smoke) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: rgba(201,168,76,0.15) !important;
    color: var(--gold2) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    width: 100% !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px 6px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    background: rgba(201,168,76,0.08) !important;
    border-bottom: 2px solid var(--gold) !important;
}

/* Metric boxes */
.metric-box {
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--gold);
}
.metric-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Alert / info box */
.info-box {
    background: rgba(201,168,76,0.08);
    border-left: 3px solid var(--gold);
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: var(--smoke);
    margin: 0.75rem 0;
}

/* Pillar card */
.pillar-card {
    background: linear-gradient(135deg, rgba(27,45,64,0.9), rgba(13,27,42,0.9));
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
}
.pillar-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--gold);
    margin-bottom: 0.4rem;
}
.pillar-why { font-size: 0.85rem; color: var(--muted); margin-bottom: 0.6rem; }
.post-idea {
    background: rgba(255,255,255,0.04);
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
}
.post-format {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    color: var(--gold2);
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin-right: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--steel) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] .stMarkdown { color: var(--smoke); }

/* Spinner */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* Expander */
.streamlit-expanderHeader {
    color: var(--smoke) !important;
    background: rgba(255,255,255,0.04) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Third-party imports ────────────────────────────────────────────────────────
try:
    from groq import Groq
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from docx import Document as DocxDocument
    from docx.shared import Pt, RGBColor
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError as e:
    st.error(f"Missing dependency: {e}. Run: pip install -r requirements.txt")
    st.stop()

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL       = "llama-3.1-8b-instant"   # Groq's free, fast Llama 3.1
EMBED_MODEL = "all-MiniLM-L6-v2"

SCHEMA_SYSTEM = """You are a senior content strategist at S&C Media Inc.
Replace 20+ hours of manual research with a polished strategy package.

Return ONE valid JSON object matching EXACTLY this schema. No prose outside the JSON:

{
  "strategy_title": "3-6 word positioning title",
  "positioning_summary": "2-3 sentences on how the client shows up online",
  "target_audience": {
    "primary_persona": "One-sentence persona",
    "pain_points": ["3 specific pain points"],
    "questions_they_ask": ["3 questions this audience Googles"]
  },
  "competitor_gaps": ["3 content gaps the client can own, each a full sentence"],
  "content_pillars": [
    {
      "pillar_name": "Short evocative name",
      "why_it_works": "1-2 sentences on why it resonates",
      "keywords": ["4-5 keywords"],
      "post_ideas": [
        {
          "title": "Specific post headline",
          "format": "Reel, Carousel, Static Post, Story, Before/After, or FAQ",
          "hook": "Opening line that stops the scroll",
          "cta": "Call-to-action"
        }
      ]
    }
  ],
  "kpis": ["3 KPIs with concrete targets"]
}

Rules: exactly 3 pillars, exactly 3 post ideas per pillar.
Post titles must reference the client's actual services. Never invent statistics."""


# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "strategy": None,
    "docx_bytes": None,
    "xlsx_bytes": None,
    "qa_history": [],
    "vectorstore": None,
    "client_name": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helper: Groq client ───────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
    )


# ── Helper: build vectorstore from uploaded files ─────────────────────────────
def build_vectorstore(uploaded_files: list) -> "Chroma | None":
    if not uploaded_files:
        return None

    all_docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in uploaded_files:
            path = Path(tmpdir) / f.name
            path.write_bytes(f.read())
            try:
                if f.name.endswith(".pdf"):
                    docs = PyPDFLoader(str(path)).load()
                else:
                    docs = TextLoader(str(path), encoding="utf-8").load()
                all_docs.extend(splitter.split_documents(docs))
            except Exception as e:
                st.warning(f"Could not read {f.name}: {e}")

    if not all_docs:
        return None

    return Chroma.from_documents(all_docs, get_embeddings())


def retrieve_context(store, query: str, k: int = 3) -> str:
    if not store:
        return "(no additional documents provided)"
    docs = store.as_retriever(search_kwargs={"k": k}).invoke(query)
    return "\n\n---\n\n".join(d.page_content for d in docs)


# ── Helper: call Groq ─────────────────────────────────────────────────────────
def call_groq_json(client: Groq, system: str, user: str) -> dict:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.25,
        max_tokens=3000,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)


def call_groq_text(client: Groq, system: str, user: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    return resp.choices[0].message.content.strip()


# ── Renderers ─────────────────────────────────────────────────────────────────
def render_docx(client_name: str, d: dict) -> bytes:
    doc = DocxDocument()

    style = doc.styles["Normal"]
    style.font.name = "Calibri"

    h0 = doc.add_heading(d.get("strategy_title", f"{client_name} Strategy"), 0)
    sub = doc.add_paragraph()
    r = sub.add_run(f"Prepared for {client_name} by S&C Media Inc.")
    r.italic = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_heading("Positioning Summary", 1)
    doc.add_paragraph(d.get("positioning_summary", ""))

    doc.add_heading("Target Audience", 1)
    aud = d.get("target_audience", {})
    doc.add_paragraph(aud.get("primary_persona", ""))

    doc.add_heading("Pain Points", 2)
    for p in aud.get("pain_points", []):
        doc.add_paragraph(p, style="List Bullet")

    doc.add_heading("Questions They're Asking", 2)
    for q in aud.get("questions_they_ask", []):
        doc.add_paragraph(q, style="List Bullet")

    doc.add_heading("Competitor Gaps & Opportunities", 1)
    for g in d.get("competitor_gaps", []):
        doc.add_paragraph(g, style="List Bullet")

    doc.add_heading("Content Pillars", 1)
    for i, pillar in enumerate(d.get("content_pillars", []), 1):
        doc.add_heading(f"Pillar {i}: {pillar.get('pillar_name', '')}", 2)
        doc.add_paragraph(pillar.get("why_it_works", ""))
        kw = doc.add_paragraph()
        kw.add_run("Keywords: ").bold = True
        kw.add_run(", ".join(pillar.get("keywords", [])))
        doc.add_heading("Post Ideas", 3)
        for idea in pillar.get("post_ideas", []):
            p = doc.add_paragraph(style="List Number")
            p.add_run(idea.get("title", "")).bold = True
            p.add_run(f"  [{idea.get('format', '')}]")
            doc.add_paragraph(f"    Hook: {idea.get('hook', '')}")
            doc.add_paragraph(f"    CTA:  {idea.get('cta', '')}")

    doc.add_heading("Success Metrics (KPIs)", 1)
    for k in d.get("kpis", []):
        doc.add_paragraph(k, style="List Bullet")

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def render_xlsx(client_name: str, d: dict) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Content Calendar"

    headers = ["Pillar", "Post #", "Title", "Format", "Hook", "CTA", "Status"]
    ws.append(headers)

    hfill = PatternFill("solid", fgColor="0D1B2A")
    hfont = Font(bold=True, color="C9A84C", size=11)
    thin  = Side(border_style="thin", color="CCCCCC")
    bdr   = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col in range(1, len(headers) + 1):
        c = ws.cell(row=1, column=col)
        c.fill, c.font = hfill, hfont
        c.alignment = Alignment(horizontal="left", vertical="center")
        c.border = bdr

    row = 2
    for pillar in d.get("content_pillars", []):
        for i, idea in enumerate(pillar.get("post_ideas", []), 1):
            ws.append([
                pillar.get("pillar_name", ""),
                i,
                idea.get("title", ""),
                idea.get("format", ""),
                idea.get("hook", ""),
                idea.get("cta", ""),
                "Not started",
            ])
            for col in range(1, len(headers) + 1):
                ws.cell(row=row, column=col).border = bdr
                ws.cell(row=row, column=col).alignment = Alignment(
                    wrap_text=True, vertical="top"
                )
            row += 1

    for i, w in enumerate([22, 8, 48, 14, 50, 30, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"

    ws2 = wb.create_sheet("Pillars Reference")
    ws2.append(["Pillar", "Why It Works", "Keywords"])
    for c in ws2[1]:
        c.fill, c.font = hfill, hfont
    for pillar in d.get("content_pillars", []):
        ws2.append([
            pillar.get("pillar_name", ""),
            pillar.get("why_it_works", ""),
            ", ".join(pillar.get("keywords", [])),
        ])
    for col, w in zip(["A", "B", "C"], [22, 70, 50]):
        ws2.column_dimensions[col].width = w
    for row_cells in ws2.iter_rows(min_row=2):
        for c in row_cells:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
#  UI
# ═══════════════════════════════════════════════════════════════════════════════

# Top bar
st.markdown("""
<div class="top-bar">
    <div>
        <div class="brand">S&C <span>Media</span></div>
        <div class="tagline">AI Content Strategy Generator</div>
    </div>
    <div style="text-align:right;">
        <div class="tagline">Powered by Llama 3.1 · Built for consultants</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at console.groq.com",
    )
    st.markdown("---")
    st.markdown('<div class="section-label">Client Setup</div>', unsafe_allow_html=True)
    client_name = st.text_input("Client Name", placeholder="e.g. VoltEdge Energy Systems")
    uploaded_files = st.file_uploader(
        "Upload research docs (optional)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        help="PDFs, text files, or notes about this client",
    )

    if st.button("Index Documents", use_container_width=True):
        if uploaded_files:
            with st.spinner("Building knowledge base..."):
                st.session_state.vectorstore = build_vectorstore(uploaded_files)
            st.success(f"Indexed {len(uploaded_files)} file(s)")
        else:
            st.info("No files uploaded — will generate from intake only.")

    st.markdown("---")
    st.markdown("""
<div style="font-size:0.72rem; color:#8A9BAD; line-height:1.6;">
<b style="color:#C9A84C;">Free tier limits (Groq)</b><br>
6,000 requests/day<br>
14,400 tokens/minute<br><br>
<b style="color:#C9A84C;">Get your API key</b><br>
console.groq.com → API Keys
</div>
""", unsafe_allow_html=True)

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Intake Form",
    "⚡  Generate Strategy",
    "📊  Results",
    "💬  Q&A",
])

# ─────────────────────────────────────────────────────
# TAB 1 — Intake Form
# ─────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-label">Client Intake</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">Fill this in before generating. '
        'The richer the intake, the sharper the strategy.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        biz_description = st.text_area(
            "What does the business do?",
            height=100,
            placeholder="One paragraph describing the business, its services, and what makes it different.",
        )
        primary_goal = st.text_area(
            "Primary goal for the next 90 days",
            height=80,
            placeholder="e.g. Generate 50 qualified leads for our commercial solar installation service.",
        )
        services = st.text_area(
            "Services / offers to spotlight",
            height=100,
            placeholder="List the specific services, packages, or offers you want content to highlight.",
        )

    with col2:
        ideal_customer = st.text_area(
            "Ideal customer",
            height=100,
            placeholder="Who are they? Age, profession, lifestyle, what do they care about?",
        )
        competitors = st.text_area(
            "Top 3 competitors",
            height=80,
            placeholder="Company names and one line on what they do well / poorly on social.",
        )
        avoid = st.text_area(
            "What NOT to post about",
            height=80,
            placeholder="Topics, tones, or formats to avoid. e.g. 'No price comparisons, no political content.'",
        )

    # Assemble intake text for the prompt
    intake_text = f"""
Business: {client_name}
Description: {biz_description}
Primary Goal: {primary_goal}
Services: {services}
Ideal Customer: {ideal_customer}
Competitors: {competitors}
Avoid: {avoid}
""".strip()

    st.session_state["intake_text"] = intake_text


# ─────────────────────────────────────────────────────
# TAB 2 — Generate
# ─────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-label">Generate Strategy Package</div>', unsafe_allow_html=True)

    if not api_key:
        st.markdown(
            '<div class="info-box">⚠️ Add your Groq API key in the sidebar to continue.</div>',
            unsafe_allow_html=True,
        )
    elif not client_name:
        st.markdown(
            '<div class="info-box">⚠️ Enter a client name in the sidebar to continue.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"""
<div class="card">
    <div class="section-label">Ready to generate</div>
    <div style="font-size:0.9rem; color:#F4F1EC; margin-top:0.4rem;">
        Client: <b>{client_name}</b><br>
        Documents indexed: <b>{"Yes" if st.session_state.vectorstore else "No (intake only)"}</b><br>
        Model: <b>{MODEL} via Groq</b>
    </div>
</div>
""", unsafe_allow_html=True)

        if st.button("⚡ Generate Full Strategy Package", type="primary", use_container_width=True):
            if not st.session_state.get("intake_text", "").strip().replace("Business:", "").strip():
                st.warning("Fill in the intake form first (Tab 1).")
            else:
                client = get_groq_client(api_key)

                with st.status("Generating strategy...", expanded=True) as status:
                    st.write("📚 Retrieving client context...")
                    store = st.session_state.vectorstore
                    ctx_audience    = retrieve_context(store, "target audience pain points")
                    ctx_competitors = retrieve_context(store, "competitor content gaps")
                    ctx_offers      = retrieve_context(store, "services and offers")

                    st.write("🧠 Calling Llama 3.1 on Groq...")
                    user_prompt = f"""
CLIENT INTAKE
=============
{st.session_state['intake_text']}

RETRIEVED CONTEXT — AUDIENCE
============================
{ctx_audience}

RETRIEVED CONTEXT — COMPETITORS
================================
{ctx_competitors}

RETRIEVED CONTEXT — OFFERS
===========================
{ctx_offers}

Generate the JSON strategy package now.
""".strip()

                    try:
                        payload = call_groq_json(client, SCHEMA_SYSTEM, user_prompt)
                        st.session_state.strategy = payload
                        st.session_state["client_name_for_results"] = client_name

                        st.write("📄 Rendering Strategy.docx...")
                        st.session_state.docx_bytes = render_docx(client_name, payload)

                        st.write("📊 Rendering Content_Pillars.xlsx...")
                        st.session_state.xlsx_bytes = render_xlsx(client_name, payload)

                        status.update(label="✅ Strategy package ready!", state="complete")

                    except Exception as e:
                        status.update(label=f"Error: {e}", state="error")
                        st.error(str(e))

        if st.session_state.strategy:
            st.markdown("---")
            st.markdown('<div class="section-label">Download Deliverables</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            safe = client_name.replace(" ", "_")
            with c1:
                st.download_button(
                    "⬇️  Download Strategy.docx",
                    data=st.session_state.docx_bytes,
                    file_name=f"{safe}_Strategy.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            with c2:
                st.download_button(
                    "⬇️  Download Content_Pillars.xlsx",
                    data=st.session_state.xlsx_bytes,
                    file_name=f"{safe}_Content_Pillars.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )


# ─────────────────────────────────────────────────────
# TAB 3 — Results preview
# ─────────────────────────────────────────────────────
with tab3:
    if not st.session_state.strategy:
        st.markdown(
            '<div class="info-box">No strategy generated yet. '
            'Fill in the intake form and click Generate.</div>',
            unsafe_allow_html=True,
        )
    else:
        d = st.session_state.strategy
        cname = st.session_state.get("client_name_for_results", "Client")

        st.markdown(f"""
<div style="margin-bottom:1.5rem;">
    <div style="font-family:'DM Serif Display',serif; font-size:2rem; color:#C9A84C;">
        {d.get('strategy_title', '')}
    </div>
    <div style="font-size:0.88rem; color:#8A9BAD; margin-top:0.3rem;">
        {d.get('positioning_summary', '')}
    </div>
</div>
""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        aud = d.get("target_audience", {})
        pillars = d.get("content_pillars", [])
        total_posts = sum(len(p.get("post_ideas", [])) for p in pillars)

        with col1:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{len(pillars)}</div><div class="metric-label">Content Pillars</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{total_posts}</div><div class="metric-label">Post Ideas</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{len(d.get("kpis", []))}</div><div class="metric-label">KPIs Defined</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Audience
        with st.expander("👤 Target Audience", expanded=True):
            st.markdown(f"**Persona:** {aud.get('primary_persona', '')}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Pain Points**")
                for p in aud.get("pain_points", []):
                    st.markdown(f"- {p}")
            with col2:
                st.markdown("**Questions They're Googling**")
                for q in aud.get("questions_they_ask", []):
                    st.markdown(f"- {q}")

        # Competitor gaps
        with st.expander("🎯 Competitor Gaps"):
            for g in d.get("competitor_gaps", []):
                st.markdown(f"- {g}")

        # Pillars
        st.markdown('<div class="section-label" style="margin-top:1rem;">Content Pillars</div>', unsafe_allow_html=True)
        for i, pillar in enumerate(pillars, 1):
            kws = " · ".join(pillar.get("keywords", []))
            ideas_html = ""
            for idea in pillar.get("post_ideas", []):
                ideas_html += f"""
<div class="post-idea">
    <span class="post-format">{idea.get('format','')}</span>
    <b>{idea.get('title','')}</b><br>
    <span style="color:#8A9BAD; font-size:0.78rem;">
        Hook: {idea.get('hook','')} &nbsp;·&nbsp; CTA: {idea.get('cta','')}
    </span>
</div>"""
            st.markdown(f"""
<div class="pillar-card">
    <div class="pillar-name">Pillar {i} · {pillar.get('pillar_name','')}</div>
    <div class="pillar-why">{pillar.get('why_it_works','')}</div>
    <div style="font-size:0.72rem; color:#C9A84C; margin-bottom:0.6rem;">{kws}</div>
    {ideas_html}
</div>
""", unsafe_allow_html=True)

        # KPIs
        with st.expander("📈 KPIs"):
            for k in d.get("kpis", []):
                st.markdown(f"- {k}")


# ─────────────────────────────────────────────────────
# TAB 4 — Q&A
# ─────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-label">Ask a Question About This Client</div>', unsafe_allow_html=True)

    if not api_key:
        st.markdown('<div class="info-box">⚠️ Add your Groq API key in the sidebar.</div>', unsafe_allow_html=True)
    else:
        # Chat history display
        for msg in st.session_state.qa_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question := st.chat_input("Ask anything about the client or strategy..."):
            st.session_state.qa_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            store = st.session_state.vectorstore
            context = retrieve_context(store, question, k=4)

            strategy_summary = ""
            if st.session_state.strategy:
                d = st.session_state.strategy
                strategy_summary = (
                    f"Strategy title: {d.get('strategy_title','')}\n"
                    f"Positioning: {d.get('positioning_summary','')}\n"
                    f"Pillars: {', '.join(p.get('pillar_name','') for p in d.get('content_pillars',[]))}"
                )

            system = (
                "You are a senior strategist at S&C Media Inc. "
                "Answer using ONLY the context and strategy provided. "
                "If the answer isn't in the context, say so plainly — never invent details."
            )
            user = (
                f"Client: {client_name}\n\n"
                f"Strategy Summary:\n{strategy_summary}\n\n"
                f"Retrieved Context:\n{context}\n\n"
                f"Question: {question}"
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    client_groq = get_groq_client(api_key)
                    answer = call_groq_text(client_groq, system, user)
                st.markdown(answer)
                st.session_state.qa_history.append({"role": "assistant", "content": answer})
