## Estruturas de pasta

yt-playlist-downloader/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── routes_playlist.py
│   │       └── routes_tasks.py
│   ├── schemas/
│   │   ├── playlist.py
│   │   └── task.py
│   ├── services/
│   │   └── playlist_analyzer.py
│   ├── workers/
│   │   └── downloader.py
│   ├── core/
│   │   ├── config.py
│   │   └── celery_app.py
│   └── utils/
│       └── filesystem.py
│
├── downloads/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## Omar Rodrigues -> Core + Engine

### Responsável por:

    - Integração com yt-dlp

    - Análise da playlist

    - Engine de download

    - Gestão de ficheiros

    - Background tasks (Celery/RQ)

### Pastas-alvo

    - app/services/
    - app/workers/
    - app/utils/

## Ricardo Luwawa -> API + Infra

### Responsável por:

    - FastAPI

    - Endpoints

    - Schemas (Pydantic)

    - Task status

