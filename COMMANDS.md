# Tech Radar - Quick Command Reference

## Local Development

### Test Rendering Pipeline
```bash
# Validate current radar.json against schema
python scripts/validate.py

# Render HTML dashboard from radar.json
python scripts/render.py

# Both in sequence
python scripts/validate.py && python scripts/render.py
```

### Run Research Agent (Claude Code)
```bash
# Run skill with Sonnet 5.5 (uses ANTHROPIC_API_KEY env var)
claude -p "/tech-radar"

# Run with explicit model
claude -p "/tech-radar" --model claude-sonnet-5-5

# Run with specific options
claude -p "/tech-radar" --no-cache --verbose
```

### Git & Version Control
```bash
# Initial setup
git init
git config user.email "your@email.com"
git config user.name "Your Name"

# Stage and commit
git add .
git commit -m "Monthly tech radar refresh"

# Push to GitHub
git push origin main

# View changes
git diff data/radar.json
git log --oneline

# Create new branch for testing
git checkout -b feature/add-new-topics
```

### Dashboard Testing
```bash
# Open dashboard in default browser (Windows)
start docs/index.html

# Open on macOS
open docs/index.html

# Open on Linux
xdg-open docs/index.html

# Quick http server (Python)
python -m http.server 8000
# Then visit: http://localhost:8000/docs/index.html
```

---

## GitHub Actions

### Manual Trigger
```bash
# Via GitHub CLI (install from https://cli.github.com/)
gh workflow run "monthly-refresh.yml"

# Or via GitHub Web UI:
# 1. Go to repo → Actions
# 2. Select "Monthly Tech Radar Refresh"
# 3. Click "Run workflow"
```

### Check Workflow Status
```bash
# List recent runs
gh run list --workflow=monthly-refresh.yml

# View latest run details
gh run view --workflow=monthly-refresh.yml

# Watch run in real-time
gh run watch --workflow=monthly-refresh.yml
```

### View Workflow Logs
```bash
# Get latest job logs
gh run view <run-id> --log

# Stream live logs
gh run watch <run-id>
```

---

## Data Management

### Update Topics Catalog
```bash
# Edit topics.yaml to add/remove technologies
nano data/topics.yaml

# Re-run agent to research new topics
claude -p "/tech-radar" --model claude-sonnet-5-5
```

### Backup Current Data
```bash
# Manual backup before changes
cp data/radar.json data/radar.json.backup-$(date +%Y%m%d)

# List all backups
ls -la data/radar.json*
```

### Compare Versions
```bash
# Diff current vs backup
diff data/.radar.backup.json data/radar.json

# View specific change
git diff data/radar.json
```

### Reset to Previous State
```bash
# If render went wrong, restore from backup
cp data/.radar.backup.json data/radar.json
python scripts/render.py

# Or use git
git checkout HEAD -- data/radar.json
python scripts/render.py
```

---

## Configuration

### Environment Variables
```bash
# Set API key for local runs
export ANTHROPIC_API_KEY=sk-...  # macOS/Linux
set ANTHROPIC_API_KEY=sk-...      # Windows cmd
$env:ANTHROPIC_API_KEY='sk-...'   # Windows PowerShell

# Verify it's set
echo $ANTHROPIC_API_KEY
```

### Modify Automation Schedule
```bash
# Edit .github/workflows/monthly-refresh.yml
nano .github/workflows/monthly-refresh.yml

# Change cron expression (line 6):
# Current:  '0 6 1 * *'  (1st of month, 6 AM UTC)
# Weekly:   '0 0 * * 0'  (Sundays at midnight)
# Daily:    '0 6 * * *'  (Every day at 6 AM)
# Hourly:   '0 * * * *'  (Every hour)

# Commit and push
git add .github/workflows/monthly-refresh.yml
git commit -m "chore: update refresh schedule"
git push
```

