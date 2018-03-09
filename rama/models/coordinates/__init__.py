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
from rama.astropy import SkyCoordDecorator, TimeDecorator
from rama.framework import Attribute, Reference, Composition
from rama.models.ivoa import StringQuantity
from rama.registry import VO
from rama.utils import Decorator


@VO('coords:domain.space.Epoch')
class Epoch(StringQuantity):
    pass


@VO('coords:Handedness')
class Handedness(StringQuantity):
    pass


@VO('coords:Coordinate')
class Coordinate:
    frame = Reference('coords:Coordinate.frame', min_occurs=0, max_occurs=1)


@VO('coords:CoordValue')
class CoordValue(Coordinate):
    axis = Reference('coords:CoordValue.axis', min_occurs=1, max_occurs=1)


@VO('coords:CompositeCoordinate')
class CompositeCoordinate(Coordinate):
    cmpt = Attribute('coords:CompositeCoordinate.cmpt', min_occurs=1, max_occurs=-1)


@VO('coords:PhysicalCoordValue')
class PhysicalCoordValue(CoordValue):
    cval = Attribute('coords:PhysicalCoordValue.cval', min_occurs=1, max_occurs=1)


@VO('coords:BinnedCoordValue')
class BinnedCoordValue(CoordValue):
    cval = Attribute('coords:BinnedCoordValue.cval', min_occurs=1, max_occurs=1)


@VO('coords:GenericCoordValue')
class GenericCoordValue(PhysicalCoordValue):
    pass


@VO('coords:CoordFrame')
class CoordFrame:
    pass


@VO('coords:CoordSys')
class CoordSys:
    pass


@VO('coords:AstroCoordSystem')
class AstroCoordSystem(CoordSys):
    coord_frame = Reference('coords:AstroCoordSystem.coordFrame', min_occurs=0, max_occurs=-1)


@VO('coords:CoordSpace')
class CoordSpace:
    axis = Composition('coords:CoordSpace.axis', min_occurs=1, max_occurs=-1)


@VO('coords:Axis')
class Axis:
    name = Attribute('coords:Axis.name', min_occurs=0, max_occurs=1)


@VO('coords:ContinuousAxis')
class ContinuousAxis(Axis):
    domain_min_occurs = Attribute('coords:ContinuousAxis.domainMin', min_occurs=0, max_occurs=1)
    domain_max_occurs = Attribute('coords:ContinuousAxis.domainMax', min_occurs=0, max_occurs=1)
    cyclic = Attribute('coords:ContinuousAxis.cyclic', min_occurs=0, max_occurs=1)


@VO('coords:BinnedAxis')
class BinnedAxis(Axis):
    length = Attribute('coords:BinnedAxis.length', min_occurs=1, max_occurs=1)


@VO('coords:DiscreteSetAxis')
class DiscreteSetAxis(Axis):
    pass


@VO('coords:GenericCoordFrame')
class GenericCoordFrame(CoordFrame):
    ref_position = Attribute('coords:GenericCoordFrame.refPosition', min_occurs=1, max_occurs=1)
    planetary_ephem = Attribute('coords:GenericCoordFrame.planetaryEphem', min_occurs=0, max_occurs=1)


@VO('coords:domain.pixel.PixelIndex')
class PixelIndex(BinnedCoordValue):
    pass


@VO('coords:domain.pixel.PixelCoordSystem')
class PixelCoordSystem(CoordSys):
    pixel_space = Composition('coords:domain.pixel.PixelCoordSystem.pixelSpace', min_occurs=1, max_occurs=1)


