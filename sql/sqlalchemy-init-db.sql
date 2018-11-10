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
INSERT INTO role (role) VALUES ('homegroup_member');
INSERT INTO role (role) VALUES ('homegroup_supervisor');

CREATE OR REPLACE FUNCTION add_user(user_email TEXT, role_name TEXT, first_name TEXT, last_name TEXT)
  RETURNS INTEGER AS $$
DECLARE
  find_out_id       INTEGER;
  marital_status_id INTEGER;
  role_id           INTEGER;
  new_person_id     INTEGER;
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

  -- Create a dummy person with the email address passed in.
  INSERT INTO person (email, first_name, last_name, phone_number, gender,
                      birthday, baptism_status, marital_status_id,
                      how_did_you_find_out_id, is_a_parent, join_date, password)
  VALUES (user_email,
    first_name, last_name, '800/555-1212', 'M', '1980-12-25', FALSE,
    marital_status_id,
    find_out_id,
    FALSE, current_date,
    '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG')
  RETURNING id
    INTO new_person_id;

  -- Make the dummy person an administrator with the password "password".
  INSERT INTO homegroup_person_role (person_id, role_id, creation_date)
  VALUES (new_person_id,
          role_id,
          current_date);

  RETURN new_person_id;
END;
$$
LANGUAGE plpgsql;

SELECT add_user('admin@example.com', 'admin', 'Admin', 'User');
