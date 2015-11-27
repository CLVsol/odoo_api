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

from erppeek import *
import csv
from filedict import *

from base import *
import argparse
import getpass


def export_medicament_list_id_from_mericament_ref_code_orizon(client, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item.id,
              medicament_list_item.medicament_ref.id,
              medicament_list_item.medicament_ref.cod_prod,
              medicament_list_item.medicament_ref.name.encode("utf-8"))

        d[medicament_list_item.medicament_ref.cod_prod] = [medicament_list_item.id]

        print('>>>>>', medicament_list_item.medicament_ref.cod_prod,
              d[medicament_list_item.medicament_ref.cod_prod])

    print('--> i: ', i)


def clv_medicament_list_updt_medicament_orizon(client, list_name, list_version_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ('medicament_id', '=', False),
         ])

    i = 0
    found = 0
    not_found = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        if medicament_list_item.medicament_ref != False:
            clv_medicament = client.model('clv_medicament')
            medicament_browse = clv_medicament.browse(\
                [('orizon_lpm_id', '=', medicament_list_item.medicament_ref.id),])
            print('>>>>>', medicament_browse)

            if medicament_browse.id != []:
                found += 1
                values = {
                    'medicament_id': medicament_browse[0].id,
                    }
                clv_medicament_list_item.write(medicament_list_item.id, values)
            else:
                not_found += 1
        else:
            not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_medicament_list_clear_subsidy_orizon(client, list_name, list_version_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ('subsidy', '!=', 0.0),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        values = {
            'subsidy': 0.0,
            }
        clv_medicament_list_item.write(medicament_list_item.id, values)

    print('--> i: ', i)


def clv_medicament_list_set_subsidy_orizon(client, infile_name, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    delimiter_char = ';'

    f = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        cod_prod = row[i.next()]
        medicament = row[i.next()]
        discount = row[i.next()]
        preco_venda = row[i.next()].replace(",", ".")
        Subsidio = row[i.next()]

        print(rownum, cod_prod, medicament)

        clv_medicament_list = client.model('clv_medicament_list')
        medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
        print('>>>>>', medicament_list_browse)

        clv_medicament_list_version = client.model('clv_medicament_list.version')
        medicament_list_version_browse = clv_medicament_list_version.browse(
            [('list_id', '=', medicament_list_browse[0].id),
             ('name', '=', list_version_name),
             ])
        print('>>>>>', medicament_list_version_browse)

        clv_medicament_list_item = client.model('clv_medicament_list.item')

        print('>>>>>', cod_prod, d[int(cod_prod)])
        try:
            medicament_list_item_id = d[int(cod_prod)]
        except:
            medicament_list_item_id = []

        if medicament_list_item_id != []:
            found += 1
            values = {
                'subsidy': 100.0,
                }
            clv_medicament_list_item.write(medicament_list_item_id[0], values)
        else:
            not_found += 1

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_medicament_list_clear_old_from(client, list_name, list_version_name, from_):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id), ])

    i = 0
    unlinked = 0
    not_unlinked = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse([('id', '=', medicament_list_item.medicament_ref.id),
                                                   ('from', '!=', from_),
                                                   ])
        print('>>>>>', orizon_lpm_browse)

        if orizon_lpm_browse.id != []:
            unlinked += 1
            medicament_list_item.unlink()
        else:
            not_unlinked += 1

    print('--> i: ', i)
    print('--> unlinked: ', unlinked)
    print('--> not_unlinked: ', not_unlinked)


def clv_medicament_list_check_orizon(client, infile_name, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    delimiter_char = ';'

    f = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    ok = 0
    not_ok = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Reembolso = row[i.next()]
        if Reembolso == '1':
            Reembolso = '100.0'
        Laboratorio = row[i.next()]
        Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        EAN_Principal = row[i.next()]
        PMC = row[i.next()].replace(",", ".")
        Desconto = row[i.next()].replace(",", ".")
        Preco_Venda = row[i.next()].replace(",", ".")
        Categoria = row[i.next()]
        Sub_Categoria = row[i.next()]
        Classificacao = row[i.next()]
        Sub_Classificacao = row[i.next()]
        Classe_Terapeutica = row[i.next()]
        Sub_Classe_Terapeutica = row[i.next()]
        Principio_Ativo = row[i.next()]

        print(rownum, Cod_Prod, Apresentacao_Do_Produto)

        clv_medicament_list_item = client.model('clv_medicament_list.item')

        print('>>>>>', Cod_Prod, d[int(Cod_Prod)])
        try:
            medicament_list_item_id = d[int(Cod_Prod)]
        except:
            medicament_list_item_id = []

        if medicament_list_item_id != []:
            found += 1
            medicament_list_item = clv_medicament_list_item.browse(
                [('id', '=', medicament_list_item_id[0]), ])[0]
            print('>>>>>>>>>>', medicament_list_item, medicament_list_item.subsidy, Reembolso,
                  medicament_list_item.discount, Desconto)
            if medicament_list_item.subsidy == float(Reembolso) and \
               medicament_list_item.discount == float(Desconto):
                ok += 1
            else:
                not_ok += 1
        else:
            not_found += 1

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> ok: ', ok)
    print('--> not_ok: ', not_ok)


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

    print('--> clv_medicament_list.py...')

    client = erppeek.Client(server, dbname, username, password)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, list_name, list_version_name, list_id_filename)
    # print('--> Executing export_medicament_list_id_from_mericament_ref_code_orizon()...')
    # export_medicament_list_id_from_mericament_ref_code_orizon(client, list_name, list_version_name, list_id_filename)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon()...')
    # clv_medicament_list_updt_medicament_orizon(client, list_name, list_version_name)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_clear_subsidy_orizon()...')
    # clv_medicament_list_clear_subsidy_orizon(client, list_name, list_version_name)

    # infile_name = '/opt/openerp/orizon_lpm/Lista_483_0_5k_LPM_1508.csv'
    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, infile_name, list_name, list_version_name, list_id_filename)
    # print('--> Executing clv_medicament_list_set_subsidy_orizon()...')
    # clv_medicament_list_set_subsidy_orizon(client, infile_name, list_name, list_version_name, list_id_filename)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # from_ = 'LPM_1509'
    # print('-->', client, list_name, list_version_name, from_)
    # print('--> Executing clv_medicament_list_clear_old_from()...')
    # clv_medicament_list_clear_old_from(client, list_name, list_version_name, from_)

    # infile_name = '/opt/openerp/orizon_lpm/Lista_483_LPM_Agosto_2015.csv'
    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, infile_name, list_name, list_version_name, list_id_filename)
    # print('--> Executing clv_medicament_list_check_orizon()...')
    # clv_medicament_list_check_orizon(client, infile_name, list_name, list_version_name, list_id_filename)

    print('--> clv_medicament_list.py')
    print('--> Execution time:', secondsToStr(time() - start))
