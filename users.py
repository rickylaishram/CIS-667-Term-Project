import database

# Register user
def add_user(name):
	d = database.Database()
	d.open()
	d.store_user(name)
	d.close()

def print_all_users():
	d = database.Database()
	d.open()
	users = d.fetch_all_users()
	d.close()
	print users

def main():
	#add_user('ricky')
	print_all_users()

if __name__ == '__main__':
	main()