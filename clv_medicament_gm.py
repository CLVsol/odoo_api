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

from base import *
import argparse
import getpass


def clv_medicament_updt_clv_medicament_gs(client):

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse([])

    clv_medicament_gm = client.model('clv_medicament_gm')

    i = 0
    found = 0
    for medicament in medicament_browse:
        i += 1
        print(i, medicament.name.encode('utf-8'))

        if medicament.gm_id is not False:
            found += 1

            cod_prod_fabricante = medicament.gm_id.cod_prod_fabricante

            medicament_gm_browse = clv_medicament_gm.browse([('cod_prod_fabricante', '=', cod_prod_fabricante), ])
            medicament_gm_id = medicament_gm_browse[0].id

            print('>>>>>', medicament_gm_id)

            values = {
                'medicament_gm_id': medicament_gm_id,
                }
            clv_medicament.write(medicament.id, values)

    print('i: ', i)
    print('found: ', found)


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

    print('--> clv_medicament_gs.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_medicament_updt_clv_medicament_gs()...')
    # clv_medicament_updt_clv_medicament_gs(client)

    print('--> clv_medicament_gs.py')
    print('--> Execution time:', secondsToStr(time() - start))
