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
# import csv
import fileinput
import re

from base import *
import argparse
import getpass

from clv_insurance_client import *
from clv_insurance import *
from clv_insured import *
from clv_tag import *

def clv_insured_mng_unlink(client, status):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([('state', '=', status),])

    i = 0
    for insured_mng in insured_mng_browse:
        i += 1
        print(i, insured_mng.name)

        history = client.model('clv_insured_mng.history')
        history_browse = history.browse([('insured_mng_id', '=', insured_mng.id),])
        history_ids = history_browse.id
        print('>>>>>', history_ids)

        history.unlink(history_ids)
        clv_insured_mng.unlink(insured_mng.id)

    print('--> i: ', i)

def clv_insured_mng_import(client, batch_name, file_name, client_name):

    Nome =           [ 0, 0]
    Endereco =       [ 1, 60]
    No =             [ 2, 100]
    Complemento =    [ 3, 106]
    Bairro =         [ 4, 126]
    Cidade =         [ 5, 156]
    UF =             [ 6, 186]
    CEP =            [ 7, 188]
    Sexo =           [ 8, 196]
    DataNascimento = [ 9, 197]
    DDD =            [10, 205]
    Telefone =       [11, 209]
    RG =             [12, 224]
    UF_Emissao =     [13, 234]
    CPF =            [14, 236]
    Operacao =       [15, 247]
    DataInativacao = [16, 248]
    Setor =          [17, 256]
    Cargo =          [18, 296]
    Email =          [19, 336]
    Matricula =      [20, 376]
    Beneficiario =   [21, 406]
    DataAtivacao =   [22, 407]
    Card_Code =      [23, 415]
    XXX =            [23, 428]

    w = [
        Nome[1],
        Endereco[1],
        No[1],
        Complemento[1],
        Bairro[1],
        Cidade[1],
        UF[1],
        CEP[1],
        Sexo[1],
        DataNascimento[1],
        DDD[1],
        Telefone[1],
        RG[1],
        UF_Emissao[1],
        CPF [1],
        Operacao[1],
        DataInativacao[1],
        Setor[1],
        Cargo[1],
        Email[1],
        Matricula[1],
        Beneficiario[1],
        DataAtivacao[1],
        Card_Code[1],
        XXX[1],
        ]

    client_id = get_insurance_client_id(client, client_name)

    insured_cat_id_titular = get_insured_category_id(client, 'Titular')
    insured_cat_id_dependente = get_insured_category_id(client, 'Dependente')
    insured_cat_id_ascendente = get_insured_category_id(client, 'Ascendente')

    insurance_id_T = get_insurance_id(client, 'HVC - Titulares')
    insurance_id_D = get_insurance_id(client, 'HVC - Dependentes')
    insurance_id_A = 0

    clv_insured_mng = client.model('clv_insured_mng')

    line_no = 0
    for line in fileinput.input([file_name]):
        line_no += 1
        s = [ line[ w[i-1] : w[i] ] for i in range(1,len(w)) ]
        
        name = s[Nome[0]]
        name = name.strip()
        name = name.replace("  ", " ")
        name = name.replace("  ", " ")
        crd_name = name
        name = name.title()
        name = name.replace(" De ", " de ")
        name = name.replace(" Da ", " da ")
        name = name.replace(" Do ", " do ")
        name = name.replace(" Dos ", " dos ")
        name = name.replace(" E ", " e ")

        print(line_no, s[CPF[0]], validate_cpf(s[CPF[0]]), name)

        values = {
            "name": name,
            "crd_name": crd_name,
            "code": False,
            "crd_code": False,
            "insurance_client_id": client_id,
            "batch_name": batch_name,
            }
        insured_mng_id = clv_insured_mng.create(values).id

        beneficiario = False
        if (s[Beneficiario[0]] != False):
            beneficiario = s[Beneficiario[0]]
            beneficiario = beneficiario.strip()
            if beneficiario == 'T':
                insured_cat_id = insured_cat_id_titular
                insurance_id = insurance_id_T
            if beneficiario == 'D':
                insured_cat_id = insured_cat_id_dependente
                insurance_id = insurance_id_D
            if beneficiario == 'A':
                insured_cat_id = insured_cat_id_ascendente
                insurance_id = insurance_id_A
            values = {
                "category_ids": [(4, insured_cat_id)],
                "insurance_id": insurance_id,
                }
            clv_insured_mng.write(insured_mng_id, values)

        if validate_cpf(s[CPF[0]]) and s[CPF[0]] != '00000000000':
            val = re.sub('[^0-9]', '', s[CPF[0]])
            if len(val) == 11:
                cpf = "%s.%s.%s-%s" % (val[0:3], val[3:6], val[6:9], val[9:11])
            values = {
                "cpf": cpf,
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[RG[0]] != False) and (s[RG[0]] != '0000000000'):
            rg = s[RG[0]]
            while rg[0] == '0':
                rg = rg[1:]
            values = {
                "rg": rg + ' - ' + s[UF_Emissao[0]],
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Sexo[0]] != False):
            gender = s[Sexo[0]]
            values = {
                "gender": gender,
                }
            clv_insured_mng.write(insured_mng_id, values)

        birthday = s[DataNascimento[0]]
        if birthday != False:
            d = [0, 2, 4, 8]
            dd = [ birthday[ d[j-1] : d[j] ] for j in range(1,len(d)) ]
            birthday = '%s-%s-%s' % (dd[2], dd[1], dd[1])
            values = {
                "birthday": birthday,
                }
            clv_insured_mng.write(insured_mng_id, values)

        number = s[No[0]]
        if number != False:
            number = str(int(number))

        complemento = s[Complemento[0]]
        if complemento != False:
            complemento = complemento.strip()
            complemento = complemento.title()
            complemento = complemento.replace(" De ", " de ")
            complemento = complemento.replace(" Da ", " da ")
            complemento = complemento.replace(" Do ", " do ")
            complemento = complemento.replace(" Dos ", " dos ")
            complemento = complemento.replace(" E ", " e ")

        email = s[Email[0]]
        if email != False:
            email = email.lower().strip()

        ddd = s[DDD[0]]
        if ddd != False:
            ddd = str(int(ddd))
        telefone = s[Telefone[0]]
        if telefone != False:
            telefone = int(telefone)
            if telefone != 0:
                telefone = str(telefone)
                val = re.sub('[^0-9]', '', telefone)
                if len(val) == 8:
                    telefone = "%s-%s" % (val[0:4], val[4:8])
                if len(val) == 9:
                    telefone = "%s %s-%s" % (val[0], val[1:5], val[5:8])
                telefone = '(' + ddd + ') ' + telefone

        cep = s[CEP[0]]

        l10n_br_zip = client.model('l10n_br.zip')
        l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', re.sub('[^0-9]', '', cep)),])
        zip_id = l10n_br_zip_browse.id

        if zip_id != []:
            zip_ = l10n_br_zip_browse[0].zip
            val = re.sub('[^0-9]', '', zip_)
            if len(val) == 8:
                zip_ = "%s-%s" % (val[0:5], val[5:8])
            street_type = l10n_br_zip_browse[0].street_type
            street = l10n_br_zip_browse[0].street
            street = street_type + ' ' + street
            if street == ' ':
                street = s[Endereco[0]]
                if street != False:
                    street = street.strip()
                    street = street.title()
                    street = street.replace(" De ", " de ")
                    street = street.replace(" Da ", " da ")
                    street = street.replace(" Do ", " do ")
                    street = street.replace(" Dos ", " dos ")
                    street = street.replace(" E ", " e ")
            district = l10n_br_zip_browse[0].district
            if district == '':
                district = s[Bairro[0]]
                if district != False:
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

            values = {
                "addr_zip": zip_,
                "addr_street": street,
                "addr_number": number,
                "addr_street2": complemento,
                "addr_country_id": country_id,
                "addr_state_id": state_id,
                "addr_l10n_br_city_id": l10n_br_city_id,
                "addr_district": district,
                "addr_email": email,
                "addr_phone": telefone,
                }
            clv_insured_mng.write(insured_mng_id, values)

        else:
            zip_ = cep
            street = s[Endereco[0]]
            if street != False:
                street = street.strip()
                street = street.title()
                street = street.replace(" De ", " de ")
                street = street.replace(" Da ", " da ")
                street = street.replace(" Do ", " do ")
                street = street.replace(" Dos ", " dos ")
                street = street.replace(" E ", " e ")
            district = s[Bairro[0]]
            if district != False:
                district = district.strip()
                district = district.title()
                district = district.replace(" De ", " de ")
                district = district.replace(" Da ", " da ")
                district = district.replace(" Do ", " do ")
                district = district.replace(" Dos ", " dos ")
                district = district.replace(" E ", " e ")
            country_id = [0]
            state_id = [0]
            l10n_br_city_id = [0]
            cidade = s[Cidade[0]]
            if district != False:
                cidade = cidade.strip()
                cidade = cidade.title()
                cidade = cidade.replace(" De ", " de ")
                cidade = cidade.replace(" Da ", " da ")
                cidade = cidade.replace(" Do ", " do ")
                cidade = cidade.replace(" Dos ", " dos ")
                cidade = cidade.replace(" E ", " e ")
            addr_notes = 'Cidade: ' + cidade + ' - ' + s[UF[0]]
            print('>>>>>', addr_notes)

            values = {
                "addr_zip": zip_,
                "addr_street": street,
                "addr_number": number,
                "addr_street2": complemento,
                "addr_country_id": country_id[0],
                "addr_state_id": state_id[0],
                "addr_l10n_br_city_id": l10n_br_city_id[0],
                "addr_district": district,
                "addr_email": email,
                "addr_phone": telefone,
                "addr_notes": addr_notes,
                }
            clv_insured_mng.write(insured_mng_id, values)
            
        if (s[Matricula[0]] != False):
            reg_number = s[Matricula[0]]
            reg_number = reg_number.strip()
            values = {
                "reg_number": reg_number,
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Card_Code[0]] != False):
            crd_code = s[Card_Code[0]]
            crd_code = crd_code.strip()
            values = {
                "crd_code": crd_code,
                }
            clv_insured_mng.write(insured_mng_id, values)

