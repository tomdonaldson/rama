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
import logging
import warnings

from astropy.io import votable
from lxml import etree

import numpy

LOG = logging.getLogger(__name__)


def parse_attributes(xml_element, role_id, context):
    attributes_xml = xml_element.xpath(_get_role_xpath_expression('ATTRIBUTE', role_id))
    return [AttributeElement(xml, role_id, context) for xml in attributes_xml]


def parse_composed_instances(xml_element, role_id, context):
        elements = xml_element.xpath(f"./{_get_local_name('COMPOSITION')}[@dmrole='{role_id}']/child::"
                                     f"{_get_local_name('INSTANCE')}")
        return [context.read_instance(element) for element in elements]


def parse_references(xml_element, role_id, context):
    reference_elements = xml_element.xpath(f"./{_get_local_name('REFERENCE')}[@dmrole='{role_id}']")

    references = []

    for reference_element in reference_elements:
        id_ref = reference_element.xpath(f"./{_get_local_name('IDREF')}")[0].text

        referred_instance = context.get_instance_by_id(id_ref)
        if referred_instance is not None:
            return referred_instance

        referred_element = reference_element.xpath(f"//{_get_local_name('INSTANCE')}[@ID='{id_ref}']")[0]
        references.append(context.read_instance(referred_element))

    # FIXME We really need to properly treat multiplicities!
    if len(references) == 1:
        return references[0]

    return references


def find(xml_document, element_class):
    root = _find_root(xml_document)
    type_id = element_class.vodml_id
    elements = root.xpath(_get_type_xpath_expression('INSTANCE', type_id))
    return elements


def resolve_type(xml_element):
    element_type = xml_element.xpath("@dmtype")[0]
    return element_type


def resolve_id(xml_element):
    ids = xml_element.xpath('@ID')
    if len(ids):
        return ids[0]
    return None


class AttributeElement:
    def __init__(self, xml_element, role_id, context):
        self.xml = xml_element
        self.role_id = role_id
        self.context = context

    @property
    def structured_instances(self):
        elements = _get_children(self.xml, "INSTANCE")
        return [self.context.read_instance(element) for element in elements]

    @property
    def constants(self):
        elements = _get_children(self.xml, "LITERAL")
        return [self._parse_literal(element) for element in elements]

    @property
    def columns(self):
        elements = _get_children(self.xml, "COLUMN")
        return [self._parse_column(element) for element in elements]

    def _parse_literal(self, xml_element):
        value = xml_element.xpath("@value")[0]
        value_type = xml_element.xpath("@dmtype")[0]
        units = xml_element.xpath("@unit")
        unit = units[0] if len(units) else None
        return self.context.get_type_by_id(value_type)(value, unit)

    def _parse_column(self, xml_element):
        column_ref = xml_element.xpath("@ref")[0]
        find_column_xpath = f"//{_get_local_name('FIELD')}[@ID='{column_ref}']"
        column_elements = xml_element.xpath(find_column_xpath)
        if not len(column_elements):
            msg = f"Can't find column with ID {column_ref}. Setting values to NaN"
            LOG.warning(msg)
            warnings.warn(msg, SyntaxWarning)
            return numpy.NaN

        column_element = column_elements[0]
        table = self._parse_table(column_element)

        column = table[column_ref]

        name = column_element.xpath("@name")[0]
        column.name = name

        return column

    def _parse_table(self, column_element):

        table_elements = column_element.xpath(f"parent::{_get_local_name('TABLE')}")
        if not len(table_elements):
            raise RuntimeError("COLUMN points to FIELD that does not have a TABLE parent")
        table_element = table_elements[0]

        table_id_index = False
        table_ids = table_element.xpath('@ID')
        if len(table_ids):
            table_id = table_ids[0]
            table = self.context.get_table_by_id(table_id)
            if table is not None:
                return table
        else:
            table_id_index = True
            table_id = int(table_element.xpath(f"count(preceding-sibling::{_get_local_name('TABLE')})"))

        if table_id_index:
            table = votable.parse_single_table(self.context.document, table_number=table_id).to_table()
            table_id = id(table)
            table_element.attrib["ID"] = str(table_id)
        else:
            table = votable.parse_single_table(self.context.document, table_id=table_id).to_table()

        self.context.add_table(table_id, table)

        return table


def _find_root(xml_document):
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(xml_document, parser)
    return tree.getroot()


def _get_type_xpath_expression(tag_name, type_id):
    tag_selector = _get_local_name(tag_name)
    return f"//{tag_selector}[@dmtype='{type_id}']"


def _get_role_xpath_expression(tag_name, role_id):
    tag_selector = _get_local_name(tag_name)
    return f".//{tag_selector}[@dmrole='{role_id}']"


def _get_local_name(tag_name):
    return f"*[local-name() = '{tag_name}']"


def _get_child_selector(tag_name):
    tag_selector = _get_local_name(tag_name)
    return f"child::{tag_selector}"

def _get_children(element, child_tag_name):
    return element.xpath(_get_child_selector(child_tag_name))

