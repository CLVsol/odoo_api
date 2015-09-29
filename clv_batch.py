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

def get_batch_id(client, batch_name, category_id=False, origin_batch_ids=False):

    clv_batch = client.model('clv_batch')
    batch_browse = clv_batch.browse([('name', '=', batch_name),])
    batch_id = batch_browse.id

    if batch_id == []:
        values = {
            "name": batch_name,
            "code": '/',
            "category_id": category_id,
            "origin_batch_ids": origin_batch_ids,
            }
        batch_id = clv_batch.create(values).id
    else:
        batch_id = batch_id[0]

    return batch_id

def get_batch_category_id(client, batch_category_name):

    clv_batch_category = client.model('clv_batch.category')
    batch_category_browse = clv_batch_category.browse([('name', '=', batch_category_name),])
    batch_category_id = batch_category_browse.id

    if batch_category_id == []:
        values = {
            "name": batch_category_name,
            "code": '/',
            }
        batch_category_id = clv_batch.create(values).id
    else:
        batch_category_id = batch_category_id[0]

    return batch_category_id

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

    print('--> clv_batch.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('--> clv_batch.py')
    print('--> Execution time:', secondsToStr(time() - start))
