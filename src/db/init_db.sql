create table if not exists Projects (
    project_id      varchar(36) primary key,
    name            text unique not null,
    path            text        not null,
    last_modified   timestamp   not null
);

create table if not exists Templates (
    template_id     varchar(36) primary key,
    name            text unique not null,
    filename        text unique not null,
    path            text        not null
);
