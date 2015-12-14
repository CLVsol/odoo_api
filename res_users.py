#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015-Today  Carlos Eduardo Vercelino - CLVsol                 #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from __future__ import print_function

from erppeek import *
import csv

from base import *
import argparse
import getpass

'''
Reference: http://help.openerp.com/question/18704/hide-menu-for-existing-group/

There are actually0-6 numbers for representing each job for a many2many/ one2many field

    (0, 0, { values }) -- link to a new record that needs to be created with the given values dictionary
    (1, ID, { values }) -- update the linked record with id = ID (write values on it)
    (2, ID) -- remove and delete the linked record with id = ID (calls unlink on ID, that will delete the
               object completely, and the link to it as well)
    (3, ID) -- cut the link to the linked record with id = ID (delete the relationship between the two
               objects but does not delete the target object itself)
    (4, ID) -- link to existing record with id = ID (adds a relationship)
    (5) -- unlink all (like using (3,ID) for all linked records)
    (6, 0, [IDs]) -- replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
'''


def res_users_export(client, file_path):

    headings_res_users = ['no', 'user_id',
                          'name', 'login', 'password_crypt', 'email',
                          'phone', 'mobile',
                          ]
    file_res_users = open(file_path, 'wb')
    writer_res_users = csv.writer(file_res_users, delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL)
    writer_res_users.writerow(headings_res_users)

    res_users = client.model('res.users')
    res_users_browse = res_users.browse([])

    i = 0
    found = 0
    not_found = 0
    for user in res_users_browse:
        i += 1

        user_id = user.id
        name = user.name.encode("utf-8")
        login = user.login
        password_crypt = user.password_crypt
        email = user.email
        phone = user.phone
        mobile = user.mobile

        print(i, user_id, name, login, password_crypt, email,
                 phone, mobile)

        row_res_users = [i, user_id,
                         name, login, password_crypt, email,
                         phone, mobile
                         ]
        writer_res_users.writerow(row_res_users)

    file_res_users.close()

    print('--> i: ', i)


def res_users_import_remote(remote_client, local_client):

    #
    # NOTE: Only user 'admin' can execute this procedure.
    #

    local_res_users = local_client.model('res.users')

    remote_res_users = remote_client.model('res.users')
    remote_users_browse = remote_res_users.browse([])

    user_count = 0
    created = 0
    for user in remote_users_browse:
        user_count += 1

        print(user_count, user.login, user.name.encode("utf-8"), 
                          user.email)

        user_id = local_res_users.browse([('login', '=', user.login),]).id

        if user_id == []:
            values = {
                'name': user.name,
                'login': user.login,
                # 'password_crypt': user.password_crypt,
                'email': user.email,
                'phone': user.phone,
                # 'email': user.email,
                'mobile': user.mobile,
                }
            user_id = local_res_users.create(values).id
            created += 1
        else:
            user_id = user_id[0]

    print('user_count: ', user_count)
    print('created: ', created)


def res_users_import_jcafb(client, file_path):

    #
    # NOTE: Only user 'admin' can execute this procedure.
    #

    delimiter_char = ';'

    f = open(file_path, "rb")
    r = csv.reader(f, delimiter=delimiter_char)

    res_users = client.model('res.users')
    hr_employee = client.model('hr.employee')
    hr_job = client.model('hr.job')

    rownum = 0
    for row in r:

        if rownum == 0:
            rownum += 1
            continue

        i = autoIncrement(0, 1)

        Nomes = row[i.next()]
        Emails = row[i.next()]
        Funcao = row[i.next()]

        print(rownum, Nomes, Emails, Funcao)

        values = {
            'name': Nomes,
            'login': Emails,
            # 'password_crypt': user.password_crypt,
            'email': Emails,
            # 'phone': user.phone,
            # 'mobile': user.mobile,
            }
        user_id = res_users.create(values).id

        hr_job_id = hr_job.browse([('name', '=', Funcao), ])[0].id

        values = {
            'name': Nomes,
            'work_email': Emails,
            # 'work_phone': user.phone,
            # 'mobile_phone': user.mobile,
            'job_id': hr_job_id,
            'user_id': user_id,
            }
        employee_id = hr_employee.create(values).id

        print('>>>>>', user_id, employee_id)

        rownum += 1

    f.close()

    print('--> rownum: ', rownum - 1)


def res_users_reset_password_jcafb(client):

    res_users = client.model('res.users')

    hr_employee = client.model('hr.employee')
    hr_employee_browse = hr_employee.browse([])

    i = 0
    found = 0
    not_found = 0
    for employee in hr_employee_browse:
        i += 1
        user = employee.user_id
        if user.login == 'admin':
            not_found += 1
        else:
            found += 1
            print(i, user.name.encode("utf-8"), user.login, user.email)
            values = {
                "password": employee.code,
                "tz": 'America/Sao_Paulo',
                }
            res_users.write(user.id, values)

    print('--> i: ', i)
    print('--> found: ', found)
    print('--> not_found: ', not_found)


