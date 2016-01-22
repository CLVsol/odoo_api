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


def survey_user_input_clear_test_entry(client, args):

    survey_user_input = client.model('survey.user_input')
    survey_user_input_browse = survey_user_input.browse([('state', '=', 'done'),
                                                         ('test_entry', '=', True), ])

    i = 0
    for user_input in survey_user_input_browse:
        i += 1

        print(i, user_input.date_create, user_input.token)

        values = {
            "test_entry": False,
            }
        survey_user_input.write(user_input.id, values)

    print('--> i: ', i)


def survey_user_input_set_email_document_code(client, args):

    survey_user_input = client.model('survey.user_input')
    survey_user_input_browse = survey_user_input.browse(args)

    survey_user_input_line = client.model('survey.user_input_line')

    i = 0
    for user_input in survey_user_input_browse:
        i += 1

        print(i, user_input.date_create, user_input.token)

        survey_user_input_line_browse = survey_user_input_line.browse(
            [('user_input_id', '=', user_input.id), ])

        if len(survey_user_input_line_browse) > 0:

            document_code = survey_user_input_line_browse[0].value_text

            print('>>>>>', document_code)

            values = {
                "email": document_code,
                }
            survey_user_input.write(user_input.id, values)

    print('--> i: ', i)


def survey_user_input_set_email_Ok(client, args):

    survey_survey = client.model('survey.survey')
    survey_FSE16_id = survey_survey.browse([(
        'title', '=',
        '[FSE16] JCAFB 2016 - Questionário Socioeconômico Familiar (Crianças e Idosos)'), ])[0].id
    survey_ISE16_id = survey_survey.browse([(
        'title', '=',
        '[ISE16] JCAFB 2016 - Questionário Socioeconômico Individual (Idosos)'), ])[0].id
    survey_CSE16_id = survey_survey.browse([(
        'title', '=',
        '[CSE16] JCAFB 2016 - Questionário Socioeconômico Individual (Crianças)'), ])[0].id
    survey_QMD16_id = survey_survey.browse([(
        'title', '=',
        '[QMD16] JCAFB 2016 - Questionário Medicamento'), ])[0].id
    survey_ITM16_id = survey_survey.browse([(
        'title', '=',
        '[ITM16] JCAFB 2016 - Interpretação das Tabelas de Medicamentos'), ])[0].id
    survey_QAN16_id = survey_survey.browse([(
        'title', '=',
        '[QAN16] JCAFB 2016 - Questionário para detecção de Anemia'), ])[0].id
    survey_QDH16_id = survey_survey.browse([(
        'title', '=',
        '[QDH16] JCAFB 2016 - Questionário - Diabetes, Hipertensão Arterial e Hipercolesterolemia'), ])[0].id
    survey_TCP16_id = survey_survey.browse([(
        'title', '=',
        '[TCP16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO PARA A CAMPANHA DE DETECÇÃO DE DIABETES, ' +
        'HIPERTENSÃO ARTERIAL E HIPERCOLESTEROLEMIA'
        ), ])[0].id
    survey_TCR16_id = survey_survey.browse([(
        'title', '=',
        '[TCR16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAMES COPROPARASITOLÓGICOS, ' +
        'DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'
        ), ])[0].id
    survey_TID16_id = survey_survey.browse([(
        'title', '=',
        '[TID16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAME DE URINA, ' +
        'COPROPARASITOLÓGICO, DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'
        ), ])[0].id

    survey_user_input = client.model('survey.user_input')
    # survey_user_input_browse = survey_user_input.browse([('state', '=', state), ])
    survey_user_input_browse = survey_user_input.browse([])

    survey_user_input_line = client.model('survey.user_input_line')

    clv_document = client.model('clv_document')

    err_message = '[!]'

    i = 0
    done = 0
    new = 0
    not_new = 0
    ok = 0
    not_ok = 0
    # linked = 0
    for user_input in survey_user_input_browse:
        i += 1

        if user_input.state != 'done':
            continue

        done += 1
        document_browse = False

        print(i, user_input.date_create, user_input.token, user_input.state)
        # if survey_FSE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_FSE16_id')
        # if survey_ISE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_ISE16_id')
        # if survey_CSE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_CSE16_id')
        print('>>>>>', '(survey)', user_input.survey_id.title.encode('utf-8'),)

        survey_user_input_line_browse = survey_user_input_line.browse(
            [('user_input_id', '=', user_input.id), ])

        # if user_input.survey_id.survey_user_input_id is not False:
        #     not_new += 1
        #     continue

        # new += 1

        is_ok = True

        if len(survey_user_input_line_browse) > 0:

            document_browse = clv_document.browse(
                [('name', '=', survey_user_input_line_browse[0].value_text), ])
            if document_browse.id != []:
                print('yyyyy', survey_user_input_line_browse[0].value_text, document_browse)
                print('>>>>>', '(document)', document_browse[0].survey_id.title.encode("utf-8"))
                if document_browse[0].survey_user_input_id is not False:
                    print('xxxxx', document_browse[0].survey_user_input_id.id, user_input.id)
                    if document_browse[0].survey_user_input_id.id == user_input.id:
                        not_new += 1
                        continue
                    else:
                        err_message = '[Duplicated Document Code!]'
                        new += 1
                        not_ok += 1
                        print('>>>>>', 'NOT Ok')
                        is_ok = False
                else:
                    new += 1
            else:
                print('yyyyy', survey_user_input_line_browse[0].value_text, document_browse)
                err_message = '[Invalid Document Code!]'
                new += 1
                not_ok += 1
                print('>>>>>', 'NOT Ok')
                is_ok = False

        line = 0
        for input_line in survey_user_input_line_browse:
            line += 1
            ir_model_data_name = ir_model_data_get_name(client,
                                                        'survey.question',
                                                        input_line.question_id.id)
            # print('>>>>>', input_line.id, ir_model_data_name,
            #       input_line.question_id.type,
            #       input_line.question_id.question.encode('utf-8'))

            if line == 1:
                if input_line.question_id.type == 'textbox':
                    document_browse = clv_document.browse(
                        [('name', '=', input_line.value_text), ])
                    if document_browse.id != []:

                        # print('>>>>>', document_browse[0].survey_id.title.encode("utf-8"))
                        if is_ok:
                            if user_input.survey_id.title.encode('utf-8') == \
                               document_browse[0].survey_id.title.encode("utf-8"):
                                ok += 1
                                print('>>>>>', 'Ok')
                                # is_ok = True
                            else:
                                err_message = '[Survey Type Mismatch!]'
                                not_ok += 1
                                print('>>>>>', 'NOT Ok')
                                is_ok = False
                        patient_code = False
                        if document_browse[0].patient_id is not False:
                            patient_code = document_browse[0].patient_id.patient_code
                        family_code = False
                        if document_browse[0].family_id is not False:
                            family_code = document_browse[0].family_id.code
                        print('>>>>>', patient_code, family_code)

            if line <= 200:
                if input_line.question_id.type == 'textbox':
                    # print('>>>>>>>>>>', ir_model_data_name)
                    print('>>>>>>>>>>', line, input_line.value_text.encode('utf-8'),
                          input_line.question_id.question.encode('utf-8'))

                    if is_ok is True:
                        if survey_FSE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'FSE16_02_02':
                                if input_line.value_text != family_code:
                                    err_message = '[Family Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_ISE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'ISE16_02_02':
                                if input_line.value_text != patient_code:
                                    err_message = '[Patient Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'ISE16_02_04':
                                if input_line.value_text != family_code:
                                    err_message = '[Family Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_CSE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'ISE16_02_02':
                                if input_line.value_text != patient_code:
                                    err_message = '[Patient Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'CSE16_02_04':
                                if input_line.value_text != family_code:
                                    err_message = '[Patient Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_QAN16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'QAN16_02_02':
                                if input_line.value_text != patient_code:
                                    err_message = '[Patient Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'QAN16_02_04':
                                if input_line.value_text != family_code:
                                    err_message = '[Family Code Mismatch!]'
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        else:
                            err_message = '[Undefined Survey Type!]'
                            ok -= 1
                            not_ok += 1
                            print('>>>>>', 'NOT Ok')
                            is_ok = False

        if is_ok:
            email = 'Ok'
        else:
            email = 'NOT Ok' + ' ' + err_message

        values = {
            "email": email,
            }
        survey_user_input.write(user_input.id, values)

    print('--> i: ', i)
    print('--> done: ', done)
    print('--> new: ', new)
    print('--> not_new: ', not_new)
    print('--> ok: ', ok)
    print('--> not_ok: ', not_ok)
    # print('--> linked: ', linked)


