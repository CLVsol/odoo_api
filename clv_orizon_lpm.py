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

def clv_orizon_lpm_import_new(client, file_name, from_):

    delimiter_char = ';'

    f  = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Laboratorio = row[i.next()]
        Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        EAN_Principal = row[i.next()]
        # Vazio = row[i.next()]
        PMC = row[i.next()].replace(",", ".")
        Desconto = row[i.next()].replace(",", ".")
        Preco_Venda = row[i.next()].replace(",", ".")
        Categoria = row[i.next()]
        Sub_Categoria = row[i.next()]
        Classificacao = row[i.next()]
        Sub_Classificacao = row[i.next()]
        Descricao = row[i.next()]
        Classe_Terapeutica = row[i.next()]
        Sub_Classe_Terapeutica = row[i.next()]
        Principio_Ativo = row[i.next()]

        print(rownum, Cod_Prod, from_)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse([('cod_prod', '=', Cod_Prod),])
        orizon_lpm_id = orizon_lpm_browse.id

        values = {
            'cod_prod': Cod_Prod,
            'latoratorio': Laboratorio,
            'produto': Produto,
            'apres_produto': Apresentacao_Do_Produto,
            'ean_principal': EAN_Principal,
            'pmc': PMC,
            'desconto': Desconto,
            'preco_venda': Preco_Venda,
            'categoria': Categoria,
            'sub_categoria': Sub_Categoria,
            'classificacao': Classificacao,
            'classe_terapeutica': Classe_Terapeutica,
            'sub_classe_terapeutica': Sub_Classe_Terapeutica,
            'principio_ativo': Principio_Ativo,

            'from': from_,
            'excluded': False,
            'product_name': Apresentacao_Do_Produto,
            }

        if orizon_lpm_id != []:
            found += 1
            orizon_lpm_id = orizon_lpm_id[0]
            clv_orizon_lpm.write(orizon_lpm_id, values)

        else:
            not_found += 1
            orizon_lpm_id = clv_orizon_lpm.create(values).id

        if Sub_Classificacao != 'N/D':
            values = {
                'sub_classificacao': Sub_Classificacao,
                }
            clv_orizon_lpm.write(orizon_lpm_id, values)

        if Descricao != None:
            values = {
                'descricao': Descricao,
                }
            clv_orizon_lpm.write(orizon_lpm_id, values)

        rownum += 1

    f.close()

    clv_orizon_lpm = client.model('clv_orizon_lpm')
    orizon_lpm_browse = clv_orizon_lpm.browse([('excluded', '=', False),
                                               ('from', '!=', from_),
                                               ])
    excluded = 0
    for orizon_lpm in orizon_lpm_browse:
        excluded += 1

        print(excluded, orizon_lpm.cod_prod)

        values = {
            'excluded': True,
            }
        clv_orizon_lpm.write(orizon_lpm.id, values)

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> excluded: ', excluded)

def get_orizon_lpm_list_id(client, list_name):

    clv_orizon_lpm_list = client.model('clv_orizon_lpm.list')
    orizon_lpm_list_browse = clv_orizon_lpm_list.browse([('name', '=', list_name),])
    orizon_lpm_list_id = orizon_lpm_list_browse.id

    if orizon_lpm_list_id == []:
        values = {
            'name': list_name,
            }
        orizon_lpm_list_id = clv_orizon_lpm_list.create(values).id
    else:
        orizon_lpm_list_id = orizon_lpm_list_id[0]

    return orizon_lpm_list_id

def clv_orizon_lpm_list_import_new(client, file_name, list_name, previous_list_name):

    list_id = get_orizon_lpm_list_id(client, list_name)
    previous_list_id = False
    if previous_list_name != False:
        previous_list_id = get_orizon_lpm_list_id(client, previous_list_name)

    delimiter_char = ';'

    f  = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    orizon_lpm_found = 0
    orizon_lpm_not_found = 0
    orizon_lpm_included = 0
    ct = False
    for row in r:

        if rownum == 0:
            if row[7] == 'CLASSE TERAPÊUTICA':
                ct = True
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Laboratorio = row[i.next()]
        Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        EAN_Principal = row[i.next()]
        # Vazio = row[i.next()]
        PMC = row[i.next()].replace(",", ".")
        Desconto = row[i.next()].replace(",", ".")
        Preco_Venda = row[i.next()].replace(",", ".")
        Categoria = row[i.next()]
        Sub_Categoria = row[i.next()]
        Classificacao = row[i.next()]
        Sub_Classificacao = row[i.next()]
        Descricao = row[i.next()]
        Classe_Terapeutica = row[i.next()]
        Sub_Classe_Terapeutica = row[i.next()]
        Principio_Ativo = row[i.next()]

        print(rownum, Cod_Prod)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse([('cod_prod', '=', Cod_Prod),])
        orizon_lpm_id = orizon_lpm_browse.id

        if orizon_lpm_id != []:
            orizon_lpm_found += 1
            orizon_lpm_id = orizon_lpm_id[0]
            orizon_lpm_from = orizon_lpm_browse.read('from')[0]

            clv_orizon_lpm_list_item = client.model('clv_orizon_lpm.list.item')
            orizon_lpm_list_item_browse = \
                clv_orizon_lpm_list_item.browse([('list_id', '=', previous_list_id),
                                                 ('medicament_id', '=', orizon_lpm_id),
                                                 ])
            previous_list_item_id = orizon_lpm_list_item_browse.id

            included = False
            if previous_list_item_id == []:
                orizon_lpm_included += 1
                included = True

            print('>>>>>', orizon_lpm_found, orizon_lpm_from, list_name, included)

            values = {
                'list_id': list_id,
                'medicament_id': orizon_lpm_id,
                'order': rownum,
                'pmc': PMC,
                'desconto': Desconto,
                'preco_venda': Preco_Venda,
                'included': included,
                }
            orizon_lpm_list_item = clv_orizon_lpm_list_item.create(values)
        else:
            orizon_lpm_not_found += 1

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)
    print('orizon_lpm_found: ', orizon_lpm_found)
    print('orizon_lpm_not_found: ', orizon_lpm_not_found)
    print('orizon_lpm_included: ', orizon_lpm_included)

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

    print('--> clv_orizon_lpm.py...')

    client = erppeek.Client(server, dbname, username, password)

    # file_name = '/opt/openerp/orizon_lpm/LPM_1509.csv'
    # from_ = 'LPM_1509'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_orizon_lpm_import_new()...')
    # clv_orizon_lpm_import_new(client, file_name, from_)

    # list_name = 'LPM_1509'
    # previous_list_name = 'LPM_1508'
    # file_name = '/opt/openerp/orizon_lpm/LPM_1509.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_orizon_lpm_list_import_new(client, file_name, list_name, previous_list_name)

    # file_name = '/opt/openerp/orizon_lpm/LPM_1510.csv'
    # from_ = 'LPM_1510'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_orizon_lpm_import_new()...')
    # clv_orizon_lpm_import_new(client, file_name, from_)

    # list_name = 'LPM_1510'
    # previous_list_name = 'LPM_1509'
    # file_name = '/opt/openerp/orizon_lpm/LPM_1510.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_orizon_lpm_list_import_new(client, file_name, list_name, previous_list_name)

    print('--> clv_orizon_lpm.py')
    print('--> Execution time:', secondsToStr(time() - start))
