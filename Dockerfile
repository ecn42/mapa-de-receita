FROM python:3.11


WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 Dash_Ceres_Capital.py