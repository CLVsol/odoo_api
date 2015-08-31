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

# import re
# import openerplib
# import xmlrpclib
# import argparse
# import getpass

hostname = 'localhost'
admin = 'admin'
admin_pw = 'admin'
# admin_pw = '*'
sock_common_url = 'http://localhost:8069/xmlrpc/common'
sock_str = 'http://localhost:8069/xmlrpc/object'

admin_user = 'admin'
admin_user_pw = 'admin' 
# admin_user_pw = '*' 

data_admin_user = 'data.admin'
data_admin_user_pw = 'data.admin' 
# data_admin_user_pw = '*' 

dbname = 'odoo'
# dbname = '*'

def get_arguments():

    global admin_pw
    global admin_user_pw
    global data_admin_user
    global data_admin_user_pw
    global dbname

    parser = argparse.ArgumentParser()
    # parser.add_argument('--admin_pw', action="store", dest="admin_pw")
    # parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
    parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
    parser.add_argument('--dbname', action="store", dest="dbname")
    parser.add_argument('--dbname', action="store", dest="dbname")

    args = parser.parse_args()
    print '%s%s' % ('--> ', args)

    # if args.admin_pw != None:
    #     admin_pw = args.admin_pw
    # elif admin_pw == '*':
    #     admin_pw = getpass.getpass('admin_pw: ')

    # if args.admin_user_pw != None:
    #     admin_user_pw = args.admin_user_pw
    # elif admin_user_pw == '*':
    #     admin_user_pw = getpass.getpass('admin_user_pw: ')

    if args.data_admin_user_pw != None:
        data_admin_user_pw = args.data_admin_user_pw
    elif data_admin_user_pw == '*':
        data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

    if args.dbname != None:
        dbname = args.dbname
    elif dbname == '*':
        dbname = raw_input('dbname: ')

def autoIncrement(start=0, step=1):
    i = start
    while 1:
        yield i
        i += step
