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
from rama.framework import Attribute
from rama.registry import VO


@VO('filter:PhotometricSystem')
class PhotometricSystem:
    description = Attribute('filter:PhotometricSystem.description', min=0, max=1)
    detector_type = Attribute('filter:PhotometricSystem.detectorType', min=1, max=1)


@VO('filter:PhotometryFilter')
class PhotometryFilter:
    fps_identifier = Attribute('filter:PhotometryFilter.fpsIdentifier', min=1, max=1)
    identifier = Attribute('filter:PhotometryFilter.identifier', min=1, max=1)
    name = Attribute('filter:PhotometryFilter.name', min=1, max=1)
    description = Attribute('filter:PhotometryFilter.description', min=1, max=1)
    band_name = Attribute('filter:PhotometryFilter.bandName', min=1, max=1)
    data_validity_from = Attribute('filter:PhotometryFilter.dataValidityFrom', min=1, max=1)
    data_validity_to = Attribute('filter:PhotometryFilter.dataValidityTo', min=1, max=1)
    spectral_location = Attribute('filter:PhotometryFilter.spectralLocation', min=1, max=1)
