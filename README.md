# Deep Scanner Forex Market Analysis Bot

Professional-grade forex market analysis engine running on Termux/Android.

## Quick Start

```bash
# Start Flask backend
cd backend && python -m flask run --host=0.0.0.0 --port=5000

# In another Termux session, start React dev server
cd frontend && npm start
```

## Installation

Automatic: Run `install.sh`
Manual: See INSTALLATION.md

## Documentation

- Technical Guide: `docs/TECHNICAL_GUIDE.md`
- API Reference: `docs/API.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

## Configuration

Edit `config/settings.json` to customize:
- Tick count (100-5000)
- Markets to scan
- Indicator periods
- Risk parameters

# REPO-BUILDER
