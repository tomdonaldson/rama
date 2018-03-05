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
import pytest
from numpy.testing import assert_array_equal

from rama.models.test.filter import PhotometryFilter
from rama.models.test.sample import SkyCoordinateFrame, Source
from rama.reader.votable import Context


@pytest.fixture
def context_test5(make_data_path, reader):
    return Context(reader, xml=make_data_path("test5.vot.xml"))


def test_coordinate_frame(context_test5):
    frames = context_test5.find_instances(SkyCoordinateFrame)

    assert len(frames) == 1
    assert frames[0].name.value == "ICRS"


def test_filters(context_test5):
    filters = context_test5.find_instances(PhotometryFilter)

    assert len(filters) == 6
    assert filters[0].name == "2mass:H"
    assert filters[1].name == "2mass:J"
    assert filters[2].name == "2mass:K"
    assert filters[3].name == "sdss:g"
    assert filters[4].name == "sdss:r"
    assert filters[5].name == "sdss:u"


def test_source(context_test5, recwarn):
    sources = context_test5.find_instances(Source)

    assert len(sources) == 1
    source = sources[0]
    assert_array_equal(source.name, [b'08120809-0206132', b'08115683-0205428', b'08115826-0205336'])

    assert "W20" in str(recwarn[0].message)
    assert "W41" in str(recwarn[1].message)
    for i in range(2, 12):
        assert "W10" in str(recwarn[i].message)




