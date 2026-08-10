CREATE Table cities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    UNIQUE (name, state)
);

CREATE Table sources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL
);

CREATE Table metric_types (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT NOT NULL,
    higher_is_better BOOLEAN NOT NULL
);

CREATE Table city_metrics (
    city_id INTEGER NOT NULL,
    metric_type_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    raw_value REAL NOT NULL,
    normalized_value REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id, metric_type_id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (metric_type_id) REFERENCES metric_types(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

CREATE Table city_scores (
    city_id INTEGER NOT NULL,
    total_score REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE Table city_metric_scores (
    city_id INTEGER NOT NULL,
    metric_type_id INTEGER NOT NULL,
    score REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id, metric_type_id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (metric_type_id) REFERENCES metric_types(id)
);