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

import clv_tag

def clv_cmed_import_new(client, infile_name, from_):

    delimiter_char = ';'

    f  = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    ct = False
    for row in r:

        if rownum == 0:
            if row[7] == 'CLASSE TERAPÊUTICA':
                ct = True
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
        if ct:
            CLASSE_TERAPEUTICA = row[i.next()]
        else:
            CLASSE_TERAPEUTICA = False
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

        print(rownum, CODIGO_GGREM, from_)

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

        print(excluded, cmed.codigo_ggrem)

        values = {
            'excluded': True,
            }
        clv_cmed.write(cmed.id, values)

    f.close()

    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> excluded: ', excluded)

def clv_cmed_check_ean(client):

    tag_id_EAN_replicado = \
        clv_tag.get_tag_id(client, 'EAN replicado', 'Registro com o código EAN replicado.')

    print('>>>>>', tag_id_EAN_replicado)


    clv_cmed = client.model('clv_cmed')
    cmed_browse = clv_cmed.browse([])
    i = 0
    found = 0
    not_found = 0
    for cmed in cmed_browse:
        i += 1
        print(i, cmed.codigo_ggrem)

        ean_cmed_ids = clv_cmed.browse([('ean', '=', cmed.ean),]).id

        if len(ean_cmed_ids) > 1:
            found += 1
            print('>>>>>', ean_cmed_ids)
            values = {
                'tag_ids': [(4, tag_id_EAN_replicado)],
                }
            clv_cmed.write(cmed.id, values)
        else:
            not_found += 1
            values = {
                'tag_ids': [(3, tag_id_EAN_replicado)],
                }
            clv_cmed.write(cmed.id, values)

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not found: ', not_found)

def clv_cmed_updt_manufacturer(client):

    clv_cmed = client.model('clv_cmed')
    cmed_browse = clv_cmed.browse([('state', '=', 'new'), 
                                   ('manufacturer', '=', False),
                                   ])

    i = 0
    found = 0
    not_found = 0
    for cmed in cmed_browse:
        i += 1

        print(i, cmed.codigo_ggrem, cmed.latoratorio.encode("utf-8"))

        clv_medicament_manufacturer_str = client.model('clv_medicament.manufacturer.str')
        manufacturer_str_browse = clv_medicament_manufacturer_str.browse([('name', '=', cmed.latoratorio),])
        manufacturer_str_id = manufacturer_str_browse.id

        if manufacturer_str_id != []:

            manufacturer_id = manufacturer_str_browse.manufacturer_id.id

            if manufacturer_id != [False]:
                found += 1
                print('>>>>>', manufacturer_str_id, manufacturer_id)
                
                values = {
                    'manufacturer': manufacturer_id[0],
                    }
                clv_cmed.write(cmed.id, values)
            else:
                not_found += 1
        else:
            not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not found: ', not_found)

def clv_cmed_updt_active_component(client):

    clv_cmed = client.model('clv_cmed')
    cmed_browse = clv_cmed.browse([('state', '=', 'new'), 
                                   ('active_component', '=', False),
                                   ])

    i = 0
    found = 0
    not_found = 0
    for cmed in cmed_browse:
        i += 1

        print(i, cmed.codigo_ggrem, cmed.principio_ativo.encode("utf-8"))

        clv_medicament_active_component_str = \
            client.model('clv_medicament.active_component.str')
        active_component_str_browse = \
            clv_medicament_active_component_str.browse([('name', '=', cmed.principio_ativo),])
        active_component_str_id = active_component_str_browse.id

        if active_component_str_id != []:

            active_component_id = active_component_str_browse.active_component_id.id

            if active_component_id != [False]:
                found += 1

                print('>>>>>', active_component_str_id, active_component_id)
                
                values = {
                    'active_component': active_component_id[0],
                    }
                clv_cmed.write(cmed.id, values)
            else:
                not_found += 1
        else:
            not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not found: ', not_found)

