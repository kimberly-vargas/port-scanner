import socket
import argparse

# Función para escanear los puertos en un dispositivo específico
def scan_ports(target_ip, ports, protocol):
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM)
            sock.settimeout(3)
            
            if protocol == 'tcp':
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    print(f"El puerto {port} está abierto en {target_ip}")
            else:
                sock.sendto(b'', (target_ip, port))
                try:
                    data, addr = sock.recvfrom(1024)
                except socket.timeout:
                    continue
                if data:
                    print(f"El puerto {port} está abierto en {target_ip}")
                
            sock.close()
        except socket.error:
            pass

# Función para escanear los primeros 1024 puertos en un dispositivo específico
def scan_first_1024_ports(target_ip, protocol):
    ports = range(1, 1025)
    scan_ports(target_ip, ports, protocol)

# Función para escanear un grupo de puertos en un dispositivo específico
def scan_specific_ports(target_ip, ports, protocol):
    scan_ports(target_ip, ports, protocol)

# Función para escanear los primeros 1024 puertos en todos los dispositivos de una red
def scan_first_1024_ports_in_network(network_ip, protocol):
    ports = range(1, 1025)
    for i in range(1, 255):
        target_ip = f"{network_ip}.{i}"
        scan_ports(target_ip, ports, protocol)

# Función para escanear un grupo de puertos en todos los dispositivos de una red
def scan_specific_ports_in_network(network_ip, ports, protocol):
    for i in range(1, 255):
        target_ip = f"{network_ip}.{i}"
        scan_ports(target_ip, ports, protocol)

# Menú en línea de comandos
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Escaneo de puertos')
    parser.add_argument('--protocol', choices=['tcp', 'udp'], help='Protocolo de transporte (TCP o UDP)')
    parser.add_argument('--target', help='Dirección IP del dispositivo a escanear')
    parser.add_argument('--ports', help='Puertos a escanear (separados por comas)')
    parser.add_argument('--network', help='Dirección IP de la red a escanear')
    args = parser.parse_args()
    if args.protocol:
        if args.target and args.ports:
            ports = [int(port) for port in args.ports.split(',')]
            print(f"Escanenado el grupo de puertos {args.ports} en el dispositivo {args.target} usando {args.protocol}...")
            scan_specific_ports(args.target, ports, args.protocol)
        elif args.target:
            print(f"Escanenado los primeros 1024 puertos en el dispositivo {args.target} usando {args.protocol}...")
            scan_first_1024_ports(args.target, args.protocol)
        elif args.network and args.ports:
            ports = [int(port) for port in args.ports.split(',')]
            print(f"Escanenado el grupo de puertos {args.ports} en todos los dispositivos de la red {args.network} usando {args.protocol}...")
            scan_specific_ports_in_network(args.network, ports, args.protocol)
        elif args.network:
            print(f"Escanenado los primeros 1024 puertos en todos los dispositivos de la red {args.network} usando {args.protocol}...")
            scan_first_1024_ports_in_network(args.network, args.protocol)
        else:
            parser.print_help()
    else:
        parser.print_help()