def clv_insured_mng_check_crd_name(client):

    tag_id_NomeCartaoMaiorQue35caracteres = get_tag_id(\
        client,
        'Nome do Cartão > 35 caracteres', 
        'Registro cujo nome do cartão é maior do que 35 caracteres.')

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([])
    i = 0
    clear_tag = 0
    set_tag = 0
    for insured_mng in insured_mng_browse:

        i += 1
        print(i, insured_mng.name)

        if len(insured_mng.crd_name) <= 35:
            clear_tag += 1
            values = {
                'tag_ids': [(3, tag_id_NomeCartaoMaiorQue35caracteres)],
                }
            clv_insured_mng.write(insured_mng.id, values)
        else:
            if insured_mng.crd_name[0] == '[':
                set_tag += 1
                values = {
                    'tag_ids': [(4, tag_id_NomeCartaoMaiorQue35caracteres)],
                    }
            else:
                set_tag += 1
                values = {
                    'tag_ids': [(4,tag_id_NomeCartaoMaiorQue35caracteres)],
                    'crd_name': '[' + str(len(insured_mng.crd_name)) + ']' + insured_mng.crd_name,
                    }
            clv_insured_mng.write(insured_mng.id, values)

    print('--> i: ', i)
    print('--> clear_tag: ', clear_tag)
    print('--> set_tag: ', set_tag)

