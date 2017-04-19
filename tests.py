import tempfile
import unittest
import os

from flask import g, url_for

import db
from application import app




app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'



class FlaskTestCase(unittest.TestCase):
    # This is a helper class that sets up the proper Flask execution context
    # so that the test cases that inherit it will work properly.
    def setUp(self):
        # Allow exceptions (if any) to propagate to the test client.
        app.testing = True
        app.csrf_enable = False

        # Create a test client.
        self.client = app.test_client(use_cookies=True)
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False

        # Create an application context for testing.
        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        # Clean up the application context.
        self.app_context.pop()



class LoginTestCase(FlaskTestCase):
    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'Log' in rv.data
        rv = self.logout()
        assert b'Log In' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Log In' in rv.data


class ApplicationTestCase(FlaskTestCase):
    """Test the basic behavior of page routing and display"""
    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_all_members_page(self):
        """Verify the all members page."""
        self.login('admin@example.com', 'password')
        resp = self.client.get(url_for('dashboard'))
        # print(resp.data)
        self.assertTrue(b'All' in resp.data, "Did not find the phrase: First")
    # def test_all_homegroups_page(self):
    #     """Verify the all homegroups page."""
    #     self.create_user('admin', 'default')
    #     rv = self.login('admin', 'default')
    #     resp = self.client.get(url_for('get_homegroups'))
    #     self.assertTrue(b'Members'in resp.data, "Did not find the word: Members")
    #     self.assertTrue(b'Edit' in resp.data, "Did not find the word: Edit")
    #     self.assertTrue(b'All Home Groups' in resp.data, "Did not find the phrase: All Home Groups")



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
        row_count = db.edit_homegroup(homegroup_id,'Test HomeGroup', 'Test Location', 'Test Description', None, None)
        test_hg = db.find_homegroup(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['Name'], 'Test HomeGroup')
        self.assertEqual(test_hg['Location'], 'Test Location')
        self.assertEqual(test_hg['Description'], 'Test Description')

# Do the right thing if this file is run standalone.
if __name__ == '__main__':
    unittest.main()