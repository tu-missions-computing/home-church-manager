import tempfile
import unittest
import os

from flask import g, url_for

import db

from application import app

app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True

        app.csrf_enable = False
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False

        app.config['BABEL_DEFAULT_LOCALE'] = 'en'

        self.client = app.test_client(use_cookies=True)
        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def post(self, url, data):
        return self.client.post(url, data=data, follow_redirects=True)

    def get(self, url):
        return self.client.get(url, follow_redirects=True)

    def login(self, email, password):
        return self.post(url_for('login'), {'email': email, 'password': password})

    def logout(self):
        return self.get(url_for('logout'))


class LoginTestCase(FlaskTestCase):
    def test_successful_login(self):
        response = self.login('admin@example.com', 'password')
        assert b'Log Out' in response.data
        response = self.logout()
        assert b'Log In' in response.data

    def test_failed_login(self):
        response = self.login('adminx', 'default')
        assert b'Invalid email address or password' in response.data


class AdminTestCase(FlaskTestCase):
    """Test the basic behavior of page routing and display for admin pages"""

    def setUp(self):
        super().setUp()
        self.login('admin@example.com', 'password')

    def tearDown(self):
        super().tearDown()
        self.logout()

    def test_all_members_page(self):
        """Verify the all members page."""
        resp = self.client.get(url_for('all_members'))
        self.assertIn(b'Name', resp.data, "Did not find the phrase: First Name")
        self.assertIn(b'Contact All Members', resp.data)

    def test_admin_dashboard(self):
        """Verify the all homegroups page."""
        resp = self.client.get(url_for('admin_home'))
        self.assertIn(b'Attendance Count', resp.data, "Did not find the phrase: Attendance Count")

    def test_all_homegroups_page(self):
        """Verify the all homegroups page."""
        resp = self.client.get(url_for('get_homegroups'))
        self.assertIn(b'All Home Groups', resp.data, "Did not find the phrase: All Home Groups")

    def test_profile_settings_page(self):
        """ Verify the profile settings page"""
        email = 'admin@example.com'
        db.open_db_connection('MyDatabase.sqlite')
        member = db.find_member_info(email)
        resp = self.client.get(url_for('edit_member', member_id=member['id']))
        self.assertIn(b'Edit My Info', resp.data, "Did not find the phrase: Edit My Info")

    def test_edit_password_page(self):
        email = 'admin@example.com'
        db.open_db_connection('MyDatabase.sqlite')
        user = db.find_user(email)
        resp = self.client.get(url_for('update_user', user_id=user['id']))
        self.assertIn(b'Update Password', resp.data, "Did not find the phrase: Update Password")
        self.assertIn(b'admin@example.com', resp.data, "Did not find the phrase: admin@example.com")

    def test_faq_page(self):
        resp = self.client.get(url_for('faq'))
        self.assertIn(b'Frequently Asked Questions', resp.data,
                        "Did not find the phrase: Frequently Asked Questions")
        self.assertIn(b'How do I view all members of all homegroups?', resp.data,
                        "Did not find the phrase: How do I view all members of all homegroups?")

    def test_contact_page(self):
        resp = self.client.get(url_for('contact'))
        self.assertIn(b'Contact Our Support Team', resp.data,
                        "Did not find the phrase: Contact Our Support Team")


class HGLeaderTestCase(FlaskTestCase):
    """Test the basic behavior of page routing and display for HG Leader pages"""

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_dashboard(self):
        """Verify the dashboard page."""
        self.logout()
        self.login('john@example.com', 'password')
        resp = self.client.get(url_for('dashboard'), follow_redirects=True)
        self.assertIn(b'Taylor Women Engaged in Engineering and Technology', resp.data,
                        "Did not find the phrase: Taylor Women Engaged in Engineering and Technology")

    def test_member_page(self):
        """Verify the member page."""
        self.login('john@example.com', 'password')
        resp = self.client.get(url_for('get_homegroup_members', homegroup_id=1), follow_redirects=True)
        self.assertIn(b'Homegroup Members', resp.data, "Did not find the phrase: Homegroup Members")

    def test_attendance_page(self):
        """Verify the member page."""
        self.login('john@example.com', 'password')
        resp = self.client.get(url_for('attendance', homegroup_id=1), follow_redirects=True)
        self.assertIn(b'Attendance Report', resp.data, "Did not find the phrase: Attendance Report")

    def test_edit_hg_page(self):
        """Verify the edit homegroup page."""
        self.login('john@example.com', 'password')
        resp = self.client.get(url_for('edit_homegroup', homegroup_id=1), follow_redirects=True)
        self.assertIn(b'Edit Home Group', resp.data, "Did not find the phrase: Edit Home Group")


