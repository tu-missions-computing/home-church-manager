import unittest
from random import choice

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

    @staticmethod
    def create_test_member(suffix=''):
        marital = db.get_marital_status_by_name('Other')
        how = db.get_how_did_you_find_out_by_name('Other')
        return db.create_member({
            'first_name': 'New', 'last_name': 'Member', 'email': 'newmember' + suffix + '@example.com', 'phone_number': '555-1212',
            'gender': 'F', 'birthday': '2001-12-25',
            'baptism_status': True,
            'marital_status_id': marital['id'], 'how_did_you_find_out_id': how['id'],
            'is_a_parent': True, 'join_date': '2018-03-24'
        })


class LoginTestCase(DatabaseTestCase):
    def test_successful_login(self):
        response = self.login('admin@example.com', 'password')
        assert b'Log Out' in response.data
        response = self.logout()
        assert b'Log In' in response.data

    def test_failed_login(self):
        response = self.login('adminx', 'default')
        assert b'Invalid email address or password' in response.data


class AdminTestCase(DatabaseTestCase):
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

    def test_faq_page(self):
        resp = self.get(url_for('faq'))
        self.assertIn(b'Haga clic en la', resp.data)

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
        """Verify the member page"""
        resp = self.get(url_for('get_homegroup_members', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Home Group A Members', resp.data)

    def test_attendance_page(self):
        """Verify the attendance page"""
        resp = self.get(url_for('attendance', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Attendance Report', resp.data)

    def test_edit_hg_page(self):
        """Verify the edit homegroup page."""
        resp = self.get(url_for('edit_homegroup', homegroup_id=self.homegroup['id']))
        self.assertIn(b'Edit Home Group', resp.data)
        self.assertIn(b'Home Group A', resp.data)


class MemberTestCase(DatabaseTestCase):
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


class UserTestCase(DatabaseTestCase):
    def setUp(self):
        super().setUp()

        member_status = self.create_test_member()
        self.member_id = member_status['id']

        all_roles = db.get_all_roles()
        self.role_id = choice(all_roles)['id']

    def test_add_user(self):
        """Make sure we can add a new user: assign the user a role"""
        row_count = db.create_member_role(self.member_id, "password", self.role_id)
        self.assertEqual(row_count, 1)

        test_role = db.find_member_role(self.member_id)
        self.assertIsNotNone(test_role)
        self.assertEqual(test_role['member_id'], self.member_id)
        self.assertEqual(test_role['password'], 'password')
        self.assertEqual(test_role['role_id'], self.role_id)

    def test_edit_user(self):
        """Make sure we can change a password"""
        row_count = db.create_member_role(self.member_id, "PASSword", self.role_id)
        self.assertEqual(row_count, 1)

        row_count = db.update_password(self.member_id, "password", self.role_id)

        test_role = db.find_member_role(self.member_id)
        self.assertIsNotNone(test_role)
        self.assertEqual(test_role['member_id'], self.member_id)
        self.assertEqual(test_role['password'], 'password')
        self.assertEqual(test_role['role_id'], self.role_id)


class HomeGroupTestCase(DatabaseTestCase):
    def setUp(self):
        super().setUp()
        self.login('admin@example.com', 'password')
        self.admin_member = db.find_user('admin@example.com')

    @staticmethod
    def create_homegroup():
        return db.create_homegroup('Test Home Group', 'Test Location', 'Test Description', -3, -78)

    def test_add_homegroup(self):
        """Make sure we can add a new homegroup"""
        hg_status = self.create_homegroup()
        self.assertEqual(hg_status['rowcount'], 1)
        homegroup_id = hg_status['id']

        test_hg = db.find_homegroup_by_id(homegroup_id)
        self.assertIsNotNone(test_hg)

        self.assertEqual(test_hg['name'], 'Test Home Group')
        self.assertEqual(test_hg['location'], 'Test Location')
        self.assertEqual(test_hg['description'], 'Test Description')
        self.assertEqual(test_hg['latitude'], -3)
        self.assertEqual(test_hg['longitude'], -78)

    def test_edit_homegroup(self):
        """Check that we can edit a home group."""
        hg_status = self.create_homegroup()
        self.assertEqual(hg_status['rowcount'], 1)
        homegroup_id = hg_status['id']

        test_hg = db.find_homegroup_by_id(homegroup_id)
        self.assertIsNotNone(test_hg)

        row_count = db.edit_homegroup(homegroup_id, 'Updated Group', 'New Location',
                                      test_hg['description'], test_hg['latitude'], -79)

        test_hg = db.find_homegroup_by_id(homegroup_id)
        self.assertIsNotNone(test_hg)
        self.assertEqual(test_hg['name'], 'Updated Group')
        self.assertEqual(test_hg['location'], 'New Location')
        self.assertEqual(test_hg['description'], 'Test Description')
        self.assertEqual(test_hg['latitude'], -3)
        self.assertEqual(test_hg['longitude'], -79)

    def test_split_homegroup(self):
        hg_status = self.create_homegroup()
        self.assertEqual(hg_status['rowcount'], 1)
        to_split_id = hg_status['id']

        members = []
        for idx in range(0,10):
            member_status = self.create_test_member(suffix=str(idx))
            member_id = member_status['id']
            members.append(member_id)
            db.add_member_to_homegroup(to_split_id, member_id)

        hg_status = self.create_homegroup()
        split1_id = hg_status['id']

        hg_status = self.create_homegroup()
        split2_id = hg_status['id']

        cnt=0
        for member in members:
            if cnt % 2 == 0:
                group = 'one'
            else:
                group = 'two'
            cnt += 1
            #/split_member/<member_id>/<homegroup_id>/<homegroup_id1>/<homegroup_id2>/<group>
            resp = self.post(url_for('split_member',
                                     member_id=member,
                                     homegroup_id=to_split_id,
                                     homegroup_id1=split1_id,
                                     homegroup_id2=split2_id,
                                     group=group),
                             {})

        new_members = db.get_homegroup_members(to_split_id)
        self.assertEqual(len(new_members), 0)
        new_members1 = db.get_homegroup_members(split1_id)
        self.assertEqual(len(new_members1), 5)
        new_members2 = db.get_homegroup_members(split1_id)
        self.assertEqual(len(new_members2), 5)

        for idx in range(0,10):
            home_group = db.find_member_homegroup(members[idx])
            if idx %2 == 0:
                self.assertEqual(home_group['homegroup_id'], split1_id)
            else:
                self.assertEqual(home_group['homegroup_id'], split2_id)

# Do the right thing if this file is run standalone.
if __name__ == '__main__':
    unittest.main()
