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


def clv_document_unlink(client, args):

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for document in document_browse:
        i += 1
        print(i, document.name.encode("utf-8"))

        history = client.model('clv_document.history')
        history_browse = history.browse([('document_id', '=', document.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_document.unlink(document.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


def clv_document_unlink_Termos(client, args):

    survey_survey = client.model('survey.survey')
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

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for document in document_browse:
        i += 1
        print(i, document.name.encode("utf-8"))

        if (document.survey_id.id == survey_TCP16_id) or \
           (document.survey_id.id == survey_TCR16_id) or \
           (document.survey_id.id == survey_TID16_id):

            history = client.model('clv_document.history')
            history_browse = history.browse([('document_id', '=', document.id), ])
            history_ids = history_browse.id
            print('>>>>>', history_ids)

            history.unlink(history_ids)
            try:
                clv_document.unlink(document.id)
                deleted += 1
            except:
                print('>>>>>', 'Not deleted!')
                not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


def clv_document_create(client, args):

    clv_document = client.model('clv_document')

    clv_patient = client.model('clv_patient')
    patient_browse = clv_patient.browse(args)

    clv_patient_category = client.model('clv_patient.category')
    cat_idoso_2016_id = clv_patient_category.browse([('name', '=', 'Idoso 2016'), ])[0].id
    cat_crianca_2016_id = clv_patient_category.browse([('name', '=', 'Criança 2016'), ])[0].id
    cat_dhc_2016_id = clv_patient_category.browse([('name', '=', 'DHC 2016'), ])[0].id
    cat_anemia_2016_id = clv_patient_category.browse([('name', '=', 'Anemia 2016'), ])[0].id

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

    i = 0
    idoso_2016 = 0
    crianca_2016 = 0
    dhc_2016 = 0
    anemia_2016 = 0
    for patient in patient_browse:
        i += 1

        print(i, patient.name.encode('utf-8'), patient.category_ids.id)

        if (cat_idoso_2016_id in patient.category_ids.id) or \
           (cat_crianca_2016_id in patient.category_ids.id):

            family_id = False
            try:
                family_id = patient.person.family_member_ids[0].family_id.id
            except:
                pass

            survey_ids = []
            for document in patient.person.family_member_ids.family_id.document_ids:
                print('>>>>>', survey_ids, document.survey_id.id)
                survey_ids = survey_ids + document.survey_id.id

            if survey_FSE16_id not in survey_ids:

                values = {
                    'survey_id': survey_FSE16_id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

        if cat_idoso_2016_id in patient.category_ids.id:
            idoso_2016 += 1

            family_id = False
            try:
                family_id = patient.person.family_member_ids[0].family_id.id
            except:
                pass

            survey_ids = []
            for document in patient.document_ids:
                print('>>>>>', survey_ids, [document.survey_id.id])
                survey_ids = survey_ids + [document.survey_id.id]

            if survey_ISE16_id not in survey_ids:

                values = {
                    'survey_id': survey_ISE16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QMD16_id not in survey_ids:

                values = {
                    'survey_id': survey_QMD16_id,
                    'family_id': family_id,
                    'patient_id': patient.id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_ITM16_id not in survey_ids:

                values = {
                    'survey_id': survey_ITM16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QAN16_id not in survey_ids:

                values = {
                    'survey_id': survey_QAN16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QDH16_id not in survey_ids:

                values = {
                    'survey_id': survey_QDH16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            # if survey_TID16_id not in survey_ids:

            #     values = {
            #         'survey_id': survey_TID16_id,
            #         'patient_id': patient.id,
            #         'family_id': family_id,
            #         }
            #     document_id = clv_document.create(values).id

            #     print('>>>>>', document_id)

            # if survey_TCP16_id not in survey_ids:

            #     values = {
            #         'survey_id': survey_TCP16_id,
            #         'patient_id': patient.id,
            #         'family_id': family_id,
            #         }
            #     document_id = clv_document.create(values).id

            #     print('>>>>>', document_id)

        if cat_crianca_2016_id in patient.category_ids.id:
            crianca_2016 += 1

            family_id = False
            try:
                family_id = patient.person.family_member_ids[0].family_id.id
            except:
                pass

            survey_ids = []
            for document in patient.document_ids:
                print('>>>>>', survey_ids, [document.survey_id.id])
                survey_ids = survey_ids + [document.survey_id.id]

            if survey_CSE16_id not in survey_ids:

                values = {
                    'survey_id': survey_CSE16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QAN16_id not in survey_ids:

                values = {
                    'survey_id': survey_QAN16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            # if survey_TCR16_id not in survey_ids:

            #     values = {
            #         'survey_id': survey_TCR16_id,
            #         'patient_id': patient.id,
            #         'family_id': family_id,
            #         }
            #     document_id = clv_document.create(values).id

            #     print('>>>>>', document_id)

        if cat_dhc_2016_id in patient.category_ids.id:
            dhc_2016 += 1

            survey_ids = []
            for document in patient.document_ids:
                print('>>>>>', survey_ids, [document.survey_id.id])
                survey_ids = survey_ids + [document.survey_id.id]

            family_id = False
            try:
                family_id = patient.person.family_member_ids[0].family_id.id
            except:
                pass

            if survey_QDH16_id not in survey_ids:

                values = {
                    'survey_id': survey_QDH16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            # if survey_TCP16_id not in survey_ids:

            #     values = {
            #         'survey_id': survey_TCP16_id,
            #         'patient_id': patient.id,
            #         'family_id': family_id,
            #         }
            #     document_id = clv_document.create(values).id

            #     print('>>>>>', document_id)

        if cat_anemia_2016_id in patient.category_ids.id:
            anemia_2016 += 1

            family_id = False
            try:
                family_id = patient.person.family_member_ids[0].family_id.id
            except:
                pass

            survey_ids = []
            for document in patient.document_ids:
                print('>>>>>', survey_ids, [document.survey_id.id])
                survey_ids = survey_ids + [document.survey_id.id]

            if survey_QAN16_id not in survey_ids:

                values = {
                    'survey_id': survey_QAN16_id,
                    'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

    print('--> i: ', i)
    print('--> idoso_2016: ', idoso_2016)
    print('--> crianca_2016: ', crianca_2016)
    print('--> dhc_2016: ', dhc_2016)
    print('--> anemia_2016: ', anemia_2016)


def clv_document_clear_survey_user_input_id(client, args):

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    i = 0
    for document in document_browse:
        i += 1
        print(i, document.name, document.survey_id.title.encode("utf-8"))

        values = {
            "survey_user_input_id": False,
            }
        clv_document.write(document.id, values)

    print('--> i: ', i)


def clv_document_get_survey_user_input_id(client, args):

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

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    survey_user_input_line = client.model('survey.user_input_line')

    i = 0
    found = 0
    not_found = 0
    for document in document_browse:
        # i += 1
        # print(i, document.name, document.survey_id.title.encode("utf-8"))

        if document.survey_id.id == survey_FSE16_id:
            i += 1

            survey_user_input_line_browse = survey_user_input_line.browse(
                [('value_text', '=', document.name), ])
            survey_user_input_line_ids = survey_user_input_line_browse.id

            if survey_user_input_line_ids != []:
                found += 1
                print(i, document.name, document.survey_id.title.encode("utf-8"),
                      survey_user_input_line_browse[0].user_input_id.state)

                # values = {
                #     "survey_user_input_id": survey_user_input_line_browse[0].user_input_id.id,
                #     }
                # clv_document.write(document.id, values)

            else:
                not_found += 1

        if document.survey_id.id == survey_ISE16_id:
            i += 1

            survey_user_input_line_browse = survey_user_input_line.browse(
                [('value_text', '=', document.name), ])
            survey_user_input_line_ids = survey_user_input_line_browse.id

            if survey_user_input_line_ids != []:
                found += 1
                print(i, document.name, document.survey_id.title.encode("utf-8"),
                      survey_user_input_line_browse[0].user_input_id.state)

                # values = {
                #     "survey_user_input_id": survey_user_input_line_browse[0].user_input_id.id,
                #     }
                # clv_document.write(document.id, values)

            else:
                not_found += 1

        if document.survey_id.id == survey_CSE16_id:
            i += 1

            survey_user_input_line_browse = survey_user_input_line.browse(
                [('value_text', '=', document.name), ])
            survey_user_input_line_ids = survey_user_input_line_browse.id

            if survey_user_input_line_ids != []:
                found += 1
                print(i, document.name, document.survey_id.title.encode("utf-8"),
                      survey_user_input_line_browse[0].user_input_id.state)

                # values = {
                #     "survey_user_input_id": survey_user_input_line_browse[0].user_input_id.id,
                #     }
                # clv_document.write(document.id, values)

            else:
                not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_document_activate_patient_and_family(client, args):

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    i = 0
    found_patient = 0
    not_found_patient = 0
    found_family = 0
    not_found_family = 0
    for document in document_browse:
        i += 1
        print(i, document.name, document.survey_id.title.encode("utf-8"))

        if document.patient_id is not False:
            found_patient += 1
            print('>>>>>', document.patient_id.state)
            if document.patient_id.state != 'active':
                client.exec_workflow('clv_patient', 'button_activate', document.patient_id.id)
        else:
            not_found_patient += 1

        if document.family_id is not False:
            found_family += 1
            print('>>>>>', document.family_id.state)
            if document.family_id.state != 'active':
                client.exec_workflow('clv_family', 'button_activate', document.family_id.id)
        else:
            not_found_family += 1

    print('--> i: ', i)
    print('--> found_patient: ', found_patient)
    print('--> not_found_patient: ', not_found_patient)
    print('--> found_family: ', found_family)
    print('--> not_found_family: ', not_found_family)


def clv_document_updt_state_done(client, args):

    clv_document = client.model('clv_document')
    document_browse = clv_document.browse(args)

    document_count = 0
    for document in document_browse:
        document_count += 1

        print(document_count, document.state, document.name.encode("utf-8"))

        client.exec_workflow('clv_document', 'button_done', document.id)

    print('document_count: ', document_count)


def clv_document_updt_state_waiting(client, args):

    clv_document = client.model('clv_document')

    document_count_1 = 0
    document_count_2 = 0
    set_waiting = 0

    document_browse = clv_document.browse(args + [('patient_id', '!=', False)])
    for document in document_browse:
        document_count_1 += 1

        print(document_count_1, document.state, document.name.encode("utf-8"))

        print('>>>>>', document.patient_id.state)
        if document.patient_id.state != 'active':
            set_waiting += 1
            client.exec_workflow('clv_document', 'button_waiting', document.id)

    document_browse = clv_document.browse(args + [('family_id', '!=', False)])
    for document in document_browse:
        document_count_2 += 1

        print(document_count_2, document.state, document.name.encode("utf-8"))

        print('>>>>>', document.family_id.state)
        if document.family_id.state != 'active':
            set_waiting += 1
            client.exec_workflow('clv_document', 'button_waiting', document.id)

    print('document_count_1: ', document_count_1)
    print('document_count_2: ', document_count_2)
    print('--> set_waiting: ', set_waiting)


def clv_document_updt_state_revised_2(client, args):

    clv_document = client.model('clv_document')

    document_count = 0
    set_revised = 0

    document_browse = clv_document.browse(args)
    for document in document_browse:
        document_count += 1

        print(document_count, document.state, document.name.encode("utf-8"))

        set_revised += 1
        client.exec_workflow('clv_document', 'button_revised', document.id)

    print('document_count: ', document_count)
    print('--> set_revised: ', set_revised)


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

    print('--> clv_document.py...')

    client = erppeek.Client(server, dbname, username, password)

    # patient_args = [('category_ids', '!=', False), ]
    # print('-->', client, patient_args)
    # print('--> Executing clv_document_create()...')
    # clv_document_create(client, patient_args)

    # # document_args = [('state', '=', 'waiting'),
    # #                  ('survey_user_input_id', '!=', False),
    # #                  ]
    # document_args = [('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_clear_survey_user_input_id()...')
    # clv_document_clear_survey_user_input_id(client, document_args)

    # document_args = [('state', '=', 'draft'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_get_survey_user_input_id()...')
    # clv_document_get_survey_user_input_id(client, document_args)

    ##############################

    # document_args = []
    # print('-->', client, document_args)
    # print('--> Executing clv_document_unlink_Termos()...')
    # clv_document_unlink_Termos(client, document_args)

    # patient_args = [('category_ids', '!=', False), ]
    # print('-->', client, patient_args)
    # print('--> Executing clv_document_create()...')
    # clv_document_create(client, patient_args)

    # document_args = [('patient_id', '=', False),
    #                  ('family_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_unlink()...')
    # clv_document_unlink(client, document_args)

    # document_args = [('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_activate_patient_and_family()...')
    # clv_document_activate_patient_and_family(client, document_args)

    # document_args = [('state', '!=', 'done'),
    #                  ('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_done()...')
    # clv_document_updt_state_done(client, document_args)

    # document_args = [('state', '!=', 'waiting'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_waiting()...')
    # clv_document_updt_state_waiting(client, document_args)

    ##############################

    # document_args = [('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_activate_patient_and_family()...')
    # clv_document_activate_patient_and_family(client, document_args)

    # document_args = [('state', '!=', 'done'),
    #                  ('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_done()...')
    # clv_document_updt_state_done(client, document_args)

    # document_args = [('state', '!=', 'waiting'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_waiting()...')
    # clv_document_updt_state_waiting(client, document_args)

    ##############################

    # # document_args = [('state', '=', 'waiting'),
    # #                  ('survey_user_input_id', '!=', False),
    # #                  ]
    # document_args = [('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_clear_survey_user_input_id()...')
    # clv_document_clear_survey_user_input_id(client, document_args)

    # document_args = [('state', '=', 'done'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_revised_2()...')
    # clv_document_updt_state_revised_2(client, document_args)

    # document_args = [('state', '=', 'waiting'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_revised_2()...')
    # clv_document_updt_state_revised_2(client, document_args)

    # document_args = [('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_activate_patient_and_family()...')
    # clv_document_activate_patient_and_family(client, document_args)

    # document_args = [('state', '!=', 'done'),
    #                  ('survey_user_input_id', '!=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_done()...')
    # clv_document_updt_state_done(client, document_args)

    # document_args = [('state', '!=', 'waiting'),
    #                  ('survey_user_input_id', '=', False),
    #                  ]
    # print('-->', client, document_args)
    # print('--> Executing clv_document_updt_state_waiting()...')
    # clv_document_updt_state_waiting(client, document_args)

    print('--> clv_document.py')
    print('--> Execution time:', secondsToStr(time() - start))
