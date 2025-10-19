import ifaddr


def get_network_cards():
    all_cards = [("All interfaces 0.0.0.0", "0.0.0.0")]
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            if isinstance(ip.ip, tuple):  # Skip IPv6
                continue
            if ip.ip.startswith("169.254."):  # Skip link-local
                continue

            label = f"{adapter.nice_name} ({ip.ip})"
            value = ip.ip
            all_cards.append((label, value))
    return all_cards