def res_users_updt_employee_access_rights_jcafb(client):

    hr_employee = client.model('hr.employee')
    hr_employee_browse = hr_employee.browse([])

    res_users = client.model('res.users')
    res_groups = client.model('res.groups')

    Base_User_id = res_groups.browse([('name', '=', 'Base User'), ])[0].id
    Base_Super_User_id = res_groups.browse([('name', '=', 'Base Super User'), ])[0].id
    Base_Manager_id = res_groups.browse([('name', '=', 'Base Manager'), ])[0].id
    Base_Register_Manager_id = res_groups.browse([('name', '=', 'Base Register Manager'), ])[0].id
    Base_Super_Manager_id = res_groups.browse([('name', '=', 'Base Super Manager'), ])[0].id
    Tag_User_id = res_groups.browse([('name', '=', 'Tag User'), ])[0].id
    Tag_Manager_id = res_groups.browse([('name', '=', 'Tag Manager'), ])[0].id
    Annotation_User_id = res_groups.browse([('name', '=', 'Annotation User'), ])[0].id
    Annotation_Manager_id = res_groups.browse([('name', '=', 'Annotation Manager'), ])[0].id
    Address_User_id = res_groups.browse([('name', '=', 'Address User'), ])[0].id
    Address_Manager_id = res_groups.browse([('name', '=', 'Address Manager'), ])[0].id
    Document_User_id = res_groups.browse([('name', '=', 'Document User'), ])[0].id
    Document_Manager_id = res_groups.browse([('name', '=', 'Document Manager'), ])[0].id
    Document_Approver_id = res_groups.browse([('name', '=', 'Document Approver'), ])[0].id
    Person_User_id = res_groups.browse([('name', '=', 'Person User'), ])[0].id
    Person_Manager_id = res_groups.browse([('name', '=', 'Person Manager'), ])[0].id
    Family_User_id = res_groups.browse([('name', '=', 'Family User'), ])[0].id
    Family_Manager_id = res_groups.browse([('name', '=', 'Family Manager'), ])[0].id
    Patient_User_id = res_groups.browse([('name', '=', 'Patient User'), ])[0].id
    Patient_Manager_id = res_groups.browse([('name', '=', 'Patient Manager'), ])[0].id
    Person_mng_User_id = res_groups.browse([('name', '=', 'Person Managment User'), ])[0].id
    Person_mng_Manager_id = res_groups.browse([('name', '=', 'Person Management Manager'), ])[0].id
    Lab_Test_User_id = res_groups.browse([('name', '=', 'Lab Test User'), ])[0].id
    Lab_Test_Manager_id = res_groups.browse([('name', '=', 'Lab Test Manager'), ])[0].id
    Lab_Test_Approver_id = res_groups.browse([('name', '=', 'Lab Test Approver'), ])[0].id
    # Pointing_User_id = res_groups.browse([('name', '=', 'Pointing User'), ])[0].id
    # Pointing_Manager_id = res_groups.browse([('name', '=', 'Pointing Manager'), ])[0].id

    Contact_Creation_id = res_groups.browse([('name', '=', 'Contact Creation'), ])[0].id
    Employee_id = res_groups.browse([('name', '=', 'Employee'), ])[0].id
    Survey_User_id = res_groups.browse([('name', '=', 'Survey / User'), ])[0].id
    Website_Comments_id = res_groups.browse([('name', '=', 'Website Comments'), ])[0].id

    Group_Jornadeiro = [
        Base_User_id,
        Base_Super_User_id,
        Base_Manager_id,
        Base_Register_Manager_id,
        # Base_Super_Manager_id,
        Tag_User_id,
        Tag_Manager_id,
        Annotation_User_id,
        Annotation_Manager_id,
        Address_User_id,
        Address_Manager_id,
        Document_User_id,
        Document_Manager_id,
        Document_Approver_id,
        Person_User_id,
        Person_Manager_id,
        Family_User_id,
        Family_Manager_id,
        Patient_User_id,
        Patient_Manager_id,
        Person_mng_User_id,
        Person_mng_Manager_id,
        Lab_Test_User_id,
        Lab_Test_Manager_id,
        Lab_Test_Approver_id,

        Contact_Creation_id,
        Employee_id,
        Survey_User_id,
        Website_Comments_id,
        ]
    print('>>>>>', Group_Jornadeiro)
    i = 0
    # for user in res_users_browse:
    for employee in hr_employee_browse:
        i += 1

        user = employee.user_id

        print(i, user.login, user.groups_id.name)

        if user.login not in ['admin', 'data.admin', 'aliceherminia@gmail.com']:
            values = {
                'groups_id': [(6, 0, Group_Jornadeiro)]
                }
            res_users.write(user.id, values)

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

    print('--> res_users.py...')

    client = erppeek.Client(server, dbname, username, password)
    # remote_client = erppeek.Client(remote_server, remote_dbname, remote_username, remote_password)

    # file_path = 'data/jcafb_res_users.csv'
    # print('-->', client, file_path)
    # print('--> Executing res_users_export()...')
    # res_users_export(client, file_path)

    # print('-->', remote_client, client)
    # print('--> Executing res_users_import_remote()...')
    # res_users_import_remote(remote_client, client)

    # file_path = '/opt/openerp/jcafb/data/JCAFB_users.csv'
    # print('-->', client, file_path)
    # print('--> Executing res_users_import_jcafb()...')
    # res_users_import_jcafb(client, file_path)

    # print('-->', client)
    # print('--> Executing res_users_reset_password_jcafb()...')
    # res_users_reset_password_jcafb(client)

    # print('-->', client)
    # print('--> Executing res_users_updt_employee_access_rights_jcafb()...')
    # res_users_updt_employee_access_rights_jcafb(client)

    print('--> res_users.py')
    print('--> Execution time:', secondsToStr(time() - start))
