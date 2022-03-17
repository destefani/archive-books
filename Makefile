build:
	docker build -t destefanim/archive-books .
run:
	docker run -it -v "$(pwd)":/workspace destefanim/archive-books make test/bin/bash	
test:
	python -m pytest test_bibliothek.py