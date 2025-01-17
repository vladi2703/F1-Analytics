# F1 Analytics Pipeline

**Live Project Site:** [F1 Analytics Dashboard](https://vladi2703.github.io/F1-Analytics/)

## Overview
Data pipeline processing Formula 1 historical data to analyze race performance, predict outcomes, and visualize championship trends. Built by Elina Yancheva and Vladimir Stoyanov.

## Pipeline Triggers
The analysis pipeline runs automatically:
- Monthly on the 1st (March-December during F1 season)
- On push to master (when notebooks or data files change)
- Manually via GitHub Actions

## Quick Start
1. View analysis: Visit the live site
2. Run locally: 
```bash
python build-site.py
```
3. Manual update: Trigger workflow in GitHub Actions tab

## Output
- Generated HTML dashboard with interactive visualizations
- Links to detailed Jupyter notebook
- Access to presentation slides
- Championship and race prediction analysis

Project code and data processing scripts available in this repository.