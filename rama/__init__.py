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
import logging

from pkg_resources import iter_entry_points

from rama.framework import VodmlDescriptor, Composition
from rama.reader import Reader
from rama.reader.votable import Votable

LOG = logging.getLogger(__name__)

for entry_point in iter_entry_points(group='vo.dm.models', name=None):
    try:
        __import__(entry_point.module_name, globals(), locals())
        LOG.info(f"Successfully imported vodml model package {entry_point.name}")
    except ImportError:
        LOG.warning(f"Cannot import vodml model package {entry_point.name}")


def read(filename, fmt='votable'):
    formats = {
        'votable': Votable,
    }

    if fmt not in formats:
        raise AttributeError(f"No such format: {fmt}. Available formats: {fmt.keys()}")

    return Reader(formats[fmt](filename))


def is_template(instance):
    if hasattr(instance, "__vo_object__"):
        return is_template(instance.__vo_object__)

    if hasattr(instance, "is_template"):
        return instance.is_template

    return False
