# Tech Radar Dashboard - GitHub Setup Guide

**📌 Complete these steps after project scaffolding to deploy your dashboard**

**Estimated time:** 10-15 minutes  
**Difficulty:** Easy (copy-paste commands)

---

## 🎯 What You'll Accomplish

After these steps, your Tech Radar Dashboard will be:
- ✅ On GitHub (version controlled)
- ✅ Live on GitHub Pages
- ✅ Auto-refreshing monthly (1st of month, 6 AM UTC)
- ✅ Accessible at: `https://YOUR_USERNAME.github.io/tech-radar/`

---

## 📋 Prerequisites

Before starting, you need:
- [ ] GitHub account (free tier is fine)
- [ ] Git installed locally (`git --version` to verify)
- [ ] Anthropic API key (from https://console.anthropic.com/account/keys)

---

## ✅ Setup Steps

### Step 1: Initialize Git Locally

Open PowerShell/Terminal and run:

```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar

git init
git config user.email "your-email@example.com"
git config user.name "Your Name"

git add .
git commit -m "Initial Tech Radar Dashboard scaffold

- Data model with 13 core technologies
- Interactive HTML dashboard with light/dark mode
- Python validation and rendering pipeline
- Claude Code research agent (Sonnet 5.5)
- GitHub Actions monthly automation
- Java developer/architect guidance included

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial Tech Radar Dashboard scaffold
 20 files changed, 250 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 ...
```

✅ **Checkpoint:** Run `git log` to verify commit created.

---

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `tech-radar`
3. **Description:** (Optional)
   ```
   Monthly Tech Radar Dashboard - Java Developer/Architect Edition. 
   Tracks AI tools, search engines, containers, cloud platforms, and Java ecosystem.
   ```
4. **Visibility:** ⭕ **Public** (required for GitHub Pages)
5. **Initialize this repository with:**
   - ❌ **DO NOT** check "Add a README file"
   - ❌ **DO NOT** check "Add .gitignore"
   - ❌ **DO NOT** check "Choose a license"
   
   (We already have these locally)

6. Click **"Create repository"**

**You'll see a page with setup instructions.** Copy the commands for "push an existing repository from the command line."

✅ **Checkpoint:** Repo created successfully.

---

### Step 3: Connect Local Repo to GitHub

GitHub will show you something like this. Run these exact commands:

```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar

git remote add origin https://github.com/YOUR_USERNAME/tech-radar.git
git branch -M main
git push -u origin main
```

⚠️ **IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username.

**Expected output:**
```
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
...
To https://github.com/YOUR_USERNAME/tech-radar.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Checkpoint:** Run `git remote -v` to verify connection.

---

### Step 4: Add GitHub Secret (API Key)

This allows GitHub Actions to call the Anthropic API for monthly research.

1. Go to your repo: `https://github.com/YOUR_USERNAME/tech-radar`
2. Click the **Settings** tab (top right, next to "About")
3. On the left sidebar, find **"Secrets and variables"** → click **"Actions"**
4. Click the **"New repository secret"** button (green button, top right)
5. Fill in the form:
   - **Name:** `ANTHROPIC_API_KEY` (exactly as shown, case-sensitive)
   - **Value:** Paste your Anthropic API key (from https://console.anthropic.com/account/keys)
   
   ```
   Example format: sk-ant-<your-key>
   ```

6. Click **"Add secret"** button

**Expected result:**
```
✓ ANTHROPIC_API_KEY
  Updated just now
```

✅ **Checkpoint:** Secret appears in the list.

---

### Step 5: Enable GitHub Pages

GitHub Pages will publish your dashboard to the web.

1. Still in **Settings**, scroll down and find **"Pages"** in the left sidebar
2. Under "Build and deployment":
   - **Source:** Select "Deploy from a branch"
   - **Branch:** Select `main` from dropdown
   - **Folder:** Select `/(root)` then `tech-radar` then `docs` (or select `/docs` folder)
   - Click **"Save"**

3. GitHub will show a message:
   ```
   ✓ Your site is published at https://YOUR_USERNAME.github.io/tech-radar/
   ```

**This URL is your live dashboard!** (May take 2-3 min to appear)

✅ **Checkpoint:** You see the GitHub Pages URL.

---

### Step 6: Test the Workflow (Optional but Recommended)

#### Option A: Trigger Workflow Manually (Recommended First)

1. Go to your repo: `https://github.com/YOUR_USERNAME/tech-radar`
2. Click the **"Actions"** tab (top)
3. On the left, you should see: **"Monthly Tech Radar Refresh"** workflow
4. Click it to open
5. Click the **"Run workflow"** button (blue button, top right)
6. Select branch: `main`
7. Click **"Run workflow"** button

**What happens next:**
- ⏳ Workflow starts (you'll see a yellow dot 🟡)
- ⏳ Takes 2-5 minutes (depends on Claude API response time)
- ✅ Turns green 🟢 when complete
- A PR will be created automatically

**View the workflow run:**
- Click on the running workflow to see logs
- Check each step: Checkout → Setup → Install → Research → Validate → Render → Create PR

#### Option B: Test Locally First (Advanced)

If you want to test before the monthly run:

```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar

# Set your API key temporarily
$env:ANTHROPIC_API_KEY='your-api-key-here'

# Run the skill
claude -p "/tech-radar"

# This will:
# 1. Research all 13 topics
# 2. Generate data/radar.json
# 3. Validate against schema
# 4. Render docs/index.html
# 5. Show diff summary
```

Takes 30-40 minutes for full research.

✅ **Checkpoint:** Workflow completes successfully (green ✅ status).

---

### Step 7: Review and Deploy

After workflow completes:

1. Go to **"Pull requests"** tab in your repo
2. You'll see a PR titled: **"chore: monthly tech radar refresh"**
3. Review the changes:
   - Click **"Files changed"** to see what was updated
   - Check the diff of `tech-radar/data/radar.json`
   - Verify topics and versions look correct

4. If everything looks good, click **"Merge pull request"**
5. Confirm the merge
6. GitHub will automatically deploy to Pages within 1-2 minutes

✅ **Checkpoint:** PR merged, dashboard is live!

---

### Step 8: Verify Deployment

1. Visit your dashboard:
   ```
   https://YOUR_USERNAME.github.io/tech-radar/
   ```

2. Test the dashboard features:
   - [ ] Click category tabs (AI Tools, Search, Containers, Cloud, Java)
   - [ ] Use search filter box
   - [ ] Toggle Developer/Architect mode
   - [ ] Toggle light/dark mode (top right)
   - [ ] Check "What changed this month" banner
   - [ ] Verify links work

3. Check the rendered HTML:
   - [ ] Right-click → "View page source"
   - [ ] Look for `window.TOPICS_DATA = [...]` containing your data
   - [ ] Verify all topics have `links[]` array with URLs

✅ **Checkpoint:** Dashboard loads and works correctly!

---

## 📊 What Happens Next

### Monthly Automation (Automatic)
- **1st of every month, 6 AM UTC:** GitHub Actions workflow runs automatically
- Researches all topics for latest versions
- Creates a PR with changes
- You review and merge
- Dashboard updates on GitHub Pages

### Manual Trigger (Anytime)
```
GitHub → Actions → "Monthly Tech Radar Refresh" → "Run workflow"
```

### Local Updates
Any time you want to run manually:
```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar
$env:ANTHROPIC_API_KEY='your-key'
claude -p "/tech-radar"
```

---

## 🆘 Troubleshooting

### Git Setup Issues

**"fatal: destination path already exists and is not an empty directory"**
- You ran `git init` in the wrong folder or repo already exists
- Solution: `cd` to `tech-radar` folder and verify with `ls -la`

**"Please tell me who you are" error**
- Solution: Set git config first:
  ```bash
  git config user.email "your@email.com"
  git config user.name "Your Name"
  ```

### GitHub Connection Issues

**"fatal: remote origin already exists"**
- Solution: 
  ```bash
  git remote remove origin
  git remote add origin https://github.com/YOUR_USERNAME/tech-radar.git
  ```

**Push fails with authentication error**
- Solution: Use GitHub personal access token
  - Go to https://github.com/settings/tokens
  - Generate new token (repo access only)
  - Use token as password when pushing

### Workflow Issues

**"ANTHROPIC_API_KEY not found"**
- Solution: Check Settings → Secrets → verify secret is named exactly `ANTHROPIC_API_KEY`
- Make sure to use a **Personal Access Token**, not repository token

**"Workflow doesn't run at scheduled time"**
- GitHub schedules run in UTC timezone
- Current: 1st of month, 6 AM UTC
- If not running: manually trigger via "Run workflow" button to test

**"Dashboard not updating after merge"**
- GitHub Pages takes 2-3 minutes to deploy
- Hard refresh browser: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Check Settings → Pages to verify deployment status

### Dashboard Issues

**"Dashboard shows no data"**
- Check browser console (F12 → Console tab)
- Look for errors loading `window.TOPICS_DATA`
- Verify `docs/index.html` was generated

**"Page looks broken or unstyled"**
- Clear browser cache: `Ctrl+Shift+Delete`
- Disable browser extensions temporarily
- Try in incognito/private mode
- Check in different browser

**"Light/dark mode not working"**
- Check localStorage is enabled in browser
- Try toggling button multiple times
- Check browser console for JS errors

---

## 💡 Tips & Best Practices

### Monthly Review Checklist
When PR appears, before merging:
- [ ] Versions match official vendor releases
- [ ] Dates are recent (within 1-2 weeks)
- [ ] Java relevance summaries are helpful
- [ ] All links are working
- [ ] Dashboard renders correctly in browser (both light & dark modes)
- [ ] Archive snapshot was saved

### Adding New Topics
Edit `data/topics.yaml`:
```yaml
  - name: New Technology
    category: AI Tools
    sources:
      - title: Official Site
        url: https://example.com
      - title: GitHub Releases
        url: https://github.com/example/releases
```

Next month's run will automatically research it.

### Customizing the Dashboard
Edit `templates/dashboard.html`:
- CSS variables at top (colors, fonts)
- HTML structure (add sections, reorder)
- JavaScript logic (tabs, search)

Then test locally:
```bash
python scripts/render.py
start docs/index.html
```

### Managing Costs
- Research runs: ~$0.10/month (Sonnet 5.5)
- Annual: ~$1.20
- No server/hosting costs (GitHub Pages is free)

---

## 📞 Support Resources

- **Claude Code:** https://claude.com/claude-code
- **GitHub Actions:** https://docs.github.com/en/actions
- **GitHub Pages:** https://pages.github.com
- **Anthropic API:** https://docs.anthropic.com

---

## ✅ Completion Checklist

- [ ] Step 1: Git initialized locally ✓
- [ ] Step 2: GitHub repository created ✓
- [ ] Step 3: Local repo pushed to GitHub ✓
- [ ] Step 4: ANTHROPIC_API_KEY secret added ✓
- [ ] Step 5: GitHub Pages enabled ✓
- [ ] Step 6: Workflow triggered (manual test) ✓
- [ ] Step 7: PR reviewed and merged ✓
- [ ] Step 8: Dashboard verified live ✓

**Once all done:** Your dashboard is fully operational! 🎉

---

**Next steps after completion:**
1. Bookmark your dashboard URL
2. Set calendar reminder for monthly reviews
3. Check it auto-refreshes next month
4. Consider customizing dashboard theme/adding topics

**Questions?** Refer back to this guide or check SETUP.md, COMMANDS.md, or README.md in the project.

---

*Last updated: October 18, 2026*  
*Generated with Claude Haiku 4.5 + Sonnet 5.5* 🤖
