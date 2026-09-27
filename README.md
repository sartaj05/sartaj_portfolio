# Sartaj Ahamad — Portfolio

A light, animated portfolio for Sartaj Ahamad, a full-stack developer working with React.js, Django, DRF, Flask, PostgreSQL, MongoDB, AI/ML integrations, and chatbot projects.

## What changed

- A clean light-blue visual system with responsive navigation, animated reveal sections, hover motion, progress meters, project filtering, and an accessible reduced-motion mode.
- A client-focused home page with clear services, proof points, selected work, experience, and calls to action.
- A database-free default mode: the public pages use fallback content from `portfolio/views.py`, so the site can run as a free Render web service without provisioning PostgreSQL.
- Contact form email delivery through SMTP environment variables. Messages are sent to `CONTACT_RECIPIENT`.
- Lightweight honeypot and minimum-time spam protection on the contact form.
- SEO essentials: canonical URLs, Open Graph/Twitter preview metadata, an SVG social preview image, `robots.txt`, and `sitemap.xml`.
- Optional privacy-friendly Plausible analytics, enabled with `PLAUSIBLE_DOMAIN`.
- A custom branded 404 page for production deployments.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver
```

The portfolio is available at `http://127.0.0.1:8000/`.

## Contact email setup

For Gmail, enable 2-Step Verification and create a Google App Password. Do not use your normal Gmail password. Set these environment variables in your local `.env` file or in Render:

```text
EMAIL_HOST_USER=your-gmail-address@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
CONTACT_RECIPIENT=sartaj.ahamad0502@gmail.com
SITE_URL=https://your-domain.example
PLAUSIBLE_DOMAIN=your-domain.example
```

If SMTP variables are missing, the form intentionally reports that email delivery is not configured instead of claiming the message was sent.

`PLAUSIBLE_DOMAIN` is optional. Leave it blank to keep analytics disabled. If enabled, create the site in Plausible and use the exact public hostname, without `https://`.

## Free Render deployment

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint** and select the repository.
3. The included `render.yaml` creates one free web service and no database.
4. Add `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` as secret environment variables in the Render dashboard.
5. Deploy. Render runs `build.sh`, collects static files, and starts Gunicorn.

The free Render service may sleep after inactivity, but it is enough for a portfolio site. A custom domain is optional and is usually paid separately by the domain provider.
