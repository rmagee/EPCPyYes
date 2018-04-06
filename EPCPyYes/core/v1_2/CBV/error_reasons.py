# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 Rob Magee.  All rights reserved.

from enum import Enum


class ErrorReason(Enum):
    '''
    As defined in section 7.5 of the CBV standard.
    '''
    did_not_occur = 'urn:epcglobal:cbv:er:did_not_occur'
    incorrect_data = 'urn:epcglobal:cbv:er:incorrect_data'

    def __str__(self):
        return self.value
