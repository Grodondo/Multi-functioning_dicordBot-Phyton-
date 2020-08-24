import mysql.connector
import pw


def add_userscore_tournament():
    mydb = connectToDB()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT COUNT(*) FROM `pingpong`.`tournaments`;")
    tournamentnumber = str(mycursor.fetchone()[0])

    mycursor.execute("\
        ALTER TABLE `pingpong`.`userscores` \
        ADD COLUMN t" + tournamentnumber + "team  VARCHAR(45) NULL AFTER `userid`,\
        ADD COLUMN t" + tournamentnumber + "wins INT ZEROFILL NULL AFTER `t" + tournamentnumber + "team`,\
        ADD COLUMN t" + tournamentnumber + "kills INT ZEROFILL NULL AFTER `t" + tournamentnumber + "wins`,\
        ADD COLUMN t" + tournamentnumber + "deaths INT ZEROFILL NULL AFTER `t" + tournamentnumber + "kills`,\
        ADD COLUMN t" + tournamentnumber + "placement INT ZEROFILL NULL AFTER `t" + tournamentnumber + "deaths`,\
        ADD COLUMN t" + tournamentnumber + "score INT ZEROFILL NULL AFTER `t" + tournamentnumber + "placement`,\
        ADD COLUMN t" + tournamentnumber + "participates TINYINT NULL AFTER `t" + tournamentnumber + "score`,\
        ADD COLUMN t" + tournamentnumber + "disqualified TINYINT NULL AFTER `t" + tournamentnumber + "participates`;\
    ")
    mycursor.close()
    mydb.close()


def add_tournament_tournament(date, time ,gamemap, gametype, speed, comment):
    mydb = connectToDB()
    mycursor = mydb.cursor()

    mycursor.execute(
        "INSERT INTO `pingpong`.`tournaments` (tdate,ttime, tmap, ttype, tcomment, tspeed) " +
        "VALUES ('" + date + "','" + time + "','" + gamemap + "','" + gametype + "','" + speed + "','" + comment + "');"
    )
    mycursor.close()
    mydb.commit()
    mydb.close()

def add_participate(dctag):
    mydb = connectToDB()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT COUNT(*) FROM `pingpong`.`tournaments`;")
    number = str(mycursor.fetchone()[0])

    mycursor.execute("Select idusers From `pingpong`.`users` Where discordtag='"+dctag+"'")
    userid = str(mycursor.fetchone()[0])

    #TODO add time constraints

    mycursor.execute("UPDATE `pingpong`.`userscores` SET t" + number + "participates" +
                     "=True Where userid= " + userid + ";")
    mycursor.close()
    mydb.commit()
    mydb.close()

def getScoreboard():
    mydb = connectToDB()


def add_register(battletag, dctag, name, nickname):
    mydb = connectToDB()
    mycursor = mydb.cursor()

    if (not nickname):
        nickname = name

    data_register = {
        'bt': battletag,
        'dt': dctag,
        'n': name,
        'nn': nickname
    }

    data_reg2 = {
        'disc': dctag,
    }

    mycursor.execute("INSERT INTO `pingpong`.`users` (battletag, discordtag, name, nickname) " +
                     "VALUES (%(bt)s,%(dt)s,%(n)s,%(nn)s);", data_register)

    mycursor.execute("Select idusers From `pingpong`.`users` Where discordtag = %(disc)s", data_reg2)

    userid = str(mycursor.fetchone()[0])

    mycursor.execute("INSERT INTO `pingpong`.`userscores` (userid)" +
                         "VALUES ('" + userid + "');")

    mycursor.close()
    mydb.commit()
    mydb.close()

def connectToDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=pw.get_db_password()
    )
    return mydb

# add_tournament_tournament("14/07/2020","roundboy","1v1","80")
# add_userscore_tournament()
