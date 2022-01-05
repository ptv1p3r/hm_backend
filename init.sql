create table public.cidades
(
    id serial
        constraint cidades_pk
            primary key
);

alter table public.cidades
    owner to postgres;