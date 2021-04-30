import os
import sys
import getpass
import pyodbc
from tkinter import *
from tkinter import ttk


global conn
global os_username

conn = pyodbc.connect(
    Driver = '{ODBC Driver 17 for SQL Server}',
    Server = 'us1261960w1\sqlexpress',
    Database = 'TimeEntryDB',
    Trusted_Connection = 'Yes',
    uid = 'TimeEntryApplication',
    password = 'password')

os_username = getpass.getuser()

def return_firstname(os_username):
	cur = conn.cursor()
	cur.execute("SELECT [FirstName] FROM TimeEntryDB.dbo.Users WHERE [OS_Username] = ?", (os_username))
	name = StringVar()
	data = []
	for name in cur.fetchall():
		data.append(name[0])
	return str(data)[2:-2]

def insert_detail(selected_client, selected_engagement, payperiod_entry, date_entry, hours_entry, comments_entry, os_username):
	cur = conn.cursor()
	cur.execute("INSERT INTO TimeEntryDB.dbo.Timesheet_Entries ([Client], [Engagement], [PayPeriod], [WorkDate], [HoursWorked], [Notes], [Username], [Status]) VALUES (?, ?, ?, ?, ?, ?, ?, 'Not Submitted')", (selected_client, selected_engagement, payperiod_entry, date_entry, hours_entry, comments_entry, os_username))
	cur.execute("""SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
				BEGIN TRANSACTION;

				DECLARE @payperiod as varchar(50)
				DECLARE @username as varchar(50)
				DECLARE @status as varchar(50)

				SET @payperiod = ?
				SET @username = ?
				SET @status = 'Not Submitted'

				UPDATE TimeEntryDB.dbo.DimPayPeriodStatus SET [Status] = 'Not Submitted' WHERE [PayPeriod] = @payperiod AND [Username] = @username AND [Status] = @status;
				IF @@ROWCOUNT = 0
				BEGIN
				INSERT TimeEntryDB.dbo.DimPayPeriodStatus([PayPeriod], [Username], [Status]) SELECT @payperiod, @username, @status;
				END
				COMMIT TRANSACTION""", payperiod_entry, os_username)
	conn.commit()
	os.system('py -3 successful_entry_window.py')
	#conn.close()

def view_detail(os_username):
	cur = conn.cursor()
	cur.execute("SELECT [EntryID], [PayPeriod], [WorkDate], [Client], [Engagement], [Notes], [HoursWorked], [Status], [Username] FROM TimeEntryDB.dbo.Timesheet_Entries WHERE [Username] = ? GROUP BY [EntryID], [PayPeriod], [WorkDate], [Client], [Engagement], [Notes], [HoursWorked], [Status], [Username] ORDER BY [EntryID] DESC", os_username)
	rows = cur.fetchall()
	return rows

def delete_selectItem(rowid):
    cur = conn.cursor()
    cur.execute("DELETE FROM TimeEntryDB.dbo.Timesheet_Entries WHERE [EntryID] = ?", rowid)
    conn.commit()
    os.system('py -3 successful_delete_window.py')

def clientengagement_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT Client_Engagement FROM TimeEntryDB.dbo.DimClientEngagements")
    data = []
    for client_list in cur.fetchall():
        data.append(client_list[0])
    return data

def client_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT [ClientName] FROM TimeEntryDB.dbo.DimClientEngagements GROUP BY [ClientName] ORDER BY [ClientName] ASC")
    data = []
    for client_list in cur.fetchall():
        data.append(client_list[0])
    return data

def engagement_dropdown(client = None):
    cur = conn.cursor()
    cur.execute("SELECT [EngagementName] FROM TimeEntryDB.dbo.DimClientEngagements WHERE [ClientName] = ?", client)
    data = []
    for engagement_list in cur.fetchall():
        data.append(engagement_list[0])
    return data

def engagementcode_dropdown(client = None, engagement = None):
    cur = conn.cursor()
    cur.execute("SELECT [EngagementID] FROM TimeEntryDB.dbo.DimClientEngagements WHERE [ClientName] = ? AND [EngagementName] = ?", client, engagement)
    data = []
    for engagementcode_list in cur.fetchall():
        data.append(engagementcode_list[0])
    return data

def payperiod_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT dpp.[PayPeriod] FROM TimeEntryDB.dbo.DimPayPeriod dpp WITH (NOLOCK) LEFT JOIN TimeEntryDB.dbo.Timesheet_Entries te ON dpp.[PayPeriod] = te.[PayPeriod] WHERE te.[Status] IN('Not Submitted', 'Rejected') OR (GETDATE() + DAY(14) >= dpp.[Date] AND te.[Status] IS NULL) GROUP BY dpp.[PayPeriod] ORDER BY max(dpp.[Date]) DESC")
    data = []
    for payperiod_list in cur.fetchall():
        data.append(payperiod_list[0])
    return data

