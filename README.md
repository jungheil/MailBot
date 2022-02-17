## MailBot

邮件发送机器人

### Deploy

e.g.

```bash
docker run -d --restart=always -p 80:7070 \
-e SMTP_HOST="smtp.xxx.com" \
-e SMTP_PORT=25 \
-e SMTP_USER="xxx@xxx.com" \
-e SMTP_PASS="xxxxxxxx" \
--name="mailbot" \
jungheil/mailbot
```

### Request

e.g.

```http
http://xxx.com/send?dst=xxx@xxx.com&subj=xxx&type=md&body=xxxxxx
```