def clv_insured_mng_updt_state_revised(client, args):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse(args)

    insured_mng_count = 0
    for insured_mng in insured_mng_browse:
        insured_mng_count += 1

        print(insured_mng_count, insured_mng.state, insured_mng.name.encode("utf-8"))

        if insured_mng.state == 'draft':
            client.exec_workflow('clv_insured_mng', 'button_revised', insured_mng.id)

    print('insured_mng_count: ', insured_mng_count)

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

    print('--> clv_insured_mng.py...')

    client = erppeek.Client(server, dbname, username, password)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_unlink("draft")...')
    # clv_insured_mng_unlink(client, 'draft')

    # print('-->', client)
    # print('--> Executing clv_insured_mng_unlink("revised")...')
    # clv_insured_mng_unlink(client, 'revised')

    # print('-->', client)
    # print('--> Executing clv_insured_mng_unlink("done")...')
    # clv_insured_mng_unlink(client, 'done')

    # print('-->', client)
    # print('--> Executing clv_insured_mng_unlink("canceled")...')
    # clv_insured_mng_unlink(client, 'canceled')

    # batch_name = 'HVC_20150928_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20150928_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # print('-->', client, batch_name, file_name, client_name)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'),]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    print('--> clv_insured_mng.py')
    print('--> Execution time:', secondsToStr(time() - start))
