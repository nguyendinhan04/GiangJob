FROM selenium/standalone-chrome:latest



COPY requirements.txt /opt/project/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /opt/project/requirements.txt