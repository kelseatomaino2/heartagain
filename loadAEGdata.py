import psycopg2
import csv
import datetime

if __name__=="__main__":
	conn = psycopg2.connect("host=localhost dbname=heartagain user=rpi_user password=rpi_user")
	cur = conn.cursor()

	with open('AEG.csv') as file:
		reader = csv.reader(file)

		for row in reader:
			values_list = []
			values_list.append('testid2')
			values_list.append(datetime.datetime.now())
			values_list.append(row[1])
			query = 'insert into ecg_data(user_id, date_time, ecg_value) VALUES(%s, %s, %s);'
			cur.execute(query, values_list)
			conn.commit()
	conn.close()

