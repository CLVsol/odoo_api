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


def survey_question_user_input_line_values(client, file_path, code):

    headings_insured = ['no',
                        'patient_code',
                        'family_code',
                        'question',
                        'question_type',
                        'value_suggested',
                        'value_text',
                        ]
    csv_file = open(file_path, 'wb')
    writer_csv_file = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_csv_file.writerow(headings_insured)

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
                family_code = False
                if clv_document_browse.family_id.id != []:
                    family_code = clv_document_browse.family_id.code[0]

                value_suggested = False
                if user_input_line.value_suggested is not False:
                    value_suggested = user_input_line.value_suggested.value.encode('utf-8')

                survey_user_input_line_2_browse = survey_user_input_line.browse([
                    ('user_input_id', '=', user_input_line.user_input_id.id),
                    ('question_id', '=', instance[2]),
                    ('answer_type', '=', 'text'),
                    ])

                value_text = False
                if survey_user_input_line_2_browse.id != []:
                    if survey_user_input_line_2_browse[0].value_text is not False:
                        value_text = survey_user_input_line_2_browse[0].value_text.encode('utf-8')

                print(i,
                      patient_code,
                      family_code,
                      question,
                      question_type,
                      value_suggested,
                      value_text,
                      )

                row_insured = [i,
                               patient_code,
                               family_code,
                               question,
                               question_type,
                               value_suggested,
                               value_text,
                               ]
                writer_csv_file.writerow(row_insured)

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
                        family_code = False
                        if clv_document_browse.family_id.id != []:
                            family_code = clv_document_browse.family_id.code[0]

                        value_suggested_2 = False
                        if user_input_line_3.value_suggested is not False:
                            value_suggested_2 = user_input_line_3.value_suggested.value.encode('utf-8')
                        value_suggested = value_suggested_2

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

                print(i,
                      patient_code,
                      family_code,
                      question,
                      question_type,
                      value_suggested,
                      value_text,
                      )

                row_insured = [i,
                               patient_code,
                               family_code,
                               question,
                               question_type,
                               value_suggested,
                               value_text,
                               ]
                writer_csv_file.writerow(row_insured)

    csv_file.close()

    print()
    print('--> i: ', i)


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

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_06_QDH16_05_05.csv'
    # code = 'QDH16_05_05'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_08_QDH16_04_10.csv'
    # code = 'QDH16_04_10'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_09_QDH16_06_06.csv'
    # code = 'QDH16_06_06'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_16_QDH16_04_07.csv'
    # code = 'QDH16_04_07'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_28_QMD16_03_02.csv'
    # code = 'QMD16_03_02'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_20_FSE16_06_06.csv'
    # code = 'FSE16_06_06'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_22_FSE16_08_01.csv'
    # code = 'FSE16_08_01'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_29_FSE16_07_04.csv'
    # code = 'FSE16_07_04'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    # file_path = '/opt/openerp/jcafb/data/jcafb_2016_30_FSE16_07_05.csv'
    # code = 'FSE16_07_05'
    # print('-->', client, file_path, code)
    # print('--> survey_question_user_input_line_values()...')
    # survey_question_user_input_line_values(client, file_path, code)

    print('--> survey.py')
    print('--> Execution time:', secondsToStr(time() - start))
    print()
