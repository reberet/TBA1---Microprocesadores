# receiver_udp.py (robusto: datagrama=mensaje + fallback por líneas + validación JSON)
# Uso:
#   python receiver_udp.py --port 5006 --idle 300 [--ack] [--debug]

import argparse, socket, json, datetime, select
from guardar import guardar_datos
from guardar import guardar_historial

def now_ts():
    return datetime.datetime.now().isoformat(timespec="seconds")

# --- Validación estricta ---
def validar_json(obj):
    """
    Verifica que el JSON tenga todos los campos requeridos con valores válidos.
    Estructura: {"disco":0-100,"ilum":0-100,"puerta":0|1,"ruido":0-140,"temp":0-100,"fuego":0|1}
    """
    schema = {
        "disco": (0, 100),
        "ilum": (0, 100),
        "puerta": (0, 1),
        "ruido": (0, 140),
        "temp": (0, 100),
        "fuego": (0, 1),
    }

    # Deben estar todas las claves
    for k, (low, high) in schema.items():
        if k not in obj:
            return False, f"Falta campo requerido: {k}"
        v = obj[k]
        if not isinstance(v, (int, float)):
            return False, f"Campo {k} no es numérico"
        if not (low <= v <= high):
            return False, f"Campo {k} fuera de rango ({v}, permitido {low}-{high})"

    return True, "OK"

def procesar_json(obj, addr, sock, args):
    valido, msg = validar_json(obj)
    guardar_historial(obj)
    if valido:
        guardar_datos(obj)
        print(f"[{now_ts()}] {addr[0]}:{addr[1]} -> {obj} (guardado)")
        if args.ack:
            try:
                sock.sendto(b"OK\n", addr)
            except OSError as e:
                print(f"[{now_ts()}] No pude enviar ACK a {addr}: {e}")
    else:
        print(f"[{now_ts()}] {addr[0]}:{addr[1]} JSON inválido: {msg} -> ignorado")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=5006, help="Puerto UDP de escucha")
    p.add_argument("--idle", type=int, default=300, help="Tiempo máx. de inactividad por emisor (s)")
    p.add_argument("--ack", action="store_true", help="Responder 'OK\\n' por UDP al remitente")
    p.add_argument("--bufsize", type=int, default=65535, help="Tamaño del buffer de recepción UDP")
    p.add_argument("--debug", action="store_true", help="Log de bytes crudos (hex + ascii preview)")
    args = p.parse_args()

    # Socket UDP de escucha
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except OSError:
        pass

    sock.bind(("0.0.0.0", args.port))
    print(f"[{now_ts()}] Servidor UDP escuchando en 0.0.0.0:{args.port} ...")

    buffers = {}
    last_activity = {}

    try:
        while True:
            rlist, _, _ = select.select([sock], [], [], 1.0)
            if rlist:
                try:
                    data, addr = sock.recvfrom(args.bufsize)
                except OSError as e:
                    print(f"[{now_ts()}] Error en recvfrom(): {e}")
                    continue

                if args.debug:
                    try:
                        ascii_preview = data.decode("utf-8", errors="replace")
                    except Exception:
                        ascii_preview = repr(data)
                    hex_preview = " ".join(f"{b:02X}" for b in data[:128])
                    print(f"[{now_ts()}] RX {addr} bytes={len(data)} ascii='{ascii_preview[:120]}' hex={hex_preview}")

                if addr not in buffers:
                    buffers[addr] = b""
                    last_activity[addr] = datetime.datetime.now()
                    print(f"[{now_ts()}] Nuevo emisor: {addr}")

                last_activity[addr] = datetime.datetime.now()

                parsed = False
                try:
                    msg_full = data.decode("utf-8", errors="replace").strip("\r\n \t")
                except Exception:
                    msg_full = ""

                if msg_full:
                    try:
                        obj = json.loads(msg_full)
                        procesar_json(obj, addr, sock, args)
                        parsed = True
                    except json.JSONDecodeError:
                        parsed = False

                if not parsed:
                    buffers[addr] += data
                    while b"\n" in buffers[addr]:
                        line, buffers[addr] = buffers[addr].split(b"\n", 1)
                        msg = line.decode("utf-8", errors="replace").rstrip("\r")
                        if not msg:
                            continue
                        try:
                            obj = json.loads(msg)
                            procesar_json(obj, addr, sock, args)
                        except json.JSONDecodeError:
                            print(f"[{now_ts()}] {addr[0]}:{addr[1]} -> (texto no JSON) {msg}")

            now = datetime.datetime.now()
            to_del = []
            for a, tlast in list(last_activity.items()):
                if (now - tlast).total_seconds() > args.idle:
                    print(f"[{now_ts()}] {a[0]}:{a[1]} inactivo {args.idle}s, limpiando estado.")
                    to_del.append(a)
            for a in to_del:
                last_activity.pop(a, None)
                buffers.pop(a, None)

    except KeyboardInterrupt:
        print("\nCerrando servidor UDP...")
    finally:
        try:
            sock.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()

