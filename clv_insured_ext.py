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

def clv_insured_ext_unlink(client, status):

    clv_insured_ext = client.model('clv_insured_ext')
    insured_ext_browse = clv_insured_ext.browse([('state', '=', status),])

    i = 0
    for insured_ext in insured_ext_browse:
        i += 1
        print(i, insured_ext.name)

        history = client.model('clv_insured_ext.history')
        history_browse = history.browse([('insured_ext_id', '=', insured_ext.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_insured_ext.unlink(insured_ext.id)

    print('--> i: ', i)

def clv_insured_ext_import(client):

    clv_insured_ext = client.model('clv_insured_ext')

    clv_insured_card = client.model('clv_insured_card')
    insured_card_browse = clv_insured_card.browse([('orizon', '=', True),])
    i = 0
    synchronized = 0
    not_synchronized = 0
    for insured_card in insured_card_browse:
        i += 1

        print(i, insured_card.code, insured_card.orizon_synchronized, insured_card.state, insured_card.name)

        clv_insured = client.model('clv_insured')
        insured_browse = clv_insured.browse([('id', '=', insured_card.insured_id.id),])

        print('>>>>>', insured_browse.code, insured_browse.name)
        print('#####', insured_card.code, insured_card.name, insured_browse.birthday[0], 
                       insured_browse.gender[0], insured_browse.id[0], insured_card.id,
                       insured_browse.cpf[0])

        values = {
            'name': insured_card.name,
            'code': insured_card.code,
            'address_id': False,
            'birthday': insured_browse.birthday[0],
            'gender': insured_browse.gender[0],
            'insured_id': insured_browse.id[0],
            'insured_card_id': insured_card.id,
            'cpf': insured_browse.cpf[0],
            }

        insured_ext_id = clv_insured_ext.create(values).id

        print('xxxxx', insured_ext_id, insured_card.orizon_state)

        values = {
            'date_activation': insured_card.date_activation,
            'date_cancelation': insured_card.date_cancelation,
            }
        if insured_card.orizon_synchronized:
            synchronized += 1
            if insured_card.orizon_state == 'active':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_activate', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
            if insured_card.orizon_state == 'canceled':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_cancel', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
        else:
            not_synchronized += 1
            if insured_card.orizon_previous_state == 'active':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_activate', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
            if insured_card.orizon_previous_state == 'canceled':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_cancel', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)

        values = {
            'synchronized': insured_card.orizon_synchronized,
            'date_synchronization': insured_card.orizon_date_synchronization,
            'date_previous_synchronization': insured_card.orizon_date_previous_synchronization,
            }
        clv_insured_ext.write(insured_ext_id, values)

    print('--> i: ', i)
    print('--> synchronized: ', synchronized)
    print('--> not_synchronized: ', not_synchronized)

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

    print('--> clv_insured_ext.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('-->', client)

    print('--> Executing clv_insured_ext_unlink("new")...')
    clv_insured_ext_unlink(client, 'new')

    print('--> Executing clv_insured_ext_unlink("processing")...')
    clv_insured_ext_unlink(client, 'processing')

    print('--> Executing clv_insured_ext_unlink("active")...')
    clv_insured_ext_unlink(client, 'active')

    print('--> Executing clv_insured_ext_unlink("suspended")...')
    clv_insured_ext_unlink(client, 'suspended')

    print('--> Executing clv_insured_ext_unlink("canceled")...')
    clv_insured_ext_unlink(client, 'canceled')

    print('-->', client)
    print('--> Executing clv_insured_ext_import()...')
    clv_insured_ext_import(client)

    print('--> clv_insured_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))
