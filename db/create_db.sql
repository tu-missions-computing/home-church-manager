drop table if exists user;
create table user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  foreign key (id) REFERENCES attendance (user_id)
);

drop table if exists meetings;
create table meetings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  foreign key (id) REFERENCES attendance (date_id)

);
drop table if exists attendance;
CREATE TABLE attendance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  meeting_id INTEGER,
  attendance BOOLEAN

);
