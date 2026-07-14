#!/usr/bin/env python3
"""
Day 66 - Email Sending
Demonstrates sending emails using SMTP
"""

import os
import json
from email_sender import EmailSender


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def setup_credentials():
    """Set up email credentials"""
    print("\n" + "="*60)
    print("EMAIL SETUP")
    print("="*60)
    print("""
For Gmail:
  1. Go to Google Account > Security
  2. Enable 2-Step Verification
  3. Generate App Password
  4. Use App Password instead of regular password

For testing:
  - Use a test email account
  - Never commit credentials to GitHub
    """)
    
    smtp_server = input("SMTP Server (default: smtp.gmail.com): ").strip()
    if not smtp_server:
        smtp_server = "smtp.gmail.com"
    
    smtp_port = input("SMTP Port (default: 587): ").strip()
    if not smtp_port:
        smtp_port = 587
    else:
        smtp_port = int(smtp_port)
    
    username = input("Email Address: ").strip()
    password = input("Password/App Password: ").strip()
    
    return smtp_server, smtp_port, username, password


def demo_test_email(sender: EmailSender):
    """Demonstrate sending a test email"""
    print_section("1. SEND TEST EMAIL")
    
    to_email = input("Enter recipient email: ").strip()
    if not to_email:
        print("No email entered, skipping...")
        return
    
    if sender.send_test_email(to_email):
        print("[OK] Test email sent successfully!")
    else:
        print("[ERROR] Failed to send test email")


def demo_welcome_email(sender: EmailSender):
    """Demonstrate sending a welcome email"""
    print_section("2. SEND WELCOME EMAIL")
    
    to_email = input("Enter recipient email: ").strip()
    if not to_email:
        print("No email entered, skipping...")
        return
    
    name = input("Enter recipient name: ").strip()
    if not name:
        name = "User"
    
    if sender.send_welcome_email(to_email, name):
        print("[OK] Welcome email sent successfully!")
    else:
        print("[ERROR] Failed to send welcome email")


def demo_report_email(sender: EmailSender):
    """Demonstrate sending a report email"""
    print_section("3. SEND REPORT EMAIL")
    
    to_email = input("Enter recipient email: ").strip()
    if not to_email:
        print("No email entered, skipping...")
        return
    
    report_data = {
        'Date': '2026-07-14',
        'Total Users': '1,234',
        'Active Users': '567',
        'Revenue': '45,678.90 TRY',
        'New Signups': '23',
        'Page Views': '12,345'
    }
    
    print("\nReport Data:")
    for key, value in report_data.items():
        print(f"  {key}: {value}")
    
    if sender.send_report_email(to_email, report_data):
        print("[OK] Report email sent successfully!")
    else:
        print("[ERROR] Failed to send report email")


def demo_custom_email(sender: EmailSender):
    """Demonstrate sending a custom email"""
    print_section("4. SEND CUSTOM EMAIL")
    
    to_email = input("Enter recipient email: ").strip()
    if not to_email:
        print("No email entered, skipping...")
        return
    
    subject = input("Enter subject: ").strip()
    if not subject:
        subject = "Custom Email from Python"
    
    print("Enter message body (type 'END' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    
    body = "\n".join(lines)
    
    if sender.send_email(to_email, subject, body):
        print("[OK] Custom email sent successfully!")
    else:
        print("[ERROR] Failed to send custom email")


def demo_send_to_multiple(sender: EmailSender):
    """Demonstrate sending to multiple recipients"""
    print_section("5. SEND TO MULTIPLE RECIPIENTS")
    
    emails_input = input("Enter emails (comma separated): ").strip()
    if not emails_input:
        print("No emails entered, skipping...")
        return
    
    emails = [email.strip() for email in emails_input.split(',')]
    
    subject = "Python Email - Multiple Recipients"
    body = f"""
    Hello,

    This email was sent to multiple recipients using Python!

    Sent at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Regards,
    Python Email Sender
    """
    
    success_count = 0
    for email in emails:
        if sender.send_email(email, subject, body):
            success_count += 1
            print(f"  [OK] Sent to {email}")
        else:
            print(f"  [ERROR] Failed to send to {email}")
    
    print(f"\n[OK] Sent successfully to {success_count}/{len(emails)} recipients")


def demo_html_email(sender: EmailSender):
    """Demonstrate sending HTML email"""
    print_section("6. SEND HTML EMAIL")
    
    to_email = input("Enter recipient email: ").strip()
    if not to_email:
        print("No email entered, skipping...")
        return
    
    html_body = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .header { background: #4CAF50; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center; }
            .content { padding: 20px; }
            .footer { background: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; color: #888; }
            .button { display: inline-block; background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>HTML Email Demo</h1>
            </div>
            <div class="content">
                <h2>Hello from Python!</h2>
                <p>This is an <strong>HTML email</strong> sent from Python using <code>smtplib</code>.</p>
                <p>You can style your emails with:</p>
                <ul>
                    <li>Colors</li>
                    <li>Fonts</li>
                    <li>Buttons</li>
                    <li>Images</li>
                </ul>
                <a href="#" class="button">Learn More</a>
            </div>
            <div class="footer">
                <p>Sent at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Python Email Sender</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    subject = "HTML Email from Python"
    
    if sender.send_email(to_email, subject, html_body, html=True):
        print("[OK] HTML email sent successfully!")
    else:
        print("[ERROR] Failed to send HTML email")


def main():
    print("=" * 60)
    print("DAY 66 - EMAIL SENDING")
    print("=" * 60 + "\n")
    
    print("WARNING: This demo requires email credentials.")
    print("For Gmail, use App Password instead of your regular password.")
    print("Your credentials will NOT be stored.\n")
    
    # Setup
    smtp_server, smtp_port, username, password = setup_credentials()
    
    if not username or not password:
        print("[ERROR] Email credentials required!")
        return
    
    sender = EmailSender(smtp_server, smtp_port, username, password)
    
    # Menus
    while True:
        print("\n" + "="*60)
        print("EMAIL SENDER MENU")
        print("="*60)
        print("1. Send Test Email")
        print("2. Send Welcome Email")
        print("3. Send Report Email")
        print("4. Send Custom Email")
        print("5. Send to Multiple Recipients")
        print("6. Send HTML Email")
        print("7. Exit")
        print("="*60)
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            demo_test_email(sender)
        elif choice == "2":
            demo_welcome_email(sender)
        elif choice == "3":
            demo_report_email(sender)
        elif choice == "4":
            demo_custom_email(sender)
        elif choice == "5":
            demo_send_to_multiple(sender)
        elif choice == "6":
            demo_html_email(sender)
        elif choice == "7":
            print("\n[OK] Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    import datetime
    main()
