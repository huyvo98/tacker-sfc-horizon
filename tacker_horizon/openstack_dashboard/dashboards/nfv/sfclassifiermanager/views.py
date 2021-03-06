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


from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import forms


from tacker_horizon.openstack_dashboard.dashboards.nfv.sfclassifiermanager \
    import forms as project_forms

from tacker_horizon.openstack_dashboard.dashboards.nfv.sfclassifiermanager \
    import tabs as sfclassifier_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = sfclassifier_tabs.SFClassifierTabs
    template_name = 'nfv/sfclassifiermanager/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class AddClassifierServiceView(forms.ModalFormView):
    form_class = project_forms.AddSFClassifierForm
    template_name = 'nfv/sfclassifiermanager/addclassifier.html'
    success_url = reverse_lazy("horizon:nfv:sfclassifiermanager:index")
    modal_id = "add_service_modal"
    modal_header = _("Create ServiceFunctionClassifier")
    submit_label = _("Create SFClassifier")
    submit_url = "horizon:nfv:sfclassifiermanager:addclassifier"

    def get_initial(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(AddClassifierServiceView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context
