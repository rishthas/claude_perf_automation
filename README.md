# PostgreSQL Performance Analysis Automation

Automated PostgreSQL performance analysis using Claude Code that generates comprehensive HTML reports and optionally emails them to specified recipients.

## Overview

This script automates the process of analyzing PostgreSQL performance, system resources, and multi-tenant metrics. It leverages Claude Code to perform intelligent analysis and generate professional, actionable reports.

## Prerequisites

- **Python 3.10 or higher**
- **Claude Code CLI** installed and configured
- **PostgreSQL 16** running on the system
- **Sudo access** for log file reading

## Installation & Setup

### Step 1: Create Virtual Environment

```bash
cd /home/ubuntu/postgres-optimization
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional - for email)

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit `.env` with your email configuration:

```env
EMAIL_FROM=your-email@example.com
EMAIL_TO=recipient1@example.com,recipient2@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
```

> **Note:** Email configuration is **OPTIONAL**. The script will work without it and simply skip sending emails.

## Usage

> **⚠️ IMPORTANT:** This script must be run **OUTSIDE** of an active Claude Code session. If you're currently in Claude, type `exit` first, then run the script.

### Basic Usage (No Email)

```bash
# Exit Claude if you're in a Claude session
exit

# Activate virtual environment and run the script
source venv/bin/activate
python claude_perf_automation.py
```

The script will:
1. Run comprehensive PostgreSQL performance analysis
2. Display a text summary in terminal
3. Save text summary to `reports/performance_report_YYYYMMDD_HHMMSS.txt`
4. Save HTML report to `reports/performance_analysis_report_DDMMYYYY.html`
5. Skip email sending if `.env` is not configured

### With Email (after configuring .env)

```bash
source venv/bin/activate
python claude_perf_automation.py
```

The script will additionally send an HTML-formatted email report.

### Automated Scheduling (Optional)

To run daily at 8 AM, add to crontab:

```bash
crontab -e
```

Then add:

```cron
0 8 * * * cd /home/ubuntu/postgres-optimization && /home/ubuntu/postgres-optimization/venv/bin/python /home/ubuntu/postgres-optimization/claude_perf_automation.py >> /home/ubuntu/postgres-optimization/cron.log 2>&1
```

## What the Script Analyzes

### 1. Database Performance
- Slow query logs (queries > 1000ms)
- Connection pool usage
- Missing indexes

### 2. System Resources
- CPU usage patterns
- Memory utilization
- Disk I/O bottlenecks

### 3. Multi-Tenant Metrics
- Per-tenant database size and growth
- Resource usage by subdomain
- Heavy user identification

### 4. Recommendations
- Prioritized optimization opportunities
- Quick wins (< 1 day implementation)
- Long-term improvements

## Output

| Type | Description | Location |
|------|-------------|----------|
| **Console Summary** | Text summary displayed on screen | Terminal output |
| **Text Summary** | Saved text report | `reports/performance_report_YYYYMMDD_HHMMSS.txt` |
| **HTML Report** | Styled HTML document for email | `reports/performance_analysis_report_DDMMYYYY.html` |
| **Email** | Professional HTML email | Sent to configured recipients |

## Troubleshooting

### Error: "claude command not found"
**Solution:** Ensure Claude Code CLI is installed and in your PATH

### Error: "Failed to save report"
**Solution:** Check that you have write permissions to the `reports/` directory

### Error: "Failed to send email"
**Solution:** Verify SMTP credentials in `.env` file are correct

### Error: "Permission denied" reading logs
**Solution:** Ensure the script is run by a user with sudo access to PostgreSQL logs

### Error: "Detected active Claude session"
**Solution:** Exit the current Claude Code session and run the script from your regular terminal

## Deactivating Virtual Environment

When done, deactivate the virtual environment:

```bash
deactivate
```

## Maintenance

- Reports are saved in `reports/` directory
- Old reports should be periodically cleaned up
- Check `cron.log` if using automated scheduling
- Review and update `.env` credentials as needed

## Project Structure

```
postgres-optimization/
├── claude_perf_automation.py    # Main automation script
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment configuration
├── .env                          # Your environment configuration (git-ignored)
├── venv/                         # Python virtual environment
├── reports/                      # Generated reports directory
│   ├── performance_report_*.txt
│   └── performance_analysis_report_*.html
└── README.md                     # This file
```

## Support

For issues with:
- **This script:** Check `CLAUDE.md` in this repository
- **Claude Code:** Visit [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues)
- **PostgreSQL:** Check `/var/log/postgresql/`

## Version

- **Script Version:** 1.0
- **Last Updated:** 2025-11-22
- **Python Version Required:** 3.10+

## License

This project is for internal PostgreSQL performance monitoring and optimization.

---

**Generated with Claude Code** - Automated PostgreSQL Performance Analysis
