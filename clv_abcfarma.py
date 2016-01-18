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
from dbfpy import dbf

from base import *
import argparse
import getpass


def clv_abcfarma_import_new(client, file_name, from_):

    db = dbf.Dbf(file_name)

    names = []
    for field in db.header.fields:
        names.append(field.name)
    print(names)

    rownum = 0
    found = 0
    not_found = 0
    for rec in db:

        if rownum == 0:
            rownum += 1

        row = rec.fieldData

        i = autoIncrement(0, 1)

        MED_ABC = row[i.next()]
        MED_CTR = row[i.next()]
        MED_LAB = row[i.next()]
        LAB_NOM = row[i.next()]
        MED_DES = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_APR = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_PCO18 = row[i.next()]
        MED_PLA18 = row[i.next()]
        MED_FRA18 = row[i.next()]
        MED_PCO17 = row[i.next()]
        MED_PLA17 = row[i.next()]
        MED_FRA17 = row[i.next()]
        MED_PCO12 = row[i.next()]
        MED_PLA12 = row[i.next()]
        MED_FRA12 = row[i.next()]
        MED_UNI = row[i.next()]
        MED_IPI = row[i.next()]
        MED_DTVIG = row[i.next()]
        EXP_13 = row[i.next()]
        MED_BARRA = row[i.next()]
        MED_GENE = row[i.next()]
        MED_NEGPOS = row[i.next()]
        MED_PRINCI = row[i.next()]
        MED_PCO19 = row[i.next()]
        MED_PLA19 = row[i.next()]
        MED_FRA19 = row[i.next()]
        MED_PCOZFM = row[i.next()]
        MED_PLAZFM = row[i.next()]
        MED_FRAZFM = row[i.next()]
        MED_PCO0 = row[i.next()]
        MED_PLA0 = row[i.next()]
        MED_FRA0 = row[i.next()]
        MED_REGIMS = row[i.next()]
        MED_VARPRE = row[i.next()]

        print(rownum, MED_ABC, MED_DES, MED_APR)

        clv_abcfarma = client.model('clv_abcfarma')
        abcfarma_browse = clv_abcfarma.browse([('med_abc', '=', MED_ABC),])
        abcfarma_id = abcfarma_browse.id

        values = {
            'med_abc': MED_ABC,
            'med_ctr': MED_CTR,
            'med_lab': MED_LAB,
            'lab_nom': LAB_NOM,
            'med_des': MED_DES,
            'med_apr': MED_APR,
            'med_pco18': MED_PCO18,
            'med_pla18': MED_PLA18,
            'med_fra18': MED_FRA18,
            'med_pco17': MED_PCO17,
            'med_pla17': MED_PLA17,
            'med_fra17': MED_FRA17,
            'med_pco12': MED_PCO12,
            'med_pla12': MED_PLA12,
            'med_fra12': MED_FRA12,
            'med_uni': MED_UNI,
            'med_ipi': MED_IPI,
            'med_dtvig': str(MED_DTVIG),
            'exp_13': EXP_13,
            'med_barra': str(MED_BARRA),
            'med_negpos': MED_NEGPOS,
            'med_pco19': MED_PCO19,
            'med_pla19': MED_PLA19,
            'med_fra19': MED_FRA19,
            'med_pcozfm': MED_PCOZFM,
            'med_plazfm': MED_PLAZFM,
            'med_frazfm': MED_FRAZFM,
            'med_pco0': MED_PCO0,
            'med_pla0': MED_PLA0,
            'med_fra0': MED_FRA0,
            
            'med_gene': MED_GENE,
            'med_princi': MED_PRINCI,
            'med_regims': MED_REGIMS,
            'med_varpre': MED_VARPRE,

            'from': from_,
            'excluded': False,
            'product_name': MED_DES + ' ' + MED_APR,
            }

        if abcfarma_id != []:
            found += 1
            abcfarma_id = abcfarma_id[0]
            clv_abcfarma.write(abcfarma_id, values)

        else:
            not_found += 1
            abcfarma_id = clv_abcfarma.create(values)

        rownum += 1

    clv_abcfarma = client.model('clv_abcfarma')
    abcfarma_browse = clv_abcfarma.browse([('excluded', '=', False),
                                           ('from', '!=', from_),])
    excluded = 0
    for abcfarma in abcfarma_browse:
        excluded += 1

        print(excluded, abcfarma.codigo_ggrem)

        values = {
            'excluded': True,
            }
        clv_abcfarma.write(abcfarma.id, values)

    # f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> excluded: ', excluded)


