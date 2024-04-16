---
date: 2024-04-16T09:08:56.752987
author: AutoGPT <info@agpt.co>
---

# aarushi-currency-exchange-1

The endpoint design is focused on performing currency conversions by accepting a base currency and optionally one or more target currency codes. Leveraging the Python programming language with the FastAPI framework, the application will provide fast, asynchronous API responses. The backend will interact with PostgreSQL through Prisma, an ORM that offers robust data management and ease of use for Python developers.

To fulfill the task requirements, the API will perform the following steps:
1. Accept a GET request with query parameters for the base currency (e.g., 'GBP') and target currency/currencies.
2. Use the provided financial data APIs, such as Open Exchange Rates or CurrencyLayer, as the reliable sources for real-time exchange rate data. This choice is based on the search results for reliable sources.
3. Implement an async function that fetches the latest exchange rates from the chosen API. This function will handle converting the base currency to the target currencies specified by the user. If 'all of them' is specified as the target, the function will fetch the exchange rates for the base currency against every available currency provided by the API.
4. Calculate the exchange rate between the base and the target currencies using the data retrieved. This involves a straightforward calculation if direct rates are available, or a conversion path if direct rates are not provided.
5. Format the response to include the exchange rate(s), the base currency, and target currencies, alongside a timestamp marking the exact time of the currency rate retrieval.

This setup ensures scalability for supporting multiple currencies, efficiency in fetching and calculating real-time exchange rates, and reliability by utilizing trusted financial data sources. The endpoint will be well-documented to guide users on how to specify base and target currencies correctly.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-currency-exchange-1'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
