FROM python:latest

RUN mkdir "/opt/venv"
RUN mkdir "/opt/venv/bin"
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
COPY main.py ./opt/venv/bin/
RUN pip install -r requirements.txt
CMD ["/opt/venv/bin/python3", "/opt/venv/bin/main.py"]
