# The Country Shed UK - Faceless Auto Site (v2)

## What this gives you
- 60+ pre-filled topics (6+ months at 2 posts/week)
- Enhanced generator with:
  - Top-picks table
  - Comparison table
  - UK-focused advice
  - Amazon UK search links using your Associate tag
- Weekly GitHub Action (plus an optional daily workflow you can enable)

## Setup (one-time)
1. Create a repo named `<your-username>.github.io` on GitHub.
2. Upload/extract these files into the repo (or push with Git).
3. Edit `_config.yml`:
   - `url: "https://<your-username>.github.io"`
   - `amazon_tag: yourtag-21` (replace with your Amazon Associates UK tag)
4. Go to **Settings -> Pages** and select build from branch `main` (if not default).
5. Open **Actions** and enable workflows. Run the **Auto-Publish Posts (Weekly)** manually the first time if you want content immediately.

## Optional
- Enable the daily workflow: rename `.github/workflows/autopost-daily-disabled.yml` to `autopost-daily.yml`.
- Add more topics by editing `scripts/topics.json`.
- Tweak the template inside `scripts/generate_posts.py` if you want different sections.

## Notes
- All content is faceless and generated automatically.
- Links are generic Amazon search results; prices and stock change frequently.
- You can later add Awin/eBay links directly into the template.