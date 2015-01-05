# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Software'
        db.create_table(u'college_software', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'college', ['Software'])

        # Adding model 'Course'
        db.create_table(u'college_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(max_length=200, null=True, blank=True)),
            ('duration_unit', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'college', ['Course'])

        # Adding M2M table for field software on 'Course'
        db.create_table(u'college_course_software', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'college.course'], null=False)),
            ('software', models.ForeignKey(orm[u'college.software'], null=False))
        ))
        db.create_unique(u'college_course_software', ['course_id', 'software_id'])

        # Adding model 'Batch'
        db.create_table(u'college_batch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Software'])),
            ('start_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('no_of_students', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('allowed_students', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'college', ['Batch'])

    def backwards(self, orm):
        # Deleting model 'Software'
        db.delete_table(u'college_software')

        # Deleting model 'Course'
        db.delete_table(u'college_course')

        # Removing M2M table for field software on 'Course'
        db.delete_table('college_course_software')

        # Deleting model 'Batch'
        db.delete_table(u'college_batch')

    models = {
        u'college.batch': {
            'Meta': {'object_name': 'Batch'},
            'allowed_students': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'no_of_students': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'software': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Software']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'college.course': {
            'Meta': {'object_name': 'Course'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'duration_unit': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'software': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['college.Software']", 'symmetrical': 'False'})
        },
        u'college.software': {
            'Meta': {'object_name': 'Software'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['college']