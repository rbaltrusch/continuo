# -*- coding: utf-8 -*-
"""Timeline module tests"""

import numpy
from continuo import layer, timeline, scale


def test_render_hit():
    timeline.Hit(note=0, length=1).render()


def test_set_time():
    timeline_ = timeline.Timeline()
    timeline_.set_time(2)
    assert timeline_._time == 2


def test_add():
    timeline_ = timeline.Timeline()
    timeline_.set_time(2)
    hit = timeline.Hit(note="A", length=23)
    timeline_.add(hit)
    assert timeline_._time == 25


def test_calculate_length():
    timeline_ = timeline.Timeline()
    timeline_.set_time(2)
    hit = timeline.Hit(note="A", length=23)
    timeline_.add(hit)

    timeline_.set_time(20)
    hit = timeline.Hit(note="A", length=4)
    timeline_.add(hit)

    assert timeline_.calculate_length() == 25


def test_construct():
    timeline_ = timeline.Timeline()
    scale_ = scale.Scale("A3", "major", length=7)
    layers = [
        layer.Layer(notes=[1, 2, 3]),
        layer.Layer(notes=[2, 5, 8]),
    ]
    timeline_.construct(layers, scale_)
    assert len(timeline_.hits) == 6
    assert timeline_.calculate_length() == 0.75


def test_render():
    timeline_ = timeline.Timeline(rate=44100, tempo=120)
    scale_ = scale.Scale("A3", "major", length=7)
    layers = [layer.Layer(notes=[1])]
    timeline_.construct(layers, scale_)
    data = timeline_.render()
    assert isinstance(data, numpy.ndarray)
    assert data.size == 44100 // 4


def test_append_note():
    class Note:
        def transpose(self, _):
            pass

    timeline_ = timeline.Timeline(tempo=120)
    timeline_.append_note(note=Note(), note_length=1, octavify=True)
    assert len(timeline_.hits) == 2
    assert timeline_.calculate_length() == 1

    timeline_.append_note(note=0, note_length=2, octavify=False)
    assert timeline_.calculate_length() == 3


def test_eigth():
    timeline_ = timeline.Timeline(rate=44100, tempo=120)
    assert timeline_.eigth == 0.25
