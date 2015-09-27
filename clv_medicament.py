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

from clv_medicament_group import *
from clv_medicament_group_member import *

def get_new_l0_medicament_active_component(client, active_component_id, concentration, pres_form, pres_form_2):

    new_medicament_id = 0

    clv_active_component = client.model('clv_medicament.active_component')
    active_component_browse = clv_active_component.browse([('id', '=', active_component_id),])

    clv_medicament_form = client.model('clv_medicament.form')
    medicament_form_browse = clv_medicament_form.browse([('id', '=', pres_form),])
    medicament_form_2_browse = clv_medicament_form.browse([('id', '=', pres_form_2),])

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse([('medicament_name', '=', active_component_browse.name[0]),
                                               ('active_component', '=', active_component_id),
                                               ('concentration', '=', concentration),
                                               # ('pres_form', '=', pres_form),
                                               ('pres_form_2', '=', pres_form_2),
                                               ('is_product', '=', 0),
                                               ])
    if medicament_browse.id == []:

        name = active_component_browse.name[0] + ' (' + active_component_browse.name[0] + ') ' + \
               concentration + ' ' + medicament_form_2_browse.name[0]

        print('>>>>>', '(new medicament)', name)

        values = {
            'name': name,
            'medicament_name': active_component_browse.name[0],
            'presentation': False,
            'code': False,
            'active_component': active_component_id,
            'concentration': concentration,
            'pres_form': medicament_form_browse.id[0],
            'pres_form_2': medicament_form_2_browse.id[0],
            'is_product': 0,
            'active': 1,
            }
        new_medicament_id = clv_medicament.create(values).id

    return new_medicament_id

def get_new_l0_medicament_name(client, medicament_name, active_component_id, concentration, pres_form, pres_form_2):

    new_medicament_id = 0

    clv_active_component = client.model('clv_medicament.active_component')
    active_component_browse = clv_active_component.browse([('id', '=', active_component_id),])

    clv_medicament_form = client.model('clv_medicament.form')
    medicament_form_browse = clv_medicament_form.browse([('id', '=', pres_form),])
    medicament_form_2_browse = clv_medicament_form.browse([('id', '=', pres_form_2),])

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse([('medicament_name', '=', medicament_name),
                                               ('active_component', '=', active_component_id),
                                               ('concentration', '=', concentration),
                                               # ('pres_form', '=', pres_form),
                                               ('pres_form_2', '=', pres_form_2),
                                               ('is_product', '=', 0),
                                               ])
    if medicament_browse.id == []:

        name = medicament_name + ' (' + active_component_browse.name[0] + ') ' + \
               concentration + ' ' + medicament_form_2_browse.name[0]

        print('>>>>>', '(new medicament)', name)

        values = {
            'name': name,
            'medicament_name': medicament_name,
            'presentation': False,
            'code': False,
            'active_component': active_component_id,
            'concentration': concentration,
            'pres_form': medicament_form_browse.id[0],
            'pres_form_2': medicament_form_2_browse.id[0],
            'is_product': 0,
            'active': 1,
            }
        new_medicament_id = clv_medicament.create(values).id

    return new_medicament_id

def include_medicament_into_group(client, medicament):

    medicament_group_id = get_medicament_group_id(client, medicament.active_component.id, 
                                                          medicament.concentration, 
                                                          medicament.pres_form_2.id)

    print('>>>>>', medicament.code, medicament.name.encode("utf-8"), medicament_group_id)

    medicament_group_member_l9 = get_medicament_group_member_id(client, medicament_group_id, 
                                                                        medicament.id, 
                                                                        9)

    print('>>>>>', medicament_group_member_l9)

    new_medicament_id = get_new_l0_medicament_active_component(client, medicament.active_component.id, 
                                                                       medicament.concentration, 
                                                                       medicament.pres_form.id, 
                                                                       medicament.pres_form_2.id)
    medicament_group_member_l0 = False
    if new_medicament_id != 0:
        medicament_group_member_l0 = get_medicament_group_member_id(client, medicament_group_id, 
                                                                            new_medicament_id, 
                                                                            0)

    print('>>>>>', medicament_group_member_l0, medicament_group_member_l0)

    new_medicament_id = get_new_l0_medicament_name(client, medicament.medicament_name,
                                                           medicament.active_component.id, 
                                                           medicament.concentration, 
                                                           medicament.pres_form.id, 
                                                           medicament.pres_form_2.id)
    medicament_group_member_l0 = False
    if new_medicament_id != 0:
        medicament_group_member_l0 = get_medicament_group_member_id(client, medicament_group_id, 
                                                                            new_medicament_id, 
                                                                            0)

    print('>>>>>', medicament_group_member_l0, medicament_group_member_l0)

