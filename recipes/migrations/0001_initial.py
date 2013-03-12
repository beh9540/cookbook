# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recipe'
        db.create_table('recipes_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('recipes', ['Recipe'])

        # Adding model 'Ingredient'
        db.create_table('recipes_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Recipe'])),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Unit'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('recipes', ['Ingredient'])

        # Adding model 'Unit'
        db.create_table('recipes_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('recipes', ['Unit'])

        # Adding model 'Favorite'
        db.create_table('recipes_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Recipe'])),
        ))
        db.send_create_signal('recipes', ['Favorite'])

        # Adding model 'RecipeStep'
        db.create_table('recipes_recipestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipes.Recipe'])),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('step', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('recipes', ['RecipeStep'])


    def backwards(self, orm):
        # Deleting model 'Recipe'
        db.delete_table('recipes_recipe')

        # Deleting model 'Ingredient'
        db.delete_table('recipes_ingredient')

        # Deleting model 'Unit'
        db.delete_table('recipes_unit')

        # Deleting model 'Favorite'
        db.delete_table('recipes_favorite')

        # Deleting model 'RecipeStep'
        db.delete_table('recipes_recipestep')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'recipes.favorite': {
            'Meta': {'object_name': 'Favorite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'recipes.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Unit']", 'null': 'True', 'blank': 'True'})
        },
        'recipes.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'recipes.recipestep': {
            'Meta': {'object_name': 'RecipeStep'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recipes.Recipe']"}),
            'step': ('django.db.models.fields.TextField', [], {})
        },
        'recipes.unit': {
            'Meta': {'object_name': 'Unit'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['recipes']