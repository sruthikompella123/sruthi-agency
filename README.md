# Sruthi Agency – Agentic AI Property Advisor

## How to Run

### Step 1 — Add your API key
Open `.env` and replace `your_api_key_here` with your key from console.anthropic.com:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx
```

### Step 2 — Install dependencies
```bash
pip3 install -r requirements.txt
```

### Step 3 — Run the server
```bash
python3 main.py
```

### Step 4 — Open in browser
Go to: http://localhost:8000

---

## Project Structure
```
sruthi-python/
├── main.py                          ← Run this to start the server
├── requirements.txt                 ← Python packages
├── .env                             ← Your API key
├── agents/
│   └── property_advisor_agent.py   ← Agentic AI loop
├── tools/
│   └── property_tools.py           ← 4 agentic tools
└── frontend/
    └── index.html                  ← Chat UI
```
