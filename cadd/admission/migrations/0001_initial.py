# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Installment'
        db.create_table(u'admission_installment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('fine_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'admission', ['Installment'])

        # Adding model 'FollowUp'
        db.create_table(u'admission_followup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follow_up_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('remarks_for_follow_up_date', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'admission', ['FollowUp'])

        # Adding model 'Enquiry'
        db.create_table(u'admission_enquiry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('student_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('details_about_clients_enquiry', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('educational_qualification', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('land_mark', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('auto_generated_num', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('saved_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_admitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'admission', ['Enquiry'])

        # Adding M2M table for field follow_up on 'Enquiry'
        db.create_table(u'admission_enquiry_follow_up', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enquiry', models.ForeignKey(orm[u'admission.enquiry'], null=False)),
            ('followup', models.ForeignKey(orm[u'admission.followup'], null=False))
        ))
        db.create_unique(u'admission_enquiry_follow_up', ['enquiry_id', 'followup_id'])

        # Adding model 'Student'
        db.create_table(u'admission_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquiry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admission.Enquiry'], null=True, blank=True)),
            ('student_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('roll_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('cadd_registration_no', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('blood_group', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('doj', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('qualifications', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('certificates_submitted', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('id_proofs_submitted', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('is_rolled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fees', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('no_installments', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'admission', ['Student'])

        # Adding M2M table for field batches on 'Student'
        db.create_table(u'admission_student_batches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'admission.student'], null=False)),
            ('batch', models.ForeignKey(orm[u'college.batch'], null=False))
        ))
        db.create_unique(u'admission_student_batches', ['student_id', 'batch_id'])

        # Adding M2M table for field installments on 'Student'
        db.create_table(u'admission_student_installments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'admission.student'], null=False)),
            ('installment', models.ForeignKey(orm[u'admission.installment'], null=False))
        ))
        db.create_unique(u'admission_student_installments', ['student_id', 'installment_id'])

    def backwards(self, orm):
        # Deleting model 'Installment'
        db.delete_table(u'admission_installment')

        # Deleting model 'FollowUp'
        db.delete_table(u'admission_followup')

        # Deleting model 'Enquiry'
        db.delete_table(u'admission_enquiry')

        # Removing M2M table for field follow_up on 'Enquiry'
        db.delete_table('admission_enquiry_follow_up')

        # Deleting model 'Student'
        db.delete_table(u'admission_student')

        # Removing M2M table for field batches on 'Student'
        db.delete_table('admission_student_batches')

        # Removing M2M table for field installments on 'Student'
        db.delete_table('admission_student_installments')

    models = {
        u'admission.enquiry': {
            'Meta': {'object_name': 'Enquiry'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'auto_generated_num': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'details_about_clients_enquiry': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'educational_qualification': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'follow_up': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['admission.FollowUp']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'land_mark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'saved_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'admission.followup': {
            'Meta': {'object_name': 'FollowUp'},
            'follow_up_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks_for_follow_up_date': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'admission.installment': {
            'Meta': {'object_name': 'Installment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fine_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'admission.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'batches': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cadd_registration_no': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doj': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enquiry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['admission.Enquiry']", 'null': 'True', 'blank': 'True'}),
            'fees': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'guardian_mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_proofs_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'installments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['admission.Installment']", 'null': 'True', 'blank': 'True'}),
            'is_rolled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'no_installments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'roll_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['admission']