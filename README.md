================================================================================
PostgreSQL Performance Analysis Automation
================================================================================

OVERVIEW
--------
This script automates PostgreSQL performance analysis using Claude Code.
It generates comprehensive HTML reports and optionally emails them to
specified recipients.

PREREQUISITES
-------------
1. Python 3.10 or higher
2. Claude Code CLI installed and configured
3. PostgreSQL 16 running on the system
4. Sudo access for log file reading

INSTALLATION & SETUP
--------------------

Step 1: Create Virtual Environment
-----------------------------------
cd /home/ubuntu/postgres-optimization
python3 -m venv venv

Step 2: Activate Virtual Environment
------------------------------------
source venv/bin/activate

Step 3: Install Dependencies
----------------------------
pip install -r requirements.txt

Step 4: Configure Environment Variables (Optional - for email)
--------------------------------------------------------------
Create a .env file in /home/ubuntu/postgres-optimization/ with:

EMAIL_FROM=your-email@example.com
EMAIL_TO=recipient1@example.com,recipient2@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password

Note: Email configuration is OPTIONAL. The script will work without it
and simply skip sending emails.

USAGE
-----

IMPORTANT: This script must be run OUTSIDE of an active Claude Code session.
If you're currently in Claude, type 'exit' first, then run the script.

Basic Usage (No Email):
-----------------------
# Exit Claude if you're in a Claude session
exit

# Then run the script
source venv/bin/activate
python claude_perf_automation.py

The script will:
1. Run comprehensive PostgreSQL performance analysis
2. Display the HTML report in terminal
3. Save report to reports/performance_report_YYYYMMDD_HHMMSS.txt
4. Skip email sending if .env is not configured

With Email (after configuring .env):
------------------------------------
source venv/bin/activate
python claude_perf_automation.py

The script will additionally send an HTML-formatted email report.

AUTOMATED SCHEDULING (Optional)
--------------------------------
To run daily at 8 AM, add to crontab:

crontab -e

Then add:
0 8 * * * cd /home/ubuntu/postgres-optimization && /home/ubuntu/postgres-optimization/venv/bin/python /home/ubuntu/postgres-optimization/claude_perf_automation.py >> /home/ubuntu/postgres-optimization/cron.log 2>&1

WHAT THE SCRIPT ANALYZES
-------------------------
1. Database Performance
   - Slow query logs (queries > 1000ms)
   - Connection pool usage
   - Missing indexes

2. System Resources
   - CPU usage patterns
   - Memory utilization
   - Disk I/O bottlenecks

3. Multi-Tenant Metrics
   - Per-tenant database size and growth
   - Resource usage by subdomain
   - Heavy user identification

4. Recommendations
   - Prioritized optimization opportunities
   - Quick wins (< 1 day implementation)
   - Long-term improvements

OUTPUT
------
- Console Summary: Text summary displayed on screen
- Text Summary: Saved to reports/performance_report_YYYYMMDD_HHMMSS.txt
- HTML Report: Styled HTML document saved to reports/performance_analysis_report_DDMMYYYY.html
- Email: Professional HTML email using the HTML report (if configured)

TROUBLESHOOTING
---------------

Error: "claude command not found"
Solution: Ensure Claude Code CLI is installed and in your PATH

Error: "Failed to save report"
Solution: Check that you have write permissions to the reports/ directory

Error: "Failed to send email"
Solution: Verify SMTP credentials in .env file are correct

Error: "Permission denied" reading logs
Solution: Ensure the script is run by a user with sudo access to PostgreSQL logs

DEACTIVATING VIRTUAL ENVIRONMENT
---------------------------------
When done, deactivate the virtual environment:
deactivate

MAINTENANCE
-----------
- Reports are saved in reports/ directory
- Old reports should be periodically cleaned up
- Check cron.log if using automated scheduling

SUPPORT
-------
For issues with:
- This script: Check /home/ubuntu/postgres-optimization/CLAUDE.md
- Claude Code: Visit https://github.com/anthropics/claude-code/issues
- PostgreSQL: Check /var/log/postgresql/

VERSION
-------
Script Version: 1.0
Last Updated: 2025-11-22
Python Version Required: 3.10+

================================================================================
