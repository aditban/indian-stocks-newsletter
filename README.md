
# Indian Stocks Daily Newsletter – Free‑tier Starter Kit

End‑to‑end skeleton that:

* collects email + ticker list (or Zerodha holdings) from a Next.js site
* stores it in Supabase
* scrapes price + news at 08:00 IST daily
* tags sentiment with FinBERT
* emails personalised HTML report through Brevo’s free SMTP

> **Not financial advice.** Use at your own risk.

---

## 1 Prerequisites

| Tool | Free quota |
|------|-----------|
| Supabase (DB + Auth) | 500 MB |
| Brevo (Sendinblue) | 300 e‑mails/day |
| GitHub Actions | 2 000 runner‑minutes/month |
| Zerodha Kite Connect (personal) | ₹0 (read‑only) |

## 2 Setup steps

1.  **Fork** this repo → keep public to stay on free GitHub Actions minutes.
2.  In Supabase → SQL Editor → run `backend/supabase_schema.sql`.
3.  Copy `.env.example` → `.env`, fill keys:
    ```bash
    SUPABASE_URL=
    SUPABASE_KEY=
    BREVO_SMTP_USER=
    BREVO_SMTP_PASS=
    NEWSAPI_KEY=
    ```
4.  Add the same keys as **GitHub repo secrets**.
5.  Deploy the `frontend/` folder on Vercel (or `npm run build && npm run start` locally).
6.  Visit `/` → subscribe yourself → check inbox at 08:00 IST next day.

---

## 3 Folder structure

```
.
├── .github/workflows/daily.yml   # cron job
├── backend
│   ├── requirements.txt
│   ├── send_mail.py
│   └── supabase_schema.sql
└── frontend
    ├── package.json
    ├── next.config.mjs
    ├── pages
    │   ├── index.tsx
    │   └── api
    │       ├── subscribe.ts
    │       └── zerodha_callback.ts
```

Feel free to replace vendors (e.g. NewsData.io ↔ NewsAPI) – everything is decoupled behind env variables.
