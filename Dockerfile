FROM python:3.12.4-alpine
LABEL Maintainer="LRVT"

COPY requirements.txt breach_data.py dehasheddumper.py /app/.
RUN pip3 install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT [ "python", "dehasheddumper.py"]

CMD [ "python", "dehasheddumper.py", "--help"]
