drop table if exists member;
create table member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  phone_number TEXT,
  gender TEXT,
  birthday TEXT,
  baptism_status BOOLEAN,
  join_date TEXT,
  foreign key (id) REFERENCES attendance (member_id),
  foreign key (id) REFERENCES homegroup_member (member_id)
);


drop table if exists homegroup;
create table homegroup (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  location TEXT,
  description TEXT,
  foreign key (id) REFERENCES homegroup_member (homegroup_id)
);

drop table if exists homegroup_member;
create table homegroup_member (
  homegroup_id,
  member_id,
  is_active BOOLEAN,
  PRIMARY KEY (homegroup_id, member_id)
);



drop table if exists meeting;
create table meeting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  time TEXT,
  foreign key (id) REFERENCES attendance (meeting_id)

);
drop table if exists attendance;
CREATE TABLE attendance (
  homegroup_id INTEGER,
  member_id INTEGER,
  meeting_id INTEGER,
  attendance BOOLEAN,
  PRIMARY KEY(homegroup_id, member_id, meeting_id)
);