def get_survey_data(client):

    survey_survey = client.model('survey.survey')
    survey_FSE16_id = survey_survey.browse([(
        'title', '=',
        '[FSE16] JCAFB 2016 - Questionário Socioeconômico Familiar (Crianças e Idosos)'), ])[0].id
    survey_ISE16_id = survey_survey.browse([(
        'title', '=',
        '[ISE16] JCAFB 2016 - Questionário Socioeconômico Individual (Idosos)'), ])[0].id
    survey_CSE16_id = survey_survey.browse([(
        'title', '=',
        '[CSE16] JCAFB 2016 - Questionário Socioeconômico Individual (Crianças)'), ])[0].id
    survey_QMD16_id = survey_survey.browse([(
        'title', '=',
        '[QMD16] JCAFB 2016 - Questionário Medicamento'), ])[0].id
    survey_ITM16_id = survey_survey.browse([(
        'title', '=',
        '[ITM16] JCAFB 2016 - Interpretação das Tabelas de Medicamentos'), ])[0].id
    survey_QAN16_id = survey_survey.browse([(
        'title', '=',
        '[QAN16] JCAFB 2016 - Questionário para detecção de Anemia'), ])[0].id
    survey_QDH16_id = survey_survey.browse([(
        'title', '=',
        '[QDH16] JCAFB 2016 - Questionário - Diabetes, Hipertensão Arterial e Hipercolesterolemia'), ])[0].id
    survey_TCP16_id = survey_survey.browse([(
        'title', '=',
        '[TCP16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO PARA A CAMPANHA DE DETECÇÃO DE DIABETES, ' +
        'HIPERTENSÃO ARTERIAL E HIPERCOLESTEROLEMIA'
        ), ])[0].id
    survey_TCR16_id = survey_survey.browse([(
        'title', '=',
        '[TCR16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAMES COPROPARASITOLÓGICOS, ' +
        'DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'
        ), ])[0].id
    survey_TID16_id = survey_survey.browse([(
        'title', '=',
        '[TID16] JCAFB 2016 - ' +
        'TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAME DE URINA, ' +
        'COPROPARASITOLÓGICO, DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'
        ), ])[0].id

    survey_user_input = client.model('survey.user_input')
    # survey_user_input_browse = survey_user_input.browse([('state', '=', state), ])
    survey_user_input_browse = survey_user_input.browse([])

    survey_user_input_line = client.model('survey.user_input_line')

    clv_document = client.model('clv_document')

    i = 0
    done = 0
    new = 0
    not_new = 0
    ok = 0
    not_ok = 0
    linked = 0
    for user_input in survey_user_input_browse:
        i += 1

        if user_input.state != 'done':
            continue

        done += 1
        document_browse = False

        print(i, user_input.date_create, user_input.token, user_input.state)
        # if survey_FSE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_FSE16_id')
        # if survey_ISE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_ISE16_id')
        # if survey_CSE16_id == user_input.survey_id.id:
        #     print('>>>>>', 'survey_CSE16_id')
        print('>>>>>', '(survey)', user_input.survey_id.title.encode('utf-8'),)

        survey_user_input_line_browse = survey_user_input_line.browse(
            [('user_input_id', '=', user_input.id), ])

        # if user_input.survey_id.survey_user_input_id is not False:
        #     not_new += 1
        #     continue

        # new += 1

        is_ok = True

        if len(survey_user_input_line_browse) > 0:

            document_browse = clv_document.browse(
                [('name', '=', survey_user_input_line_browse[0].value_text), ])
            if document_browse != []:
                print('>>>>>', '(document)', document_browse[0].survey_id.title.encode("utf-8"))
                if document_browse[0].survey_user_input_id is not False:
                    print('xxxxx', document_browse[0].survey_user_input_id.id, user_input.id)
                    if document_browse[0].survey_user_input_id.id == user_input.id:
                        not_new += 1
                        continue
                    else:
                        new += 1
                        not_ok += 1
                        print('>>>>>', 'NOT Ok')
                        is_ok = False
                else:
                    new += 1

        line = 0
        for input_line in survey_user_input_line_browse:
            line += 1
            ir_model_data_name = ir_model_data_get_name(client,
                                                        'survey.question',
                                                        input_line.question_id.id)
            # print('>>>>>', input_line.id, ir_model_data_name,
            #       input_line.question_id.type,
            #       input_line.question_id.question.encode('utf-8'))

            if line == 1:
                if input_line.question_id.type == 'textbox':
                    document_browse = clv_document.browse(
                        [('name', '=', input_line.value_text), ])
                    if document_browse != []:

                        # print('>>>>>', document_browse[0].survey_id.title.encode("utf-8"))
                        if is_ok:
                            if user_input.survey_id.title.encode('utf-8') == \
                               document_browse[0].survey_id.title.encode("utf-8"):
                                ok += 1
                                print('>>>>>', 'Ok')
                                # is_ok = True
                            else:
                                not_ok += 1
                                print('>>>>>', 'NOT Ok')
                                is_ok = False
                        patient_code = False
                        if document_browse[0].patient_id is not False:
                            patient_code = document_browse[0].patient_id.patient_code
                        family_code = False
                        if document_browse[0].family_id is not False:
                            family_code = document_browse[0].family_id.code
                        print('>>>>>', patient_code, family_code)

            if line <= 200:
                if input_line.question_id.type == 'textbox':
                    # print('>>>>>>>>>>', ir_model_data_name)
                    print('>>>>>>>>>>', line, input_line.value_text.encode('utf-8'),
                          input_line.question_id.question.encode('utf-8'))

                    if is_ok is True:
                        if survey_FSE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'FSE16_02_02':
                                if input_line.value_text != family_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_ISE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'ISE16_02_02':
                                if input_line.value_text != patient_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'ISE16_02_04':
                                if input_line.value_text != family_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_CSE16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'ISE16_02_02':
                                if input_line.value_text != patient_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'CSE16_02_04':
                                if input_line.value_text != family_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        elif survey_QAN16_id == user_input.survey_id.id:
                            if ir_model_data_name == 'QAN16_02_02':
                                if input_line.value_text != patient_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False
                            if ir_model_data_name == 'QAN16_02_04':
                                if input_line.value_text != family_code:
                                    ok -= 1
                                    not_ok += 1
                                    print('>>>>>', 'NOT Ok')
                                    is_ok = False

                        else:
                            ok -= 1
                            not_ok += 1
                            print('>>>>>', 'NOT Ok')
                            is_ok = False

        if is_ok:
            values = {
                "survey_user_input_id": user_input.id,
                }
            clv_document.write(document_browse[0].id, values)
            linked += 1

    print('--> i: ', i)
    print('--> done: ', done)
    print('--> new: ', new)
    print('--> not_new: ', not_new)
    print('--> ok: ', ok)
    print('--> not_ok: ', not_ok)
    print('--> linked: ', linked)


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

    # print('-->', client)
    # print('--> Executing survey_user_input_clear_test_entry()...')
    # survey_user_input_clear_test_entry(client)

    # # user_input_args = [('state', '=', 'done'),
    # #                    ('email', '=', False), ]
    # user_input_args = [('state', '=', 'done'), ]
    # print('-->', client, user_input_args)
    # print('--> Executing survey_user_input_set_email_document_code()...')
    # survey_user_input_set_email_document_code(client, user_input_args)

    # user_input_args = [('state', '=', 'done'),
    #                    ('email', '=', False), ]
    # user_input_args = [('state', '=', 'done'), ]
    # print('-->', client, user_input_args)
    # print('--> Executing survey_user_input_set_email_Ok()...')
    # survey_user_input_set_email_Ok(client, user_input_args)

    # print('-->', client)
    # print('--> Executing get_survey_data()...')
    # get_survey_data(client)

    print('--> survey.py')
    print('--> Execution time:', secondsToStr(time() - start))
