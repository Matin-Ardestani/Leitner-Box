import sqlite3
from pathlib import Path

# connect to database
connection = sqlite3.connect('%s/src/words.db' % str(Path.cwd()))
cursor = connection.cursor()

# -Tables-
# box 1 | 2 | 3 | 4 | 5 | out( word VARCHAR(100) , meaning VARCHAR(100) )

# insert or change
while True:
    start = str(input('Do you want to insert a new item?(y/n) '))
    if start == 'y':
        insert = True
        insert_word = str(input('What is your new word? '))
        insert_meaning = str(input('What does \'%s\' mean? ' % insert_word))

        # add new word to db
        quary = 'INSERT INTO box1 VALUES ( \'%s\' , \'%s\' );' % (insert_word , insert_meaning)
        cursor.execute(quary)
        connection.commit()

    elif start == 'n':
        insert = False
        break



# choose box
current_box = 0
while (current_box > 5) or (current_box < 1):
    current_box = int(input('\nSelect your box (1,2,3,4,5) : '))


# show words
cursor.execute('SELECT * FROM box%s;' % current_box)

words_list = []
for i in cursor:
    words_list.append(i)

for item in words_list:
    word , meaning = item[0] , item[1]


    print('\n%s => %s' % (word , meaning))
    answer = str(input('Did you know that? '))
    if answer == 'y':

        # insert word to the next box
        if current_box != 5:
            quary = 'INSERT INTO box%s VALUES( \'%s\' , \'%s\' );' % (current_box+1 , word , meaning)
            cursor.execute(quary) # insert to the next box

            quary = 'DELETE FROM box%s WHERE word=\'%s\' ;' % (current_box , word)
            cursor.execute(quary) # delete from former box
        else:
            quary = 'INSERT INTO out VALUES( \'%s\' , \'%s\' );' % (word , meaning)
            cursor.execute(quary) # insert to the out box

            quary = 'DELETE FROM box%s WHERE word=\'%s\' ;' % (current_box , word)
            cursor.execute(quary) # delete from former box

            print('You have learned this word perfectly!')

        connection.commit()

    elif answer == 'n':
        # insert word to the next box
        if current_box != 1:
            quary = 'INSERT INTO box%s VALUES( \'%s\' , \'%s\' );' % (current_box-1 , word , meaning)
            cursor.execute(quary) # insert to the next box

            quary = 'DELETE FROM box%s WHERE word=\'%s\' ;' % (current_box , word)
            cursor.execute(quary) # delete from former box

            connection.commit()
