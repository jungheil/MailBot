FROM python:3.8-alpine

ENV SMTP_HOST smtp.xxx.com
ENV SMTP_PORT 25
ENV SMTP_USER user
ENV SMTP_PASS pass

ENV ACCESS_PATH /send
ENV SERVER_HOST 0.0.0.0

RUN pip install flask markdown

COPY MailBot.py main.py ./

EXPOSE 7070

CMD ["python", "./main.py"]