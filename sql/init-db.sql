-- This file contains data that must be inserted into
-- a new database for the application to run properly.

INSERT INTO marital_status (marital_status_name) values ('Single');
INSERT INTO marital_status (marital_status_name) values ('Married');
INSERT INTO marital_status (marital_status_name) values ('Divorced');
INSERT INTO marital_status (marital_status_name) values ('Widowed');
INSERT INTO marital_status (marital_status_name) values ('Other');


INSERT INTO how_did_you_find_out (how_did_you_find_out_name) values ('Friends or family');
INSERT INTO how_did_you_find_out (how_did_you_find_out_name) values ('Radio station');
INSERT INTO how_did_you_find_out (how_did_you_find_out_name) values ('Social media');
INSERT INTO how_did_you_find_out (how_did_you_find_out_name) values ('Special event');
INSERT INTO how_did_you_find_out (how_did_you_find_out_name) values ('Other');


INSERT INTO role (role) VALUES ('homegroup_leader');
INSERT INTO role (role) VALUES ('admin');


INSERT INTO member (email, first_name, last_name, phone_number, gender,
                    birthday, baptism_status, marital_status_id,
                    how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('admin@example.com',
  'Admin', 'User', '800 555 1212', 'M', '1980-12-25', FALSE,
  (SELECT id
   FROM marital_status
   WHERE marital_status_name = 'Single'),
  (SELECT id
   FROM how_did_you_find_out
   WHERE how_did_you_find_out_name = 'Other'),
  FALSE, '2001-01-01', TRUE);


INSERT INTO member_role (member_id, password, role_id, is_active)
VALUES ((SELECT id
         FROM member
         WHERE email = 'admin@example.com'),
        '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG',
        (SELECT id
         FROM role
         WHERE role = 'admin'),
        TRUE);

CREATE FUNCTION add_admin(email TEXT)
  RETURNS INTEGER AS $$
DECLARE
  find_out_id       integer;
  marital_status_id integer;
BEGIN
  SELECT id
  INTO STRICT find_out_id
  FROM how_did_you_find_out
  WHERE how_did_you_find_out_name = 'Other';

  SELECT id
  INTO STRICT marital_status_id
  FROM marital_status
  WHERE marital_status_name = 'Other';

  INSERT INTO member (email, first_name, last_name, phone_number, gender,
                      birthday, baptism_status, marital_status_id,
                      how_did_you_find_out_id, is_a_parent, join_date, is_active)
  VALUES (email,
    'Admin', 'User', '800/555-1212', 'M', '1980-12-25', FALSE,
    marital_status_id,
    find_out_id,
    FALSE, '2001-01-01', TRUE);

  RETURN 0;
END;
$$
LANGUAGE plpgsql;

SELECT add_admin('foo@example.com');