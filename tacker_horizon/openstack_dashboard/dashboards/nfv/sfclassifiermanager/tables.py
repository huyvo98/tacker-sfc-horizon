from horizon import messages
from horizon import tables
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from django.utils.translation import ungettext_lazy
from tacker_horizon.openstack_dashboard import api
from openstack_dashboard import policy
import logging
LOG = logging.getLogger(__name__)

class SFClassifierItem(object):
    def __init__(self , id, name, description, status, chain, tenant_id, instance_id, infra_driver, attributes, acl_match_criteria):
        self.name = name
        self.description = description
        self.id = id
        self.status = status
        self.chain = chain
        self.tenant_id = tenant_id
        self.instance_id = instance_id
        self.infra_driver = infra_driver
        self.attributes = attributes
        self.acl_match_criteria = acl_match_criteria

class SFClassifierItemList():
    SFClassifierItemLIST_P = []

    @classmethod
    def get_obj_given_sfclassifier_id(cls, sfclassifier_id):
        for obj in cls.SFClassifierItemLIST_P:
            if obj.id == sfclassifier_id:
                return obj

    @classmethod
    def add_item(cls, item):
        cls.SFClassifierItemLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.SFClassifierItemLIST_P = []



class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class ActionUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, id):
        try:
            sfclassifier = api.tacker.get_sfclassifier(request, id)

            item = SFClassifierItemList.get_obj_given_sfclassifier_id(sfclassifier['id'])

            return item
        except Http404:
            raise
        except Exception as e:
            messages.error(request, e)
            raise

class DeleteSFCClassifier(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete SFC Classifier",
            u"Delete SFC Classifiers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete SFC Classifier",
            u"Delete SFC Classifiers",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_sfc_classifier(request,obj_id)

class AddServicesLink(tables.LinkAction):
    name = "addClassifier"
    verbose_name = _("create a SFClassifier")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:sfclassifiermanager:addclassifier"

class SFClassifierTable(tables.DataTable):
    id = tables.Column("id",verbose_name=_("ID"))

    name = tables.Column("name", \
                         verbose_name=_("SFClassifier Name"))
    description = tables.Column("description", \
                           verbose_name=_("Description"))
    status = tables.Column('status', verbose_name=_("Status"))
    chain = tables.Column("chain", verbose_name=_("Chain"))
    LOG.info(">>>>>>dstVM = %s " % chain)

    acl_match_criteria = tables.Column("acl_match_criteria", verbose_name="Match")
    tenant_id = tables.Column("tanant_id", verbose_name=_("Tenant ID"))
    instance_id = tables.Column("instance_id", verbose_name=_("Instance ID"))
    infra_driver = tables.Column("infra_driver", verbose_name=_("Infra Driver"))
    attributes = tables.Column("attributes", verbose_name=_("Attributes"))
    #symmetrical = tables.Column("symmetrical", verbose_name=_("Symmetrical"))

    class Meta:
        name = "SFClassifier"
        verbose_name = _("SFClassifier")
        SFC_columns = ["SFC",]
        row_class = ActionUpdateRow
        table_actions = (MyFilterAction,AddServicesLink,DeleteSFCClassifier)

