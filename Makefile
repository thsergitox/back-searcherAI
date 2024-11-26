run:
	docker build -t backsearch . && docker run -p 8000:8000 backsearch