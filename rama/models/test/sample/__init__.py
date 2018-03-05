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
from rama.framework import Attribute, Reference, Composition
from rama.models.ivoa import StringQuantity

from rama.registry import VO


@VO('sample:catalog.LuminosityType')
class LuminosityType(StringQuantity):
    pass


@VO('sample:catalog.SourceClassification')
class SourceClassification(StringQuantity):
    pass


@VO('sample:catalog.SkyError')
class SkyError:
    pass


@VO('sample:catalog.AlignedEllipse')
class AlignedEllipse(SkyError):
    long_error = Attribute('sample:catalog.AlignedEllipse.longError', min=1, max=1)
    lat_error = Attribute('sample:catalog.AlignedEllipse.latError', min=1, max=1)


@VO('sample:catalog.CircleError')
class CircleError(SkyError):
    radius = Attribute('sample:catalog.CircleError.radius', min=1, max=1)


@VO('sample:catalog.GenericEllipse')
class GenericEllipse(SkyError):
    major = Attribute('sample:catalog.GenericEllipse.major', min=1, max=1)
    minor = Attribute('sample:catalog.GenericEllipse.minor', min=1, max=1)
    pa = Attribute('sample:catalog.GenericEllipse.pa', min=0, max=-1)


@VO('sample:catalog.SkyCoordinate')
class SkyCoordinate:
    longitude = Attribute('sample:catalog.SkyCoordinate.longitude', min=1, max=1)
    latitude = Attribute('sample:catalog.SkyCoordinate.latitude', min=1, max=1)
    frame = Reference('sample:catalog.SkyCoordinate.frame', min=1, max=1)


@VO('sample:catalog.AstroObject')
class AstroObject:
    label = Attribute('sample:catalog.AstroObject.label', min=0, max=1)


@VO('sample:catalog.AbstractSource')
class AbstractSource(AstroObject):
    name = Attribute('sample:catalog.AbstractSource.name', min=1, max=1)
    description = Attribute('sample:catalog.AbstractSource.description', min=0, max=1)
    position = Attribute('sample:catalog.AbstractSource.position', min=1, max=1)
    position_error = Attribute('sample:catalog.AbstractSource.positionError', min=0, max=1)
    classification = Attribute('sample:catalog.AbstractSource.classification', min=1, max=1)
    luminosity = Composition('sample:catalog.AbstractSource.luminosity', min=0, max=-1)


@VO('sample:catalog.LuminosityMeasurement')
class LuminosityMeasurement:
    value = Attribute('sample:catalog.LuminosityMeasurement.value', min=1, max=1)
    error = Attribute('sample:catalog.LuminosityMeasurement.error', min=0, max=1)
    description = Attribute('sample:catalog.LuminosityMeasurement.description', min=0, max=1)
    type = Attribute('sample:catalog.LuminosityMeasurement.type', min=1, max=1)
    filter = Reference('sample:catalog.LuminosityMeasurement.filter', min=1, max=1)


@VO('sample:catalog.SDSSSource')
class SDSSSource(AbstractSource):
    pass


@VO('sample:catalog.SkyCoordinateFrame')
class SkyCoordinateFrame:
    name = Attribute('sample:catalog.SkyCoordinateFrame.name', min=1, max=1)
    document_u_r_i = Attribute('sample:catalog.SkyCoordinateFrame.documentURI', min=1, max=1)
    equinox = Attribute('sample:catalog.SkyCoordinateFrame.equinox', min=0, max=1)
    system = Attribute('sample:catalog.SkyCoordinateFrame.system', min=0, max=1)


@VO('sample:catalog.Source')
class Source(AbstractSource):
    pass


@VO('sample:catalog.TwoMassSource')
class TwoMassSource(AbstractSource):
    pass
