# Makefile 내용
up:
	docker build -t my-app .
	docker run -p 5001:5000 my-app