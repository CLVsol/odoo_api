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

    # server = 'http://localhost:8069'
    server = 'http://192.168.25.112:8069'

    # username = 'username'
    username = '*'
    # paswword = 'paswword' 
    paswword = '*' 

    dbname = 'odoo'
    # dbname = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> res_users.py...')

    client = erppeek.Client(server, dbname, username, password)

    # file_path = 'data/jcafb_res_users.csv'
    # print('-->', client, file_path)
    # print('--> Executing res_users_export()...')
    # res_users_export(client, file_path)

    print('--> res_users.py')
    print('--> Execution time:', secondsToStr(time() - start))