@VO('coords:domain.pixel.PixelSpace')
class PixelSpace(CoordSpace):
    handedness = Attribute('coords:domain.pixel.PixelSpace.handedness', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.StdRefPosition')
class StdRefPosition(StringQuantity):
    pass


@VO('coords:domain.space.StdRefFrame')
class StdRefFrame(StringQuantity):
    pass


@VO('coords:domain.space.SpatialCoordValue')
class SpatialCoordValue(PhysicalCoordValue):
    pass


@VO('coords:domain.space.RefLocation')
class RefLocation:
    pass


@VO('coords:domain.space.StdRefLocation')
class StdRefLocation(RefLocation):
    position = Attribute('coords:domain.space.StdRefLocation.position', min_occurs=1, max_occurs=1)


@VO('coords:domain.space.CustomRefLocation')
class CustomRefLocation(RefLocation):
    epoch = Attribute('coords:domain.space.CustomRefLocation.epoch', min_occurs=0, max_occurs=1)
    position = Attribute('coords:domain.space.CustomRefLocation.position', min_occurs=1, max_occurs=1)
    velocity = Attribute('coords:domain.space.CustomRefLocation.velocity', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.SpatialCoord')
class SpatialCoord(CompositeCoordinate):
    pass


@VO('coords:domain.space.SpatialCoord1D')
class SpatialCoord1D(SpatialCoord):
    pass


@VO('coords:domain.space.SpatialCoord2D')
class SpatialCoord2D(SpatialCoord):
    pass


@VO('coords:domain.space.SpatialCoord3D')
class SpatialCoord3D(SpatialCoord):
    pass


@VO('coords:domain.space.SkyCoord')
@Decorator(SkyCoordDecorator)
class SkyCoord(Coordinate):
    pass


@VO('coords:domain.space.EquatorialCoord')
class EquatorialCoord(SkyCoord):
    ra = Attribute('coords:domain.space.EquatorialCoord.ra', min_occurs=0, max_occurs=1)
    dec = Attribute('coords:domain.space.EquatorialCoord.dec', min_occurs=0, max_occurs=1)
    r = Attribute('coords:domain.space.EquatorialCoord.r', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.GalacticCoord')
class GalacticCoord(SkyCoord):
    l = Attribute('coords:domain.space.GalacticCoord.l', min_occurs=0, max_occurs=1)
    b = Attribute('coords:domain.space.GalacticCoord.b', min_occurs=0, max_occurs=1)
    r = Attribute('coords:domain.space.GalacticCoord.r', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.EclipticCoord')
class EclipticCoord(SkyCoord):
    elong = Attribute('coords:domain.space.EclipticCoord.elong', min_occurs=0, max_occurs=1)
    elat = Attribute('coords:domain.space.EclipticCoord.elat', min_occurs=0, max_occurs=1)
    r = Attribute('coords:domain.space.EclipticCoord.r', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.CartesianCoord')
class CartesianCoord(SkyCoord):
    x = Attribute('coords:domain.space.CartesianCoord.x', min_occurs=0, max_occurs=1)
    y = Attribute('coords:domain.space.CartesianCoord.y', min_occurs=0, max_occurs=1)
    z = Attribute('coords:domain.space.CartesianCoord.z', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.LongLatCoord')
class LongLatCoord(SkyCoord):
    long = Attribute('coords:domain.space.LongLatCoord.long', min_occurs=0, max_occurs=1)
    lat = Attribute('coords:domain.space.LongLatCoord.lat', min_occurs=0, max_occurs=1)
    r = Attribute('coords:domain.space.LongLatCoord.r', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.UnitSphereCoord')
class UnitSphereCoord(SkyCoord):
    dircosx = Attribute('coords:domain.space.UnitSphereCoord.dircosx', min_occurs=0, max_occurs=1)
    dircosy = Attribute('coords:domain.space.UnitSphereCoord.dircosy', min_occurs=0, max_occurs=1)
    dircosz = Attribute('coords:domain.space.UnitSphereCoord.dircosz', min_occurs=0, max_occurs=1)


@VO('coords:domain.space.SpaceFrame')
class SpaceFrame(CoordFrame):
    ref_position = Attribute('coords:domain.space.SpaceFrame.refPosition', min_occurs=1, max_occurs=1)
    space_ref_frame = Attribute('coords:domain.space.SpaceFrame.spaceRefFrame', min_occurs=1, max_occurs=1)
    equinox = Attribute('coords:domain.space.SpaceFrame.equinox', min_occurs=0, max_occurs=1)
    planetary_ephem = Attribute('coords:domain.space.SpaceFrame.planetaryEphem', min_occurs=1, max_occurs=1)


@VO('coords:domain.spectral.SpectralValue')
class SpectralValue(PhysicalCoordValue):
    pass


@VO('coords:domain.spectral.Wavelength')
class Wavelength(SpectralValue):
    pass


@VO('coords:domain.spectral.Frequency')
class Frequency(SpectralValue):
    pass


@VO('coords:domain.spectral.Energy')
class Energy(SpectralValue):
    pass


@VO('coords:domain.time.TimeScale')
class TimeScale(StringQuantity):
    pass


@VO('coords:domain.time.TimeOffset')
class TimeOffset(PhysicalCoordValue):
    pass


@VO('coords:domain.time.TimeStamp')
@Decorator(TimeDecorator)
class TimeStamp(Coordinate):
    pass


@VO('coords:domain.time.ISOTime')
class ISOTime(TimeStamp):
    date = Attribute('coords:domain.time.ISOTime.date', min_occurs=1, max_occurs=1)


@VO('coords:domain.time.JD')
class JD(TimeStamp):
    date = Attribute('coords:domain.time.JD.date', min_occurs=1, max_occurs=1)


@VO('coords:domain.time.MJD')
class MJD(TimeStamp):
    date = Attribute('coords:domain.time.MJD.date', min_occurs=1, max_occurs=1)


@VO('coords:domain.time.MET')
class MET(TimeStamp):
    time = Attribute('coords:domain.time.MET.time', min_occurs=1, max_occurs=1)
    time0 = Attribute('coords:domain.time.MET.time0', min_occurs=1, max_occurs=1)


@VO('coords:domain.time.TimeFrame')
class TimeFrame(CoordFrame):
    ref_position = Attribute('coords:domain.time.TimeFrame.refPosition', min_occurs=1, max_occurs=1)
    timescale = Attribute('coords:domain.time.TimeFrame.timescale', min_occurs=1, max_occurs=1)
    ref_direction = Attribute('coords:domain.time.TimeFrame.refDirection', min_occurs=0, max_occurs=1)
    time0 = Attribute('coords:domain.time.TimeFrame.time0', min_occurs=0, max_occurs=1)


@VO('coords:domain.redshift.DopplerDefinition')
class DopplerDefinition(StringQuantity):
    pass


@VO('coords:domain.redshift.RedshiftValue')
class RedshiftValue(PhysicalCoordValue):
    pass


@VO('coords:domain.redshift.Redshift')
class Redshift(RedshiftValue):
    pass


@VO('coords:domain.redshift.DopplerVelocity')
class DopplerVelocity(RedshiftValue):
    doppler_definition = Attribute('coords:domain.redshift.DopplerVelocity.dopplerDefinition', min_occurs=1, max_occurs=1)


@VO('coords:domain.polarization.PolStokesEnum')
class PolStokesEnum(StringQuantity):
    pass


@VO('coords:domain.polarization.PolCircularEnum')
class PolCircularEnum(StringQuantity):
    pass


@VO('coords:domain.polarization.PolLinearEnum')
class PolLinearEnum(StringQuantity):
    pass


@VO('coords:domain.polarization.PolVectorEnum')
class PolVectorEnum(StringQuantity):
    pass


@VO('coords:domain.polarization.PolCoordValue')
class PolCoordValue(CoordValue):
    pass


@VO('coords:domain.polarization.PolLinear')
class PolLinear(PolCoordValue):
    cval = Attribute('coords:domain.polarization.PolLinear.cval', min_occurs=1, max_occurs=1)


@VO('coords:domain.polarization.PolVector')
class PolVector(PolCoordValue):
    cval = Attribute('coords:domain.polarization.PolVector.cval', min_occurs=1, max_occurs=1)


@VO('coords:domain.polarization.PolStokes')
class PolStokes(PolCoordValue):
    cval = Attribute('coords:domain.polarization.PolStokes.cval', min_occurs=1, max_occurs=1)


@VO('coords:domain.polarization.PolCircular')
class PolCircular(PolCoordValue):
    cval = Attribute('coords:domain.polarization.PolCircular.cval', min_occurs=1, max_occurs=1)
