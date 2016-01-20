#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                 #
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

from ir_model_data import *


def get_survey_user_input(client, state, survey_code):

    survey_user_input = client.model('survey.user_input')
    # survey_user_input_browse = survey_user_input.browse([('state', '=', state), ])
    survey_user_input_browse = survey_user_input.browse([])

    survey_user_input_line = client.model('survey.user_input_line')

    i = 0
    for user_input in survey_user_input_browse:
        i += 1
        print(i, user_input.token, user_input.state,
              user_input.survey_id.title.encode('utf-8'))

        survey_user_input_line_browse = survey_user_input_line.browse(
            [('survey_id', '=', user_input.survey_id.id), ])
        for input_line in survey_user_input_line_browse:
            ir_model_data_name = ir_model_data_get_name(client,
                                                        'survey.question',
                                                        input_line.question_id.id)
            print('>>>>>', input_line.id, ir_model_data_name,
                  input_line.question_id.type,
                  input_line.question_id.question.encode('utf-8'))

            if input_line.question_id.type == 'textbox':
                print('>>>>>>>>>>', input_line.value_text)


def get_survey_data(client):

    survey_user_input = client.model('survey.user_input')
    # survey_user_input_browse = survey_user_input.browse([('state', '=', state), ])
    survey_user_input_browse = survey_user_input.browse([])

    survey_user_input_line = client.model('survey.user_input_line')

    clv_document = client.model('clv_document')

    i = 0
    for user_input in survey_user_input_browse:
        i += 1
        # print(i, user_input.token, user_input.state,
        #       user_input.survey_id.title.encode('utf-8'))
        print(i, user_input.token, user_input.state)
        print('>>>>>', user_input.survey_id.title.encode('utf-8'))

        survey_user_input_line_browse = survey_user_input_line.browse(
            [('user_input_id', '=', user_input.id), ])
        line = 0
        for input_line in survey_user_input_line_browse:
            line += 1
            # ir_model_data_name = ir_model_data_get_name(client,
            #                                             'survey.question',
            #                                             input_line.question_id.id)
            # print('>>>>>', input_line.id, ir_model_data_name,
            #       input_line.question_id.type,
            #       input_line.question_id.question.encode('utf-8'))

            if line == 1:
                if input_line.question_id.type == 'textbox':
                    document_browse = clv_document.browse(
                        [('name', '=', input_line.value_text), ])
                    if document_browse != []:
                        print('>>>>>', document_browse[0].survey_id.title.encode("utf-8"))
                        if user_input.survey_id.title.encode('utf-8') == \
                           document_browse[0].survey_id.title.encode("utf-8"):
                            print('>>>>>', 'Ok')
                        else:
                            print('>>>>>', 'NOT Ok')

            if line <= 200:
                if input_line.question_id.type == 'textbox':
                    print('>>>>>>>>>>', line, input_line.value_text,
                          input_line.question_id.question.encode('utf-8'))

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

    get_arguments()

    from time import time
    start = time()

    print('--> survey.py...')

    client = erppeek.Client(server, dbname, username, password)

    # state = 'new'
    # survey_code = '040.008-46'
    # print('-->', client, state, survey_code)
    # print('--> Executing get_survey_user_input()...')
    # get_survey_user_input(client, state, survey_code)

    print('-->', client)
    print('--> Executing get_survey_data()...')
    get_survey_data(client)

    print('--> survey.py')
    print('--> Execution time:', secondsToStr(time() - start))
