import unittest

from flask import g, url_for

from application import app
import db


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        app.csrf_enable = False

        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'
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


class DatabaseTestCase(FlaskTestCase):
    @staticmethod
    def bounce_db_connection():
        """Bounce the database connection; ensures data are persistent."""
        db.close_db_connection()
        db.open_db_connection()

    @staticmethod
    def execute_sql(resource_name):
        """Helper function to run a SQL script on the database."""
        with app.open_resource(resource_name, mode='r') as f:
            g.cursor.execute(f.read())
        g.connection.commit()

    def setUp(self):
        super().setUp()
        db.open_db_connection()
        self.execute_sql('sql/clear-db.sql')
        self.execute_sql('sql/init-db.sql')

    def tearDown(self):
        self.execute_sql('sql/clear-db.sql')
        self.execute_sql('sql/init-db.sql')
        db.close_db_connection()
        super().tearDown()


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_member = None

    def setUp(self):
        super().setUp()
        self.login('admin@example.com', 'password')
        self.admin_member = db.find_user('admin@example.com')
        self.assertIsNotNone(self.admin_member, "Can't find admin member")

    def tearDown(self):
        self.logout()
        super().tearDown()

    def test_all_members_page(self):
        """Verify the all members page."""
        resp = self.get(url_for('all_members'))
        self.assertIn(b'Name', resp.data)
        self.assertIn(b'Contact All Members', resp.data)

    def test_admin_dashboard(self):
        """Verify the admin dashboard."""
        resp = self.get(url_for('admin_home'))
        self.assertIn(b'ATTENDING HOME GROUPS', resp.data)

    def test_all_homegroups_page(self):
        """Verify the all homegroups page."""
        resp = self.get(url_for('get_homegroups'))
        self.assertIn(b'All Home Groups', resp.data, "Did not find the phrase: All Home Groups")

    def test_profile_settings_page(self):
        """ Verify the profile settings page"""
        resp = self.get(url_for('edit_member', member_id=self.admin_member['id']))
        self.assertIn(b'Edit My Info', resp.data, "Did not find the phrase: Edit My Info")

    def test_edit_password_page(self):
        resp = self.get(url_for('update_user', user_id=self.admin_member['id']))
        self.assertIn(b'Update Password', resp.data, "Did not find the phrase: Update Password")

    @unittest.skip('Need better way to localize FAQ page')
    def test_faq_page(self):
        resp = self.get(url_for('faq'))
        self.assertIn(b'Frequently Asked Questions', resp.data)
        self.assertIn(b'How do I view', resp.data)

    def test_contact_page(self):
        resp = self.get(url_for('contact'))
        self.assertIn(b'Contact Our Team', resp.data)


