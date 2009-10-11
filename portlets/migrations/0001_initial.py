
from south.db import db
from django.db import models
from portlets.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Slot'
        db.create_table('portlets_slot', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
        ))
        db.send_create_signal('portlets', ['Slot'])
        
        # Adding model 'PortletAssignment'
        db.create_table('portlets_portletassignment', (
            ('id', models.AutoField(primary_key=True)),
            ('slot', models.ForeignKey(orm.Slot)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name="pa_content")),
            ('content_id', models.PositiveIntegerField()),
            ('portlet_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name="pa_portlets")),
            ('portlet_id', models.PositiveIntegerField()),
            ('position', models.PositiveSmallIntegerField(default=999)),
        ))
        db.send_create_signal('portlets', ['PortletAssignment'])
        
        # Adding model 'PortletRegistration'
        db.create_table('portlets_portletregistration', (
            ('id', models.AutoField(primary_key=True)),
            ('type', models.CharField(unique=True, max_length=30)),
            ('name', models.CharField(unique=True, max_length=50)),
        ))
        db.send_create_signal('portlets', ['PortletRegistration'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Slot'
        db.delete_table('portlets_slot')
        
        # Deleting model 'PortletAssignment'
        db.delete_table('portlets_portletassignment')
        
        # Deleting model 'PortletRegistration'
        db.delete_table('portlets_portletregistration')
        
    
    
    models = {
        'portlets.slot': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'portlets.portletassignment': {
            'Meta': {'ordering': '["position"]'},
            'content_id': ('models.PositiveIntegerField', [], {}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': '"pa_content"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'portlet_id': ('models.PositiveIntegerField', [], {}),
            'portlet_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': '"pa_portlets"'}),
            'position': ('models.PositiveSmallIntegerField', [], {'default': '999'}),
            'slot': ('models.ForeignKey', ["orm['portlets.Slot']"], {})
        },
        'portlets.portletregistration': {
            'Meta': {'ordering': '("name",)'},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'type': ('models.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }
    
    complete_apps = ['portlets']
