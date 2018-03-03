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

from rama.utils import Singleton


@Singleton
class TypeRegistry:
    """
    This class provides a registry to resolve types from their vodml_ids. In this simple
    implementation the types are found among all the classes in the global namespace
    (see `find_globals` method).
    """

    def __init__(self):
        self._type_map = {}

    # TODO docstrings
    def get_by_id(self, vodml_id):
        element_class = self._type_map.get(vodml_id, None)
        if element_class is None:
            raise ValueError(f"Cannot find element with type id: {vodml_id}")
        return element_class

    def add(self, cls):
        if hasattr(cls, 'vodml_id') and inspect.isclass(cls):
            self._type_map[cls.vodml_id] = cls

    def clean(self):
        self._type_map = {}


class VO:
    """
    TODO docstring
    """

    def __init__(self, vodml_id):
        self.vodml_id = vodml_id

    def __call__(self, cls):
        cls.vodml_id = self.vodml_id
        TypeRegistry.instance.add(cls)
        return cls