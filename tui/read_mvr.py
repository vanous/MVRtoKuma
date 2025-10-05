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
    with pymvr.GeneralSceneDescription(path) as mvr_scene:
        if hasattr(mvr_scene, "scene") and mvr_scene.scene:
            for layer in mvr_scene.scene.layers:
                if layer.child_list is not None:
                    layer_fixtures = []
                    process_mvr_child_list(layer.child_list, layer_fixtures)
                    layer_result = {
                        "layer_name": layer.name or "",
                        "fixtures": layer_fixtures,
                    }
                    fixtures.append(layer_result)

        for layer in fixtures:
            name = layer.get("layer_name", "")
            if name is not None:
                layers.append(name)
            for fixture in layer.get("fixtures", []):
                fixture_class_uuid = fixture.classing
                if hasattr(mvr_scene, "scene") and mvr_scene.scene:
                    auxdata = mvr_scene.scene.aux_data
                    if auxdata is not None:
                        mvr_classes = auxdata.classes

                for class_ in mvr_classes:
                    if class_.uuid == fixture_class_uuid:
                        if class_.name:
                            classes.append(class_.name)

    tags["classes"] = classes
    tags["layers"] = layers
    return (fixtures, tags)
