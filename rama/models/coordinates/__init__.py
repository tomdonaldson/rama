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
from rama.framework import Attribute, Reference
from rama.models.ivoa import StringQuantity
from rama.registry import VO


@VO("coords:domain.spatial.RefLocation")
class RefLocation:
  pass


@VO("coords:domain.spatial.StdRefLocation")
class StdRefLocation:
    position = Attribute("coords:domain.spatial.StdRefLocation.position")


@VO("coords:domain.spatial.SkyCoord")
class SkyCoord:
     pass


@VO("coords:domain.spatial.CelestialCoord")
class CelestialCoord(SkyCoord):
    ra = Attribute("coords:domain.spatial.CelestialCoord.ra")
    dec = Attribute("coords:domain.spatial.CelestialCoord.dec")


@VO("coords:CoordFrame")
class CoordFrame:
     pass


@VO("coords:domain.temporal.TimeFrame")
class TimeFrame(CoordFrame):
    ref_position = Attribute("coords:domain.temporal.TimeFrame.refPosition")
    timescale = Attribute("coords:domain.temporal.TimeFrame.timescale")


@VO("coords:domain.spatial.SpaceFrame")
class SpaceFrame(CoordFrame):
    ref_position = Attribute("coords:domain.spatial.SpaceFrame.refPosition")
    space_ref_frame = Attribute("coords:domain.spatial.SpaceFrame.spaceRefFrame")
    equinox = Attribute("coords:domain.spatial.SpaceFrame.equinox")


@VO("coords:domain.temporal.TimeStamp")
class TimeStamp:
     pass


@VO("coords:domain.temporal.ISOTime")
class ISOTime:
    date = Attribute("coords:domain.temporal.ISOTime.date")


@VO("coords:domain.temporal.JD")
class JD:
    date = Attribute("coords:domain.temporal.JD.date")


@VO("coords:domain.temporal.TimeScale")
class TimeScale(StringQuantity):
    """
    For simplicity, assume this is just a string, which is fine for this notebook.
    """
    pass


@VO("coords:Coordinate")
class Coordinate:
    pass


@VO("coords:CoordValue")
class CoordValue(Coordinate):
    axis = Reference("coords:CoordValue.axis")


@VO("coords:PhysicalCoordValue")
class PhysicalCoordValue(CoordValue):
    cval = Attribute("coords:PhysicalCoordValue.cval")


@VO("coords:GenericCoordValue")
class GenericCoordValue(PhysicalCoordValue):
    pass


@VO("coords:domain.spatial.Epoch")
class Epoch(StringQuantity):
    """
    For simplicity, assume this is just a string, which is fine for this notebook.
    """
    pass


@VO("coords:domain.spatial.StdRefPosition")
class StdRefPosition(StringQuantity):
    """
    For simplicity, assume this is just a string, which is fine for this notebook.
    """
    pass


@VO("coords:domain.spatial.StdRefFrame")
class StdRefFrame(StringQuantity):
    """
    For simplicity, assume this is just a string, which is fine for this notebook.
    """
    pass
