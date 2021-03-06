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

def get_medicament_group_member_id(client, medicament_group_id, medicament_id, level=9):

    clv_medicament_group_member = client.model('clv_medicament_group_member')
    medicament_group_member_browse = clv_medicament_group_member.browse([('group_id', '=', medicament_group_id),
                                                                         ('medicament_id', '=', medicament_id),
                                                                         ])
    medicament_group_member_id = medicament_group_member_browse.id

    if medicament_group_member_id == []:
        values = {
            'group_id': medicament_group_id,
            'medicament_id': medicament_id,
            'level': level,
            'order': 10,
            'active': 1,
            }
        medicament_group_member_id = clv_medicament_group_member.create(values).id
    else:
        medicament_group_member_id = medicament_group_member_id[0]

    return medicament_group_member_id

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

    print('--> clv_medicament_group_member.py...')

    print('--> clv_medicament_group_member.py')
    print('--> Execution time:', secondsToStr(time() - start))
