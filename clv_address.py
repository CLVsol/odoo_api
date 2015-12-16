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


def clv_address_unlink(client, args):

    clv_address = client.model('clv_address')
    address_browse = clv_address.browse(args)

    i = 0
    deleted = 0
    not_deleted = 0
    for address in address_browse:
        i += 1
        print(i, address.name.encode("utf-8"))

        clv_person = client.model('clv_person')
        person_browse = clv_person.browse([('address_id', '=', address.id), ])
        person_ids = person_browse.id
        print('>>>>>', person_ids)

        for person_id in person_ids:
            values = {
                "address_id": False,
                }
            clv_person.write(person_id, values)

        history = client.model('clv_address.history')
        history_browse = history.browse([('address_id', '=', address.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        try:
            clv_address.unlink(address.id)
            deleted += 1
        except:
            print('>>>>>', 'Not deleted!')
            not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


def clv_address_unlink_aExcluir(client):

    clv_tag = client.model('clv_tag')
    tag_aExcluir = clv_tag.browse([('name', '=', 'aExcluir'), ])[0].id

    clv_address = client.model('clv_address')
    address_browse = clv_address.browse([])

    i = 0
    deleted = 0
    not_deleted = 0
    for address in address_browse:
        i += 1
        print(i, address.name.encode("utf-8"), address.tag_ids.id)

        for tag_id in address.tag_ids.id:

            if tag_id == tag_aExcluir:

                history = client.model('clv_address.history')
                history_browse = history.browse([('address_id', '=', address.id), ])
                history_ids = history_browse.id
                print('>>>>>', history_ids)

                history.unlink(history_ids)
                try:
                    clv_address.unlink(address.id)
                    deleted += 1
                except:
                    print('>>>>>', 'Not deleted!')
                    not_deleted += 1

    print('--> i: ', i)
    print('--> deleted: ', deleted)
    print('--> not_deleted: ', not_deleted)


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

    print('--> clv_address.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_address_unlink_aExcluir()...')
    # clv_address_unlink_aExcluir(client)

    # address_args = [('state', '=', 'draft'),
    #                 ('street', '=', False), ]
    # print('-->', client, address_args)
    # print('--> Executing clv_address_unlink()...')
    # clv_address_unlink(client, address_args)

    print('--> clv_address.py')
    print('--> Execution time:', secondsToStr(time() - start))
