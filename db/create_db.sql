drop table if exists user;
create table user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  phone_number TEXT,
  gender TEXT,
  birthday TEXT,
  baptism_status BOOLEAN,
  join_date TEXT,
  foreign key (id) REFERENCES attendance (user_id),
  foreign key (id) REFERENCES homegroup_user (user_id)
);


drop table if exists homegroup;
create table homegroup (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  location TEXT,
  description TEXT,
  foreign key (id) REFERENCES homegroup_user (homegroup_id)
);

drop table if exists homegroup_user;
create table homegroup_user (
  homegroup_id,
  user_id,
  PRIMARY KEY (homegroup_id, user_id)
);



drop table if exists meeting;
create table meeting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  foreign key (id) REFERENCES attendance (date_id)

);
drop table if exists attendance;
CREATE TABLE attendance (
  user_id INTEGER,
  meeting_id INTEGER,
  attendance BOOLEAN,
  PRIMARY KEY(user_id, meeting_id)
);
