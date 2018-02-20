from django.db import models


class KingdomManager(models.Manager):

    def get_kingdom_by_name(self, name):
        filtered = super(KingdomManager, self).filter(latin_name__iexact=name).first()
        if not filtered:
            filtered = super(KingdomManager, self).filter(name__iexact=name).first()
        return filtered


class GenusManager(models.Manager):

    def get_genus_by_name(self, name):
        name = name.replace('-', ' ')
        filtered = super(GenusManager, self).filter(latin_name__iexact=name).first()
        if not filtered:
            filtered = super(GenusManager, self).filter(name__iexact=name).first()
        return filtered


class SpeciesManager(models.Manager):

    def get_species_by_name(self, name):
        name = name.replace('-', ' ')
        filtered = super(SpeciesManager, self).filter(latin_name__iexact=name).first()
        if not filtered:
            filtered = super(SpeciesManager, self).filter(name__iexact=name).first()
        return filtered

    def get_species_from_genus(self, genus):
        return super(SpeciesManager, self).filter(genus=genus).order_by('name')


class CultivarManager(models.Manager):

    def get_cultivar_by_name(self, species, name):
        filtered = super(CultivarManager, self).filter(species=species).filter(name__iexact=name).first()
        return filtered

    def get_cultivars_from_species(self, species):
        return super(CultivarManager, self).filter(species=species).order_by('name')


class FruitingPlantManager(models.Manager):

    def get_plants_for_user(self, user):
        return super(FruitingPlantManager, self).filter(user_creator=user)

    def get_plants_that_are_living(self):
        return self.filter(date_died__isnull=True)

