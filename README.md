# LLM Web Scraper

[![Download](https://img.shields.io/badge/Download-Windows_App-blue?style=for-the-badge&logo=windows)](https://github.com/matchacone/WebbyScraper/releases/latest)

Hi! This is my first ever app that I've ever made in Python. It's not the best but I figured that its a good starting point in my journey to becoming a SWE, AI Engineer, or Data Scientist.

## Features
* **Intelligent Extraction:** Uses LLMs to convert raw HTML into structured JSON/CSV data based on natural language tags.
* **Modern UI:** Built with Flet (Flutter for Python) featuring a dark-mode dashboard, sidebar navigation, and responsive layout.
* **Data Visualization:** Instantly view scraped data in interactive Tables, JSON tree views, or Markdown.
* **Batch Processing:** Supports scraping single URLs or bulk lists of URLs.
* **Export Options:** Save results to local storage with timestamped filenames in CSV formats.

## Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** [Flet](https://flet.dev/)
* **Data Handling:** Pandas
* **AI Integration:** Crawl4AI

  ## 🖥️ Usage

1.  **Run the Application:**

2.  **Configure the Scrape:**
    * **Mode:** Select "Single URL" or "Multiple URLs".
    * **Target:** Paste the website link(s).
    * **Data to Extract:** Type the fields you want (e.g., `price, product_name, rating, email`).
    * **LLM MODEL:** There are different models you can use depending on the provider (e.g "openai/gpt-4o", "ollama/llama2.0", "aws/titan")
    * **API Key:** Enter your provider's API key in the settings panel.

3.  **View & Save:**
    * Click **Start Scrape**.
    * Toggle between **Markdown**, **JSON**, and **CSV** views to inspect the data.
    * Click **Save File** to export the data to the `output/` folder.
