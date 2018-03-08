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
from astropy import units as u


@VO("ivoa:RealQuantity")
class RealQuantity:

    def __init__(self, value, unit):
        value = float(value)
        try:
            quantity = value * u.Unit(unit)
        except (ValueError, TypeError):
            quantity = value * u.dimensionless_unscaled
        super().__setattr__('quantity', quantity)

    def __getattr__(self, attr):
        return getattr(self.quantity, attr)

    def __setattr__(self, attr, value):
        setattr(self.quantity, attr, value)

    def __str__(self):
        return self.quantity.__str__()

    def __repr__(self):
        return self.quantity.__repr__()

    def __eq__(self, other):
        return self.quantity.__eq__(other)


@VO("ivoa:string")
class StringQuantity:

    def __new__(self, value, unit):
        return str(value)


@VO("ivoa:boolean")
class VOBool:
    def __new__(cls, value, *args, **kwargs):
        return value.lower() == 'true'
