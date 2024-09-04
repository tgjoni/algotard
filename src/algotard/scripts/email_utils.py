"""Email utils to notfiy admins."""

import os

import mailjet_rest
from dotenv import load_dotenv

load_dotenv()


MAILJET_API_KEY = os.environ["MAILJET_API_KEY"]
MAILJET_API_SECRET = os.environ["MAILJET_API_SECRET"]


def get_emails_to_send() -> list[str]:
    """Get the emails of users to notify from env.

    Returns
    -------
    list[str]
        List of emails to notify.
    """
    emails = os.environ["MAILJET_SEND_EMAIL"].split(",")
    return emails


def format_emails_mailjet(emails: list[str]) -> list[dict[str, str]]:
    """Format emails for Mailjet.

    Parameters
    ----------
    emails : list[str]
        List of emails to notify.

    Returns
    -------
    list[dict[str, str]]
        Format for emails to pass for Mailjet API.
    """
    return [{"Email": v} for v in emails]


def send_email(subject: str, body: str, emails: list[dict[str, str]]) -> None:
    """Send email to users.

    Parameters
    ----------
    subject : str
        Subject of the email
    body : str
        Body of the email
    emails : list[dict[str, str]]
        Emails formatted for Mailjet
    """

    # Intialize the Mailjet API
    mailjet = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version="v3.1"
    )
    # Format the data.
    data = {
        "Messages": [
            {
                "From": {"Email": "support@momentomori.me", "Name": "Algotard"},
                "To": emails,
                "Subject": subject,
                "TextPart": body,
            }
        ]
    }
    # Send the email
    mailjet.send.create(data=data)
