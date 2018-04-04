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

import uuid
import json
from EPCPyYes.core.v1_2 import json_events
from EPCPyYes.core.tests.test_template_events import CoreEventTests
from EPCPyYes.core.v1_2.helpers import gtin_to_urn
from EPCPyYes.core.v1_2.events import Action, QuantityElement

from EPCPyYes.core.v1_2.CBV import helpers


class JSONTestCase(CoreEventTests):

    def test_json_agg_event(self):
        epcs = self.create_epcs(1000, 1010)
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        # get the current time and tz
        ae = self.create_aggregation_event(epcs, parent_id)
        json.loads("{%s}" % ae.render())
        print("{%s}" % ae.render())

    def create_aggregation_event(self, epcs, parent_id):
        business_transaction_list = self.create_business_transaction_list()
        biz_location, read_point, source_list = self.create_source_list()
        destination_list = self.create_destination_list()
        trade_item = helpers.make_trade_item_master_data_urn('305555', '0',
                                                             '555551')
        child_quantity_list = [
            QuantityElement(epc_class=trade_item, quantity=100),
            QuantityElement(epc_class=trade_item, quantity=94.3,
                            uom='LB')]
        event_id = str(uuid.uuid4())
        error_declaration = self.create_error_declaration()
        ae = json_events.AggregationEvent(
            action=Action.add.value,
            parent_id=parent_id, child_epcs=epcs,
            business_transaction_list=business_transaction_list,
            biz_location=biz_location, read_point=read_point,
            source_list=source_list,
            destination_list=destination_list,
            child_quantity_list=child_quantity_list,
            error_declaration=error_declaration,
            event_id=event_id
        )
        return ae
