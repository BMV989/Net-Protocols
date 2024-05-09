import binascii
import socket

from dns_packets.config_dns import DNSConfig
from dns_packets.dns_packet_creator import DNSCreator
from dns_packets.dns_packet_parser import DNSParser


def resolve_name(name: str, record_type: str, class_record: str, root_dns: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        dns_config: DNSConfig = DNSConfig().set_query(name, record_type, class_record)
        dns_query = DNSCreator(dns_config).to_bin()

        if len(dns_query) % 2:
            dns_query += '0'

        client.sendto(bytes.fromhex(dns_query), (root_dns, 53))
        return DNSParser(binascii.b2a_hex(client.recv(1024)))
