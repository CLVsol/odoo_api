#!/usr/bin/env python
# -*- encoding: utf-8 -*-
################################################################################
#                                                                              #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                  #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Affero General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU Affero General Public License for more details.                          #
#                                                                              #
# You should have received a copy of the GNU Affero General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
################################################################################

from __future__ import print_function

import xmlrpclib
from erppeek import *
import csv
import re

from base import *
import argparse
import getpass

def clv_medicament_dispensation_ext_import_orizon(client, file_name):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')

    res_partner = client.model('res.partner')
    partner_browse = res_partner.browse([('name', '=', 'Orizon'),])
    partner_id = partner_browse.id[0]

    delimiter_char = ';'

    f  = open(file_name, "rb")
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
        Qtde = row[i.next()]
        Autorizacao = row[i.next()]
        Data_da_Venda = row[i.next()]
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

        Crm =  Uf_Crm + '-CRM-' + Crm
        
        print(rownum, code_form, Nome_do_Beneficiario, Cod_Prod, Data_da_Venda, Cnpj, Crm, Uf_Crm)

        values = {
            'name': '/',
            'dispensation_date': Data_da_Venda,
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

def clv_medicament_dispensation_ext_updt_pharmacy(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('pharmacy_id', '=', False),])

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
        pharmacy_browse = clv_pharmacy.browse([('cnpj', '=', cnpj),])
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
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('prescriber_id', '=', False),])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.prescriber_code)

        clv_professional = client.model('clv_professional')
        prescriber_browse = clv_professional.browse([('professional_id', '=', dispensation_ext.prescriber_code),])
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
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('insured_card_id', '=', False),])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.insured_card_code)

        clv_insured_card = client.model('clv_insured_card')
        insured_card_browse = clv_insured_card.browse([('code', '=', dispensation_ext.insured_card_code),])
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

def clv_medicament_dispensation_ext_updt_medicament_ref(client):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('medicament_ref', '=', False),])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.medicament_code)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse([('cod_prod', '=', dispensation_ext.medicament_code),])
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
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse([('medicament', '=', False),])

    i = 0
    found = 0
    not_found = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.medicament_ref)

        clv_medicament = client.model('clv_medicament')
        medicament_browse = clv_medicament.browse([('orizon_lpm_id', '=', dispensation_ext.medicament_ref.id),])
        medicament_id = medicament_browse.id

        if medicament_id != []:
            found += 1

            values = {
                'medicament': medicament_id[0],
                }
            clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

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

    if args.dbname != None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

    if args.username != None:
        username = args.username
    elif username == '*':
        username = raw_input('username: ')

    if args.password != None:
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
    # print('--> Executing clv_medicament_dispensation_ext_updt_pharmacy()...')
    # clv_medicament_dispensation_ext_updt_pharmacy(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_prescriber()...')
    # clv_medicament_dispensation_ext_updt_prescriber(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_insured_card()...')
    # clv_medicament_dispensation_ext_updt_insured_card(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament_ref()...')
    # clv_medicament_dispensation_ext_updt_medicament_ref(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_ext_updt_medicament()...')
    # clv_medicament_dispensation_ext_updt_medicament(client)

    print('--> clv_medicament_dispensation_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))
