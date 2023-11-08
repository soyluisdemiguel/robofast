# ChatGPT Plugin Skeleton

A FastAPI-based skeleton for creating ChatGPT plugins with Auth0 authentication and Stripe payment integration.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Introduction

This repository provides a skeleton project for creating plugins for ChatGPT. It's built with FastAPI and integrates Auth0 for user authentication and Stripe for handling payments. This skeleton can be used as a starting point for developing plugins that require user subscriptions.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- FastAPI
- Auth0 account
- Stripe account

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/chatgpt-plugin-skeleton.git
   cd chatgpt-plugin-skeleton

2. Install dependencies
   ```bash
   pipenv install
   ```
3. Setup the application on Heroku
   - You need to have `APP_` prefix for environment variables used in the application. You can change this behavior from `src/app/config.py` file.
   - Make sure you have these environment variables set correctly:
     - ENVIRONMENT
     - AUTH0_DOMAIN
     - AUTH0_CLIENT_ID
     - AUTH0_CLIENT_SECRET
     - AUTH0_API_IDENTIFIER
     - AUTH0_MGM_CLIENT_ID
     - AUTH0_MGM_CLIENT_SECRET
     - CHATGPT_AUTH_TOKEN
     - STRIPE_SECRET_KEY
     - STATE_SECRET_KEY
     - BASE_URL

#### Note
1. When choosing a name for your plugin, name used for model should follow this pattern: `[a-zA-Z][a-zA-Z0-9_]*`. 
2. After creating the plugin, you need to capture the call-back url and update your auth0 application to authorize it. 
You can find the call-back url in the logs of your application.
The call-back url should be in this format: `https://chat.openai.com/aip/plugin-{uuid}/oauth/callback`
3. Please check the `src/helpers/prompts.py` to adjust the prompt based on your use-case.
4. After creating your tenant on Auth0, you need to go to settings and set the default audience to the one created for this application. 
The ChatGPT doesn't support sending the audience in the request, so you need to set the default audience to the one created for this application.
5. To be able to run the setup script, you need to have all the environment variables set correctly. 
An easy solution is to either run the script on your deployment environment or set the environment variables in a `.env` file in the root of the project.