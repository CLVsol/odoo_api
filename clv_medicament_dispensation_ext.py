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

from base import *
import argparse
import getpass

def clv_medicament_dispensation_ext_import(client, file_name):

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')

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
        Qtde = row[i.next()]
        Crm = row[i.next()]
        Uf_Crm = row[i.next()]
        Cod_Prod = row[i.next()]
        # EAN = row[i.next()]
        Data_da_Venda = row[i.next()]
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
            'name': False,
            'dispensation_date': Data_da_Venda,
            'medicament_code': Cod_Prod,
            'insured_card_code': code_form,
            'prescriber_code': Crm,
            'pharmacy_code': Cnpj,
            'pack_quantity': Qtde_UN,
            'sale_value': Total_Venda,
            'subsidy_value': Total_Subsidio,
            'at_sight_value': Total_Pago_a_Vista,
            }
        medicament_dispensation_ext_id = clv_medicament_dispensation_ext.create(values)

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)

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

    file_name = '/opt/openerp/orizon/Desconto_em_Folha_Sintetico_21_07_a_20_08.csv'
    print('-->', client, file_name)
    print('--> Executing clv_medicament_dispensation_ext_import()...')
    clv_medicament_dispensation_ext_import(client, file_name)

    print('--> clv_medicament_dispensation_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))
