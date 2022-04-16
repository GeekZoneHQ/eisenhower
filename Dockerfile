FROM python:latest

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
COPY main.py ./$PATH
RUN pip install -r requirements.txt
CMD ["/opt/venv/bin/python3", "main.py"]
