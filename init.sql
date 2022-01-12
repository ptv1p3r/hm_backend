-- Creation of consultas table
CREATE TABLE IF NOT EXISTS consultas
(
    id
    serial
    constraint
    consultas_pk
    primary
    key
    constraint
    medicos___fk
    references
    medicos,
    descricao
    varchar
(
    255
) not null,
    date_create timestamp,
    date_modify timestamp
    );

-- Creation of medicos table
CREATE TABLE IF NOT EXISTS medicos
(
    id
    serial
    constraint
    medicos_pk
    primary
    key,
    morada
    varchar
(
    255
),
    email varchar
(
    255
),
    codpost varchar
(
    8
),
    nome varchar
(
    255
) not null,
    nif varchar
(
    10
),
    ced_profissional varchar
(
    50
) not null,
    telemovel varchar
(
    20
),
    data_nascimento timestamp
    );

-- Creation of utentes table
CREATE TABLE IF NOT EXISTS utentes
(
    id
    serial
    constraint
    utentes_pk
    primary
    key,
    nome
    varchar
(
    255
),
    morada varchar
(
    255
),
    data_nascimento timestamp,
    telemovel varchar
(
    20
),
    email varchar
(
    255
),
    nif varchar
(
    10
),
    codpost varchar
(
    10
),
    nmr_utente varchar
(
    20
)
    );
