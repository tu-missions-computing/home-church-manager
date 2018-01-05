
drop  table if exists member CASCADE;
create table member (
  id SERIAL PRIMARY KEY ,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE,
  phone_number TEXT,
  gender TEXT,
  birthday TEXT,
  baptism_status BOOLEAN,
  marital_status BOOLEAN,
  join_date TEXT,
  is_active BOOLEAN

);

drop table if exists member_role  CASCADE;
create table member_role(
  member_id INTEGER,
  password TEXT,
  role_id INTEGER,
  foreign key (member_id) REFERENCES member(id),
  foreign key (role_id) references role(id)
);
drop table if exists role CASCADE;
create table role (
  id SERIAL PRIMARY KEY ,
  role TEXT
);




drop table if exists homegroup CASCADE;
create table homegroup (
  id SERIAL PRIMARY KEY ,
  name TEXT,
  location TEXT,
  description TEXT,
  latitude REAL,
  longitude REAL,
  is_active BOOLEAN

);

drop table if exists homegroup_leader CASCADE;
create table homegroup_leader (
  member_id INTEGER,
  homegroup_id INTEGER,
  is_active boolean,
  foreign key (member_id) REFERENCES member(id),
  foreign key (homegroup_id) references homegroup(id),
  PRIMARY KEY (member_id, homegroup_id)
);


drop table if exists homegroup_member CASCADE;
create table homegroup_member (
  homegroup_id INTEGER,
  member_id INTEGER,
  is_active BOOLEAN,
  foreign key (member_id) REFERENCES member (id),
  foreign key (homegroup_id) REFERENCES homegroup(id),
  PRIMARY KEY (homegroup_id, member_id)
);



drop table if exists meeting CASCADE;
create table meeting (
  id SERIAL PRIMARY KEY ,
  date TEXT,
  time TEXT

);
drop table if exists attendance CASCADE;
CREATE TABLE attendance (
  homegroup_id INTEGER,
  member_id INTEGER,
  meeting_id INTEGER,
  attendance BOOLEAN,
  foreign key (member_id) REFERENCES member (id),
  foreign key (meeting_id) REFERENCES meeting (id),
  PRIMARY KEY(homegroup_id, member_id, meeting_id)
);
