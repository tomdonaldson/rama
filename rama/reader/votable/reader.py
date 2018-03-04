# Copyright 2018 Smithsonian Astrophysical Observatory
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import inspect
import logging
from weakref import WeakValueDictionary

from rama.framework import VodmlDescriptor, Attribute, Reference, Composition
from rama.reader.votable import parser
from rama.registry import TypeRegistry


LOG = logging.getLogger(__name__)


class AbstractFieldReader:
    """
    Concrete parser must extend this class and provide a method read(self, context, xml_element)
    """
    field_type = None

    def __init__(self, descriptor):
        self.descriptor = descriptor

    def read(self, context, xml_element):
        raise NotImplementedError()

    @property
    def vodml_id(self):
        return self.descriptor.vodml_id

    #TODO this could be done more cleanly with a decorator
    @staticmethod
    def get_field_reader(field):
        for subclass in AbstractFieldReader.__subclasses__():
            if subclass.field_type == type(field):
                return subclass(field)

        raise AttributeError(f"Cannot find a suitable reader for field: {field}")


class AttributeFieldReader(AbstractFieldReader):
    """
    Parser for attribute lists, i.e. attributes of any multiplicity greater than 1.
    """
    field_type = Attribute

    def read(self, context, xml_element):
        attribute_elements = parser.parse_attributes(xml_element, self.vodml_id, context)

        attributes = []
        for attribute_element in attribute_elements:
            attributes.extend(attribute_element.structured_instances)
            attributes.extend(attribute_element.constants)
            attributes.extend(attribute_element.columns)

        return self._select_return_value(attributes)

    def _select_return_value(self, attributes):
        max_occurs = self.descriptor.max
        if max_occurs == 1 and len(attributes) == 1:
            return attributes[0]

        if max_occurs == 1 and len(attributes) == 0:
            return None

        return attributes


class CompositionFieldReader(AbstractFieldReader):
    """
    Parser for composition relationships.
    """
    field_type = Composition

    def read(self, context, xml_element):
        return parser.parse_composed_instances(xml_element, self.vodml_id, context)


class ReferenceReader(AbstractFieldReader):
    """
    Parser for references.
    """
    field_type = Reference

    def read(self, context, xml_element):
        return parser.parse_references(xml_element, self.vodml_id, context)


class InstanceFactory:
    """
    A factory that makes instances of a class based on an `INSTANCE` xml Element.
    """

    @staticmethod
    def make(instance_class, xml_element, context):
        """
        instance_class is the class to be instantiated
        xml_element is the xml Element serializing the instance
        parser is the VodmlReader instance passed through to provide context.
        """
        instance_id = parser.resolve_id(xml_element)

        instance = context.get_instance_by_id(instance_id)
        if instance is not None:
            return instance

        return InstanceFactory._new_instance(context, instance_id, xml_element, instance_class)

    @staticmethod
    def _new_instance(context, instance_id, xml_element, instance_class):
        instance = instance_class()
        instance.__id__ = instance_id
        context.add_instance(instance)

        def is_field(x):
            return inspect.isdatadescriptor(x) and isinstance(x, VodmlDescriptor)

        fields = inspect.getmembers(instance_class, is_field)
        for field_name, field_object in fields:
            setattr(instance, field_name, context.read(field_object, xml_element))

        return instance

# TODO docstrings
class Context:
    def __init__(self, reader, xml=None):
        self.__standalone_instances = WeakValueDictionary()
        self.__tables = {}
        self.__xml = xml
        self.__reader = reader

    def read(self, field, xml_element):
        return self.__reader.read(field, xml_element, self)

    def read_instance(self, xml_element):
        return self.__reader.read_instance(xml_element, self)

    def get_type_by_id(self, type_id):
        return self.__reader.get_by_id(type_id)

    def find_instances(self, cls):
        if self.__xml is None:
            raise AttributeError("When using the context to find instances you must provide an xml object"
                                 " to the initializer")

        return self.__reader.find_instances(self.__xml, cls, context=self)

    def add_instance(self, instance):
        if instance.__id__ is not None:
            self.__standalone_instances[instance.__id__] = instance

    def get_instance_by_id(self, instance_id):
        return self.__standalone_instances.get(instance_id, None)

    def add_table(self, table_id, table):
        self.__tables[table_id] = table

    def get_table_by_id(self, table_id):
        return self.__tables.get(table_id, None)

    @property
    def document(self):
        return self.__xml


class VodmlReader:
    """
    Root Parser.
    """

    def __init__(self):
        self.registry = TypeRegistry.instance
        self.factory = InstanceFactory

    def find_instances(self, xml_document, element_class, context=None):
        """
        Find all instances of the `element_class` class in a votable.
        """
        if context is None:
            context = Context(reader=self)
        return [self.read_instance(element, context) for element in parser.find(xml_document, element_class)]

    def read_instance(self, xml_element, context):
        """
        Parse an `INSTANCE` represented by the `xml_element`
        """
        type_id = parser.resolve_type(xml_element)
        element_class = self.registry.get_by_id(type_id)
        return self.factory.make(element_class, xml_element, context)

    def get_by_id(self, vodml_id):
        "Resolve a vodml_id to the corresponding class"
        return self.registry.get_by_id(vodml_id)

    def read(self, field, xml_element, context):
        field_parser = AbstractFieldReader.get_field_reader(field)
        return field_parser.read(context, xml_element)
