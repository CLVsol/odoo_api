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

def clv_medicament_dispensation_updt_medicament_ref_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(\
        [('medicament_ref', '=', False),
         ('dispensation_ext_id', '!=', False),
         ])

    i = 0
    found = 0
    not_found = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.medicament_code)

        clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
        dispensation_ext_browse = clv_medicament_dispensation_ext.browse(\
            [('id', '=', dispensation.dispensation_ext_id.id),])
        dispensation_ext_id = dispensation_ext_browse.id

        if dispensation_ext_id != []:
            found += 1

            values = {
                'medicament_ref': 'clv_orizon_lpm,' + \
                                  str(dispensation_ext_browse.medicament_ref[0].id),
                }
            clv_medicament_dispensation.write(dispensation.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)

def clv_medicament_dispensation_updt_refund_price_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(\
        [('at_sight_value', '!=', 0.0),
         ('refund_price', '!=', 0.0),
         ])

    i = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.at_sight_value, dispensation.refund_price)

        values = {
            'refund_price': 0.0,
            }
        clv_medicament_dispensation.write(dispensation.id, values)

    print('i: ', i)

def clv_medicament_dispensation_import_dispensation_ext_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse(\
        [('dispensation_id', '=', False),
         ('pharmacy_id', '!=', False),
         ('prescriber_id', '!=', False),
         ('insured_card_id', '!=', False),
         ('medicament', '!=', False),
         ('dispensation_date', '!=', False),
         ], order='name')

    i = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.dispensation_date)

        values = {
            'name': '/',
            'dispensation_date': dispensation_ext.dispensation_date,
            'medicament': dispensation_ext.medicament.id,
            'max_retail_price': 0.0,
            'pack_quantity': dispensation_ext.pack_quantity,
            'refund_price': 0.0,
            'sale_value': dispensation_ext.sale_value,
            'at_sight_value': dispensation_ext.at_sight_value,
            'insured_card_id': dispensation_ext.insured_card_id.id,
            'prescriber_id': dispensation_ext.prescriber_id.id,
            'pharmacy_id': dispensation_ext.pharmacy_id.id,
            'dispenser': False,
            'medicament_ref': 'clv_orizon_lpm,' + \
                              str(dispensation_ext.medicament_ref.id),
            'dispensation_ext_id': dispensation_ext.id,
            }
        medicament_dispensation_id = clv_medicament_dispensation.create(values)

        values = {
            'dispensation_id': medicament_dispensation_id.id,
            }
        clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

    print('i: ', i)

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

    print('--> clv_medicament_dispensation.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price_orizon()...')
    # clv_medicament_dispensation_updt_refund_price_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    print('--> clv_medicament_dispensation.py')
    print('--> Execution time:', secondsToStr(time() - start))
