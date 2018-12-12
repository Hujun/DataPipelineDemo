# DataPipelineDemo
Simple data pipeline demo based on redis as (task) queue and web UI using websocket

## Prerequistes

- [docker engine](https://www.docker.com/)
- [docker compose](https://docs.docker.com/compose/overview/)

## How to run

1. Clone this repo on your localhost
```shell
git clone https://github.com/Hujun/DataPipelineDemo && cd DataPipelineDemo
```
2. Run prepared compose file. The images will be automatically built
```shell
docker-compose up
```
3. Use your browser to visit `localhost:8687`. __Attention__ that the page use directly `WebSocket API`. If it occurs some error, please update your browser to the latest version.
