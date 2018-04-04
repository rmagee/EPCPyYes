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
# Copyright 2018 SerialLab Corp.  All rights reserved.
'''
This module just overrides the constructors of the template_events
EPCIS classes in order to specify JSON templates instead of the
EPCIS XML templates in the template_events module.
'''
import json
from datetime import datetime
from EPCPyYes.core.v1_2 import template_events
from EPCPyYes.core.v1_2.events import Action, ErrorDeclaration


class JSONFormatMixin:
    '''
    Provides formatting options for JSON output such as compression (stripping
    of white space) and pretty printing. Must be used on a class that already
    utilizes the `template_events.TemplateMixin`.
    '''

    def render_pretty(self, indent=4, sort_keys=False):
        '''
        Pretty prints the JSON output.
        :param indent: Default of 4.
        :param sort_keys: Default of False.
        :return: A formatted JSON string indented and (potentially) sorted.
        '''
        return json.dumps(json.loads(self.render()), indent=indent,
                          sort_keys=sort_keys)

    def render_compressed(self):
        '''
        Will strip all white space from the template output.
        :return: A JSON string with no whitespace.
        '''
        return json.dumps(json.loads(self.render()))


class ObjectEvent(template_events.ObjectEvent, JSONFormatMixin):
    def __init__(self, event_time: datetime = datetime.utcnow().isoformat(),
                 event_timezone_offset: str = '+00:00',
                 record_time: datetime = None, action: str = Action.add.value,
                 epc_list: list = None, biz_step=None, disposition=None,
                 read_point=None, biz_location=None, event_id: str = None,
                 error_declaration: ErrorDeclaration = None,
                 source_list: list = None, destination_list: list = None,
                 business_transaction_list: list = None, ilmd: list = None,
                 quantity_list: list = None):
        super().__init__(event_time, event_timezone_offset, record_time,
                         action, epc_list, biz_step, disposition, read_point,
                         biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list, ilmd, quantity_list)
        self.template = self._env.get_template("json/object_event.json")


class AggregationEvent(template_events.AggregationEvent, JSONFormatMixin):
    def __init__(self, event_time: datetime = datetime.utcnow().isoformat(),
                 event_timezone_offset: str = '+00:00',
                 record_time: datetime = None, action: str = Action.add.value,
                 parent_id: str = None, child_epcs: list = None,
                 child_quantity_list: list = None, biz_step: str = None,
                 disposition: str = None, read_point: str = None,
                 biz_location: str = None, event_id: str = None,
                 error_declaration: ErrorDeclaration = None, source_list=None,
                 destination_list=None, business_transaction_list=None):
        super().__init__(event_time, event_timezone_offset, record_time,
                         action, parent_id, child_epcs, child_quantity_list,
                         biz_step, disposition, read_point, biz_location,
                         event_id, error_declaration, source_list,
                         destination_list, business_transaction_list)
        self.template = self._env.get_template("json/aggregation_event.json")


class TransactionEvent(template_events.TransactionEvent, JSONFormatMixin):
    def __init__(self, event_time: datetime = datetime.utcnow().isoformat(),
                 event_timezone_offset: str = '+00:00',
                 record_time: datetime = None, action: str = Action.add.value,
                 parent_id: str = None, epc_list: list = None,
                 biz_step: str = None, disposition: str = None,
                 read_point: str = None, biz_location: str = None,
                 event_id: str = None,
                 error_declaration: ErrorDeclaration = None, source_list=None,
                 destination_list=None, business_transaction_list=None,
                 quantity_list: list = None):
        super().__init__(event_time, event_timezone_offset, record_time,
                         action, parent_id, epc_list, biz_step, disposition,
                         read_point, biz_location, event_id, error_declaration,
                         source_list, destination_list,
                         business_transaction_list, quantity_list)
        self.template = self._env.get_template("json/transaction_event.json")


class TransformationEvent(template_events.TransformationEvent,
                          JSONFormatMixin):
    def __init__(self, event_time: datetime = datetime.utcnow().isoformat(),
                 event_timezone_offset: str = '+00:00',
                 record_time: datetime = None, event_id: str = None,
                 input_epc_list=None, input_quantity_list=None,
                 output_epc_list=None, output_quantity_list=None,
                 transformation_id=None, biz_step: str = None,
                 disposition: str = None, read_point: str = None,
                 biz_location: str = None, business_transaction_list=None,
                 source_list=None, destination_list=None, ilmd=None,
                 error_declaration: ErrorDeclaration = None):
        super().__init__(event_time, event_timezone_offset, record_time,
                         event_id, input_epc_list, input_quantity_list,
                         output_epc_list, output_quantity_list,
                         transformation_id, biz_step, disposition, read_point,
                         biz_location, business_transaction_list, source_list,
                         destination_list, ilmd, error_declaration)
        self.template = self._env.get_template(
            "json/transformation_event.json")
