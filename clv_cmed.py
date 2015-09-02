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

def clv_cmed_import_new(client, infile_name, from_):

    delimiter_char = ';'

    f  = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        PRINCIPIO_ATIVO = row[i.next()]
        CNPJ = row[i.next()]
        LABORATORIO = row[i.next()]
        CODIGO_GGREM = row[i.next()]
        EAN = row[i.next()]
        PRODUTO = row[i.next()]
        APRESENTACAO = row[i.next()]
        CLASSE_TERAPEUTICA = row[i.next()]
        PF_0 = row[i.next()].replace(",", ".")
        if PF_0 == 'Liberado':
            PF_0 = ""
        PF_12 = row[i.next()].replace(",", ".")
        PF_17 = row[i.next()].replace(",", ".")
        PF_18 = row[i.next()].replace(",", ".")
        PF_19 = row[i.next()].replace(",", ".")
        PF_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(",", ".")
        PMC_0 = row[i.next()].replace(",", ".")
        PMC_12 = row[i.next()].replace(",", ".")
        PMC_17 = row[i.next()].replace(",", ".")
        PMC_18 = row[i.next()].replace(",", ".")
        PMC_19 = row[i.next()].replace(",", ".")
        PMC_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(",", ".")
        RESTRICAO_HOSPITALAR = row[i.next()]
        CAP = row[i.next()]
        CONFAZ_87 = row[i.next()]
        ANALISE_RECURSAL = row[i.next()]

        print(rownum, CODIGO_GGREM, from_, PRODUTO, APRESENTACAO)

        clv_cmed = client.model('clv_cmed')
        cmed_browse = clv_cmed.browse([('codigo_ggrem', '=', CODIGO_GGREM),])
        cmed_id = cmed_browse.id

        values = {
            'principio_ativo': PRINCIPIO_ATIVO,
            'cnpj': CNPJ,
            'latoratorio': LABORATORIO,
            'codigo_ggrem': CODIGO_GGREM,
            'ean': EAN,
            'produto': PRODUTO,
            'apresentacao': APRESENTACAO,
            'classe_terapeutica': CLASSE_TERAPEUTICA,
            'pf_0': PF_0,
            'pf_12': PF_12,
            'pf_17': PF_17,
            'pf_18': PF_18,
            'pf_19': PF_19,
            'pf_17_zfm': PF_17_ZONA_FRANCA_DE_MANAUS,
            'pmc_0': PMC_0,
            'pmc_12': PMC_12,
            'pmc_17': PMC_17,
            'pmc_18': PMC_18,
            'pmc_19': PMC_19,
            'pmc_17_zfm': PMC_17_ZONA_FRANCA_DE_MANAUS,
            'restr_hospitalar': RESTRICAO_HOSPITALAR,
            'cap': CAP,
            'confaz_87': CONFAZ_87,
            'analise_recursal': ANALISE_RECURSAL,

            'from': from_,
            'excluded': False,
            'product_name': PRODUTO + ' ' + APRESENTACAO,
            }

        if cmed_id != []:
            found += 1
            cmed_id = cmed_id[0]
            clv_cmed.write(cmed_id, values)

        else:
            not_found += 1
            cmed_id = clv_cmed.create(values)

        rownum += 1

    clv_cmed = client.model('clv_cmed')
    cmed_browse = clv_cmed.browse([('excluded', '=', False),
                                   ('from', '!=', from_),])
    excluded = 0
    for cmed in cmed_browse:
        excluded += 1

        print(excluded, cmed.name)

        values = {
                'excluded': True,
                }
        clv_cmed.write(cmed.id, values)

    f.close()

    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> excluded: ', excluded)

def get_arguments():

    global admin_pw
    global admin_user_pw
    global data_admin_user_pw
    global username
    global password
    global dbname
    global infile_name
    global from_

    parser = argparse.ArgumentParser()
    # parser.add_argument('--admin_pw', action="store", dest="admin_pw")
    # parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
    # parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    parser.add_argument('--infile', action="store", dest="infile_name")
    parser.add_argument('--from', action="store", dest="from_")

    args = parser.parse_args()
    print('%s%s' % ('--> ', args))

    # if args.admin_pw != None:
    #     admin_pw = args.admin_pw
    # elif admin_pw == '*':
    #     admin_pw = getpass.getpass('admin_pw: ')

    # if args.admin_user_pw != None:
    #     admin_user_pw = args.admin_user_pw
    # elif admin_user_pw == '*':
    #     admin_user_pw = getpass.getpass('admin_user_pw: ')

    # if args.data_admin_user_pw != None:
    #     data_admin_user_pw = args.data_admin_user_pw
    # elif data_admin_user_pw == '*':
    #     data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

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

    if args.infile_name != None:
        infile_name = args.infile_name
    elif infile_name == '*':
        infile_name = raw_input('infile_name: ')

    if args.from_ != None:
        from_ = args.from_
    elif from_ == '*':
        from_ = raw_input('from_: ')

if __name__ == '__main__':

    server = 'http://localhost:8069'
    admin = 'admin'
    admin_pw = 'admin'
    # admin_pw = '*'

    admin_user = 'admin'
    admin_user_pw = 'admin' 
    # admin_user_pw = '*' 

    data_admin_user = 'data.admin'
    data_admin_user_pw = 'data.admin' 
    # data_admin_user_pw = '*' 

    # username = 'username'
    username = '*'
    # paswword = 'paswword' 
    paswword = '*' 

    dbname = 'odoo'
    # dbname = '*'

    # infile_name = '/opt/openerp/cmed/CMED_2015_08_21.csv'
    infile_name = '*'
    # from_ = 'CMED_2015_08_21'
    from_ = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_cmed.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('-->', client, infile_name, from_)
    print('--> Executing clv_cmed_import_new()...')
    clv_cmed_import_new(client, infile_name, from_)

    print('--> clv_cmed.py')
    print('--> Execution time:', secondsToStr(time() - start))
