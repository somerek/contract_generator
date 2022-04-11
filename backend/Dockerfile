FROM python:3.10-slim as py-image
FROM py-image as builder
WORKDIR /opt/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM py-image
RUN apt update && apt install -y curl wkhtmltopdf
ENV dir=/usr/local/bin
COPY --from=builder ${dir} ${dir}
ENV dir=/usr/local/lib/python3.10/site-packages
COPY --from=builder ${dir} ${dir}
COPY app.py .
COPY pdf_interest_report.html .

ARG POSTGRES_USER
RUN echo $POSTGRES_USER
RUN sed -i "s/POSTGRES_USER/$POSTGRES_USER/g" app.py
ARG POSTGRES_PASSWORD
RUN sed -i "s/POSTGRES_PASSWORD/$POSTGRES_PASSWORD/g" app.py
ARG POSTGRES_DB
RUN sed -i "s/POSTGRES_DB/$POSTGRES_DB/g" app.py

EXPOSE 5000
COPY entrypoint.sh .
CMD [ "sh", "-c", "/entrypoint.sh"]

#HEALTHCHECK --interval=5s --timeout=5s --retries=5 CMD curl --fail http://localhost:5000/contract/api/v1.0/contract-download/7 || exit 1
