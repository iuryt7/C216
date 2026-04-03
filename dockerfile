FROM python:3.10-slim

COPY sistema_faculdade.py .

CMD [ "python", "sistema_faculdade.py" ]