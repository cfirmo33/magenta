# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Classes for converting between chord progressions and models inputs/outputs.

MajorMinorChordOneHotEncoding is an encoding.OneHotEncoding that specifies a
one-hot encoding for ChordProgression events, i.e. chord symbol strings. This
encoding has 25 classes, all 12 major and minor triads plus "no chord".

TriadChordOneHotEncoding is another encoding.OneHotEncoding that specifies a
one-hot encoding for ChordProgression events, i.e. chord symbol strings. This
encoding has 49 classes, all 12 major/minor/augmented/diminished triads plus
"no chord".
"""

# internal imports
from magenta.music import chord_symbols_lib
from magenta.music import constants
from magenta.music import encoder_decoder

NOTES_PER_OCTAVE = constants.NOTES_PER_OCTAVE
NO_CHORD = constants.NO_CHORD

# Mapping from pitch class index to name.
_PITCH_CLASS_MAPPING = ['C', 'C#', 'D', 'Eb', 'E', 'F',
                        'F#', 'G', 'Ab', 'A', 'Bb', 'B']


class ChordEncodingException(Exception):
  pass


class MajorMinorChordOneHotEncoding(encoder_decoder.OneHotEncoding):
  """Encodes chords as root + major/minor, with zero index for "no chord".

  Encodes chords as follows:
    0:     "no chord"
    1-12:  chords with a major triad, where 1 is C major, 2 is C# major, etc.
    13-24: chords with a minor triad, where 13 is C minor, 14 is C# minor, etc.
  """

  def __init__(self, chord_symbol_functions=
               chord_symbols_lib.ChordSymbolFunctions.get()):
    """Initialize the MajorMinorChordOneHotEncoding object.

    Args:
      chord_symbol_functions: ChordSymbolFunctions object with which to perform
          the actual parsing of chord symbol strings.
    """
    self._chord_symbol_functions = chord_symbol_functions

  @property
  def num_classes(self):
    return 2 * NOTES_PER_OCTAVE + 1

  @property
  def default_event(self):
    return NO_CHORD

  def encode_event(self, event):
    if event == NO_CHORD:
      return 0

    root = self._chord_symbol_functions.chord_symbol_root(event)
    quality = self._chord_symbol_functions.chord_symbol_quality(event)

    if quality == chord_symbols_lib.CHORD_QUALITY_MAJOR:
      return root + 1
    elif quality == chord_symbols_lib.CHORD_QUALITY_MINOR:
      return root + NOTES_PER_OCTAVE + 1
    else:
      raise ChordEncodingException('chord is neither major nor minor: %s'
                                   % event)

  def decode_event(self, index):
    if index == 0:
      return NO_CHORD
    elif index - 1 < 12:
      # major
      return _PITCH_CLASS_MAPPING[index - 1]
    else:
      # minor
      return _PITCH_CLASS_MAPPING[index - NOTES_PER_OCTAVE - 1] + 'm'


class TriadChordOneHotEncoding(encoder_decoder.OneHotEncoding):
  """Encodes chords as root + triad type, with zero index for "no chord".

  Encodes chords as follows:
    0:     "no chord"
    1-12:  chords with a major triad, where 1 is C major, 2 is C# major, etc.
    13-24: chords with a minor triad, where 13 is C minor, 14 is C# minor, etc.
    25-36: chords with an augmented triad, where 25 is C augmented, etc.
    37-48: chords with a diminished triad, where 37 is C diminished, etc.
  """

  def __init__(self, chord_symbol_functions=
               chord_symbols_lib.ChordSymbolFunctions.get()):
    """Initialize the TriadChordOneHotEncoding object.

    Args:
      chord_symbol_functions: ChordSymbolFunctions object with which to perform
          the actual parsing of chord symbol strings.
    """
    self._chord_symbol_functions = chord_symbol_functions

  @property
  def num_classes(self):
    return 4 * NOTES_PER_OCTAVE + 1

  @property
  def default_event(self):
    return NO_CHORD

  def encode_event(self, event):
    if event == NO_CHORD:
      return 0

    root = self._chord_symbol_functions.chord_symbol_root(event)
    quality = self._chord_symbol_functions.chord_symbol_quality(event)

    if quality == chord_symbols_lib.CHORD_QUALITY_MAJOR:
      return root + 1
    elif quality == chord_symbols_lib.CHORD_QUALITY_MINOR:
      return root + NOTES_PER_OCTAVE + 1
    elif quality == chord_symbols_lib.CHORD_QUALITY_AUGMENTED:
      return root + 2 * NOTES_PER_OCTAVE + 1
    elif quality == chord_symbols_lib.CHORD_QUALITY_DIMINISHED:
      return root + 3 * NOTES_PER_OCTAVE + 1
    else:
      raise ChordEncodingException('chord is not a standard triad: %s' % event)

  def decode_event(self, index):
    if index == 0:
      return NO_CHORD
    elif index - 1 < 12:
      # major
      return _PITCH_CLASS_MAPPING[index - 1]
    elif index - NOTES_PER_OCTAVE - 1 < 12:
      # minor
      return _PITCH_CLASS_MAPPING[index - NOTES_PER_OCTAVE - 1] + 'm'
    elif index - 2 * NOTES_PER_OCTAVE - 1 < 12:
      # augmented
      return _PITCH_CLASS_MAPPING[index - 2 * NOTES_PER_OCTAVE - 1] + 'aug'
    else:
      # diminished
      return _PITCH_CLASS_MAPPING[index - 3 * NOTES_PER_OCTAVE - 1] + 'dim'
