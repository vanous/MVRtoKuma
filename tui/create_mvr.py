import pymvr
from pathlib import Path


def create_mvr(devices):
    mvr_writer = pymvr.GeneralSceneDescriptionWriter()
    scene_obj = pymvr.Scene()
    aux_data = pymvr.AUXData()
    layers = pymvr.Layers()
    scene_obj.layers = layers
    scene_obj.aux_data = aux_data

    layer = pymvr.Layer(name="Network discovery")
    layers.append(layer)

    child_list = pymvr.ChildList()
    layer.child_list = child_list

    for net_fixture in devices:
        fixture = pymvr.Fixture(name=net_fixture.short_name)
        fixture.addresses.network.append(pymvr.Network(ipv4=net_fixture.ip_address))
        if net_fixture.address is not None:
            address = 1
            universe = 1
            try:
                address = int(net_fixture.address or 1)
                universe = int(net_fixture.universe or 1)
            except:
                ...
            fixture.addresses.address.append(
                pymvr.Address(
                    dmx_break=0,
                    universe=universe,
                    address=address,
                )
            )

        child_list.fixtures.append(fixture)

    scene_obj.to_xml(parent=mvr_writer.xml_root)

    output_path = Path("discovered_devices.mvr")
    mvr_writer.write_mvr(output_path)
