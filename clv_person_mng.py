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
import csv
import re

from base import *
import argparse
import getpass

from clv_person import *
from clv_tag import *


def clv_person_mng_unlink(client, status):

    clv_person_mng = client.model('clv_person_mng')
    person_mng_browse = clv_person_mng.browse([('state', '=', status), ])

    i = 0
    for person_mng in person_mng_browse:
        i += 1
        print(i, person_mng.name)

        history = client.model('clv_person_mng.history')
        history_browse = history.browse([('person_mng_id', '=', person_mng.id), ])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_person_mng.unlink(person_mng.id)

    print('--> i: ', i)


def clv_person_mng_import_jcafb_2016_crianca(client, file_path, batch_name):

    delimiter_char = ';'

    f = open(file_path, "rb")
    r = csv.reader(f, delimiter=delimiter_char)

    clv_person_mng = client.model('clv_person_mng')

    rownum = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        NOME = row[i.next()]
        RESPONSAVEL = row[i.next()]
        NASCIMENTO = row[i.next()]
        ENDERECO = row[i.next()]
        CONATO = row[i.next()]

        print(rownum, NOME, RESPONSAVEL, NASCIMENTO, ENDERECO, CONATO)

        values = {
            'name': NOME,
            'responsible': RESPONSAVEL,
            'person_phone': CONATO,
            "batch_name": batch_name,
            }
        person_mng_id = clv_person_mng.create(values).id

        birthday = NASCIMENTO
        if birthday is not False:
            # d = [0, 2, 4, 8]
            # dd = [birthday[d[j-1]: d[j]] for j in range(1, len(d))]
            # birthday = '%s-%s-%s' % (dd[2], dd[1], dd[1])
            values = {
                "birthday": birthday,
                }
            clv_person_mng.write(person_mng_id, values)

        l10n_br_zip = client.model('l10n_br.zip')
        l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', '14250000'), ])
        zip_id = l10n_br_zip_browse.id

        if zip_id != []:
            zip_ = l10n_br_zip_browse[0].zip
            val = re.sub('[^0-9]', '', zip_)
            if len(val) == 8:
                zip_ = "%s-%s" % (val[0:5], val[5:8])
            # street_type = l10n_br_zip_browse[0].street_type
            street = l10n_br_zip_browse[0].street
            # street = street_type + ' ' + street
            street = ' '
            if street == ' ':
                street = ENDERECO
                if street is not False:
                    street = street.strip()
                    street = street.title()
                    street = street.replace(" De ", " de ")
                    street = street.replace(" Da ", " da ")
                    street = street.replace(" Do ", " do ")
                    street = street.replace(" Dos ", " dos ")
                    street = street.replace(" E ", " e ")
            district = l10n_br_zip_browse[0].district
            if district == '':
                # district = s[Bairro[0]]
                district = False
                if district is not False:
                    district = district.strip()
                    district = district.title()
                    district = district.replace(" De ", " de ")
                    district = district.replace(" Da ", " da ")
                    district = district.replace(" Do ", " do ")
                    district = district.replace(" Dos ", " dos ")
                    district = district.replace(" E ", " e ")
            country_id = l10n_br_zip_browse[0].country_id.id
            state_id = l10n_br_zip_browse[0].state_id.id
            l10n_br_city_id = l10n_br_zip_browse[0].l10n_br_city_id.id

            print('>>>>>', birthday, zip_, street, country_id, state_id, l10n_br_city_id)

            values = {
                "addr_zip": zip_,
                "addr_street": street,
                # "addr_number": number,
                # "addr_street2": complemento,
                "addr_country_id": country_id,
                "addr_state_id": state_id,
                "addr_l10n_br_city_id": l10n_br_city_id,
                # "addr_district": district,
                # "addr_email": email,
                # "addr_phone": telefone,
                }
            clv_person_mng.write(person_mng_id, values)

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)


def clv_person_mng_import_jcafb_2016_idoso(client, file_path, batch_name):

    delimiter_char = ';'

    f = open(file_path, "rb")
    r = csv.reader(f, delimiter=delimiter_char)

    clv_person_mng = client.model('clv_person_mng')

    rownum = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        NOME = row[i.next()]
        ENDERECO = row[i.next()]

        print(rownum, NOME, ENDERECO)

        values = {
            'name': NOME,
            "batch_name": batch_name,
            }
        person_mng_id = clv_person_mng.create(values).id

        l10n_br_zip = client.model('l10n_br.zip')
        l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', '14250000'), ])
        zip_id = l10n_br_zip_browse.id

        if zip_id != []:
            zip_ = l10n_br_zip_browse[0].zip
            val = re.sub('[^0-9]', '', zip_)
            if len(val) == 8:
                zip_ = "%s-%s" % (val[0:5], val[5:8])
            # street_type = l10n_br_zip_browse[0].street_type
            street = l10n_br_zip_browse[0].street
            # street = street_type + ' ' + street
            street = ' '
            if street == ' ':
                street = ENDERECO
                if street is not False:
                    street = street.strip()
                    street = street.title()
                    street = street.replace(" De ", " de ")
                    street = street.replace(" Da ", " da ")
                    street = street.replace(" Do ", " do ")
                    street = street.replace(" Dos ", " dos ")
                    street = street.replace(" E ", " e ")
            district = l10n_br_zip_browse[0].district
            if district == '':
                # district = s[Bairro[0]]
                district = False
                if district is not False:
                    district = district.strip()
                    district = district.title()
                    district = district.replace(" De ", " de ")
                    district = district.replace(" Da ", " da ")
                    district = district.replace(" Do ", " do ")
                    district = district.replace(" Dos ", " dos ")
                    district = district.replace(" E ", " e ")
            country_id = l10n_br_zip_browse[0].country_id.id
            state_id = l10n_br_zip_browse[0].state_id.id
            l10n_br_city_id = l10n_br_zip_browse[0].l10n_br_city_id.id

            print('>>>>>', zip_, street, country_id, state_id, l10n_br_city_id)

            values = {
                "addr_zip": zip_,
                "addr_street": street,
                # "addr_number": number,
                # "addr_street2": complemento,
                "addr_country_id": country_id,
                "addr_state_id": state_id,
                "addr_l10n_br_city_id": l10n_br_city_id,
                # "addr_district": district,
                # "addr_email": email,
                # "addr_phone": telefone,
                }
            clv_person_mng.write(person_mng_id, values)

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)


