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

def clv_insured_card_include_partner_orizon(client):

    res_partner = client.model('res.partner')
    res_partner_browse = res_partner.browse([('name', '=', 'Orizon'),])
    res_partner_id = res_partner_browse.id[0]

    clv_insured_card = client.model('clv_insured_card')
    insured_card_browse = clv_insured_card.browse([('orizon', '=', True),])

    i = 0
    for insured_card in insured_card_browse:
        i += 1

        print(i, insured_card.code, insured_card.name)

        values = {
            'partner_ids': [(4, res_partner_id)],
            }
        clv_insured_card.write(insured_card.id, values)

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

    print('--> clv_insured_card.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('-->', client)
    print('--> Executing clv_insured_card_include_partner_orizon()...')
    clv_insured_card_include_partner_orizon(client)

    print('--> clv_insured_card.py')
    print('--> Execution time:', secondsToStr(time() - start))
