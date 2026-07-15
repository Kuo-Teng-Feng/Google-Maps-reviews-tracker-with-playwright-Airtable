# Google Maps Review Monitor

A lightweight Python automation tool built with **Playwright** to monitor recent **Google Maps** reviews for multiple restaurants.

The script searches each restaurant, sorts reviews by **Newest**, extracts reviews posted **today**, parses useful information, and uploads the results to **Airtable** for further analysis.

---

## Features

* Search multiple restaurants on Google Maps
* Sort reviews by **Newest**
* Extract only reviews posted **today**
* Parse:

  * Reviewer
  * Rating
  * Review text
  * Review language
  * Review time
  * Restaurant name
* Export structured data to Airtable
* Designed for scheduled daily execution

---

## Technologies

* Python 3
* Playwright
* pyairtable
* Regular Expressions (Regex)

---

## Installation

Install the required packages:

```bash
pip install playwright pyairtable
playwright install chromium
```

---

## Configuration

Before running the script, replace the following placeholders with your own values.

```python
keywords = [
    "Your Restaurant 1",
    "Your Restaurant 2",
    "Your Restaurant 3"
]

AIRTABLE_TOKEN = "Your Airtable token"
BASE_ID = "Your Base ID"
TABLE_NAME = "Your Table Name"
```

> **Important**
>
> Never upload real API tokens or personal credentials to a public repository.

---

## Run

```bash
python google_maps_review_monitor.py
```

---

## Workflow

```
Google Maps
      │
      ▼
Search Restaurant
      │
      ▼
Sort Reviews (Newest)
      │
      ▼
Extract Today's Reviews
      │
      ▼
Parse Review Information
      │
      ▼
Upload to Airtable
```

---

## Example Output

```
Restaurant : Example Restaurant
Time       : 2 hours ago
Reviewer   : John
Rating     : 5
Language   : Chinese (Traditional)
Review     : Excellent food and friendly service.
```

---

## Notes

* Google Maps updates its HTML structure periodically. Some Playwright selectors may require adjustment in the future.
* This project is intended for educational and personal automation purposes.
* The repository contains placeholder configuration only. Users must provide their own Airtable credentials and restaurant list before running the script.

---

## Author

Created by **Teng-Feng Kuo**

Feel free to fork this project or adapt it for your own review-monitoring workflow.
