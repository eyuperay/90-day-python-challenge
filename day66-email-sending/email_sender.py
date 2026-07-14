"""
Email Sender Module
Sends emails using SMTP
"""

import smtplib
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import json


class EmailSender:
    """Email sender using SMTP"""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", 
                 smtp_port: int = 587,
                 username: str = None,
                 password: str = None):
        """
        Initialize email sender
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port (587 for TLS, 465 for SSL)
            username: Email username
            password: Email password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.log_file = "logs/email.log"
        
        os.makedirs("logs", exist_ok=True)
    
    def log(self, message: str):
        """Log email activity"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def send_email(self, to_email: str, subject: str, body: str,
                   from_email: str = None, html: bool = False,
                   attachments: List[str] = None) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            from_email: Sender email address (default: username)
            html: Whether body is HTML
            attachments: List of file paths to attach
        
        Returns:
            True if sent successfully, False otherwise
        """
        if from_email is None:
            from_email = self.username
        
        if not self.username or not self.password:
            self.log("ERROR: Email credentials not set")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach body
            if html:
                body_part = MIMEText(body, 'html')
            else:
                body_part = MIMEText(body, 'plain')
            msg.attach(body_part)
            
            # Attach files
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            self.log(f"Email sent to: {to_email} - Subject: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            self.log(f"SMTP Authentication Error: {e}")
            return False
        except smtplib.SMTPException as e:
            self.log(f"SMTP Error: {e}")
            return False
        except Exception as e:
            self.log(f"Error sending email: {e}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach a file to email"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                
                filename = os.path.basename(file_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"'
                )
                msg.attach(part)
                self.log(f"Attached file: {filename}")
                
        except Exception as e:
            self.log(f"Error attaching file {file_path}: {e}")
    
    def send_test_email(self, to_email: str) -> bool:
        """Send a test email"""
        subject = "Python Email Test"
        body = f"""
        Hello,

        This is a test email sent from Python!

        Sent at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        If you received this, your email setup is working correctly!

        Regards,
        Python Email Sender
        """
        
        return self.send_email(to_email, subject, body)
    
    def send_welcome_email(self, to_email: str, name: str) -> bool:
        """Send a welcome email"""
        subject = f"Welcome {name}!"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px;">
            <h2 style="color: #4CAF50;">Welcome!</h2>
            <p>Dear <strong>{name}</strong>,</p>
            <p>Thank you for joining our community!</p>
            <p>We're excited to have you on board.</p>
            <hr>
            <p style="color: #888; font-size: 12px;">
                This is an automated email. Please do not reply to this email.
            </p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, html=True)
    
    def send_report_email(self, to_email: str, report_data: dict) -> bool:
        """Send a report email"""
        subject = "Daily Report"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px;">
            <h2 style="color: #4CAF50;">Daily Report</h2>
            <p><strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <table style="border-collapse: collapse; width: 100%%;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Metric</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Value</th>
                </tr>
        """
        
        for key, value in report_data.items():
            body += f"""
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">{key}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{value}</td>
                </tr>
            """
        
        body += """
            </table>
            <hr>
            <p style="color: #888; font-size: 12px;">
                This is an automated report. Please do not reply to this email.
            </p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, html=True)
    
    def save_credentials(self, filename: str = "credentials.json"):
        """Save credentials to file (encrypted in production)"""
        creds = {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'username': self.username,
            'password': '***'  # Don't save password in plain text
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(creds, f, indent=2)
        
        self.log(f"Credentials saved to {filename}")
    
    def load_credentials(self, filename: str = "credentials.json") -> bool:
        """Load credentials from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                creds = json.load(f)
            
            self.smtp_server = creds.get('smtp_server', self.smtp_server)
            self.smtp_port = creds.get('smtp_port', self.smtp_port)
            self.username = creds.get('username', self.username)
            
            self.log(f"Credentials loaded from {filename}")
            return True
            
        except FileNotFoundError:
            self.log(f"Credentials file not found: {filename}")
            return False
        except Exception as e:
            self.log(f"Error loading credentials: {e}")
            return False
