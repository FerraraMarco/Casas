from function import rem, chg, connection, exe

cursor = connection()

queryId = "select id from activity.activity order by(id)"
queryS = "select startdate from activity.activity order by(id)"
queryE = "select enddate from activity.activity order by(id)"
remSD = "ALTER TABLE activity.activity DROP COLUMN if exists date"
queryStart = "ALTER TABLE activity.activity ADD COLUMN date date"
remD = "ALTER TABLE activity.activity DROP COLUMN if exists duration"
duration = "ALTER TABLE activity.activity ADD COLUMN duration int"
queryIdE = "select id from activity.event order by(event.id)"
queryDate = "select date from activity.event order by(event.id)"
remOD = "ALTER TABLE activity.event DROP COLUMN if exists onlyDate"
queryOD = "ALTER TABLE activity.event ADD COLUMN onlyDate date"

# drop column
cursor.execute(remSD)
cursor.execute(remD)
cursor.execute(remOD)
# add new column
cursor.execute(queryStart)
cursor.execute(duration)
cursor.execute(queryOD)

colId = exe(cursor, queryId)
colS = exe(cursor, queryS)
colE = exe(cursor, queryE)
colIdE = exe(cursor, queryIdE)
colDate = exe(cursor, queryDate)


for i in range(len(colId)):
    queryUP = "update activity.activity set date = '" + str(chg(colS[i]).date()) + \
              "' where id ='" + rem(colId[i]) + "'"
    cursor.execute(queryUP)

for i in range(len(colId)):
    start = chg(colS[i])
    end = chg(colE[i])
    deltaSec = (end - start).microseconds
    queryUP = "update activity.activity set duration = '" + str(deltaSec) + "' where id ='" + \
              rem(colId[i]) + "'"
    cursor.execute(queryUP)

for i in range(len(colIdE)):
    queryUP = "update activity.event set onlyDate = '" + str(chg(colDate[i]).date()) + \
              "' where id ='" + rem(colIdE[i]) + "'"
    cursor.execute(queryUP)
