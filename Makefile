build:
	docker build -t destefanim/archive-books .
push:
	docker push destefanim/archive-books
run:
	docker run -it -v "$(pwd)":/workspace destefanim/archive-books /bin/bash	
test:
	python -m pytest test_bibliothek.py