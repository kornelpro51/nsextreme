# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('nsextreme_video','video_video')
        db.rename_table('nsextreme_videocategory','video_videocategory')
        db.rename_table('nsextreme_videocomment','video_videocomment')
        pass

    def backwards(self, orm):
        db.rename_table('video_video','nsextreme_video')
        db.rename_table('video_videocategory','nsextreme_videocategory')
        db.rename_table('video_videocomment', 'nsextreme_videocomment')
        pass

    models = {
        
    }

    complete_apps = ['nsextreme']