# PayJoy Currency Converter - Technical Assessment - Jorge Tuesta

Automation Engineer (Tools Specialist) Assessment Solution

---

## Overview

This solution automates the customer question: *"What is the exchange rate for my currency?"*

It consists of three components:
- REST API: Converts USD amounts to target currency using live exchange rates
- Chatbot Flow: Landbot integration for conversational customer experience
- Documentation: This README

---

## How to run the API locally

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup steps

1. **Clone the repository**

    git clone <your-repo-url>
    cd payjoy-assessment


2. **Install dependencies**

    pip install -r requirements.txt


3. **Set up environment variables** (see next section)

4. **Run the API**

    python api/main.py

5. **Test the API**

In another terminal:

    curl "http://127.0.0.1:8000/convert?amount=200&currency=BRL"


    Expected response:
    {
    "amount_usd": 200,
    "currency": "BRL",
    "converted": 1045.80,
    "rate": 5.229
    }

---

## Environment variables setup

### Getting your ExchangeRate API key

1. Go to https://www.exchangerate-api.com
2. Sign up (free tier, no credit card required)
3. Confirm your email
4. Copy your API key from the dashboard

### Creating .env file

1. In the root of your project, create a file named `.env` (note: no extension)
2. Add your credentials (check **.env.example**):

    EXCHANGERATE_API_KEY=your_api_key_here
    EXCHANGERATE_API_URL=https://v6.exchangerate-api.com/v6

**Important:** Never commit `.env` to version control. Use `.env.example` as a template for other developers.

---

## Technical choices & architecture

### Why Python + FastAPI?

- Python: Rapid development, clean syntax, strong ecosystem for APIs
- FastAPI: Modern, fast, automatic API documentation, built-in validation with Pydantic, async support for concurrent requests

### Why Landbot for the Chatbot?

- Free tier available with webhook support
- No-code interface for quick integration
- Supports JSON parsing from external APIs
- Good for MVP/demo purposes

### Project Structure

payjoy-assessment/
├── api/
│ └── main.py # FastAPI application with /convert endpoint
├── requirements.txt # Python dependencies
├── .env # Your API credentials (DO NOT COMMIT)
├── .env.example # Template for environment variables
└── README.md # This file


### Key Design Decisions

1. Single endpoint ("/convert"): Simplicity and focus on the core requirement
2. Input validation: Check for positive amounts and valid 3-letter currency codes before calling external API
3. Error handling: Separate handling for missing parameters, invalid currencies, API failures, and network errors
4. Async function: Allows concurrent requests without blocking
5. Health check endpoint: ("/health") for monitoring API availability
6. Environment variables: API key never hardcoded for security
7. Timeout on external calls: 5-second timeout prevents hanging requests to ExchangeRate API

---

## Chatbot Flow (Landbot)

The chatbot follows this sequence:

1. **Greeting**: "Hi 😀 Welcome to PayJoy. What is the monthly installment on your phone in USD?"
   - Input: Captures `amount` as a number (regex pattern restriction - only real numbers)

2. **Currency Selection**: "Please enter your currency."
   - Input: Captures `currency` as text (regex pattern restriction - 3 letters and uppercase)

3. **Webhook Call**: Sends GET request to API endpoint with `amount` and `currency` parameters
    - Output: `converted` key from response json.
    - Output: `detail` key from response json.

4. **Result Display**: Shows the converted amount in a friendly message
   - Success (API reponse 200): "Your monthly payment is:  `converted` `currency`. Thanks!"
   - Error(API response 400): "Error🫣: `detail`. Please try again."
   - Error(API response another code): "API not available 😱. Try again later!"

---

## What I would improve with more time

### Short term
- Trim whitespace, convert currency to uppercase automatically
- More user-friendly messages in the chatbot when errors occur
- Implement rate limiting to prevent abuse (e.g., max 100 requests/minute)
- Add structured logging to track API calls and errors

### Medium term
- Store conversion history for analytics (SQLAlchemy + PostgreSQL)
- Add API key authentication for the endpoint
- Containerize the API for easier deployment

### Long term
- Localize chatbot messages based on user locale(multiple languages)
- Retry logic with exponential backoff for external API failures
- Track conversion patterns, popular currencies, peak usage times
- Test different chatbot flows and messaging

---

## How to Measure Success in Production

### Key Metrics to Track

1. API Performance:
   - Response time (target: <500ms)
   - Availability/uptime (target: 99.9%)
   - Error rate (target: <1%)
   - Request volume per hour/day

2. Chatbot Engagement:
   - Conversation completion rate (% of users who complete the flow)
   - Conversation drop-off rate (where do users abandon)
   - Average conversation duration
   - Error recovery rate (% of users who retry after an error)

3. User Satisfaction:
   - User feedback/sentiment analysis
   - Support tickets related to currency conversion

4. Business Metrics:
   - Reduction in manual agent support (time saved per query)
   - Cost per conversation (API costs vs. agent cost)
   - Conversion to purchase after currency question answered
   - Customer retention (do users who use the bot have better retention?)


## Dependencies

See requirements.txt:
- fastapi - Web framework
- uvicorn - ASGI server
- python-dotenv - Environment variable management
- requests - HTTP client for external API calls
- pydantic - Data validation

---


---

## Exposing the API with ngrok (For Landbot Integration)

Since Landbot requires HTTPS and your API runs on localhost (http), use **ngrok** to expose it to the internet with a secure HTTPS URL.

### Step 1: Install ngrok

Download from: https://ngrok.com/download

### Step 2: Create a Free ngrok Account

1. Go to https://ngrok.com
2. Sign up for a free account
3. Copy your authtoken from the dashboard

### Step 3: Connect ngrok with your token

    ngrok config add-authtoken your_authtoken_here

### Step 4: Start ngrok

Make sure your API is running in one terminal:

    python api/main.py

In a new terminal, expose your API:

    ngrok http 8000

    Copy the HTTPS URL (e.g., `https://abc123def456.ngrok.io`)

### Step 5: Use in Landbot

In your Landbot webhook configuration, use:

    https://abc123def456.ngrok.io/convert

## Author

Jorge Tuesta