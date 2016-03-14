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
    cursor_1.execute('''
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

    cursor_2 = conn.cursor()
    cursor_2.execute('''
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


def jcafb_2016_export_3(client, file_path, db_path, code_1, code_2, code_3):

    table_name = 'question_user_input_line_values' + '_' + code_1 + '_' + code_2
    table_name_1 = 'question_user_input_line_values' + '_' + code_1
    table_name_2 = 'question_user_input_line_values' + '_' + code_2
    table_name_3 = 'question_user_input_line_values' + '_' + code_3

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
            value_text_2 TEXT,
            question_3 TEXT,
            question_type_3 TEXT,
            value_suggested_3 TEXT,
            value_text_3 TEXT
            );
    ''')

    cursor_1 = conn.cursor()
    cursor_1.execute('''
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

    cursor_2 = conn.cursor()
    cursor_2.execute('''
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

    cursor_3 = conn.cursor()
    cursor_3.execute('''
        SELECT * FROM ''' + table_name_3 + ''';
    ''')

    all_rows = cursor_3.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_3 = cursor.fetchone()
        if row_3 is not None:
            id_3 = row_3[0]
            print('>>>>>', row_3, id_3)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_3 = ? WHERE id = ? ''',
                           (question, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_3 = ? WHERE id = ? ''',
                           (question_type, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_3 = ? WHERE id = ? ''',
                           (value_suggested, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_3 = ? WHERE id = ? ''',
                           (value_text, id_3))
        else:
            print('>>>>>', row_3)
            cursor.execute('''
                           INSERT INTO ''' + table_name + '''(
                               patient_code,
                               family_code,
                               question_3,
                               question_type_3,
                               value_suggested_3,
                               value_text_3
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


def jcafb_2016_export_4(client, file_path, db_path, code_1, code_2, code_3, code_4):

    table_name = 'question_user_input_line_values' + '_' + code_1 + '_' + code_2
    table_name_1 = 'question_user_input_line_values' + '_' + code_1
    table_name_2 = 'question_user_input_line_values' + '_' + code_2
    table_name_3 = 'question_user_input_line_values' + '_' + code_3
    table_name_4 = 'question_user_input_line_values' + '_' + code_4

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
            value_text_2 TEXT,
            question_3 TEXT,
            question_type_3 TEXT,
            value_suggested_3 TEXT,
            value_text_3 TEXT,
            question_4 TEXT,
            question_type_4 TEXT,
            value_suggested_4 TEXT,
            value_text_4 TEXT
            );
    ''')

    cursor_1 = conn.cursor()
    cursor_1.execute('''
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

    cursor_2 = conn.cursor()
    cursor_2.execute('''
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
            cursor.execute('''SELECT id, family_code FROM ''' + table_name + ''' WHERE family_code=?''',
                           (family_code,))
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

    cursor_3 = conn.cursor()
    cursor_3.execute('''
        SELECT * FROM ''' + table_name_3 + ''';
    ''')

    all_rows = cursor_3.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_3 = cursor.fetchone()
        if row_3 is not None:
            id_3 = row_3[0]
            print('>>>>>', row_3, id_3)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_3 = ? WHERE id = ? ''',
                           (question, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_3 = ? WHERE id = ? ''',
                           (question_type, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_3 = ? WHERE id = ? ''',
                           (value_suggested, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_3 = ? WHERE id = ? ''',
                           (value_text, id_3))
        else:
            cursor.execute('''SELECT id, family_code FROM ''' + table_name + ''' WHERE family_code=?''',
                           (family_code,))
            row_3 = cursor.fetchone()
            if row_3 is not None:
                id_3 = row_3[0]
                print('>>>>>', row_3, id_3)
                cursor.execute('''UPDATE ''' + table_name + ''' SET question_3 = ? WHERE id = ? ''',
                               (question, id_3))
                cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_3 = ? WHERE id = ? ''',
                               (question_type, id_3))
                cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_3 = ? WHERE id = ? ''',
                               (value_suggested, id_3))
                cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_3 = ? WHERE id = ? ''',
                               (value_text, id_3))
            else:
                print('>>>>>', row_3)
                cursor.execute('''
                               INSERT INTO ''' + table_name + '''(
                                   patient_code,
                                   family_code,
                                   question_3,
                                   question_type_3,
                                   value_suggested_3,
                                   value_text_3
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

    cursor_4 = conn.cursor()
    cursor_4.execute('''
        SELECT * FROM ''' + table_name_4 + ''';
    ''')

    all_rows = cursor_4.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_4 = cursor.fetchone()
        if row_4 is not None:
            id_4 = row_4[0]
            print('>>>>>', row_4, id_4)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_4 = ? WHERE id = ? ''',
                           (question, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_4 = ? WHERE id = ? ''',
                           (question_type, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_4 = ? WHERE id = ? ''',
                           (value_suggested, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_4 = ? WHERE id = ? ''',
                           (value_text, id_4))
        else:
            cursor.execute('''SELECT id, family_code FROM ''' + table_name + ''' WHERE family_code=?''',
                           (family_code,))
            row_4 = cursor.fetchone()
            if row_4 is not None:
                id_4 = row_4[0]
                print('>>>>>', row_4, id_4)
                cursor.execute('''UPDATE ''' + table_name + ''' SET question_4 = ? WHERE id = ? ''',
                               (question, id_4))
                cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_4 = ? WHERE id = ? ''',
                               (question_type, id_4))
                cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_4 = ? WHERE id = ? ''',
                               (value_suggested, id_4))
                cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_4 = ? WHERE id = ? ''',
                               (value_text, id_4))
            else:
                print('>>>>>', row_4)
                cursor.execute('''
                               INSERT INTO ''' + table_name + '''(
                                   patient_code,
                                   family_code,
                                   question_4,
                                   question_type_4,
                                   value_suggested_4,
                                   value_text_4
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


def jcafb_2016_export_5(client, file_path, db_path, code_1, code_2, code_3, code_4, code_5):

    table_name = 'question_user_input_line_values' + '_' + code_1 + '_' + code_2
    table_name_1 = 'question_user_input_line_values' + '_' + code_1
    table_name_2 = 'question_user_input_line_values' + '_' + code_2
    table_name_3 = 'question_user_input_line_values' + '_' + code_3
    table_name_4 = 'question_user_input_line_values' + '_' + code_4
    table_name_5 = 'question_user_input_line_values' + '_' + code_5

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
            value_text_2 TEXT,
            question_3 TEXT,
            question_type_3 TEXT,
            value_suggested_3 TEXT,
            value_text_3 TEXT,
            question_4 TEXT,
            question_type_4 TEXT,
            value_suggested_4 TEXT,
            value_text_4 TEXT,
            question_5 TEXT,
            question_type_5 TEXT,
            value_suggested_5 TEXT,
            value_text_5 TEXT
            );
    ''')

    cursor_1 = conn.cursor()
    cursor_1.execute('''
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

    cursor_2 = conn.cursor()
    cursor_2.execute('''
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

    cursor_3 = conn.cursor()
    cursor_3.execute('''
        SELECT * FROM ''' + table_name_3 + ''';
    ''')

    all_rows = cursor_3.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_3 = cursor.fetchone()
        if row_3 is not None:
            id_3 = row_3[0]
            print('>>>>>', row_3, id_3)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_3 = ? WHERE id = ? ''',
                           (question, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_3 = ? WHERE id = ? ''',
                           (question_type, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_3 = ? WHERE id = ? ''',
                           (value_suggested, id_3))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_3 = ? WHERE id = ? ''',
                           (value_text, id_3))
        else:
            print('>>>>>', row_3)
            cursor.execute('''
                           INSERT INTO ''' + table_name + '''(
                               patient_code,
                               family_code,
                               question_3,
                               question_type_3,
                               value_suggested_3,
                               value_text_3
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

    cursor_4 = conn.cursor()
    cursor_4.execute('''
        SELECT * FROM ''' + table_name_4 + ''';
    ''')

    all_rows = cursor_4.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_4 = cursor.fetchone()
        if row_4 is not None:
            id_4 = row_4[0]
            print('>>>>>', row_4, id_4)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_4 = ? WHERE id = ? ''',
                           (question, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_4 = ? WHERE id = ? ''',
                           (question_type, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_4 = ? WHERE id = ? ''',
                           (value_suggested, id_4))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_4 = ? WHERE id = ? ''',
                           (value_text, id_4))
        else:
            print('>>>>>', row_4)
            cursor.execute('''
                           INSERT INTO ''' + table_name + '''(
                               patient_code,
                               family_code,
                               question_4,
                               question_type_4,
                               value_suggested_4,
                               value_text_4
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

    cursor_5 = conn.cursor()
    cursor_5.execute('''
        SELECT * FROM ''' + table_name_5 + ''';
    ''')

    all_rows = cursor_5.fetchall()
    for row in all_rows:
        patient_code = row[1]
        family_code = row[2]
        question = row[3]
        question_type = row[4]
        value_suggested = row[5]
        value_text = row[6]

        cursor.execute('''SELECT id, patient_code FROM ''' + table_name + ''' WHERE patient_code=?''', (patient_code,))
        row_5 = cursor.fetchone()
        if row_5 is not None:
            id_5 = row_5[0]
            print('>>>>>', row_5, id_5)
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_5 = ? WHERE id = ? ''',
                           (question, id_5))
            cursor.execute('''UPDATE ''' + table_name + ''' SET question_type_5 = ? WHERE id = ? ''',
                           (question_type, id_5))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_suggested_5 = ? WHERE id = ? ''',
                           (value_suggested, id_5))
            cursor.execute('''UPDATE ''' + table_name + ''' SET value_text_5 = ? WHERE id = ? ''',
                           (value_text, id_5))
        else:
            print('>>>>>', row_4)
            cursor.execute('''
                           INSERT INTO ''' + table_name + '''(
                               patient_code,
                               family_code,
                               question_5,
                               question_type_5,
                               value_suggested_5,
                               value_text_5
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
    # code = 'CSE16_03_03'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'CSE16_03_04'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_05_01'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_05_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_05_03'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_05_04'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

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

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QAN16_04_05'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QAN16_05_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_03_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

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

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_03'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_06'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_08_03'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_08_06'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_08_08'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_08_11'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_10_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_10_03'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_10_06'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QMD16_03_02'
    # print('-->', client, db_path, code)
    # print('--> survey_question_user_input_line_values_sqlite()...')
    # survey_question_user_input_line_values_sqlite(client, db_path, code)

    # #######################################

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_02_QDH16_03_02_QDH16_06_03.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_03_02'
    # code_2 = 'QDH16_06_03'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_03_QDH16_06_03_QDH16_08_06_QDH16_08_11.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_06_03'
    # code_2 = 'QDH16_08_06'
    # code_3 = 'QDH16_10_12'
    # print('-->', client, file_path, db_path, code_1, code_2, code_3)
    # print('--> jcafb_2016_export_3()...')
    # jcafb_2016_export_3(client, file_path, db_path, code_1, code_2, code_3)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_04_QDH16_06_03_QDH16_08_03.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_06_03'
    # code_2 = 'QDH16_08_03'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_05_QDH16_06_03_QDH16_08_03.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_06_03'
    # code_2 = 'QDH16_08_03'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_06_QDH16_05_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_05_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_07_QDH16_05_05_QDH16_08_08.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_05_05'
    # code_2 = 'QDH16_08_08'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_08_QDH16_04_10.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_10'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_09_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_12_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_13_QDH16_10_02_QDH16_10_03_QDH16_05_05_QDH16_06_03_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_10_02'
    # code_2 = 'QDH16_10_03'
    # code_3 = 'QDH16_05_05'
    # code_4 = 'QDH16_06_03'
    # code_5 = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code_1, code_2, code_3, code_4, code_5)
    # print('--> jcafb_2016_export_5()...')
    # jcafb_2016_export_5(client, file_path, db_path, code_1, code_2, code_3, code_4, code_5)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_14_QDH16_10_06_QDH16_05_05_QDH16_06_03_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_10_06'
    # code_2 = 'QDH16_05_05'
    # code_3 = 'QDH16_06_03'
    # code_4 = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code_1, code_2, code_3, code_4)
    # print('--> jcafb_2016_export_4()...')
    # jcafb_2016_export_4(client, file_path, db_path, code_1, code_2, code_3, code_4)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_15_QDH16_05_05_QDH16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QDH16_05_05'
    # code_2 = 'QDH16_06_06'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_16_QDH16_04_07.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QDH16_04_07'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_17_QAN16_04_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QAN16_04_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_18_QAN16_04_05_QAN16_05_02.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'QAN16_04_05'
    # code_2 = 'QAN16_05_02'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_19_QAN16_04_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QAN16_04_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_20_FSE16_06_06.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_06_06'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_21_FSE16_05_01_FSE16_05_02_FSE16_05_03_FSE16_05_04.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'FSE16_05_01'
    # code_2 = 'FSE16_05_02'
    # code_3 = 'FSE16_05_03'
    # code_4 = 'FSE16_05_04'
    # print('-->', client, file_path, db_path, code_1, code_2, code_3, code_4)
    # print('--> jcafb_2016_export_4()...')
    # jcafb_2016_export_4(client, file_path, db_path, code_1, code_2, code_3, code_4)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_22_FSE16_08_01.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_08_01'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_23_FSE16_08_01.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'FSE16_08_01'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_25_QAN16_04_05.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code = 'QAN16_04_05'
    # print('-->', client, file_path, db_path, code)
    # print('--> jcafb_2016_export()...')
    # jcafb_2016_export(client, file_path, db_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_27_CSE16_03_03_CSE16_03_04.csv'
    # db_path = '/opt/openerp/jcafb/data/jcafb_2016.sqlite'
    # code_1 = 'CSE16_03_03'
    # code_2 = 'CSE16_03_04'
    # print('-->', client, file_path, db_path, code_1, code_2)
    # print('--> jcafb_2016_export_2()...')
    # jcafb_2016_export_2(client, file_path, db_path, code_1, code_2)

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
