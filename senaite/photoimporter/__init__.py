# -*- coding: utf-8 -*-

import logging
import imghdr
import os
from bika.lims.browser import BrowserView
from bika.lims.catalog import CATALOG_ANALYSIS_REQUEST_LISTING
from bika.lims.utils import tmpID
from bika.lims import api
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

logger = logging.getLogger("senaite.photoimpoter")

class ARPhotosImporter(BrowserView):

    def import_ar_photos(self):
        """ You seed at 100, object added will start at 101
        """
        logger.info('Inside import_ar_photos')
        bc= api.get_tool(CATALOG_ANALYSIS_REQUEST_LISTING)
        bsc = api.get_tool("bika_setup_catalog")
        #folder = self.context.bika_setup.getPhotoImporterFolder()
        folder = self.context.bika_setup.PhotoImporterFolder
        errors = []
        archive = []
        if not os.path.isdir(folder):
            logger.info('Photos Folder not found: {}'.format(folder))
            return 'Folder: {} not found'.format(folder)

        errors_dir = '%s/errors' % folder
        archives_dir = '%s/archives' % folder
        if not os.path.exists(errors_dir):
            os.makedirs(errors_dir)
        if not os.path.exists(archives_dir):
            os.makedirs(archives_dir)

        for photo in os.listdir(folder):
            filepath = os.path.join(folder, photo)
            #Is directory
            if os.path.isdir(filepath):
                continue

            #Is not an image
            if imghdr.what(filepath) is None:
                continue

            ar_photo, file_extension = os.path.splitext(photo)
            ar_photo = ar_photo.upper()
            ar = bc(portal_type='AnalysisRequest', id=ar_photo)
            if len(ar) == 0:
                # Move to errors folder 
                destination = '{}/{}'.format(errors_dir, photo)
                os.rename(filepath, destination)
                continue

            if len(ar) == 1:
                ar = ar[0].getObject()
                attachment = _createObjectByType("Attachment", self.context,
                                                 tmpID())
                att_types = bsc(portal_type='AttachmentType',
                                                      inactive_state='active',
                                                      sort_on="sortable_title",
                                                      sort_order="ascending")
                att_type_uid = ''
                for att_type in att_types:
                    obj = att_type.getObject()
                    if obj.title == 'Image':
                        att_type_uid = obj.UID()
                        break

                f = open(filepath)
                attachment.setAttachmentFile(f)
                f.close()
                attachment.setAttachmentType(att_type_uid)
                attachment.setReportOption('r')

                # Attach to AR
                ar.setAttachment(attachment.UID())
                # Move to archives folder 
                destination = '{}/{}'.format(archives_dir, photo)
                os.rename(filepath, destination)
            else:
                logger.error('Found more than one AR: {}'.format(ar))
        logger.info('Done')
        return 'Done'
