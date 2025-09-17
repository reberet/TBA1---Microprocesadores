# receiver_udp.py (robusto: datagrama=mensaje + fallback por líneas)
# Uso:
#   python receiver_udp.py --port 5006 --idle 300 [--ack] [--debug]
import argparse, socket, json, datetime, select, sys
from guardar import guardar_datos
def now_ts():
    return datetime.datetime.now().isoformat(timespec="seconds")

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

    # Bind en todas las interfaces
    sock.bind(("0.0.0.0", args.port))
    print(f"[{now_ts()}] Servidor UDP escuchando en 0.0.0.0:{args.port} ...")

    # Estado por emisor (address -> buffers y tiempo)
    buffers = {}        # addr -> bytes buffer (acumula hasta '\n')
    last_activity = {}  # addr -> datetime

    try:
        while True:
            # select con timeout corto para revisar expiraciones
            rlist, _, _ = select.select([sock], [], [], 1.0)

            # Recepción no bloqueante (si hay datos)
            if rlist:
                try:
                    data, addr = sock.recvfrom(args.bufsize)
                except OSError as e:
                    print(f"[{now_ts()}] Error en recvfrom(): {e}")
                    continue

                # Debug crudo (opcional)
                if args.debug:
                    try:
                        ascii_preview = data.decode("utf-8", errors="replace")
                    except Exception:
                        ascii_preview = repr(data)
                    hex_preview = " ".join(f"{b:02X}" for b in data[:128])
                    print(f"[{now_ts()}] RX {addr} bytes={len(data)} ascii='{ascii_preview[:120]}' hex={hex_preview}")

                # Inicializa estructuras si es la primera vez que vemos este addr
                if addr not in buffers:
                    buffers[addr] = b""
                    last_activity[addr] = datetime.datetime.now()
                    print(f"[{now_ts()}] Nuevo emisor: {addr}")

                # Actualiza actividad
                last_activity[addr] = datetime.datetime.now()

                # --- Modo 1: intentar parsear el datagrama completo como JSON ---
                parsed = False
                try:
                    msg_full = data.decode("utf-8", errors="replace").strip("\r\n \t")
                except Exception:
                    msg_full = ""

                if msg_full:
                    try:
                        obj = json.loads(msg_full)
                        guardar_datos(obj)
                        print('SE GUARDO')
                        print(f"[{now_ts()}] {addr[0]}:{addr[1]} -> {obj}")
                        parsed = True
                        if args.ack:
                            try:
                                sock.sendto(b"OK\n", addr)
                            except OSError as e:
                                print(f"[{now_ts()}] No pude enviar ACK a {addr}: {e}")
                    except json.JSONDecodeError:
                        parsed = False  # seguimos al fallback

                # --- Modo 2 (fallback): acumulación por líneas con '\n' ---
                if not parsed:
                    buffers[addr] += data
                    while b"\n" in buffers[addr]:
                        line, buffers[addr] = buffers[addr].split(b"\n", 1)
                        msg = line.decode("utf-8", errors="replace").rstrip("\r")
                        if not msg:
                            continue
                        try:
                            obj = json.loads(msg)
                            guardar_datos(obj)
                            print(f"[{now_ts()}] {addr[0]}:{addr[1]} -> {obj}")
                            if args.ack:
                                try:
                                    sock.sendto(b"OK\n", addr)
                                except OSError as e:
                                    print(f"[{now_ts()}] No pude enviar ACK a {addr}: {e}")
                        except json.JSONDecodeError:                           
                            guardar_datos(obj)
                            print(f"[{now_ts()}] {addr[0]}:{addr[1]} -> (texto) {msg}")

            # Revisa emisores inactivos y limpia
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
