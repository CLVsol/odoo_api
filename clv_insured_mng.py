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

def clv_insured_mng_unlink(client, status):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([('state', '=', status),])

    i = 0
    for insured_mng in insured_mng_browse:
        i += 1
        print(i, insured_mng.name)

        history = client.model('clv_insured_mng.history')
        history_browse = history.browse([('insured_mng_id', '=', insured_mng.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_insured_mng.unlink(insured_mng.id)

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

    print('--> clv_insured_mng.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('-->', client)

    print('--> Executing clv_insured_mng_unlink("draft")...')
    clv_insured_mng_unlink(client, 'draft')

    print('--> Executing clv_insured_mng_unlink("revised")...')
    clv_insured_mng_unlink(client, 'revised')

    print('--> Executing clv_insured_mng_unlink("done")...')
    clv_insured_mng_unlink(client, 'done')

    print('--> Executing clv_insured_mng_unlink("canceled")...')
    clv_insured_mng_unlink(client, 'canceled')

    print('--> clv_insured_mng.py')
    print('--> Execution time:', secondsToStr(time() - start))
