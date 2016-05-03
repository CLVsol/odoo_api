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

from base import *
import argparse
import getpass

from clv_insurance_client import *


def get_insured_category_id(client, category_name):

    clv_insured_category = client.model('clv_insured.category')
    insured_category_browse = clv_insured_category.browse([('name', '=', category_name),])
    insured_category_id = insured_category_browse.id

    if insured_category_id == []:
        values = {
            'name': category_name,
            }
        insured_category_id = clv_insured_category.create(values).id
    else:
        insured_category_id = insured_category_id[0]

    return insured_category_id


def clv_insured_export_VCAS(client, file_path, date_inclusion):

    clv_insurance_client = client.model('clv_insurance_client')
    insurance_client_browse = clv_insurance_client.browse(\
        [('name', '=', 'VCAS - Vera Cruz Associação de Saúde'),])
    client_id_VCAS = insurance_client_browse[0].id

    headings_insured = ['no', 
                        'name', 'code',
                        'birthday', 'gender',
                        'insured_category',
                        'insurance_client', 'reg_number',
                        'insurance', 
                        'state',
                        'date_activation',
                         ]
    file_insured = open(file_path, 'wb')
    writer_insured = csv.writer(file_insured, delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL)
    writer_insured.writerow(headings_insured)

    clv_insured = client.model('clv_insured')
    insured_browse = clv_insured.browse([('state', '!=', 'canceled'),
                                         ('date_inclusion', '<=', date_inclusion),
                                         ('insurance_client_id', '=', client_id_VCAS),])

    i = 0
    for insured in insured_browse:
        i += 1

        name = insured.name.encode("utf-8")
        code = insured.code
        birthday = insured.birthday
        gender = insured.gender
        insured_category = insured.category_ids[0].name.encode("utf-8")
        insurance_client = insured.insurance_client_id.name.encode("utf-8")
        reg_number = insured.reg_number
        insurance = insured.insurance_id.name.encode("utf-8")
        state = insured.state
        date_inclusion = insured.date_inclusion

        print(i, insured.name.encode("utf-8"))
        row_insured = [i, 
                       name, code,
                       birthday, gender,
                       insured_category,
                       insurance_client, reg_number,
                       insurance,
                       state,
                       date_inclusion,
                       ]
        writer_insured.writerow(row_insured)

    file_insured.close()

    print('i: ', i)


def clv_insured_export_HVC(client, file_path, date_inclusion):

    clv_insurance_client = client.model('clv_insurance_client')
    insurance_client_browse = clv_insurance_client.browse(\
        [('name', '=', 'HVC - Hospital Vera Cruz'),])
    client_id_HVC = insurance_client_browse[0].id

    headings_insured = ['no', 
                        'name', 'code',
                        'birthday', 'gender',
                        'insured_category',
                        'insurance_client', 'reg_number',
                        'insurance', 
                        'state',
                        'date_activation',
                         ]
    file_insured = open(file_path, 'wb')
    writer_insured = csv.writer(file_insured, delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL)
    writer_insured.writerow(headings_insured)

    clv_insured = client.model('clv_insured')
    insured_browse = clv_insured.browse([('state', '!=', 'canceled'),
                                         ('date_inclusion', '<=', date_inclusion),
                                         ('insurance_client_id', '=', client_id_HVC),])

    i = 0
    for insured in insured_browse:
        i += 1

        name = insured.name.encode("utf-8")
        code = insured.code
        birthday = insured.birthday
        gender = insured.gender
        insured_category = insured.category_ids[0].name.encode("utf-8")
        insurance_client = insured.insurance_client_id.name.encode("utf-8")
        reg_number = insured.reg_number
        insurance = insured.insurance_id.name.encode("utf-8")
        state = insured.state
        date_inclusion = insured.date_inclusion

        print(i, insured.name.encode("utf-8"))
        row_insured = [i, 
                       name, code,
                       birthday, gender,
                       insured_category,
                       insurance_client, reg_number,
                       insurance,
                       state,
                       date_inclusion,
                       ]
        writer_insured.writerow(row_insured)

    file_insured.close()

    print('i: ', i)


