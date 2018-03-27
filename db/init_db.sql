
INSERT INTO marital_status(marital_status_name) values ('Soltero');
INSERT INTO marital_status(marital_status_name) values ('Casado');
INSERT INTO marital_status(marital_status_name) values ('Divorciado');
INSERT INTO marital_status(marital_status_name) values ('Viudo');
INSERT INTO marital_status(marital_status_name) values ('Otro');


INSERT INTO how_did_you_find_out(how_did_you_find_out_name) values ('Amigos o familia');
INSERT INTO how_did_you_find_out(how_did_you_find_out_name) values ('Estación de radio');
INSERT INTO how_did_you_find_out(how_did_you_find_out_name) values ('Medios de comunicación social');
INSERT INTO how_did_you_find_out(how_did_you_find_out_name) values ('Evento especial');
INSERT INTO how_did_you_find_out(how_did_you_find_out_name) values ('Otro');



INSERT INTO member(email, first_name, last_name,  phone_number, gender, birthday, baptism_status, martial_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) values ('admin@example.com', 'Jonathan', 'Guido', '02-0398423',
'M', '1980-03-12', '1', 1, 1, '1', '03-27-2018', '1');


INSERT INTO member( email, first_name, last_name, phone_number, gender, birthday, baptism_status, martial_status_id,
 how_did_you_find_out_id,  is_a_parent, join_date, is_active)
VALUES ('john@example.com', 'John', 'Smith', '5555555555', 'M', '1980-03-12', '1', 2, 2, '1', '2016-08-01', '1');



INSERT INTO homegroup (name, location, description, latitude, longitude, is_active) VALUES
  ('Singles Group', 'Avenida Loja, Cuenca, Ecuador',
   'Growing together and discovering our purpose as single individuals.', -2.9055067, -79.0273297, '1');

INSERT INTO role (role) VALUES ('homegroup_leader');
INSERT INTO role (role) VALUES ('admin');

INSERT INTO member_role(1, '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG', 2, '1')
INSERT INTO member_role(2, '$2b$12$fFU3LXEp5t5yfggXUzZaIu/RdrQrr4NLC7pH4cTedNL4stXeq3d9q', 1, '1')

INSERT INTO homegroup_leader (member_id, homegroup_id, is_active) VALUES (1, 1, '1');
