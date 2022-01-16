-- Creation of medicos table
create table if not exists medicos
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
    data_nascimento timestamp,
    datecreate timestamp,
    datemodify timestamp
    );

-- Creation of utentes table
create table if not exists utentes
(
    id              serial
        constraint utentes_pk
            primary key,
    nome            varchar(255),
    morada          varchar(255),
    data_nascimento timestamp,
    telemovel       varchar(20),
    email           varchar(255),
    nif             varchar(10),
    codpost         varchar(10),
    nmr_utente      varchar(20),
    datecreate      timestamp,
    datemodify      timestamp
);


-- Creation of consultas table
create table if not exists consultas
(
    id         serial
        constraint consultas_pk
            primary key,
    descricao  varchar(255) not null,
    datecreate timestamp,
    datemodify timestamp,
    data       timestamp,
    id_medico  integer
        constraint medicos_fk
            references medicos,
    id_utente  integer
        constraint utentes_fk
            references utentes
);
