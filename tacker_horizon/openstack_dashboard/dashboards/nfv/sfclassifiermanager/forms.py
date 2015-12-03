from django.utils.translation import ugettext_lazy as _
from horizon import forms

import logging
from tacker_horizon.openstack_dashboard.api import tacker as tacker_api
from horizon import messages
from horizon import exceptions

LOG = logging.getLogger(__name__)


class AddSFClassifierForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=50, label= "SFClassifier Name")
    description = forms.CharField(max_length=200)
    chain = forms.ChoiceField(label=_("SFC"))
    match = forms.CharField(max_length=500)


    def __init__(self, request, *args, **kwargs):
        super(AddSFClassifierForm, self).__init__(request, *args, **kwargs)
        has_more_data = True

        available_sfcs = tacker_api.sfc_list(request)
        sfcs = []
        for sfc in available_sfcs:
            sfcs.append((sfc['id'],sfc['name']))
        LOG.info(">>>>>>>>>>>>>>>>available_sfcs = %s" % available_sfcs)
        LOG.info(">>>>>>>>>>>>>>options for fields chain:   %s" % dir(self.fields['chain']))
        self.fields['chain'].choices = [('', _('Select SFC applies for chain'))
                                           ]+sfcs
        LOG.debug("done setting sfc")

    def handle(self, request, data):
        try:
            name = data['name']
            description = data['description']

            chain = data['chain']
            #dict(item.split("=") for item in parsed_args.match.split(","))
            match = dict(item.split("=") for item in data['match'].split(","))
            sfc_classifier_arg = {"sfc_classifier" :{"name":name, "chain":chain, "match":match, "description":description}}
            LOG.info("Creating Service Function Classifier with sfc_classifier_arg = %s" % sfc_classifier_arg)
            tacker_api.create_sfc_classifier(request, sfc_classifier_arg)
            messages.success(request,
                             _('SFClassifier %s has been created.'))
            return True
        except Exception:
            exceptions.handle(request,
                              _('Unable to create Service Function Classifier.'))