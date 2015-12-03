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


from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs


from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.api import tacker as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.sfcmanager import tables
from tacker_horizon.openstack_dashboard.dashboards.nfv.sfcmanager.tables import SFCItemList,SFCItem
import logging
LOG = logging.getLogger(__name__)

class SFCTab(tabs.TableTab):
    name = _("SFC Tab")
    slug = "sfc_tab"
    table_classes = (tables.SFCTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def build_dict_vnfs(self, list_vnfs):
        dict_vnfs = {}
        for vnf in list_vnfs:
            dict_vnfs[vnf['id']] = vnf['name']
        return dict_vnfs

    def _get_vnf_names(self, list_vnf_ids, dict_vnfs):
        vnf_names = []
        for vnf_id in list_vnf_ids:
            vnf_names.append(dict_vnfs[vnf_id])
        return vnf_names
    def get_SFC_data(self):
        try:

            self._has_more = True
            SFCItemList.clear_list()
            sfcs = api.tacker.sfc_list(self.request)
            print "SFC Listing: " + str(sfcs)
            list_vnfs = tacker_api.vnf_list(self.request)

            dict_vnfs = self.build_dict_vnfs(list_vnfs)
            LOG.debug(">>>>>>>dict of vnfs on get_SFC_data: %s" % dict_vnfs)
            for sfc in sfcs:
                LOG.info(">>>>>>>>>>>>>>sfc includes: %s" % sfc)
                LOG.debug(">>>>>>>>>>>>>sfc chain: %s" % sfc["chain"])
                vnf_names = self._get_vnf_names(sfc["chain"],dict_vnfs)
                obj = SFCItem(status=sfc['status'],
                                       name=sfc['name'],
                                       description=sfc['description'],
                                       chain=vnf_names,
                                       tenant_id=sfc['tenant_id'],
                                       instance_id=sfc['instance_id'],
                                       infra_driver=sfc['infra_driver'],
                                       attributes=sfc['attributes'],
                                       symmetrical=sfc['symmetrical'],
                                       id=sfc['id'],
                                       )
                LOG.info(">>>>>>>>>>>object value for SFClassifierItem :   %s" % obj)
                SFCItemList.add_item(obj)
            return SFCItemList.SFCItemLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class SFCTabs(tabs.TabGroup):
    slug = "sfcmanager_tabs"
    tabs = (SFCTab,)
    sticky = True
