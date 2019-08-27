# metadata-parser

A quick-and-dirty API to fetch metadata from a web page.

## Run locally

```shell
pip install -r requirements.txt
python debugserver.py
curl http://localhost:8888/?url=https://www.lemonde.fr/international/article/2019/08/26/les-embarrassantes-demandes-de-la-famille-hohenzollern_5502825_3210.html
{"title": "Les embarrassantes demandes de la famille Hohenzollern", "description": "La gauche allemande s\u2019indigne des n\u00e9gociations engag\u00e9es entre le gouvernement et les Hohenzollern, dont le soutien \u00e0 Hitler est \u00e9tabli. La famille r\u00e9clame aujourd\u2019hui la restitution de biens confisqu\u00e9s en\u00a01918.", "image": "https://img.lemde.fr/2019/08/26/324/0/3888/1944/1440/720/60/0/6354c60_Sg6caw39crxK53xmPfDR7Rmp.jpg"}
```

## Deploy

This is designed to be deployed on [now.sh](https://zeit.co/now). The endpoint is `/api/parse?url=xxx`.
