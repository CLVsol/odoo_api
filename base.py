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

import re


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t*1000,), 1000, 60, 60])


def autoIncrement(start=0, step=1):
    i = start
    while 1:
        yield i
        i += step


def validate_cpf(cpf):

    if not cpf.isdigit():
        cpf = re.sub('[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    cpf = map(int, cpf)
    new = cpf[:9]
    while len(new) < 11:
        r = sum([(len(new) + 1 - i) * v for i, v in enumerate(new)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        new.append(f)
    if new == cpf:
        return True
    return False
