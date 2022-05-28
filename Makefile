test:
	python3 -m pytest

extract:
	python3 src/flatmates_scraper.py

load:
	python3 src/load_to_db.py
