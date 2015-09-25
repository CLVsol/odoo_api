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

def clv_medicament_list_updt_medicament_orizon(client, list_name, list_version_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name),])
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
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name),])
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

    print('--> clv_medicament_list.py...')

    client = erppeek.Client(server, dbname, username, password)

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

    print('--> clv_medicament_list.py')
    print('--> Execution time:', secondsToStr(time() - start))
