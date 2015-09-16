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
import re

from base import *
import argparse
import getpass

def clv_insured_ext_unlink(client, status):

    clv_insured_ext = client.model('clv_insured_ext')
    insured_ext_browse = clv_insured_ext.browse([('state', '=', status),])

    i = 0
    for insured_ext in insured_ext_browse:
        i += 1
        print(i, insured_ext.name)

        history = client.model('clv_insured_ext.history')
        history_browse = history.browse([('insured_ext_id', '=', insured_ext.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_insured_ext.unlink(insured_ext.id)

    print('--> i: ', i)

def clv_insured_ext_import(client):

    clv_insured_ext = client.model('clv_insured_ext')

    clv_insured_card = client.model('clv_insured_card')
    insured_card_browse = clv_insured_card.browse([('orizon', '=', True),])
    i = 0
    synchronized = 0
    not_synchronized = 0
    for insured_card in insured_card_browse:
        i += 1

        print(i, insured_card.code, insured_card.orizon_synchronized, insured_card.state, insured_card.name)

        clv_insured = client.model('clv_insured')
        insured_browse = clv_insured.browse([('id', '=', insured_card.insured_id.id),])

        clv_address = client.model('clv_address')
        address_browse = clv_address.browse([('id', '=', insured_browse.address_home_id.id[0]),])
        zip_code = False
        if address_browse.zip != []:
            zip_code = address_browse.zip[0]

        print('>>>>>', insured_browse.code, insured_browse.name)
        print('#####', insured_card.code, insured_card.name, insured_browse.birthday[0], 
                       insured_browse.gender[0], insured_browse.id[0], insured_card.id,
                       insured_browse.cpf[0],
                       zip_code)

        values = {
            'name': insured_card.name,
            'code': insured_card.code,
            'address_id': False,
            'birthday': insured_browse.birthday[0],
            'gender': insured_browse.gender[0],
            'insured_id': insured_browse.id[0],
            'insured_card_id': insured_card.id,
            'cpf': insured_browse.cpf[0],
            'zip_code': zip_code,
            }

        insured_ext_id = clv_insured_ext.create(values).id

        print('xxxxx', insured_ext_id, insured_card.orizon_state)

        values = {
            'date_activation': insured_card.date_activation,
            'date_cancelation': insured_card.date_cancelation,
            }
        if insured_card.orizon_synchronized:
            synchronized += 1
            if insured_card.orizon_state == 'active':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_activate', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
            if insured_card.orizon_state == 'canceled':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_cancel', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
        else:
            not_synchronized += 1
            if insured_card.orizon_previous_state == 'active':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_activate', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)
            if insured_card.orizon_previous_state == 'canceled':
                client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
                client.exec_workflow('clv_insured_ext', 'button_cancel', insured_ext_id)
                clv_insured_ext.write(insured_ext_id, values)

        values = {
            'synchronized': insured_card.orizon_synchronized,
            'date_synchronization': insured_card.orizon_date_synchronization,
            'date_previous_synchronization': insured_card.orizon_date_previous_synchronization,
            }
        clv_insured_ext.write(insured_ext_id, values)

    print('--> i: ', i)
    print('--> synchronized: ', synchronized)
    print('--> not_synchronized: ', not_synchronized)

def clv_insured_ext_syncronize_orizon(client, file_name):

    text_file = open(file_name, "w")

    clv_insured_ext = client.model('clv_insured_ext')
    insured_ext_browse = clv_insured_ext.browse([('synchronized', '=', False),
                                                 ('processing_synchronization', '=', False),
                                                 ])

    i = 0
    for insured_ext in insured_ext_browse:
        i += 1

        clv_insured = client.model('clv_insured')
        insured_browse = clv_insured.browse([('id', '=', insured_ext.insured_id.id),])

        clv_insured_card = client.model('clv_insured_card')
        insured_card_browse = clv_insured_card.browse([('id', '=', insured_ext.insured_card_id.id),])

        code = insured_ext.code
        name = insured_ext.name.encode("utf-8")
        state = insured_card_browse.state[0]
        orizon_previous_state = insured_ext.state

        print(i, code, name, state, orizon_previous_state)

        gender = insured_ext.gender
        birthday = insured_ext.birthday

        if insured_ext.zip_code != False:
            cep = insured_ext.zip_code
        else:
            cep = ''

        Cod_Convenio =     [ 1,   1,  6, '001865']

        clv_insurance = client.model('clv_insurance')
        insured_browse = clv_insurance.browse([('id', '=', insured_browse.insurance_id[0].id),])
        insurance = insured_browse.name[0]

        Cod_Contrato = False
        if insurance == 'HVC - Dependentes':
            Cod_Contrato =     [ 2,   7,  6, '001583']
        if insurance == 'HVC - Titulares':
            Cod_Contrato =     [ 2,   7,  6, '001583']
        if insurance == 'VCAS - Dependentes':
            Cod_Contrato =     [ 2,   7,  6, '001583']
        if insurance == 'VCAS - Titulares':
            Cod_Contrato =     [ 2,   7,  6, '001583']

        if insurance == 'BioBox - Pleno':
            Cod_Contrato =     [ 2,   7,  6, '001568']
        if insurance == 'BioBox - Fixo':
            Cod_Contrato =     [ 2,   7,  6, '001569']
        if insurance.encode("utf-8") == 'BioBox - Variável':
            Cod_Contrato =     [ 2,   7,  6, '001570']

        code = re.sub('[^0-9]', '', code)
        code = ''.join((code, (30 - len(code)) * ' '))
        Cod_Beneficiario = [ 3,  13, 30, code]

        Cod_Empresa =      [ 4,  43, 10, 10 * ' ']

        name = ''.join((name, (40 - len(name)) * ' '))
        Nome  =            [ 5,  53, 40, name]

        End_Logradouro =   [ 6,  93, 40, 40 * ' ']
        End_No =           [ 7, 133,  6, 6 * '0']
        End_Complemento =  [ 8, 139, 20, 20 * ' ']
        End_Bairro =       [ 9, 159, 30, 30 * ' ']
        End_Cidade =       [10, 189, 30, 30 * ' ']
        End_UF =           [11, 219,  2, 2 * ' ']

        print('>>>>>', cep)
        cep = re.sub('[^0-9]', '', cep)
        cep = ''.join((cep, (8 - len(cep)) * '0'))
        End_CEP =          [12, 221,  8, cep]

        Sexo =             [13, 229,  1, gender]

        birthday = re.sub('[^0-9]', '', birthday)
        d = [0, 4, 6, 8]
        dd = [ birthday[ d[j-1] : d[j] ] for j in range(1,len(d)) ]
        birthday = '%s%s%s' % (dd[2], dd[1], dd[0])
        Data_Nascimento =  [14, 230,  8, birthday]

        DDD =              [15, 238,  4, 4 * '0']
        Telefone =         [16, 242, 15, 15 * '0']
        RG =               [17, 257, 10, 10 * '0']
        UF_Emissao_RG =    [18, 267,  2, 2 * ' ']
        CPF =              [19, 269, 11, 11 * ' ']

        if state == 'active':
            to = 'I'
        else:
            to = 'E'
        Tipo_de_Operacao = [20, 280,  1, to]

        Data_Inativacao =  [21, 281,  8, 8 * ' ']

        # code_titular = ''
        # code_titular = re.sub('[^0-9]', '', code_titular)
        # code_titular = ''.join((code_titular, (30 - len(code_titular)) * ' '))
        # Cod_Titular =      [22, 289, 30, code_titular]
        Cod_Titular = Cod_Beneficiario

        LCDF =             [23, 319, 15, 15 * '0']

        LCS =              [24, 334, 15, '000000000050000']

        ADS_Usuario =      [25, 349, 40, 40 * ' ']
        CF_Usuario =       [26, 389, 40, 40 * ' ']
        Email_Usuario =    [27, 429, 40, 40 * ' ']
        Matricula =        [28, 469, 30, 30 * ' ']
        Data_Ativacao =    [29, 499,  8, 8 * ' ']

        line = list('')
        line.insert( 1, Cod_Convenio[3])
        line.insert( 2, Cod_Contrato[3])
        line.insert( 3, Cod_Beneficiario[3])
        line.insert( 4, Cod_Empresa[3])
        line.insert( 5, Nome[3])
        line.insert( 6, End_Logradouro[3])
        line.insert( 7, End_No[3])
        line.insert( 8, End_Complemento[3])
        line.insert( 9, End_Bairro[3])
        line.insert(10, End_Cidade[3])
        line.insert(11, End_UF[3])
        line.insert(12, End_CEP[3])
        line.insert(13, Sexo[3])
        line.insert(14, Data_Nascimento[3])
        line.insert(15, DDD[3])
        line.insert(16, Telefone[3])
        line.insert(17, RG[3])
        line.insert(18, UF_Emissao_RG[3])
        line.insert(19, CPF[3])
        line.insert(20, Tipo_de_Operacao[3])
        line.insert(21, Data_Inativacao[3])
        line.insert(22, Cod_Titular[3])
        line.insert(23, LCDF[3])
        line.insert(24, LCS[3])
        line.insert(25, ADS_Usuario[3])
        line.insert(26, CF_Usuario[3])
        line.insert(27, Email_Usuario[3])
        line.insert(28, Matricula[3])
        line.insert(29, Data_Ativacao[3])

        print('>>>>>', ''.join(line))

        # text_file.write(''.join(line) + '\n')
        text_file.write(''.join(line) + '\r\n')

        values = {
            'processing_synchronization': True,
            }
        clv_insured_ext.write(insured_ext.id, values)

    text_file.close()

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

    print('--> clv_insured_ext.py...')

    client = erppeek.Client(server, dbname, username, password)

    print('-->', client)

    # print('--> Executing clv_insured_ext_unlink("new")...')
    # clv_insured_ext_unlink(client, 'new')

    # print('--> Executing clv_insured_ext_unlink("processing")...')
    # clv_insured_ext_unlink(client, 'processing')

    # print('--> Executing clv_insured_ext_unlink("active")...')
    # clv_insured_ext_unlink(client, 'active')

    # print('--> Executing clv_insured_ext_unlink("suspended")...')
    # clv_insured_ext_unlink(client, 'suspended')

    # print('--> Executing clv_insured_ext_unlink("canceled")...')
    # clv_insured_ext_unlink(client, 'canceled')

    # print('-->', client)
    # print('--> Executing clv_insured_ext_import()...')
    # clv_insured_ext_import(client)

    print('-->', client)
    file_name = '/opt/openerp/orizon/USU1865_20150915_150902_I.TXT'
    print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    clv_insured_ext_syncronize_orizon(client, file_name)

    print('--> clv_insured_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))
