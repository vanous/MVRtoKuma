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
