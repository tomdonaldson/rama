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
from rama.framework import Attribute, AttributeList, Reference, Composition
from rama.registry import VO


@VO("meas:CoordMeasure")
class CoordMeasure:
    coord_frame = Reference("meas:CoordMeasure.coordFrame")
    coord = Attribute("meas:CoordMeasure.coord")
    error = Composition("meas:CoordMeasure.error")


@VO("meas:GenericCoordMeasure")
class GenericCoordMeasure(CoordMeasure):
    pass


@VO("meas:TimeMeasure")
class TimeMeasure(CoordMeasure):
    pass


@VO("meas:StdTimeMeasure")
class StdTimeMeasure(TimeMeasure):
    pass


@VO("meas:SkyPosition")
class SkyPosition(CoordMeasure):
    pass


@VO("meas:Error")
class Error:
    pass


@VO("meas:Error1D")
class Error1D(Error):
    pass


@VO("meas:BasicError1D")
class BasicError1D(Error1D):
    stat_error = Attribute("meas:BasicError1D.statError")
    sys_error = Attribute("meas:BasicError1D.sysError")
    ran_error = Attribute("meas:BasicError1D.ranError")


@VO("meas:Error2D")
class Error2D(Error):
    pass


@VO("meas:BasicError2D")
class BasicError2D(Error2D):
    stat_error = Attribute("meas:BasicError2D.statError")
    sys_error = Attribute("meas:BasicError2D.sysError")
    ran_error = Attribute("meas:BasicError2D.ranError")


@VO("meas:Uncertainty")
class Uncertainty:
    pass


@VO("meas:Uncertainty1D")
class Uncertainty1D(Uncertainty):
    pass


@VO("meas:Symmetrical1D")
class Symmetrical1D(Uncertainty1D):
    radius = Attribute("meas:Symmetrical1D.radius")


@VO("meas:Uncertainty2D")
class Uncertainty2D(Uncertainty):
    pass


@VO("meas:Ellipse")
class Ellipse(Uncertainty2D):
    semi_axis = AttributeList("meas:Ellipse.semiAxis")
    pos_angle = Attribute("meas:Ellipse.posAngle")


@VO("meas:Symmetrical2D")
class Symmetrical2D(Uncertainty2D):
    radius = Attribute("meas:Symmetrical2D.radius")
