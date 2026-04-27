import asyncio
from app.logger import get_logger

logger = get_logger(__name__)

async def send_email(to_email: str, subject: str, body: str):
    """
    Simulates sending an email via an external SMTP service (like SendGrid).
    In a real app, this would use aiosmtplib or an HTTP client.
    """
    logger.info(f"Preparing to send email to {to_email}...")
    await asyncio.sleep(2)  # Simulate network latency
    logger.info(f"[EMAIL SENT] To: {to_email} | Subject: {subject} | Body: {body}")

async def send_stock_alert(product_name: str, current_stock: int):
    """
    Simulates sending an alert to the warehouse/management channel.
    """
    logger.info(f"Preparing to send low stock alert for {product_name}...")
    await asyncio.sleep(1)  # Simulate latency
    logger.info(f"[ALERT SENT] Low stock for {product_name}! Only {current_stock} remaining.")