### Customize Dashboard Template
```bash
# Edit HTML template
nano templates/dashboard.html

# Modify CSS variables for theme
# Look for: :root { ... } and [data-theme="dark"] { ... }

# After changes, re-render
python scripts/render.py
```

---

## Troubleshooting

### Agent Not Running
```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Test Claude Code CLI
claude --version

# Run with verbose output
claude -p "/tech-radar" --verbose
```

### Validation Fails
```bash
# See detailed error
python scripts/validate.py

# Common fixes:
# - Add missing fields to radar.json
# - Fix date format to YYYY-MM-DD
# - Ensure all topics have links array
```

### Render Fails
```bash
# Check dependencies installed
pip list | grep -E "jinja2|jsonschema"

# Install if missing
pip install jinja2 jsonschema

# Try rendering with debug info
python scripts/render.py

# Check output file
ls -la docs/index.html
```

### GitHub Actions Not Triggering
```bash
# Check workflow file syntax
gh workflow view .github/workflows/monthly-refresh.yml

# List all workflows
gh workflow list

# View recent runs
gh run list --workflow=.github/workflows/monthly-refresh.yml

# Manually trigger to test
gh workflow run "monthly-refresh.yml"
```

---

## Development Tips

### Adding New Data Fields
```bash
# 1. Update schema first
nano schema/radar.schema.json

# 2. Add field to agent instructions
nano .claude/agents/tech-radar-researcher.md

# 3. Update template if needed
nano templates/dashboard.html

# 4. Test with existing data
python scripts/validate.py

# 5. Commit schema changes
git add schema/radar.schema.json
git commit -m "schema: add new field"
```

### Testing Agent Locally
```bash
# Run agent with timeout and turn limit
claude -p "/tech-radar" --max-turns 50 --timeout 300

# Or modify skill to research just one topic
# Edit .claude/skills/tech-radar/SKILL.md to focus on single category
```

### Debugging Dashboard JS
```bash
# Open browser DevTools
# Windows/Linux: F12 or Ctrl+Shift+I
# macOS: Cmd+Option+I

# Check:
# 1. Network tab - are requests completing?
# 2. Console tab - any JS errors?
# 3. Elements/Inspector - is data injected?
# 4. Look for: window.TOPICS_DATA in console
```

---

## Maintenance Checklist

### Weekly
- [ ] Spot-check live dashboard
- [ ] Monitor GitHub Actions runs (if scheduled)

### Monthly (after refresh)
- [ ] Review PR changes carefully
- [ ] Verify all URLs are accessible
- [ ] Check version numbers against official sources
- [ ] Test in both light and dark modes
- [ ] Merge PR to trigger GitHub Pages deploy

### Quarterly
- [ ] Update topics.yaml with new emerging tech
- [ ] Review agent instructions for accuracy
- [ ] Check for deprecated technologies to remove
- [ ] Update Java ecosystem section (Loom, Valhalla, etc.)

### Annually
- [ ] Archive and review historical snapshots
- [ ] Consider redesigning dashboard template
- [ ] Evaluate cost vs. value
- [ ] Plan any major schema changes

---

## Performance Notes

| Operation | Time | Tokens | Cost |
|-----------|------|--------|------|
| Validate radar.json | <1s | 0 | \$0.00 |
| Render dashboard | ~5s | 0 | \$0.00 |
| Full research (15 topics) | ~30-40m | 2-3k | \$0.10 |
| GitHub Actions overhead | ~5m | 0 | \$0.00 |
| **Total per month** | ~45m | 2-3k | **\$0.10** |

---

## Resources

- **Claude Code:** https://claude.com/claude-code
- **GitHub Actions:** https://docs.github.com/en/actions
- **Anthropic API:** https://docs.anthropic.com
- **GitHub CLI:** https://cli.github.com
- **Python jsonschema:** https://python-jsonschema.readthedocs.io
- **Jinja2 Templates:** https://jinja.palletsprojects.com

---

**Last Updated:** October 18, 2026
