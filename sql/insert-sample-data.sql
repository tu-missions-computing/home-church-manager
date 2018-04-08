-- This file contains sample data used for testing and training.
-- It is not for use when initializing a production database.

INSERT INTO member (email, first_name, last_name, phone_number, gender, birthday, baptism_status, marital_status_id,
                    how_did_you_find_out_id, is_a_parent, join_date, is_active)
values ('admin@example.com', 'Jonathan', 'Guido', '02-0398423',
                             'M', '1980-03-12', '1', 1, 1, '1', '03-27-2018', '1');
INSERT INTO member (email, first_name, last_name, phone_number, gender, birthday, baptism_status, marital_status_id,
                    how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('john@example.com', 'John', 'Smith', '5555555555', 'M', '1980-03-12', '1', 2, 2, '1', '2016-08-01', '1');



INSERT INTO public.meeting (date, time) VALUES ('2018-03-25', '23:26');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-25', '23:26');
INSERT INTO public.meeting (date, time) VALUES ('2018-02-25', '23:27');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-01', '23:30');
INSERT INTO public.meeting (date, time) VALUES ('2018-01-25', '23:31');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-19', '22:45');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-20', '20:46');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-21', '19:47');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-22', '17:48');
INSERT INTO public.meeting (date, time) VALUES ('2018-02-14', '23:55');
INSERT INTO public.meeting (date, time) VALUES ('2018-02-15', '23:56');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-26', '09:18');
INSERT INTO public.meeting (date, time) VALUES ('2018-01-26', '09:19');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-07', '00:29');
INSERT INTO public.meeting (date, time) VALUES ('2018-03-26', '10:30');


INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('Gustavo', 'A', 'example1@example.com', '555555555', 'M', '2003-03-21', true, 1, 3, false, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Alejandra', 'Zambrano', 'Alejandra@gmail.com', '3323049293', 'F', '1995-02-08', true, 2, 3, false, '2018-03-25',
   true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Mendoza', 'Alfredo', 'mendoza@example.com', '5555555555', 'M', '1981-03-15', false, 1, 1, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Garcia', 'Princeton', 'garcia@example.com', '7779998888', 'F', '1982-03-02', true, 2, 2, false, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Pilar', 'Roberto', 'pilar@example.com', '8192929300', 'F', '1983-03-22', false, 4, 1, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Xavier', 'Guillermo', 'xavier@example.com', '9102990999', 'M', '2000-03-21', true, 5, 1, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Diego', 'Estaban', 'diego@example.com', '7478182999', 'M', '1993-03-06', false, 1, 2, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES
  ('Elena', 'Danilo', 'elena@example.com', '81992039929', 'F', '2005-03-13', true, 1, 3, false, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('Pepe', 'A', 'example2@example.com', '7182990000', 'M', '1995-03-16', true, 4, 3, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('Fernando', 'A', 'example3@example.com', '8829882000', 'M', '1996-03-11', true, 1, 2, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('Ishmael', 'A', 'example4@example.com', '82900039439', 'M', '1997-03-15', true, 4, 1, true, '2018-03-25', true);
INSERT INTO public.member (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
                           how_did_you_find_out_id, is_a_parent, join_date, is_active)
VALUES ('Ivanova', 'A', 'example5@example.com', '8289993000', 'M', '1998-03-14', true, 1, 3, false, '2018-03-25', true);


INSERT INTO public.homegroup (name, location, description, latitude, longitude, creation_date, is_active) VALUES
  ('Grupo Parejas', 'Cuenca, Ecuador', 'Un grupo para que las parejas crezcan en su relación con Dios', -2.9001286,
   -79.0059, '03-24-2018', true);
INSERT INTO public.homegroup (name, location, description, latitude, longitude, creation_date, is_active) VALUES
  ('Grupo Mayor', 'Centre Historica Cuenca, Ecuador', 'Un grupo para personas mayores para aprender', -2.91392,
   -79.01411, '03-25-2018', true);
INSERT INTO public.homegroup (name, location, description, latitude, longitude, creation_date, is_active) VALUES
  ('Grupo Universitario', 'Avenida Loja, Cuenca, Ecuador',
   'Un grupo para estudiantes universitarios que se reúne todos los miércoles a las 6 p.m.', -2.9155438, -79.03264,
   '03-27-2018', true);


INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (2, 3, true);
INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (10, 1, true);
INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (3, 2, true);


INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 2, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 4, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (1, 3, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (1, 4, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (1, 5, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (1, 7, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 1, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 5, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 3, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 9, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 11, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 13, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 14, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 5, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 6, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 7, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 8, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 9, '01-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (2, 10, '02-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES (3, 12, '01-27-2018', true);


INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 3, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 4, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 5, 1, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 7, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 3, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 4, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 5, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 7, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 3, 3, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 4, 3, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 5, 3, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 7, 3, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 3, 4, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 4, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 5, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 7, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 3, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 4, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 5, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 7, 5, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 10, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 11, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 11, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 12, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 12, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 3, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 13, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 14, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 11, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 5, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 9, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 4, 15, true);


INSERT INTO public.member_role (member_id, password, role_id, is_active)
VALUES (1, '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG', 2, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active)
VALUES (2, '$2b$12$fFU3LXEp5t5yfggXUzZaIu/RdrQrr4NLC7pH4cTedNL4stXeq3d9q', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active)
VALUES (10, '$2b$12$QKxOfwupJyXuRopVFZdFVOasanhZRj0nhuwcoBWEClm9YnM6nG5Qq', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active)
VALUES (14, '$2b$12$FnTGF6vw669Caq3mpNKbpu9jSVpuQJpqtL/PqQSzR1qMBYxcto8.W', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active)
VALUES (3, '$2b$12$JrD7JZ.8cJDa/orbP4CGwORolalghHztPL9p22/kCLvMYTgOa.q3m', 1, true);
