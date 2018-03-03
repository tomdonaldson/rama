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
import os
import pytest
from rama.parser.votable import VodmlParser
from rama.models.measurements import SkyPosition

@pytest.fixture
def parser():
    return VodmlParser()

@pytest.fixture
def simple_position_file():
    basedir = os.path.dirname(__file__)
    filename = 'simple-position.vot.xml'
    return os.path.join(basedir, 'data', filename)


def test_parsing_coordinates(parser, simple_position_file):
    sky_positions = parser.find_instances(simple_position_file, SkyPosition)
    pos = sky_positions[0]

    assert 1 == len(sky_positions)
    assert 10.34209135 == pos.coord.ra.value
    assert 41.13232112 == pos.coord.dec.value
    assert "FK5" == pos.coord_frame.space_ref_frame.value
    assert "J1975" == pos.coord_frame.equinox.value
    assert "TOPOCENTER" == pos.coord_frame.ref_position.position.value