#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function

from erppeek import *
import csv
import re

from base import *
import argparse
import getpass


def clv_medicament_dispensation_ext_unlink(client, args):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    medicament_dispensation_ext_browse = clv_medicament_dispensation_ext.browse(args)

    i = 0
    for medicament_dispensation_ext in medicament_dispensation_ext_browse:
        i += 1
        print(i, medicament_dispensation_ext.name)

        history = client.model('clv_medicament_dispensation_ext.history')
        history_browse = history.browse(
            [('medicament_dispensation_ext_id', '=', medicament_dispensation_ext.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_medicament_dispensation_ext.unlink(medicament_dispensation_ext.id)

    print('--> i: ', i)


def clv_medicament_dispensation_ext_updt_state_waiting(client, args):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    medicament_dispensation_ext_browse = clv_medicament_dispensation_ext.browse(args)

    count = 0
    for medicament_dispensation_ext in medicament_dispensation_ext_browse:
        count += 1

        print(count, medicament_dispensation_ext.state, medicament_dispensation_ext.name)

        if medicament_dispensation_ext.state == 'draft':
            client.exec_workflow('clv_medicament_dispensation_ext',
                                 'button_waiting',
                                 medicament_dispensation_ext.id)

    print('count: ', count)


def clv_medicament_dispensation_ext_import_orizon(client, file_name):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')

    res_partner = client.model('res.partner')
    partner_browse = res_partner.browse([('name', '=', 'Orizon'), ])
    partner_id = partner_browse.id[0]

    delimiter_char = ';'

    f = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        # Empresa = row[i.next()]
        ID_do_Beneficiario = row[i.next()]
        Nome_do_Beneficiario = row[i.next()]
        # ID_do_Titular = row[i.next()]
        # Nome_do_Titular = row[i.next()]
        # Matricula_Funcional = row[i.next()]
        # Limite_Subsidio = row[i.next()]
        Apresentacao_do_Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        # Qtde = row[i.next()]
        Autorizacao = row[i.next()]
        # Data_da_Venda = row[i.next()]
        Data_da_Captura = row[i.next()]
        Crm = row[i.next()]
        Uf_Crm = row[i.next()]
        # EAN = row[i.next()]
        Cnpj = row[i.next()]
        # Razao_Social = row[i.next()]
        Nome_Fantasia = row[i.next()]
        # Saldo_Subsidio = row[i.next()]
        # Limite_para_DF = row[i.next()]
        # Saldo_DF = row[i.next()]
        Qtde_UN = row[i.next()]
        Transacoes = row[i.next()]
        Total_Venda = row[i.next()].replace(",", ".")
        Total_Subsidio = row[i.next()].replace(",", ".")
        Total_Pago_a_Vista = row[i.next()].replace(",", ".")
        # Valor_da_Folha = row[i.next()]

        crd_code = ID_do_Beneficiario
        code_len = len(crd_code) - 2
        while len(crd_code) < 16:
            crd_code = '0' + crd_code
        code_str = "%s.%s.%s.%s.%s-%s" % (str(crd_code[0]) + str(crd_code[1]),
                                          str(crd_code[2]) + str(crd_code[3]) + str(crd_code[4]),
                                          str(crd_code[5]) + str(crd_code[6]) + str(crd_code[7]),
                                          str(crd_code[8]) + str(crd_code[9]) + str(crd_code[10]),
                                          str(crd_code[11]) + str(crd_code[12]) + str(crd_code[13]),
                                          str(crd_code[14]) + str(crd_code[15]))
        if code_len <= 3:
            code_form = code_str[18 - code_len:21]
        elif code_len > 3 and code_len <= 6:
            code_form = code_str[17 - code_len:21]
        elif code_len > 6 and code_len <= 9:
            code_form = code_str[16 - code_len:21]
        elif code_len > 9 and code_len <= 12:
            code_form = code_str[15 - code_len:21]
        elif code_len > 12 and code_len <= 14:
            code_form = code_str[14 - code_len:21]

        Crm = Uf_Crm + '-CRM-' + Crm

        print(rownum, code_form, Nome_do_Beneficiario, Cod_Prod, Data_da_Captura, Cnpj, Crm, Uf_Crm)

        values = {
            # 'name': '/',
            'name': False,
            'dispensation_date': Data_da_Captura,
            'medicament_code': Cod_Prod,
            'medicament_description': Apresentacao_do_Produto,
            'insured_card_code': code_form,
            'insured_name': Nome_do_Beneficiario,
            'prescriber_code': Crm,
            'pharmacy_code': Cnpj,
            'pharmacy_name': Nome_Fantasia,
            'pack_quantity': Qtde_UN,
            'sale_value': Total_Venda,
            'subsidy_value': Total_Subsidio,
            'at_sight_value': Total_Pago_a_Vista,
            'authorization_code': Autorizacao,
            'partner_id': partner_id,
            }
        medicament_dispensation_ext_id = clv_medicament_dispensation_ext.create(values)

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)


def clv_medicament_dispensation_ext_updt_name(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('name', '=', False),
                                                                      ],
                                                                     order='authorization_code')

    i = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.authorization_code, dispensation_ext.dispensation_date)

        values = {
            'name': '/',
            }
        clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

    print('i: ', i)


