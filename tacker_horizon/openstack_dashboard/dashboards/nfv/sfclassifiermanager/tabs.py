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
from tacker_horizon.openstack_dashboard.dashboards.nfv.sfclassifiermanager import tables
from tacker_horizon.openstack_dashboard.dashboards.nfv.sfclassifiermanager.tables import SFClassifierTable, SFClassifierItem
from tacker_horizon.openstack_dashboard.dashboards.nfv.sfclassifiermanager.tables import SFClassifierItemList

import logging
LOG = logging.getLogger(__name__)

class SFClassifierTab(tabs.TableTab):
    name = _("SFClassifier Tab")
    slug = "sfclassifier_tab"
    table_classes = (tables.SFClassifierTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def build_dict_sfcs(self, list_sfcs):
        dict_sfcs = {}
        for sfc in list_sfcs:
            dict_sfcs[sfc['id']] = sfc['name']
        return dict_sfcs

    def get_SFClassifier_data(self):
        try:

            self._has_more = True
            SFClassifierItemList.clear_list()
            sfcclassifiers = api.tacker.sfclassifier_list(self.request)['sfc_classifiers']
            print "SFClassifier Listing: " + str(sfcclassifiers)
            list_sfcs = tacker_api.sfc_list(self.request)
            dict_sfcs = self.build_dict_sfcs(list_sfcs)
            for sfcclassifier in sfcclassifiers:
                LOG.info(">>>>>>>>>>>>>>sfclassifier includes: %s" % sfcclassifier)
                chain_id = sfcclassifier['chain']
                chain_name = dict_sfcs[chain_id]
                obj = SFClassifierItem(status=sfcclassifier['status'],
                                       name=sfcclassifier['name'],
                                       description=sfcclassifier['description'],
                                       chain=chain_name,
                                       tenant_id=sfcclassifier['tenant_id'],
                                       instance_id=sfcclassifier['instance_id'],
                                       infra_driver=sfcclassifier['infra_driver'],
                                       attributes=sfcclassifier['attributes'],
                                       #symmetrical=sfcclassifier['symmetrical'],
                                       id=sfcclassifier['id'],
                                       acl_match_criteria=sfcclassifier['acl_match_criteria'])
                LOG.info(">>>>>>>>>>>object value for SFClassifierItem :   %s" % obj)
                SFClassifierItemList.add_item(obj)
            return SFClassifierItemList.SFClassifierItemLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class SFClassifierTabs(tabs.TabGroup):
    slug = "sfc_classifier_manager_tabs"
    tabs = (SFClassifierTab,)
    sticky = True
