'''
Created on Feb 20, 2012

@author: nils
'''

from django.db import models
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.forms import ModelForm
from galaxy_connector.models import Instance
from guardian.shortcuts import assign, get_users_with_perms, get_groups_with_perms


class UserProfile ( models.Model ):
    '''
    Extends Django user model: https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
    '''
    uuid = UUIDField( unique=True, auto=True )

    user = models.OneToOneField( User )
    affiliation = models.CharField( max_length=100, blank=True )

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name + " (" + self.affiliation + "): " + self.user.email


# automatic creation of a user profile when a user is created: 
def create_user_profile( sender, instance, created, **kwargs ):
    if created:
        UserProfile.objects.create( user=instance )

post_save.connect( create_user_profile, sender=User )            



class BaseResource ( models.Model ):
    '''
    Abstract base class for core resources such as projects, analyses, data sets and so on.
    
    See https://docs.djangoproject.com/en/1.3/topics/db/models/#abstract-base-classes for details.
    '''
    uuid = UUIDField( unique=True, auto=True )
    name = models.CharField( max_length=250 )
    summary = models.CharField( max_length=1000, blank=True )
    creation_date = models.DateTimeField( auto_now_add=True )
    modification_date = models.DateTimeField( auto_now=True )    

    def __unicode__(self):
        return self.name + " (" + self.uuid + ")"
        
    class Meta:
        abstract = True


class OwnableResource ( BaseResource ):
    '''
    Abstract base class for core resources that can be owned (projects, data sets, workflows, workflow engines, etc.).
    
    IMPORTANT: expects derived classes to have "add/read/change/write_xxx" permissions, where "xxx" is the simple_modelname
    '''
    def __unicode__( self ):
        return self.name
    
    def set_owner( self, user ):
        assign( "add_%s" % self._meta.verbose_name, user, self )
        assign( "read_%s" % self._meta.verbose_name, user, self )
        assign( "delete_%s" % self._meta.verbose_name, user, self )
        assign( "change_%s" % self._meta.verbose_name, user, self )

    def get_owner( self ):
        # ownership is determined by "add" permission
        user_permissions = get_users_with_perms( self, attach_perms=True, with_group_users=False )
        
        for user, permission in user_permissions.iteritems():
            if "add_%s" % self._meta.verbose_name in permission:
                return user
    
    class Meta:
        verbose_name = "ownableresource"
        abstract = True
        

class SharableResource ( OwnableResource ):
    '''
    Abstract base class for core resources that can be shared (projects, data sets, workflows, workflow engines, etc.).
    
    IMPORTANT: expects derived classes to have "add/read/change/write_xxx" + "share_xxx" permissions, where "xxx" is the simple_modelname    
    '''
    def __unicode__(self):
        return self.name
    
    def set_owner( self, user ):
        super( SharableResource, self ).set_owner( user )
        assign( "share_%s" % self._meta.verbose_name, user, self )
        
    def share( self, group, readonly=True ):
        assign( "read_%s" % self._meta.verbose_name, group, self )
        
        if not readonly:
            assign( "change_%s" % self._meta.verbose_name, group, self )
        
        
    class Meta:
        verbose_name = "sharableresource"
        abstract = True


class ManageableResource:
    '''
    Abstract base class for manageable resources such as disk space and workflow engines.    
    '''

    def __unicode__(self):
        return self.name + " (" + self.uuid + ")"

    def set_manager_group( self, group ):
        assign( "add_%s" % self._meta.verbose_name, group, self )
        assign( "read_%s" % self._meta.verbose_name, group, self )
        assign( "delete_%s" % self._meta.verbose_name, group, self )
        assign( "change_%s" % self._meta.verbose_name, group, self )

    def get_manager_group( self ):
        # ownership is determined by "add" permission
        group_permissions = get_groups_with_perms( self, attach_perms=True )
        
        for group, permission in group_permissions.iteritems():
            if "add_%s" % self._meta.verbose_name in permission:
                return group
    
    class Meta:
        verbose_name = "manageableresource"
        abstract = True

        
