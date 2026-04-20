---
title: OpenClaw Data Storage Policy
summary: Data stored locally on VPS with GitHub backup; third-party clouds prohibited.
tags: []
keywords: []
importance: 50
recency: 1
maturity: draft
createdAt: '2026-04-20T07:19:53.302Z'
updatedAt: '2026-04-20T07:19:53.302Z'
---
## Reason
Document storage preferences from Anh Bình

## Raw Concept
**Task:**
Define OpenClaw storage policy

**Timestamp:** 2026-04-20

**Author:** Anh Bình

## Narrative
### Structure
Data resides on the local VPS. Backups are exclusive to the specified private GitHub repository.

### Rules
Rule 1: Never use third-party cloud storage for OpenClaw data.

## Facts
- **storage_location**: Data must be stored locally on the VPS. [project]
- **backup_target**: Backups are allowed only on the private GitHub repository cevasonic/OpenClawBotV1. [project]
- **storage_constraint**: Third-party cloud storage is strictly prohibited. [project]
