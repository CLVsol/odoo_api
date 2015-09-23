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

    print('-->', client)
    print('--> Executing clv_medicament_dispensation_updt_medicament_ref_orizon()...')
    clv_medicament_dispensation_updt_medicament_ref_orizon(client)

    print('--> clv_medicament_dispensation.py')
    print('--> Execution time:', secondsToStr(time() - start))
