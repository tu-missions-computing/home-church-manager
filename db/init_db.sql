
INSERT INTO marital_status(marital_status_name) values ('Soltero');
INSERT INTO marital_status(marital_status_name) values ('Casado');
INSERT INTO marital_status(marital_status_name) values ('Divorciado');
INSERT INTO marital_status(marital_status_name) values ('Viudo');
INSERT INTO marital_status(marital_status_name) values ('Otro');


INSERT INTO how_did_you_find_out(id, how_did_you_find_out_name) values (1,'Amigos o familia');
INSERT INTO how_did_you_find_out(id, how_did_you_find_out_name) values (2,'Estación de radio');
INSERT INTO how_did_you_find_out(id, how_did_you_find_out_name) values (3,'Medios de comunicación social');
INSERT INTO how_did_you_find_out(id, how_did_you_find_out_name) values (4,'Evento especial');
INSERT INTO how_did_you_find_out(id, how_did_you_find_out_name) values (5, 'Otro');



INSERT INTO member(email, first_name, last_name,  phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) values ('admin@example.com', 'Jonathan', 'Guido', '02-0398423',
'M', '1980-03-12', '1', 1, 1, '1', '03-27-2018', '1');


INSERT INTO member( email, first_name, last_name, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id,  is_a_parent, join_date, is_active)
VALUES ('john@example.com', 'John', 'Smith', '5555555555', 'M', '1980-03-12', '1', 2, 2, '1', '2016-08-01', '1');


INSERT INTO role (role) VALUES ('homegroup_leader');
INSERT INTO role (role) VALUES ('admin');



INSERT INTO public.meeting (id, date, time) VALUES (1, '2018-03-25', '23:26');
INSERT INTO public.meeting (id, date, time) VALUES (2, '2018-03-25', '23:26');
INSERT INTO public.meeting (id, date, time) VALUES (3, '2018-02-25', '23:27');
INSERT INTO public.meeting (id, date, time) VALUES (4, '2018-03-01', '23:30');
INSERT INTO public.meeting (id, date, time) VALUES (5, '2018-01-25', '23:31');
INSERT INTO public.meeting (id, date, time) VALUES (6, '2018-03-19', '22:45');
INSERT INTO public.meeting (id, date, time) VALUES (7, '2018-03-20', '20:46');
INSERT INTO public.meeting (id, date, time) VALUES (8, '2018-03-21', '19:47');
INSERT INTO public.meeting (id, date, time) VALUES (9, '2018-03-22', '17:48');
INSERT INTO public.meeting (id, date, time) VALUES (10, '2018-02-14', '23:55');
INSERT INTO public.meeting (id, date, time) VALUES (11, '2018-02-15', '23:56');
INSERT INTO public.meeting (id, date, time) VALUES (12, '2018-03-26', '09:18');
INSERT INTO public.meeting (id, date, time) VALUES (13, '2018-01-26', '09:19');
INSERT INTO public.meeting (id, date, time) VALUES (14, '2018-03-07', '00:29');
INSERT INTO public.meeting (id, date, time) VALUES (15, '2018-03-26', '10:30');



INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (101, 'Gustavo', 'A', 'example1@example.com', '555555555', 'M', '2018-03-21', true, 1, 3, false, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (102, 'Alejandra', 'Zambrano', 'Alejandra@gmail.com', '3323049293', 'F', '1995-02-08', true, 2, 3, false, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (103, 'Mendoza', 'Alfredo', 'mendoza@example.com', '5555555555', 'M', '2018-03-15', false, 1, 1, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (104, 'Garcia', 'Princeton', 'garcia@example.com', '7779998888', 'F', '2018-03-02', true, 2, 2, false, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (105, 'Pilar', 'Roberto', 'pilar@example.com', '8192929300', 'F', '2018-03-22', false, 4, 1, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (106, 'Xavier', 'Guillermo', 'xavier@example.com', '9102990999', 'M', '2018-03-21', true, 5, 1, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (107, 'Diego', 'Estaban', 'diego@example.com', '7478182999', 'M', '2018-03-06', false, 1, 2, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (108, 'Elena', 'Danilo', 'elena@example.com', '81992039929', 'F', '2018-03-13', true, 1, 3, false, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (109, 'Pepe', 'A', 'example2@example.com', '7182990000', 'M', '2018-03-16', true, 4, 3, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (110, 'Fernando', 'A', 'example3@example.com', '8829882000', 'M', '2018-03-11', true, 1, 2, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (111, 'Ishmael', 'A', 'example4@example.com', '82900039439', 'M', '2018-03-15', true, 4, 1, true, '2018-03-25', true);
INSERT INTO public.member (id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status_id,
 how_did_you_find_out_id, is_a_parent, join_date, is_active) VALUES (112, 'Ivanova', 'A', 'example5@example.com', '8289993000', 'M', '2018-03-14', true, 1, 3, false, '2018-03-25', true);


INSERT INTO public.homegroup ( name, location, description, latitude, longitude, creation_date, is_active) VALUES ( 'Grupo Parejas', 'Cuenca, Ecuador', 'Un grupo para que las parejas crezcan en su relación con Dios', -2.9001286, -79.0059, '03-24-2018', true);
INSERT INTO public.homegroup ( name, location, description, latitude, longitude, creation_date,  is_active) VALUES ( 'Grupo Mayor', 'Centre Historica Cuenca, Ecuador', 'Un grupo para personas mayores para aprender', -2.91392, -79.01411,'03-25-2018', true);
INSERT INTO public.homegroup ( name, location, description, latitude, longitude, creation_date, is_active) VALUES ( 'Grupo Universitario', 'Avenida Loja, Cuenca, Ecuador', 'Un grupo para estudiantes universitarios que se reúne todos los miércoles a las 6 p.m.', -2.9155438, -79.03264,'03-27-2018', true);


INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (2, 3, true);
INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (108, 1, true);
INSERT INTO public.homegroup_leader (member_id, homegroup_id, is_active) VALUES (101, 2, true);


INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 2, '03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 102,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (1, 101,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (1, 102,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (1, 103,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (1, 105,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 1,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 103,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 101,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 107,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 109,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 111,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 112,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 103,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 104,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 105,'03-27-2018', true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 106, '03-27-2018',true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 107, '03-27-2018',true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (2, 108, '03-27-2018',true);
INSERT INTO public.homegroup_member (homegroup_id, member_id,join_date, is_active) VALUES (3, 110, '03-27-2018',true);




INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 101, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 102, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 103, 1, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 105, 1, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 101, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 102, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 103, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 105, 2, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 101, 3, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 102, 3, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 103, 3, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 105, 3, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 101, 4, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 102, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 103, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 105, 4, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 101, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 102, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 103, 5, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (1, 105, 5, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 6, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 6, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 8, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 8, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 10, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 10, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 7, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 7, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 11, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 11, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 11, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 9, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 9, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 12, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 12, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 13, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 13, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 14, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 14, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 110, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 101, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 111, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 112, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 109, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 103, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 107, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 2, 15, false);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 1, 15, true);
INSERT INTO public.attendance (homegroup_id, member_id, meeting_id, attendance) VALUES (3, 102, 15, true);



INSERT INTO public.member_role (member_id, password, role_id, is_active) VALUES (1, '$2b$12$13vsC8uSUk2EhzNZRQNJju65HdsPmihPbwcuSDDiZ6oxFaI.cr0nG', 2, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active) VALUES (2, '$2b$12$fFU3LXEp5t5yfggXUzZaIu/RdrQrr4NLC7pH4cTedNL4stXeq3d9q', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active) VALUES (108, '$2b$12$QKxOfwupJyXuRopVFZdFVOasanhZRj0nhuwcoBWEClm9YnM6nG5Qq', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active) VALUES (112, '$2b$12$FnTGF6vw669Caq3mpNKbpu9jSVpuQJpqtL/PqQSzR1qMBYxcto8.W', 1, true);
INSERT INTO public.member_role (member_id, password, role_id, is_active) VALUES (101, '$2b$12$JrD7JZ.8cJDa/orbP4CGwORolalghHztPL9p22/kCLvMYTgOa.q3m', 1, true);
