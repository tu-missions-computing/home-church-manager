## Utility makefile
.PHONY: extract init compile update

extract:
	pybabel extract -F babel.cfg -o messages.pot .

init:
	pybabel init -i messages.pot -d translations -l es

compile:
	pybabel compile -d translations

update:
	pybabel update -i messages.pot -d translations
