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
import numpy
import pytest
from astropy import units as u

from rama.models.coordinates import SpaceFrame
from rama.models.measurements import SkyPosition
from rama.reader.votable import Context, VodmlReader


@pytest.fixture
def simple_position_file(make_data_path):
    return make_data_path('simple-position.vot.xml')


@pytest.fixture
def simple_position_columns_file(make_data_path):
    return make_data_path('simple-position-columns.vot.xml')


@pytest.fixture
def invalid_file(make_data_path):
    return make_data_path('invalid.vot.xml')


@pytest.fixture
def references_file(make_data_path):
    return make_data_path('references.vot.xml')


def test_parsing_coordinates(reader, simple_position_file):
    sky_positions = reader.find_instances(simple_position_file, SkyPosition)
    pos = sky_positions[0]

    assert 1 == len(sky_positions)
    assert 10.34209135 * u.deg == pos.coord.ra
    assert 41.13232112 * u.deg == pos.coord.dec
    assert "FK5" == pos.coord.frame.space_ref_frame
    assert "J1975" == pos.coord.frame.equinox
    assert "TOPOCENTER" == pos.coord.frame.ref_position.position


def test_references_are_same_object(reader, references_file):
    sky_positions = reader.find_instances(references_file, SkyPosition)

    assert sky_positions[0].coord.frame is sky_positions[1].coord.frame


def test_referred_built_only_once(reader, references_file):
    context = Context(reader, xml=references_file)
    frame = context.find_instances(SpaceFrame)[0]
    frame2 = context.find_instances(SpaceFrame)[0]
    sky_positions = context.find_instances(SkyPosition)

    assert frame is frame2
    assert sky_positions[0].coord.frame is frame
    assert sky_positions[1].coord.frame is frame


def test_context_without_filaname(reader):
    context = Context(reader)
    with pytest.raises(AttributeError):
        context.find_instances(SpaceFrame)


def test_parsing_columns(reader, simple_position_columns_file, recwarn):
    context = Context(reader, xml=simple_position_columns_file)
    sky_positions = context.find_instances(SkyPosition)
    position = sky_positions[0]

    assert 1 == len(sky_positions)
    expected_ra = numpy.array([10.0, 20.0], dtype='float32') * u.deg
    expected_dec = numpy.array([11.0, 21.0], dtype='float32') * u.deg
    numpy.testing.assert_array_equal(expected_ra, position.coord.ra)
    numpy.testing.assert_array_equal(expected_dec, position.coord.dec)

    assert "W20" in str(recwarn[0].message)
    assert "W41" in str(recwarn[1].message)
    for i in range(2, 12):
        assert "W10" in str(recwarn[i].message)


def test_attribute_multiplicity(reader, make_data_path, recwarn):
    context = Context(reader, xml=make_data_path("asymmetric-2d-position.vot.xml"))
    position = context.find_instances(SkyPosition)[0]

    plus = position.error[0].stat_error.plus
    assert len(plus) == 2

    minus = position.error[0].stat_error.minus
    assert len(minus) == 2

    assert "Dangling reference" in str(recwarn[0].message)


def test_invalid_file(reader, invalid_file):
    context = Context(reader, xml=invalid_file)

    with pytest.warns(SyntaxWarning) as record:
        sky_positions = context.find_instances(SkyPosition)
        assert "ID foo" in str(record[-1].message)
        assert "W50" in str(record[12].message)

    position = sky_positions[0]

    assert 1 == len(sky_positions)
    expected_ra = numpy.array([numpy.NaN, numpy.NaN])
    expected_dec = numpy.array([11.0, 21.0]) * u.dimensionless_unscaled
    numpy.testing.assert_array_equal(expected_ra, position.coord.ra)
    numpy.testing.assert_array_equal(expected_dec, position.coord.dec)
