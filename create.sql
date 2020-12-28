create table if not exists people(
id integer,
name text not null,
primary key(id)
);

create table if not exists times(
id integer,
id_person integer,
day integer check (day between 0 and 6),
start text,
end text,
primary key(id),
foreign key(id_person) references people(id)
);

create table if not exists parties(
id integer,
day integer check (day between 0 and 6),
start text,
end text,
primary key(id)
);

create table if not exists attendance(
id integer,
id_party integer,
id_person integer,
primary key(id),
foreign key(id_party) references parties(id),
foreign key(id_person) references people(id)
);
