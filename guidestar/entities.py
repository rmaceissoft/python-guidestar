
class Items(list):
    pass


class Item(object):

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        return pickle

    def __getattr__(self, name):
        #invoken when refering to attribute that it is not valid or it was not present at json response
        return None

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into a model instance."""
        instance = cls()
        for k, v in json.items():
            if hasattr(cls, 'exclude') and k in cls.exclude:
                pass
            elif hasattr(cls, 'parsers') and k in cls.parsers:
                func = cls.parsers[k]
                setattr(instance, k, func(v))
            else:
                setattr(instance, k, v)
        return instance

    @classmethod
    def parse_list(cls, json):
        items = Items()
        if type(json) is list:
            objects = json
        else:
            objects = json.get('hits', [])

        for obj in objects:
            items.append(cls.parse(obj))
        return items


class NteeCode(Item):
    parsers = {
        'ntee_code_details': lambda v: v.get('nteecodedescription')
    }


class GeographicArea(Item):
    exclude = ('organization_id', )


class PersonType(Item):
    exclude = ('last_modified', )


class Person(Item):
    parsers = {
        'person_types': PersonType.parse_list
    }
    exclude = ('organizationid', )


class Program(Item):
    exclude = ('organizationid', )


class Organization(Item):
    parsers = {
        'geographic_areas_served': GeographicArea.parse_list,
        'organization_ntee_codes': NteeCode.parse_list,
        'people': Person.parse_list,
        'programs': Program.parse_list

    }
