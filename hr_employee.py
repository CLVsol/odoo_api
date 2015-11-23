#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol                 #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from __future__ import print_function

from erppeek import *
# import csv

from base import *
import argparse
import getpass


def hr_employee_updt_from_res_users_updt_jcafb(client):

    res_users = client.model('res.users')
    res_users_browse = res_users.browse([])

    hr_employee = client.model('hr.employee')

    i = 0
    found = 0
    not_found = 0
    for user in res_users_browse:
        i += 1
        print(i, user.name.encode("utf-8"), user.login, user.email)
        if user.login == user.email:
            found += 1
            values = {
                'name': user.name,
                'work_email': user.email,
                'work_phone': user.phone,
                'mobile_phone': user.mobile,
                'user_id': user.id,
                }
            employee_id = hr_employee.create(values).id
            print('>>>>>', employee_id)
        else:
            not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def hr_employee_updt_code(client):

    hr_employee = client.model('hr.employee')
    hr_employee_browse = hr_employee.browse([])

    i = 0
    for employee in hr_employee_browse:
        i += 1
        print(i, employee.name.encode("utf-8"), employee.user_id.login, employee.user_id.email)
        values = {
            "code": '/',
            }
        hr_employee.write(employee.id, values)

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

    print('--> hr_employee.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing hr_employee_updt_from_res_users_updt_jcafb()...')
    # hr_employee_updt_from_res_users_updt_jcafb(client)

    # print('-->', client)
    # print('--> Executing hr_employee_updt_code()...')
    # hr_employee_updt_code(client)

    print('--> hr_employee.py')
    print('--> Execution time:', secondsToStr(time() - start))
