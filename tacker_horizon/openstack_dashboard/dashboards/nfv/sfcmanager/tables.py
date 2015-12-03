# Copyright 2015 Brocade Communications System, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from horizon import messages
from horizon import tables
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from django.utils.translation import ungettext_lazy
from tacker_horizon.openstack_dashboard import api
from openstack_dashboard import policy
import logging
LOG = logging.getLogger(__name__)

class SFCItem(object):
    def __init__(self , id, name, description, status, chain, tenant_id, instance_id, infra_driver, attributes, symmetrical):
        self.name = name
        self.description = description
        self.id = id
        self.status = status
        self.chain = chain
        self.tenant_id = tenant_id
        self.instance_id = instance_id
        self.infra_driver = infra_driver
        self.attributes = attributes
        self.symmetrical = symmetrical


class SFCItemList():
    SFCItemLIST_P = []

    @classmethod
    def get_obj_given_sfc_id(cls, sfc_id):
        for obj in cls.SFCItemLIST_P:
            if obj.id == sfc_id:
                return obj

    @classmethod
    def add_item(cls, item):
        cls.SFCItemLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.SFCItemLIST_P = []

class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class ActionUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, id):
        try:
            sfc = api.tacker.get_sfc(request, id)

            item = SFCItemList.get_obj_given_sfc_id(sfc['id'])

            return item
        except Http404:
            raise
        except Exception as e:
            messages.error(request, e)
            raise

class DeleteSFC(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete SFC",
            u"Delete SFC",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete SFC",
            u"Delete SFCs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_sfc(request,obj_id)

class AddServicesLink(tables.LinkAction):
    name = "addSFC"
    verbose_name = _("create a Service Function Chain")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:sfcmanager:addsfc"

class SFCTable(tables.DataTable):
    id = tables.Column("id",verbose_name=_("ID"))

    name = tables.Column("name", \
                         verbose_name=_("SFC Name"))
    description = tables.Column("description", \
                           verbose_name=_("Description"))
    status = tables.Column('status', verbose_name=_("Status"))
    chain = tables.Column("chain", verbose_name=_("Chain"))
    LOG.info(">>>>>>chain = %s " % chain)
    tenant_id = tables.Column("tanant_id", verbose_name=_("Tenant ID"))
    instance_id = tables.Column("instance_id", verbose_name=_("Instance ID"))
    infra_driver = tables.Column("infra_driver", verbose_name=_("Infra Driver"))
    attributes = tables.Column("attributes", verbose_name=_("Attributes"))
    symmetrical = tables.Column("symmetrical", verbose_name=_("Symmetrical"))

    class Meta:
        name = "SFC"
        verbose_name = _("SFC")
        SFC_columns = ["SFC",]
        row_class = ActionUpdateRow
        table_actions = (MyFilterAction,AddServicesLink,DeleteSFC)
