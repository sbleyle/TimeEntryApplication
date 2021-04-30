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

def payperiod_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT [PayPeriod] FROM TimeEntryDB.dbo.DimPayPeriod GROUP BY [PayPeriod] ORDER BY max([Date]) ASC")
    data = []
    for payperiod_list in cur.fetchall():
        data.append(payperiod_list[0])
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

def hours_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT HourIncrements FROM TimeEntryDB.dbo.DimHourIncrements")
    data = []
    for hours_list in cur.fetchall():
        data.append(hours_list[0])
    return data

def user_dropdown():
    cur = conn.cursor()
    cur.execute("SELECT [FullName] from TimeEntryDB.dbo.Users GROUP BY [FullName] ORDER BY [FullName] ASC")
    data = []
    for user_list in cur.fetchall():
        data.append(user_list[0])
    return data

def lock_timesheet(payperiodselected, userselected, os_username):
	cur = conn.cursor()
	cur.execute("UPDATE TimeEntryDB.dbo.DimPayPeriodStatus SET [Status] = 'Under Review' FROM TimeEntryDB.dbo.Users u WHERE DimPayPeriodStatus.[PayPeriod] = ? AND u.[FullName] = ? AND u.[OS_Username] = DimPayPeriodStatus.[Username]", payperiodselected, userselected)
	cur.execute("UPDATE TimeEntryDB.dbo.Timesheet_Entries SET [Status] = dpps.[Status] FROM TimeEntryDB.dbo.Timesheet_Entries te INNER JOIN TimeEntryDB.dbo.DimPayPeriodStatus dpps ON te.[Username] = dpps.[Username] AND te.[PayPeriod] = dpps.[PayPeriod] WHERE te.[PayPeriod] = ? AND te.[Username] = ?", payperiodselected, os_username)
	os.system('py -3 successful_timesheet_lock_window.py')
	conn.commit()
	#conn.close()

def approve_timesheet(payperiodselected, userselected, os_username):
	cur = conn.cursor()
	cur.execute("UPDATE TimeEntryDB.dbo.DimPayPeriodStatus SET [Status] = 'Approved' FROM TimeEntryDB.dbo.Users u WHERE DimPayPeriodStatus.[PayPeriod] = ? AND u.[FullName] = ? AND u.[OS_Username] = DimPayPeriodStatus.[Username]", payperiodselected, userselected)
	cur.execute("UPDATE TimeEntryDB.dbo.Timesheet_Entries SET [Status] = dpps.[Status] FROM TimeEntryDB.dbo.Timesheet_Entries te INNER JOIN TimeEntryDB.dbo.DimPayPeriodStatus dpps ON te.[Username] = dpps.[Username] AND te.[PayPeriod] = dpps.[PayPeriod] WHERE te.[PayPeriod] = ? AND te.[Username] = ?", payperiodselected, os_username)
	os.system('py -3 successful_timesheet_approval_window.py')
	conn.commit()
	#conn.close()

def reject_timesheet(payperiodselected, userselected, os_username):
	cur = conn.cursor()
	cur.execute("UPDATE TimeEntryDB.dbo.DimPayPeriodStatus SET [Status] = 'Rejected' FROM TimeEntryDB.dbo.Users u WHERE DimPayPeriodStatus.[PayPeriod] = ? AND u.[FullName] = ? AND u.[OS_Username] = DimPayPeriodStatus.[Username]", payperiodselected, userselected)
	cur.execute("UPDATE TimeEntryDB.dbo.Timesheet_Entries SET [Status] = dpps.[Status] FROM TimeEntryDB.dbo.Timesheet_Entries te INNER JOIN TimeEntryDB.dbo.DimPayPeriodStatus dpps ON te.[Username] = dpps.[Username] AND te.[PayPeriod] = dpps.[PayPeriod] WHERE te.[PayPeriod] = ? AND te.[Username] = ?", payperiodselected, os_username)
	os.system('py -3 successful_timesheet_rejection_window.py')
	conn.commit()
	#conn.close()

def payperiodselected():
    cur = conn.cursor()
    cur.execute("SELECT [PayPeriod] FROM TimeEntryDB.dbo.Timesheet_Entries")
    data = []
    for payperiod_list in cur.fetchall():
        data.append(payperiod_list[0])
    return data

def submittedtimesheets(payperiod, os_username):
    cur = conn.cursor()
    cur.execute("SELECT [FullName] FROM Users LEFT JOIN Timesheet_Entries ON Users.[OS_Username] = Timesheet_Entries.[Username] LEFT JOIN DimPayPeriod ON Timesheet_Entries.[PayPeriod] = DimPayPeriod.[PayPeriod] WHERE Timesheet_Entries.[Status] IN('Awaiting Approval', 'Under Review') AND DimPayPeriod.[PayPeriod] = ? AND Users.[TimeApprover] = ? Group BY Users.FullName", payperiod, os_username)
    data = []
    for submitted in cur.fetchall():
        data.append(submitted[0])
    return data

def hours_by_client_engagement(payperiod_selected, user_selected):
	cur = conn.cursor()
	cur.execute("SELECT [Client], [Engagement], SUM([HoursWorked]) AS [Hours Worked] FROM TimeEntryDB.dbo.Timesheet_Entries LEFT JOIN Users ON Timesheet_Entries.[Username] = Users.[OS_Username] WHERE Timesheet_Entries.[PayPeriod] = ? AND Users.[FullName] = ? GROUP BY [Client], [Engagement]", payperiod_selected, user_selected)
	rows = cur.fetchall()
	return rows

def hours_by_day(payperiod_selected, user_selected):
	cur = conn.cursor()
	cur.execute("SELECT [WorkDate], [Weekday], SUM([HoursWorked]) AS [Hours Worked] FROM TimeEntryDB.dbo.Timesheet_Entries LEFT JOIN DimPayPeriod ON DimPayPeriod.[Date] = Timesheet_Entries.[WorkDate] LEFT JOIN Users ON Timesheet_Entries.[Username] = Users.[OS_Username] WHERE Timesheet_Entries.[PayPeriod] = ? AND Users.[FullName] = ? GROUP BY [WorkDate], [Weekday] ORDER BY [WorkDate] ASC", payperiod_selected, user_selected)
	rows = cur.fetchall()
	return rows

def notes_by_day_client(payperiod_selected, user_selected):
	cur = conn.cursor()
	cur.execute("SELECT [WorkDate], [Client], [Notes], SUM([HoursWorked]) AS [HoursWorked] FROM TimeEntryDB.dbo.Timesheet_Entries LEFT JOIN TimeEntryDB.dbo.Users ON Timesheet_Entries.[Username] = Users.[OS_Username] LEFT JOIN TimeEntryDB.dbo.DimPayPeriod ON Timesheet_Entries.[WorkDate] = DimPayPeriod.[Date] WHERE Timesheet_Entries.[PayPeriod] = ? AND Users.[FullName] = ? GROUP BY [WorkDate], [Client], [Notes] ORDER BY [WorkDate] ASC", payperiod_selected, user_selected)
	rows = cur.fetchall()
	return rows

def unsubmitted_timesheet_list():
	cur = conn.cursor()
	cur.execute("SELECT u.[FullName], te.[PayPeriod] FROM TimeEntryDB.dbo.Users u LEFT JOIN TimeEntryDB.dbo.Timesheet_Entries te ON u.[OS_Username] = te.[Username] WHERE te.[Status] = 'Not Submitted' AND u.[OS_Username] = te.[Username] Group BY u.[FullName], te.[PayPeriod]")
	rows = cur.fetchall()
	return rows