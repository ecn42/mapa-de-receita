FROM python:3.11

#coment
WORKDIR /app
COPY . ./

VOLUME ["/app/dir", "/app/dirhist"]

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 Dash_Ceres_Capital.py