def date_dropdown(payperiod = None):
    cur = conn.cursor()
    cur.execute("SELECT [Date] FROM TimeEntryDB.dbo.DimPayPeriod WHERE PayPeriod = ?", payperiod)
    data = []
    for date_list in cur.fetchall():
        data.append(date_list[0])
    return data

def hours_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT HourIncrements FROM TimeEntryDB.dbo.DimHourIncrements")
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def user_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT [FirstName] from TimeEntryDB.dbo.Users GROUP BY [FirstName] ORDER BY [FirstName] ASC")
    data = []
    for user_list in cur.fetchall():
        data.append(user_list[0])
    return data

def hours_sum():
    cur = conn.cursor()
    cur.execute("SELECT SUM(HourIncrements) FROM TimeEntryDB.dbo.DimHourIncrements")
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def submit_timesheet(payperiodselected, os_username):
	cur = conn.cursor()
	cur.execute("UPDATE TimeEntryDB.dbo.DimPayPeriodStatus SET [Status] = 'Awaiting Approval' FROM TimeEntryDB.dbo.Timesheet_Entries te INNER JOIN TimeEntryDB.dbo.DimPayPeriodStatus dpps ON te.[Username] = dpps.[Username] AND te.[PayPeriod] = dpps.[PayPeriod] WHERE te.[PayPeriod] = ? AND te.[Username] = ?", payperiodselected, os_username)
	cur.execute("UPDATE TimeEntryDB.dbo.Timesheet_Entries SET [Status] = dpps.[Status] FROM TimeEntryDB.dbo.Timesheet_Entries te INNER JOIN TimeEntryDB.dbo.DimPayPeriodStatus dpps ON te.[Username] = dpps.[Username] AND te.[PayPeriod] = dpps.[PayPeriod] WHERE te.[PayPeriod] = ? AND te.[Username] = ?", payperiodselected, os_username)
	conn.commit()
	os.system('py -3 successful_timesheet_submission_window.py')
	#conn.close()

