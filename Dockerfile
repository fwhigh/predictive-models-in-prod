FROM 015216235264.dkr.ecr.us-west-1.amazonaws.com/pmip:latest

EXPOSE 8000
ENTRYPOINT [ "bash" ]
CMD [ "-c", "gunicorn -w 3 -b :8000 wsgi" ]
