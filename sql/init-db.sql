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


SELECT add_user('admin@example.com', 'admin', 'Admin', 'User');
