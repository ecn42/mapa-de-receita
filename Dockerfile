FROM python:3.11


WORKDIR /app
COPY . ./

VOLUME /data

# Create a volume for data persistence
VOLUME /app/data

# Mount the directories to the volume
RUN mkdir -p /app/data/dir /app/data/dirhist
RUN ln -s /app/data/dir /app/dir
RUN ln -s /app/data/dirhist /app/dirhist

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 Dash_Ceres_Capital.py