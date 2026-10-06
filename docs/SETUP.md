# Ben 10 Market - Setup Guide

This guide explains how to set up and run the Ben 10 Market application.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A Telegram account
- Google Cloud Platform account (for Google Sheets integration)

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `.env.example` file to `.env`:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file and fill in the required values:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
   - `ALIEXPRESS_API_KEY`: Your AliExpress API key (optional for now)
   - `GOOGLE_SHEETS_CREDENTIALS_JSON`: Path to your Google Sheets service account JSON file
   - `SPREADSHEET_ID`: Your Google Spreadsheet ID

## Google Sheets Setup

1. Create a Google Cloud Project
2. Enable the Google Sheets API and Google Drive API
3. Create a Service Account and download the JSON credentials file
4. Share your Google Sheet with the service account email (found in the JSON file)
5. Update the `GOOGLE_SHEETS_CREDENTIALS_JSON` and `SPREADSHEET_ID` in your `.env` file

## Running the Application

To start the Telegram bot:
```
python src/main.py
```

To run integration tests:
```
python test_integration.py
```

## Using the Bot

1. Find your bot on Telegram using the bot username
2. Send `/start` to initialize the bot
3. Use the buttons to interact with the application:
   - "Получить актуальный отчет" - Generate and upload a market analysis report
   - "Настройки парсинга" - Configure data source settings
   - "Синхронизировать БД" - Sync the local database

## Development

The project follows these architectural principles:
- Strict separation of concerns between backend and frontend layers
- Asynchronous programming for network operations
- Comprehensive error handling and logging
- Retry mechanisms with exponential backoff for network resilience

## Troubleshooting

If you encounter issues:
1. Check that all environment variables are properly configured
2. Verify that your Google Sheets credentials are correct
3. Ensure your Telegram bot token is valid
4. Check the `app.log` file for detailed error messages