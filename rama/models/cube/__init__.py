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
from rama.utils import Adapter

from rama.cube import CubePoint
from rama.framework import Composition, Attribute
from rama.registry import VO


@VO('cube:DataProduct')
class DataProduct:
    coord_sys = Composition('cube:DataProduct.coordSys', min_occurs=1, max_occurs=-1)
    mappings = Composition('cube:DataProduct.mappings', min_occurs=0, max_occurs=1)


@VO('cube:PixelatedDataProduct')
class PixelatedDataProduct(DataProduct):
    pixel_coord_sys = Composition('cube:PixelatedDataProduct.pixelCoordSys', min_occurs=1, max_occurs=1)


@VO('cube:PointDataProduct')
class PointDataProduct(DataProduct):
    pass


@VO('cube:NDImage')
class NDImage(PixelatedDataProduct):
    data = Composition('cube:NDImage.data', min_occurs=0, max_occurs=-1)


@VO('cube:SparseCube')
class SparseCube(PointDataProduct):
    data = Composition('cube:SparseCube.data', min_occurs=0, max_occurs=-1)


@VO('cube:DataElement')
class DataElement:
    axis = Composition('cube:DataElement.axis', min_occurs=0, max_occurs=-1)


@VO('cube:Voxel')
class Voxel(DataElement):
    pixel_axis = Composition('cube:Voxel.pixelAxis', min_occurs=1, max_occurs=-1)


@VO('cube:NDPoint')
@Adapter(CubePoint)
class NDPoint(DataElement):
    pass


@VO('cube:DataAxis')
class DataAxis:
    dependent = Attribute('cube:DataAxis.dependent', min_occurs=1, max_occurs=1)
    measurement = Composition('cube:DataAxis.measurement', min_occurs=1, max_occurs=1)


@VO('cube:PixelAxis')
class PixelAxis:
    coord = Attribute('cube:PixelAxis.coord', min_occurs=1, max_occurs=1)
