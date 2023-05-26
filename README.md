# Notion Google Flights

## Description

This program parses emails from Google Flight Alerts and creates a Notion database record with the contents.

Useful for tracking flight prices and getting a sense of how they change over time.

To be used in combination with the corresponding notion Template for easy setup.

## Setup

First create a mail account for the program to use, and then forward all emails from Google Flights to it automatically.

Add a `.env` file (alongside `main.py`) with the following variables:

- NOTION_KEY: Your Notion API key
- NOTION_DB_TRAVEL: The ID of the PriceNotificationDB in the template
- NOTION_DB_OPERATOR: The ID of the OperatorDB in the template
- NOTION_DB_DESTINATION: The ID of the DestinationDB in the template

- EMAIL_IMAP: The IMAP server of your email provider
- EMAIL_USERNAME: Your email address
- EMAIL_PASSWORD: Your email password

To get ID of a database, copy the URL of the database and extract the ID from it.

Add the main.py script to your crontab to run it periodically.