def clv_person_mng_import_jcafb_2016_idoso_set_batch_name(client, file_path, batch_name):

    delimiter_char = ';'

    f = open(file_path, "rb")
    r = csv.reader(f, delimiter=delimiter_char)

    clv_person_mng = client.model('clv_person_mng')

    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        NOME = row[i.next()]
        ENDERECO = row[i.next()]

        print(rownum, NOME, ENDERECO)

        person_mng_ids = clv_person_mng.browse([('name', '=', NOME), ]).id

        if person_mng_ids != []:
            found += 1
            person_mng_id = person_mng_ids[0]

            values = {
                "batch_name": batch_name,
                }
            clv_person_mng.write(person_mng_id, values)
        else:
            not_found += 1
            print('>>>>> not found: ', not_found)

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_person_mng_search_person(client):

    clv_person_mng = client.model('clv_person_mng')
    person_mng_browse = clv_person_mng.browse([('person_id', '=', False), ])
    clv_person = client.model('clv_person')

    i = 0
    found = 0
    not_found = 0
    for person_mng in person_mng_browse:
        i += 1
        print(i, person_mng.name)

        person_id = clv_person.browse([('name', '=', person_mng.name), ]).id

        if person_id == []:
            not_found += 1
        else:
            found += 1
            values = {
                "person_id": person_id[0],
                }
            clv_person_mng.write(person_mng.id, values)

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_person_mng_set_addr_name(client):

    clv_person_mng = client.model('clv_person_mng')
    person_mng_browse = clv_person_mng.browse([('addr_name', '=', False), ])

    i = 0
    for person_mng in person_mng_browse:
        i += 1
        print(i, person_mng.name)

        addr_street = person_mng.addr_street

        values = {
            "addr_street": False,
            }
        clv_person_mng.write(person_mng.id, values)

        values = {
            "addr_street": addr_street,
            }
        clv_person_mng.write(person_mng.id, values)

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

    print('--> clv_person_mng.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("draft")...')
    # clv_person_mng_unlink(client, 'draft')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("revised")...')
    # clv_person_mng_unlink(client, 'revised')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("done")...')
    # clv_person_mng_unlink(client, 'done')

    # print('-->', client)
    # print('--> Executing clv_person_mng_unlink("canceled")...')
    # clv_person_mng_unlink(client, 'canceled')

    # batch_name = 'Criancas_2016_Rural'
    # file_path = '/opt/openerp/jcafb/data/Criancas_2016_Rural.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_crianca()...')
    # clv_person_mng_import_jcafb_2016_crianca(client, file_path, batch_name)

    # batch_name = 'Criancas_2016_Urbana'
    # file_path = '/opt/openerp/jcafb/data/Criancas_2016_Urbana.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_crianca()...')
    # clv_person_mng_import_jcafb_2016_crianca(client, file_path, batch_name)

    # batch_name = 'Idosos_2016_completa'
    # file_path = '/opt/openerp/jcafb/data/Idosos_2016_completa.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_idoso()...')
    # clv_person_mng_import_jcafb_2016_idoso(client, file_path, batch_name)

    # batch_name = 'Idosos_2016_novos'
    # file_path = '/opt/openerp/jcafb/data/Idosos_2016_novos.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_idoso_set_batch_name()...')
    # clv_person_mng_import_jcafb_2016_idoso_set_batch_name(client, file_path, batch_name)

    # batch_name = 'Idosos_2016_selecionados'
    # file_path = '/opt/openerp/jcafb/data/Idosos_2016_selecionados.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_idoso_set_batch_name()...')
    # clv_person_mng_import_jcafb_2016_idoso_set_batch_name(client, file_path, batch_name)

    # batch_name = 'Idosos_2016_urbana'
    # file_path = '/opt/openerp/jcafb/data/Idosos_2016_urbana.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_idoso_set_batch_name()...')
    # clv_person_mng_import_jcafb_2016_idoso_set_batch_name(client, file_path, batch_name)

    # batch_name = 'Idosos_2016_rural'
    # file_path = '/opt/openerp/jcafb/data/Idosos_2016_rural.csv'
    # print('-->', client, file_path, batch_name)
    # print('--> Executing clv_person_mng_import_jcafb_2016_idoso_set_batch_name()...')
    # clv_person_mng_import_jcafb_2016_idoso_set_batch_name(client, file_path, batch_name)

    # print('-->', client)
    # print('--> Executing clv_person_mng_search_person()...')
    # clv_person_mng_search_person(client)

    # print('-->', client)
    # print('--> Executing clv_person_mng_set_addr_name()...')
    # clv_person_mng_set_addr_name(client)

    print('--> clv_person_mng.py')
    print('--> Execution time:', secondsToStr(time() - start))
