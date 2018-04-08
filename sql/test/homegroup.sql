-- Insert data for homegroup testing.

DO $$
DECLARE
  new_homegroup_id INTEGER;
  new_leader_id    INTEGER;
BEGIN
  INSERT INTO homegroup (name, location, description, latitude, longitude, creation_date, is_active)
  VALUES ('Home Group A', 'Cuenca, Ecuador', 'Test Home Group A', -2.9, -79, '2018-03-24', TRUE)
  RETURNING id
    INTO new_homegroup_id;

  new_leader_id := add_user('leader@example.com', 'homegroup_leader', 'H.G.', 'Leader');

  INSERT INTO homegroup_leader (member_id, homegroup_id, is_active)
  VALUES (new_leader_id, new_homegroup_id, TRUE);
END;
$$;


