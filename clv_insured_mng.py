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
# import csv
import fileinput
import re

from base import *
import argparse
import getpass

from clv_insurance_client import *
from clv_insurance import *
from clv_insured import *
from clv_insured_card import *
from clv_tag import *
from clv_batch import *


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


def clv_insured_mng_convert_txt_csv(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A):

    Nome = [0, 0]
    Endereco = [1, 60]
    No = [2, 100]
    Complemento = [3, 106]
    Bairro = [4, 126]
    Cidade = [5, 156]
    UF = [6, 186]
    CEP = [7, 188]
    Sexo = [8, 196]
    DataNascimento = [9, 197]
    DDD = [10, 205]
    Telefone = [11, 209]
    RG = [12, 224]
    UF_Emissao = [13, 234]
    CPF = [14, 236]
    Operacao = [15, 247]
    DataInativacao = [16, 248]
    Setor = [17, 256]
    Cargo = [18, 296]
    Email = [19, 336]
    Matricula = [20, 376]
    Beneficiario = [21, 406]
    DataAtivacao = [22, 407]
    Card_Code = [23, 415]
    XXX = [23, 428]

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
        CPF[1],
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

    line_no = 0
    for line in fileinput.input([file_name]):
        line_no += 1
        s = [line[w[i - 1]:w[i]] for i in range(1, len(w))]

        name = s[Nome[0]]
        name = name.strip()
        name = name.replace("  ", " ")
        name = name.replace("  ", " ")
        # crd_name = name.upper()
        name = name.title()
        name = name.replace(" De ", " de ")
        name = name.replace(" Da ", " da ")
        name = name.replace(" Do ", " do ")
        name = name.replace(" Dos ", " dos ")
        name = name.replace(" E ", " e ")

        print(line_no, s[CPF[0]], validate_cpf(s[CPF[0]]), name)

        beneficiario = False
        if (s[Beneficiario[0]] is not False):
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

        if (s[RG[0]] is not False) and (s[RG[0]] != '0000000000') and (s[RG[0]] != '          '):
            rg = s[RG[0]]
            while rg[0] == '0':
                rg = rg[1:]
            values = {
                "rg": rg + ' - ' + s[UF_Emissao[0]],
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Sexo[0]] is not False):
            gender = s[Sexo[0]]
            values = {
                "gender": gender,
                }
            clv_insured_mng.write(insured_mng_id, values)

        birthday = s[DataNascimento[0]]
        if birthday is not False:
            d = [0, 2, 4, 8]
            dd = [birthday[d[j-1]:d[j]] for j in range(1, len(d))]
            birthday = '%s-%s-%s' % (dd[2], dd[1], dd[1])
            values = {
                "birthday": birthday,
                }
            clv_insured_mng.write(insured_mng_id, values)

        number = s[No[0]]
        if number is not False:
            number = str(int(number))

        complemento = s[Complemento[0]]
        if complemento is not False:
            complemento = complemento.strip()
            complemento = complemento.title()
            complemento = complemento.replace(" De ", " de ")
            complemento = complemento.replace(" Da ", " da ")
            complemento = complemento.replace(" Do ", " do ")
            complemento = complemento.replace(" Dos ", " dos ")
            complemento = complemento.replace(" E ", " e ")

        email = s[Email[0]]
        if email is not False:
            email = email.lower().strip()

        ddd = s[DDD[0]]
        if ddd is not False:
            if ddd == '    ':
                ddd = '0000'
            ddd = str(int(ddd))
        telefone = s[Telefone[0]]
        if telefone is not False:
            if telefone == '               ':
                telefone = '000000000000000'
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
        l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', re.sub('[^0-9]', '', cep)), ])
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
                district = s[Bairro[0]]
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
            if street is not False:
                street = street.strip()
                street = street.title()
                street = street.replace(" De ", " de ")
                street = street.replace(" Da ", " da ")
                street = street.replace(" Do ", " do ")
                street = street.replace(" Dos ", " dos ")
                street = street.replace(" E ", " e ")
            district = s[Bairro[0]]
            if district is not False:
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
            cidade = s[Cidade[0]].encode('utf-8')
            if district is not False:
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

        if (s[Matricula[0]] is not False):
            reg_number = s[Matricula[0]]
            reg_number = reg_number.strip()
            values = {
                "reg_number": reg_number,
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Card_Code[0]] is not False):
            crd_code = s[Card_Code[0]]
            crd_code = crd_code.strip()
            values = {
                "crd_code": crd_code,
                }
            clv_insured_mng.write(insured_mng_id, values)


def clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A):

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
        CPF[1],
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

    # insurance_id_T = get_insurance_id(client, 'HVC - Titulares')
    insurance_id_T = get_insurance_id(client, insurance_T)
    # insurance_id_D = get_insurance_id(client, 'HVC - Dependentes')
    insurance_id_D = get_insurance_id(client, insurance_D)
    insurance_id_A = get_insurance_id(client, insurance_A)

    clv_insured_mng = client.model('clv_insured_mng')

    line_no = 0
    for line in fileinput.input([file_name]):
        line_no += 1
        s = [line[w[i - 1]:w[i]] for i in range(1, len(w))]

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
        if (s[Beneficiario[0]] is not False):
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

        if (s[RG[0]] is not False) and (s[RG[0]] != '0000000000') and (s[RG[0]] != '          '):
            rg = s[RG[0]]
            while rg[0] == '0':
                rg = rg[1:]
            values = {
                "rg": rg + ' - ' + s[UF_Emissao[0]],
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Sexo[0]] is not False):
            gender = s[Sexo[0]]
            values = {
                "gender": gender,
                }
            clv_insured_mng.write(insured_mng_id, values)

        birthday = s[DataNascimento[0]]
        if birthday is not False:
            d = [0, 2, 4, 8]
            dd = [birthday[d[j-1]:d[j]] for j in range(1, len(d))]
            birthday = '%s-%s-%s' % (dd[2], dd[1], dd[1])
            values = {
                "birthday": birthday,
                }
            clv_insured_mng.write(insured_mng_id, values)

        number = s[No[0]]
        if number is not False:
            number = str(int(number))

        complemento = s[Complemento[0]]
        if complemento is not False:
            complemento = complemento.strip()
            complemento = complemento.title()
            complemento = complemento.replace(" De ", " de ")
            complemento = complemento.replace(" Da ", " da ")
            complemento = complemento.replace(" Do ", " do ")
            complemento = complemento.replace(" Dos ", " dos ")
            complemento = complemento.replace(" E ", " e ")

        email = s[Email[0]]
        if email is not False:
            email = email.lower().strip()

        ddd = s[DDD[0]]
        if ddd is not False:
            if ddd == '    ':
                ddd = '0000'
            ddd = str(int(ddd))
        telefone = s[Telefone[0]]
        if telefone is not False:
            if telefone == '               ':
                telefone = '000000000000000'
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
        l10n_br_zip_browse = l10n_br_zip.browse([('zip', '=', re.sub('[^0-9]', '', cep)), ])
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
                district = s[Bairro[0]]
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
            if street is not False:
                street = street.strip()
                street = street.title()
                street = street.replace(" De ", " de ")
                street = street.replace(" Da ", " da ")
                street = street.replace(" Do ", " do ")
                street = street.replace(" Dos ", " dos ")
                street = street.replace(" E ", " e ")
            district = s[Bairro[0]]
            if district is not False:
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
            cidade = s[Cidade[0]].encode('utf-8')
            if district is not False:
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

        if (s[Matricula[0]] is not False):
            reg_number = s[Matricula[0]]
            reg_number = reg_number.strip()
            values = {
                "reg_number": reg_number,
                }
            clv_insured_mng.write(insured_mng_id, values)

        if (s[Card_Code[0]] is not False):
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


def clv_insured_mng_updt_state_waiting(client, args):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse(args)

    insured_mng_count = 0
    for insured_mng in insured_mng_browse:
        insured_mng_count += 1

        print(insured_mng_count, insured_mng.state, insured_mng.name.encode("utf-8"))

        if insured_mng.state == 'draft':
            client.exec_workflow('clv_insured_mng', 'button_revised', insured_mng.id)
            client.exec_workflow('clv_insured_mng', 'button_waiting', insured_mng.id)

        if insured_mng.state == 'revised':
            client.exec_workflow('clv_insured_mng', 'button_waiting', insured_mng.id)

    print('insured_mng_count: ', insured_mng_count)


