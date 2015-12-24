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


def clv_document_create(client, args):

    clv_document = client.model('clv_document')

    clv_patient = client.model('clv_patient')
    patient_browse = clv_patient.browse(args)

    clv_patient_category = client.model('clv_patient.category')
    cat_idoso_2016_id = clv_patient_category.browse([('name', '=', 'Idoso 2016'), ])[0].id
    cat_crianca_2016_id = clv_patient_category.browse([('name', '=', 'Criança 2016'), ])[0].id

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
    survey_QAN16_id = survey_survey.browse([(
        'title', '=',
        '[QAN16] JCAFB 2016 - Questionário para detecção de Anemia'), ])[0].id
    survey_QDH16_id = survey_survey.browse([(
        'title', '=',
        '[QDH16] JCAFB 2016 - Questionário - Diabetes, Hipertensão Arterial e Hipercolesterolemia'), ])[0].id
    survey_ITM16_id = survey_survey.browse([(
        'title', '=',
        '[ITM16] JCAFB 2016 - Interpretação das Tabelas de Medicamentos'), ])[0].id
    survey_TCP16_id = survey_survey.browse([(
        'title', '=',
        '[TCP16] JCAFB 2016 - TERMO DE CONSENTIMENTO PARA A CAMPANHA DE DETECÇÃO DE DIABETES, HIPERTENSÃO ARTERIAL E HIPERCOLESTEROLEMIA'), ])[0].id
    survey_TCR16_id = survey_survey.browse([(
        'title', '=',
        '[TCR16] JCAFB 2016 - TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAMES COPROPARASITOLÓGICOS, DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'), ])[0].id
    survey_TID16_id = survey_survey.browse([(
        'title', '=',
        '[TID16] JCAFB 2016 - TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO PARA REALIZAÇÃO DE EXAME DE URINA, COPROPARASITOLÓGICO, DETECÇÃO DE ANEMIA E QUESTIONÁRIO SOCIOECONÔMICO'), ])[0].id

    i = 0
    idoso_2016 = 0
    crianca_2016 = 0
    for patient in patient_browse:
        i += 1

        print(i, patient.name.encode('utf-8'), patient.category_ids.id)

        if (cat_idoso_2016_id in patient.category_ids.id) or \
           (cat_crianca_2016_id in patient.category_ids.id):

            family_id = patient.person.family_member_ids[0].family_id.id

            survey_ids = []
            for document in patient.person.family_member_ids.family_id.document_ids:
                survey_ids = survey_ids + document.survey_id.id

            if survey_FSE16_id not in survey_ids:

                values = {
                    'survey_id': survey_FSE16_id,
                    # 'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QMD16_id not in survey_ids:

                values = {
                    'survey_id': survey_QMD16_id,
                    # 'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_ITM16_id not in survey_ids:

                values = {
                    'survey_id': survey_ITM16_id,
                    # 'patient_id': patient.id,
                    'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

        if cat_idoso_2016_id in patient.category_ids.id:
            idoso_2016 += 1

            survey_ids = []
            for document in patient.person.family_member_ids.family_id.document_ids:
                survey_ids = survey_ids + document.survey_id.id

            if survey_ISE16_id not in survey_ids:

                values = {
                    'survey_id': survey_ISE16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QAN16_id not in survey_ids:

                values = {
                    'survey_id': survey_QAN16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QDH16_id not in survey_ids:

                values = {
                    'survey_id': survey_QDH16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_TID16_id not in survey_ids:

                values = {
                    'survey_id': survey_TID16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_TCP16_id not in survey_ids:

                values = {
                    'survey_id': survey_TCP16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

        if cat_crianca_2016_id in patient.category_ids.id:
            crianca_2016 += 1

            survey_ids = []
            for document in patient.person.family_member_ids.family_id.document_ids:
                survey_ids = survey_ids + document.survey_id.id

            if survey_CSE16_id not in survey_ids:

                values = {
                    'survey_id': survey_CSE16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_QAN16_id not in survey_ids:

                values = {
                    'survey_id': survey_QAN16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

            if survey_TCR16_id not in survey_ids:

                values = {
                    'survey_id': survey_TCR16_id,
                    'patient_id': patient.id,
                    # 'family_id': family_id,
                    }
                document_id = clv_document.create(values).id

                print('>>>>>', document_id)

    print('--> i: ', i)
    print('--> idoso_2016: ', idoso_2016)
    print('--> crianca_2016: ', crianca_2016)


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

    patient_args = [('category_ids', '!=', False), ]
    print('-->', client, patient_args)
    print('--> Executing clv_document_create()...')
    clv_document_create(client, patient_args)

    print('--> clv_document.py')
    print('--> Execution time:', secondsToStr(time() - start))
