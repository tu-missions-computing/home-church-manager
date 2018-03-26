DROP TABLE IF EXISTS member_role;
DROP TABLE IF EXISTS homegroup_leader;
DROP TABLE IF EXISTS homegroup_member;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS homegroup;
DROP TABLE IF EXISTS meeting;

CREATE TABLE member (
  id             SERIAL PRIMARY KEY,
  first_name     TEXT,
  last_name      TEXT,
  email          TEXT UNIQUE,
  phone_number   TEXT,
  gender         TEXT,
  birthday       TEXT,
  baptism_status BOOLEAN,
  marital_status BOOLEAN,
  join_date      TEXT,
  is_active      BOOLEAN
);

CREATE TABLE role (
  id   SERIAL PRIMARY KEY,
  role TEXT
);

CREATE TABLE member_role (
  member_id INTEGER,
  password  TEXT,
  role_id   INTEGER,
  is_active BOOLEAN,
  FOREIGN KEY (member_id) REFERENCES member (id),
  FOREIGN KEY (role_id) REFERENCES role (id),
  PRIMARY KEY (member_id, role_id)
);

CREATE TABLE homegroup (
  id          SERIAL PRIMARY KEY,
  name        TEXT,
  location    TEXT,
  description TEXT,
  latitude    REAL,
  longitude   REAL,
  is_active   BOOLEAN
);

CREATE TABLE homegroup_leader (
  member_id    INTEGER,
  homegroup_id INTEGER,
  is_active    BOOLEAN,
  FOREIGN KEY (member_id) REFERENCES member (id),
  FOREIGN KEY (homegroup_id) REFERENCES homegroup (id),
  PRIMARY KEY (member_id, homegroup_id)
);

CREATE TABLE homegroup_member (
  homegroup_id INTEGER,
  member_id    INTEGER,
  is_active    BOOLEAN,
  FOREIGN KEY (member_id) REFERENCES member (id),
  FOREIGN KEY (homegroup_id) REFERENCES homegroup (id),
  PRIMARY KEY (homegroup_id, member_id)
);

CREATE TABLE meeting (
  id   SERIAL PRIMARY KEY,
  date TEXT,
  time TEXT

);

CREATE TABLE attendance (
  homegroup_id INTEGER,
  member_id    INTEGER,
  meeting_id   INTEGER,
  attendance   BOOLEAN,
  FOREIGN KEY (member_id) REFERENCES member (id),
  FOREIGN KEY (meeting_id) REFERENCES meeting (id),
  PRIMARY KEY (homegroup_id, member_id, meeting_id)
);

ALTER SEQUENCE member_id_seq RESTART WITH 101;
ALTER SEQUENCE homegroup_id_seq RESTART WITH 101;
ALTER SEQUENCE role_id_seq RESTART WITH 101;
