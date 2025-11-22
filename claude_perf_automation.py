#!/usr/bin/env python3
import subprocess
import os
import sys
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class ClaudeCodeAutomation:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.report_dir = '/home/ubuntu/postgres-optimization/reports'

        # Load environment variables from .env file
        env_path = '/home/ubuntu/postgres-optimization/.env'
        if os.path.exists(env_path):
            load_dotenv(env_path)
            self.log(f"Loaded environment variables from {env_path}")

    def log(self, message):
        """Print log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    def run_claude_analysis(self):
        """Execute Claude Code for performance analysis"""

        # Check if we're already in a Claude session
        if os.getenv('CLAUDE_SESSION') or os.path.exists('/tmp/claude-active-session'):
            self.log("WARNING: Detected active Claude session. This script should be run OUTSIDE of Claude.")
            self.log("Please exit Claude and run this script directly from the terminal.")
            return None, None

        self.log("Starting Claude Code performance analysis...")

        # Generate filename with current date
        timestamp = datetime.now().strftime('%d%m%Y')
        html_filename = f'performance_analysis_report_{timestamp}.html'
        html_filepath = os.path.join(self.report_dir, html_filename)

        analysis_prompt = f"""Please perform a comprehensive performance analysis and save the results as a complete HTML report.

IMPORTANT: Save the HTML report to: {html_filepath}

ANALYSIS REQUIREMENTS:
1. **Database Performance**
   - Check PostgreSQL slow query logs
   - Analyze connection pool usage
   - Identify queries > 1000ms
   - Check for missing indexes

2. **System Resources**
   - CPU usage patterns
   - Memory utilization
   - Disk I/O bottlenecks

3. **Multi-Tenant Metrics**
   - Per-tenant database size and growth
   - Resource usage by subdomain
   - Heavy user identification

4. **Recommendations**
   - Prioritized optimization opportunities
   - Quick wins (< 1 day implementation)
   - Long-term improvements

REPORT MUST INCLUDE:
- Executive summary with top 3 critical issues
- Detailed findings with metrics
- Actionable recommendations
- SQL optimization scripts where applicable

HTML REQUIREMENTS:
- Complete HTML document with proper structure
- Embedded CSS styling for professional email formatting
- Styled tables, code blocks, and clear section headings
- Make it visually appealing and easy to read

Analyze logs from the last 24 hours.

CRITICAL: Save the complete HTML report to {html_filepath}"""

        try:
            # Create a temporary prompt file
            prompt_file = '/tmp/claude_analysis_prompt.txt'
            with open(prompt_file, 'w') as f:
                f.write(analysis_prompt)

            # Run claude with the prompt from stdin
            self.log("Executing Claude Code analysis (this may take several minutes)...")

            with open(prompt_file, 'r') as f:
                result = subprocess.run(
                    ['claude', '--dangerously-skip-permissions'],
                    stdin=f,
                    cwd='/home/ubuntu/postgres-optimization',
                    capture_output=True,
                    text=True,
                    timeout=600
                )

            # Clean up prompt file
            os.remove(prompt_file)

            if result.returncode != 0:
                self.log(f"ERROR: Claude Code returned exit code {result.returncode}")
                if result.stderr:
                    self.log(f"STDERR: {result.stderr}")
                return None, None

            self.log("Analysis completed successfully")

            # Read the HTML file that Claude generated
            if os.path.exists(html_filepath):
                with open(html_filepath, 'r') as f:
                    html_content = f.read()
                self.log(f"HTML report loaded from: {html_filepath}")
                return result.stdout, html_content
            else:
                self.log(f"WARNING: HTML file not found at {html_filepath}, using stdout")
                return result.stdout, None

        except subprocess.TimeoutExpired:
            self.log("ERROR: Claude Code analysis timed out after 600 seconds")
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
            return None, None
        except FileNotFoundError:
            self.log("ERROR: 'claude' command not found. Is Claude Code installed?")
            return None, None
        except Exception as e:
            self.log(f"ERROR: Unexpected error running Claude Code: {str(e)}")
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
            return None, None

    def save_report(self, content):
        """Save report to file"""
        try:
            # Create reports directory if it doesn't exist
            os.makedirs(self.report_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'performance_report_{timestamp}.txt'
            filepath = os.path.join(self.report_dir, filename)

            with open(filepath, 'w') as f:
                f.write(content)

            self.log(f"Report saved to: {filepath}")
            return filepath

        except Exception as e:
            self.log(f"ERROR: Failed to save report: {str(e)}")
            return None

    def get_html_content(self, report_content):
        """Extract or use HTML content directly from Claude's output"""
        # Claude is now generating HTML directly, so we just return it
        # If the output doesn't contain HTML tags, wrap it in basic HTML
        if '<html' in report_content.lower():
            return report_content
        else:
            # Fallback in case Claude didn't output HTML
            self.log("WARNING: Output doesn't appear to be HTML, wrapping in basic HTML")
            return f'''<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
<pre>{report_content}</pre>
</body>
</html>'''

    def send_email_report(self, html_content):
        """Send email with HTML formatted report"""

        # Check if email env vars are set
        required_vars = ['EMAIL_FROM', 'EMAIL_TO', 'SMTP_HOST', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            self.log(f"WARNING: Email sending skipped - missing env vars: {', '.join(missing_vars)}")
            return False

        if not html_content:
            self.log("ERROR: No HTML content to send")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Daily PostgreSQL Performance Report - {datetime.now().strftime("%Y-%m-%d")}'
            msg['From'] = os.getenv('EMAIL_FROM')
            msg['To'] = ', '.join(os.getenv('EMAIL_TO').split(','))

            # Use the HTML content directly from the file
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as server:
                server.starttls()
                server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD'))
                server.send_message(msg)

            self.log("Email report sent successfully")
            return True

        except Exception as e:
            self.log(f"ERROR: Failed to send email: {str(e)}")
            return False

def main():
    """Main execution function"""
    automation = ClaudeCodeAutomation(verbose=True)

    print("=" * 80)
    print("PostgreSQL Performance Analysis Automation")
    print("=" * 80)
    print()

    # Run analysis - returns both summary and HTML content
    summary, html_content = automation.run_claude_analysis()

    if not summary:
        print("\nERROR: Failed to generate analysis report")
        sys.exit(1)

    # Display summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(summary)
    print("=" * 80)

    # Save text summary
    filepath = automation.save_report(summary)

    # Send email with HTML content if available
    if html_content:
        automation.send_email_report(html_content)
        print(f"\nHTML report ready for email")
    else:
        print("\nWARNING: HTML report not generated, email not sent")

    print("\nAnalysis complete!")
    if filepath:
        print(f"Summary saved to: {filepath}")

if __name__ == "__main__":
    main()
