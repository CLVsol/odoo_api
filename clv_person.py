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

from clv_address import *

def clv_person_unlink(client, args):

    clv_person = client.model('clv_person')
    person_browse = clv_person.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for person in person_browse:
        i += 1
        print(i, person.name.encode("utf-8"))

        history = client.model('clv_person.history')
        history_browse = history.browse([('person_id', '=', person.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_person.unlink(person.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)

def clv_person_import_remote(remote_client, local_client):

    clv_address = local_client.model('clv_address')
    local_clv_person = local_client.model('clv_person')

    remote_clv_person = remote_client.model('clv_person')
    remote_person_browse = remote_clv_person.browse([])

    i = 0
    person_count = 0
    address_count = 0
    spouse_count = 0
    father_count = 0
    mother_count = 0
    responsible_count = 0
    for person in remote_person_browse:
        person_count += 1

        print(person_count, person.code, person.name.encode("utf-8"), person.tag_ids, person.category_ids)
        print('>>>>>', person.gender, person.birthday)
        address_id = False
        if person.address_id != False:
            print('>>>>>', person.address_id.name.encode("utf-8"))
            if person.address_id.street != False:
                print('>>>>>>>>>>', person.address_id.street.encode("utf-8"), 
                                    person.address_id.number)
            if person.address_id.district != False:
                print('>>>>>>>>>>', person.address_id.district.encode("utf-8"))

            address_id = clv_address.browse([('name', '=', person.address_id.name),]).id

            if address_id == []:
                values = {
                    'name': person.address_id.name,
                    'street': person.address_id.street,
                    'number': person.address_id.number,
                    'district': person.address_id.district,
                    }
                address_id = clv_address.create(values).id
                address_count += 1
            else:
                address_id = address_id[0]

        values = {
            'name': person.name,
            'code': person.code,
            'birthday': person.birthday,
            'gender': person.gender,
            'address_id': address_id,
            'date_inclusion': person.date_inclusion,
            }
        local_person_id = local_clv_person.create(values).id

    i = 0
    for person in remote_person_browse:
        i += 1

        local_person = local_clv_person.browse([('code', '=', person.code),])[0]
        print(i, local_person.code, local_person.name.encode("utf-8"))

        if person.spouse_id != False:
            spouse_count += 1
            spouse = local_clv_person.browse([('code', '=', person.spouse_id.code),])[0]
            print('>>>>> spouse', spouse.code, spouse.name.encode("utf-8"))
            values = {
                'spouse_id': spouse.id,
                }
            local_clv_person.write(local_person.id, values)
        if person.father_id != False:
            father_count += 1
            father = local_clv_person.browse([('code', '=', person.father_id.code),])[0]
            print('>>>>> father', father.code, father.name.encode("utf-8"))
            values = {
                'father_id': father.id,
                }
            local_clv_person.write(local_person.id, values)
        if person.mother_id != False:
            mother_count += 1
            mother = local_clv_person.browse([('code', '=', person.mother_id.code),])[0]
            print('>>>>> mother', mother.code, mother.name.encode("utf-8"))
            values = {
                'mother_id': mother.id,
                }
            local_clv_person.write(local_person.id, values)
        if person.responsible_id != False:
            responsible_count += 1
            responsible = local_clv_person.browse([('code', '=', person.responsible_id.code),])[0]
            print('>>>>> responsible', responsible.code, responsible.name.encode("utf-8"))
            values = {
                'responsible_id': responsible.id,
                }
            local_clv_person.write(local_person.id, values)

    print('i: ', i)
    print('person_count: ', person_count)
    print('address_count: ', address_count)
    print('spouse_count: ', spouse_count)
    print('father_count: ', father_count)
    print('mother_count: ', mother_count)
    print('responsible_count: ', responsible_count)

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
    # password = 'paswword' 
    password = '*' 

    dbname = 'odoo'
    # dbname = '*'

    remote_server = 'http://192.168.25.112:8069'

    # remote_username = 'username'
    remote_username = '*'
    # remote_password = 'paswword' 
    remote_password = '*' 

    remote_dbname = 'odoo'
    # remote_dbname = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_person.py...')

    client = erppeek.Client(server, dbname, username, password)
    remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # person_args = []
    # print('-->', client, person_args)
    # print('--> Executing clv_person_unlink("new")...')
    # clv_person_unlink(client, person_args)

    # address_args = []
    # print('-->', client, address_args)
    # print('--> Executing clv_address_unlink("new")...')
    # clv_address_unlink(client, address_args)

    # print('-->', remote_client, client)
    # print('--> Executing clv_person_import_remote()...')
    # clv_person_import_remote(remote_client, client)

    print('--> clv_person.py')
    print('--> Execution time:', secondsToStr(time() - start))
