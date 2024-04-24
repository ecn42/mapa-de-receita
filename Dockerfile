FROM python:3.11


WORKDIR /app
COPY . ./

RUN mkdir -p /app/data/dir /app/data/dirhist
VOLUME ["/app/dir", "/app/dirhist"]

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --server.port 8080 --showSidebarNavigation = false Dash_Ceres_Capital.py