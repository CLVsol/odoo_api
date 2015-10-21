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

from clv_address import *

def clv_family_unlink(client, args):

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for family in family_browse:
        i += 1
        print(i, family.name.encode("utf-8"))

        history = client.model('clv_family.history')
        history_browse = history.browse([('family_id', '=', family.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_family.unlink(family.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)

def clv_family_import_remote(remote_client, local_client):

    clv_address = local_client.model('clv_address')
    local_clv_family = local_client.model('clv_family')

    remote_clv_family = remote_client.model('clv_family')
    remote_family_browse = remote_clv_family.browse([])

    family_count = 0
    address_count = 0
    for family in remote_family_browse:
        family_count += 1

        print(family_count, family.code, family.name.encode("utf-8"), 
                            family.tag_ids, family.category_ids)

        address_id = False
        if family.address_id != False:
            print('>>>>>', family.address_id.name.encode("utf-8"))
            if family.address_id.street != False:
                print('>>>>>>>>>>', family.address_id.street.encode("utf-8"), 
                                    family.address_id.number)
            if family.address_id.district != False:
                print('>>>>>>>>>>', family.address_id.district.encode("utf-8"))

            address_id = clv_address.browse([('name', '=', family.address_id.name),]).id

            if address_id == []:
                values = {
                    'name': family.address_id.name,
                    'street': family.address_id.street,
                    'number': family.address_id.number,
                    'district': family.address_id.district,
                    }
                address_id = clv_address.create(values).id
                address_count += 1
            else:
                address_id = address_id[0]

        values = {
            'name': family.name,
            'code': family.code,
            'address_id': address_id,
            'date_inclusion': family.date_inclusion,
            }
        local_family_id = local_clv_family.create(values).id

    print('family_count: ', family_count)
    print('address_count: ', address_count)

def get_arguments():

    global username
    global password
    global dbname

    global remote_username
    global remote_password
    global remote_dbname

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    parser.add_argument('--ruser', action="store", dest="remote_username")
    parser.add_argument('--rpw', action="store", dest="remote_password")
    parser.add_argument('--rdb', action="store", dest="remote_dbname")

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

    if args.remote_dbname != None:
        remote_dbname = args.remote_dbname
    elif remote_dbname == '*':
        remote_dbname = raw_input('remote_dbname: ')

    if args.remote_username != None:
        remote_username = args.remote_username
    elif remote_username == '*':
        remote_username = raw_input('remote_username: ')

    if args.remote_password != None:
        remote_password = args.remote_password
    elif remote_password == '*':
        remote_password = getpass.getpass('remote_password: ')

if __name__ == '__main__':

    server = 'http://localhost:8069'

    # username = 'username'
    username = '*'
    # paswword = 'paswword' 
    paswword = '*' 

    dbname = 'odoo'
    # dbname = '*'

    remote_server = 'http://192.168.25.105:8069'

    # remote_username = 'username'
    remote_username = '*'
    # remote_password = 'paswword' 
    remote_password = '*' 

    remote_dbname = 'odoo'
    # remote_dbname = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_family.py...')

    client = erppeek.Client(server, dbname, username, password)
    remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # family_args = []
    # print('-->', client, family_args)
    # print('--> Executing clv_family_unlink("new")...')
    # clv_family_unlink(client, family_args)

    # address_args = []
    # print('-->', client, address_args)
    # print('--> Executing clv_address_unlink("new")...')
    # clv_address_unlink(client, address_args)

    # print('-->', remote_client, client)
    # print('--> Executing clv_family_import_remote()...')
    # clv_family_import_remote(remote_client, client)

    print('--> clv_family.py')
    print('--> Execution time:', secondsToStr(time() - start))
