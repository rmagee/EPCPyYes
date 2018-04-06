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
# Copyright 2015 Rob Magee.  All rights reserved.
from typing import List
import uuid
from json import JSONEncoder
from EPCPyYes.core.v1_2 import events
from EPCPyYes.core.SBDH import sbdh

QList = List[events.QuantityElement]

import json


class JSONFormatMixin:
    '''
    Provides formatting options for JSON output such as compression (stripping
    of white space) and pretty printing. Must be used on a class that already
    utilizes the `template_events.TemplateMixin`.
    '''

    def render_pretty_json(self, indent=4, sort_keys=False):
        '''
        Pretty prints the JSON output.
        :param indent: Default of 4.
        :param sort_keys: Default of False.
        :return: A formatted JSON string indented and (potentially) sorted.
        '''
        return json.dumps(self.encoder.default(self), indent=indent,
                          sort_keys=sort_keys)

    def render_json(self):
        '''
        Will strip all white space from the template output.
        :return: A JSON string with no whitespace.
        '''
        return self.encoder.encode(self)


class SourceListJSONEncoder(JSONEncoder):
    def default(self, o):
        return {
            o.type: o.source
        }


class QuantityMixin:
    def get_quantity_list(self, list: QList):
        if list:
            ret = [{"epcClass": item.epc_class,
                    "quantity": item.quantity,
                    "uom": item.uom}
                   for item in list]
        else:
            ret = {}
        return ret


class ErrorDeclarationMixin:
    '''
    Handles encoding the error declarations for encoders that require this.
    '''

    def get_error_declaration(self,
                              error_declaration: events.ErrorDeclaration):
        if error_declaration:
            return {
                "declarationTime": error_declaration.declaration_time,
                "reason": error_declaration.reason,
                "correctiveEventIDs": [id for id in
                                       error_declaration.corrective_event_ids]
            }


class ListMixin:
    '''
    Handles the source destination BT and ILMD lists for encoders that
    require these.
    '''

    def get_source_list(self, o):
        '''
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of source values.
        '''
        if o.source_list:
            ret = {item.type: item.source for item in o.source_list}
        else:
            ret = {}
        return ret

    def get_destination_list(self, o):
        '''
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of destination values.
        '''
        if o.destination_list:
            ret = {item.type: item.destination for item in o.destination_list}
        else:
            ret = {}
        return ret

    def get_business_transaction_list(self, o):
        '''
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of BT values.
        '''
        if o.business_transaction_list:
            ret = {str(bt.biz_transaction): str(bt.type) for bt in
                   o.business_transaction_list}
        else:
            ret = {}
        return ret

    def get_ilmd_list(self, o):
        '''
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of ILMD values.
        '''
        if o.ilmd:
            ret = {str(item.name): item.value for item in o.ilmd}
        else:
            ret = {}
        return ret


class EPCISEventEncoder(JSONEncoder, ErrorDeclarationMixin,
                        QuantityMixin):
    '''
    All EPCIS classes share these common elements.  This is the base
    encoder.
    '''

    def default(self, o: events.EPCISEvent):
        ret = {
            'eventID': o.event_id or uuid.uuid4().hex,
            'eventTime': o.event_time,
            'eventTimezoneOffset': o.event_timezone_offset,
            'recordTime': o.record_time,
            'errorDeclaration': self.get_error_declaration(
                o.error_declaration),
        }
        return ret


class EPCISBusinessEventEncoder(EPCISEventEncoder, ListMixin):
    '''
    These elements are shared by the object, aggregation and transaction
    event classes- this is the base for those.
    '''

    def default(self, o):
        if isinstance(o, events.EPCISBusinessEvent):
            ret = super(EPCISBusinessEventEncoder, self).default(o)
            ret.update(
                {

                    'action': o.action,
                    'disposition': o.disposition,
                    'bizStep': o.biz_step,
                    'readPoint': o.read_point,
                    'bizLocation': o.biz_location,
                    'sourceList': self.get_source_list(o),
                    'destinationList': self.get_destination_list(o),
                    'businessTransactionList': \
                        self.get_business_transaction_list(o)
                }
            )
            return ret


class ObjectEventEncoder(EPCISBusinessEventEncoder, ListMixin):
    '''
    Encodes an `EPCPyYes.core.v1_2.template_events.ObjectEvent` to
    JSON.
    '''

    def default(self, o):
        if isinstance(o, events.ObjectEvent):
            ret = super(ObjectEventEncoder,
                        self).default(o)
            ret.update(
                {
                    'epc_list': [epc for epc in o.epc_list],
                    'ilmd': self.get_ilmd_list(o),
                    'quantity_list': self.get_quantity_list(o.quantity_list),
                }
            )
            return {'objectEvent': ret}