def get_abcfarma_list_id(client, list_name):

    clv_abcfarma_list = client.model('clv_abcfarma.list')
    abcfarma_list_browse = clv_abcfarma_list.browse([('name', '=', list_name),])
    abcfarma_list_id = abcfarma_list_browse.id

    if abcfarma_list_id == []:
        values = {
            'name': list_name,
            }
        abcfarma_list_id = clv_abcfarma_list.create(values).id
    else:
        abcfarma_list_id = abcfarma_list_id[0]

    return abcfarma_list_id


def clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name):

    list_id = get_abcfarma_list_id(client, list_name)
    previous_list_id = False
    if previous_list_name is not False:
        previous_list_id = get_abcfarma_list_id(client, previous_list_name)

    db = dbf.Dbf(file_name)

    names = []
    for field in db.header.fields:
        names.append(field.name)
    print(names)

    rownum = 0
    abcfarma_found = 0
    abcfarma_not_found = 0
    abcfarma_included = 0
    for rec in db:

        if rownum == 0:
            rownum += 1

        row = rec.fieldData

        i = autoIncrement(0, 1)

        MED_ABC = row[i.next()]
        MED_CTR = row[i.next()]
        MED_LAB = row[i.next()]
        LAB_NOM = row[i.next()]
        MED_DES = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_APR = row[i.next()].decode('ISO 8859-1').encode('utf-8')
        MED_PCO18 = row[i.next()]
        MED_PLA18 = row[i.next()]
        MED_FRA18 = row[i.next()]
        MED_PCO17 = row[i.next()]
        MED_PLA17 = row[i.next()]
        MED_FRA17 = row[i.next()]
        MED_PCO12 = row[i.next()]
        MED_PLA12 = row[i.next()]
        MED_FRA12 = row[i.next()]
        MED_UNI = row[i.next()]
        MED_IPI = row[i.next()]
        MED_DTVIG = row[i.next()]
        EXP_13 = row[i.next()]
        MED_BARRA = row[i.next()]
        MED_GENE = row[i.next()]
        MED_NEGPOS = row[i.next()]
        MED_PRINCI = row[i.next()]
        MED_PCO19 = row[i.next()]
        MED_PLA19 = row[i.next()]
        MED_FRA19 = row[i.next()]
        MED_PCOZFM = row[i.next()]
        MED_PLAZFM = row[i.next()]
        MED_FRAZFM = row[i.next()]
        MED_PCO0 = row[i.next()]
        MED_PLA0 = row[i.next()]
        MED_FRA0 = row[i.next()]
        MED_REGIMS = row[i.next()]
        MED_VARPRE = row[i.next()]

        print(rownum, MED_ABC, MED_DES, MED_APR)

        clv_abcfarma = client.model('clv_abcfarma')
        abcfarma_browse = clv_abcfarma.browse([('med_abc', '=', MED_ABC), ])
        abcfarma_id = abcfarma_browse.id

        if abcfarma_id != []:
            abcfarma_found += 1
            abcfarma_id = abcfarma_id[0]
            abcfarma_from = abcfarma_browse.read('from')[0]

            clv_abcfarma_list_item = client.model('clv_abcfarma.list.item')
            abcfarma_list_item_browse = \
                clv_abcfarma_list_item.browse([('list_id', '=', previous_list_id),
                                               ('medicament_id', '=', abcfarma_id),
                                               ])
            previous_list_item_id = abcfarma_list_item_browse.id

            included = False
            if previous_list_item_id == []:
                abcfarma_included += 1
                included = True

            print('>>>>>', abcfarma_found, abcfarma_from, list_name, included)

            values = {
                'list_id': list_id,
                'medicament_id': abcfarma_id,
                'order': rownum,
                'med_pco18': MED_PCO18,
                'med_pla18': MED_PLA18,
                'med_fra18': MED_FRA18,
                'med_pco17': MED_PCO17,
                'med_pla17': MED_PLA17,
                'med_fra17': MED_FRA17,
                'med_pco12': MED_PCO12,
                'med_pla12': MED_PLA12,
                'med_fra12': MED_FRA12,
                'med_pco19': MED_PCO19,
                'med_pla19': MED_PLA19,
                'med_fra19': MED_FRA19,
                'med_pcozfm': MED_PCOZFM,
                'med_plazfm': MED_PLAZFM,
                'med_frazfm': MED_FRAZFM,
                'med_pco0': MED_PCO0,
                'med_pla0': MED_PLA0,
                'med_fra0': MED_FRA0,
                'included': included,
                }
            abcfarma_list_item = clv_abcfarma_list_item.create(values)
        else:
            abcfarma_not_found += 1

        rownum += 1

    # f.close()

    print('rownum: ', rownum - 1)
    print('abcfarma_found: ', abcfarma_found)
    print('abcfarma_not_found: ', abcfarma_not_found)
    print('abcfarma_included: ', abcfarma_included)


