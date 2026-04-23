# S&C Media — AI Strategy Generator

A web app that replaces 20+ hours of manual content research with a
60-second AI-generated strategy package. Produces a Word doc and Excel
spreadsheet ready for client kickoff meetings.

## Quick start (local)

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to the web (free, 5 minutes)

### Step 1 — Push to GitHub
1. Create a free account at github.com
2. Create a new repository (e.g. `sc-media-strategy`)
3. Upload `app.py` and `requirements.txt` to it

### Step 2 — Deploy on Streamlit Community Cloud
1. Go to share.streamlit.io and sign in with GitHub
2. Click **New app**
3. Select your repository and set **Main file path** to `app.py`
4. Click **Deploy**

That's it. Streamlit gives you a public URL (e.g. `yourname-sc-media.streamlit.app`)
you can share with your team and client.

### Step 3 — Get a Groq API key (free)
1. Go to console.groq.com
2. Sign up (free, no credit card)
3. Go to **API Keys** → **Create API key**
4. Paste it into the app's sidebar when prompted

## What it does

1. **Intake Form** — fill in the client's goals, services, audience, and competitors
2. **Generate** — one click produces a full strategy package in ~10 seconds
3. **Results** — preview pillars, post ideas, and KPIs directly in the browser
4. **Download** — grab `Strategy.docx` and `Content_Pillars.xlsx`
5. **Q&A** — ask follow-up questions grounded in the client's documents

## Files

| File | Purpose |
|------|---------|
| `app.py` | The entire web application |
| `requirements.txt` | Python dependencies |

## Notes

- The Groq free tier supports 6,000 requests/day and 14,400 tokens/minute —
  more than enough for demos and small team use.
- Upload PDFs or text files in the sidebar to ground the strategy in real
  research documents (competitor analyses, market reports, etc.).
- The app runs entirely in the browser — no local Python or Ollama needed.