def payperiodselected():
    cur = conn.cursor()
    cur.execute("SELECT [PayPeriod] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for payperiod_list in cur.fetchall():
        data.append(payperiod_list[0])
    return data

def clientnameelected():
    cur = conn.cursor()
    cur.execute("SELECT [ClientName] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for client_list in cur.fetchall():
        data.append(client_list[0])
    return data

def workdateselected():
    cur = conn.cursor()
    cur.execute("SELECT [WorkDate] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for workdate_list in cur.fetchall():
        data.append(workdate_list[0])
    return data

def notesentered():
    cur = conn.cursor()
    cur.execute("SELECT [Notes] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for notes_list in cur.fetchall():
        data.append(notes_list[0])
    return data

def hoursentered():
    cur = conn.cursor()
    cur.execute("SELECT [HoursWorked] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def currentstatus():
    cur = conn.cursor()
    cur.execute("SELECT [Status] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for status_list in cur.fetchall():
        data.append(status_list[0])
    return data

def unsubmittedtimesheets(payperiod = None):
    cur = conn.cursor()
    cur.execute("SELECT [FirstName] FROM Users LEFT JOIN Timesheet_Entries ON Users.OS_Username = Timesheet_Entries.Username LEFT JOIN DimPayPeriod ON Timesheet_Entries.PayPeriod = DimPayPeriod.PayPeriod WHERE Timesheet_Entries.[Status] = 'Not Submitted' AND DimPayPeriod.[PayPeriod] = ? Group BY Users.FirstName", payperiod)
    data = []
    for unsubmitted in cur.fetchall():
        data.append(unsubmitted[0])
    return data
###################################################################################################
###################################################################################################

def week1_monday(os_username):
    cur = conn.cursor()
    cur.execute(
        """SELECT
	    CASE
            WHEN DATENAME(dw, GETDATE()) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, GETDATE()) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
            ELSE 0
	    END
        FROM Timesheet_Entries te
        LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
        WHERE dpp.[Weekday] = 'Monday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
        GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_monday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Monday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Monday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_tuesday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Tuesday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_tuesday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Tuesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Tuesday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_wednesday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Wednesday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_wednesday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Wednesday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Wednesday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_thursday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Thursday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_thursday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Thursday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Thursday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_friday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Friday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_friday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Friday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Friday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_saturday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Saturday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_saturday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Saturday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Saturday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_sunday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Sunday' AND dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week2_sunday(os_username):
    cur = conn.cursor()
    cur.execute("""SELECT
	CASE 
		WHEN DATENAME(dw, GETDATE()) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 1 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, GETDATE()) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -1, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -2, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -3, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -4, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -5, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		WHEN DATENAME(dw, dateadd(DD, -6, cast(getdate() as date))) = 'Sunday' AND dpp.[WeekNumber] = 2 THEN SUM(te.[HoursWorked])
		ELSE 0
	END
FROM Timesheet_Entries te
LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
WHERE dpp.[Weekday] = 'Sunday' AND dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= [Week1Date] AND CONVERT(date, GETDATE()) <= [Week2Date] AND te.[Username] = ?
GROUP BY dpp.[WeekNumber]""", os_username)
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def week1_total(os_username):
	cur = conn.cursor()
	cur.execute("SELECT SUM(te.[HoursWorked]) FROM Timesheet_Entries te LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate] WHERE dpp.[WeekNumber] = 1 AND CONVERT(date, GETDATE()) >= dpp.[Week1Date] AND CONVERT(date, GETDATE()) <= dpp.[Week2Date] AND te.[Username] = ? GROUP BY dpp.[WeekNumber]", os_username)
	data = []
	for hours_list in cur.fetchall():
		data.append(hours_list[0])
	return data

def week2_total(os_username):
	cur = conn.cursor()
	cur.execute("SELECT SUM(te.[HoursWorked]) FROM Timesheet_Entries te LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate] WHERE dpp.[WeekNumber] = 2 AND CONVERT(date, GETDATE()) >= dpp.[Week1Date] AND CONVERT(date, GETDATE()) <= dpp.[Week2Date] AND te.[Username] = ? GROUP BY dpp.[WeekNumber]", os_username)
	data = []
	for hours_list in cur.fetchall():
		data.append(hours_list[0])
	return data

def week1_by_client_hours(os_username):
	cur = conn.cursor()
	cur.execute("""
		SELECT

			COALESCE(te.[Client], 'Total') AS [Client]
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Monday' THEN [HoursWorked] ELSE 0 END) AS 'Monday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Tuesday' THEN [HoursWorked] ELSE 0 END) AS 'Tuesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Wednesday' THEN [HoursWorked] ELSE 0 END) AS 'Wednesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Thursday' THEN [HoursWorked] ELSE 0 END) AS 'Thursday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Friday' THEN [HoursWorked] ELSE 0 END) AS 'Friday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Saturday' THEN [HoursWorked] ELSE 0 END) AS 'Saturday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Sunday' THEN [HoursWorked] ELSE 0 END) AS 'Sunday'
			,SUM([HoursWorked]) AS [Total]

		FROM Timesheet_Entries te
		LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
		WHERE dpp.[WeekNumber] = 1 AND GETDATE() >= dateadd(d, -7, [Week1Date]) AND GETDATE() <= [Week2Date] AND te.[Username] = ?
		GROUP BY ROLLUP(te.[Client])""", os_username)
	rows = cur.fetchall()
	return rows

def week2_by_client_hours(os_username):
	cur = conn.cursor()
	cur.execute("""
		SELECT

			COALESCE(te.[Client], 'Total') AS [Client]
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Monday' THEN [HoursWorked] ELSE 0 END) AS 'Monday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Tuesday' THEN [HoursWorked] ELSE 0 END) AS 'Tuesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Wednesday' THEN [HoursWorked] ELSE 0 END) AS 'Wednesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Thursday' THEN [HoursWorked] ELSE 0 END) AS 'Thursday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Friday' THEN [HoursWorked] ELSE 0 END) AS 'Friday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Saturday' THEN [HoursWorked] ELSE 0 END) AS 'Saturday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 2 AND dpp.[Weekday] = 'Sunday' THEN [HoursWorked] ELSE 0 END) AS 'Sunday'
			,SUM([HoursWorked]) AS [Total]

		FROM Timesheet_Entries te
		LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
		WHERE dpp.[WeekNumber] = 2 AND GETDATE() >= dateadd(d, -7, [Week1Date]) AND GETDATE() <= [Week2Date] AND te.[Username] = ?
		GROUP BY ROLLUP(te.[Client])""", os_username)
	rows = cur.fetchall()
	return rows

def weeks_combined(os_username):
	cur = conn.cursor()
	cur.execute("""
		SELECT

			COALESCE(dpp.[Week], 'Total') AS [Week]
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Monday' THEN [HoursWorked] ELSE 0 END) AS 'Monday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Tuesday' THEN [HoursWorked] ELSE 0 END) AS 'Tuesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Wednesday' THEN [HoursWorked] ELSE 0 END) AS 'Wednesday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Thursday' THEN [HoursWorked] ELSE 0 END) AS 'Thursday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Friday' THEN [HoursWorked] ELSE 0 END) AS 'Friday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Saturday' THEN [HoursWorked] ELSE 0 END) AS 'Saturday'
			,SUM(CASE WHEN dpp.[WeekNumber] = 1 AND dpp.[Weekday] = 'Sunday' THEN [HoursWorked] ELSE 0 END) AS 'Sunday'
			,SUM([HoursWorked]) AS [Total]

		FROM Timesheet_Entries te
		LEFT JOIN DimPayPeriod dpp ON dpp.[Date] = te.[WorkDate]
		WHERE GETDATE() >= dateadd(d, -7, [Week1Date]) AND GETDATE() <= [Week2Date]
		GROUP BY ROLLUP(dpp.[Week])""")
	rows = cur.fetchall()
	return rows