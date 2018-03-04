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
from weakref import WeakValueDictionary

import astropy.units as u
from lxml import etree
from pandas import read_html

from rama.framework import VodmlDescriptor, AttributeList, Attribute, Reference, Composition
from rama.registry import TypeRegistry


def _get_type_xpath_expression(tag_name, type_id):
    tag_selector = _get_local_name(tag_name)
    return f"//{tag_selector}[@dmtype='{type_id}']"


def _get_role_xpath_expression(tag_name, role_id):
    tag_selector = _get_local_name(tag_name)
    return f"//{tag_selector}[@dmrole='{role_id}']"


def _get_local_name(tag_name):
    return f"*[local-name() = '{tag_name}']"


def _get_child_selector(tag_name):
    tag_selector = _get_local_name(tag_name)
    return f"child::{tag_selector}"

def _get_children(element, child_tag_name):
    return element.xpath(_get_child_selector(child_tag_name))


class AbstractParser:
    """
    Concrete parser must extend this class and provide a method parse(self, vodml_parser, xml_element)
    """

    def __init__(self, descriptor):
        self.vodml_id = descriptor.vodml_id


class AttributeListParser(AbstractParser):
    """
    Parser for attribute lists, i.e. attributes of any multiplicity greater than 1.
    """

    def parse(self, context, xml_element):
        return self._parse_attributes(context, xml_element)

    def _parse_attributes(self, context, xml_element):
        role_id = self.vodml_id
        attribute_elements = xml_element.xpath(_get_role_xpath_expression('ATTRIBUTE', role_id))

        if not len(attribute_elements):
            return (None,)

        attributes = []

        for attribute_element in attribute_elements:
            instance_elements = _get_children(attribute_element, "INSTANCE")
            literal_elements = _get_children(attribute_element, "LITERAL")
            column_elements = _get_children(attribute_element, "COLUMN")

            if len(instance_elements):
                attributes.append(context.parse_instance(instance_elements[0]))

            elif len(literal_elements):
                attributes.append(self._parse_literal(context, literal_elements[0]))

            elif len(column_elements):
                attributes.append(self._parse_column(context, column_elements[0]))

        return tuple(attributes)

    def _parse_literal(self, context, xml_element):
        value = xml_element.xpath("@value")[0]
        value_type = xml_element.xpath("@dmtype")[0]
        units = xml_element.xpath("@unit")
        unit = units[0] if len(units) else None
        return context.get_type_by_id(value_type)(value, unit)

    def _parse_column(self, context, xml_element):
        table = self._parse_table(xml_element)

        column_ref = xml_element.xpath("@ref")[0]
        find_column_xpath = f"//{_get_local_name('FIELD')}[@ID='{column_ref}']"
        find_index_xpath = f"count({find_column_xpath}/preceding-sibling::{_get_local_name('FIELD')})"
        column_element = xml_element.xpath(find_column_xpath)[0]
        column_index = int(xml_element.xpath(find_index_xpath))
        column = table[:, column_index]

        units = column_element.xpath("@unit")
        unit = units[0] if len(units) else None

        quantity = True  # whether this is an astropy quantity.
        if unit is not None:
            # FIXME unit might not be recognized
            column = column * u.Unit(unit, parse_strict='warn')
        else:
            try:  # any (numerical) column astropy can handle
                column = u.Quantity(column)
            except:
                quantity = False

        if quantity:
            name = column_element.xpath("@name")[0]
            column.name = name

        return column

    def _parse_table(self, xml_element):
        table_html = etree.tostring(xml_element.xpath(f"//{_get_local_name('TABLEDATA')}")[0])
        return read_html(f"<table>{table_html}</table>")[0].as_matrix()


class AttributeParser(AttributeListParser):
    """
    Parser for attributes of multiplicity = 1. This parser is basically an AttributeListParser that returns
    a single instance rather than a tuple.
    """

    def parse(self, context, xml_element):
        return self._parse_attribute(context, xml_element)

    def _parse_attribute(self, context, xml_element):
        attributes = self._parse_attributes(context, xml_element)
        if len(attributes):
            return attributes[0]
        return None


class CompositionParser(AbstractParser):
    """
    Parser for composition relationships.
    """

    def parse(self, context, xml_element):
        role_id = self.vodml_id
        elements = xml_element.xpath(f"./{_get_local_name('COMPOSITION')}[@dmrole='{role_id}']/child::"
                                     f"{_get_local_name('INSTANCE')}")
        return [context.parse_instance(element) for element in elements]


