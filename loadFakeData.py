import psycopg2
import csv
import datetime

if __name__=="__main__":
	conn = psycopg2.connect("host=localhost dbname=heartagain user=rpi_user password=rpi_user")
	cur = conn.cursor()
	with open('file1.csv') as file:
		reader = csv.reader(file)
		numbers_list = next(reader)
		for number in numbers_list:
			values_list = []
			values_list.append('testid')
			values_list.append(datetime.datetime.now())
			values_list.append(number)

			query = 'insert into ecg_data(user_id, date, ecg_value) VALUES(%s, %s, %s);'
			cur.execute(query, values_list)
			conn.commit()
	conn.close()
