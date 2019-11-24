import mysql.connector
from organisor import Tutor, Tutee, match

cnx = mysql.connector.connect(
    user='root', password='KtvGEJmNHsvo7mJl',
    host='35.242.131.39', database='orangeCat'
)
cursor = cnx.cursor()

def create_matchings(cnx, cursor):

    tutor_list = []

    cursor.execute("select tutor_id from tutor")

    for t in [i for i in cursor.fetchall()]:
        cursor.execute("select subject_id from tutor_subject where tutor_id=%s", (t))
        subjects_list = [i for i in cursor.fetchall()]
        cursor.execute("select time_id from tutor_time where tutor_id=%s", (t))
        times_list = [i for i in cursor.fetchall()]
        tutor_list.append(Tutor(t, subjects_list, [0 for j in range(len(subjects_list))], times_list))
    
    tutee_list = []

    cursor.execute("select tutee_id from tutee")

    for t in [i for i in cursor.fetchall()]:
        cursor.execute("select time_id from tutee_time where tutee_id=%s", (t))
        times_list = [i for i in cursor.fetchall()]
        subjects_list = [None, None]
        cursor.execute("select first_subject from tutee where tutee_id=%s", (t))
        subjects_list[0] = [i for i in cursor.fetchall()][0]
        cursor.execute("select second_subject from tutee where tutee_id=%s", (t))
        subjects_list[1] = [i for i in cursor.fetchall()][0]
        tutee_list.append(Tutee(t, subjects_list, times_list))
    
    return match(tutor_list, tutee_list)

if __name__=='__main__':
    cnx = mysql.connector.connect(
        user='root', password='KtvGEJmNHsvo7mJl',
        host='35.242.131.39', database='orangeCat'
    )
    cursor = cnx.cursor()
    matchings = create_matchings(cnx, cursor)
    for m in matchings:
        cursor.execute("insert into tutor_tutee values (%s, %s, %s, %s)",
            (m[0].oid[0], m[1].oid[0], m[2][0], m[3][0]))
    cnx.commit()
    cursor.close()
    cnx.close()