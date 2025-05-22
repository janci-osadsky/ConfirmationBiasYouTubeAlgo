# Recommendation Algorithm Simulation - Information Bubble

This project simulates user behavior on the YouTube platform to analyze the formation of information bubbles and the impact of recommendation algorithms on content homogenization. It was developed as part of a bachelor's thesis focused on confirmation bias in online environments.

## Overview

The tool utilizes Selenium with `undetected-chromedriver` to control a Chrome browser, simulating user actions like searching, watching, scrolling, liking, and interacting with videos. Two distinct user behavior models are implemented:

* **Watcher**: Passively watches relevant videos.
* **Interacter**: Actively likes, scrolls, and skips irrelevant content.

## Features

* Heuristic simulation of two types of user behavior.
* Detection of recommended videos from the sidebar.
* Filtering of relevant videos using multiple techniques (weighted keywords, etc.).
* Scroll and mouse movement simulation to mimic human activity.
* Automatic login support with user profile persistence.

## Directory Structure

```
.
├── API_scratch.py              # Metadata extraction module
├── config.py                   # Configuration constants
├── filter_program.py          # Filtering logic
├── simulation.py              # Main simulation logic (this file)
├── links.txt                  # Temporary file storing recommended links
├── results.txt                # Log file of decisions and clicked links
```

## Requirements

* Python 3.11+
* Chrome browser
* Undetected Chromedriver
* Selenium 4.9.1
* Internet connection

## Setup

1. Install dependencies:

```bash
pip install selenium==4.9.1 undetected-chromedriver
```

2. Download ChromeDriver compatible with your browser version.
3. Create a Chrome profile in `C:/uc_logged_profile` and sign into YouTube if needed.
4. Configure `config.py` with your search queries, XPath selectors, and other settings.

## Running the Simulation

```bash
python simulation.py
```

The script runs simulations over several topics, alternating between watcher and interacter models. All interactions and results are logged in `results.txt`.

## Filtering Types

* **basic**: Keyword match
* **weighted**: Weighted keyword matching
* **old**: Deprecated logic for comparison

## Customization

You can adjust:

* Number of iterations
* Behavior probabilities
* Filters
* Duration of mouse movement and scrolls

## Known Limitations

* Occasional failures due to YouTube layout changes.
* Dynamic content may not always be captured in time.
* Accuracy of relevance depends on keyword configuration.

## Future Work

* JSON-based result logging.
* Integration of real-time sentiment analysis.
* Enhanced behavior models based on psychological literature.

---

For academic or research inquiries, contact: *Ján Osadský / FMFI UK*
