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

from erppeek import *
# import csv
# import fileinput
# import re

from base import *
import argparse
import getpass

from clv_person import *
from clv_tag import *


def clv_person_mng_unlink(client, status):

    clv_person_mng = client.model('clv_person_mng')
    person_mng_browse = clv_person_mng.browse([('state', '=', status), ])

    i = 0
    for person_mng in person_mng_browse:
        i += 1
        print(i, person_mng.name)

        history = client.model('clv_person_mng.history')
        history_browse = history.browse([('person_mng_id', '=', person_mng.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_person_mng.unlink(person_mng.id)

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

    print('--> clv_person_mng.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("draft")...')
    # clv_person_mng_unlink(client, 'draft')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("revised")...')
    # clv_person_mng_unlink(client, 'revised')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("done")...')
    # clv_person_mng_unlink(client, 'done')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("canceled")...')
    # clv_person_mng_unlink(client, 'canceled')

    print('--> clv_person_mng.py')
    print('--> Execution time:', secondsToStr(time() - start))
