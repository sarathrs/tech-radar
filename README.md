# Tech Radar Dashboard: Java Developer/Architect Edition

A comprehensive, self-updating dashboard tracking the latest versions and developments in AI tools, cloud platforms, container technologies, search engines, and the Java ecosystem.

**Live Dashboard**: [tech-radar.example.com](https://tech-radar.example.com) (TODO: Update with actual domain)

## Features

- **Verified Information**: All data sourced from official vendors (GitHub releases, official blogs, documentation)
- **Monthly Refresh**: Automated research and updates every 1st of the month (6 AM UTC)
- **Java Focus**: Every technology includes developer and architect relevance for Java teams
- **Interactive UI**: Category tabs, search/filter, Developer/Architect toggle, confidence badges, dark mode
- **Archive**: Historical snapshots preserved for each refresh cycle
- **Zero Build**: Static HTML dashboard, no build step required for deployment

## Categories Tracked

- **AI Tools**: Claude, ChatGPT, Google Gemini, OpenAI Codex
- **Search Engines**: Elasticsearch, OpenSearch, Solr
- **Containers**: Kubernetes, Docker, Podman, Containerd
- **Cloud**: AWS, Microsoft Azure, Google Cloud Platform (major services & announcements)
- **Java Ecosystem**: JDK, Spring Boot, Quarkus, Micronaut, Loom/Valhalla, GraalVM, Jakarta EE, Java SDKs (AWS, Azure, GCP), Elasticsearch Java Client, Kubernetes Fabric8 Client

## Project Structure

```
Claude/
├── data/
│   ├── topics.yaml              # Source of truth: topics, categories, official sources
│   ├── radar.json               # Generated: latest research (refreshed monthly)
│   └── .radar.backup.json       # Previous version (for diff detection)
├── schema/
│   └── radar.schema.json        # JSON Schema for radar.json validation
├── templates/
│   └── dashboard.html           # Static template with embedded CSS/JS
├── scripts/
│   ├── validate.py              # Validates radar.json against schema
│   └── render.py                # Renders dashboard HTML with embedded data
├── docs/
│   ├── index.html               # Published dashboard (GitHub Pages)
│   └── archive/                 # Historical snapshots (YYYY-MM-DD-HH-MM-SS.html)
├── .claude/
│   ├── agents/
│   │   └── tech-radar-researcher.md   # Sonnet-based research agent
│   └── skills/
│       └── tech-radar/
│           └── SKILL.md         # Orchestration workflow
├── .github/
│   └── workflows/
│       └── monthly-refresh.yml  # GitHub Actions: schedule & CI/CD
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ (for Claude Code CLI)
- GitHub account with repository access
- Anthropic API key (for `ANTHROPIC_API_KEY` secret)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Claude
   ```

2. **Install Python dependencies**:
   ```bash
   pip install jsonschema jinja2
   ```

3. **Install Claude Code CLI**:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

### Local Development

#### 1. Validate Data

Check that `data/radar.json` is valid:

```bash
python scripts/validate.py
```

Exit code `0` = valid; non-zero = errors.

#### 2. Render Dashboard

Generate `docs/index.html` from `data/radar.json`:

```bash
python scripts/render.py
```

Outputs:
- `docs/index.html` — main dashboard
- `docs/archive/YYYY-MM-DD-HH-MM-SS.html` — timestamped snapshot

#### 3. Preview in Browser

Open `docs/index.html` in your browser:

```bash
# macOS
open docs/index.html

# Windows
start docs/index.html

# Linux
xdg-open docs/index.html
```

#### 4. Run Research Locally (Optional)

Trigger the research agent directly:

```bash
claude -p "/tech-radar" --model claude-sonnet-5-5
```

(Requires `ANTHROPIC_API_KEY` environment variable)

## Monthly Refresh Workflow

The dashboard refreshes automatically on the **1st of each month at 6 AM UTC**. The process:

1. **Research**: Sonnet-based agent fetches latest versions from official sources
2. **Validate**: Python script checks schema compliance and data completeness
3. **Render**: Dashboard HTML is generated with embedded data
4. **Archive**: Timestamped snapshot saved for historical reference
5. **Review**: Automated PR created for human review and merge
6. **Deploy**: On merge to `main`, GitHub Pages deploys new dashboard

### Triggering Manually

Run the workflow immediately (instead of waiting for cron):

1. Go to **Actions** → **Monthly Tech Radar Refresh**
2. Click **Run workflow**
3. Select branch (usually `main`)
4. Click **Run workflow**

Or via CLI:

```bash
gh workflow run monthly-refresh.yml
```

## Adding New Topics

To track a new technology:

1. **Edit `data/topics.yaml`**:
   ```yaml
   - name: My Technology
     category: Cloud  # or: AI Tools, Search Engines, Containers, Java Ecosystem
     sources:
       - title: Official Website
         url: https://example.com
       - title: GitHub Releases
         url: https://github.com/example/releases
       - title: Official Blog
         url: https://example.com/blog
   ```

2. **Validate** (optional):
   ```bash
   python scripts/validate.py  # Will fail until radar.json is updated
   ```

3. **Wait for monthly refresh**, or trigger manually
   - The research agent will pick up the new topic
   - Updates `data/radar.json` with version, changes, Java relevance, etc.
   - Creates a PR for review

## Understanding Confidence Levels

Each topic includes a confidence badge indicating data source reliability:

| Level | Meaning | Example |
|-------|---------|---------|
| **High** | Official vendor source (GitHub release, official blog) | Kubernetes 1.31 from k8s.io |
| **Medium** | Recent announcement from authoritative source | AWS SDK update from AWS blog |
| **Low** | Older info (>30 days) or secondary sources | Archive of 3-month-old release |
| **Unverified** | Could not confirm version; placeholder | "Latest" version without date |

Prioritize high/medium confidence data for critical decisions.

## Dashboard Navigation

### Tabs
- **All Topics**: View everything
- **AI Tools**, **Search Engines**, **Containers**, **Cloud**, **Java Ecosystem**: Filter by category

### Search/Filter
- Type to search by topic name, version, or feature keywords
- Results update in real-time

### Developer/Architect Toggle
- Each topic card shows Java relevance summaries
- Click **"Show Java Relevance"** to expand
- Developer summary: practical tips and integration patterns
- Architect summary: system design and deployment considerations

### Dark Mode
- Toggle with the moon icon (top right)
- Preference saved to browser localStorage

### Deprecations & EOL
- Red alert section lists all deprecated features across topics
- Plan upgrades accordingly

## Monitoring & Maintenance

### GitHub Actions Logs

View workflow execution logs:

1. Go to **Actions** → **Monthly Tech Radar Refresh**
2. Select the latest run
3. View step logs for details (Research, Validate, Render)

### Failure Handling

| Failure | Resolution |
|---------|-----------|
| Schema validation fails | Check `data/radar.json` format; see error message for field |
| Research timeout | Agent may have hit rate limits; retry later or reduce topic count |
| HTML render error | Ensure `templates/dashboard.html` is valid |
| GitHub Pages deploy fails | Check repository settings; ensure `docs/` is publish source |

### Cost Estimate

- **Agent run** (Sonnet 5.5): ~$0.05–0.15 per month (~15–30 min @ ~$0.003/min)
- **GitHub Actions**: Free tier (public repos)
- **Total**: < $2/month

## Customization

### Adding Categories

Edit `.claude/agents/tech-radar-researcher.md` and:
1. Add category to "Categories" section
2. List topics to track under that category
3. Update `data/topics.yaml` with new topics
4. Re-run research

### Branding

Dashboard colors and fonts are CSS variables in `templates/dashboard.html`:

```css
:root {
  --color-accent: #0066cc;       /* Primary color */
  --color-bg: #ffffff;           /* Background */
  --color-fg: #1a1a1a;           /* Text */
  /* ... more variables ... */
}
```

Modify these to match your brand.

### Deployment Domain

In `.github/workflows/monthly-refresh.yml`, update:

```yaml
cname: tech-radar.example.com  # Replace with your domain
```

And configure DNS CNAME record pointing to `<username>.github.io`.

## Testing

### Unit Test: Validation

```bash
# Should pass
python scripts/validate.py

# Test with invalid data (optional)
echo '{"topics": []}' > data/radar.json
python scripts/validate.py  # Should fail
```

### Unit Test: Render

```bash
# Should generate docs/index.html
python scripts/render.py

# Check output
ls -la docs/index.html
```

### Integration Test: Full Workflow

```bash
# Simulate full research + validate + render
python scripts/validate.py && python scripts/render.py && echo "✓ All checks passed"
```

### Browser Test

1. Open `docs/index.html` in browser
2. Click tabs (should filter topics)
3. Type in search (should highlight matches)
4. Toggle "Show Java Relevance" (should expand card)
5. Toggle dark mode (should switch theme)
6. Click source links (should open in new tab)
7. Scroll footer (should show all sections)

## API Reference

### `data/radar.json` Schema

See `schema/radar.schema.json` for the full JSON Schema.

Example topic:

```json
{
  "name": "Claude",
  "category": "AI Tools",
  "latest_version": "3.5 Sonnet",
  "release_date": "2024-06-20",
  "key_changes": [
    "50% faster inference than Claude 3 Opus",
    "Extended context window to 200k tokens"
  ],
  "deprecations": [
    "Claude 2.0 reached end-of-life"
  ],
  "java_relevance": {
    "developer_summary": "...",
    "architect_summary": "..."
  },
  "links": [
    {
      "title": "Anthropic Claude Official",
      "url": "https://www.anthropic.com/claude"
    }
  ],
  "confidence": "high",
  "last_verified": "2026-10-15T14:32:00Z"
}
```

## Troubleshooting

### "jinja2 not found"
```bash
pip install jinja2
```

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### "docs/index.html is blank"
Check `data/radar.json` is valid:
```bash
python scripts/validate.py
```

### "GitHub Pages not deploying"
1. Ensure `docs/` branch is `main` (Settings → Pages)
2. Check for deploy errors in Actions logs
3. Try pushing again or triggering workflow manually

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a branch (`feature/my-improvement`)
3. Make changes (update YAML, improve HTML/CSS, fix scripts)
4. Submit a pull request with a clear description

For schema or workflow changes, please discuss in an issue first.

## License

This project is provided as-is for educational and organizational use.

## Support

For issues or questions:

1. Check **Troubleshooting** section above
2. Review `.github/workflows/monthly-refresh.yml` logs for automation issues
3. Open a GitHub issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior

## References

- [Anthropic Claude API](https://docs.anthropic.com/)
- [JSON Schema Specification](https://json-schema.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Guide](https://docs.github.io/)
- [OpenJDK Release Notes](https://jdk.java.net/)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Kubernetes Releases](https://kubernetes.io/releases/)

---

**Last updated**: October 2026
**Maintained by**: Claude Code Agent (Sonnet 5.5)
**Refresh cycle**: Monthly (1st of month, 6 AM UTC)