def clv_insured_mng_check_insured(client, args):

    tag_id_VerificarDuplicidadeDeBeneficiario = get_tag_id(\
        client,
        'Verificar Duplicidade de Beneficiário', 
        'Registro cujo número de registro já está cadastrado. Verificar manualmente se o Beneficiário já está cadastrado.')

    clv_insured = client.model('clv_insured')
    clv_insured_mng_relation = client.model('clv_insured_mng.relation')

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse(args)
    i = 0
    for insured_mng in insured_mng_browse:
        i += 1

        print(i, insured_mng.reg_number, insured_mng.name.encode('utf-8'),
              insured_mng.insurance_client_id.name.encode('utf-8'))

        insured_browse = clv_insured.browse(
            [('insurance_client_id', '=', insured_mng.insurance_client_id.id),
             ('name', '=', insured_mng.name),
             ])
        insured_ids = insured_browse.id

        if insured_ids != []:
            print('>>>>>', insured_ids)

            values = {
                'tag_ids': [(4, tag_id_VerificarDuplicidadeDeBeneficiario)],
                }
            clv_insured_mng.write(insured_mng.id, values)

            for insured_id in insured_ids:
                values = {
                    "insured_mng_id": insured_mng.id,
                    "insured_id": insured_id,
                    }
                relation_id = clv_insured_mng_relation.create(values).id

        insured_browse = clv_insured.browse(
            [('insurance_client_id', '=', insured_mng.insurance_client_id.id),
             ('reg_number', '=', insured_mng.reg_number),
             ])
        insured_ids = insured_browse.id

        if insured_ids != []:
            print('>>>>>', insured_ids)

            values = {
                'tag_ids': [(4, tag_id_VerificarDuplicidadeDeBeneficiario)],
                }
            clv_insured_mng.write(insured_mng.id, values)

            for insured_id in insured_ids:
                values = {
                    "insured_mng_id": insured_mng.id,
                    "insured_id": insured_id,
                    }
                relation_id = clv_insured_mng_relation.create(values).id

        # else:
        #     values = {
        #         'tag_ids': [(3, tag_id_VerificarDuplicidadeDeBeneficiario)],
        #         }
        #     clv_insured_mng.write(insured_mng.id, values)


def clv_insured_mng_updt_insured_code(client):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([('state', '=', 'revised'),
                                                 ('code', '=', False),
                                                 ])
    i = 0
    for insured_mng in insured_mng_browse:

        i += 1
        print(i, insured_mng.name, insured_mng.code)

        values = {
            'code': '/',
            }
        clv_insured_mng.write(insured_mng.id, values)


def clv_insured_mng_updt_insured_crd_code(client):

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([('state', '=', 'revised'),
                                                 ('crd_code', '=', False),
                                                 ])
    i = 0
    for insured_mng in insured_mng_browse:

        i += 1
        print(i, insured_mng.crd_name, insured_mng.crd_code)

        values = {
            'crd_code': '/',
            }
        clv_insured_mng.write(insured_mng.id, values)

    insured_mng_browse = clv_insured_mng.browse([('state', '=', 'revised'),
                                                 ('crd_code', '!=', False),
                                                 ])
    for insured_mng in insured_mng_browse:

        crd_code = insured_mng.crd_code
        code_form = crd_code

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

        i += 1
        print(i, insured_mng.crd_name, insured_mng.crd_code, code_form)

        values = {
            'crd_code': code_form,
            }
        clv_insured_mng.write(insured_mng.id, values)

    insured_mng_browse = clv_insured_mng.browse([('state', '=', 'revised'),
                                                 ('crd_code', '=', '0'),
                                                 ])
    for insured_mng in insured_mng_browse:

        i += 1
        print(i, insured_mng.crd_name, insured_mng.crd_code)

        values = {
            'crd_code': '/',
            }
        clv_insured_mng.write(insured_mng.id, values)

    print('--> i: ', i)


def clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME):

    date_inclusion = PREFIX

    insured_cat_id_titular = get_insured_category_id(client, 'Titular')
    insured_cat_id_dependente = get_insured_category_id(client, 'Dependente')
    insured_cat_id_ascendente = get_insured_category_id(client, 'Ascendente')

    batch_cat_id_producao = get_batch_category_id(client, 'Produção')
    batch_producao_id = get_batch_id(client,
                                     PRODUCTION_BATCH_NAME, 
                                     batch_cat_id_producao)

    batch_cat_id_cliente = get_batch_category_id(client, 'Cliente')
    batch_client_id = get_batch_id(client,
                                   CLIENT_BATCH_NAME, 
                                   batch_cat_id_cliente, 
                                   [(4, batch_producao_id)])

    batch_cat_id_familiar = get_batch_category_id(client, 'Grupo Familiar')

    print(batch_client_id, batch_producao_id)

    clv_address = client.model('clv_address')
    clv_insured = client.model('clv_insured')
    clv_insured_card = client.model('clv_insured_card')
    clv_insured_card_batch = client.model('clv_insured_card.batch')

    clv_insured_mng = client.model('clv_insured_mng')
    insured_mng_browse = clv_insured_mng.browse([('state', '=', 'waiting'),])

    i = 0
    for insured_mng in insured_mng_browse:

        if insured_mng.batch_name == CLIENT_BATCH_NAME:

            if insured_cat_id_titular in insured_mng.category_ids.id:
                i += 1
                print(i, insured_mng.name)

                seq_N += 1

                batch_id = get_batch_id(client,
                                        PREFIX + '-%0*d ' % (5, seq_N) + insured_mng.crd_name, 
                                        batch_cat_id_familiar, 
                                        [(4, batch_client_id)])

                if insured_mng.address_home_id == False:

                    values = {
                        "name": insured_mng.name,
                        "alias": insured_mng.addr_alias,
                        "code": insured_mng.addr_code,
                        'notes': insured_mng.addr_notes,
                        'street': insured_mng.addr_street,
                        'street2': insured_mng.addr_street2,
                        'zip': insured_mng.addr_zip,
                        'city': insured_mng.addr_city,
                        'state_id': insured_mng.addr_state_id,
                        'country_id': insured_mng.addr_country_id,
                        'email': insured_mng.addr_email,
                        'phone': insured_mng.addr_phone,
                        'fax': insured_mng.addr_fax,
                        'mobile': insured_mng.addr_mobile,
                        'l10n_br_city_id': insured_mng.addr_l10n_br_city_id,
                        'district': insured_mng.addr_district,
                        'number': insured_mng.addr_number,
                        }
                    address_id = clv_address.create(values).id

                    values = {
                        "address_home_id": address_id,
                        }
                    clv_insured_mng.write(insured_mng.id, values)

                else:
                    address_id = insured_mng.address_home_id

                if insured_mng.insured_id == False:
                    
                    values = {
                        "name": insured_mng.name,
                        "code": insured_mng.code,
                        "address_home_id": insured_mng.address_id,
                        "insurance_client_id": insured_mng.insurance_client_id.id,
                        "reg_number": insured_mng.reg_number,
                        "insurance_id": insured_mng.insurance_id.id,
                        "category_ids": [(4, insured_cat_id_titular)],
                        "cpf": insured_mng.cpf,
                        "rg": insured_mng.rg,
                        "birthday": insured_mng.birthday,
                        "gender": insured_mng.gender,
                        "date_inclusion": date_inclusion,
                        }
                    insured_id = clv_insured.create(values).id
                    
                    values = {
                        "insured_id": insured_id,
                        }
                    clv_insured_mng.write(insured_mng.id, values)

                if insured_mng.insured_card_id == False:

                    values = {
                        "name": insured_mng.crd_name,
                        "code": insured_mng.crd_code,
                        "insured_id": insured_id,
                        }
                    insured_card_id = clv_insured_card.create(values).id

                    values = {
                        "insured_card_id": insured_card_id,
                        }
                    clv_insured_mng.write(insured_mng.id, values)

                    values = {
                        "seq": seq_N,
                        "batch_id": batch_client_id,
                        "insured_card_id": insured_card_id,
                        }
                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                    values = {
                        "seq": seq_N,
                        "batch_id": batch_id,
                        "insured_card_id": insured_card_id,
                        }
                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                    values = {
                        "seq": seq_N,
                        "batch_id": batch_producao_id,
                        "insured_card_id": insured_card_id,
                        }
                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                client.exec_workflow('clv_insured_mng', 'button_done', insured_mng.id)

                insured_mng_browse_2 = clv_insured_mng.browse(\
                    [('reg_number', '=', insured_mng.reg_number), 
                     ('insurance_client_id', '=', insured_mng.insurance_client_id.id),
                     ('state', '=', 'waiting'),
                     ])
                for insured_mng_2 in insured_mng_browse_2:

                    if insured_mng_2.id != insured_mng.id:

                        values = {
                            "holder_id": insured_id,
                            "address_home_id": address_id,
                            }
                        clv_insured_mng.write(insured_mng_2.id, values)
                        
                        if (insured_cat_id_dependente in insured_mng_2.category_ids.id) or \
                           (insured_cat_id_ascendente in insured_mng_2.category_ids.id):

                            i += 1
                            print('>>>>>', i, insured_mng_2.name)

                            seq_N += 1

                            if insured_mng_2.insured_id == False:

                                values = {
                                    "name": insured_mng_2.name,
                                    "code": insured_mng_2.code,
                                    "address_home_id": address_id,
                                    "insurance_client_id": insured_mng_2.insurance_client_id.id,
                                    "reg_number": insured_mng_2.reg_number,
                                    "insurance_id": insured_mng_2.insurance_id.id,
                                    "category_ids": [(4, insured_cat_id_dependente)],
                                    "holder_id": insured_id,
                                    "cpf": insured_mng_2.cpf,
                                    "rg": insured_mng_2.rg,
                                    "birthday": insured_mng_2.birthday,
                                    "gender": insured_mng_2.gender,
                                    "date_inclusion": date_inclusion,
                                    }
                                insured_2_id = clv_insured.create(values).id

                                values = {
                                    "insured_id": insured_2_id,
                                    }
                                clv_insured_mng.write(insured_mng_2.id, values)

                            if insured_mng_2.insured_card_id == False:

                                values = {
                                    "name": insured_mng_2.crd_name,
                                    "code": insured_mng_2.crd_code,
                                    "insured_id": insured_2_id,
                                    }
                                insured_card_2_id = clv_insured_card.create(values).id

                                values = {
                                    "insured_card_id": insured_card_2_id,
                                    }
                                clv_insured_mng.write(insured_mng_2.id, values)

                                values = {
                                    "seq": seq_N,
                                    "batch_id": batch_client_id,
                                    "insured_card_id": insured_card_2_id,
                                    }
                                insured_card_batch_id = clv_insured_card_batch.create(values).id

                                values = {
                                    "seq": seq_N,
                                    "batch_id": batch_id,
                                    "insured_card_id": insured_card_2_id,
                                    }
                                insured_card_batch_id = clv_insured_card_batch.create(values).id

                                values = {
                                    "seq": seq_N,
                                    "batch_id": batch_producao_id,
                                    "insured_card_id": insured_card_2_id,
                                    }
                                insured_card_batch_id = clv_insured_card_batch.create(values).id

                                client.exec_workflow('clv_insured_mng', 'button_done', insured_mng_2.id)

            else:

                insured_mng_browse_3 = clv_insured_mng.browse([('id', '=', insured_mng.id),])

                if insured_mng_browse_3[0].state == 'waiting':

                    insured_browse = clv_insured.browse(\
                        [('reg_number', '=', insured_mng.reg_number), 
                         ('insurance_client_id', '=', insured_mng.insurance_client_id.id),
                         ])
                    for insured in insured_browse:

                        if insured_cat_id_titular in insured.category_ids.id:

                            print(0, insured.name)

                            insured_card_browse = clv_insured_card.browse([('insured_id', '=', insured.id),])

                            batch_id = get_batch_id(client,
                                                    PREFIX + '-%0*d ' % (5, seq_N) + \
                                                    insured_card_browse[0].name, 
                                                    batch_cat_id_familiar, 
                                                    [(4, batch_client_id)])

                            values = {
                                "holder_id": insured.id,
                                "address_home_id": insured.address_home_id.id,
                                }
                            clv_insured_mng.write(insured_mng.id, values)

                            if (insured_cat_id_dependente in insured_mng.category_ids.id) or \
                               (insured_cat_id_ascendente in insured_mng.category_ids.id):

                                i += 1
                                print('>>>>>', i, insured_mng.name)

                                seq_N += 1

                                if insured_mng_2.insured_id == False:

                                    values = {
                                        "name": insured_mng.name,
                                        "code": insured_mng.code,
                                        "address_home_id": insured.address_home_id.id,
                                        "insurance_client_id": insured_mng.insurance_client_id.id,
                                        "reg_number": insured_mng.reg_number,
                                        "insurance_id": insured_mng.insurance_id.id,
                                        "category_ids": [(4, insured_cat_id_dependente)],
                                        "holder_id": insured.id,
                                        "cpf": insured_mng.cpf,
                                        "rg": insured_mng.rg,
                                        "birthday": insured_mng.birthday,
                                        "gender": insured_mng.gender,
                                        "date_inclusion": date_inclusion,
                                        }
                                    insured_2_id = clv_insured.create(values).id

                                    values = {
                                        "insured_id": insured_2_id,
                                        }
                                    clv_insured_mng.write(insured_mng.id, values)

                                if insured_mng_2.insured_card_id == False:

                                    values = {
                                        "name": insured_mng.crd_name,
                                        "code": insured_mng.crd_code,
                                        "insured_id": insured_2_id,
                                        }
                                    insured_card_2_id = clv_insured_card.create(values).id

                                    values = {
                                        "insured_card_id": insured_card_2_id,
                                        }
                                    clv_insured_mng.write(insured_mng.id, values)

                                    values = {
                                        "seq": seq_N,
                                        "batch_id": batch_client_id,
                                        "insured_card_id": insured_card_2_id,
                                        }
                                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                                    values = {
                                        "seq": seq_N,
                                        "batch_id": batch_id,
                                        "insured_card_id": insured_card_2_id,
                                        }
                                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                                    values = {
                                        "seq": seq_N,
                                        "batch_id": batch_producao_id,
                                        "insured_card_id": insured_card_2_id,
                                        }
                                    insured_card_batch_id = clv_insured_card_batch.create(values).id

                                    client.exec_workflow('clv_insured_mng', 'button_done', insured_mng.id)

    print('--> i: ', i)


