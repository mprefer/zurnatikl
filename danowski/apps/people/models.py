from django.db import models
from danowski.apps.geo.models import Location


#Schools
class SchoolManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class School(models.Model):
    '''School of poetry'''

    objects = SchoolManager()

    CATEGORIZER_CHOICES =(
        ('Donald Allen', 'Donald Allen'),
    )

    name = models.CharField(max_length=255)
    ''' Name of school of poetry'''
    categorizer = models.CharField(max_length=100, blank=True, choices=CATEGORIZER_CHOICES)
    '''Name of categorizer'''
    location = models.ForeignKey(Location, blank=True, null=True)
    ''':class:`Location` of school of poetry'''
    notes = models.TextField(blank=True)

    def natural_key(self):
        return (self.name,)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'categorizer', 'location')
        ordering = ['name']

    @property
    def network_id(self):
        #: node identifier when generating a network
        return 'school:%s' % self.id

    @property
    def network_attributes(self):
        #: data to be included as node attributes when generating a network
        return {
            'label': unicode(self),
            'name': self.name,
            'categorizer': self.categorizer,
        }



# Person and person parts
class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Person(models.Model):
    'A person associated with a school of poetry, journal issue, item, etc.'

    objects = PersonManager()

    #: choices for :attr:`gender`
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male')
    )
    #: choices for :attr:`race`
    RACE_CHOICES = (
        ('American Indian or Alaska Native', 'American Indian or Alaska Native'),
        ('Asian', 'Asian'),
        ('Black or African American', 'Black or African American'),
        ('Hispanic', 'Hispanic'),
        ('Latino', 'Latino'),
        ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'),
        ('White', 'White'),
    )

    #: first name
    first_name = models.CharField(max_length=100, blank=True)
    #: last name
    last_name = models.CharField(max_length=100)
    #: race
    race = models.CharField(max_length=50, blank=True, choices=RACE_CHOICES)
    #: raceself-description
    racial_self_description = models.CharField(max_length=100, blank=True)
    #: gender
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    #: schools associated with; many to many relation to :model:`School`
    schools = models.ManyToManyField('School', blank=True)
    #: uri
    uri = models.URLField(blank=True)
    #: dwelling locations
    dwelling = models.ManyToManyField(Location, blank=True, related_name = 'dwelling_info')
    #: notes
    notes = models.TextField(blank=True)

    def natural_key(self):
        return (self.first_name, self.last_name)

    def __unicode__(self):
        if not self.first_name:
            return self.last_name
        else:
            return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        verbose_name_plural = 'People'
        unique_together = ('first_name', 'last_name')
        ordering = ['last_name', 'first_name']

    @property
    def network_id(self):
        #: node identifier when generating a network
        return 'person:%s' % self.id

    @property
    def network_attributes(self):
        #: data to be included as node attributes when generating a network
        return {
            'label': unicode(self),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'race': self.race,
            'gender': self.gender,
            'uri': self.uri
        }



class NameManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name, person):
        self.get(first_name=first_name, last_name=last_name)


class Name(models.Model):

    objects = NameManager()

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    person = models.ForeignKey('Person')

    def natural_key(self):
        return (self.first_name, self.last_name)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PenNameManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class PenName(models.Model):

    objects = PenNameManager()

    name = models.CharField(max_length=200)
    person = models.ForeignKey('Person')

    def natural_key(self):
        return (self.name)

    def __unicode__(self):
        return self.name
