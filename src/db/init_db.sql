create table if not exists Projects (
    project_id  varchar(36) primary key,
    name        text unique not null,
    path        text not null
);
