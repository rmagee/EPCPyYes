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
from EPCPyYes.core.v1_2.helpers import get_current_utc_time_and_offset, \
    gtin_to_urn
from EPCPyYes.core.v1_2.CBV.instance_lot_master_data import \
    InstanceLotMasterDataAttribute, \
    LotLevelAttributeName, ItemLevelAttributeName
from EPCPyYes.core.v1_2.events import Action, QuantityElement
from EPCPyYes.core.v1_2.CBV.business_steps import BusinessSteps
from EPCPyYes.core.v1_2.CBV.dispositions import Disposition
from EPCPyYes.core.v1_2.CBV import helpers


class JSONTestCase(CoreEventTests):

    def test_epcis_base_template(self):
        oe1 = self.create_object_event_json_template()
        oe2 = self.create_object_event_json_template()

        object_events = [oe1, oe2]
        ag1 = self.create_aggregation_event(self.create_epcs(1000, 1009),
                                            gtin_to_urn('305555', '2',
                                                        '555555', '235'))
        ag2 = self.create_aggregation_event(self.create_epcs(1010, 1019),
                                            gtin_to_urn('305555', '2',
                                                        '555555', '216'))
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        epcs = self.create_epcs(1000, 1010)
        transaction_event = self.create_transaction_json_event(epcs, parent_id)
        txe = self.create_transformation_event()
        #header = self.create_sbdh() # TODO add the header back in
        epcis_document = json_events.EPCISDocument(
            header=None,
            object_events=object_events,
            aggregation_events=[ag1, ag2],
            transaction_events=[transaction_event],
            transformation_events=[txe]
        )
        print(epcis_document.render_pretty())

    def test_epcis_base_template_2(self):
        oe1 = self.create_object_event_json_template()
        oe2 = self.create_object_event_json_template()

        object_events = [oe1, oe2]
        ag1 = self.create_aggregation_event(self.create_epcs(1000, 1009),
                                            gtin_to_urn('305555', '2',
                                                        '555555', '235'))
        ag2 = self.create_aggregation_event(self.create_epcs(1010, 1019),
                                            gtin_to_urn('305555', '2',
                                                        '555555', '216'))
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        epcs = self.create_epcs(1000, 1010)
        transaction_event = self.create_transaction_json_event(epcs, parent_id)
        txe = self.create_transformation_event()
        #header = self.create_sbdh() # TODO add the header back in
        epcis_document = json_events.EPCISDocument(
            header=None,
            object_events=object_events,
            aggregation_events=[],
            transaction_events=[],
            transformation_events=[]
        )
        print(epcis_document.render_pretty())
        epcis_document = json_events.EPCISDocument(
            header=None,
            object_events=[],
            aggregation_events=[ag1, ag2],
            transaction_events=None,
            transformation_events=[txe]
        )
        print(epcis_document.render_pretty())

    def test_json_agg_event(self):
        '''
        Creates and then validates the JSON data representation
        of an EPCIS Aggregation Event
        '''
        epcs = self.create_epcs(1000, 1010)
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        # get the current time and tz
        ae = self.create_aggregation_event(epcs, parent_id)
        print(ae.render_pretty())

    def test_json_object_event(self):
        '''
        Creates and then validates the JSON data representation
        of an EPCIS Object Event
        '''
        oe = self.create_object_event_json_template()
        print(oe.render_pretty())

    def test_json_transformation_event(self):
        xe = self.create_transformation_event()
        print(xe.render_pretty())

    def test_permutated_object_event_data(self):
        '''
        Tests the output when elements are added and removed
        to ensure commas are not messing with the validity of the
        JSON.
        '''
        epcs = self.create_epcs(1000, 1010)
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        # get the current time and tz
        ae = self.create_object_event_json_template()
        ae.biz_step = None
        ae.destination_list = None
        print(ae.render_pretty())
        ae = self.create_object_event_json_template()
        ae.child_quantity_list = None
        print(ae.render_pretty())
        ae = self.create_object_event_json_template()
        ae.record_time = None
        ae.event_timezone_offset = None
        ae.disposition = None
        print(ae.render_pretty())
        ae = self.create_object_event_json_template()
        ae.ilmd = None
        print(ae.render_pretty())

    def test_permutated_event_data(self):
        '''
        Tests the output when elements are added and removed
        to ensure commas are not messing with the validity of the
        JSON.
        '''
        epcs = self.create_epcs(1000, 1010)
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        # get the current time and tz
        ae = self.create_aggregation_event(epcs, parent_id)
        ae.biz_step = None
        ae.destination_list = None
        print(ae.render_pretty())
        ae = self.create_aggregation_event(epcs, parent_id)
        ae.child_quantity_list = None
        print(ae.render_pretty())
        ae = self.create_aggregation_event(epcs, parent_id)
        ae.record_time = None
        ae.event_timezone_offset = None
        ae.disposition = None
        print(ae.render())
        print(ae.render_pretty())
        ae = self.create_aggregation_event(epcs, parent_id)
        ae.business_transaction_list = None
        print(ae.render())
        print(ae.render_pretty())

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

    def test_transaction_event_template(self):
        epcs = self.create_epcs(1000, 1010)
        parent_id = gtin_to_urn('305555', '1', '555551', 1000)
        te = self.create_transaction_json_event(epcs, parent_id)
        # render the event using it's default template
        data = te.render_pretty()
        print(data)
        # make sure the data we want is there
        self.assertTrue('+00:00' in data)
        self.assertIn('urn:epc:id:sgtin:305555.1555555.1000',
                      data,
                      'URN for start SGTIN not present.')
        self.assertIn('urn:epc:id:sgtin:305555.1555555.1001',
                      data,
                      'URN for start SGTIN not present.')
        self.assertIn('ADD', data,
                      'EPCIS action not present.')
        self.assertIn(BusinessSteps.shipping.value, data,
                      'Business step not present')
        self.assertIn(Disposition.in_transit.value, data,
                      'Disposition not present')

    def create_object_event_json_template(self):
        epcs = self.create_epcs()
        # get the current time and tz
        now, tzoffset = get_current_utc_time_and_offset()
        business_transaction_list = self.create_business_transaction_list()
        biz_location, read_point, source_list = self.create_source_list()
        destination_list = self.create_destination_list()
        ilmd = [
            InstanceLotMasterDataAttribute(
                name=LotLevelAttributeName.itemExpirationDate.value,
                value='2015-12-31'),
            InstanceLotMasterDataAttribute(
                name=ItemLevelAttributeName.lotNumber.value,
                value='DL232')
        ]
        oe = self.create_json_object_event(biz_location, business_transaction_list,
                                      destination_list, epcs, now, read_point,
                                      source_list, tzoffset,
                                      action=Action.add.value,
                                      ilmd=ilmd)
        oe.clean()
        return oe

    def create_json_object_event(self, biz_location, business_transaction_list,
                            destination_list, epcs, now, read_point,
                            source_list, tzoffset, action=None, ilmd=None):
        # create the event
        event_id = str(uuid.uuid4())
        error_declaration = self.create_error_declaration()
        oe = json_events.ObjectEvent(now, tzoffset,
                         record_time=now,
                         action=action,
                         epc_list=epcs,
                         biz_step=BusinessSteps.commissioning.value,
                         disposition=Disposition.encoded.value,
                         business_transaction_list=business_transaction_list,
                         biz_location=biz_location,
                         read_point=read_point,
                         source_list=source_list,
                         destination_list=destination_list,
                         ilmd=ilmd, error_declaration=error_declaration,
                         event_id=event_id)
        return oe

    def create_transaction_json_event(self, epcs, parent_id):
        now, tzoffset = get_current_utc_time_and_offset()
        business_transaction_list = self.create_business_transaction_list()
        biz_location, read_point, source_list = self.create_source_list()
        destination_list = self.create_destination_list()
        trade_item = helpers.make_trade_item_master_data_urn('305555', '0',
                                                             '555551')
        disposition = Disposition.in_transit.value
        biz_step = BusinessSteps.shipping.value
        quantity_list = [
            QuantityElement(epc_class=trade_item, quantity=100),
            QuantityElement(epc_class=trade_item, quantity=94.3,
                            uom='LB')]

        event_id = str(uuid.uuid4())
        error_declaration = self.create_error_declaration()

        te = json_events.TransactionEvent(
            now,
            tzoffset,
            now,
            action=Action.add.value,
            parent_id=parent_id,
            epc_list=epcs,
            business_transaction_list=business_transaction_list,
            biz_location=biz_location,
            read_point=read_point,
            source_list=source_list,
            destination_list=destination_list,
            biz_step=biz_step,
            disposition=disposition,
            event_id=event_id,
            error_declaration=error_declaration)
        te.quantity_list = quantity_list
        return te

    def create_transformation_event(self):
        now, tzoffset = get_current_utc_time_and_offset()
        event_id = str(uuid.uuid4())
        error_declaration = self.create_error_declaration()
        input_epcs = self.create_epcs(1000, 1010)
        output_epcs = self.create_epcs(2000, 2010)
        business_transaction_list = self.create_business_transaction_list()
        biz_location, read_point, source_list = self.create_source_list()
        destination_list = self.create_destination_list()

        ilmd = [
            InstanceLotMasterDataAttribute(
                name=LotLevelAttributeName.itemExpirationDate.value,
                value='2015-12-31'),
            InstanceLotMasterDataAttribute(
                name=ItemLevelAttributeName.lotNumber.value,
                value='DL232')
        ]

        trade_item = helpers.make_trade_item_master_data_urn('305555', '0',
                                                             '555551')
        output_quantity_list = [
            QuantityElement(epc_class=trade_item, quantity=10, uom='EA'),
            QuantityElement(epc_class=trade_item, quantity=94.3,
                            uom='LB')]
        input_quantity_list = [
            QuantityElement(epc_class=trade_item, quantity=100, uom='EA'),
            QuantityElement(epc_class=trade_item, quantity=94.3,
                            uom='LB')]

        te = json_events.TransformationEvent(
            now, tzoffset, now, event_id, input_epcs,
            input_quantity_list=input_quantity_list,
            output_epc_list=output_epcs,
            output_quantity_list=output_quantity_list,
            transformation_id=str(uuid.uuid4()),
            biz_step=BusinessSteps.repackaging.value,
            disposition=Disposition.returned.value,
            read_point=read_point,
            biz_location=biz_location,
            business_transaction_list=business_transaction_list,
            source_list=source_list,
            destination_list=destination_list,
            error_declaration=error_declaration,
            ilmd=ilmd)
        return te