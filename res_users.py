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

def res_users_export(client, file_path):

    headings_res_users = ['no', 'user_id',
                          'name', 'login', 'password_crypt', 'email',
                          'phone', 'mobile',
                           ]
    file_res_users = open(file_path, 'wb')
    writer_res_users = csv.writer(file_res_users, delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL)
    writer_res_users.writerow(headings_res_users)

    res_users = client.model('res.users')
    res_users_browse = res_users.browse([])

    i = 0
    found = 0
    not_found = 0
    for user in res_users_browse:
        i += 1

        user_id = user.id
        name = user.name.encode("utf-8")
        login = user.login
        password_crypt = user.password_crypt
        email = user.email
        phone = user.phone
        mobile = user.mobile

        print(i, user_id, name, login, password_crypt, email,
                 phone, mobile)

        row_res_users = [i, user_id,
                         name, login, password_crypt, email,
                         phone, mobile
                         ]
        writer_res_users.writerow(row_res_users)

    file_res_users.close()

    print('--> i: ', i)

def res_users_import_remote(remote_client, local_client):

    local_res_users = local_client.model('res.users')

    remote_res_users = remote_client.model('res.users')
    remote_users_browse = remote_res_users.browse([])

    user_count = 0
    created = 0
    for user in remote_users_browse:
        user_count += 1

        print(user_count, user.login, user.name.encode("utf-8"), 
                          user.email)

        user_id = local_res_users.browse([('login', '=', user.login),]).id

        if user_id == []:
            values = {
                'name': user.name,
                'login': user.login,
                'password_crypt': user.password_crypt,
                'email': user.email,
                'phone': user.phone,
                'email': user.email,
                'mobile': user.mobile,
                }
            user_id = local_res_users.create(values).id
            created += 1
        else:
            user_id = user_id[0]

    print('user_count: ', user_count)
    print('created: ', created)

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

    print('--> res_users.py...')

    client = erppeek.Client(server, dbname, username, password)
    remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # file_path = 'data/jcafb_res_users.csv'
    # print('-->', client, file_path)
    # print('--> Executing res_users_export()...')
    # res_users_export(client, file_path)

    print('-->', remote_client, client)
    print('--> Executing res_users_import_remote()...')
    res_users_import_remote(remote_client, client)

    print('--> res_users.py')
    print('--> Execution time:', secondsToStr(time() - start))
