from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import smtplib
import logging
import html
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self,
                 smtp_host: str = 'smtp-relay.brevo.com',
                 smtp_port: int = 587,
                 sender_email: str = '8735c8001@smtp-brevo.com',
                 sender_password: str = 'mxkEg24tMTwV3UH8'):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_contact_confirmation(self, recipient_email: str, submission_data: dict):
        """
        Send a contact form confirmation email with enhanced error handling
        
        :param recipient_email: Email address of the recipient
        :param submission_data: Dictionary containing submission details
        :return: Boolean indicating email sending success
        """
        try:
            # Extensive logging for debugging
            logger.info(f"Attempting to send email to {recipient_email}")
            logger.info(f"SMTP Configuration - Host: {self.smtp_host}, Port: {self.smtp_port}")
            logger.info(f"Sender Email: {self.sender_email}")

            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = 'Building India Digital - Contact Form Submission'

            # Sanitize input data to prevent potential injection
            name = html.escape(submission_data.get('name', 'Valued Customer'))
            email = html.escape(submission_data.get('email', 'N/A'))
            phone = html.escape(submission_data.get('phone', 'N/A'))
            message_text = html.escape(submission_data.get('message', 'N/A'))

            # Plain Text Version
            plain_text = f"""
            Dear {name},

            Thank you for reaching out to Building India Digital.

            We have received your contact form submission and will get back to you soon.

            Submission Details:
            - Name: {name}
            - Email: {email}
            - Phone: {phone}
            - Message: {message_text}

            Best regards,
            Building India Digital Team
            """

            # HTML Version
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Contact Form Submission</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                    }}
                    .header {{
                        background-color: #f4f4f4;
                        padding: 10px;
                        text-align: center;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    .content {{ padding: 20px; }}
                    .footer {{
                        text-align: center;
                        font-size: 12px;
                        color: #777;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Building India Digital</h2>
                    </div>
                    <div class="content">
                        <p>Dear {name},</p>

                        <p>Thank you for reaching out to Building India Digital. We have received your contact form submission and will get back to you soon.</p>

                        <h3>Submission Details:</h3>
                        <table>
                            <tr>
                                <td><strong>Name:</strong></td>
                                <td>{name}</td>
                            </tr>
                            <tr>
                                <td><strong>Email:</strong></td>
                                <td>{email}</td>
                            </tr>
                            <tr>
                                <td><strong>Phone:</strong></td>
                                <td>{phone}</td>
                            </tr>
                            <tr>
                                <td><strong>Message:</strong></td>
                                <td>{message_text}</td>
                            </tr>
                        </table>

                        <p>Best regards,<br>Building India Digital Team</p>
                    </div>
                    <div class="footer">
                        <p>&copy; 2025 Building India Digital. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Attach both plain text and HTML versions
            part1 = MIMEText(plain_text, 'plain')
            part2 = MIMEText(html_content, 'html')

            message.attach(part1)
            message.attach(part2)

            # Create secure context
            context = ssl.create_default_context()

            # Sending logic with comprehensive error handling
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                try:
                    # Start TLS for security
                    server.starttls(context=context)
                    
                    # Login
                    server.login(self.sender_email, self.sender_password)
                    
                    # Send email
                    server.send_message(message)
                    
                    logger.info(f"Email sent successfully to {recipient_email}")
                    return True
                
                except smtplib.SMTPAuthenticationError as auth_error:
                    logger.error(f"SMTP Authentication Failed: {auth_error}")
                    logger.error(f"Check SMTP credentials for {self.sender_email}")
                    return False
                
                except smtplib.SMTPException as smtp_error:
                    logger.error(f"SMTP Sending Error: {smtp_error}")
                    return False
        
        except Exception as e:
            logger.error(f"Unexpected error in email sending: {e}")
            return False

    def test_email_sending(self, test_recipient: str):
        """
        Test email sending functionality
        
        :param test_recipient: Email address to send test email
        :return: Boolean indicating test email sending success
        """
        test_data = {
            'name': 'Test User',
            'email': test_recipient,
            'phone': '1234567890',
            'message': 'This is a test email to verify email sending functionality.'
        }
        
        return self.send_contact_confirmation(test_recipient, test_data)