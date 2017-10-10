from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib


GMAP_TEMPLATE = 'google.com/maps/?q={lat:f},{lng:f}'


def send_apt(apt, *, fromaddr, passwd, toaddr, dry=False):
    logger = logging.getLogger()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    user = fromaddr.split('@')[0]
    server.login(user, passwd)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    subject = '%.0f $' % apt['price']
    if apt['dims']:
        subject += ' -- ' + apt['dims']
    subject += ' -- ' + apt['title']
    msg['Subject'] = subject

    parts = []
    parts.append(apt['url'])
    hood = 'Hood: '
    if apt['hood']:
        lat, lng = apt['geo']
        map_url = GMAP_TEMPLATE.format(lat=lat, lng=lng)
        hood += '<a href="%s">%s</a>' % (map_url, apt['hood'])
    else:
        hood += 'Undefined'
    parts.append(hood)

    for i, link in enumerate(apt['images']):
        img = '<img src="%s" alt="%d">' % (link, i)
        parts.append(img)

    body = apt['body']
    body = body.replace('\n', '<br>')
    parts.append(body)

    text = '<br>'.join(parts)
    msgText = MIMEText(text, 'html')
    msg.attach(msgText)

    try:
        if not dry:
            server.sendmail(fromaddr, toaddr, msg.as_string())
    except smtplib.SMTPDataError as e:
        logger.error('ERROR: COULD NOT SEND E-MAIL\n' + str(e))
    server.quit()