def clv_insured_export_RMC(client, file_path, date_inclusion):

    clv_insurance_client = client.model('clv_insurance_client')
    insurance_client_browse = clv_insurance_client.browse(
        [('name', '=', 'RMC - Ressonância Magnética Campinas'), ])
    client_id_RMC = insurance_client_browse[0].id

    headings_insured = ['no',
                        'name', 'code',
                        'birthday', 'gender',
                        'insured_category',
                        'insurance_client', 'reg_number',
                        'insurance',
                        'state',
                        'date_activation',
                        ]
    file_insured = open(file_path, 'wb')
    writer_insured = csv.writer(file_insured, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_insured.writerow(headings_insured)

    clv_insured = client.model('clv_insured')
    insured_browse = clv_insured.browse([('state', '!=', 'canceled'),
                                         ('date_inclusion', '<=', date_inclusion),
                                         ('insurance_client_id', '=', client_id_RMC), ])

    i = 0
    for insured in insured_browse:
        i += 1

        name = insured.name.encode("utf-8")
        code = insured.code
        birthday = insured.birthday
        gender = insured.gender
        insured_category = insured.category_ids[0].name.encode("utf-8")
        insurance_client = insured.insurance_client_id.name.encode("utf-8")
        reg_number = insured.reg_number
        insurance = insured.insurance_id.name.encode("utf-8")
        state = insured.state
        date_inclusion = insured.date_inclusion

        print(i, insured.name.encode("utf-8"))
        row_insured = [i,
                       name, code,
                       birthday, gender,
                       insured_category,
                       insurance_client, reg_number,
                       insurance,
                       state,
                       date_inclusion,
                       ]
        writer_insured.writerow(row_insured)

    file_insured.close()

    print('i: ', i)


def clv_insured_updt_reg_number(client, client_name):

    insurance_client_id = get_insurance_client_id(client, client_name)

    clv_insured = client.model('clv_insured')
    insured_browse = clv_insured.browse([('insurance_client_id', '=', insurance_client_id), ])

    insured_count = 0
    for insured in insured_browse:
        insured_count += 1

        reg_number = insured.reg_number

        print(insured_count, reg_number, insured.name.encode("utf-8"))

        if reg_number[0] == '0':
            while reg_number[0] == '0':
                reg_number = reg_number[1:]

            print('>>>>>', reg_number)

            values = {
                "reg_number": reg_number,
                }
            clv_insured.write(insured.id, values)

    print('insured_count: ', insured_count)


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

    print('--> clv_insured.py...')

    client = erppeek.Client(server, dbname, username, password)

    # file_path = '/opt/openerp/biobox/data/insured_2015_09_30.csv'
    # print('-->', client, file_path)
    # print('--> Executing clv_insured_export()...')
    # clv_insured_export(client, file_path)

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2015_10_31.csv'
    # date_inclusion = '2015-10-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2015_10_31.csv'
    # date_inclusion = '2015-10-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2015_11_30.csv'
    # date_inclusion = '2015-11-30'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2015_11_30.csv'
    # date_inclusion = '2015-11-30'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    ##########################################

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2015_12_31.csv'
    # date_inclusion = '2015-12-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2015_12_31.csv'
    # date_inclusion = '2015-12-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    ##########################################

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2016_01_31.csv'
    # date_inclusion = '2016-01-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2016_01_31.csv'
    # date_inclusion = '2016-01-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    ##########################################

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2016_02_29.csv'
    # date_inclusion = '2016-02-29'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2016-02-29.csv'
    # date_inclusion = '2016-02-29'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    # 2016-04-02 #########################################

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2016_03_31.csv'
    # date_inclusion = '2016-03-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2016-03-31.csv'
    # date_inclusion = '2016-03-31'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    # 2016-05-03 #########################################

    # file_path = '/opt/openerp/biobox/data/insured_VCAS_2016_04_30.csv'
    # date_inclusion = '2016-04-30'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_VCAS()...')
    # clv_insured_export_VCAS(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_HVC_2016_04_30.csv'
    # date_inclusion = '2016-04-30'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_HVC()...')
    # clv_insured_export_HVC(client, file_path, date_inclusion)

    # file_path = '/opt/openerp/biobox/data/insured_RMC_2016_04_30.csv'
    # date_inclusion = '2016-04-30'
    # print('-->', client, file_path, date_inclusion)
    # print('--> Executing clv_insured_export_RMC()...')
    # clv_insured_export_RMC(client, file_path, date_inclusion)

    print('--> clv_insured.py')
    print('--> Execution time:', secondsToStr(time() - start))
