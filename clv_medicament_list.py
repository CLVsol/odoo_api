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
from filedict import *

from base import *
import argparse
import getpass


def get_medicament_list_id(client, list_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    medicament_list_id = medicament_list_browse.id

    if medicament_list_id == []:
        values = {
            'name': list_name,
            }
        medicament_list_id = clv_medicament_list.create(values).id
    else:
        medicament_list_id = medicament_list_id[0]

    return medicament_list_id


def get_medicament_list_version_id(client, list_id, list_version_name):

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', list_id),
         ('name', '=', list_version_name),
         ])
    medicament_list_version_id = medicament_list_version_browse.id

    if medicament_list_version_id == []:
        values = {
            'list_id': list_id,
            'name': list_version_name,
            }
        medicament_list_version_id = clv_medicament_list_version.create(values).id
    else:
        medicament_list_version_id = medicament_list_version_id[0]

    return medicament_list_version_id


def export_medicament_list_id_from_mericament_ref_code_orizon(client, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item.id,
              medicament_list_item.medicament_ref.id,
              medicament_list_item.medicament_ref.cod_prod,
              medicament_list_item.medicament_ref.name.encode("utf-8"))

        d[medicament_list_item.medicament_ref.cod_prod] = [medicament_list_item.id]

        print('>>>>>', medicament_list_item.medicament_ref.cod_prod,
              d[medicament_list_item.medicament_ref.cod_prod])

    print('--> i: ', i)


def clv_medicament_list_updt_medicament_orizon(client, list_name, list_version_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ('medicament_id', '=', False),
         ])

    i = 0
    found = 0
    not_found = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        if medicament_list_item.medicament_ref != False:
            clv_medicament = client.model('clv_medicament')
            medicament_browse = clv_medicament.browse(\
                [('orizon_lpm_id', '=', medicament_list_item.medicament_ref.id),])
            print('>>>>>', medicament_browse)

            if medicament_browse.id != []:
                found += 1
                values = {
                    'medicament_id': medicament_browse[0].id,
                    }
                clv_medicament_list_item.write(medicament_list_item.id, values)
            else:
                not_found += 1
        else:
            not_found += 1

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_medicament_list_clear_subsidy_orizon(client, list_name, list_version_name):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id),
         ('subsidy', '!=', 0.0),
         ])

    i = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        values = {
            'subsidy': 0.0,
            }
        clv_medicament_list_item.write(medicament_list_item.id, values)

    print('--> i: ', i)


def clv_medicament_list_set_subsidy_orizon(client, infile_name, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    delimiter_char = ';'

    f = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        cod_prod = row[i.next()]
        medicament = row[i.next()]
        discount = row[i.next()]
        preco_venda = row[i.next()].replace(",", ".")
        Subsidio = row[i.next()]

        print(rownum, cod_prod, medicament)

        clv_medicament_list = client.model('clv_medicament_list')
        medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
        print('>>>>>', medicament_list_browse)

        clv_medicament_list_version = client.model('clv_medicament_list.version')
        medicament_list_version_browse = clv_medicament_list_version.browse(
            [('list_id', '=', medicament_list_browse[0].id),
             ('name', '=', list_version_name),
             ])
        print('>>>>>', medicament_list_version_browse)

        clv_medicament_list_item = client.model('clv_medicament_list.item')

        print('>>>>>', cod_prod, d[int(cod_prod)])
        try:
            medicament_list_item_id = d[int(cod_prod)]
        except:
            medicament_list_item_id = []

        if medicament_list_item_id != []:
            found += 1
            values = {
                'subsidy': 100.0,
                }
            clv_medicament_list_item.write(medicament_list_item_id[0], values)
        else:
            not_found += 1

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def clv_medicament_list_clear_old_from(client, list_name, list_version_name, from_):

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', medicament_list_version_browse[0].id), ])

    i = 0
    unlinked = 0
    not_unlinked = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item)

        clv_orizon_lpm = client.model('clv_orizon_lpm')
        orizon_lpm_browse = clv_orizon_lpm.browse([('id', '=', medicament_list_item.medicament_ref.id),
                                                   ('from', '!=', from_),
                                                   ])
        print('>>>>>', orizon_lpm_browse)

        if orizon_lpm_browse.id != []:
            unlinked += 1
            medicament_list_item.unlink()
        else:
            not_unlinked += 1

    print('--> i: ', i)
    print('--> unlinked: ', unlinked)
    print('--> not_unlinked: ', not_unlinked)


