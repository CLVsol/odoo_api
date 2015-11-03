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
import fileinput
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

        print(i, insured_card.code, insured_card.synchronized, insured_card.state, insured_card.name)

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
        if insured_card.synchronized:
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
            'synchronized': insured_card.synchronized,
            'date_synchronization': insured_card.date_synchronization,
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

def clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization):

    Cod_Convenio =     [ 0,   0]
    Cod_Contrato =     [ 1,   6]
    Cod_Beneficiario = [ 2,  12]
    Cod_Empresa =      [ 3,  42]
    Nome =             [ 4,  52]
    End_Logradouro =   [ 5,  92]
    End_No =           [ 6, 132]
    End_Complemento =  [ 7, 138]
    End_Bairro =       [ 8, 158]
    End_Cidade =       [ 9, 188]
    End_UF =           [10, 218]
    End_CEP =          [11, 220]
    Sexo =             [12, 228]
    Data_Nascimento =  [13, 229]
    DDD =              [14, 237]
    Telefone =         [15, 241]
    RG =               [16, 256]
    UF_Emissao_RG =    [17, 266]
    CPF =              [18, 268]
    Tipo_de_Operacao = [19, 279]
    Data_Inativacao =  [20, 280]
    Cod_Titular =      [21, 293]
    LCDF =             [22, 318]
    LCS =              [23, 333]
    ADS_Usuario =      [24, 348]
    CF_Usuario =       [25, 388]
    Email_Usuario =    [26, 428]
    Matricula =        [27, 468]
    Data_Ativacao =    [28, 498]
    XXX =              [29, 506]

    w = [
        Cod_Convenio[1],
        Cod_Contrato[1],
        Cod_Beneficiario[1],
        Cod_Empresa[1],
        Nome[1],
        End_Logradouro[1],
        End_No[1],
        End_Complemento[1],
        End_Bairro[1],
        End_Cidade[1],
        End_UF[1],
        End_CEP[1],
        Sexo[1],
        Data_Nascimento[1],
        DDD[1],
        Telefone[1],
        RG[1],
        UF_Emissao_RG[1],
        CPF[1],
        Tipo_de_Operacao[1],
        Data_Inativacao[1],
        Cod_Titular[1],
        LCDF[1],
        LCS[1],
        ADS_Usuario[1],
        CF_Usuario[1],
        Email_Usuario[1],
        Matricula[1],
        Data_Ativacao[1],
        XXX[1],
        ]

    line_no = 0
    for line in fileinput.input([file_name]):
        line_no += 1
        s = [ line[ w[i-1] : w[i] ] for i in range(1,len(w)) ]
        
        crd_code = s[Cod_Beneficiario[0]].strip()
        code_len = len(crd_code) - 2
        while len(crd_code) < 16:
            crd_code = '0' + crd_code
        code_str = "%s.%s.%s.%s.%s-%s" % (str(crd_code[0]) + str(crd_code[1]),
                                          str(crd_code[2]) + str(crd_code[3]) + str(crd_code[4]),
                                          str(crd_code[5]) + str(crd_code[6]) + str(crd_code[7]),
                                          str(crd_code[8]) + str(crd_code[9]) + str(crd_code[10]),
                                          str(crd_code[11]) + str(crd_code[12]) + str(crd_code[13]),
                                          str(crd_code[14]) + str(crd_code[15]))
        if code_len <= 3:
            code_form = code_str[18 - code_len:21]
        elif code_len > 3 and code_len <= 6:
            code_form = code_str[17 - code_len:21]
        elif code_len > 6 and code_len <= 9:
            code_form = code_str[16 - code_len:21]
        elif code_len > 9 and code_len <= 12:
            code_form = code_str[15 - code_len:21]
        elif code_len > 12 and code_len <= 14:
            code_form = code_str[14 - code_len:21]

        clv_insured_ext = client.model('clv_insured_ext')
        insured_ext_browse = clv_insured_ext.browse([('code', '=', code_form),])
        insured_ext_id = insured_ext_browse.id[0]

        print(line_no, s[Tipo_de_Operacao[0]], code_form, s[Nome[0]], insured_ext_id)

        if s[Tipo_de_Operacao[0]] == 'I':
            values = {
                'synchronized': True,
                'processing_synchronization': False,
                'date_synchronization': date_synchronization,
                'date_activation': date_synchronization,
                }
            client.exec_workflow('clv_insured_ext', 'button_process', insured_ext_id)
            client.exec_workflow('clv_insured_ext', 'button_activate', insured_ext_id)
        if s[Tipo_de_Operacao[0]] == 'E':
            values = {
                'synchronized': True,
                'processing_synchronization': False,
                'date_synchronization': date_synchronization,
                'date_cancelation': date_synchronization,
                }
            client.exec_workflow('clv_insured_ext', 'button_cancel', insured_ext_id)
        clv_insured_ext.write(insured_ext_id, values)

    print('--> line_no: ', line_no)

def clv_insured_ext_set_partner_orizon(client):

    clv_insured_ext = client.model('clv_insured_ext')
    insured_ext_browse = clv_insured_ext.browse([('partner_ids', '=', False),])

    i = 0
    for insured_ext in insured_ext_browse:
        i += 1

        print(i, insured_ext.code, insured_ext.name)

        res_partner = client.model('res.partner')
        partner_browse = res_partner.browse([('name', '=', 'Orizon'),])
        partner_ids = partner_browse.id[0]

        values = {
            'partner_ids': partner_ids,
            }
        clv_insured_ext.write(insured_ext.id, values)

    print('--> i: ', i)