class DataSet ( SharableResource ):

    def __unicode__(self):
        return self.name + " - " + self.summary

    class Meta:
        verbose_name = "dataset"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' % verbose_name ),
            ('share_%s' % verbose_name, 'Can share %s' % verbose_name ),
        )


class WorkflowDataInput ( models.Model ):
    name = models.CharField( max_length=200 )
    internal_id = models.IntegerField()

    def __unicode__(self):
        return self.name + " (" + str( self.internal_id ) + ")"


class WorkflowEngine ( OwnableResource, ManageableResource ):
    # TODO: remove Galaxy dependency
    instance = models.ForeignKey( Instance, blank=True )
    
    def __unicode__(self):
        return self.name + " - " + self.summary

    class Meta:
        verbose_name = "workflowengine"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' % verbose_name ),
        )

                 
class DiskQuota ( SharableResource, ManageableResource ):
    # quota is given in bytes
    maximum = models.IntegerField()
    current = models.IntegerField()
    
    def __unicode__(self):
        return self.name + " - Quota: " + str(self.current/(1024*1024*1024)) + " of " + str(self.maximum/(1024*1024*1024)) + "GB available"

    class Meta:
        verbose_name = "diskquota"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' % verbose_name ),
            ('share_%s' % verbose_name, 'Can share %s' % verbose_name ),
        )

        
class Workflow ( SharableResource, ManageableResource ):

    data_inputs = models.ManyToManyField( WorkflowDataInput, blank=True )
    internal_id = models.CharField( max_length=50, unique=True, blank=True )
    
    # TODO: require this information
    workflow_engine = models.ForeignKey( WorkflowEngine, blank=True, null=True )    

    def __unicode__(self):
        return self.name + " - " + self.summary

    class Meta:
        verbose_name = "workflow"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' % verbose_name ),
            ('share_%s' % verbose_name, 'Can share %s' % verbose_name ),
        )

    
class Project( SharableResource ):
    description = models.CharField( max_length=5000, blank=True )    

    def __unicode__(self):
        return self.name + " - " + self.summary
    
    class Meta:
        verbose_name = "project"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' % verbose_name ),
            ('share_%s' % verbose_name, 'Can share %s' % verbose_name ),
        )


class WorkflowDataInputMap( models.Model ):
    #workflow_data_input_internal_id = models.IntegerField()
    workflow_data_input_name = models.CharField( max_length=200 )    
    data_uuid = UUIDField( auto=False )
    
    pair_id = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return str( self.workflow_data_input_name ) + " <-> " + self.data_uuid
    
                
class Analysis ( OwnableResource ):
    project = models.ForeignKey( Project, related_name="analyses" )
    data_set = models.ForeignKey( DataSet, blank=True )
    workflow = models.ForeignKey( Workflow, blank=True )
    workflow_data_input_maps = models.ManyToManyField( WorkflowDataInputMap, blank=True )
    workflow_steps_num = models.IntegerField(blank=True, null=True)
    workflow_copy = models.TextField(blank=True, null=True)
    history_id = models.TextField(blank=True, null=True)
    workflow_galaxy_id = models.TextField(blank=True, null=True)
    library_id = models.TextField(blank=True, null=True)    
    
    def __unicode__(self):
        return self.name + " - " + self.summary
    
    class Meta:
        verbose_name = "analysis"
        permissions = (
            ('read_%s' % verbose_name, 'Can read %s' %  verbose_name ),
        )


class ExtendedGroup ( Group ):
    ''' Extends the default Django Group in auth with a group of users that own and manage manageable resources for the group.'''    
    manager_group = models.ForeignKey( "self", blank=True, null=True )
    
    def delete(self):
                
        super( ExtendedGroup, self).delete()
    
    def is_managed(self):
        return ( self.manager_group is not None ); 
