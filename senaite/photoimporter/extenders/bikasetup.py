from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.content.bikasetup import BikaSetup
from bika.lims.fields import ExtStringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.public import *
from zope.component import adapts
from zope.interface import implements


class PhotoPathField(ExtStringField):
    """
    """


class BikaSetupSchemaExtender(object):
    adapts(BikaSetup)
    implements(IOrderableSchemaExtender)

    fields = [
        PhotoPathField(
            'PhotoImporterFolder', 
            schemata="Analyses",
            widget=StringWidget(
                label=_("Photo Importer Folder"),
                description=_("The folder on the filesystem where the photos"
                            "will reside")
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
