import ifaddr
import ipaddress


def get_network_cards():
    all_cards = [("0.0.0.0", "0.0.0.0", "255.255.255.255")]
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            if isinstance(ip.ip, tuple):  # Skip IPv6
                continue
            if ip.ip.startswith("169.254."):  # Skip link-local
                continue

            label = f"{adapter.nice_name} ({ip.ip})"
            ip_address = ip.ip

            netmask_str = ip.network_prefix
            interface = ipaddress.IPv4Interface(f"{ip_address}/{netmask_str}")
            broadcast = interface.network.broadcast_address

            all_cards.append((ip_address, label, broadcast))
    return all_cards
