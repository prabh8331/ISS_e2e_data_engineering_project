

### Add mail and password to envronment variable in airflow webserver and scheduler

<!-- this was a temprory solution, so added diretly to docker-compose file of airflow scheduler and webserver-->
<!-- docker exec -it airflow-scheduler-1 bash
docker exec -it airflow-webserver-1 bash
```bash

export GMAIL_EMAIL=your_email@gmail.com
export GMAIL_PASSWORD=your_password

env
```
 -->

add following in airflow webserve and scheduler docker-compose.yml file - 
```yml
services:
  webserver:
    environment:
      - GMAIL_EMAIL=your_email@gmail.com
      - GMAIL_PASSWORD=your_password
```