def include_medicaments_into_groups(client, args):

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse(args)

    medicament_count = 0
    for medicament in medicament_browse:

        medicament_count += 1
        print(medicament_count, medicament.name.encode("utf-8"))

        include_medicament_into_group(client, medicament)

    print('medicament_count: ', medicament_count)

def clv_medicament_updt_code(client, args):

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse(args)

    medicament_count = 0
    for medicament in medicament_browse:
        medicament_count += 1

        print(medicament_count, medicament.name)

        values = {
            'code': '/',
            }
        clv_medicament.write(medicament.id, values)

    print('medicament_count: ', medicament_count)

def clv_medicament_updt_state_active(client, args):

    clv_medicament = client.model('clv_medicament')
    medicament_browse = clv_medicament.browse(args)

    medicament_count = 0
    for medicament in medicament_browse:
        medicament_count += 1

        print(medicament_count, medicament.state, medicament.name)

        if medicament.state == 'new':
            client.exec_workflow('clv_medicament', 'button_revised', medicament.id)
            client.exec_workflow('clv_medicament', 'button_waiting', medicament.id)
            client.exec_workflow('clv_medicament', 'button_activate', medicament.id)

        if medicament.state == 'waiting':
            client.exec_workflow('clv_medicament', 'button_activate', medicament.id)

    print('medicament_count: ', medicament_count)

def clv_medicament_mark_verify_from_orizon_lpm(client):

    args = [('excluded', '=', False),
            ('medicament_ids', '!=', False),]
    clv_orizon_lpm = client.model('clv_orizon_lpm')
    orizon_lpm_browse = clv_orizon_lpm.browse(args)

    orizon_lpm_count = 0
    medicament_ok = 0
    medicament_to_verify = 0
    for orizon_lpm in orizon_lpm_browse:

        orizon_lpm_count += 1
        print(orizon_lpm_count, orizon_lpm.name.encode("utf-8"))

        clv_medicament = client.model('clv_medicament')
        medicament_browse = clv_medicament.browse([('id', '=', orizon_lpm.medicament_ids[0].id),
                                                   ('state', '!=', 'active'),
                                                   ('state', '!=', 'waiting'),
                                                   ])
        print('>>>>>', medicament_browse.id)

        if medicament_browse.id != []:
            medicament_to_verify += 1
        else:
            medicament_ok += 1

    print('orizon_lpm_count: ', orizon_lpm_count)
    print('medicament_to_verify: ', medicament_to_verify)
    print('medicament_ok: ', medicament_ok)

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

    print('--> clv_medicament.py...')

    client = erppeek.Client(server, dbname, username, password)

    # medicament_args = [('is_product', '=', True),
    #                    ('state', '=', 'waiting'),]
    # print('-->', client, medicament_args)
    # print('--> Executing include_medicaments_into_groups()...')
    # include_medicaments_into_groups(client, medicament_args)

    # medicament_args = [('code', '=', False),]
    # print('-->', client, medicament_args)
    # print('--> Executing clv_medicament_updt_code()...')
    # clv_medicament_updt_code(client, medicament_args)

    # medicament_args = [('state', '=', 'new'),
    #                    ('is_product', '=', False),]
    # print('-->', client, medicament_args)
    # print('--> Executing clv_medicament_updt_state_active()...')
    # clv_medicament_updt_state_active(client, medicament_args)

    # medicament_args = [('state', '=', 'waiting'),]
    # print('-->', client, medicament_args)
    # print('--> Executing clv_medicament_updt_state_active()...')
    # clv_medicament_updt_state_active(client, medicament_args)

    # print('-->', client)
    # print('--> Executing clv_medicament_mark_verify_from_orizon_lpm()...')
    # clv_medicament_mark_verify_from_orizon_lpm(client)

    print('--> clv_medicament.py')
    print('--> Execution time:', secondsToStr(time() - start))
