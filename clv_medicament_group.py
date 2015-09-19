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

def get_medicament_group_id(client, active_component, concentration = False, pres_form = False):

    clv_medicament_group = client.model('clv_medicament_group')
    medicament_group_browse = clv_medicament_group.browse([('active_component', '=', active_component),
                                                           ('concentration', '=', concentration),
                                                           ('pres_form', '=', pres_form),])
    medicament_group_id = medicament_group_browse.id

    clv_active_component = client.model('clv_medicament.active_component')
    active_component_browse = clv_active_component.browse([('id', '=', active_component),])

    clv_medicament_form = client.model('clv_medicament.form')
    medicament_form_browse = clv_medicament_form.browse([('id', '=', pres_form),])

    if medicament_group_id == []:
        if pres_form != False:
            name = active_component_browse.name[0] + ' ' + concentration + ' (' + medicament_form_browse.name[0] + ')'
        else:
            name = active_component_browse.name[0] + ' ' + concentration
        values = {
            'name': name,
            'medicament_name': active_component_browse.name[0],
            'active_component': active_component_browse.id[0],
            'concentration': concentration,
            'pres_form': medicament_form_browse.id[0],
            'active': 1,
            }
        medicament_group_id = clv_medicament_group.create(values).id
    else:
        medicament_group_id = medicament_group_id[0]

    return medicament_group_id

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

    print('--> clv_medicament_group.py...')

    print('--> clv_medicament_group.py')
    print('--> Execution time:', secondsToStr(time() - start))
