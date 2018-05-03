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
from rama.models.measurements import GenericCoordMeasure, SkyPosition, StdTimeMeasure


class VoAxis:
    name = None
    model_class = None

    def __init__(self, axis):
        self._axis = axis

    @property
    def dependent(self):
        return self._axis.dependent

    @property
    def measurement(self):
        return self._axis.measurement.coord

    @property
    def stat_error(self):
        return self._axis.measurement.error.stat_error

    @property
    def is_scalar(self):
        return self.measurement.isscalar

    @property
    def unit(self):
        return self.measurement.unit

    @classmethod
    def is_vo_axis_for(cls, axis):
        return isinstance(axis.measurement, cls.model_class)


class TimeAxis(VoAxis):
    model_class = StdTimeMeasure

    def __init__(self, axis):
        super().__init__(axis)
        self.name = axis.measurement.coord.name

    @property
    def measurement(self):
        return self._axis.measurement.coord

class SkyPositionAxis(VoAxis):
    name = 'position'
    model_class = SkyPosition


class GenericCoordMeasureAxis(VoAxis):
    name = 'generic'
    model_class = GenericCoordMeasure

    def __init__(self, axis):
        super().__init__(axis)
        self.name = axis.measurement.coord.cval.name

    @property
    def measurement(self):
        return self._axis.measurement.coord.cval


def vo_axis_factory(axis):
    for cls in VoAxis.__subclasses__():
        if cls.is_vo_axis_for(axis):
            return cls(axis)

    raise ValueError(f"No VoAxis subclasses found for instance axis: {axis.measurement}")


class CubePoint:
    def __init__(self, ndpoint):
        self._ndpoint = ndpoint
        self._index = {}
        self.dependent = []
        self.independent = []

        for axis in ndpoint.axis:
            vo_axis = vo_axis_factory(axis)
            self._index[vo_axis.name] = vo_axis
            if axis.dependent:
                self.dependent.append(vo_axis.name)
            else:
                self.independent.append(vo_axis.name)

    @property
    def axes(self):
        return self._index.values()

    def __getitem__(self, item):
        return self._index[item]
