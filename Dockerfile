

EXPOSE 8000
ENTRYPOINT []
CMD [ "gunicorn", "-w", "3", "-b", ":8000", "wsgi" ]