def clv_medicament_dispensation_ext_updt_pharmacy(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('pharmacy_id', '=', False),
                                                                      ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        val = re.sub('[^0-9]', '', dispensation_ext.pharmacy_code)
        if len(val) == 14:
            cnpj = "%s.%s.%s/%s-%s" % (val[0:2], val[2:5], val[5:8], val[8:12], val[12:14])

        i += 1
        print(i, dispensation_ext.name, cnpj)

        clv_pharmacy = client.model('clv_pharmacy')
        pharmacy_browse = clv_pharmacy.browse([('cnpj', '=', cnpj), ])
        pharmacy_id = pharmacy_browse.id

        if pharmacy_id != []:
            found += 1

            values = {
                'pharmacy_id': pharmacy_id[0],
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_ext_updt_prescriber(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('prescriber_id', '=', False),
                                                                      ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.prescriber_code)

        clv_professional = client.model('clv_professional')
        prescriber_browse = clv_professional.browse(
            [('professional_id', '=', dispensation_ext.prescriber_code), ])
        prescriber_id = prescriber_browse.id

        if prescriber_id != []:
            found += 1

            values = {
                'prescriber_id': prescriber_id[0],
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_ext_updt_insured_card(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('insured_card_id', '=', False),
                                                                      ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.insured_card_code)

        clv_insured_card = client.model('clv_insured_card')
        insured_card_browse = clv_insured_card.browse(
            [('code', '=', dispensation_ext.insured_card_code), ])
        insured_card_id = insured_card_browse.id

        if insured_card_id != []:
            found += 1

            values = {
                'insured_card_id': insured_card_id[0],
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('medicament_ref', '=', False), ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.medicament_code)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse(
            [('cod_prod', '=', dispensation_ext.medicament_code), ])
        orizon_lpm_id = orizon_lpm_browse.id

        if orizon_lpm_id != []:
            found += 1

            values = {
                'medicament_ref': 'clv_orizon_lpm,' + str(orizon_lpm_id[0]),
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_ext_updt_medicament(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('state', '=', 'draft'),
                                                                      ('medicament', '=', False), ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        if dispensation_ext.medicament_ref is not False:
            print(i, dispensation_ext.name, dispensation_ext.medicament_ref.name.encode('utf-8'))

            clv_medicament = client.model('clv_medicament')
            medicament_browse = clv_medicament.browse(
                [('orizon_lpm_id', '=', dispensation_ext.medicament_ref.id), ])
            medicament_id = medicament_browse.id

            if medicament_id != []:
                found += 1

                values = {
                    'medicament': medicament_id[0],
                }
                clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

            else:
                not_found += 1
        else:
            print(i, dispensation_ext.name, dispensation_ext.medicament_ref)

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_ext_updt_dispensation(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation')

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse(
        [('state', '=', 'draft'),
         ('dispensation_id', '=', False),
         ('pharmacy_id', '!=', False),
         ('prescriber_id', '!=', False),
         ('insured_card_id', '!=', False),
         ('medicament', '!=', False),
         ('dispensation_date', '!=', False),
         ])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.medicament_ref.name.encode('utf-8'))

        clv_medicament_dispensation = client.model('clv_medicament_dispensation')
        medicament_dispensation_browse = clv_medicament_dispensation.browse(
            [('pharmacy_id', '=', dispensation_ext.pharmacy_id.id),
             ('prescriber_id', '=', dispensation_ext.prescriber_id.id),
             ('insured_card_id', '=', dispensation_ext.insured_card_id.id),
             ('medicament', '=', dispensation_ext.medicament.id),
             ('dispensation_date', '=', dispensation_ext.dispensation_date),
             ])
        dispensation_id = medicament_dispensation_browse.id

        if dispensation_id != []:
            found += 1

            values = {
                'dispensation_id': dispensation_id[0],
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

            values = {
                'dispensation_ext_id': dispensation_ext.id,
                }
            clv_medicament_dispensation.write(dispensation_id[0], values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


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

    print('--> clv_medicament_dispensation_ext.py...')

    client = erppeek.Client(server, dbname, username, password)

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_21_05_a_20_09.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # dispensation_args = [('state', '=', 'draft'),]
    # print('-->', client, dispensation_args)
    # print('--> Executing clv_medicament_dispensation_ext_updt_state_waiting()...')
    # clv_medicament_dispensation_ext_updt_state_waiting(client, dispensation_args)

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_21_09_a_27_09.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_28_09_a_20_10.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_21_10_a_31_10.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # medicament_dispensation_ext_args = [('name', '=', False), ]
    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_unlink()...')
    # clv_medicament_dispensation_ext_unlink(client, medicament_dispensation_ext_args)

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_01_11_a_20_11.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_21_11_a_30_11.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_01_12_a_20_12.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-12-2015_ate_20-01-2016.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-01-2016_ate_31-01-2016.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_01-02_ate_10-02.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_11-02_ate_20_02.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-02_ate_29-02.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_01-03_ate_10-03.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    #######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_11-03_ate_20-03.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # 2016-04-01 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-03_ate_31-03.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # 2016-04-12 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_01-04_ate_10-04.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-04-22 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_11-04_ate_20-04.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-05-04 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-04_ate_30-04.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-05-11 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_01-05_ate_10-05.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-05-23 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_11-05_ate_20-05.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-06-02 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_21-05_ate_31-05.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-06-13 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-Analitico_01-06_a_10-06.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### 2016-06-21 ######################################

    # file_name = '/opt/openerp/orizon/Desconto_em_Folha-AnalItico_11-06_a_20-06.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-25) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_21-05-2017_ate_31-05-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-26a) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-06-2017_ate_30-06-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-26b) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-07-2017_ate_31-07-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-26c) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-08-2017_ate_31-08-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-26d) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-09-2017_ate_30-09-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-11-27a) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Anaiitico_01-10_ate_31-10.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-12-06) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-11_ate_30-11.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2017-12-20) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-12_ate_19-12.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-02-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_01-01_ate_31-01.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-02-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-02-01_ate_2018-02-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # file_name = '/opt/openerp/orizon/1898_Desconto_em_Folha_Analitico_2018-02-01_ate_2018-02-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-03-01) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-02-21_ate_2018-02-28.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-03-21) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-03-01_ate_2018-03-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-04-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-03-21_ate_2018-03-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-04-23) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-04-01_ate_2018-04-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-05-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-04-21_ate_2018-04-30.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-05-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-05-01_ate_2018-05-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-06-04) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-05-21_ate_2018-05-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-06-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-06-01_ate_2018-06-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-07-04) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-06-21_ate_2018-06-30.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-07-23) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-07-01_ate_2018-07-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-08-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-07-21_ate_2018-07-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-08-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-08-01_ate_2018-08-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-09-06) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-08-21_ate_2018-08-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-09-25) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-09-01_ate_2018-09-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-10-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-09-21_ate_2018-09-30.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-10-25) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-10-01_ate_2018-10-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-11-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-10-21_ate_2018-10-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-11-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-11-01_ate_2018-11-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')

    # ##### (2018-12-05) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-11-21_ate_2018-11-30.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2018-12-26) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-12-01_ate_2018-12-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-01-06) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2018-12-21_ate_2018-12-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-01-21) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-01-01_ate_2019-01-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-02-04) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-01-21_ate_2019-01-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-02-21) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-02-01_ate_2019-02-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-03-07) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-02-21_ate_2019-02-28.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-03-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-03-01_ate_2019-03-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-04-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-03-21_ate_2019-03-31.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-04-22) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-04-01_ate_2019-04-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-05-02) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-04-21_ate_2019-04-30.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    # ##### (2019-05-21) ######################################

    # file_name = '/opt/openerp/orizon/1865_Desconto_em_Folha_Analitico_2019-05-01_ate_2019-05-20.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_name()...')
    # clv_medicament_dispensation_ext_updt_name(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_dispensation()...')
    # clv_medicament_dispensation_ext_updt_dispensation(client)

    print('--> clv_medicament_dispensation_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))

    # file_name = '/opt/openerp/orizon/1897_Desconto_em_Folha_Analitico_01-01-2017_ate_30-09-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)

    # file_name = '/opt/openerp/orizon/1898_Desconto_em_Folha_Analitico_01-01-2017_ate_30-09-2017.csv'
    # print('-->', client, file_name)
    # print('--> Executing clv_medicament_dispensation_ext_import_orizon()...')
    # clv_medicament_dispensation_ext_import_orizon(client, file_name)
