# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permission'
        db.create_table(u'staff_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attendance_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('student_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('master_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fees_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('register_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expense_module', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'staff', ['Permission'])

        # Adding model 'Staff'
        db.create_table(u'staff_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['staff.Permission'], null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('land_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('blood_group', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('doj', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('qualifications', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'staff', ['Staff'])

    def backwards(self, orm):
        # Deleting model 'Permission'
        db.delete_table(u'staff_permission')

        # Deleting model 'Staff'
        db.delete_table(u'staff_staff')

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'staff.permission': {
            'Meta': {'object_name': 'Permission'},
            'attendance_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expense_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fees_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'register_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student_module': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'staff.staff': {
            'Meta': {'object_name': 'Staff'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doj': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['staff.Permission']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['staff']