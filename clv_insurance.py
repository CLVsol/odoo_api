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

from base import *
import argparse
import getpass


def get_insurance_id(client, insurance_name):

    clv_insurance = client.model('clv_insurance')
    insurance_browse = clv_insurance.browse([('name', '=', insurance_name), ])
    insurance_id = insurance_browse.id

    if insurance_id == []:
        values = {
            'name': insurance_name,
        }
        insurance_id = clv_insurance.create(values).id
    else:
        insurance_id = insurance_id[0]

    return insurance_id


def clv_insurance_unlink(client, args):

    clv_insurance = client.model('clv_insurance')
    insurance_browse = clv_insurance.browse(args)

    i = 0
    for insurance in insurance_browse:
        i += 1
        print(i, insurance.name)

        history = client.model('clv_insurance.history')
        history_browse = history.browse([('insurance_id', '=', insurance.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_insurance.unlink(insurance.id)

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

    print('--> clv_insurance.py...')

    client = erppeek.Client(server, dbname, username, password)

    # insurance_args = [('state', '=', 'canceled'), ]
    # print('-->', client, insurance_args)
    # print('--> Executing clv_insurance_unlink()...')
    # clv_insurance_unlink(client, insurance_args)

    print('--> clv_insurance.py')
    print('--> Execution time:', secondsToStr(time() - start))
