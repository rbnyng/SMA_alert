# SMA Crossover Checker

This repository contains a Python script and a GitHub Actions workflow for tracking the Simple Moving Averages (SMA) of the Vanguard Total Stock Market ETF (VTI). It calculates 15-day and 190-day SMAs and sends an email notification when the 15-day SMA crosses over or under the 190-day SMA, with a state-tracking feature to ensure notifications are sent only on state changes.

## Features

- **Automated SMA Tracking**: Automated calculation of 15-day and 190-day SMAs using GitHub Actions.
- **Stateful Email Notifications**: Sends an email notification only when the SMA crossover state changes (either crosses above or below).
- **Test Email Functionality**: Ability to trigger a test email to verify the setup.

## Setup and Configuration

### Prerequisites

- Python 3.x
- A GitHub account
- SMTP server credentials for sending emails (configured for Gmail)


### Configuring GitHub Secrets

Set up the following secrets in your GitHub repository for the email functionality:

- `SENDER_EMAIL`: Your email address for sending notifications.
- `SENDER_PASSWORD`: Your email password or app-specific password.
- `RECEIVER_EMAIL`: The email address to receive notifications.

### Usage

The script is primarily designed for automatic execution through GitHub Actions. It can be manually run for testing: python alert.py

### GitHub Actions Workflow

The `.github/workflows/main.yml` file schedules the workflow to run daily at 12 PM Eastern Time and allows manual triggering for sending a test email or checking the SMA crossover.

### State Tracking

The script tracks the state of the last SMA crossover in a file named `state.txt`. It ensures that email notifications are sent only when the crossover state changes.

### Sending a Test Email

Manually trigger the workflow in GitHub Actions with the `workflow_dispatch` event, and set `sendTestEmail` to `true` for sending a test email.