class ReferenceParser:
    """
    Parser for references.
    """

    def __init__(self, descriptor):
        self.vodml_id = descriptor.vodml_id

    def parse(self, context, xml_element):
        role_id = self.vodml_id
        reference_elements = xml_element.xpath(f"./{_get_local_name('REFERENCE')}[@dmrole='{role_id}']")
        if not len(reference_elements):
            return None

        reference_element = reference_elements[0]

        id_ref = reference_element.xpath(f"./{_get_local_name('IDREF')}")[0].text

        referred_instance = context.get_instance_by_id(id_ref)
        if referred_instance is not None:
            return referred_instance

        referred_element = reference_element.xpath(f"//{_get_local_name('INSTANCE')}[@ID='{id_ref}']")[0]
        referred_instance = context.parse_instance(referred_element)
        return referred_instance


class InstanceFactory:
    """
    A factory that makes instances of a class based on an `INSTANCE` xml Element.
    """

    @staticmethod
    def make(instance_class, xml_element, context):
        """
        instance_class is the class to be instantiated
        xml_element is the xml Element serializing the instance
        parser is the VodmlParser instance passed through to provide context.
        """
        instance_id = InstanceFactory._find_id(xml_element)

        instance = InstanceFactory._try_context(context, instance_id)
        if instance is not None:
            return instance

        return InstanceFactory._new_instance(context, instance_id, xml_element, instance_class)

    @staticmethod
    def _find_id(xml_element):
        instance_ids = xml_element.xpath('@ID')
        if len(instance_ids):
            return instance_ids[0]
        return None

    @staticmethod
    def _try_context(context, instance_id):
        if instance_id is not None:
            return context.get_instance_by_id(instance_id)

    @staticmethod
    def _new_instance(context, instance_id, xml_element, instance_class):
        instance = instance_class()
        instance.__id__ = instance_id
        context.add_instance(instance)

        def is_field(x):
            return inspect.isdatadescriptor(x) and isinstance(x, VodmlDescriptor)

        fields = inspect.getmembers(instance_class, is_field)
        for field_name, field_object in fields:
            setattr(instance, field_name, context.parse(field_object, xml_element))

        return instance

# TODO docstrings
class Context:
    def __init__(self, parser, xml=None):
        self.__standalone_instances = WeakValueDictionary()
        self.__xml = xml
        self.__parser = parser

    def parse(self, field, xml_element):
        return self.__parser.parse(field, xml_element, self)

    def parse_instance(self, xml_element):
        return self.__parser.parse_instance(xml_element, self)

    def get_type_by_id(self, type_id):
        return self.__parser.get_by_id(type_id)

    def find_instances(self, cls):
        if self.__xml is None:
            raise AttributeError("When using the context to find instances you must provide an xml object"
                                 " to the initializer")

        return self.__parser.find_instances(self.__xml, cls, context=self)

    def add_instance(self, instance):
        if instance.__id__ is not None:
            self.__standalone_instances[instance.__id__] = instance

    def get_instance_by_id(self, instance_id):
        return self.__standalone_instances.get(instance_id, None)


class VodmlParser:
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
        root = self._find_root(xml_document)
        if context is None:
            context = Context(parser=self)

        type_id = element_class.vodml_id
        elements = root.xpath(_get_type_xpath_expression('INSTANCE', type_id))
        return [self.parse_instance(element, context) for element in elements]

    def parse_instance(self, xml_element, context):
        """
        Parse an `INSTANCE` represented by the `xml_element`
        """
        element_class = self._resolve_type(xml_element)
        return self.factory.make(element_class, xml_element, context)

    def get_by_id(self, vodml_id):
        "Resolve a vodml_id to the corresponding class"
        return self.registry.get_by_id(vodml_id)

    def parse(self, field, xml_element, context):
        field_parser = self._get_parser(field)
        return field_parser.parse(context, xml_element)

    @staticmethod
    def _get_parser(field):
        parser_dict = {
            AttributeList: AttributeListParser,
            Attribute: AttributeParser,
            Reference: ReferenceParser,
            Composition: CompositionParser,
        }

        ## TODO Handle key error
        return parser_dict[field.__class__](field)

    @staticmethod
    def _find_root(xml_document):
        parser = etree.XMLParser(ns_clean=True)
        tree = etree.parse(xml_document, parser)
        return tree.getroot()

    def _resolve_type(self, xml_element):
        element_type = xml_element.xpath("@dmtype")[0]
        element_class = self.registry.get_by_id(element_type)
        return element_class