# Copyright (C) 2025 vanous
#
# This file is part of MVRtoKuma.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from types import SimpleNamespace
import pymvr
from pathlib import Path


def process_mvr_child_list(child_list, result):
    for fixture in child_list.fixtures:
        result.append((fixture))
    for group in child_list.group_objects:
        if group.child_list is not None:
            process_mvr_child_list(group.child_list, result)


def get_fixtures(file_path):
    path = Path(file_path)
    fixtures = []
    tags = {"classes": [], "layers": []}
    classes = []
    layers = []
    positions = []
    with pymvr.GeneralSceneDescription(path) as mvr_scene:
        if hasattr(mvr_scene, "scene") and mvr_scene.scene:
            for layer in mvr_scene.scene.layers:
                if layer.child_list is not None:
                    layer_fixtures = []
                    process_mvr_child_list(layer.child_list, layer_fixtures)
                    layer_result = SimpleNamespace(
                        layer=layer,
                        fixtures=layer_fixtures,
                    )
                    fixtures.append(layer_result)

        for layer in fixtures:
            mvr_layer = layer.layer
            if mvr_layer is not None:
                layers.append(
                    SimpleNamespace(uuid=mvr_layer.uuid, name=mvr_layer.name, id="")
                )
            for fixture in layer.fixtures or []:
                fixture_class_uuid = fixture.classing
                fixture_position_uuid = fixture.position
                if hasattr(mvr_scene, "scene") and mvr_scene.scene:
                    auxdata = mvr_scene.scene.aux_data
                    if auxdata is not None:
                        mvr_classes = auxdata.classes
                        mvr_positions = auxdata.positions
                print("added fixture")
                for class_ in mvr_classes:
                    if class_.uuid == fixture_class_uuid:
                        if class_.name:
                            class_ns = SimpleNamespace(
                                uuid=class_.uuid, name=class_.name, id=""
                            )
                            if class_ns not in classes:
                                classes.append(class_ns)
                for position in mvr_positions:
                    if position.uuid == fixture_position_uuid:
                        if position.name:
                            position_ns = SimpleNamespace(
                                uuid=position.uuid, name=position.name, id=""
                            )
                            if position_ns not in positions:
                                positions.append(position_ns)

    tags["classes"] = classes
    tags["positions"] = positions
    tags["layers"] = layers
    print("done mvr parsing", fixtures, tags)
    return (fixtures, tags)
