# Dockerfile with Name to Spectrum Generator
# author: Micha Birklbauer
# version: 1.0.0

FROM python:3.10.4

LABEL maintainer="micha.birklbauer@gmail.com"

RUN pip install matplotlib
RUN pip install ms2pip
RUN pip install streamlit

RUN mkdir app
COPY streamlit_app.py app
WORKDIR app
RUN mkdir img
COPY img/fhooe_logo.png img

CMD  ["streamlit", "run", "streamlit_app.py"]