def get_arguments():

    global username
    global password
    global dbname
    # global file_name
    # global from_

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    # parser.add_argument('--infile', action="store", dest="file_name")
    # parser.add_argument('--from', action="store", dest="from_")

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

    # if args.file_name != None:
    #     file_name = args.file_name
    # elif file_name == '*':
    #     file_name = raw_input('file_name: ')

    # if args.from_ != None:
    #     from_ = args.from_
    # elif from_ == '*':
    #     from_ = raw_input('from_: ')


if __name__ == '__main__':

    server = 'http://localhost:8069'

    # username = 'username'
    username = '*'
    # paswword = 'paswword'
    paswword = '*'

    dbname = 'odoo'
    # dbname = '*'

    # file_name = '*'
    # from_ = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_abcfarma.py...')

    client = erppeek.Client(server, dbname, username, password)

    # file_name = '/opt/openerp/abcfarma/TABELA_2015_09.dbf'
    # from_ = 'TABELA_2015_09'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_abcfarma_import_new()...')
    # clv_abcfarma_import_new(client, file_name, from_)

    # file_name = '/opt/openerp/abcfarma/TABELA_2015_10.dbf'
    # from_ = 'TABELA_2015_10'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_abcfarma_import_new()...')
    # clv_abcfarma_import_new(client, file_name, from_)

    # file_name = '/opt/openerp/abcfarma/TABELA_2015_11.dbf'
    # from_ = 'TABELA_2015_11'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_abcfarma_import_new()...')
    # clv_abcfarma_import_new(client, file_name, from_)

    # file_name = '/opt/openerp/abcfarma/TABELA_2015_12.dbf'
    # from_ = 'TABELA_2015_12'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_abcfarma_import_new()...')
    # clv_abcfarma_import_new(client, file_name, from_)

    # list_name = 'TABELA_2014_01'
    # previous_list_name = False
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_01.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_02'
    # previous_list_name = 'TABELA_2014_01'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_02.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_03'
    # previous_list_name = 'TABELA_2014_02'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_03.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_04'
    # previous_list_name = 'TABELA_2014_03'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_04.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_05'
    # previous_list_name = 'TABELA_2014_04'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_05.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_06'
    # previous_list_name = 'TABELA_2014_05'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_06.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_07'
    # previous_list_name = 'TABELA_2014_06'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_07.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_08'
    # previous_list_name = 'TABELA_2014_07'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_08.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_09'
    # previous_list_name = 'TABELA_2014_08'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_09.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_10'
    # previous_list_name = 'TABELA_2014_09'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_10.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_11'
    # previous_list_name = 'TABELA_2014_10'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_11.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2014_12'
    # previous_list_name = 'TABELA_2014_11'
    # file_name = '/opt/openerp/abcfarma/TABELA_2014_12.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_01'
    # previous_list_name = 'TABELA_2014_12'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_01.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_02'
    # previous_list_name = 'TABELA_2015_01'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_02.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_03'
    # previous_list_name = 'TABELA_2015_02'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_03.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_04'
    # previous_list_name = 'TABELA_2015_03'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_04.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_05'
    # previous_list_name = 'TABELA_2015_04'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_05.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_06'
    # previous_list_name = 'TABELA_2015_05'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_06.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_07'
    # previous_list_name = 'TABELA_2015_06'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_07.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_08'
    # previous_list_name = 'TABELA_2015_07'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_08.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_09'
    # previous_list_name = 'TABELA_2015_08'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_09.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_10'
    # previous_list_name = 'TABELA_2015_09'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_10.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_11'
    # previous_list_name = 'TABELA_2015_10'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_11.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    # list_name = 'TABELA_2015_12'
    # previous_list_name = 'TABELA_2015_11'
    # file_name = '/opt/openerp/abcfarma/TABELA_2015_12.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    ##################################

    # file_name = '/opt/openerp/abcfarma/TABELA_2016_01.dbf'
    # from_ = 'TABELA_2016_01'
    # print('-->', client, file_name, from_)
    # print('--> Executing clv_abcfarma_import_new()...')
    # clv_abcfarma_import_new(client, file_name, from_)

    # list_name = 'TABELA_2016_01'
    # previous_list_name = 'TABELA_2015_12'
    # file_name = '/opt/openerp/abcfarma/TABELA_2016_01.dbf'
    # print('-->', client, file_name, list_name, previous_list_name)
    # clv_abcfarma_list_import_new(client, file_name, list_name, previous_list_name)

    print('--> clv_abcfarma.py')
    print('--> Execution time:', secondsToStr(time() - start))
