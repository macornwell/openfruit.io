

class CultivarSpeciesMixin:
    def validate_species_cultivar(self):
        if not self.cultivar and not self.species:
            raise Exception('Need cultivar or a species.')
        if self.cultivar:
            if not self.species:
                self.species = self.cultivar.species
            else:
                if self.cultivar.species != self.species:
                    raise Exception("Cultivar's species is not the same as the instance's species.")

