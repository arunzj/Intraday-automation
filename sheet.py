import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def create_connection():
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creads=ServiceAccountCredentials.from_json_keyfile_name("GoogleSheet1-d5e055b7a2b3.json",scope)
	client= gspread.authorize(creads)
	return client

def get_sheet(client,workbook):
	sheet = client.open("FinTracker")
	return sheet

def get_worksheet(name):
	
	client=create_connection()
	spread_sheet=get_sheet(client,'FinTracker')

	worksheet=spread_sheet.worksheet(name)
	return worksheet
	# record_lst=intra_sheet.get_all_records()
	# pprint(len(record_lst))
	# #pprint(sheet.get_all_records())