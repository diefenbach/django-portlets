from south.db import db
from django.db import models
from portlets.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'PortletRegistration.active'
        db.add_column('portlets_portletregistration', 'active', models.BooleanField(default=True))
        
    def backwards(self, orm):
        
        # Deleting field 'PortletRegistration.active'
        db.delete_column('portlets_portletregistration', 'active')
        
    models = {
        'portlets.portletblocking': {
            'Meta': {'unique_together': '["slot","content_id","content_type"]'},
            'content_id': ('models.PositiveIntegerField', [], {}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': '"pb_content"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slot': ('models.ForeignKey', ["orm['portlets.Slot']"], {})
        },
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
            'active': ('models.BooleanField', [], {'default': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'type': ('models.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }
    
    complete_apps = ['portlets']
