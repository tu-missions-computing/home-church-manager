INSERT INTO member (email, first_name, last_name, phone_number, gender, birthday,
                    baptism_status, marital_status, join_date, is_active)
VALUES ('john@example.com', 'John', 'Smith', '5555555555', 'M', '1980-03-12', '1', '1', '2016-08-01', '1');
INSERT INTO member (email, first_name, last_name, phone_number, gender, birthday,
                    baptism_status, marital_status, join_date, is_active)
VALUES ('admin@example.com', 'Joel', 'Guido', '02-398423', 'M', '1980-05-02', '1', '1', '2016-08-01', '1');


INSERT INTO homegroup (name, location, description, latitude, longitude, is_active) VALUES
  ('Singles Group', 'Avenida Loja, Cuenca, Ecuador',
   'Growing together and discovering our purpose as single individuals.', -2.9055067, -79.0273297, '1');

INSERT INTO role (role) VALUES ('homegroup_leader');
INSERT INTO role (role) VALUES ('admin');

INSERT INTO homegroup_leader (member_id, homegroup_id, is_active) VALUES (1, 1, '1');
