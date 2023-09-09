test:
	python3 -m pytest

extract:
	python3 src/flatmates_scraper.py

load:
	python3 src/load_to_db.py

model:
	python3 src/model.py

model-serve:
	python3 src/app.py
