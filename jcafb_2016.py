#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol                 #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from __future__ import print_function

from erppeek import *

from base import *
import argparse
import getpass

import sqlite3
import csv


def ir_model_data_get_instance(client, code):

    ir_model_data = client.model('ir.model.data')
    ir_model_data_browse = ir_model_data.browse([('name', '=', code), ])

    if ir_model_data_browse.name != []:
        instance = ir_model_data_browse.name[0], ir_model_data_browse.model[0], ir_model_data_browse.res_id[0]
        return instance
    else:
        instance = False, False, False
        return instance


def survey_question_user_input_line_values_sqlite(client, db_path, code):

    table_name = 'question_user_input_line_values' + '_' + code

    # conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            patient_code,
            family_code TEXT,
            question TEXT,
            question_type TEXT,
            value_suggested TEXT,
            value_text TEXT
            );
    ''')

    instance = ir_model_data_get_instance(client, code)
    print('------>', instance)
    print()

    survey_question = client.model('survey.question')
    survey_question_browse = survey_question.browse([
        ('id', '=', instance[2]),
        ])

    question = survey_question_browse[0].question.encode('utf-8')
    question_type = survey_question_browse[0].type

    survey_user_input_line = client.model('survey.user_input_line')
    survey_user_input_line_browse = survey_user_input_line.browse([
        ('question_id', '=', instance[2]),
        ])

    survey_user_input = client.model('survey.user_input')
    survey_user_input_browse = survey_user_input.browse([
        ('survey_id', '=', survey_question_browse[0].survey_id.id),
        ])

    clv_document = client.model('clv_document')

    if question_type == 'simple_choice':

        i = 0
        for user_input_line in survey_user_input_line_browse:

            if user_input_line.answer_type == 'suggestion':

                i += 1

                clv_document_browse = clv_document.browse([
                    ('survey_user_input_id', '=', user_input_line.user_input_id.id),
                    ])

                patient_code = False
                if clv_document_browse.patient_id.id != []:
                    patient_code = clv_document_browse.patient_id.patient_code[0]
                if patient_code is False:
                    patient_code = None

                family_code = False
                if clv_document_browse.family_id.id != []:
                    family_code = clv_document_browse.family_id.code[0]
                if family_code is False:
                    family_code = None

                value_suggested = False
                if user_input_line.value_suggested is not False:
                    value_suggested = user_input_line.value_suggested.value.encode('utf-8')
                if value_suggested is False:
                    value_suggested = None

                survey_user_input_line_2_browse = survey_user_input_line.browse([
                    ('user_input_id', '=', user_input_line.user_input_id.id),
                    ('question_id', '=', instance[2]),
                    ('answer_type', '=', 'text'),
                    ])

                value_text = False
                if survey_user_input_line_2_browse.id != []:
                    if survey_user_input_line_2_browse[0].value_text is not False:
                        value_text = survey_user_input_line_2_browse[0].value_text.encode('utf-8')
                if value_text is False:
                    value_text = None

                print(i,
                      patient_code,
                      family_code,
                      question,
                      question_type,
                      value_suggested,
                      value_text,
                      )

                cursor.execute('''
                               INSERT INTO ''' + table_name + '''(
                                   patient_code,
                                   family_code,
                                   question,
                                   question_type,
                                   value_suggested,
                                   value_text
                                   )
                               VALUES(?,?,?,?,?,?)''',
                               (patient_code,
                                family_code,
                                question,
                                question_type,
                                value_suggested,
                                value_text
                                )
                               )

    if question_type == 'multiple_choice':

        i = 0
        for user_input in survey_user_input_browse:

            i += 1
            first_user_input_line = True

            survey_user_input_line_3_browse = survey_user_input_line.browse([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', instance[2]),
                ])

            for user_input_line_3 in survey_user_input_line_3_browse:

                if user_input_line_3.answer_type == 'suggestion':

                    if first_user_input_line is True:

                        clv_document_browse = clv_document.browse([
                            ('survey_user_input_id', '=', user_input_line_3.user_input_id.id),
                            ])

                        patient_code = False
                        if clv_document_browse.patient_id.id != []:
                            patient_code = clv_document_browse.patient_id.patient_code[0]
                        if patient_code is False:
                            patient_code = None

                        family_code = False
                        if clv_document_browse.family_id.id != []:
                            family_code = clv_document_browse.family_id.code[0]
                        if family_code is False:
                            family_code = None

                        value_suggested_2 = False
                        if user_input_line_3.value_suggested is not False:
                            value_suggested_2 = user_input_line_3.value_suggested.value.encode('utf-8')
                        value_suggested = value_suggested_2
                        if value_suggested is False:
                            value_suggested = None

                        first_user_input_line = False

                    else:

                        value_suggested_2 = False
                        if user_input_line_3.value_suggested is not False:
                            value_suggested_2 = user_input_line_3.value_suggested.value.encode('utf-8')
                        value_suggested = value_suggested + ';' + value_suggested_2

                survey_user_input_line_2_browse = survey_user_input_line.browse([
                    ('user_input_id', '=', user_input.id),
                    ('question_id', '=', instance[2]),
                    ('answer_type', '=', 'text'),
                    ])

                value_text = False
                if survey_user_input_line_2_browse.id != []:
                    if survey_user_input_line_2_browse[0].value_text is not False:
                        value_text = survey_user_input_line_2_browse[0].value_text.encode('utf-8')
                if value_text is False:
                    value_text = None

                print(i,
                      patient_code,
                      family_code,
                      question,
                      question_type,
                      value_suggested,
                      value_text,
                      )

                cursor.execute('''
                               INSERT INTO ''' + table_name + '''(
                                   patient_code,
                                   family_code,
                                   question,
                                   question_type,
                                   value_suggested,
                                   value_text
                                   )
                               VALUES(?,?,?,?,?,?)''',
                               (patient_code,
                                family_code,
                                question,
                                question_type,
                                value_suggested,
                                value_text
                                )
                               )

    data = cursor.execute('''
        SELECT * FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        print(row)

    conn.commit()
    conn.close()

    print()
    print('--> i: ', i)


