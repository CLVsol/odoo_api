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

from clv_patient import *

def clv_patient_unlink(client, args):

    clv_patient = client.model('clv_patient')
    patient_browse = clv_patient.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for patient in patient_browse:
        i += 1
        print(i, patient.name.encode("utf-8"))

        history = client.model('clv_patient.history')
        history_browse = history.browse([('patient_id', '=', patient.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_patient.unlink(patient.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)

def get_patient_category_id(client, patient_category_name, patient_category_code='/'):

    clv_patient_category = client.model('clv_patient.category')
    patient_category_browse = clv_patient_category.browse(\
        [('name', '=', patient_category_name),])
    patient_category_id = patient_category_browse.id

    if patient_category_id == []:
        values = {
            "name": patient_category_name,
            "code": patient_category_code,
            }
        patient_category_id = clv_patient_category.create(values).id
    else:
        patient_category_id = patient_category_id[0]

    return patient_category_id

def clv_patient_import_remote(remote_client, local_client):

    local_clv_person = local_client.model('clv_person')
    local_clv_patient = local_client.model('clv_patient')

    remote_clv_patient = remote_client.model('clv_patient')
    remote_patient_browse = remote_clv_patient.browse([])

    patient_count = 0
    for patient in remote_patient_browse:
        patient_count += 1

        local_person = local_clv_person.browse([('code', '=', patient.person.code),])[0]

        print(patient_count, patient.code, patient.name.encode("utf-8"), 
                             patient.tag_ids, patient.category_ids)

        values = {
            'person': local_person.id,
            'patient_code': patient.patient_code,
            'patient_date_inclusion': patient.patient_date_inclusion,
            }
        local_patient_id = local_clv_patient.create(values).id

        for category in patient.category_ids:
            patient_cat_id = get_patient_category_id(client, category.name, category.code)
            values = {
                'category_ids': [(4, patient_cat_id)],
                }
            local_clv_patient.write(local_patient_id, values)

    print('patient_count: ', patient_count)

def get_arguments():

    global username
    global password
    global dbname

    global remote_username
    global remote_password
    global remote_dbname

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', action="store", dest="username")
    parser.add_argument('--pw', action="store", dest="password")
    parser.add_argument('--db', action="store", dest="dbname")

    parser.add_argument('--ruser', action="store", dest="remote_username")
    parser.add_argument('--rpw', action="store", dest="remote_password")
    parser.add_argument('--rdb', action="store", dest="remote_dbname")

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

    if args.remote_dbname != None:
        remote_dbname = args.remote_dbname
    elif remote_dbname == '*':
        remote_dbname = raw_input('remote_dbname: ')

    if args.remote_username != None:
        remote_username = args.remote_username
    elif remote_username == '*':
        remote_username = raw_input('remote_username: ')

    if args.remote_password != None:
        remote_password = args.remote_password
    elif remote_password == '*':
        remote_password = getpass.getpass('remote_password: ')

if __name__ == '__main__':

    server = 'http://localhost:8069'

    # username = 'username'
    username = '*'
    # paswword = 'paswword' 
    paswword = '*' 

    dbname = 'odoo'
    # dbname = '*'

    remote_server = 'http://192.168.25.105:8069'

    # remote_username = 'username'
    remote_username = '*'
    # remote_password = 'paswword' 
    remote_password = '*' 

    remote_dbname = 'odoo'
    # remote_dbname = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_patient.py...')

    client = erppeek.Client(server, dbname, username, password)
    remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # patient_args = []
    # print('-->', client, patient_args)
    # print('--> Executing clv_patient_unlink("new")...')
    # clv_patient_unlink(client, patient_args)

    # print('-->', remote_client, client)
    # print('--> Executing clv_patient_import_remote()...')
    # clv_patient_import_remote(remote_client, client)

    print('--> clv_patient.py')
    print('--> Execution time:', secondsToStr(time() - start))