def clv_insured_ext_updt_from_insured_card_orizon(client):

    clv_insured_ext = client.model('clv_insured_ext')

    clv_insured_card = client.model('clv_insured_card')

    insured_card_browse = clv_insured_card.browse([('state', '=', 'active'),])

    i = 0
    new = 0
    synchronized = 0
    not_synchronized = 0
    for insured_card in insured_card_browse:
        i += 1

        partner = False
        if insured_card.partner_ids.name != []:
            partner = insured_card.partner_ids[0].name

        print(i, insured_card.code, partner, insured_card.state, insured_card.name)

        clv_insured = client.model('clv_insured')
        insured_browse = clv_insured.browse([('id', '=', insured_card.insured_id.id),])

        clv_address = client.model('clv_address')
        address_browse = clv_address.browse([('id', '=', insured_browse.address_home_id.id[0]),])
        zip_code = False
        if address_browse.zip != []:
            zip_code = address_browse.zip[0]

        insured_ext_browse = clv_insured_ext.browse([('insured_card_id', '=', insured_card.id),])
        if insured_ext_browse.id == []:
            new += 1

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

        else:
            if insured_ext_browse[0].state == insured_card.state:
                synchronized += 1
            else:
                not_synchronized += 1

                if insured_ext_browse[0].synchronized:
                    values = {
                        'date_previous_synchronization': insured_ext_browse.date_synchronization[0],
                        }
                    clv_insured_ext.write(insured_ext_browse[0].id, values)

                    values = {
                        'synchronized': False,
                        'date_synchronization': False,
                        }
                    clv_insured_ext.write(insured_ext_browse[0].id, values)

    insured_card_browse = clv_insured_card.browse([('state', '=', 'canceled'),])

    for insured_card in insured_card_browse:
        i += 1

        partner = False
        if insured_card.partner_ids.name != []:
            partner = insured_card.partner_ids[0].name

        print(i, insured_card.code, partner, insured_card.state, insured_card.name)

        insured_ext_browse = clv_insured_ext.browse([('insured_card_id', '=', insured_card.id),])
        if insured_ext_browse.id != []:
            if insured_ext_browse[0].state == insured_card.state:
                synchronized += 1
            else:
                not_synchronized += 1

                if insured_ext_browse[0].synchronized:
                    values = {
                        'date_previous_synchronization': insured_ext_browse.date_synchronization[0],
                        }
                    clv_insured_ext.write(insured_ext_browse[0].id, values)

                    values = {
                        'synchronized': False,
                        'date_synchronization': False,
                        }
                    clv_insured_ext.write(insured_ext_browse[0].id, values)

    print('--> i: ', i)
    print('--> new: ', new)
    print('--> synchronized: ', synchronized)
    print('--> not_synchronized: ', not_synchronized)

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

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20150915_150902_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20150915_150902_I.TXT'
    # date_synchronization = '2015-09-16 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    # print('-->', client)
    # print('--> Executing clv_insured_ext_set_partner_orizon()...')
    # clv_insured_ext_set_partner_orizon(client)

    # print('-->', client)
    # print('--> Executing clv_insured_ext_updt_from_insured_card_orizon()...')
    # clv_insured_ext_updt_from_insured_card_orizon(client)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20150925_150903_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20150925_150903_I.TXT'
    # date_synchronization = '2015-09-25 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    # print('-->', client)
    # print('--> Executing clv_insured_ext_updt_from_insured_card_orizon()...')
    # clv_insured_ext_updt_from_insured_card_orizon(client)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151014_151001_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151014_151001_I.TXT'
    # date_synchronization = '2015-10-16 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    # print('-->', client)
    # print('--> Executing clv_insured_ext_updt_from_insured_card_orizon()...')
    # clv_insured_ext_updt_from_insured_card_orizon(client)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151019_151002_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151019_151002_I.TXT'
    # date_synchronization = '2015-10-19 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    # print('-->', client)
    # print('--> Executing clv_insured_ext_updt_from_insured_card_orizon()...')
    # clv_insured_ext_updt_from_insured_card_orizon(client)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151030_151003_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151030_151003_I.TXT'
    # date_synchronization = '2015-10-30 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    #######################################

    # print('-->', client)
    # print('--> Executing clv_insured_ext_updt_from_insured_card_orizon()...')
    # clv_insured_ext_updt_from_insured_card_orizon(client)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151103_151101_I.TXT'
    # print('--> Executing clv_insured_ext_syncronize_orizon(' + file_name + ')...')
    # clv_insured_ext_syncronize_orizon(client, file_name)

    # print('-->', client)
    # file_name = '/opt/openerp/orizon/USU1865_20151103_151101_I.TXT'
    # date_synchronization = '2015-11-03 21:00:00'
    # print('--> Executing clv_insured_ext_sync_confirm_orizon() for "' + file_name + '"...')
    # clv_insured_ext_sync_confirm_orizon(client, file_name, date_synchronization)

    print('--> clv_insured_ext.py')
    print('--> Execution time:', secondsToStr(time() - start))
