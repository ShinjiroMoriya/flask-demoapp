from app import app
import sendgrid

sg = sendgrid.SendGridClient(app.config.get('SENDGRID_API_KEY'))
