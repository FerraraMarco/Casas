import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from function import rem, chg

name_db = ""
username_db = "postgres"
password_db = ""
host_db = "127.0.0.1"
port_db = "5432"

connection = psycopg2.connect(user=username_db, password=password_db, database=name_db, host=host_db, port=port_db)
cursor = connection.cursor()
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

queryId = "select id from activity.activity order by(id)"
queryS = "select startdate from activity.activity order by(id)"
queryE = "select enddate from activity.activity order by(id)"
remSD = "ALTER TABLE activity.activity DROP COLUMN if exists date"
queryStart = "ALTER TABLE activity.activity ADD COLUMN date date"
remD = "ALTER TABLE activity.activity DROP COLUMN if exists duration"
duration = "ALTER TABLE activity.activity ADD COLUMN duration int"
queryIdS = "select id from activity.event where event.id >= 8873149 order by(event.id)"
queryDate = "select date from activity.event where event.id >= 8873149 order by(event.id)"
remOD = "ALTER TABLE activity.event DROP COLUMN if exists onlyDate"
queryOD = "ALTER TABLE activity.event ADD COLUMN onlyDate date"

cursor.execute(remSD)
cursor.execute(remD)
cursor.execute(remOD)

cursor.execute(queryId)
colId = cursor.fetchall()
cursor.execute(queryS)
colS = cursor.fetchall()
cursor.execute(queryE)
colE = cursor.fetchall()
cursor.execute(queryStart)
cursor.execute(duration)
cursor.execute(queryOD)
cursor.execute(queryIdS)
colIdS = cursor.fetchall()
cursor.execute(queryDate)
colDate = cursor.fetchall()


for i in range(len(colId)):
    queryUP = "update activity.activity set date = '" + str(chg(colS[i]).date()) + \
              "' where id ='" + rem(str(colId[i])) + "'"
    cursor.execute(queryUP)

for i in range(len(colId)):
    start = chg(colS[i])
    end = chg(colE[i])
    deltaSec = (end - start).microseconds
    queryUP = "update activity.activity set duration = '" + str(deltaSec) + "' where id ='" + \
              rem(str(colId[i])) + "'"
    cursor.execute(queryUP)

for i in range(len(colIdS)):
    queryUP = "update activity.event set onlyDate = '" + str(chg(colDate[i]).date()) + \
              "' where id ='" + rem(str(colIdS[i])) + "'"
    cursor.execute(queryUP)
