# Home Church Manager

Developed By: Nysha Chen, Ryley Hoekert, Christine Urban, Krista Hapner, & Ellen Sokolowski


## Before You Begin
1. Add database and call it: MyDatabase.sqlite.
2. Add python file called `mail_settings.py`
   with your email settings. Use this template:
   
    def config_email(app):
        app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME='<your email address>'
            MAIL_PASSWORD='<your email password>'
        )

2. Run create_db.sql and init_db.sql to create and initialize the database
3. Log in to the iHogar@gmail.com account. **The password will be emailed to you.**

## Regular Visitor

The only permissions a regular visitor to the site has is to view the Home Group Locator,
FAQ, and Contact pages.

**Home Group Locator**
1. Type in the desired address into the search bar. This will locate your position on the
map, so you can visualize where you are in relation to Home Groups in the area.
2. Click on a red pin on the map to see the home group information, such as contact info.

**FAQ**

Lists common questions related to the site. 
You can also click on the link "Contact Our Support Team" at the bottom
to take you to our contact page.

**Contact**

This tab on the navigation bar will take you to a form where you can fill out a message. After clicking "Send",
check the iHogar@gmail.com account to see the message pop up in the inbox.

## Admnistrator

The admin has full priveleges and access to most functions of the site. The only function an admin cannot do is take attendance.

Default Login Information
- Email: `admin@example.com`
- Password: `password`

### Tasks

**View All Attendance**

You can view attendance for all the home groups on the chart on the admin homepage.
Click on the little hamburger menu in the top right of the chart to download as a JEPG, PNG, PDF, or vector image.

**Edit Personal Profile**
1. Open hamburger menu in top left screen and select "Welcome, Ryley"
1. Select "Profile Settings" from sub-menu
1. Edit information, press "Save Member"

**Change Password**
1. Open hamburger menu and select "Welcome, Ryley"
1. Select "Update Password" from sub-menu
1. Type in current password and new password, press "Update Password"

### Home Groups

**Create a Home Group**
1. Open hamburger menu and select Home Groups
1. Select green "Add Home Group" button
1. Fill out fields and press "Find Location"
1. Press "Save Home Group"
1. If you fail to fill out a field, errors will pop up telling you to fill in required fields.

**Edit a Home Group**
1. Open hamburger menu and select Home Groups
1. Press light blue edit button in desired Home Group's row
1. Edit desired fields and press Save Home Group

**View Members of a Home Group**
1. Open  hamburger menu and select Home Groups
1. Press yellow Members button in desired Home Group's row

**Add Member To a Specific Home Group**
1. Open hamburger menu and select Home Groups
1. Press yellow Members button in desired Home Group's row
1. Select Add Member
1. Search for Existing Member using search box. If member is found, select Add to Home Group.
1. If no member is found, select Create New Member
1. Fill out fields and press Save Member
1. If you fail to fill out a field, errors will pop up telling you to fill in required fields.

**Email Members of a Specific Home Group**
1. Open hamburger menu and select Home Groups
1. Press yellow Members button in desired Home Group's row
1. Select Email Members button. 
    This will open your computer's default mail application with "To" field pre-populated with
    the emails of the homegroup members.

**Search for Member of Home Group By Name**
1. Open hamburger menu and select Home Groups
1. Press yellow Members button in desired Home Group's row
1. Type in members name into the search bar, results will pop-up as you type.

**View Attendance Reports of a Specific Home Group**
1. Open hamburger menu and select Home Groups
1. Press dark blue Attendance button in desired Home Group's row
1. This will display a graph of the home group's attendance. It will also list all of the attendance reports
   submitted for that home group. Select the View button in the desired report row to view the attendance report.

**Delete a Home Group**
1. Open hamburger menu and select Home Groups
1. Press red Remove button in desired Home Group's row

**Reactivate a Home Group**
1. Open hamburger menu and select Home Groups
1. Make sure "Show Inactive Home Groups" checkbox is a selected at top of page
1. Press Reactivate button in desired Home Group's row

### CHURCH MEMBERS

These are all of the members of the church, including those who are in home groups**

**Add Member (General)**
1. Open task bar hamburger menu in top left screen and select Members
1. Select green "Add Member" button
1. Fill out fields and press "Save Member"
1. If you fail to fill out a field, errors will pop up telling you to fill in required fields.

**Edit Member Role (Create User Account)**
1. Open task bar hamburger menu in top left screen and select Members
1. Press yellow "Role" button in desired Member's row
1. Fill out member's email (enter your personal email for testing purposes)
   and temporary password (they will be able to change this)
1. Press "Create User". This will create a user account for the member so they can log into the system.
   An automatic email will be sent when you press the button--check your email to see the message.

**Search with Advanced Filters**
1. Open task bar hamburger menu and select "Members"
1. Press "Advanced Search" button under search bar
1. Select checkboxes next to criterion you want to filter by, then scroll down to see results

#### FAQ/Contact
 
See above for instructions


## Home Group Leader

The Homegroup Leader has limited priveleges--they can only take attendance, view reports, edit their homegroup,
and add/edit/delete members in their homegroup

Login Information:
- Email: `john@example.com`
- Password: `password`

### Attendance

**View Homegroup Attendance Graph**

You can view all attendance for your specific homegroup on the homepage.
This can be downloaded in several formats.

**Take Attendance**
1. Open hamburger menu and select Attendance1. Open hamburger menu and select Attendance
1. Enter in a date and time and select Take Attendance
1. Press the checkboxes next to all members present, click Save at bottom of screen

**View/Edit Past Attendance Reports**
1. Open hamburger menu and select Attendance
1. Press View Attendance History button
1. Select Edit button in desired Report's row
1. Edit by simply selecting/de-selecting checkbox next to member and click Save

### Home Group

**Edit Home Group Information**
1. Open hamburger menu and select Edit Home Group Info
1. Edit desired fields and click Save Homegroup

**View Homegroup Members**
1. Open hamburger menu and select Members
1. Edit/Remove/Reactivate member works the same as other pages

**Add Homegroup Member**
1. Open hamburger menu and select Members
1. Fill in all fields and press Save Member

### FAQ/Contact

See above for instructions

Thank you for using Home Church Manager! If you have any questions, please contact the developers:
* Krista Hapner (`krista_hapner@taylor.edu`)
* Nysha Chen (`nysha_chen@taylor.edu`)
* Ryley Hoekert (`ryley_hoekert@taylor.edu`)
* Ellen Sokolowski (`ellen_sokolowski@taylor.edu`)
* Christine Urban (`christine_urban@taylor.edu`)
