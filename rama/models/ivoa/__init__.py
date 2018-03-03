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
from rama.registry import VO


@VO("ivoa:RealQuantity")
class RealQuantity:
    """
    Represents ivoa:RealQuantity
    """

    def __init__(self, value, unit):
        self.value = float(value)
        self.unit = unit


@VO("ivoa:real")
class Real(RealQuantity):
    """
    Represents ivoa:real, just makes it the same as RealQuantity
    """
    pass


@VO("ivoa:string")
class StringQuantity:
    """
    Represents all ivoa:* quantities that can be represented with a string in Python.
    In this simple implementation that does not provide validation, enumerations are
    also treated as simple strings.
    """
    vodml_id = "ivoa:string"

    def __init__(self, value, unit):
        self.value = str(value)
        self.unit = unit


@VO("ivoa:boolean")
class BooleanQuantity:
    """
    Represents ivoa:boolean
    """

    def __init__(self, value, unit):
        self.value = value.lower() == 'true'
        self.unit = unit


@VO("ivoa:anyURI")
class Uri(StringQuantity):
    pass