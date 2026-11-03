# hafeezoyeneyin.com

Portfolio site for Hafeez Oyeneyin Web Design & Development (a service of Oyeneyin Solutions LLC).
Plain HTML/CSS/JS, hosted on GitHub Pages. No build step is needed to host it; the Python script only regenerates pages.

```
index.html, work.html, services.html, about.html, contact.html, 404.html
work-<project>.html     one case study per project
assets/site.css         all styles
assets/site.js          all behavior (form endpoint + headline words at the top)
tools/build.py          source of truth: CONFIG + PROJECTS data and page templates
```

## Editing content

Pages are generated. Change text in `tools/build.py`, then run:

```
python tools/build.py
```

- **Email / phone:** `CONFIG` at the top of `tools/build.py`.
- **Projects:** the `PROJECTS` list. Add a dict to add a case study. It shows up on Work, gets its own page, and joins the "next project" chain. `FEATURED` picks the three shown on the homepage.
- **Live previews:** `"live": True` loads the real site inside the frame. Set `False` and the designed poster shows instead.
- **Form endpoint + headline words:** top of `assets/site.js`.

## Client quotes

The biggest thing that will make the site feel established. Ask each client for one or two sentences and permission to use their name, then fill in their project's `quote` in `tools/build.py`:

```
"quote": {"text": "...", "name": "Alexis R.", "role": "Director"},
```

Quotes appear on the case study and in a "In their words" section on the homepage (hidden until at least one exists).

## Before launch

- [ ] **Form:** create a form at formspree.io pointed at that Gmail, paste the endpoint into `FORM_ENDPOINT` in `assets/site.js`.
- [ ] **Tipsy Trail HTTPS:** tipsytrailbc.com currently fails on `https://` (certificate doesn't match). In the `tipsytrailbc` repo: Settings → Pages → remove the custom domain, save, add it back, wait for the certificate, then tick **Enforce HTTPS**. After that, in `tools/build.py` change its `url` to `https://tipsytrailbc.com/` and `live` to `True`, and rebuild.
- [ ] **Client OK:** confirm each client is fine being featured (especially the festival, which is pre-launch).

## Deploy (GitHub Pages)

1. Create a repo (e.g. `hafeezoyeneyin.com`) and push everything in this folder.
2. Repo **Settings → Pages**: deploy from the `main` branch, root folder.
3. After buying the domain, add these DNS records at the registrar:
   - `A` records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `CNAME` for `www` → `<your-github-username>.github.io`
4. Back in **Settings → Pages**, set the custom domain and tick **Enforce HTTPS** once the certificate is issued.

The `CNAME` file is left out until you own the domain; until then the site works at `hoyeneyi.github.io/<repo>`. When the domain is ready, add a file named `CNAME` containing `hafeezoyeneyin.com`.

Note: the claude.ai preview can't load other websites inside the page, so it shows the designed posters. Live previews appear once the site is deployed.
