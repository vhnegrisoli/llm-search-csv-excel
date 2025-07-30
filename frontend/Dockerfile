FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
EXPOSE 8501
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
CMD ["streamlit", "run", "/app/streamlit_app.py", "--server.address=0.0.0.0"]