warmup:
	( \
		virtualenv venv; \
		source venv/bin/activate; \
		pip install -r requirements.txt \
	)
run:
	( \
		source venv/bin/activate; \
		python cli.py \
	)
test:
	py.test tests
