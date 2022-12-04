FROM python:3.10

WORKDIR /usr/src/app

COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .
RUN make data
RUN make database
CMD ["streamlit", "run", "src/streamlit_app.py"]