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

from base import *
import argparse
import getpass

from clv_address import *
from clv_tag import *


def get_family_member_role_id(client, role_name, role_description):

    clv_family_member_role = client.model('clv_family.member_role')
    family_member_role_browse = clv_family_member_role.browse(\
        [('name', '=', role_name),])
    family_member_role_id = family_member_role_browse.id

    if family_member_role_id == []:
        values = {
            "name": role_name,
            "description": role_description,
            }
        family_member_role_id = clv_family_member_role.create(values).id
    else:
        family_member_role_id = family_member_role_id[0]

    return family_member_role_id


def clv_family_unlink(client, args):

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for family in family_browse:
        i += 1
        print(i, family.name.encode("utf-8"))

        history = client.model('clv_family.history')
        history_browse = history.browse([('family_id', '=', family.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_family.unlink(family.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


def clv_family_unlink_aExcluir(client):

    clv_tag = client.model('clv_tag')
    tag_aExcluir = clv_tag.browse([('name', '=', 'aExcluir'), ])[0].id

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse([])

    i = 0
    deleted = 0
    not_deleted = 0
    for family in family_browse:
        i += 1
        print(i, family.name.encode("utf-8"), family.tag_ids.id)

        for tag_id in family.tag_ids.id:

            if tag_id == tag_aExcluir:

                history = client.model('clv_family.history')
                history_browse = history.browse([('family_id', '=', family.id), ])
                history_ids = history_browse.id
                print('>>>>>', history_ids)

                history.unlink(history_ids)
                try:
                    clv_family.unlink(family.id)
                    deleted += 1
                except:
                    print('>>>>>', 'Not deleted!')
                    not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


def clv_family_import_remote(remote_client, local_client):

    clv_address = local_client.model('clv_address')
    local_clv_family = local_client.model('clv_family')

    remote_clv_family = remote_client.model('clv_family')
    remote_family_browse = remote_clv_family.browse([])

    family_count = 0
    address_count = 0
    for family in remote_family_browse:
        family_count += 1

        print(family_count, family.code, family.name.encode("utf-8"), 
                            family.tag_ids, family.category_ids)

        address_id = False
        if family.address_id != False:
            print('>>>>>', family.address_id.name.encode("utf-8"))
            if family.address_id.street != False:
                print('>>>>>>>>>>', family.address_id.street.encode("utf-8"), 
                                    family.address_id.number)
            if family.address_id.district != False:
                print('>>>>>>>>>>', family.address_id.district.encode("utf-8"))

            address_id = clv_address.browse([('name', '=', family.address_id.name),]).id

            if address_id == []:
                values = {
                    'name': family.address_id.name,
                    'street': family.address_id.street,
                    'number': family.address_id.number,
                    'district': family.address_id.district,
                    }
                address_id = clv_address.create(values).id
                address_count += 1
            else:
                address_id = address_id[0]

        values = {
            'name': family.name,
            'code': family.code,
            'address_id': address_id,
            'date_inclusion': family.date_inclusion,
            }
        local_family_id = local_clv_family.create(values).id

    print('family_count: ', family_count)
    print('address_count: ', address_count)


def clv_family_member_import_remote(remote_client, local_client):

    clv_family = local_client.model('clv_family')
    clv_person = local_client.model('clv_person')

    local_clv_family_member = local_client.model('clv_family.member')

    remote_clv_family_person = remote_client.model('clv_family.person')
    remote_family_member_browse = remote_clv_family_person.browse([\
        ('family_id', '!=', False),
        ('person_id', '!=', False),
        ('role', '!=', False),
        ])

    person_count = 0
    for family_person in remote_family_member_browse:
        person_count += 1

        print(person_count, family_person.family_id.name.encode("utf-8"), 
                            family_person.person_id.name.encode("utf-8"), 
                            family_person.role.name.encode("utf-8"))

        family_id = clv_family.browse(\
            [('name', '=', family_person.family_id.name),])[0].id

        person_id = clv_person.browse(\
            [('name', '=', family_person.person_id.name),])[0].id

        role_id = get_family_member_role_id(client, family_person.role.name, 
                                                    family_person.role.description)

        values = {
            'family_id': family_id,
            'member_id': person_id,
            'role': role_id,
            }
        local_family_member_id = local_clv_family_member.create(values).id

    print('person_count: ', person_count)


def clv_family_mark_aExcluir(client, args):

    tag_id_aExcluir = get_tag_id(
        client,
        'aExcluir',
        'Registro a ser excluído.')

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse(args)

    i = 0
    for family in family_browse:
        i += 1
        print(i, family.name.encode("utf-8"))

        values = {
            'tag_ids': [(4, tag_id_aExcluir)],
            }
        clv_family.write(family.id, values)

    print('--> i: ', i)


def clv_family_reset_name(client, args):

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse(args)

    i = 0
    for family in family_browse:
        i += 1
        print(i, family.name.encode("utf-8"), family.address_id.name.encode("utf-8"))

        values = {
            'name': family.address_id.name,
            }
        clv_family.write(family.id, values)

    print('--> i: ', i)


def clv_family_mark_Nome_Replicado(client, args):

    tag_id_Nome_Replicado = get_tag_id(
        client,
        'Nome Replicado',
        'Registro com Nome duplicado.')

    clv_family = client.model('clv_family')
    family_browse = clv_family.browse(args)

    i = 0
    replicated = 0
    for family in family_browse:
        i += 1

        count_replicated_name = len(clv_family.browse([('name', '=', family.name), ]).id)

        print(i, family.name.encode("utf-8"), count_replicated_name)

        if count_replicated_name > 1:
            replicated += 1
            values = {
                'tag_ids': [(4, tag_id_Nome_Replicado)],
                }
            clv_family.write(family.id, values)

    print('--> i: ', i)
    print('--> replicated: ', replicated)


def clv_person_set_family_community(client, args):

    clv_person = client.model('clv_person')
    person_browse = clv_person.browse(args)

    clv_community_family = client.model('clv_community.family')

    i = 0
    for person in person_browse:
        i += 1

        community_person_ids = person.community_ids.community_id.id

        print(i, person.name.encode('utf-8'), community_person_ids)

        for community_id in community_person_ids:

            family_id = person.family_member_ids[0].family_id.id

            community_family_ids = clv_community_family.browse(
                [('community_id', '=', community_id),
                 ('family_id', '=', family_id),
                 ]).id

            print('>>>>>', community_id, community_family_ids)

            if community_family_ids == []:
                values = {
                    'community_id': community_id,
                    'family_id': family_id,
                    }
                community_family_id = clv_community_family.create(values).id
                print('>>>>>', community_family_id)

    print('--> i: ', i)


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

    remote_server = 'http://192.168.25.112:8069'

    remote_username = 'username'
    # remote_username = '*'
    remote_password = 'paswword'
    # remote_password = '*'

    remote_dbname = 'odoo'
    # remote_dbname = '*'

    get_arguments()

    from time import time
    start = time()

    print('--> clv_family.py...')

    client = erppeek.Client(server, dbname, username, password)
    # remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # family_args = []
    # print('-->', client, family_args)
    # print('--> Executing clv_family_unlink("new")...')
    # clv_family_unlink(client, family_args)

    # address_args = []
    # print('-->', client, address_args)
    # print('--> Executing clv_address_unlink("new")...')
    # clv_address_unlink(client, address_args)

    # print('-->', remote_client, client)
    # print('--> Executing clv_family_import_remote()...')
    # clv_family_import_remote(remote_client, client)

    # print('-->', remote_client, client)
    # print('--> Executing clv_family_member_import_remote()...')
    # clv_family_member_import_remote(remote_client, client)

    # family_args = [('member_ids', '=', False), ]
    # print('-->', client, family_args)
    # print('--> Executing clv_family_mark_aExcluir()...')
    # clv_family_mark_aExcluir(client, family_args)

    # family_args = [('member_ids', '=', False), ]
    # print('-->', client, family_args)
    # print('--> Executing clv_family_unlink()...')
    # clv_family_unlink(client, family_args)

    # family_args = [('address_id', '!=', False), ]
    # print('-->', client, family_args)
    # print('--> Executing clv_family_unlink()...')
    # clv_family_reset_name(client, family_args)

    # family_args = []
    # print('-->', client, family_args)
    # print('--> Executing clv_family_mark_Nome_Replicado()...')
    # clv_family_mark_Nome_Replicado(client, family_args)

    # print('-->', client)
    # print('--> Executing clv_family_unlink_aExcluir()...')
    # clv_family_unlink_aExcluir(client)

    # person_args = []
    # print('-->', client, person_args)
    # print('--> Executing clv_person_set_family_community()...')
    # clv_person_set_family_community(client, person_args)

    print('--> clv_family.py')
    print('--> Execution time:', secondsToStr(time() - start))
