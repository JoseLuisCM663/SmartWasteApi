smartwaste_api/
│
├── app/                       # Código principal de la aplicación
│   ├── main.py                # Punto de entrada de la aplicación FastAPI
│   ├── config.py              # Configuración (env, settings, DB config)
│   ├── database/              # Conexión y modelo de base de datos
│   │   ├── connection.py
│   │   └── models.py
│   ├── api/                   # Rutas organizadas por módulo
│   │   ├── sensores.py        # ms-sensores
│   │   ├── rutas.py           # ms-rutas
│   │   ├── usuarios.py        # ms-usuarios
│   │   ├── alertas.py         # ms-alertas
│   │   └── analitica.py       # ms-analitica
│   ├── schemas/               # Pydantic models (validación de datos)
│   │   ├── sensores.py
│   │   ├── rutas.py
│   │   ├── usuarios.py
│   │   ├── alertas.py
│   │   └── analitica.py
│   ├── services/              # Lógica de negocio por módulo
│   │   ├── sensores_service.py
│   │   └── ...
│   ├── utils/                 # Funciones utilitarias comunes
│   │   └── auth.py
│   └── events/                # Configuraciones como startup/shutdown
│       └── handlers.py
│
├── .env                       # Variables de entorno
├── requirements.txt           # Lista de dependencias
├── Dockerfile                 # Para contenedor Docker
├── README.md
└── alembic/                   # (Opcional) Migraciones si usas SQLAlchemy