def clv_medicament_list_check_orizon(client, infile_name, list_name, list_version_name, list_id_filename):

    d = filedict.FileDict(filename=list_id_filename)

    clv_medicament_list = client.model('clv_medicament_list')
    medicament_list_browse = clv_medicament_list.browse([('name', '=', list_name), ])
    print('>>>>>', medicament_list_browse)

    clv_medicament_list_version = client.model('clv_medicament_list.version')
    medicament_list_version_browse = clv_medicament_list_version.browse(
        [('list_id', '=', medicament_list_browse[0].id),
         ('name', '=', list_version_name),
         ])
    print('>>>>>', medicament_list_version_browse)

    delimiter_char = ';'

    f = open(infile_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    ok = 0
    not_ok = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Reembolso = row[i.next()]
        if Reembolso == '1':
            Reembolso = '100.0'
        Laboratorio = row[i.next()]
        Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        EAN_Principal = row[i.next()]
        PMC = row[i.next()].replace(",", ".")
        Desconto = row[i.next()].replace(",", ".")
        Preco_Venda = row[i.next()].replace(",", ".")
        Categoria = row[i.next()]
        Sub_Categoria = row[i.next()]
        Classificacao = row[i.next()]
        Sub_Classificacao = row[i.next()]
        Classe_Terapeutica = row[i.next()]
        Sub_Classe_Terapeutica = row[i.next()]
        Principio_Ativo = row[i.next()]

        print(rownum, Cod_Prod, Apresentacao_Do_Produto)

        clv_medicament_list_item = client.model('clv_medicament_list.item')

        print('>>>>>', Cod_Prod, d[int(Cod_Prod)])
        try:
            medicament_list_item_id = d[int(Cod_Prod)]
        except:
            medicament_list_item_id = []

        if medicament_list_item_id != []:
            found += 1
            medicament_list_item = clv_medicament_list_item.browse(
                [('id', '=', medicament_list_item_id[0]), ])[0]
            print('>>>>>>>>>>', medicament_list_item, medicament_list_item.subsidy, Reembolso,
                  medicament_list_item.discount, Desconto)
            if medicament_list_item.subsidy == float(Reembolso) and \
               medicament_list_item.discount == float(Desconto):
                ok += 1
            else:
                not_ok += 1
        else:
            not_found += 1

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)
    print('--> found: ', found)
    print('--> not_found: ', not_found)
    print('--> ok: ', ok)
    print('--> not_ok: ', not_ok)


def clv_medicament_list_include_orizon(client, file_name, list_name, list_version_name):

    list_id = get_medicament_list_id(client, list_name)
    list_version_id = get_medicament_list_version_id(client, list_id, list_version_name)

    delimiter_char = ';'

    clv_orizon_lpm = client.model('clv_orizon_lpm')
    clv_medicament = client.model('clv_medicament')
    clv_medicament_list_item = client.model('clv_medicament_list.item')

    f = open(file_name, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    orizon_lpm_found = 0
    orizon_lpm_not_found = 0
    medicament_found = 0
    medicament_not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Reembolso = row[i.next()]
        if Reembolso == '1':
            Reembolso = '100.0'
        Laboratorio = row[i.next()]
        Produto = row[i.next()]
        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        EAN_Principal = row[i.next()]
        PMC = row[i.next()].replace(",", ".")
        Desconto = row[i.next()].replace(",", ".")
        Preco_Venda = row[i.next()].replace(",", ".")
        Categoria = row[i.next()]
        Sub_Categoria = row[i.next()]
        Classificacao = row[i.next()]
        Sub_Classificacao = row[i.next()]
        Descricao = row[i.next()]
        Classe_Terapeutica = row[i.next()]
        Sub_Classe_Terapeutica = row[i.next()]
        Principio_Ativo = row[i.next()]

        print(rownum, Cod_Prod, Apresentacao_Do_Produto)

        orizon_lpm_browse = clv_orizon_lpm.browse([('cod_prod', '=', Cod_Prod), ])
        if len(orizon_lpm_browse) == 1:
            orizon_lpm_found += 1
            orizon_lpm_id = orizon_lpm_browse[0].id
            print('>>>>>', orizon_lpm_id)

            medicament_browse = clv_medicament.browse([('orizon_lpm_id', '=', orizon_lpm_id), ])
            medicament_id = False
            if len(medicament_browse) == 1:
                medicament_found += 1
                medicament_id = medicament_browse[0].id
                print('>>>>>', medicament_id)

            else:
                medicament_not_found += 1

            values = {
                'list_version_id': list_version_id,
                'medicament_id': medicament_id,
                'medicament_ref': 'clv_orizon_lpm,' + str(orizon_lpm_id),
                'order': orizon_lpm_found,
                'discount': Desconto,
                'subsidy': Reembolso,
                }
            medicament_list_item_id = clv_medicament_list_item.create(values).id
            print('>>>>>>>>>>', medicament_list_item_id)

        else:
            orizon_lpm_not_found += 1

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)
    print('orizon_lpm_found: ', orizon_lpm_found)
    print('orizon_lpm_not_found: ', orizon_lpm_not_found)
    print('medicament_found: ', medicament_found)
    print('medicament_not_found: ', medicament_not_found)


def clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path):

    headings_item = ['no',
                     # 'medicament_id',
                     # 'medicament_ref',
                     'cod_BioBox', 'cod_abc', 'cod_garantemed', 'cod_orizon',
                     'nome_biobox', 'medicament_name', 'presentation',
                     'active_component_name', 'active_component_code',
                     'concentration', 'pres_form', 'pres_form_2',
                     'discount', 'subsidy',
                     'notes',
                     ]
    file_item = open(file_path, 'wb')
    writer_item = csv.writer(file_item, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_item.writerow(headings_item)

    list_id = get_medicament_list_id(client, medicament_list)
    list_version_id = get_medicament_list_version_id(client, list_id, medicament_list_version)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', list_version_id), ])

    # test = medicament_list_item_browse.read('medicament_id medicament_ref')
    # print('>>>>>', test)

    item_count = 0
    for medicament_list_item in medicament_list_item_browse:
        item_count += 1

        medicament_id = False
        nome_biobox = False
        cod_BioBox = False
        cod_abc = False
        cod_garantemed = False
        cod_orizon = False

        medicament_name = False
        presentation = False
        active_component_name = False
        active_component_code = False
        concentration = False
        pres_form = False
        pres_form_2 = False

        medicament_ref = False

        notes = False
        if medicament_list_item.notes is not False:
            notes = medicament_list_item.notes.encode('utf-8')

        if medicament_list_item.medicament_id is not False:
            medicament_id = medicament_list_item.medicament_id.id
            nome_biobox = medicament_list_item.medicament_id.name.encode('utf-8')
            cod_BioBox = medicament_list_item.medicament_id.code
            if medicament_list_item.medicament_id.medicament_name is not False:
                medicament_name = medicament_list_item.medicament_id.medicament_name.encode('utf-8')
            if medicament_list_item.medicament_id.presentation is not False:
                presentation = medicament_list_item.medicament_id.presentation.encode('utf-8')
            if medicament_list_item.medicament_id.active_component is not False:
                active_component_name = medicament_list_item.medicament_id.active_component.name.encode('utf-8')
                active_component_code = medicament_list_item.medicament_id.active_component.code
            if medicament_list_item.medicament_id.concentration is not False:
                concentration = medicament_list_item.medicament_id.concentration.encode('utf-8')
            if medicament_list_item.medicament_id.pres_form is not False:
                pres_form = medicament_list_item.medicament_id.pres_form.name.encode('utf-8')
            if medicament_list_item.medicament_id.pres_form_2 is not False:
                pres_form_2 = medicament_list_item.medicament_id.pres_form_2.name.encode('utf-8')

            if medicament_list_item.medicament_id.abcfarma_id is not False:
                cod_abc = medicament_list_item.medicament_id.abcfarma_id.med_abc

            if medicament_list_item.medicament_id.medicament_gm_id is not False:
                cod_garantemed = medicament_list_item.medicament_id.medicament_gm_id.cod_prod_fabricante

            if medicament_list_item.medicament_id.orizon_lpm_id is not False:
                cod_orizon = medicament_list_item.medicament_id.orizon_lpm_id.cod_prod

        if medicament_list_item.medicament_ref is not False:
            medicament_ref = medicament_list_item.medicament_ref.id

            if reference == 'clv_orizon_lpm':
                cod_orizon = medicament_list_item.medicament_ref.cod_prod

        discount = medicament_list_item.discount
        subsidy = medicament_list_item.subsidy

        print(item_count, medicament_list_item.order,
              medicament_id, medicament_ref,
              cod_BioBox, cod_abc, cod_garantemed, cod_orizon)

        row_item = [medicament_list_item.order,
                    # medicament_id,
                    # medicament_ref,
                    cod_BioBox, cod_abc, cod_garantemed, cod_orizon,
                    nome_biobox, medicament_name, presentation,
                    active_component_name, active_component_code,
                    concentration, pres_form, pres_form_2,
                    discount, subsidy,
                    notes
                    ]
        writer_item.writerow(row_item)

    file_item.close()

    print('item_count: ', item_count)


def clv_medicament_list_updt_medicament_orizon_2(client, medicament_list, medicament_list_version):

    list_id = get_medicament_list_id(client, medicament_list)
    list_version_id = get_medicament_list_version_id(client, list_id, medicament_list_version)

    clv_medicament_list_item = client.model('clv_medicament_list.item')
    medicament_list_item_browse = clv_medicament_list_item.browse(
        [('list_version_id', '=', list_version_id),
         ('medicament_id', '=', False),
         ])

    clv_medicament = client.model('clv_medicament')

    i = 0
    found = 0
    not_found = 0
    for medicament_list_item in medicament_list_item_browse:
        i += 1
        print(i, medicament_list_item.medicament_ref.name.encode('utf-8'))

        medicament_browse = clv_medicament.browse(
            [('orizon_lpm_id', '=', medicament_list_item.medicament_ref.id), ])

        if medicament_browse.id != []:
            found += 1
            print('>>>>>', found, medicament_browse[0].name.encode('utf-8'))
            values = {
                'medicament_id': medicament_browse[0].id,
                }
            clv_medicament_list_item.write(medicament_list_item.id, values)
        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_list_import(client, file_path, list_name, list_version_name):

    clv_orizon_lpm = client.model('clv_orizon_lpm')

    delimiter_char = ';'

    f = open(file_path, "rb")
    r = csv.reader(f, delimiter=delimiter_char)
    rownum = 0
    found = 0
    not_found = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Cod_Prod = row[i.next()]
        Apresentacao_Do_Produto = row[i.next()]
        Desconto = row[i.next()]
        Reembolso = row[i.next()]

        print(rownum, Cod_Prod, Apresentacao_Do_Produto, Desconto, Reembolso)

        orizon_lpm_id = clv_orizon_lpm.browse([('cod_prod', '=', Cod_Prod), ]).id
        if orizon_lpm_id != []:
            found += 1
            print('>>>>>', orizon_lpm_id)
        else:
            not_found += 1
            print('XXXXXXXXXX', orizon_lpm_id)

        rownum += 1

    f.close()

    print('rownum: ', rownum - 1)
    print('found: ', found)
    print('not_found: ', not_found)


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

    print('--> clv_medicament_list.py...')

    client = erppeek.Client(server, dbname, username, password)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, list_name, list_version_name, list_id_filename)
    # print('--> Executing export_medicament_list_id_from_mericament_ref_code_orizon()...')
    # export_medicament_list_id_from_mericament_ref_code_orizon(client, list_name, list_version_name, list_id_filename)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon()...')
    # clv_medicament_list_updt_medicament_orizon(client, list_name, list_version_name)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_clear_subsidy_orizon()...')
    # clv_medicament_list_clear_subsidy_orizon(client, list_name, list_version_name)

    # infile_name = '/opt/openerp/orizon_lpm/Lista_483_0_5k_LPM_1508.csv'
    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, infile_name, list_name, list_version_name, list_id_filename)
    # print('--> Executing clv_medicament_list_set_subsidy_orizon()...')
    # clv_medicament_list_set_subsidy_orizon(client, infile_name, list_name, list_version_name, list_id_filename)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # from_ = 'LPM_1509'
    # print('-->', client, list_name, list_version_name, from_)
    # print('--> Executing clv_medicament_list_clear_old_from()...')
    # clv_medicament_list_clear_old_from(client, list_name, list_version_name, from_)

    # infile_name = '/opt/openerp/orizon_lpm/Lista_483_LPM_Agosto_2015.csv'
    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1508'
    # list_id_filename = "data/cod_prod_list_id_for_Orizon_483_0_5k_1508"
    # print('-->', client, infile_name, list_name, list_version_name, list_id_filename)
    # print('--> Executing clv_medicament_list_check_orizon()...')
    # clv_medicament_list_check_orizon(client, infile_name, list_name, list_version_name, list_id_filename)

    # file_name = '/opt/openerp/orizon_lpm/Lista_483_0_5k_BioBox_x_Orizon_1511.csv'
    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1511'
    # print('-->', client, file_name, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_include_orizon()...')
    # clv_medicament_list_include_orizon(client, file_name, list_name, list_version_name)

    ###########################################

    # medicament_list = 'CPqD - Memento'
    # medicament_list_version = '1500'
    # reference = 'clv_medicament'
    # file_path = '/opt/openerp/biobox/data/ml_CPqD_Memento_1500_2016_01_13.csv'
    # print('-->', client, medicament_list, medicament_list_version, reference, file_path)
    # print('--> Executing clv_medicament_list_export()...')
    # clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path)

    # medicament_list = 'CPqD - Anexo'
    # medicament_list_version = '1500'
    # reference = 'clv_medicament'
    # file_path = '/opt/openerp/biobox/data/ml_CPqD_Anexo_1500_2016_01_13.csv'
    # print('-->', client, medicament_list, medicament_list_version, reference, file_path)
    # print('--> Executing clv_medicament_list_export()...')
    # clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path)

    # medicament_list = 'Econômico'
    # medicament_list_version = '1401'
    # reference = 'clv_medicament'
    # file_path = '/opt/openerp/biobox/data/ml_Economico_1401_2016_01_13.csv'
    # print('-->', client, medicament_list, medicament_list_version, reference, file_path)
    # print('--> Executing clv_medicament_list_export()...')
    # clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path)

    # medicament_list = 'Orizon 478 (1,0k)'
    # medicament_list_version = '1508'
    # reference = 'clv_orizon_lpm'
    # file_path = '/opt/openerp/biobox/data/ml_Orizon_478_1_0k_1508_2016_01_13.csv'
    # print('-->', client, medicament_list, medicament_list_version, reference, file_path)
    # print('--> Executing clv_medicament_list_export()...')
    # clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path)

    # medicament_list = 'Orizon 483 (0,5k)'
    # medicament_list_version = '1511'
    # reference = 'clv_orizon_lpm'
    # file_path = '/opt/openerp/biobox/data/ml_Orizon_483_0_5k_1511_2016_01_13.csv'
    # print('-->', client, medicament_list, medicament_list_version, reference, file_path)
    # print('--> Executing clv_medicament_list_export()...')
    # clv_medicament_list_export(client, medicament_list, medicament_list_version, reference, file_path)

    ###########################################

    # list_name = 'Orizon 478 (1,0k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon_2()...')
    # clv_medicament_list_updt_medicament_orizon_2(client, list_name, list_version_name)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1511'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon_2()...')
    # clv_medicament_list_updt_medicament_orizon_2(client, list_name, list_version_name)

    # list_name = 'Orizon 147 (4,0k)'
    # list_version_name = '1508'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon_2()...')
    # clv_medicament_list_updt_medicament_orizon_2(client, list_name, list_version_name)

    # list_name = 'Orizon 478 (1,0k)'
    # list_version_name = '1500'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon_2()...')
    # clv_medicament_list_updt_medicament_orizon_2(client, list_name, list_version_name)

    # list_name = 'Orizon 483 (0,5k)'
    # list_version_name = '1500'
    # print('-->', client, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_updt_medicament_orizon_2()...')
    # clv_medicament_list_updt_medicament_orizon_2(client, list_name, list_version_name)

    ###########################################

    # file_path = '/opt/openerp/biobox/data/Lista_Flex_Parceiro_1602.csv'
    # list_name = 'Flex Parceiro'
    # list_version_name = '1602'
    # print('-->', client, file_path, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_import()...')
    # clv_medicament_list_import(client, file_path, list_name, list_version_name)

    # file_path = '/opt/openerp/biobox/data/Lista_Flex_Acesso_1602.csv'
    # list_name = 'Flex Acesso'
    # list_version_name = '1602'
    # print('-->', client, file_path, list_name, list_version_name)
    # print('--> Executing clv_medicament_list_import()...')
    # clv_medicament_list_import(client, file_path, list_name, list_version_name)

    print('--> clv_medicament_list.py')
    print('--> Execution time:', secondsToStr(time() - start))