class AggregationEventEncoder(EPCISBusinessEventEncoder):
    '''
    Encodes an `EPCPyYes.core.v1_2.template_events.AggregationEvent` to
    JSON.
    '''

    def default(self, o: events.AggregationEvent):
        ret = super().default(o)
        ret.update(
            {
                "parentID": o.parent_id,
                "childEPCs": [epc for epc in o.child_epcs],
                "childQuantityList": self.get_quantity_list(
                    o.child_quantity_list)
            }
        )
        return {'aggregationEvent': ret}


class TransactionEventEncoder(EPCISBusinessEventEncoder):
    '''
    Encodes an `EPCPyYes.core.v1_2.template_events.TransactionEvent` to
    JSON.
    '''

    def default(self, o: events.TransactionEvent):
        ret = super().default(o)
        ret.update(
            {
                "parentID": o.parent_id,
                "epcList": [epc for epc in o.epc_list],
                "quantityList": self.get_quantity_list(o.quantity_list)
            }
        )
        return {"transactionEvent": ret}


class TransformationEventEncoder(EPCISEventEncoder, ListMixin):
    '''
    Encodes an `EPCPyYes.core.v1_2.template_events.TransformationEvent` to
    JSON.  This class can not inherit from the business base class due
    to its radically different structure and general purpose.
    '''

    def default(self, o: events.TransformationEvent):
        ret = super(TransformationEventEncoder, self).default(o)
        ret.update(
            {
                "inputEPCList": [epc for epc in o.input_epc_list],
                "inputQuantityList": self.get_quantity_list(
                    o.input_quantity_list),
                "outputEPCList": [epc for epc in o.output_epc_list],
                "outputQuantityList": self.get_quantity_list(
                    o.output_quantity_list),
                "transformationID": o.transformation_id,
                "bizStep": str(o.biz_step),
                "bizLocation": o.biz_location,
                "disposition": str(o.disposition),
                "readPoint": o.read_point,
                "bizLocation": o.biz_location,
                "bizTransactionList": self.get_business_transaction_list(o),
                "sourceList": self.get_source_list(o),
                "destinationList": self.get_destination_list(o),
                "ilmd": self.get_ilmd_list(o)
            }
        )
        return {"transformationEvent": ret}


class PartnerIdentificationEncoder(JSONEncoder):
    '''
    PartnerID encoder for the SBDH header.
    '''

    def default(self, o: sbdh.PartnerIdentification):
        if o:
            ret = {
                "authority": o.authority,
                "value": o.value
            }
        else:
            ret = {}
        return ret


class PartnerEncoder(JSONEncoder):
    def default(self, o: sbdh.Partner):
        pije = PartnerIdentificationEncoder()
        ret = {
            "partnerType": str(o.partner_type),
            "partnerID": pije.default(o.partner_id),
            "contact": o.contact,
            "emailAddress": o.email_address,
            "faxNumber": o.fax_number,
            "telephoneNumber": o.telephone_number,
            "contactTypeIdentifier": o.contact_type_identifier
        }
        return ret


class DocumentIdentificationEncoder(JSONEncoder):
    def default(self, o: sbdh.DocumentIdentification):
        if o.creation_date_and_time:
            creation_date_and_time = o.creation_date_and_time if \
                isinstance(o.creation_date_and_time, str) \
                else o.creation_date_and_time.isoformat()
        else:
            creation_date_and_time = None
        ret = {
            "standard": o.standard,
            "typeVersion": o.type_version,
            "instanceIdentifier": o.instance_identifier,
            "documentType": str(o.document_type),
            "mutlipleType": str(
                o.multiple_type).lower() if o.multiple_type else None,
            "creationDateAndTime": creation_date_and_time
        }
        return ret


class StandardBusinessDocumentHeaderEncoder(JSONEncoder):
    def default(self, o: sbdh.StandardBusinessDocumentHeader):
        dije = DocumentIdentificationEncoder()
        pe = PartnerEncoder()
        ret = {
            "namespace": o.namespace,
            "schemaLocation": o.schema_location,
            "documentIdentification": dije.default(o.document_identification),
            "partners": [pe.default(partner) for partner in o.partners]
        }
        return ret


class EPCISDocumentEncoder(JSONEncoder):
    def default(self, o: events.EPCISDocument):
        if o.created_date:
            created_date = o.created_date if \
                isinstance(o.created_date, str) \
                else o.created_date.isoformat()
        else:
            created_date = None
        sbdh = StandardBusinessDocumentHeaderEncoder()
        obj = ObjectEventEncoder()
        agg = AggregationEventEncoder()
        trans = TransformationEventEncoder()
        xact = TransactionEventEncoder()
        ret = {}
        if o.header:
            ret["header"] = sbdh.default(o.header)
        ret["events"] = self.list_events(o.object_events, obj) + \
                        self.list_events(o.aggregation_events, agg) + \
                        self.list_events(o.transaction_events, xact) + \
                        self.list_events(o.transformation_events, trans)

        ret["createdDate"] = created_date
        return ret

    def list_events(self, event_list, encoder):
        return [encoder.default(event) for event in event_list] or []
