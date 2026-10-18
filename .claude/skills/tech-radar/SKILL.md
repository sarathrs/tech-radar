# Tech Radar Refresh Skill

Orchestrates a monthly refresh of the Tech Radar Dashboard. Researches latest info on AI tools, search engines, containers, cloud platforms, and Java ecosystem; validates output; renders HTML dashboard; archives snapshot; and prepares diff summary for human review.

## Workflow

### Step 1: Verify Input Files
- [ ] Read `data/topics.yaml` — list of technologies and their official source URLs
- [ ] Read `schema/radar.schema.json` — required output structure
- [ ] Check if `data/radar.json` exists (for diff baseline); copy to `data/.radar.backup.json`

### Step 2: Launch Research Agent
- [ ] Invoke `tech-radar-researcher` subagent with:
  - Topics list (from topics.yaml)
  - Schema (from radar.schema.json)
  - Instructions: research latest versions, set confidence, include Java relevance, always cite URLs
  - Model: `claude-sonnet-5-5` (for monthly runs, this is the main research capability)
- [ ] Agent outputs: `data/radar.json` (validated, ready-to-render)

### Step 3: Validate Schema
- [ ] Run `python scripts/validate.py data/radar.json`
  - Exit code 0 = success; 1 = schema error
  - If error: report validation failures and halt (do not render invalid data)
  - Check: all required fields present, dates are ISO 8601, URLs are reachable (warn, not fail)

### Step 4: Render Dashboard
- [ ] Run `python scripts/render.py`
  - Input: `data/radar.json` (from agent)
  - Output: 
    - `docs/index.html` (live dashboard)
    - `docs/archive/YYYY-MM-DD-HH-MM-SS.html` (timestamped snapshot)
  - Embedded in HTML: data JSON, search index, toggle state
  - Compute diff vs `data/.radar.backup.json`: highlight new/updated topics, removed deprecations

### Step 5: Generate Diff Summary
- [ ] Compare `data/.radar.backup.json` (previous) vs `data/radar.json` (current)
  - New topics added
  - Version bumps (old → new)
  - New deprecations
  - Removed topics
  - Java ecosystem changes (JDK, Spring Boot, etc.)
- [ ] Write summary as markdown for PR description:
  ```
  # Tech Radar Update — YYYY-MM

  ## What Changed This Month

  **New Topics**: X
  **Version Bumps**: Y
  **New Deprecations**: Z
  **Java Ecosystem Updates**: ...

  ## Notable Changes
  - [Topic]: X → Y (confidence: high)
  - [JDK]: 23 LTS released
  - ...

  [View Dashboard](https://link-to-pages) | [Full Diff](git diff...)
  ```

### Step 6: Invoke dataviz Skill (Optional)
- [ ] If rendering includes charts (e.g., release-cadence timeline, version-currency heatmap):
  - Read `/dataviz` skill for color palette, accessibility rules, interaction patterns
  - Ensure light/dark mode safe colors
  - WCAG AA contrast minimum

### Step 7: Success Handoff
- [ ] Confirm:
  - ✓ `data/radar.json` valid and written
  - ✓ `docs/index.html` rendered and readable
  - ✓ `docs/archive/YYYY-MM-DD-HH-MM-SS.html` snapshot created
  - ✓ Diff summary generated
- [ ] Report: "Tech Radar monthly refresh complete. Ready for PR review."

## Usage (Local)

```bash
cd C:\Users\sarath\Explore\MarketPlace\Claude\tech-radar

# Run the skill interactively in Claude Code
claude -p "/tech-radar"

# Or, in CI (GitHub Actions):
claude -p "/tech-radar" --model claude-sonnet-5-5
```

## Usage (GitHub Actions)

Triggered by `.github/workflows/monthly-refresh.yml`:
```bash
# CI invocation (cron-scheduled or workflow_dispatch)
- run: claude -p "/tech-radar" --model claude-sonnet-5-5
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Rollback

If radar.json is invalid or data is stale:
```bash
# Restore from backup
cp data/.radar.backup.json data/radar.json

# Re-render
python scripts/render.py

# Check output
open docs/index.html
```

## Maintenance

- **Monthly**: Skill is auto-invoked via GitHub Actions on the 1st of each month (6 AM UTC)
- **On-demand**: Use `workflow_dispatch` to trigger manually anytime
- **New topics**: Update `data/topics.yaml`, add official sources, re-run skill
- **Schema changes**: Update `schema/radar.schema.json`, ensure backward compatibility

## Cost / Performance

- Research time: ~30-40 min (15 topics, standard WebSearch mode)
- Token usage: ~2-3k tokens (Sonnet 5.5)
- Render time: ~5 sec (Python)
- Total wall-clock: ~45 min (incl. agent startup, CI overhead)
- Monthly cost: ~$0.10 (Sonnet input/output at standard rates)

## Next Steps (Post-Merge)

- Merge PR to main → GitHub Pages auto-deploys `docs/index.html`
- Archive snapshot remains in `docs/archive/` for historical reference
- Next refresh scheduled for 1st of next month