def clv_insured_updt_state_processing(client, args):

    clv_insured = client.model('clv_insured')

    clv_insured_card = client.model('clv_insured_card')
    insured_card_browse = clv_insured_card.browse(args)

    i = 0
    for insured_card in insured_card_browse:

        insured = clv_insured.browse([('id', '=', insured_card.insured_id.id),])[0]

        if insured.state == 'new':
            i += 1
            print(i, insured.name, insured.state)
            client.exec_workflow('clv_insured', 'button_process', insured.id)

    print('i: ', i)


def clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME):

    headings_insured_card = ['seq', 
                             'name', 'code',
                             'insurance', 'insurance_client',
                             ]
    file_insured_card = open(file_path, 'wb')
    writer_insured_card = csv.writer(file_insured_card, 
                                     delimiter = ';', 
                                     quotechar = '"', 
                                     quoting=csv.QUOTE_ALL)
    writer_insured_card.writerow(headings_insured_card)

    clv_insured_card = client.model('clv_insured_card')
    clv_insured = client.model('clv_insured')

    clv_batch = client.model('clv_batch')
    batch_browse = clv_batch.browse(\
        [('state', '=', 'processing'), 
         ('name', '=', PRODUCTION_BATCH_NAME),
         ])

    i = 0
    for batch in batch_browse:

        print(batch.name.encode("utf-8"))

        for insured_card_batch in batch.insured_card_batch_ids:

            i += 1

            insured_card = clv_insured_card.browse(
                [('id', '=', insured_card_batch.insured_card_id.id),])[0]

            insured = clv_insured.browse(
                [('id', '=', insured_card.insured_id.id),])[0]

            seq = insured_card_batch.seq
            crd_name = insured_card.name.encode("utf-8")
            crd_code = insured_card.code
            insurance = insured.insurance_id.name.encode("utf-8")
            insurance_client = insured.insurance_client_id.name.encode("utf-8")

            print(i, seq, crd_name, crd_code, insurance, insurance_client)

            row_insured_card = [seq, 
                                crd_name, crd_code,
                                insurance, insurance_client,
                                ]
            writer_insured_card.writerow(row_insured_card)

    file_insured_card.close()


def clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME):

    headings_insured = ['no', 
                        'batch_producao', 'batch_client', 'batch_familiar',
                        'reg_number', 'crd_code', 'crd_name',
                         ]
    file_insured = open(file_path, 'wb')
    writer_insured = csv.writer(file_insured, delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL)
    writer_insured.writerow(headings_insured)

    clv_insured_card = client.model('clv_insured_card')
    clv_insured = client.model('clv_insured')

    clv_batch = client.model('clv_batch')
    batch_browse = clv_batch.browse(\
        [('state', '=', 'checking'), 
         ('name', '=', PRODUCTION_BATCH_NAME),
         ])

    i = 0
    card_count = 0
    for batch in batch_browse:

        batch_producao = batch.name.encode("utf-8")

        i += 1
        print(i, batch.name.encode("utf-8"), batch.derived_batch_ids)

        print(batch.name.encode("utf-8"))

        for derived_batch in batch.derived_batch_ids:

            batch_client = derived_batch.name.encode("utf-8")

            if derived_batch.state == 'checking':
                i += 1
                print('>>>>', i, derived_batch.name.encode("utf-8"))

                for derived_batch_2 in derived_batch.derived_batch_ids:

                    batch_familiar = derived_batch_2.name.encode("utf-8")

                    if derived_batch_2.state == 'checking':
                        i += 1
                        print('>>>>>>>>', i, derived_batch_2.name.encode("utf-8"))

                        for insured_card_batch in derived_batch_2.insured_card_batch_ids:
                            i += 1

                            insured_card = clv_insured_card.browse(
                                [('id', '=', insured_card_batch.insured_card_id.id),])[0]

                            insured = clv_insured.browse(
                                [('id', '=', insured_card.insured_id.id),])[0]

                            crd_name = insured_card.name.encode("utf-8")
                            crd_code = insured_card.code
                            reg_number = insured.reg_number
                            category = insured.category_ids[0].name

                            if insured_card.state == 'processing':
                                card_count += 1
                                print('>>>>>>>>>>>>', i, 
                                                      batch_producao, batch_client, batch_familiar, 
                                                      reg_number, crd_code, crd_name,
                                                      category)

                                row_insured = [card_count, 
                                               batch_producao, batch_client, batch_familiar,
                                               reg_number, crd_code, crd_name,
                                               ]
                                writer_insured.writerow(row_insured)

    file_insured.close()

    print('i: ', i)
    print('card_count: ', card_count)


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

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2015-09-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20150928_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2015-09-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2015-09-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2015-09-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    ########################################

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

    # batch_name = 'HVC_20151028_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20151028_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # print('-->', client, batch_name, file_name, client_name)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2015-10-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20151028_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2015-10-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2015-10-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2015-10-28'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    ########################################

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

    # batch_name = 'HVC_20151125_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20151125_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # print('-->', client, batch_name, file_name, client_name)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2015-11-25'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20151125_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2015-11-25'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2015-11-25'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2015-11-25'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    ########################################

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

    # batch_name = 'HVC_20151231_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20160104_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # print('-->', client, batch_name, file_name, client_name)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2015-12-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20151231_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2015-12-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2015-12-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2015-12-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    ########################################

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

    # batch_name = 'HVC_20160129_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20160129_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # print('-->', client, batch_name, file_name, client_name)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2016-01-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20160129_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2016-01-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2016-01-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # ******* Skiped - Executed Manually *******
    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2016-01-31'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    ########################################

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

    # batch_name = 'PUB_20160201_01'
    # file_name = '/opt/openerp/biobox/data/PUB_20160201_01.txt'
    # client_name = 'PUB - Public Broker'
    # insurance_T = 'PUB - FLEX PARCEIRO'
    # insurance_D = ''
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2016-02-01'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'PUB_20160201_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2016-02-01'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2016-02-01'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # ******* Skiped - Executed Manually *******
    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2016-02-01'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    # 1 #######################################

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

    # batch_name = 'GSUL_20160218_01'
    # file_name = '/opt/openerp/biobox/data/GSUL_20160218_01.txt'
    # client_name = 'GSul - Serviços Administrativos'
    # insurance_T = 'GSUL - PLENO'
    # insurance_D = 'GSUL - COPAR 30'
    # insurance_A = 'GSUL - FLEX ACESSO'
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2016-02-22'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'GSUL_20160218_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2016-02-22'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2016-02-22'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # ******* Skiped - Executed Manually *******
    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2016-02-22'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    # 2 #######################################

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

    # batch_name = 'PUB_20160219_01'
    # file_name = '/opt/openerp/biobox/data/PUB_20160219_01.txt'
    # client_name = 'PUB - Public Broker'
    # insurance_T = 'PUB - FLEX PARCEIRO'
    # insurance_D = ''
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2016-02-23'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'PUB_20160219_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2016-02-23'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2016-02-23'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # ******* Skiped - Executed Manually *******
    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2016-02-23'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    ########################################

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

    # batch_name = 'HVC_20160229_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20160229_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # insurance_T = 'HVC - PLENO'
    # insurance_D = 'HVC - COPAR 25'
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # seq_N = 0
    # PREFIX = '2016-02-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20160229_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # PREFIX = '2016-02-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # PREFIX = '2016-02-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # PREFIX = '2016-02-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    # 2016-03-23 #######################################

    # 01 ##########

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

    # 02 ##########

    # batch_name = 'PUB_20160318_01'
    # file_name = '/opt/openerp/biobox/data/PUB_20160318_01.txt'
    # client_name = 'PUB - Public Broker'
    # insurance_T = 'PUB - FLEX PARCEIRO'
    # insurance_D = ''
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # batch_name = 'GSUL_20160321_01'
    # file_name = '/opt/openerp/biobox/data/GSUL_20160321_01.txt'
    # client_name = 'GSul - Serviços Administrativos'
    # insurance_T = 'GSUL - PLENO'
    # insurance_D = 'GSUL - COPAR 30'
    # insurance_A = 'GSUL - FLEX ACESSO'
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # 03 ##########

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # 04 ##########

    # seq_N = 0
    # PREFIX = '2016-03-18'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'PUB_20160318_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # seq_N = 0
    # PREFIX = '2016-03-21'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'GSUL_20160321_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # 05 ##########

    # PREFIX = '2016-03-18'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # PREFIX = '2016-03-21'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # 06 ##########

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # 07 ##########

    # PREFIX = '2016-03-18'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # PREFIX = '2016-03-21'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # 08 ##########

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # 09 ##########

    # PREFIX = '2016-03-21'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # PREFIX = '2016-03-18'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # 10 ##########

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    # 2016-03-29 #######################################

    # 01 ##########

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

    # 02 ##########

    # batch_name = 'HVC_20160328_01'
    # file_name = '/opt/openerp/biobox/data/HVC_20160328_01.txt'
    # client_name = 'HVC - Hospital Vera Cruz'
    # insurance_T = 'HVC - PLENO'
    # insurance_D = 'HVC - COPAR 25'
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # batch_name = 'VCAS_20160328_01'
    # file_name = '/opt/openerp/biobox/data/VCAS_20160328_01.txt'
    # client_name = 'VCAS - Vera Cruz Associação de Saúde'
    # insurance_T = 'VCAS - PLENO'
    # insurance_D = 'VCAS - COPAR 25'
    # insurance_A = ''
    # print('-->', client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)
    # print('--> Executing clv_insured_mng_import()...')
    # clv_insured_mng_import(client, batch_name, file_name, client_name, insurance_T, insurance_D, insurance_A)

    # 03 ##########

    # print('-->', client)
    # print('--> Executing clv_insured_mng_check_crd_name()...')
    # clv_insured_mng_check_crd_name(client)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_check_insured()...')
    # clv_insured_mng_check_insured(client, insured_args)

    # insured_args = [('state', '=', 'draft'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_revised()...')
    # clv_insured_mng_updt_state_revised(client, insured_args)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_code()...')
    # clv_insured_mng_updt_insured_code(client)

    # print('-->', client)
    # print('--> Executing clv_insured_mng_updt_insured_crd_code()...')
    # clv_insured_mng_updt_insured_crd_code(client)

    # insured_args = [('state', '=', 'revised'), ]
    # print('-->', client, insured_args)
    # print('--> Executing clv_insured_mng_updt_state_waiting()...')
    # clv_insured_mng_updt_state_waiting(client, insured_args)

    # 04 ##########

    # seq_N = 0
    # PREFIX = '2016-03-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'HVC_20160328_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # seq_N = 1000
    # PREFIX = '2016-03-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # CLIENT_BATCH_NAME = 'VCAS_20160328_01'
    # print('-->', client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)
    # print('--> Executing clv_insured_mng_create_insured()...')
    # clv_insured_mng_create_insured(client, seq_N, PREFIX, PRODUCTION_BATCH_NAME, CLIENT_BATCH_NAME)

    # 05 ##########

    # PREFIX = '2016-03-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # batch_args = [('state', '=', 'draft'),
    #               ('name', '=', PRODUCTION_BATCH_NAME),
    #               ]
    # print('-->', client)
    # print('--> Executing clv_batch_updt_state_processing()...')
    # clv_batch_updt_state_processing(client, batch_args)

    # 06 ##########

    # insured_card_args = [('state', '=', 'processing'), ]
    # print('-->', client, insured_card_args)
    # print('--> Executing clv_insured_updt_state_processing()...')
    # clv_insured_updt_state_processing(client, insured_card_args)

    # 07 ##########

    # PREFIX = '2016-03-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/insured_card_producao_' + PREFIX + '.csv'
    # print('-->', client, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_insured_card_export_producao()...')
    # clv_insured_card_export_producao(client, file_path, PRODUCTION_BATCH_NAME)

    # 08 ##########

    # batch_args = [('state', '=', 'processing'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_checking()...')
    # clv_batch_updt_state_checking(client, batch_args)

    # 09 ##########

    # PREFIX = '2016-03-29'
    # PRODUCTION_BATCH_NAME = PREFIX + ' Produção'
    # file_path = '/opt/openerp/biobox/data/protocolo_produção_' + PREFIX + '.csv'
    # print('-->', client, file_path, PRODUCTION_BATCH_NAME)
    # print('--> Executing clv_batch_producao_export_protocolo()...')
    # clv_batch_producao_export_protocolo(client, file_path, PRODUCTION_BATCH_NAME)

    # 10 ##########

    # batch_args = [('state', '=', 'checking'),
    #               ('name_category', '=', 'Grupo Familiar'),
    #               ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # batch_args = [('state', '=', 'checking'), ]
    # print('-->', client, batch_args)
    # print('--> Executing clv_batch_updt_state_done()...')
    # clv_batch_updt_state_done(client, batch_args)

    # card_args = [('state', '=', 'processing'), ]
    # print('-->', client, card_args)
    # print('--> Executing clv_insured_card_updt_state_active()...')
    # clv_insured_card_updt_state_active(client, card_args)

    print('--> clv_insured_mng.py')
    print('--> Execution time:', secondsToStr(time() - start))
