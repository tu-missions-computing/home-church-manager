DROP TABLE IF EXISTS member_role;
DROP TABLE IF EXISTS homegroup_leader;
DROP TABLE IF EXISTS homegroup_member;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS marital_status;
DROP TABLE IF EXISTS how_did_you_find_out;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS homegroup;
DROP TABLE IF EXISTS meeting;

CREATE TABLE marital_status (
  id                  SERIAL PRIMARY KEY,
  marital_status_name TEXT
);

CREATE TABLE how_did_you_find_out (
  id                        SERIAL PRIMARY KEY,
  how_did_you_find_out_name TEXT
);

CREATE TABLE member (
  id                      SERIAL PRIMARY KEY,
  first_name              TEXT,
  last_name               TEXT,
  email                   TEXT UNIQUE,
  phone_number            TEXT,
  gender                  TEXT,
  birthday                TEXT,
  baptism_status          BOOLEAN,
  marital_status_id       INTEGER,
  how_did_you_find_out_id INTEGER,
  is_a_parent             BOOLEAN,
  join_date               TEXT,
  is_active               BOOLEAN,
  FOREIGN KEY (how_did_you_find_out_id) REFERENCES how_did_you_find_out (id),
  FOREIGN KEY (marital_status_id) REFERENCES marital_status (id)
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
  id            SERIAL PRIMARY KEY,
  name          TEXT,
  location      TEXT,
  description   TEXT,
  latitude      REAL,
  longitude     REAL,
  creation_date TEXT,
  is_active     BOOLEAN
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
  join_date    TEXT,
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


CREATE OR REPLACE FUNCTION add_user(user_email TEXT, role_name TEXT, first_name TEXT, last_name TEXT)
  RETURNS INTEGER AS $$
DECLARE
  find_out_id       INTEGER;
  marital_status_id INTEGER;
  role_id           INTEGER;
  new_member_id     INTEGER;
BEGIN
  -- Find the ID of how you found out "other".
  SELECT id
  INTO STRICT find_out_id
  FROM how_did_you_find_out
  WHERE how_did_you_find_out_name = 'Other';

  -- Find the ID of martial status "other".
  SELECT id
  INTO STRICT marital_status_id
  FROM marital_status
  WHERE marital_status_name = 'Other';

  -- Find the ID of the role passed in.
  SELECT id
  INTO STRICT role_id
  FROM role
  WHERE role = role_name;

  -- Create a dummy member with the email address passed in.
  INSERT INTO member (email, first_name, last_name, phone_number, gender,
                      birthday, baptism_status, marital_status_id,
                      how_did_you_find_out_id, is_a_parent, join_date, is_active)
  VALUES (user_email,
    first_name, last_name, '800/555-1212', 'M', '1980-12-25', FALSE,
    marital_status_id,
    find_out_id,
    FALSE, '2001-01-01', TRUE)
  RETURNING id
    INTO new_member_id;

  -- Make the dummy member an administrator with the password "password".
  INSERT INTO member_role (member_id, password, role_id, is_active)
  VALUES (new_member_id,
          '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG',
          role_id,
          TRUE);

  RETURN new_member_id;
END;
$$
LANGUAGE plpgsql;
