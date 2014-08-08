from django.db import models

# for parsing natural key
class CountryManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)

class GeonamesCountry(models.Model):
    '''Minimal country information, based on geonames country info download
http://download.geonames.org/export/dump/countryInfo.txt'''
    #: country name

    objects = CountryManager()

    name = models.CharField(max_length=255)
    #: two-letter ISO country code
    code = models.CharField(max_length=2, unique=True)
    #: ISO-numeric code
    numeric_code = models.IntegerField()
    #: two-letter continent code
    continent = models.CharField(max_length=2)
    #: numeric geonames id
    geonames_id = models.IntegerField()

    class Meta:
        verbose_name_plural = 'geonames countries'

    # generate natural key
    def natural_key(self):
        return (self.code,)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)

class ContinentManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)

class GeonamesContinent(models.Model):
    '''Continent names and codes from GeoNames, as listed at
http://download.geonames.org/export/dump/'''
    #: continent name

    objects = ContinentManager()

    name = models.CharField(max_length=255)
    #: two-letter continent code
    code = models.CharField(max_length=2, unique=True)
    #: geonames id
    geonames_id = models.IntegerField()

    # generate natural key
    def natural_key(self):
        return (self.code,)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class StateManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)

class StateCode(models.Model):
    'U.S. State abbreviation and FIPS codes, for generating maps'
    #: state name

    objects = StateManager()

    name = models.CharField(max_length=255)
    #: two-letter state abbrevation
    code = models.CharField(max_length=2, unique=True)
    #: numeric FIPS code
    fips = models.IntegerField()

    class Meta:
        verbose_name_plural = 'geonames statecode'

    # generate natural key
    def natural_key(self):
        return (self.code,)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class LocationManager(models.Manager):
    def get_by_natural_key(self, street_address, city, zipcode):
        return self.get(street_address=street_address, city=city, zipcode=zipcode)


class Location(models.Model):
    """
    Locations or Addresses
    """

    objects = LocationManager()

    street_address = models.CharField(max_length=255, blank=True, help_text='Street name and number')
    '''Street name and number'''
    city = models.CharField(max_length=255, help_text='City name')
    '''City name'''
    state = models.ForeignKey(StateCode, blank=True, null=True, help_text='State name')
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(GeonamesCountry, help_text='Country name')
    ''' Country name'''

    # generate natural key
    def natural_key(self):
        return (self.street_address, self.city, self.zipcode)

    def __unicode__(self):
        return '%s %s %s %s %s' \
               % (self.street_address, self.city, self.state, self.zipcode, self.country)

    class Meta:
        unique_together = ('street_address', 'city', 'state', 'zipcode', 'country')
        ordering = ['street_address', 'city', 'state', 'zipcode', 'country']
