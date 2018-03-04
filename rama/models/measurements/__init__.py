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
from rama.registry import VO



@VO('meas:Uncertainty')
class Uncertainty:
    pass


@VO('meas:Uncertainty1D')
class Uncertainty1D(Uncertainty):
    pass


@VO('meas:Uncertainty2D')
class Uncertainty2D(Uncertainty):
    pass


@VO('meas:Uncertainty3D')
class Uncertainty3D(Uncertainty):
    pass


@VO('meas:Symmetrical1D')
class Symmetrical1D(Uncertainty1D):
    radius = Attribute('meas:Symmetrical1D.radius', min=1, max=1)


@VO('meas:Asymmetrical1D')
class Asymmetrical1D(Uncertainty1D):
    plus = Attribute('meas:Asymmetrical1D.plus', min=1, max=1)
    minus = Attribute('meas:Asymmetrical1D.minus', min=1, max=1)


@VO('meas:Bounds1D')
class Bounds1D(Uncertainty1D):
    lo_limit = Attribute('meas:Bounds1D.loLimit', min=1, max=1)
    hi_limit = Attribute('meas:Bounds1D.hiLimit', min=1, max=1)


@VO('meas:Symmetrical2D')
class Symmetrical2D(Uncertainty2D):
    radius = Attribute('meas:Symmetrical2D.radius', min=1, max=1)


@VO('meas:Asymmetrical2D')
class Asymmetrical2D(Uncertainty2D):
    plus = Attribute('meas:Asymmetrical2D.plus', min=2, max=2)
    minus = Attribute('meas:Asymmetrical2D.minus', min=2, max=2)


@VO('meas:Bounds2D')
class Bounds2D(Uncertainty2D):
    lo_limit = Attribute('meas:Bounds2D.loLimit', min=2, max=2)
    hi_limit = Attribute('meas:Bounds2D.hiLimit', min=2, max=2)


@VO('meas:Symmetrical3D')
class Symmetrical3D(Uncertainty3D):
    radius = Attribute('meas:Symmetrical3D.radius', min=1, max=1)


@VO('meas:Asymmetrical3D')
class Asymmetrical3D(Uncertainty3D):
    plus = Attribute('meas:Asymmetrical3D.plus', min=3, max=3)
    minus = Attribute('meas:Asymmetrical3D.minus', min=3, max=3)


@VO('meas:Bounds3D')
class Bounds3D(Uncertainty3D):
    lo_limit = Attribute('meas:Bounds3D.loLimit', min=3, max=3)
    hi_limit = Attribute('meas:Bounds3D.hiLimit', min=3, max=3)


@VO('meas:Ellipse')
class Ellipse(Uncertainty2D):
    semi_axis = Attribute('meas:Ellipse.semiAxis', min=2, max=2)
    pos_angle = Attribute('meas:Ellipse.posAngle', min=1, max=1)


@VO('meas:Ellipsoid')
class Ellipsoid(Uncertainty3D):
    semi_axis = Attribute('meas:Ellipsoid.semiAxis', min=3, max=3)
    pos_angle = Attribute('meas:Ellipsoid.posAngle', min=2, max=2)


@VO('meas:Matrix')
class Matrix:
    pass


@VO('meas:Matrix2x2')
class Matrix2x2(Matrix):
    m11 = Attribute('meas:Matrix2x2.m11', min=1, max=1)
    m12 = Attribute('meas:Matrix2x2.m12', min=1, max=1)
    m21 = Attribute('meas:Matrix2x2.m21', min=1, max=1)
    m22 = Attribute('meas:Matrix2x2.m22', min=1, max=1)


@VO('meas:Matrix3x3')
class Matrix3x3(Matrix):
    m11 = Attribute('meas:Matrix3x3.m11', min=1, max=1)
    m12 = Attribute('meas:Matrix3x3.m12', min=1, max=1)
    m13 = Attribute('meas:Matrix3x3.m13', min=1, max=1)
    m21 = Attribute('meas:Matrix3x3.m21', min=1, max=1)
    m22 = Attribute('meas:Matrix3x3.m22', min=1, max=1)
    m23 = Attribute('meas:Matrix3x3.m23', min=1, max=1)
    m31 = Attribute('meas:Matrix3x3.m31', min=1, max=1)
    m32 = Attribute('meas:Matrix3x3.m32', min=1, max=1)
    m33 = Attribute('meas:Matrix3x3.m33', min=1, max=1)


@VO('meas:CovarianceMatrix2D')
class CovarianceMatrix2D(Uncertainty2D):
    matrix = Attribute('meas:CovarianceMatrix2D.matrix', min=1, max=1)


@VO('meas:CovarianceMatrix3D')
class CovarianceMatrix3D(Uncertainty3D):
    matrix = Attribute('meas:CovarianceMatrix3D.matrix', min=1, max=1)


@VO('meas:CoordMeasure')
class CoordMeasure:
    coord = Attribute('meas:CoordMeasure.coord', min=1, max=1)
    error = Composition('meas:CoordMeasure.error', min=0, max=1)
    coord_frame = Reference('meas:CoordMeasure.coordFrame', min=0, max=1)


@VO('meas:Error')
class Error:
    pass


@VO('meas:Error1D')
class Error1D(Error):
    pass


@VO('meas:Error2D')
class Error2D(Error):
    pass


@VO('meas:Error3D')
class Error3D(Error):
    pass


@VO('meas:BasicError1D')
class BasicError1D(Error1D):
    stat_error = Attribute('meas:BasicError1D.statError', min=0, max=1)
    sys_error = Attribute('meas:BasicError1D.sysError', min=0, max=1)
    ran_error = Attribute('meas:BasicError1D.ranError', min=0, max=1)


@VO('meas:BasicError2D')
class BasicError2D(Error2D):
    stat_error = Attribute('meas:BasicError2D.statError', min=0, max=1)
    sys_error = Attribute('meas:BasicError2D.sysError', min=0, max=1)
    ran_error = Attribute('meas:BasicError2D.ranError', min=0, max=1)


@VO('meas:BasicError3D')
class BasicError3D(Error3D):
    stat_error = Attribute('meas:BasicError3D.statError', min=0, max=1)
    sys_error = Attribute('meas:BasicError3D.sysError', min=0, max=1)
    ran_error = Attribute('meas:BasicError3D.ranError', min=0, max=1)


@VO('meas:GenericCoordMeasure')
class GenericCoordMeasure(CoordMeasure):
    pass


@VO('meas:Position')
class Position(CoordMeasure):
    pass


@VO('meas:Position1D')
class Position1D(Position):
    pass


@VO('meas:Position2D')
class Position2D(Position):
    pass


@VO('meas:Position3D')
class Position3D(Position):
    pass


@VO('meas:SpectralCoordMeasure')
class SpectralCoordMeasure(CoordMeasure):
    pass


@VO('meas:TimeMeasure')
class TimeMeasure(CoordMeasure):
    pass


@VO('meas:Polarization')
class Polarization:
    coord = Attribute('meas:Polarization.coord', min=1, max=1)


@VO('meas:RedshiftCoordMeasure')
class RedshiftCoordMeasure(CoordMeasure):
    pass


@VO('meas:GenPosition2D')
class GenPosition2D(Position2D):
    pass


@VO('meas:SkyPosition')
class SkyPosition(Position2D):
    pass


@VO('meas:GenTimeMeasure')
class GenTimeMeasure(TimeMeasure):
    pass


@VO('meas:StdTimeMeasure')
class StdTimeMeasure(TimeMeasure):
    pass

