import mysql.connector
import pw

def add_userscore_tournament():
    mydb = connectToDB()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT COUNT(*) FROM `pingpong`.`tournaments`;")
    tournamentnumber =str(mycursor.fetchone()[0])

    mycursor.execute("\
        ALTER TABLE `pingpong`.`userscores` \
        ADD COLUMN t" + tournamentnumber + "team  VARCHAR(45) NULL AFTER `userid`,\
        ADD COLUMN t" + tournamentnumber + "participated TINYINT NULL AFTER `t" + tournamentnumber + "team`,\
        ADD COLUMN t" + tournamentnumber + "wins INT ZEROFILL NULL AFTER `t" + tournamentnumber + "participated`,\
        ADD COLUMN t" + tournamentnumber + "kills INT ZEROFILL NULL AFTER `t" + tournamentnumber + "wins`,\
        ADD COLUMN t" + tournamentnumber + "deaths INT ZEROFILL NULL AFTER `t" + tournamentnumber + "kills`,\
        ADD COLUMN t" + tournamentnumber + "placement INT ZEROFILL NULL AFTER `t" + tournamentnumber + "deaths`,\
        ADD COLUMN t" + tournamentnumber + "score INT ZEROFILL NULL AFTER `t" + tournamentnumber + "placement`;\
    ")
    mycursor.close()
    mydb.close()


def add_tournament_tournament(date, gamemap, gametype, speed, comment="no comment"):
    mydb = connectToDB()
    mycursor = mydb.cursor()

    mycursor.execute(
        "INSERT INTO `pingpong`.`tournaments` (tdate, tmap, ttype, tcomment, tspeed) "+
        "VALUES ('" + date + "','" + gamemap + "','" + gametype + "','" + speed + "','" + comment + "');"
    )
    mycursor.close()
    mydb.commit()
    mydb.close()

def getScoreboard():
    mydb = connectToDB()


def connectToDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=pw.get_db_password()
    )
    return mydb


#add_tournament_tournament("14/07/2020","roundboy","1v1","80")
#add_userscore_tournament()

