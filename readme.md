# CRM Database Chatbot

Welcome to the CRM Database Chatbot project!

## Overview

This project features a chatbot designed to interact with a CRM database, allowing users to ask questions in natural language about CRM data. The chatbot converts these questions into SQL queries, retrieves relevant data, and provides responses in easy-to-understand natural language. Additionally, it supports generating visualizations such as line and bar charts to help users gain insights from the data.

## Features

- **Natural Language Queries:** Ask questions in plain language about CRM data.
- **SQL Query Generation:** The chatbot converts your questions into SQL queries.
- **Data Visualization:** Generate line and bar charts based on the data.
- **Tabular Data Display:** View data in tabular format when requested.

## Tech Stack

- **LangChain:** For building and managing language models and their interactions.
- **Google Gemini API:** Provides generative AI capabilities for interpreting and processing natural language queries.
- **Pandas:** For data manipulation and analysis.
- **Streamlit:** For creating interactive web applications.
- **Matplotlib & Seaborn:** For generating visualizations and charts.
- **SQLAlchemy:** For interacting with the database.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/crm-database-chatbot.git
   cd crm-database-chatbot
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   You may also create and activate a virtual environment if desired.

## Usage

1. **Run the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the chatbot:**

   - Open the Streamlit application in your browser.
   - Type your queries into the chat input field.
   - The chatbot will process your query, generate SQL commands, retrieve data, and provide responses.

