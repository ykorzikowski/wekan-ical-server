Simple HTTP server returning calendar entries for all [Wekan](https://github.com/wekan/wekan) cards with set due date. To be used with Lightning or similar calendar app (read-only).
Yes, it's not the best solution, but it does the job (at least for me).
Depends on: https://github.com/wekan/wekan-python-api-client

# Docker
```yaml
---
version: '3'

services:
  wekan_calendar_sync:
    container_name: service_wekan_calendar_sync
    image: ykorzikowski/wekan-ical-server:latest
    restart: always
    environment:
      TZ=Europe/Amsterdam
      WEKAN_HOST=http://127.0.0.1:8090
      WEKAN_USER=admin
      WEKAN_PW=admin
```

# Running manually
`python wekan_ical_server.py`
(don't forget to set your Wekan url and login/passwd)
then add new network calendar in your app with url: `http://LISTEN_HOST:LISTEN_PORT`
Done.
