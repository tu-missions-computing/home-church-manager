## Utility makefile
.PHONY: extract init compile update

extract:
	pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .


compile:
	pybabel compile -d translations

update:
	pybabel update -i messages.pot -d translations