def get_cmed_list_id(client, list_name):

    clv_cmed_list = client.model('clv_cmed.list')
    cmed_list_browse = clv_cmed_list.browse([('name', '=', list_name),])
    cmed_list_id = cmed_list_browse.id

    if cmed_list_id == []:
        values = {
            'name': list_name,
            }
        cmed_list_id = clv_cmed_list.create(values).id
    else:
        cmed_list_id = cmed_list_id[0]

    return cmed_list_id

def clv_cmed_list_import_new(client, file_name, list_name, previous_list_name):

    list_id = get_cmed_list_id(client, list_name)
    previous_list_id = False
    if previous_list_name != False:
        previous_list_id = get_cmed_list_id(client, previous_list_name)

    delimiter_char = ';'

    f  = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    cmed_found = 0
    cmed_not_found = 0
    cmed_included = 0
    ct = False
    for row in r:

        if rownum == 0:
            if row[7] == 'CLASSE TERAPÊUTICA':
                ct = True
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
        if ct:
            CLASSE_TERAPEUTICA = row[i.next()]
        else:
            CLASSE_TERAPEUTICA = False
        PF_0 = row[i.next()].replace(",", ".")
        if PF_0 == 'Liberado':
            PF_0 = ""
        PF_12 = row[i.next()].replace(".", "").replace(",", ".")
        PF_17 = row[i.next()].replace(".", "").replace(",", ".")
        PF_18 = row[i.next()].replace(".", "").replace(",", ".")
        PF_19 = row[i.next()].replace(".", "").replace(",", ".")
        PF_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(".", "").replace(",", ".")
        PMC_0 = row[i.next()].replace(".", "").replace(",", ".")
        PMC_12 = row[i.next()].replace(".", "").replace(",", ".")
        PMC_17 = row[i.next()].replace(".", "").replace(",", ".")
        PMC_18 = row[i.next()].replace(".", "").replace(",", ".")
        PMC_19 = row[i.next()].replace(".", "").replace(",", ".")
        PMC_17_ZONA_FRANCA_DE_MANAUS = row[i.next()].replace(".", "").replace(",", ".")
        RESTRICAO_HOSPITALAR = row[i.next()]
        CAP = row[i.next()]
        CONFAZ_87 = row[i.next()]
        ANALISE_RECURSAL = row[i.next()]

        print(rownum, CODIGO_GGREM)

        clv_cmed = client.model('clv_cmed')
        cmed_browse = clv_cmed.browse([('codigo_ggrem', '=', CODIGO_GGREM),])
        cmed_id = cmed_browse.id

        if cmed_id != []:
            cmed_found += 1
            cmed_id = cmed_id[0]
            cmed_from = cmed_browse.read('from')[0]

            clv_cmed_list_item = client.model('clv_cmed.list.item')
            cmed_list_item_browse = \
                clv_cmed_list_item.browse([('list_id', '=', previous_list_id),
                                           ('medicament_id', '=', cmed_id),
                                           ])
            previous_list_item_id = cmed_list_item_browse.id

            included = False
            if previous_list_item_id == []:
                cmed_included += 1
                included = True

            print('>>>>>', cmed_found, cmed_from, list_name, included)

            values = {
                'list_id': list_id,
                'medicament_id': cmed_id,
                'order': rownum,
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
                'included': included,
                }
            cmed_list_item = clv_cmed_list_item.create(values)
        else:
            cmed_not_found += 1

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)
    print('cmed_found: ', cmed_found)
    print('cmed_not_found: ', cmed_not_found)
    print('cmed_included: ', cmed_included)