class DatabaseTestCase(FlaskTestCase):
    """Test database access and update functions."""

    # This method is invoked once before all the tests in this test case.
    @classmethod
    def setUpClass(cls):
        """So that we don't overwrite application data, create a temporary database file."""
        (file_descriptor, cls.file_name) = tempfile.mkstemp()
        os.close(file_descriptor)

    # This method is invoked once after all the tests in this test case.

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary database file."""
        os.unlink(cls.file_name)

    @staticmethod
    def execute_script(resource_name):
        """Helper function to run a SQL script on the test database."""
        with app.open_resource(resource_name, mode='r') as f:
            g.db.cursor().executescript(f.read())
        g.db.commit()

    def setUp(self):
        """Open the database connection and create all the tables."""
        super(DatabaseTestCase, self).setUp()
        db.open_db_connection(self.file_name)
        self.execute_script('db/create_db.sql')

    def tearDown(self):
        """Clear all tables in the database and close the connection."""
        self.execute_script('db/clear_db.sql')
        db.close_db_connection()
        super(DatabaseTestCase, self).tearDown()

    # USER ########################################

    # Test adding a new user
    def test_add_user(self):
        """Make sure we can add a new user"""
        row_count = db.create_user("testing@test.com", "password", 1)
        self.assertEqual(row_count, 1)
        user_id = db.recent_user()['id']
        test_hg = db.find_user_info(user_id)
        self.assertIsNotNone(test_hg)
        self.assertEqual(test_hg['email'], 'testing@test.com')
        self.assertEqual(test_hg['password'], 'password')
        self.assertEqual(test_hg['role_id'], 1)

    # def test_edit_user(self):
    #     """Make sure we can edit a homegroup"""
    #     row_count = db.create_user("testing@test.com", "password", 1)
    #     user_id = db.recent_user()['id']
    #     row_count = db.update_user("testingggggg@test.com", "passwordssss", 1)
    #     test_hg = db.find_user_info(user_id)
    #     self.assertIsNotNone(test_hg)
    #     print("emaillll", test_hg['email'])
    #     self.assertEqual(test_hg['email'], 'testingggggg@test.com')
    #     self.assertEqual(test_hg['password'], 'passwordssss')
    #     self.assertEqual(test_hg['role_id'], 1)

    def test_find_roles(self):
        """Make sure we can find roles"""
        g.db.execute("INSERT INTO role(role) VALUES('admin')")
        roles = db.find_roles()
        self.assertEqual(roles[0][1], "admin")

    # def test_find_user(self):
    #     """Make sure we can find user"""
    #     row_count = db.create_member("Seth", "Gerald", "Seth@example.com", "922", "Male", "Christmas", 0, 0, "2/3/09")
    #     member_id = db.find()['id']

    # MEMBER ########################################

    # Test adding a new member
    def test_add_member(self):
        """Make sure we can add a new user"""
        row_count = db.create_member("Ryley", "Hoekert", "ryley@email.com", "7192009832", "Female", "Never", 1, 0,
                                     "9/12/16")
        self.assertEqual(row_count, 1)
        member_id = db.recent_member()['id']
        test_hg = db.find_member(member_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['first_name'], 'Ryley')
        self.assertEqual(test_hg['last_name'], 'Hoekert')
        self.assertEqual(test_hg['email'], 'ryley@email.com')
        self.assertEqual(test_hg['phone_number'], '7192009832')
        self.assertEqual(test_hg['gender'], 'Female')
        self.assertEqual(test_hg['birthday'], 'Never')
        self.assertEqual(test_hg['baptism_status'], 1)
        self.assertEqual(test_hg['join_date'], '9/12/16')

    def test_edit_member(self):
        """Make sure we can edit a homegroup"""
        row_count = db.create_member("Seth", "Gerald", "Seth@example.com", "922", "Male", "Christmas", 0, 0, "2/3/09")
        member_id = db.recent_member()['id']
        row_count = db.edit_member(member_id, 'First', 'Last', 'test@example.com', "2", "Male", "Easter", 1, 1,
                                   "2/3/09")
        test_hg = db.find_member(member_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['first_name'], 'First')
        self.assertEqual(test_hg['last_name'], 'Last')
        self.assertEqual(test_hg['email'], 'test@example.com')
        self.assertEqual(test_hg['phone_number'], '2')
        self.assertEqual(test_hg['gender'], 'Male')
        self.assertEqual(test_hg['birthday'], 'Easter')
        self.assertEqual(test_hg['baptism_status'], 1)
        self.assertEqual(test_hg['join_date'], '2/3/09')

    # HOME GROUP ########################################

    def test_add_homegroup(self):
        """Make sure we can add a new homegroup"""
        row_count = db.create_homegroup('Test HomeGroup', 'Test Location', 'Test Description', None, None)
        self.assertEqual(row_count, 1)
        homegroup_id = db.recent_homegroup()['id']
        test_hg = db.find_homegroup(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['Name'], 'Test HomeGroup')
        self.assertEqual(test_hg['Location'], 'Test Location')
        self.assertEqual(test_hg['Description'], 'Test Description')

    def test_edit_homegroup(self):
        """Make sure we can edit a homegroup"""
        row_count = db.create_homegroup('Fake', 'Fake Location', 'Fake Description', None, None)
        homegroup_id = db.recent_homegroup()['id']
        row_count = db.edit_homegroup(homegroup_id, 'Test HomeGroup', 'Test Location', 'Test Description', None, None)
        test_hg = db.find_homegroup(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['Name'], 'Test HomeGroup')
        self.assertEqual(test_hg['Location'], 'Test Location')
        self.assertEqual(test_hg['Description'], 'Test Description')


# Do the right thing if this file is run standalone.
if __name__ == '__main__':
    unittest.main()
