FROM python:3.11


WORKDIR /app
COPY . ./

RUN mkdir -p /app/data/dir /app/data/dirhist
VOLUME /app/data 
RUN ln -s /app/data/dir /app/dir
RUN ln -s /app/data/dirhist /app/dirhist 

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 Dash_Ceres_Capital.py