def get_arguments():

    global admin_pw
    global admin_user_pw
    global data_admin_user_pw
    global username
    global password
    global dbname
    # global infile_name
    # global from_

    parser = argparse.ArgumentParser()
    # parser.add_argument('--admin_pw', action="store", dest="admin_pw")
    # parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
    # parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    # parser.add_argument('--infile', action="store", dest="infile_name")
    # parser.add_argument('--from', action="store", dest="from_")

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

    # if args.infile_name != None:
    #     infile_name = args.infile_name
    # elif infile_name == '*':
    #     infile_name = raw_input('infile_name: ')

    # if args.from_ != None:
    #     from_ = args.from_
    # elif from_ == '*':
    #     from_ = raw_input('from_: ')

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

    # infile_name = '*'
    # from_ = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_cmed.py...')

    client = erppeek.Client(server, dbname, username, password)

    # infile_name = '/opt/openerp/cmed/CMED_2015_08_21.csv'
    # from_ = 'CMED_2015_08_21'
    # print('-->', client, infile_name, from_)
    # print('--> Executing clv_cmed_import_new()...')
    # clv_cmed_import_new(client, infile_name, from_)

    # print('-->', client)
    # print('--> Executing clv_cmed_check_ean()...')
    # clv_cmed_check_ean(client)

    # print('-->', client)
    # print('--> Executing clv_cmed_updt_manufacturer()...')
    # clv_cmed_updt_manufacturer(client)

    # print('-->', client)
    # print('--> Executing clv_cmed_updt_active_component()...')
    # clv_cmed_updt_active_component(client)

    # list_name = 'CMED_2014_01_08'
    # previous_list_name = False
    # file_name = '/opt/openerp/cmed/CMED_2014_01_08.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_02_20'
    # previous_list_name = 'CMED_2014_01_08'
    # file_name = '/opt/openerp/cmed/CMED_2014_02_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_03_18'
    # previous_list_name = 'CMED_2014_02_20'
    # file_name = '/opt/openerp/cmed/CMED_2014_03_18.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_04_22'
    # previous_list_name = 'CMED_2014_03_18'
    # file_name = '/opt/openerp/cmed/CMED_2014_04_22.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_05_20'
    # previous_list_name = 'CMED_2014_04_22'
    # file_name = '/opt/openerp/cmed/CMED_2014_05_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_06_18'
    # previous_list_name = 'CMED_2014_05_20'
    # file_name = '/opt/openerp/cmed/CMED_2014_06_18.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_07_30'
    # previous_list_name = 'CMED_2014_06_18'
    # file_name = '/opt/openerp/cmed/CMED_2014_07_30.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_08_20'
    # previous_list_name = 'CMED_2014_07_30'
    # file_name = '/opt/openerp/cmed/CMED_2014_08_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_09_22'
    # previous_list_name = 'CMED_2014_08_20'
    # file_name = '/opt/openerp/cmed/CMED_2014_09_22.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_10_20'
    # previous_list_name = 'CMED_2014_09_22'
    # file_name = '/opt/openerp/cmed/CMED_2014_10_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_11_20'
    # previous_list_name = 'CMED_2014_10_20'
    # file_name = '/opt/openerp/cmed/CMED_2014_11_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2014_12_22'
    # previous_list_name = 'CMED_2014_11_20'
    # file_name = '/opt/openerp/cmed/CMED_2014_12_22.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_01_20'
    # previous_list_name = 'CMED_2014_12_22'
    # file_name = '/opt/openerp/cmed/CMED_2015_01_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_02_20'
    # previous_list_name = 'CMED_2015_01_20'
    # file_name = '/opt/openerp/cmed/CMED_2015_02_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_03_30'
    # previous_list_name = 'CMED_2015_02_20'
    # file_name = '/opt/openerp/cmed/CMED_2015_03_30.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_04_14'
    # previous_list_name = 'CMED_2015_03_30'
    # file_name = '/opt/openerp/cmed/CMED_2015_04_14.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_05_14'
    # previous_list_name = 'CMED_2015_04_14'
    # file_name = '/opt/openerp/cmed/CMED_2015_05_14.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_06_22'
    # previous_list_name = 'CMED_2015_05_14'
    # file_name = '/opt/openerp/cmed/CMED_2015_06_22.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_07_20'
    # previous_list_name = 'CMED_2015_06_22'
    # file_name = '/opt/openerp/cmed/CMED_2015_07_20.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'CMED_2015_08_21'
    # previous_list_name = 'CMED_2015_07_20'
    # file_name = '/opt/openerp/cmed/CMED_2015_08_21.csv'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_cmed_list_import_new(client, file_name, list_name, previous_list_name)

    print('--> clv_cmed.py')
    print('--> Execution time:', secondsToStr(time() - start))
