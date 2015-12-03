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
from horizon import forms

import logging
from tacker_horizon.openstack_dashboard.api import tacker as tacker_api
from horizon import messages
from horizon import exceptions

LOG = logging.getLogger(__name__)

class AddSFCForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=50, label= "SFC Name")
    description = forms.CharField(required=False, max_length=200)
    chain = forms.CharField(max_length=500, label=_("Chain VNFs"))
    symmetrical = forms.BooleanField(required=True)
    #infra_driver = forms.CharField(required=False, max_length=200)
    #instance_id = forms.CharField(required=False, max_length=200)

    def __init__(self, request, *args, **kwargs):
        super(AddSFCForm, self).__init__(request, *args, **kwargs)
        has_more_data = True

        available_vnfs = tacker_api.vnf_list(request)
        vnfs = []
        for vnf in available_vnfs:
            vnfs.append((vnf['id'],vnf['name']))
        LOG.info(">>>>>>>>>>>>>>>>available_vnfs = %s" % available_vnfs)
        self.fields['chain'].choices = [('', _('Select SFC applies for chain'))
                                           ]+vnfs
        LOG.debug("done initial adding sfc form")

    def handle(self, request, data):
        LOG.info(">>>>>>>>>>>>>>>>in handle, data = %s" % data)
        try:
            name = data['name']
            description = data['description']
            symmetrical = data['symmetrical']
            #instance_id = data["instance_id"]
            #infra_driver = data["infra_driver"]

            chain_vnfs = data['chain'].split(",")
            chain = ["testVNF1","testVNF2"]
            sfc_arg = {"sfc" :{"name":name, "chain":chain_vnfs,"description":description,"symmetrical":symmetrical}}
            LOG.info("Creating Service Function Classifier with sfc_classifier_arg = %s" % sfc_arg)
            tacker_api.create_sfc(request, sfc_arg)
            messages.success(request,
                             _('ServiceFunctionChain %s has been created.'))
            return True
        except Exception:
            exceptions.handle(request,
                              _('Unable to create Service Function Chain with data = %s' % data))