
from south.db import db
from django.db import models
from portlets.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PortletBlocking'
        db.create_table('portlets_portletblocking', (
            ('id', models.AutoField(primary_key=True)),        
            ('slot', models.ForeignKey(orm.Slot)),
            ('content_id', models.PositiveIntegerField()),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name="pb_content")),
        ))
        db.send_create_signal('portlets', ['PortletBlocking'])
        
        # Creating unique_together for [slot, content_id, content_type] on PortletBlocking.
        db.create_unique('portlets_portletblocking', ['slot_id', 'content_id', 'content_type_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PortletBlocking'
        db.delete_table('portlets_portletblocking')
        
        # Deleting unique_together for [slot, content_id, content_type] on PortletBlocking.
        db.delete_unique('portlets_portletblocking', ['slot_id', 'content_id', 'content_type_id'])
        
    
    
    models = {
        'portlets.portletblocking': {
            'Meta': {'unique_together': '["slot","content_id","content_type"]'},
            'content_id': ('models.PositiveIntegerField', [], {}),
            'content_type': ('models.ForeignKey', ['ContentType'], {'related_name': '"pb_content"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slot': ('models.ForeignKey', ['"Slot"'], {})
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
            'content_type': ('models.ForeignKey', ['ContentType'], {'related_name': '"pa_content"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'portlet_id': ('models.PositiveIntegerField', [], {}),
            'portlet_type': ('models.ForeignKey', ['ContentType'], {'related_name': '"pa_portlets"'}),
            'position': ('models.PositiveSmallIntegerField', [], {'default': '999'}),
            'slot': ('models.ForeignKey', ['"Slot"'], {})
        },
        'portlets.portletregistration': {
            'Meta': {'ordering': '("name",)'},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'type': ('models.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }
    
    complete_apps = ['portlets']
