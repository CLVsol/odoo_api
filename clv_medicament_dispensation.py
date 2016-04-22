#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from __future__ import print_function

from erppeek import *
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

from base import *
import argparse
import getpass


def clv_medicament_dispensation_updt_medicament_ref_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(
        [('medicament_ref', '=', False),
         ('dispensation_ext_id', '!=', False),
         ])

    i = 0
    found = 0
    not_found = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.medicament_code)

        clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
        dispensation_ext_browse = clv_medicament_dispensation_ext.browse(
            [('id', '=', dispensation.dispensation_ext_id.id), ])
        dispensation_ext_id = dispensation_ext_browse.id

        if dispensation_ext_id != []:
            found += 1

            values = {
                'medicament_ref': 'clv_orizon_lpm,' +
                                  str(dispensation_ext_browse.medicament_ref[0].id),
                }
            clv_medicament_dispensation.write(dispensation.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_updt_refund_price_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(
        [('at_sight_value', '!=', 0.0),
         ('refund_price', '!=', 0.0),
         ])

    i = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.at_sight_value, dispensation.refund_price)

        values = {
            'refund_price': 0.0,
            }
        clv_medicament_dispensation.write(dispensation.id, values)

    print('i: ', i)


def clv_medicament_dispensation_import_dispensation_ext_orizon(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')

    clv_medicament_dispensation_ext = client.model('clv_medicament_dispensation_ext')
    dispensation_ext_browse = clv_medicament_dispensation_ext.browse(
        [('state', '=', 'draft'),
         ('dispensation_id', '=', False),
         ('pharmacy_id', '!=', False),
         ('prescriber_id', '!=', False),
         ('insured_card_id', '!=', False),
         ('medicament', '!=', False),
         ('dispensation_date', '!=', False),
         ], order='name')

    i = 0
    for dispensation_ext in dispensation_ext_browse:

        i += 1
        print(i, dispensation_ext.name, dispensation_ext.dispensation_date)

        values = {
            'name': '/',
            'dispensation_date': dispensation_ext.dispensation_date,
            'medicament': dispensation_ext.medicament.id,
            'max_retail_price': 0.0,
            'pack_quantity': dispensation_ext.pack_quantity,
            'refund_price': 0.0,
            'sale_value': dispensation_ext.sale_value,
            'at_sight_value': dispensation_ext.at_sight_value,
            'insured_card_id': dispensation_ext.insured_card_id.id,
            'prescriber_id': dispensation_ext.prescriber_id.id,
            'pharmacy_id': dispensation_ext.pharmacy_id.id,
            'dispenser': False,
            'medicament_ref': 'clv_orizon_lpm,' +
                              str(dispensation_ext.medicament_ref.id),
            'dispensation_ext_id': dispensation_ext.id,
            }
        medicament_dispensation_id = clv_medicament_dispensation.create(values)

        values = {
            'dispensation_id': medicament_dispensation_id.id,
            }
        clv_medicament_dispensation_ext.write(dispensation_ext.id, values)

        client.exec_workflow('clv_medicament_dispensation_ext', 'button_waiting', dispensation_ext.id)

    print('i: ', i)


def clv_medicament_dispensation_updt_mrp(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(
        [('max_retail_price', '=', 0.0),
         ])

    i = 0
    found = 0
    not_found = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.medicament, dispensation.medicament.abcfarma_id)

        if dispensation.medicament.abcfarma_id is not False:
            found += 1
            abcfarma = dispensation.medicament.abcfarma_id

            print('>>>>>', abcfarma.med_abc, abcfarma.med_pco18)

            values = {
                'max_retail_price': abcfarma.med_pco18,
                }
            clv_medicament_dispensation.write(dispensation.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def clv_medicament_dispensation_updt_refund_price(client):

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(
        [('refund_price', '=', 0.0),
         ('dispensation_ext_id', '!=', False),
         ('at_sight_value', '=', 0.0),
         ])

    i = 0
    found = 0
    not_found = 0
    for dispensation in dispensation_browse:

        i += 1
        print(i, dispensation.name, dispensation.medicament_ref.id)

        if dispensation.medicament_ref is not False:
            found += 1

            print('>>>>>', dispensation.sale_value / dispensation.pack_quantity)

            values = {
                'refund_price': dispensation.sale_value / dispensation.pack_quantity,
                }
            clv_medicament_dispensation.write(dispensation.id, values)

        else:
            not_found += 1

    print('i: ', i)
    print('found: ', found)
    print('not_found: ', not_found)


def _age(birthday, now):

    if birthday:
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        now = datetime.strptime(now, '%Y-%m-%d')
        delta = relativedelta(birthday, now)
        # age = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
        age = str(delta.years)
    else:
        age = "No Date of Birth!"

    return age


def clv_medicament_dispensation_export(client, file_path, start_date, end_date):

    headings_dispensation = ['no', 'prescription', 'template', 'name', 'dispensation_date', 'medicament_code',
                             'medicament', 'medicament_ref', 'max_retail_price', 'pack_quantity', 'refund_price',
                             'total_refund_price',
                             'sale_value', 'at_sight_value', 'insured_card', 'state', 'prescriber', 'pharmacy',
                             'med_abc', 'cod_prod', 'insurance_client', 'reg_number', 'insured_name', 'category',
                             'titular_name',
                             'active_component', 'active_component_code', 'concentration', 'pres_form', 'pres_form_2',
                             'birthday', 'age', 'insured_card_name'
                             ]
    file_dispensation = open(file_path, 'wb')
    writer_dispensation = csv.writer(file_dispensation, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer_dispensation.writerow(headings_dispensation)

    clv_medicament_dispensation = client.model('clv_medicament_dispensation')
    dispensation_browse = clv_medicament_dispensation.browse(
        [('state', '!=', 'canceled'),
         ('dispensation_date', '>=', start_date),
         ('dispensation_date', '<=', end_date),
         ], order='name')
    i = 0
    for dispensation in dispensation_browse:
        i += 1

        print(i, dispensation.dispensation_date, dispensation.name)

        if dispensation.template_id is not False:
            prescription = dispensation.template_id.prescription_id.name
        else:
            prescription = False
        if dispensation.template_id is not False:
            template = dispensation.template_id.name
        else:
            template = False
        name = dispensation.name
        dispensation_date = dispensation.dispensation_date
        medicament_code = dispensation.medicament.code
        medicament = dispensation.medicament.name.encode('utf-8')
        if dispensation.medicament_ref is not False:
            medicament_ref = dispensation.medicament_ref.name.encode('utf-8')
        else:
            medicament_ref = False
        max_retail_price = dispensation.max_retail_price
        pack_quantity = dispensation.pack_quantity
        refund_price = dispensation.refund_price
        sale_value = dispensation.sale_value
        total_refund_price = dispensation.total_refund_price
        at_sight_value = dispensation.at_sight_value
        insured_card_name = dispensation.insured_card_id.name.encode("utf-8")
        insured_card = dispensation.insured_card_id.code
        state = dispensation.insured_card_id.state
        prescriber = dispensation.prescriber_id.name.encode("utf-8") + \
            ' [' + dispensation.prescriber_id.professional_id + ']'
        pharmacy = dispensation.pharmacy_id.name.encode("utf-8")
        if dispensation.medicament.abcfarma_id is not False:
            med_abc = dispensation.medicament.abcfarma_id.med_abc
        else:
            med_abc = False
        if dispensation.medicament_ref is not False:
            cod_prod = dispensation.medicament_ref.cod_prod
        else:
            cod_prod = False
        insurance_client = dispensation.insured_card_id.insured_id.insurance_client_id.name.encode("utf-8")
        reg_number = dispensation.insured_card_id.insured_id.reg_number
        insured_name = dispensation.insured_card_id.insured_id.name.encode("utf-8")
        category_id = dispensation.insured_card_id.insured_id.category_ids
        clv_insured_category = client.model('clv_insured.category')
        insured_category_browse = clv_insured_category.browse([('id', '=', category_id.id), ])
        category_name = insured_category_browse[0].name
        if dispensation.insured_card_id.insured_id.holder_id is not False:
            titular_name = dispensation.insured_card_id.insured_id.holder_id.name.encode("utf-8")
        else:
            # titular_name = False
            titular_name = insured_name

        if dispensation.medicament.active_component is not False:
            active_component = dispensation.medicament.active_component.name.encode("utf-8")
            active_component_code = dispensation.medicament.active_component.code
        else:
            active_component = False
            active_component_code = False
        concentration = dispensation.medicament.concentration
        if dispensation.medicament.pres_form is not False:
            pres_form = dispensation.medicament.pres_form.name.encode("utf-8")
        else:
            pres_form = False
        if dispensation.medicament.pres_form_2 is not False:
            pres_form_2 = dispensation.medicament.pres_form_2.name.encode("utf-8")
        else:
            pres_form_2 = False

        birthday = dispensation.insured_card_id.insured_id.birthday
        age = _age(dispensation_date, birthday)

        print(i, prescription, template, name, dispensation_date, medicament_code, medicament, medicament_ref,
              max_retail_price, pack_quantity,
              refund_price, total_refund_price, insured_card, state, prescriber, pharmacy, med_abc, cod_prod,
              insurance_client, reg_number, insured_name, category_name, titular_name,
              active_component, active_component_code, concentration, pres_form, pres_form_2,
              birthday, age, insured_card_name)

        row_dispensation = [i, prescription, template, name, dispensation_date, medicament_code, medicament,
                            medicament_ref,
                            str('{0:.2f}'.format(round(max_retail_price, 2))).replace('.', ','),
                            pack_quantity, str('{0:.2f}'.format(round(refund_price, 2))).replace('.', ','),
                            str('{0:.2f}'.format(round(total_refund_price, 2))).replace('.', ','),
                            str('{0:.2f}'.format(round(sale_value, 2))).replace('.', ','),
                            str('{0:.2f}'.format(round(at_sight_value, 2))).replace('.', ','),
                            insured_card, state, prescriber, pharmacy, med_abc, cod_prod,
                            insurance_client, reg_number, insured_name, category_name, titular_name,
                            active_component, active_component_code, concentration, pres_form, pres_form_2,
                            birthday, age, insured_card_name
                            ]
        writer_dispensation.writerow(row_dispensation)

    file_dispensation.close()

    print('i: ', i)


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

    print('--> clv_medicament_dispensation.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_medicament_ref_orizon()...')
    # clv_medicament_dispensation_updt_medicament_ref_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price_orizon()...')
    # clv_medicament_dispensation_updt_refund_price_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_09_21.csv"
    # start_date = '2015-08-21'
    # end_date = '2015-09-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_05_21_a_09_20.csv"
    # start_date = '2015-05-21'
    # end_date = '2015-09-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_09_21_a_10_20.csv"
    # start_date = '2015-09-21'
    # end_date = '2015-10-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_05_21_a_10_31.csv"
    # start_date = '2015-05-21'
    # end_date = '2015-10-31'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_10_21_a_11_20.csv"
    # start_date = '2015-10-21'
    # end_date = '2015-11-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_11_01_a_11_30.csv"
    # start_date = '2015-11-01'
    # end_date = '2015-11-30'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_11_21_a_12_20.csv"
    # start_date = '2015-11-21'
    # end_date = '2015-12-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_12_21_a_2016_01_20.csv"
    # start_date = '2015-12-21'
    # end_date = '2016-01-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2016_01_01_a_2016_01_31.csv"
    # start_date = '2016-01-01'
    # end_date = '2016-01-31'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2015_12_01_a_2015_12_31.csv"
    # start_date = '2015-12-01'
    # end_date = '2015-12-31'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2016_01_21_a_2016_02_20.csv"
    # start_date = '2016-01-21'
    # end_date = '2016-02-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2016_02_01_a_2016_02_29.csv"
    # start_date = '2016-02-01'
    # end_date = '2016-02-29'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2016_02_21_a_2016_03_20.csv"
    # start_date = '2016-02-21'
    # end_date = '2016-03-20'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    # 2016-04-01 ######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # file_path = "/opt/openerp/biobox/data/bb_dispensation_2016_03_01_a_2016_03_31.csv"
    # start_date = '2016-03-01'
    # end_date = '2016-03-31'
    # print('-->', client, file_path, start_date, end_date)
    # print('--> Executing clv_medicament_dispensation_export()...')
    # clv_medicament_dispensation_export(client, file_path, start_date, end_date)

    # 2016-04-12 ######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    # ##### 2016-04-22 ######################################

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_import_dispensation_ext_orizon()...')
    # clv_medicament_dispensation_import_dispensation_ext_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_mrp()...')
    # clv_medicament_dispensation_updt_mrp(client)

    # print('-->', client)
    # print('--> Executing clv_medicament_dispensation_updt_refund_price()...')
    # clv_medicament_dispensation_updt_refund_price(client)

    print('--> clv_medicament_dispensation.py')
    print('--> Execution time:', secondsToStr(time() - start))
