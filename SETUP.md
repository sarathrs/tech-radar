# Tech Radar Dashboard - Setup & Next Steps

🎉 **Project successfully scaffolded!** All files are in place and tested locally.

**Project Root:** `C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar\`

## ✅ What's Been Generated

### Data & Schema
- **`data/topics.yaml`** - 13 technologies across 5 categories (AI Tools, Search Engines, Containers, Cloud, Java)
- **`data/radar.json`** - Sample seeded data with realistic versions (Claude 3.5 Sonnet, GPT-4o, Elasticsearch 8.14, etc.)
- **`schema/radar.schema.json`** - JSON Schema validating all radar.json entries
- **`data/.radar.backup.json`** - Backup for computing monthly diffs

### Rendering Pipeline
- **`scripts/validate.py`** - Validates radar.json against schema (✅ tested, passes)
- **`scripts/render.py`** - Converts radar.json → docs/index.html + archived snapshots (✅ tested, generates 34KB HTML)
- **`templates/dashboard.html`** - Single self-contained HTML file with:
  - Category tabs (AI Tools, Search, Containers, Cloud, Java)
  - Developer/Architect toggle
  - Search/filter box
  - Version table
  - Light/dark mode
  - Responsive design (flexbox, mobile-friendly)

### Dashboard Output
- **`docs/index.html`** - Live dashboard (ready to deploy to GitHub Pages)
- **`docs/archive/`** - Timestamped monthly snapshots

### Agent & Automation
- **`.claude/agents/tech-radar-researcher.md`** - Subagent definition (Sonnet 5.5, researches topics, validates output)
- **`.claude/skills/tech-radar/SKILL.md`** - Workflow orchestration (read topics → research → validate → render → diff summary)
- **`.github/workflows/monthly-refresh.yml`** - GitHub Actions cron trigger (1st of month, 6 AM UTC)

### Docs
- **`README.md`** - Project overview and usage
- **`.gitignore`** - Standard Node/Python ignores

---

## 🚀 Next Steps

### 1. Initialize Git Repo
```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar

# Initialize git
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Create initial commit
git add .
git commit -m "Initial Tech Radar Dashboard scaffold

- Data model with 13 core technologies
- Validation schema
- HTML dashboard template with light/dark mode
- Python render pipeline
- Claude Code agent + skill definitions
- GitHub Actions workflow for monthly refresh

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

# Add remote (create empty repo on GitHub first)
git remote add origin https://github.com/YOUR_USERNAME/tech-radar.git
git branch -M main
git push -u origin main
```

### 2. Set Up GitHub Secrets
In your GitHub repo:
1. Go to **Settings → Secrets and variables → Actions**
2. Add `ANTHROPIC_API_KEY` with your Anthropic API key
3. (Optional) Enable GitHub Pages:
   - Go to **Settings → Pages**
   - Set Source to "Deploy from a branch"
   - Select `main` branch, `docs/` folder
   - Save

### 3. Test Locally (Claude Code)
```bash
# From project root, run the skill manually
claude -p "/tech-radar"

