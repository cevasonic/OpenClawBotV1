# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260502-001] correction

**Logged**: 2026-05-02T20:34:00+07:00
**Priority**: medium
**Status**: promoted
**Area**: config

### Summary
Skill tinhtien output format was difficult to read; user requested clearer display with model name on separate line and cost, %, Req on next line.

### Details
Initially the skill printed all info in a compact table that was hard to parse. After user feedback, we reformatted to show each model name on its own line, followed by indented line showing cost, percentage, and request count. Also grouped low-request models into "Model khác" and sorted by cost descending.

### Suggested Action
Keep this format as default for tinhtien skill output.

### Metadata
- Source: conversation
- Related Files: /root/.openclaw/workspace/skills/tinhtien/scripts/tinhtien.sh
- Tags: tinhtien, formatting, user-feedback

### Resolution
- **Promoted**: AGENTS.md
- **Notes**: Added skill output formatting guidelines to AGENTS.md under "Skill Output Formatting" section