INSERT INTO member(email, first_name, last_name,  phone_number, gender, birthday, baptism_status, join_date ) values ('john@example.com', 'John', 'Smith', '555-555-5555', 'M', 'March 2, 1980', 1, 'August 1, 2016');
INSERT INTO member(email, first_name, last_name,  phone_number, gender, birthday, baptism_status, join_date ) values ('nysha@example.com', 'Nysha', 'Chen', '111-222-3333', 'F', 'May 2, 1990', 1, 'August 1, 2016');
INSERT INTO member(email, first_name, last_name,  phone_number, gender, birthday, baptism_status, join_date ) values ('christine@example.com', 'Christine', 'Urban', '555-135-3245', 'F', 'May 13, 1993', 1, 'August 1, 2016');

INSERT INTO homegroup(name, location, description, latitude, longitude) values ('TWEET', '236 W. Reade Ave \n Upland, IN 46989', 'Taylor Women Engaged in Engineering and Technology',40.4756, -85.4944);

INSERT INTO homegroup(name, location, description, latitude, longitude) values ('Ball State CRU', '2000 W University Ave Muncie, IN 47306', 'Cru at Ball State is a movement of people passionate about knowing Jesus and telling His story by getting, giving, and multiplying the Gospel.',40.2061, -85.4070);



INSERT INTO homegroup_member values (1,1,1);
INSERT INTO homegroup_member values (1,2,1);

INSERT INTO attendance VALUES (1,1,1,1);
INSERT INTO attendance VALUES (1,2,1,1);
INSERT INTO attendance VALUES (1,1,2,1);
INSERT INTO attendance VALUES (1,2,2,1);

INSERT INTO meeting(date, time) values ('03-07-2017', '12:00');
INSERT INTO meeting(date, time) values ('03-13-2017', '16:00');

INSERT INTO role(role) values ('member');
INSERT INTO role(role) values ('homegroup_leader');
INSERT INTO role(role) values ('admin');



INSERT INTO user(email, password, role_id) values ('john@example.com', 'password',  2);
INSERT INTO user(email, password, role_id) values ('nysha@example.com', 'password',  1);
INSERT INTO user(email, password, role_id) values ('christine@example.com', 'password', 3);


INSERT INTO homegroup_leader(user_id, homegroup_id) values(1, 1);