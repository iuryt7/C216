CREATE TABLE IF NOT EXISTS alunos (
    id          VARCHAR PRIMARY KEY,
    nome        VARCHAR NOT NULL,
    email       VARCHAR NOT NULL,
    curso       VARCHAR NOT NULL,
    matricula   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS curso_counters (
    curso       VARCHAR PRIMARY KEY,
    contador    INTEGER NOT NULL DEFAULT 0
);
