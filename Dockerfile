FROM python:3.11

#coment
WORKDIR /app
COPY . ./

VOLUME dir-volume /app/dir
VOLUME dirhist-volume /app/dirhist
VOLUME assetallocation app/assetallocation
VOLUME historicocomissoes app/historicocomissoes

RUN pip install -r requirements.txt

EXPOSE 8080

CMD streamlit run --client.showSidebarNavigation=False --server.port 8080 Dash_Ceres_Capital.py