def jcafb_2016_export(client, file_path, db_path, code):

    table_name = 'question_user_input_line_values' + '_' + code

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()

    data = cursor.execute('''
        SELECT * FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        print(row)

    data = cursor.execute('''
        SELECT * FROM ''' + table_name + ''';
    ''')

    csv_file = open(file_path, 'wb')
    writer_csv_file = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_csv_file.writerow([field[0] for field in cursor.description])

    writer_csv_file.writerows(data)

    csv_file.close()
    conn.close()


def jcafb_2016_export_2(client, file_path, db_path, code_1, code_2):

    table_name = 'question_user_input_line_values' + '_' + code_1 + '_' + code_2
    table_name_1 = 'question_user_input_line_values' + '_' + code_1
    table_name_2 = 'question_user_input_line_values' + '_' + code_2

    conn = sqlite3.connect(db_path)
    conn.text_factory = str

    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE ''' + table_name + ''';''')
    except Exception as e:
        print('------->', e)
    cursor.execute('''
        CREATE TABLE ''' + table_name + ''' (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            patient_code,
            family_code TEXT,
            question_1 TEXT,
            question_type_1 TEXT,
            value_suggested_1 TEXT,
            value_text_1 TEXT,
            question_2 TEXT,
            question_type_2 TEXT,
            value_suggested_2 TEXT,
            value_text_2 TEXT
            );
    ''')

    cursor_1 = conn.cursor()

    data_1 = cursor_1.execute('''
        SELECT * FROM ''' + table_name_1 + ''';
    ''')

    print(data_1)
    print([field[0] for field in cursor_1.description])
    for row in cursor_1:
        print(row)

    cursor_2 = conn.cursor()

    data_2 = cursor_2.execute('''
        SELECT * FROM ''' + table_name_2 + ''';
    ''')

    print(data_2)
    print([field[0] for field in cursor_2.description])
    for row in cursor_2:
        print(row)

    data_1 = cursor_1.execute('''
        SELECT * FROM ''' + table_name_1 + ''';
    ''')

    all_rows = cursor_1.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''
                       INSERT INTO ''' + table_name + '''(
                           patient_code,
                           family_code,
                           question_1,
                           question_type_1,
                           value_suggested_1,
                           value_text_1
                           )
                       VALUES(?,?,?,?,?,?)''',
                       (patient_code,
                        family_code,
                        question,
                        question_type,
                        value_suggested,
                        value_text
                        )
                       )

    conn.commit()

    data_2 = cursor_2.execute('''
        SELECT * FROM ''' + table_name_2 + ''';
    ''')

    all_rows = cursor_2.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_2 = cursor.fetchone()
        if row_2 is not None:
            id_2 = row_2[0]
            print('>>>>>', row_2, id_2)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_2 = ? WHERE id = ? ''',
                           (question, id_2))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_2 = ? WHERE id = ? ''',
                           (question_type, id_2))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_2 = ? WHERE id = ? ''',
                           (value_suggested, id_2))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_2 = ? WHERE id = ? ''',
                           (value_text, id_2))
        else:
            print('>>>>>', row_2)
            cursor.execute('''
                           INSERT INTO ''' + table_name + '''(
                               patient_code,
                               family_code,
                               question_2,
                               question_type_2,
                               value_suggested_2,
                               value_text_2
                               )
                           VALUES(?,?,?,?,?,?)''',
                           (patient_code,
                            family_code,
                            question,
                            question_type,
                            value_suggested,
                            value_text
                            )
                           )

    conn.commit()

    data = cursor.execute('''
        SELECT * FROM ''' + table_name + ''';
    ''')

    print(data)
    print([field[0] for field in cursor.description])
    for row in cursor:
        print(row)

    data = cursor.execute('''
        SELECT * FROM ''' + table_name + ''';
    ''')

    csv_file = open(file_path, 'wb')
    writer_csv_file = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_csv_file.writerow([field[0] for field in cursor.description])

    writer_csv_file.writerows(data)

    csv_file.close()
    conn.close()


def get_arguments():

    global username
    global password
    global dbname

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    args = parser.parse_args()
    print('%s%s' % ('--> ', args))

    if args.dbname is not None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

    if args.username is not None:
        username = args.username
    elif username == '*':
        username = raw_input('username: ')

    if args.password is not None:
        password = args.password
    elif password == '*':
        password = getpass.getpass('password: ')


if __name__ == '__main__':

    server = 'http://localhost:8069'

    # username = 'username'
    username = '*'
    # paswword = 'paswword'
    paswword = '*'

    dbname = 'odoo'
    # dbname = '*'

    print()
    get_arguments()

    from time import time
    start = time()

    print('--> survey.py...')

    client = erppeek.Client(server, dbname, username, password)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_06_06'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_07_04'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_07_05'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_08_01'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    code = 'QDH16_03_02'
    print('-->', client, db_path, code)
    print('--> survey_question_user_input_line_values_sqlite()...')
    survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_07'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_10'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_05_05'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    code = 'QDH16_06_03'
    print('-->', client, db_path, code)
    print('--> survey_question_user_input_line_values_sqlite()...')
    survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_06'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QMD16_03_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # #######################################

    file_path = '/opt/openerp/jcafb/data/jcafb_2016_02_QDH16_03_02_QDH16_06_03.csv'
    db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    code_1 = 'QDH16_03_02'
    code_2 = 'QDH16_06_03'
    print('-->', client, file_path, db_path, code_1, code_2)
    print('--> jcafb_2016_export()...')
    jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_08_QDH16_04_10.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_10'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_06_QDH16_05_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_05_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_09_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_16_QDH16_04_07.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_07'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_20_FSE16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_06_06'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_22_FSE16_08_01.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_08_01'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_28_QMD16_03_02.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QMD16_03_02'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_29_FSE16_07_04.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_07_04'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_30_FSE16_07_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_07_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # #######################################

    print()
    print('--> survey.py')
    print('--> Execution time:', secondsToStr(time() - start))
    print()