# This will:
# ✓ Read data/topics.yaml
# ✓ Launch tech-radar-researcher agent
# ✓ Generate/update data/radar.json
# ✓ Validate schema
# ✓ Render docs/index.html
# ✓ Show diff vs previous version
```

### 4. View the Dashboard
```bash
# Open generated HTML in browser
open docs/index.html  # macOS
start docs/index.html  # Windows
xdg-open docs/index.html  # Linux
```

Test features:
- [ ] Click category tabs (AI Tools, Search, Containers, Cloud, Java)
- [ ] Toggle Developer/Architect mode
- [ ] Use search filter box
- [ ] Toggle light/dark mode (top-right)
- [ ] Hover over version cells to see confidence badge
- [ ] Check "What changed this month" banner (compares vs .radar.backup.json)

### 5. First Full Run with Research Agent
```bash
# Generate fresh research data (uses Sonnet 5.5)
claude -p "/tech-radar" --model claude-sonnet-5-5
```

This will:
- Fetch official sources for all 13 topics
- Search for latest versions, key changes, deprecations
- Verify with high confidence standard info
- Escalate to extended search for niche/emerging tech
- Include Java developer/architect guidance for each
- Populate radar.json
- Render dashboard
- Show what's new/changed

### 6. GitHub Actions Setup
Once pushed to GitHub, the monthly-refresh workflow will:
- **Trigger:** 1st of each month, 6 AM UTC (or manual via `workflow_dispatch`)
- **Run:** Claude Code skill to research, validate, render
- **Output:** PR with changes for human review
- **Deploy:** On merge to main, GitHub Pages auto-updates

Trigger manually anytime:
1. Go to **Actions → Monthly Tech Radar Refresh**
2. Click **Run workflow**
3. Select branch (main)
4. Click **Run**

---

## 📚 File Reference

| File | Purpose | Status |
|------|---------|--------|
| `data/topics.yaml` | Tech catalog with source URLs | ✅ Complete |
| `data/radar.json` | Current research data | ✅ Seeded sample |
| `schema/radar.schema.json` | Validation schema | ✅ Complete |
| `scripts/validate.py` | Schema validator | ✅ Tested |
| `scripts/render.py` | HTML renderer | ✅ Tested |
| `templates/dashboard.html` | UI template | ✅ Complete |
| `docs/index.html` | Output dashboard | ✅ Generated |
| `.claude/agents/tech-radar-researcher.md` | Research agent | ✅ Complete |
| `.claude/skills/tech-radar/SKILL.md` | Workflow skill | ✅ Complete |
| `.github/workflows/monthly-refresh.yml` | CI/CD workflow | ✅ Complete |
| `README.md` | Project docs | ✅ Complete |

---

## 🔧 Customization

### Add New Technologies
1. Edit `data/topics.yaml` - add name, category, source URLs
2. Next run of `/tech-radar` will research them automatically

### Modify Dashboard Theme
1. Edit `templates/dashboard.html` - CSS variables in `<style>`
2. Customize colors, fonts, spacing, breakpoints
3. Re-run `python scripts/render.py` to regenerate

### Expand Java Guidance
1. Edit `.claude/agents/tech-radar-researcher.md`
2. Update "Java Ecosystem specifics" section with more considerations
3. Agent will include them in future runs

### Change Schedule
1. Edit `.github/workflows/monthly-refresh.yml` line 6
2. Update cron expression: `'minute hour day month day-of-week'`
   - Current: `'0 6 1 * *'` = 1st of month, 6 AM UTC
   - Example: `'0 0 * * 0'` = Every Sunday at midnight UTC

---

## 📊 Architecture Overview

```
User: Needs Java Dev/Architect Tech Radar
   ↓
/tech-radar skill (Claude Code)
   ↓
tech-radar-researcher agent (Sonnet 5.5)
   ├→ Read topics.yaml
   ├→ WebSearch official sources
   ├→ WebFetch GitHub releases, blogs
   ├→ Verify versions & dates
   └→ Write radar.json
   ↓
validate.py (schema check)
   ↓
render.py (HTML generation)
   ├→ Compute diff vs backup
   ├→ Inject data into template
   └→ Write index.html + archive snapshot
   ↓
GitHub Actions (monthly cron)
   ├→ Run skill automatically
   ├→ Create PR with changes
   └→ Deploy to GitHub Pages on merge
   ↓
https://your-username.github.io/tech-radar/
```

---

## 💡 Tips & Best Practices

### For Monthly Reviews (PR Checklist)
- [ ] Versions match official vendor releases
- [ ] Dates are recent (within 1-2 weeks)
- [ ] Java relevance summaries are helpful
- [ ] No hallucinated/unverified data
- [ ] All links are working and authoritative
- [ ] Dashboard renders correctly in browser (light & dark modes)
- [ ] Archive snapshot saved

### Cost Management
- **Research run:** ~$0.10 (Sonnet 5.5, ~2-3k tokens, ~30 min)
- **Monthly cost:** ~$0.10
- **Annual cost:** ~$1.20
- *Note: Requires ANTHROPIC_API_KEY secret in GitHub*

### Troubleshooting

**"ANTHROPIC_API_KEY not set"**
- GitHub Actions: Add secret in Settings → Secrets
- Local: Set env var: `export ANTHROPIC_API_KEY=sk-...`

**Schema validation fails**
- Run `python scripts/validate.py` to see errors
- Common: missing `links`, invalid dates, empty fields
- Fix radar.json and re-run render.py

**Dashboard doesn't render**
- Check `docs/index.html` exists
- Ensure `templates/dashboard.html` has closing tags
- Check browser console for JS errors

**Workflow doesn't trigger**
- Verify cron expression in `.github/workflows/monthly-refresh.yml`
- Manual trigger: Actions tab → Run workflow
- Check workflow logs for errors

---

## 📞 Support

- **Claude Code docs:** https://claude.com/claude-code
- **GitHub Actions docs:** https://docs.github.com/en/actions
- **Anthropic API:** https://docs.anthropic.com

---

**Generated with Claude Haiku 4.5 + Sonnet 5.5** 🤖

*Last updated: October 18, 2026*