class HomeGroupLeaderTestCase(DatabaseTestCase):
    """Test the basic behavior of page routing and display for HG Leader pages"""

    def setUp(self):
        super().setUp()
        self.execute_sql('sql/test/homegroup.sql')
        self.homegroup = db.find_homegroup_by_name('Home Group A')
        self.login('leader@example.com', 'password')

    def tearDown(self):
        self.logout()
        super().tearDown()

    def test_dashboard(self):
        """Verify the dashboard page."""
        resp = self.get(url_for('dashboard'))
        self.assertIn(b'Home Group A Dashboard', resp.data)

    def test_member_page(self):
        """Verify the member page."""
        resp = self.get(url_for('get_homegroup_members', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Home Group A Members', resp.data)

    def test_attendance_page(self):
        """Verify the attendance page."""
        resp = self.get(url_for('attendance', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Attendance Report', resp.data)

    def test_edit_hg_page(self):
        """Verify the edit homegroup page."""
        resp = self.get(url_for('edit_homegroup', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Edit Home Group', resp.data)
        self.assertIn(b'Home Group A', resp.data)


class MemberTestCase(DatabaseTestCase):
    @staticmethod
    def create_test_member():
        marital = db.get_marital_status_by_name('Other')
        how = db.get_how_did_you_find_out_by_name('Other')

        return db.create_member({
            'first_name': 'New', 'last_name': 'Member', 'email': 'newmember@example.com', 'phone_number': '555-1212',
            'gender': 'F', 'birthday': '2001-12-25',
            'baptism_status': True,
            'marital_status_id': marital['id'], 'how_did_you_find_out_id': how['id'],
            'is_a_parent': True, 'join_date': '2018-03-24'
        })

    def test_add_member(self):
        """Make sure we can add a new member."""
        member_status = self.create_test_member()
        self.assertEqual(member_status['rowcount'], 1)

        self.bounce_db_connection()

        test_member = db.find_member(member_status['id'])
        self.assertIsNotNone(test_member)

        self.assertEqual(test_member['first_name'], 'New')
        self.assertEqual(test_member['last_name'], 'Member')
        self.assertEqual(test_member['email'], 'newmember@example.com')
        self.assertEqual(test_member['phone_number'], '555-1212')
        self.assertEqual(test_member['gender'], 'F')
        self.assertEqual(test_member['birthday'], '2001-12-25')
        self.assertEqual(test_member['baptism_status'], True)
        self.assertEqual(test_member['join_date'], '2018-03-24')

    def test_edit_member(self):
        """Make sure we can edit an existing member."""
        member_status = self.create_test_member()
        self.assertEqual(member_status['rowcount'], 1)

        member_id = member_status['id']
        test_member = db.find_member(member_id)
        self.assertIsNotNone(test_member)

        test_member['first_name'] = 'Edited'
        test_member['email'] = 'editedmember@example.com'
        test_member['phone_number'] = '555-1234'
        test_member['join_date'] = '2017-03-24'
        row_count = db.edit_member(test_member)
        self.assertEqual(row_count, 1)

        self.bounce_db_connection()

        edited_member = db.find_member(member_id)
        self.assertIsNotNone(edited_member)
        self.assertEqual(edited_member['first_name'], 'Edited')
        self.assertEqual(edited_member['last_name'], 'Member')
        self.assertEqual(edited_member['email'], 'editedmember@example.com')
        self.assertEqual(edited_member['phone_number'], '555-1234')
        self.assertEqual(edited_member['gender'], 'F')
        self.assertEqual(edited_member['birthday'], '2001-12-25')
        self.assertEqual(edited_member['baptism_status'], True)
        self.assertEqual(edited_member['join_date'], '2017-03-24')
        self.assertEqual(edited_member['is_active'], True)

class UserTestCase(FlaskTestCase):
    def test_add_user(self):
        """Make sure we can add a new user"""
        row_count = db.create_member_role("testing@test.com", "password", 1)
        self.assertEqual(row_count, 1)
        user_id = db.recent_user()['id']
        test_hg = db.find_user_info(user_id)
        self.assertIsNotNone(test_hg)
        self.assertEqual(test_hg['email'], 'testing@test.com')
        self.assertEqual(test_hg['password'], 'password')
        self.assertEqual(test_hg['role_id'], 1)

    # def test_edit_user(self):
    #     """Make sure we can edit a homegroup"""
    #     row_count = db.create_member_role("testing@test.com", "password", 1)
    #     user_id = db.recent_user()['id']
    #     row_count = db.update_password("testingggggg@test.com", "passwordssss", 1)
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


class HomeGroupTestCase(FlaskTestCase):
    def test_add_homegroup(self):
        """Make sure we can add a new homegroup"""
        row_count = db.create_homegroup('Test HomeGroup', 'Test Location', 'Test Description', None, None)
        self.assertEqual(row_count, 1)
        homegroup_id = db.recent_homegroup()['id']
        test_hg = db.find_homegroup_by_id(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['Name'], 'Test HomeGroup')
        self.assertEqual(test_hg['Location'], 'Test Location')
        self.assertEqual(test_hg['Description'], 'Test Description')

    def test_edit_homegroup(self):
        """Make sure we can edit a homegroup"""
        row_count = db.create_homegroup('Fake', 'Fake Location', 'Fake Description', None, None)
        homegroup_id = db.recent_homegroup()['id']
        row_count = db.edit_homegroup(homegroup_id, 'Test HomeGroup', 'Test Location', 'Test Description', None, None)
        test_hg = db.find_homegroup_by_id(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['Name'], 'Test HomeGroup')
        self.assertEqual(test_hg['Location'], 'Test Location')
        self.assertEqual(test_hg['Description'], 'Test Description')

# Do the right thing if this file is run standalone.
if __name__ == '__main__':
    unittest.main()
