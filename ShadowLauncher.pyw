# # #!/usr/bin/env python3
# # import sys
# # import re
# # import hmac
# # import json
# # import time
# # import base64
# # import hashlib
# # import io
# # import os
# # import uuid
# # import platform
# # import ctypes
# # import urllib.request
# # import urllib.error
# # import ssl
# # import webbrowser
# # import socket

# # # ═══ EMBEDDED LICENSE KEY ═══
# # _LICENSE_KEY = ""

# # def _has_console():
# #     return sys.stdin is not None and sys.stdin.isatty()

# # def _gui_input(title, prompt):
# #     import tkinter as tk
# #     from tkinter import simpledialog
# #     root = tk.Tk()
# #     root.withdraw()
# #     root.attributes('-topmost', True)
# #     result = simpledialog.askstring(title, prompt, parent=root)
# #     root.destroy()
# #     return result

# # def _ask(title, prompt):
# #     if _has_console():
# #         print(f"\n  {prompt}")
# #         try:
# #             return input("  > ").strip()
# #         except (EOFError, RuntimeError):
# #             return _gui_input(title, prompt)
# #     else:
# #         return _gui_input(title, prompt)

# # def _show_msg(title, message, msg_type=0):
# #     if _has_console():
# #         print(f"\n  {message}")
# #     ctypes.windll.user32.MessageBoxW(0, message, title, msg_type)

# # def _show_expired_window(error_text, button_text="Renew Subscription"):
# #     import tkinter as tk
# #     root = tk.Tk()
# #     root.title("Shadow Lab")
# #     root.geometry("480x280")
# #     root.resizable(False, False)
# #     root.configure(bg="#1a1a2e")
# #     root.attributes('-topmost', True)
# #     try:
# #         root.iconify()
# #         root.update()
# #         root.deiconify()
# #     except Exception:
# #         pass
# #     root.update_idletasks()
# #     x = (root.winfo_screenwidth() // 2) - (480 // 2)
# #     y = (root.winfo_screenheight() // 2) - (280 // 2)
# #     root.geometry(f"+{x}+{y}")

# #     tk.Label(root, text="Subscription Expired", font=("Segoe UI", 16, "bold"), fg="#e94560", bg="#1a1a2e").pack(pady=(20, 10))
# #     tk.Label(root, text=error_text, font=("Segoe UI", 10), fg="#eaeaea", bg="#1a1a2e", wraplength=440, justify="center").pack(pady=(0, 15))

# #     def _open_pricing():
# #         webbrowser.open("https://shadowlab.fun/#pricing")
# #         root.destroy()
# #     def _close():
# #         root.destroy()

# #     frm = tk.Frame(root, bg="#1a1a2e")
# #     frm.pack(pady=5)
# #     tk.Button(frm, text=button_text, font=("Segoe UI", 10, "bold"), bg="#e94560", fg="#ffffff", bd=0, padx=20, pady=8, cursor="hand2", command=_open_pricing).pack(side="left", padx=5)
# #     tk.Button(frm, text="Close", font=("Segoe UI", 10), bg="#16213e", fg="#eaeaea", bd=0, padx=20, pady=8, cursor="hand2", command=_close).pack(side="left", padx=5)
# #     root.mainloop()

# # if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
# #     try:
# #         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
# #     except Exception:
# #         pass

# # _K1 = "366afe534167590241a4782bb5ad96aea5728e22ce1924749a48150fc4a9a5cd"
# # _K2 = "3918f3f3e8d335dbff05e5d30bd93f82db2c17798034b06120012c6a5553a546"
# # _ENC_INFO = b"shadow-lab:enc:v3:aes256gcm"
# # _MAC_INFO = b"shadow-lab:mac:v3:hmacsha256"

# # def _hkdf_extract(salt, ikm):
# #     return hmac.new(salt, ikm, hashlib.sha256).digest()

# # def _hkdf_expand(prk, info, length):
# #     okm, t, i = b'', b'', 1
# #     while len(okm) < length:
# #         t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
# #         okm += t
# #         i += 1
# #     return okm[:length]

# # def _hkdf(master_key, salt, info, length):
# #     prk = _hkdf_extract(salt, master_key)
# #     return _hkdf_expand(prk, info, length)

# # def _keystream(seed, length):
# #     result, block = b'', seed
# #     while len(result) < length:
# #         block = hmac.new(seed, block, hashlib.sha256).digest()
# #         result += block
# #     return result[:length]

# # def _format_time_remaining(seconds):
# #     if seconds <= 0:
# #         return "Expired"
# #     days = seconds // 86400
# #     hours = (seconds % 86400) // 3600
# #     minutes = (seconds % 3600) // 60
# #     parts = []
# #     if days > 0:
# #         parts.append(f"{days} day{'s' if days != 1 else ''}")
# #     if hours > 0:
# #         parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
# #     if days == 0 and minutes > 0:
# #         parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
# #     if not parts:
# #         parts.append(f"{seconds} sec{'s' if seconds != 1 else ''}")
# #     return " ".join(parts) + " remaining"

# # def _verify(key):
# #     try:
# #         K1 = bytes.fromhex(_K1)
# #         K2 = bytes.fromhex(_K2)
# #     except Exception:
# #         return {"ok": False, "code": "E_CFG"}

# #     m = re.match(r'^SHADOW-([A-Z]+)-V3-([A-Za-z0-9\-_]+)$', key.strip())
# #     if not m:
# #         return {"ok": False, "code": "E_FMT"}

# #     b64 = m.group(2).replace('-', '+').replace('_', '/')
# #     b64 += '=' * ((4 - len(b64) % 4) % 4)
# #     try:
# #         packed = base64.b64decode(b64)
# #     except Exception:
# #         return {"ok": False, "code": "E_DEC"}

# #     if len(packed) < 97:
# #         return {"ok": False, "code": "E_LEN"}

# #     salt       = packed[0:32]
# #     iv         = packed[32:48]
# #     auth_tag   = packed[48:64]
# #     stored_mac = packed[64:96]
# #     ciphertext = packed[96:]

# #     aes_key = _hkdf(K1, salt, _ENC_INFO, 32)

# #     try:
# #         from Crypto.Cipher import AES
# #         cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
# #         xored  = cipher.decrypt_and_verify(ciphertext, auth_tag)
# #     except ImportError:
# #         return {"ok": False, "code": "E_DEP"}
# #     except ValueError:
# #         return {"ok": False, "code": "E_AES"}

# #     xor_seed = hmac.new(aes_key, salt + iv, hashlib.sha256).digest()
# #     stream   = _keystream(xor_seed, len(xored))
# #     plain    = bytes(a ^ b for a, b in zip(xored, stream))

# #     if len(plain) < 1:
# #         return {"ok": False, "code": "E_PAD"}

# #     pad_len       = plain[0]
# #     payload_bytes = plain[1 + pad_len:]

# #     try:
# #         data = json.loads(payload_bytes.decode("utf-8"))
# #     except Exception:
# #         return {"ok": False, "code": "E_JSON"}

# #     now      = int(time.time())
# #     exp_ts   = data.get("e", 0)
# #     active   = now < exp_ts
# #     diff_sec = max(0, exp_ts - now)

# #     return {
# #         "ok": active,
# #         "time_str": _format_time_remaining(diff_sec),
# #         "code": "ACTIVE" if active else "EXPIRED"
# #     }

# # def _get_hwid():
# #     raw = f"{uuid.getnode()}-{platform.node()}-{platform.machine()}"
# #     return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# # def _test_connection(host, port=443, timeout=5):
# #     try:
# #         sock = socket.create_connection((host, port), timeout=timeout)
# #         sock.close()
# #         return True
# #     except Exception as e:
# #         return str(e)

# # # ═══ FIX: HTTP 308 Redirect Handler ═══
# # class HTTP308RedirectHandler(urllib.request.HTTPRedirectHandler):
# #     def http_error_308(self, req, fp, code, msg, headers):
# #         return self.http_error_302(req, fp, code, msg, headers)
# #     https_error_308 = http_error_308

# # def _verify_online(key, hwid):
# #     import ssl
# #     ctx = ssl._create_unverified_context()

# #     urls = [
# #         "https://shadowlab.fun/api/license/verify/", 
# #         "http://shadowlab.fun/api/license/verify/", 
# #         "http://localhost:3000/api/license/verify/", 
# #     ]

# #     api_url = os.environ.get("SHADOW_API_URL", "").strip()
# #     if api_url:
# #         urls.insert(0, api_url)

# #     payload = json.dumps({
# #         "license_key": key.strip(),
# #         "device_identifier_hash": hwid
# #     }).encode("utf-8")

# #     proxies = urllib.request.getproxies()
# #     handlers = [urllib.request.ProxyHandler(proxies)]
# #     handlers.append(urllib.request.HTTPSHandler(context=ctx))
# #     # ═══ FIX: Add 308 redirect handler ═══
# #     handlers.append(HTTP308RedirectHandler())
# #     opener = urllib.request.build_opener(*handlers)

# #     last_error = ""
# #     connection_log = []

# #     for url in urls:
# #         try:
# #             req = urllib.request.Request(
# #                 url,
# #                 data=payload,
# #                 headers={
# #                     "Content-Type": "application/json",
# #                     "User-Agent": "ShadowVerify/3.0 (Windows NT 10.0; Win64; x64)"
# #                 },
# #                 method="POST"
# #             )
# #             with opener.open(req, timeout=10) as resp:
# #                 if resp.status == 200:
# #                     data = json.loads(resp.read().decode("utf-8"))
# #                     if data.get("authorized"):
# #                         return {
# #                             "ok": True,
# #                             "source": "ONLINE_DATABASE",
# #                             "time_str": data.get("time_remaining", "Active"),
# #                             "plan": data.get("plan_name", "Pro"),
# #                             "code": "ACTIVE"
# #                         }
# #         except urllib.error.HTTPError as e:
# #             if e.code in (400, 401, 403, 429):
# #                 try:
# #                     body_text = e.read().decode("utf-8", errors="ignore")
# #                     err_data = json.loads(body_text)
# #                     err_state = err_data.get("subscription_state", "EXPIRED")
# #                     err_msg   = err_data.get("error", "Subscription Unauthorized")
# #                     return {
# #                         "ok": False,
# #                         "source": "ONLINE_DATABASE",
# #                         "code": err_state,
# #                         "msg": err_msg
# #                     }
# #                 except Exception:
# #                     pass
# #             last_error = f"HTTP {e.code} on {url}"
# #             connection_log.append(last_error)
# #             continue
# #         except urllib.error.URLError as e:
# #             last_error = f"{url}: {e.reason}"
# #             connection_log.append(last_error)
# #             continue
# #         except Exception as e:
# #             last_error = f"{url}: {str(e)}"
# #             connection_log.append(last_error)
# #             continue

# #     tcp_test = _test_connection("shadowlab.fun", 443)
# #     tcp_ok = tcp_test is True

# #     if not tcp_ok:
# #         net_msg = (
# #             f"TCP test to shadowlab.fun:443 FAILED ({tcp_test})\n\n"
# #             "Your network is actively blocking the license server.\n"
# #             "Try using a mobile hotspot or disable VPN."
# #         )
# #     else:
# #         net_msg = (
# #             "Server is reachable but API returned an error.\n"
# #             "Please contact support with the error details below."
# #         )

# #     full_log = "\n".join(connection_log)
# #     return {
# #         "ok": False,
# #         "code": "E_NET",
# #         "msg": f"Could not reach license server.\n\n{net_msg}\n\nAttempt log:\n{full_log}"
# #     }

# # def _error_details(result):
# #     code = result.get("code", "")
# #     msg  = result.get("msg", "")

# #     if code == "E_NET":
# #         return (msg, "Buy Subscription")
# #     elif code == "REVOKED" or "REVOKED" in msg:
# #         return ("This license key was revoked. Contact support.", "Buy Subscription")
# #     elif code == "DEVICE_LOCKED" or "HWID_MISMATCH" in msg:
# #         return ("License is bound to another PC. Reset in Dashboard.", "Buy Subscription")
# #     elif code == "EXPIRED":
# #         return ("Your subscription has expired. Please renew your subscription.", "Renew Subscription")
# #     elif code == "E_FMT":
# #         return ("Invalid license key format. Check the key and try again.", "Buy Subscription")
# #     elif code == "E_SIG":
# #         return ("This key has been modified. Contact support.", "Buy Subscription")
# #     else:
# #         if msg:
# #             return (msg, "Buy Subscription")
# #         return ("Your license is not valid or has expired. Contact support.", "Buy Subscription")

# # def _find_injector():
# #     if getattr(sys, 'frozen', False):
# #         base = os.path.dirname(sys.executable)
# #     else:
# #         base = os.path.dirname(os.path.abspath(__file__))

# #     candidates = [
# #         os.path.join(base, "DLL_Injector", "DLL_Injector.exe"),
# #         os.path.join(os.path.dirname(base), "DLL_Injector", "DLL_Injector.exe"),
# #         os.path.join(base, "dll_injector", "dll_injector.exe"),
# #         r"C:\Users\Stranger\Desktop\ProcessHider\DLL_Injector\DLL_Injector.exe",
# #     ]

# #     for path in candidates:
# #         if os.path.exists(path):
# #             return path
# #     return None

# # def _launch_injector():
# #     injector_path = _find_injector()
# #     if not injector_path:
# #         _show_msg("Error", "DLL_Injector.exe not found.", 0x10)
# #         return False

# #     ret = ctypes.windll.shell32.ShellExecuteW(
# #         None, "runas", injector_path, None,
# #         os.path.dirname(injector_path), 1
# #     )
# #     if ret > 32:
# #         return True
# #     else:
# #         _show_msg("Error", f"Failed to launch injector as Administrator.\nUAC denied or error code: {ret}", 0x10)
# #         return False

# # def main():
# #     if _LICENSE_KEY and _LICENSE_KEY.strip():
# #         key = _LICENSE_KEY.strip()
# #     elif len(sys.argv) > 1:
# #         key = " ".join(sys.argv[1:]).strip()
# #     else:
# #         key = _ask("License Key", "Enter your license key:")

# #     if not key:
# #         _show_msg("Error", "No license key entered.", 0x10)
# #         sys.exit(1)

# #     hwid = _get_hwid()
# #     result = _verify_online(key, hwid)

# #     if not result.get("ok"):
# #         error_text, button_text = _error_details(result)
# #         _show_expired_window(error_text, button_text)
# #         sys.exit(1)

# #     _launch_injector()
# #     sys.exit(0)

# # if __name__ == "__main__":
# #     main()


# #!/usr/bin/env python3

# #!/usr/bin/env python3
# import sys
# import re
# import hmac
# import json
# import time
# import base64
# import hashlib
# import io
# import os
# import uuid
# import platform
# import ctypes
# import urllib.request
# import urllib.error
# import urllib.parse
# import ssl
# import webbrowser
# import socket

# # ═══ EMBEDDED LICENSE KEY ═══
# _LICENSE_KEY = ""

# def _has_console():
#     return sys.stdin is not None and sys.stdin.isatty()

# def _gui_input(title, prompt):
#     import tkinter as tk
#     from tkinter import simpledialog
#     root = tk.Tk()
#     root.withdraw()
#     root.attributes('-topmost', True)
#     result = simpledialog.askstring(title, prompt, parent=root)
#     root.destroy()
#     return result

# def _ask(title, prompt):
#     if _has_console():
#         print(f"\n  {prompt}")
#         try:
#             return input("  > ").strip()
#         except (EOFError, RuntimeError):
#             return _gui_input(title, prompt)
#     else:
#         return _gui_input(title, prompt)

# def _show_msg(title, message, msg_type=0):
#     if _has_console():
#         print(f"\n  {message}")
#     ctypes.windll.user32.MessageBoxW(0, message, title, msg_type)

# def _show_expired_window(error_text, button_text="Renew Subscription"):
#     import tkinter as tk
#     root = tk.Tk()
#     root.title("Shadow Lab")
#     root.geometry("480x280")
#     root.resizable(False, False)
#     root.configure(bg="#1a1a2e")
#     root.attributes('-topmost', True)
#     try:
#         root.iconify()
#         root.update()
#         root.deiconify()
#     except Exception:
#         pass
#     root.update_idletasks()
#     x = (root.winfo_screenwidth() // 2) - (480 // 2)
#     y = (root.winfo_screenheight() // 2) - (280 // 2)
#     root.geometry(f"+{x}+{y}")

#     tk.Label(root, text="Subscription Expired", font=("Segoe UI", 16, "bold"), fg="#e94560", bg="#1a1a2e").pack(pady=(20, 10))
#     tk.Label(root, text=error_text, font=("Segoe UI", 10), fg="#eaeaea", bg="#1a1a2e", wraplength=440, justify="center").pack(pady=(0, 15))

#     def _open_pricing():
#         webbrowser.open("https://shadowlab.fun/#pricing")
#         root.destroy()
#     def _close():
#         root.destroy()

#     frm = tk.Frame(root, bg="#1a1a2e")
#     frm.pack(pady=5)
#     tk.Button(frm, text=button_text, font=("Segoe UI", 10, "bold"), bg="#e94560", fg="#ffffff", bd=0, padx=20, pady=8, cursor="hand2", command=_open_pricing).pack(side="left", padx=5)
#     tk.Button(frm, text="Close", font=("Segoe UI", 10), bg="#16213e", fg="#eaeaea", bd=0, padx=20, pady=8, cursor="hand2", command=_close).pack(side="left", padx=5)
#     root.mainloop()

# if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
#     try:
#         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
#     except Exception:
#         pass

# _K1 = "366afe534167590241a4782bb5ad96aea5728e22ce1924749a48150fc4a9a5cd"
# _K2 = "3918f3f3e8d335dbff05e5d30bd93f82db2c17798034b06120012c6a5553a546"
# _ENC_INFO = b"shadow-lab:enc:v3:aes256gcm"
# _MAC_INFO = b"shadow-lab:mac:v3:hmacsha256"

# def _hkdf_extract(salt, ikm):
#     return hmac.new(salt, ikm, hashlib.sha256).digest()

# def _hkdf_expand(prk, info, length):
#     okm, t, i = b'', b'', 1
#     while len(okm) < length:
#         t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
#         okm += t
#         i += 1
#     return okm[:length]

# def _hkdf(master_key, salt, info, length):
#     prk = _hkdf_extract(salt, master_key)
#     return _hkdf_expand(prk, info, length)

# def _keystream(seed, length):
#     result, block = b'', seed
#     while len(result) < length:
#         block = hmac.new(seed, block, hashlib.sha256).digest()
#         result += block
#     return result[:length]

# def _format_time_remaining(seconds):
#     if seconds <= 0:
#         return "Expired"
#     days = seconds // 86400
#     hours = (seconds % 86400) // 3600
#     minutes = (seconds % 3600) // 60
#     parts = []
#     if days > 0:
#         parts.append(f"{days} day{'s' if days != 1 else ''}")
#     if hours > 0:
#         parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
#     if days == 0 and minutes > 0:
#         parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
#     if not parts:
#         parts.append(f"{seconds} sec{'s' if seconds != 1 else ''}")
#     return " ".join(parts) + " remaining"

# def _verify(key):
#     try:
#         K1 = bytes.fromhex(_K1)
#         K2 = bytes.fromhex(_K2)
#     except Exception:
#         return {"ok": False, "code": "E_CFG"}

#     m = re.match(r'^SHADOW-([A-Z]+)-V3-([A-Za-z0-9\-_]+)$', key.strip())
#     if not m:
#         return {"ok": False, "code": "E_FMT"}

#     b64 = m.group(2).replace('-', '+').replace('_', '/')
#     b64 += '=' * ((4 - len(b64) % 4) % 4)
#     try:
#         packed = base64.b64decode(b64)
#     except Exception:
#         return {"ok": False, "code": "E_DEC"}

#     if len(packed) < 97:
#         return {"ok": False, "code": "E_LEN"}

#     salt       = packed[0:32]
#     iv         = packed[32:48]
#     auth_tag   = packed[48:64]
#     stored_mac = packed[64:96]
#     ciphertext = packed[96:]

#     aes_key = _hkdf(K1, salt, _ENC_INFO, 32)

#     try:
#         from Crypto.Cipher import AES
#         cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
#         xored  = cipher.decrypt_and_verify(ciphertext, auth_tag)
#     except ImportError:
#         return {"ok": False, "code": "E_DEP"}
#     except ValueError:
#         return {"ok": False, "code": "E_AES"}

#     xor_seed = hmac.new(aes_key, salt + iv, hashlib.sha256).digest()
#     stream   = _keystream(xor_seed, len(xored))
#     plain    = bytes(a ^ b for a, b in zip(xored, stream))

#     if len(plain) < 1:
#         return {"ok": False, "code": "E_PAD"}

#     pad_len       = plain[0]
#     payload_bytes = plain[1 + pad_len:]

#     try:
#         data = json.loads(payload_bytes.decode("utf-8"))
#     except Exception:
#         return {"ok": False, "code": "E_JSON"}

#     now      = int(time.time())
#     exp_ts   = data.get("e", 0)
#     active   = now < exp_ts
#     diff_sec = max(0, exp_ts - now)

#     return {
#         "ok": active,
#         "time_str": _format_time_remaining(diff_sec),
#         "code": "ACTIVE" if active else "EXPIRED"
#     }

# def _get_hwid():
#     raw = f"{uuid.getnode()}-{platform.node()}-{platform.machine()}"
#     return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# def _test_connection(host, port=443, timeout=5):
#     try:
#         sock = socket.create_connection((host, port), timeout=timeout)
#         sock.close()
#         return True
#     except Exception as e:
#         return str(e)

# # ═══ FIX: HTTP 308 Redirect Handler (preserves POST method & body) ═══
# class HTTP308RedirectHandler(urllib.request.HTTPRedirectHandler):
#     def http_error_308(self, req, fp, code, msg, headers):
#         # 308 = Permanent Redirect, must preserve method and body (like 307)
#         newurl = headers.get('Location')
#         if not newurl:
#             return None
#         newurl = urllib.parse.urljoin(req.full_url, newurl)
        
#         # Create new request preserving POST data and headers
#         newreq = urllib.request.Request(
#             newurl,
#             data=req.data,
#             headers=dict(req.header_items()),
#             method=req.get_method(),
#             unverifiable=True
#         )
#         # Remove hop-by-hop headers
#         for h in ('Content-Length', 'Transfer-Encoding', 'Host'):
#             newreq.headers.pop(h, None)
        
#         return self.parent.open(newreq, timeout=req.timeout)
    
#     https_error_308 = http_error_308

# def _verify_online(key, hwid):
#     import ssl
#     ctx = ssl._create_unverified_context()

#     # Try both with and without trailing slash to avoid 308 loops
#     urls = [
#         "https://shadowlab.fun/api/license/verify",
#         "https://shadowlab.fun/api/license/verify/", 
#         "http://shadowlab.fun/api/license/verify",
#         "http://shadowlab.fun/api/license/verify/", 
#         "http://localhost:3000/api/license/verify",
#         "http://localhost:3000/api/license/verify/", 
#     ]

#     api_url = os.environ.get("SHADOW_API_URL", "").strip()
#     if api_url:
#         urls.insert(0, api_url)

#     payload = json.dumps({
#         "license_key": key.strip(),
#         "device_identifier_hash": hwid
#     }).encode("utf-8")

#     proxies = urllib.request.getproxies()
#     handlers = [
#         urllib.request.ProxyHandler(proxies),
#         urllib.request.HTTPSHandler(context=ctx),
#         HTTP308RedirectHandler()
#     ]
#     opener = urllib.request.build_opener(*handlers)

#     last_error = ""
#     connection_log = []

#     for url in urls:
#         try:
#             req = urllib.request.Request(
#                 url,
#                 data=payload,
#                 headers={
#                     "Content-Type": "application/json",
#                     "User-Agent": "ShadowVerify/3.0 (Windows NT 10.0; Win64; x64)"
#                 },
#                 method="POST"
#             )
#             with opener.open(req, timeout=10) as resp:
#                 if resp.status == 200:
#                     data = json.loads(resp.read().decode("utf-8"))
#                     if data.get("authorized"):
#                         return {
#                             "ok": True,
#                             "source": "ONLINE_DATABASE",
#                             "time_str": data.get("time_remaining", "Active"),
#                             "plan": data.get("plan_name", "Pro"),
#                             "code": "ACTIVE"
#                         }
#         except urllib.error.HTTPError as e:
#             if e.code in (400, 401, 403, 429):
#                 try:
#                     body_text = e.read().decode("utf-8", errors="ignore")
#                     err_data = json.loads(body_text)
#                     err_state = err_data.get("subscription_state", "EXPIRED")
#                     err_msg   = err_data.get("error", "Subscription Unauthorized")
#                     return {
#                         "ok": False,
#                         "source": "ONLINE_DATABASE",
#                         "code": err_state,
#                         "msg": err_msg
#                     }
#                 except Exception:
#                     pass
#             last_error = f"HTTP {e.code} on {url}"
#             connection_log.append(last_error)
#             continue
#         except urllib.error.URLError as e:
#             last_error = f"{url}: {e.reason}"
#             connection_log.append(last_error)
#             continue
#         except Exception as e:
#             last_error = f"{url}: {str(e)}"
#             connection_log.append(last_error)
#             continue

#     tcp_test = _test_connection("shadowlab.fun", 443)
#     tcp_ok = tcp_test is True

#     if not tcp_ok:
#         net_msg = (
#             f"TCP test to shadowlab.fun:443 FAILED ({tcp_test})\n\n"
#             "Your network is actively blocking the license server.\n"
#             "Try using a mobile hotspot or disable VPN."
#         )
#     else:
#         net_msg = (
#             "Server is reachable but API returned an error.\n"
#             "Please contact support with the error details below."
#         )

#     full_log = "\n".join(connection_log)
#     return {
#         "ok": False,
#         "code": "E_NET",
#         "msg": f"Could not reach license server.\n\n{net_msg}\n\nAttempt log:\n{full_log}"
#     }

# def _error_details(result):
#     code = result.get("code", "")
#     msg  = result.get("msg", "")

#     if code == "E_NET":
#         return (msg, "Buy Subscription")
#     elif code == "REVOKED" or "REVOKED" in msg:
#         return ("This license key was revoked. Contact support.", "Buy Subscription")
#     elif code == "DEVICE_LOCKED" or "HWID_MISMATCH" in msg:
#         return ("License is bound to another PC. Reset in Dashboard.", "Buy Subscription")
#     elif code == "EXPIRED":
#         return ("Your subscription has expired. Please renew your subscription.", "Renew Subscription")
#     elif code == "E_FMT":
#         return ("Invalid license key format. Check the key and try again.", "Buy Subscription")
#     elif code == "E_SIG":
#         return ("This key has been modified. Contact support.", "Buy Subscription")
#     else:
#         if msg:
#             return (msg, "Buy Subscription")
#         return ("Your license is not valid or has expired. Contact support.", "Buy Subscription")

# def _find_injector():
#     if getattr(sys, 'frozen', False):
#         base = os.path.dirname(sys.executable)
#     else:
#         base = os.path.dirname(os.path.abspath(__file__))

#     candidates = [
#         os.path.join(base, "DLL_Injector", "DLL_Injector.exe"),
#         os.path.join(os.path.dirname(base), "DLL_Injector", "DLL_Injector.exe"),
#         os.path.join(base, "dll_injector", "dll_injector.exe"),
#         r"C:\Users\Stranger\Desktop\ProcessHider\DLL_Injector\DLL_Injector.exe",
#     ]

#     for path in candidates:
#         if os.path.exists(path):
#             return path
#     return None

# def _launch_injector():
#     injector_path = _find_injector()
#     if not injector_path:
#         _show_msg("Error", "DLL_Injector.exe not found.", 0x10)
#         return False

#     ret = ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", injector_path, None,
#         os.path.dirname(injector_path), 1
#     )
#     if ret > 32:
#         return True
#     else:
#         _show_msg("Error", f"Failed to launch injector as Administrator.\nUAC denied or error code: {ret}", 0x10)
#         return False

# def main():
#     if _LICENSE_KEY and _LICENSE_KEY.strip():
#         key = _LICENSE_KEY.strip()
#     elif len(sys.argv) > 1:
#         key = " ".join(sys.argv[1:]).strip()
#     else:
#         key = _ask("License Key", "Enter your license key:")

#     if not key:
#         _show_msg("Error", "No license key entered.", 0x10)
#         sys.exit(1)

#     hwid = _get_hwid()
#     result = _verify_online(key, hwid)

#     if not result.get("ok"):
#         error_text, button_text = _error_details(result)
#         _show_expired_window(error_text, button_text)
#         sys.exit(1)

#     _launch_injector()
#     sys.exit(0)

# if __name__ == "__main__":
#     main()






# import sys
# import re
# import hmac
# import json
# import time
# import base64
# import hashlib
# import io
# import os
# import uuid
# import platform
# import ctypes
# import urllib.request
# import urllib.error
# import urllib.parse
# import ssl
# import webbrowser
# import socket
# import email.utils
 
# _LICENSE_KEY = ""

# def _has_console():
#     return sys.stdin is not None and sys.stdin.isatty()

# def _gui_input(title, prompt):
#     import tkinter as tk
#     from tkinter import simpledialog
#     root = tk.Tk()
#     root.withdraw()
#     root.attributes('-topmost', True)
#     result = simpledialog.askstring(title, prompt, parent=root)
#     root.destroy()
#     return result

# def _ask(title, prompt):
#     if _has_console():
#         print(f"\n  {prompt}")
#         try:
#             return input("  > ").strip()
#         except (EOFError, RuntimeError):
#             return _gui_input(title, prompt)
#     else:
#         return _gui_input(title, prompt)

# def _show_msg(title, message, msg_type=0):
#     if _has_console():
#         print(f"\n  {message}")
#     ctypes.windll.user32.MessageBoxW(0, message, title, msg_type)

# def _show_expired_window(error_text, button_text="Renew Subscription"):
#     import tkinter as tk
#     root = tk.Tk()
#     root.title("Shadow Lab")
#     root.geometry("480x280")
#     root.resizable(False, False)
#     root.configure(bg="#1a1a2e")
#     root.attributes('-topmost', True)
#     try:
#         root.iconify()
#         root.update()
#         root.deiconify()
#     except Exception:
#         pass
#     root.update_idletasks()
#     x = (root.winfo_screenwidth() // 2) - (480 // 2)
#     y = (root.winfo_screenheight() // 2) - (280 // 2)
#     root.geometry(f"+{x}+{y}")

#     tk.Label(root, text="Subscription Expired", font=("Segoe UI", 16, "bold"), fg="#e94560", bg="#1a1a2e").pack(pady=(20, 10))
#     tk.Label(root, text=error_text, font=("Segoe UI", 10), fg="#eaeaea", bg="#1a1a2e", wraplength=440, justify="center").pack(pady=(0, 15))

#     def _open_pricing():
#         webbrowser.open("https://shadowlab.fun/#pricing")
#         root.destroy()
#     def _close():
#         root.destroy()

#     frm = tk.Frame(root, bg="#1a1a2e")
#     frm.pack(pady=5)
#     tk.Button(frm, text=button_text, font=("Segoe UI", 10, "bold"), bg="#e94560", fg="#ffffff", bd=0, padx=20, pady=8, cursor="hand2", command=_open_pricing).pack(side="left", padx=5)
#     tk.Button(frm, text="Close", font=("Segoe UI", 10), bg="#16213e", fg="#eaeaea", bd=0, padx=20, pady=8, cursor="hand2", command=_close).pack(side="left", padx=5)
#     root.mainloop()

# if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
#     try:
#         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
#     except Exception:
#         pass

# _K1 = "366afe534167590241a4782bb5ad96aea5728e22ce1924749a48150fc4a9a5cd"
# _K2 = "3918f3f3e8d335dbff05e5d30bd93f82db2c17798034b06120012c6a5553a546"
# _ENC_INFO = b"shadow-lab:enc:v3:aes256gcm"
# _MAC_INFO = b"shadow-lab:mac:v3:hmacsha256"

# def _hkdf_extract(salt, ikm):
#     return hmac.new(salt, ikm, hashlib.sha256).digest()

# def _hkdf_expand(prk, info, length):
#     okm, t, i = b'', b'', 1
#     while len(okm) < length:
#         t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
#         okm += t
#         i += 1
#     return okm[:length]

# def _hkdf(master_key, salt, info, length):
#     prk = _hkdf_extract(salt, master_key)
#     return _hkdf_expand(prk, info, length)

# def _keystream(seed, length):
#     result, block = b'', seed
#     while len(result) < length:
#         block = hmac.new(seed, block, hashlib.sha256).digest()
#         result += block
#     return result[:length]

# def _format_time_remaining(seconds):
#     if seconds <= 0:
#         return "Expired"
#     days = seconds // 86400
#     hours = (seconds % 86400) // 3600
#     minutes = (seconds % 3600) // 60
#     parts = []
#     if days > 0:
#         parts.append(f"{days} day{'s' if days != 1 else ''}")
#     if hours > 0:
#         parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
#     if days == 0 and minutes > 0:
#         parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
#     if not parts:
#         parts.append(f"{seconds} sec{'s' if seconds != 1 else ''}")
#     return " ".join(parts) + " remaining"
 
# def _get_trusted_time(timeout=5):
#     """Get current Unix timestamp from a trusted web source."""
#     sources = [
#         ("http://worldtimeapi.org/api/ip", "json"),
#         ("http://www.google.com", "header"),
#         ("http://www.cloudflare.com", "header"),
#     ]
#     for url, method in sources:
#         try:
#             req = urllib.request.Request(
#                 url,
#                 headers={"User-Agent": "ShadowVerify/3.0"},
#                 method="HEAD" if method == "header" else "GET"
#             )
#             with urllib.request.urlopen(req, timeout=timeout) as resp:
#                 if method == "json":
#                     data = json.loads(resp.read().decode("utf-8"))
#                     return int(data["unixtime"])
#                 else:
#                     date_str = resp.headers.get('Date')
#                     if date_str:
#                         dt = email.utils.parsedate_to_datetime(date_str)
#                         return int(dt.timestamp())
#         except Exception:
#             continue
#     return None

# def _validate_system_time(max_drift=300):
#     """
#     Compare local system time with trusted network time.
#     Returns (ok: bool, drift_seconds: int or None)
#     """
#     trusted = _get_trusted_time()
#     if trusted is None: 
#         return True, None
#     local = int(time.time())
#     drift = local - trusted   
#     if abs(drift) > max_drift:
#         return False, drift
#     return True, None

# def _verify(key):
#     try:
#         K1 = bytes.fromhex(_K1)
#         K2 = bytes.fromhex(_K2)
#     except Exception:
#         return {"ok": False, "code": "E_CFG"}

#     m = re.match(r'^SHADOW-([A-Z]+)-V3-([A-Za-z0-9\-_]+)$', key.strip())
#     if not m:
#         return {"ok": False, "code": "E_FMT"}

#     b64 = m.group(2).replace('-', '+').replace('_', '/')
#     b64 += '=' * ((4 - len(b64) % 4) % 4)
#     try:
#         packed = base64.b64decode(b64)
#     except Exception:
#         return {"ok": False, "code": "E_DEC"}

#     if len(packed) < 97:
#         return {"ok": False, "code": "E_LEN"}

#     salt       = packed[0:32]
#     iv         = packed[32:48]
#     auth_tag   = packed[48:64]
#     stored_mac = packed[64:96]
#     ciphertext = packed[96:]

#     aes_key = _hkdf(K1, salt, _ENC_INFO, 32)

#     try:
#         from Crypto.Cipher import AES
#         cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
#         xored  = cipher.decrypt_and_verify(ciphertext, auth_tag)
#     except ImportError:
#         return {"ok": False, "code": "E_DEP"}
#     except ValueError:
#         return {"ok": False, "code": "E_AES"}

#     xor_seed = hmac.new(aes_key, salt + iv, hashlib.sha256).digest()
#     stream   = _keystream(xor_seed, len(xored))
#     plain    = bytes(a ^ b for a, b in zip(xored, stream))

#     if len(plain) < 1:
#         return {"ok": False, "code": "E_PAD"}

#     pad_len       = plain[0]
#     payload_bytes = plain[1 + pad_len:]

#     try:
#         data = json.loads(payload_bytes.decode("utf-8"))
#     except Exception:
#         return {"ok": False, "code": "E_JSON"}
 
#     time_ok, drift = _validate_system_time(max_drift=300)
#     if not time_ok:
#         direction = "ahead" if drift > 0 else "behind"
#         return {
#             "ok": False,
#             "code": "E_TIME",
#             "msg": (
#                 f"Your system time is incorrect.\n"
#                 f"Local time is {abs(drift)} seconds {direction} of real time.\n\n"
#                 f"Please correct your system date/time and try again."
#             )
#         }

#     now      = int(time.time())
#     exp_ts   = data.get("e", 0)
#     active   = now < exp_ts
#     diff_sec = max(0, exp_ts - now)
#     expiry_minutes = diff_sec // 60

#     return {
#         "ok": active,
#         "time_str": _format_time_remaining(diff_sec),
#         "expiry_minutes": expiry_minutes,
#         "code": "ACTIVE" if active else "EXPIRED"
#     }

# def _get_hwid():
#     raw = f"{uuid.getnode()}-{platform.node()}-{platform.machine()}"
#     return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# def _test_connection(host, port=443, timeout=5):
#     try:
#         sock = socket.create_connection((host, port), timeout=timeout)
#         sock.close()
#         return True
#     except Exception as e:
#         return str(e)
 
# class HTTP308RedirectHandler(urllib.request.HTTPRedirectHandler):
#     def http_error_308(self, req, fp, code, msg, headers):
#         newurl = headers.get('Location')
#         if not newurl:
#             return None
#         newurl = urllib.parse.urljoin(req.full_url, newurl)
#         newreq = urllib.request.Request(
#             newurl,
#             data=req.data,
#             headers=dict(req.header_items()),
#             method=req.get_method(),
#             unverifiable=True
#         )
#         for h in ('Content-Length', 'Transfer-Encoding', 'Host'):
#             newreq.headers.pop(h, None)
#         return self.parent.open(newreq, timeout=req.timeout)
#     https_error_308 = http_error_308

# def _verify_online(key, hwid):
#     import ssl
#     ctx = ssl._create_unverified_context()

#     urls = [
#         "https://shadowlab.fun/api/license/verify",
#         "https://shadowlab.fun/api/license/verify/",
#         "http://shadowlab.fun/api/license/verify",
#         "http://shadowlab.fun/api/license/verify/",
#         "http://localhost:3000/api/license/verify",
#         "http://localhost:3000/api/license/verify/",
#     ]

#     api_url = os.environ.get("SHADOW_API_URL", "").strip()
#     if api_url:
#         urls.insert(0, api_url)

#     payload = json.dumps({
#         "license_key": key.strip(),
#         "device_identifier_hash": hwid
#     }).encode("utf-8")

#     proxies = urllib.request.getproxies()
#     handlers = [
#         urllib.request.ProxyHandler(proxies),
#         urllib.request.HTTPSHandler(context=ctx),
#         HTTP308RedirectHandler()
#     ]
#     opener = urllib.request.build_opener(*handlers)

#     last_error = ""
#     connection_log = []

#     for url in urls:
#         try:
#             req = urllib.request.Request(
#                 url,
#                 data=payload,
#                 headers={
#                     "Content-Type": "application/json",
#                     "User-Agent": "ShadowVerify/3.0 (Windows NT 10.0; Win64; x64)"
#                 },
#                 method="POST"
#             )
#             with opener.open(req, timeout=10) as resp:
#                 if resp.status == 200:
#                     data = json.loads(resp.read().decode("utf-8"))
#                     if data.get("authorized"):
#                         return {
#                             "ok": True,
#                             "source": "ONLINE_DATABASE",
#                             "time_str": data.get("time_remaining", "Active"),
#                             "plan": data.get("plan_name", "Pro"),
#                             "code": "ACTIVE"
#                         }
#         except urllib.error.HTTPError as e:
#             if e.code in (400, 401, 403, 429):
#                 try:
#                     body_text = e.read().decode("utf-8", errors="ignore")
#                     err_data = json.loads(body_text)
#                     err_state = err_data.get("subscription_state", "EXPIRED")
#                     err_msg   = err_data.get("error", "Subscription Unauthorized")
#                     return {
#                         "ok": False,
#                         "source": "ONLINE_DATABASE",
#                         "code": err_state,
#                         "msg": err_msg
#                     }
#                 except Exception:
#                     pass
#             last_error = f"HTTP {e.code} on {url}"
#             connection_log.append(last_error)
#             continue
#         except urllib.error.URLError as e:
#             last_error = f"{url}: {e.reason}"
#             connection_log.append(last_error)
#             continue
#         except Exception as e:
#             last_error = f"{url}: {str(e)}"
#             connection_log.append(last_error)
#             continue

#     tcp_test = _test_connection("shadowlab.fun", 443)
#     tcp_ok = tcp_test is True

#     if not tcp_ok:
#         net_msg = (
#             f"TCP test to shadowlab.fun:443 FAILED ({tcp_test})\n\n"
#             "Your network is actively blocking the license server.\n"
#             "Try using a mobile hotspot or disable VPN."
#         )
#     else:
#         net_msg = (
#             "Server is reachable but API returned an error.\n"
#             "Please contact support with the error details below."
#         )

#     full_log = "\n".join(connection_log)
#     return {
#         "ok": False,
#         "code": "E_NET",
#         "msg": f"Could not reach license server.\n\n{net_msg}\n\nAttempt log:\n{full_log}"
#     }
 
# def _get_offline_error_msg(result):
#     code = result.get("code", "")
#     msgs = {
#         "E_CFG": "Configuration error. Contact support.",
#         "E_FMT": "Invalid license key format. Check the key and try again.",
#         "E_DEC": "Could not decode license key. Check for typos.",
#         "E_LEN": "License key data is too short. Key may be truncated.",
#         "E_DEP": "Missing dependency: pycryptodome. Install it: pip install pycryptodome",
#         "E_AES": "License key decryption failed. Key may be corrupted.",
#         "E_PAD": "Invalid padding in license data.",
#         "E_JSON": "License data is corrupted (invalid JSON).",
#         "E_TIME": result.get("msg", "Your system time is incorrect. Please correct it and try again."),
#     }
#     return msgs.get(code, f"Offline validation error: {code}")
 
# def _validate_license(key, hwid):
#     """
#     Validates license through BOTH offline (key extraction) and online (API) checks.
#     Only passes if both agree the license is ACTIVE.
#     If they disagree, shows mismatch error.
#     """ 
#     offline = _verify(key)
 
#     if offline["code"] not in ("ACTIVE", "EXPIRED"):
#         return {
#             "ok": False,
#             "code": offline["code"],
#             "msg": _get_offline_error_msg(offline),
#             "source": "OFFLINE"
#         }
 
#     online = _verify_online(key, hwid)
 
#     if online.get("code") == "E_NET":
#         return online
 
#     if not online.get("ok") and online.get("code") in ("REVOKED", "DEVICE_LOCKED"):
#         return online
 
#     offline_active = offline["ok"]
#     online_active = online.get("ok", False)
 
#     if offline_active and online_active:
#         return {
#             "ok": True,
#             "code": "ACTIVE",
#             "time_str": online.get("time_str", offline.get("time_str", "Active")),
#             "expiry_minutes": offline.get("expiry_minutes", 0),
#             "plan": online.get("plan", "Pro"),
#             "source": "DUAL_VERIFIED"
#         }
 
#     if not offline_active and not online_active:
#         return {
#             "ok": False,
#             "code": "EXPIRED",
#             "msg": "Your subscription has expired. Please renew your subscription.",
#             "time_str": offline.get("time_str", online.get("time_str", "Expired")),
#             "expiry_minutes": offline.get("expiry_minutes", 0)
#         }
 
#     off_status = "ACTIVE" if offline_active else offline.get("code", "EXPIRED")
#     on_status = "ACTIVE" if online_active else online.get("code", "FAILED")
#     return {
#         "ok": False,
#         "code": "E_MISMATCH",
#         "msg": (
#             f"License validation mismatch.\n"
#             f"Offline check: {off_status}\n"
#             f"Online check: {on_status}\n\n"
#             "License may be tampered, cloned, or server data is out of sync."
#         )
#     }

# def _error_details(result):
#     code = result.get("code", "")
#     msg  = result.get("msg", "")

#     if code == "E_NET":
#         return (msg, "Buy Subscription")
#     elif code == "E_MISMATCH":
#         return (msg, "Buy Subscription")
#     elif code == "E_TIME":
#         return (msg, "Close")
#     elif code == "REVOKED" or "REVOKED" in msg:
#         return ("This license key was revoked. Contact support.", "Buy Subscription")
#     elif code == "DEVICE_LOCKED" or "HWID_MISMATCH" in msg:
#         return ("License is bound to another PC. Reset in Dashboard.", "Buy Subscription")
#     elif code == "EXPIRED":
#         return ("Your subscription has expired. Please renew your subscription.", "Renew Subscription")
#     elif code == "E_FMT":
#         return ("Invalid license key format. Check the key and try again.", "Buy Subscription")
#     elif code == "E_SIG":
#         return ("This key has been modified. Contact support.", "Buy Subscription")
#     elif code in ("E_CFG", "E_DEC", "E_LEN", "E_DEP", "E_AES", "E_PAD", "E_JSON"):
#         return (msg or "License validation failed.", "Buy Subscription")
#     else:
#         if msg:
#             return (msg, "Buy Subscription")
#         return ("Your license is not valid or has expired. Contact support.", "Buy Subscription")

# def _find_injector():
#     if getattr(sys, 'frozen', False):
#         base = os.path.dirname(sys.executable)
#     else:
#         base = os.path.dirname(os.path.abspath(__file__))

#     candidates = [
#         os.path.join(base, "DLL_Injector", "DLL_Injector.exe"),
#         os.path.join(os.path.dirname(base), "DLL_Injector", "DLL_Injector.exe"),
#         os.path.join(base, "dll_injector", "dll_injector.exe"),
#         os.path.join(base, "DLL_Injector", "dll_injector.exe"),
#         r"C:\Users\Stranger\Desktop\ProcessHider\DLL_Injector\DLL_Injector.exe",
#     ]

#     for path in candidates:
#         if os.path.exists(path):
#             return path
#     return None

# def _launch_injector(expiry_minutes=None):
#     injector_path = _find_injector()
#     if not injector_path:
#         _show_msg("Error", "DLL_Injector.exe not found.\n\nSearched paths:\n" + "\n".join([
#             os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)), "DLL_Injector", "DLL_Injector.exe"),
#             "and 4 other locations."
#         ]), 0x10)
#         return False

#     # ═══ FIX: Build parameter string with explicit conversion ═══
#     params = ""
#     if expiry_minutes is not None and int(expiry_minutes) > 0:
#         params = str(int(expiry_minutes))
    
#     # DEBUG: Show what we're about to pass (appears before UAC prompt)
#     ctypes.windll.user32.MessageBoxW(
#         0,
#         f"About to launch:\n{injector_path}\n\nWith timer argument:\n{params} minutes",
#         "ShadowHide Launcher Debug",
#         0x40  # MB_ICONINFORMATION
#     )
    
#     # ═══ FIX: Explicit ctypes prototype so ShellExecuteW marshals correctly ═══
#     shell32 = ctypes.windll.shell32
#     ShellExecuteW = shell32.ShellExecuteW
#     ShellExecuteW.argtypes = [
#         ctypes.c_void_p,      # hwnd
#         ctypes.c_wchar_p,     # lpOperation
#         ctypes.c_wchar_p,     # lpFile
#         ctypes.c_wchar_p,     # lpParameters
#         ctypes.c_wchar_p,     # lpDirectory
#         ctypes.c_int          # nShowCmd
#     ]
#     ShellExecuteW.restype = ctypes.c_void_p

#     ret = ShellExecuteW(
#         None,                    # hwnd
#         "runas",                 # lpOperation (UAC elevate)
#         injector_path,           # lpFile
#         params if params else None,  # lpParameters
#         os.path.dirname(injector_path),  # lpDirectory
#         1                        # nShowCmd = SW_SHOWNORMAL
#     )
    
#     # ShellExecute returns HINSTANCE > 32 on success
#     if ret and ret > 32:
#         print(f"[DEBUG] ShellExecuteW succeeded (return={ret})")
#         return True
#     else:
#         err_msg = f"Failed to launch injector as Administrator.\nShellExecuteW returned: {ret}\n\nPath: {injector_path}\nParams: {params}"
#         print(f"[DEBUG] {err_msg}")
#         _show_msg("Launch Error", err_msg, 0x10)
#         return False

# def main():
#     if _LICENSE_KEY and _LICENSE_KEY.strip():
#         key = _LICENSE_KEY.strip()
#     elif len(sys.argv) > 1:
#         key = " ".join(sys.argv[1:]).strip()
#     else:
#         key = _ask("License Key", "Enter your license key:")

#     if not key:
#         _show_msg("Error", "No license key entered.", 0x10)
#         sys.exit(1)

#     hwid = _get_hwid()
 
#     result = _validate_license(key, hwid)

#     if not result.get("ok"):
#         error_text, button_text = _error_details(result)
#         _show_expired_window(error_text, button_text)
#         sys.exit(1)

#     expiry_minutes = result.get("expiry_minutes", 0)
    
#     # ═══ DEBUG: Show what the license calculated ═══
#     print(f"[DEBUG] License valid. Time remaining: {result.get('time_str', 'Unknown')}")
#     print(f"[DEBUG] Passing expiry_minutes to injector: {expiry_minutes}")
    
#     _launch_injector(expiry_minutes)
#     sys.exit(0)

# if __name__ == "__main__":
#     main()





















import sys
import re
import hmac
import json
import time
import base64
import hashlib
import io
import os
import uuid
import platform
import ctypes
import urllib.request
import urllib.error
import urllib.parse
import ssl
import webbrowser
import socket
import email.utils
import tempfile
import winreg

_LICENSE_KEY = ""

def _has_console():
    return sys.stdin is not None and sys.stdin.isatty()

def _gui_input(title, prompt):
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    result = simpledialog.askstring(title, prompt, parent=root)
    root.destroy()
    return result

def _ask(title, prompt):
    if _has_console():
        print(f"\n  {prompt}")
        try:
            return input("  > ").strip()
        except (EOFError, RuntimeError):
            return _gui_input(title, prompt)
    else:
        return _gui_input(title, prompt)

def _show_msg(title, message, msg_type=0):
    if _has_console():
        print(f"\n  {message}")
    ctypes.windll.user32.MessageBoxW(0, message, title, msg_type)

def _show_expired_window(error_text, button_text="Renew Subscription"):
    import tkinter as tk
    root = tk.Tk()
    root.title("Shadow Lab")
    root.geometry("480x280")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")
    root.attributes('-topmost', True)
    try:
        root.iconify()
        root.update()
        root.deiconify()
    except Exception:
        pass
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (480 // 2)
    y = (root.winfo_screenheight() // 2) - (280 // 2)
    root.geometry(f"+{x}+{y}")

    tk.Label(root, text="Subscription Expired", font=("Segoe UI", 16, "bold"), fg="#e94560", bg="#1a1a2e").pack(pady=(20, 10))
    tk.Label(root, text=error_text, font=("Segoe UI", 10), fg="#eaeaea", bg="#1a1a2e", wraplength=440, justify="center").pack(pady=(0, 15))

    def _open_pricing():
        webbrowser.open("https://shadowlab.fun/#pricing")
        root.destroy()
    def _close():
        root.destroy()

    frm = tk.Frame(root, bg="#1a1a2e")
    frm.pack(pady=5)
    tk.Button(frm, text=button_text, font=("Segoe UI", 10, "bold"), bg="#e94560", fg="#ffffff", bd=0, padx=20, pady=8, cursor="hand2", command=_open_pricing).pack(side="left", padx=5)
    tk.Button(frm, text="Close", font=("Segoe UI", 10), bg="#16213e", fg="#eaeaea", bd=0, padx=20, pady=8, cursor="hand2", command=_close).pack(side="left", padx=5)
    root.mainloop()

if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

_K1 = "366afe534167590241a4782bb5ad96aea5728e22ce1924749a48150fc4a9a5cd"
_K2 = "3918f3f3e8d335dbff05e5d30bd93f82db2c17798034b06120012c6a5553a546"
_ENC_INFO = b"shadow-lab:enc:v3:aes256gcm"
_MAC_INFO = b"shadow-lab:mac:v3:hmacsha256"

def _hkdf_extract(salt, ikm):
    return hmac.new(salt, ikm, hashlib.sha256).digest()

def _hkdf_expand(prk, info, length):
    okm, t, i = b'', b'', 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        okm += t
        i += 1
    return okm[:length]

def _hkdf(master_key, salt, info, length):
    prk = _hkdf_extract(salt, master_key)
    return _hkdf_expand(prk, info, length)

def _keystream(seed, length):
    result, block = b'', seed
    while len(result) < length:
        block = hmac.new(seed, block, hashlib.sha256).digest()
        result += block
    return result[:length]

def _format_time_remaining(seconds):
    if seconds <= 0:
        return "Expired"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if days == 0 and minutes > 0:
        parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
    if not parts:
        parts.append(f"{seconds} sec{'s' if seconds != 1 else ''}")
    return " ".join(parts) + " remaining"

def _get_trusted_time(timeout=5):
    sources = [
        ("http://worldtimeapi.org/api/ip", "json"),
        ("http://www.google.com", "header"),
        ("http://www.cloudflare.com", "header"),
    ]
    for url, method in sources:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "ShadowVerify/3.0"},
                method="HEAD" if method == "header" else "GET"
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if method == "json":
                    data = json.loads(resp.read().decode("utf-8"))
                    return int(data["unixtime"])
                else:
                    date_str = resp.headers.get('Date')
                    if date_str:
                        dt = email.utils.parsedate_to_datetime(date_str)
                        return int(dt.timestamp())
        except Exception:
            continue
    return None

def _validate_system_time(max_drift=300):
    trusted = _get_trusted_time()
    if trusted is None:
        return True, None
    local = int(time.time())
    drift = local - trusted
    if abs(drift) > max_drift:
        return False, drift
    return True, None

def _verify(key):
    try:
        K1 = bytes.fromhex(_K1)
        K2 = bytes.fromhex(_K2)
    except Exception:
        return {"ok": False, "code": "E_CFG"}

    m = re.match(r'^SHADOW-([A-Z]+)-V3-([A-Za-z0-9\-_]+)$', key.strip())
    if not m:
        return {"ok": False, "code": "E_FMT"}

    b64 = m.group(2).replace('-', '+').replace('_', '/')
    b64 += '=' * ((4 - len(b64) % 4) % 4)
    try:
        packed = base64.b64decode(b64)
    except Exception:
        return {"ok": False, "code": "E_DEC"}

    if len(packed) < 97:
        return {"ok": False, "code": "E_LEN"}

    salt       = packed[0:32]
    iv         = packed[32:48]
    auth_tag   = packed[48:64]
    stored_mac = packed[64:96]
    ciphertext = packed[96:]

    aes_key = _hkdf(K1, salt, _ENC_INFO, 32)

    try:
        from Crypto.Cipher import AES
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
        xored  = cipher.decrypt_and_verify(ciphertext, auth_tag)
    except ImportError:
        return {"ok": False, "code": "E_DEP"}
    except ValueError:
        return {"ok": False, "code": "E_AES"}

    xor_seed = hmac.new(aes_key, salt + iv, hashlib.sha256).digest()
    stream   = _keystream(xor_seed, len(xored))
    plain    = bytes(a ^ b for a, b in zip(xored, stream))

    if len(plain) < 1:
        return {"ok": False, "code": "E_PAD"}

    pad_len       = plain[0]
    payload_bytes = plain[1 + pad_len:]

    try:
        data = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        return {"ok": False, "code": "E_JSON"}

    time_ok, drift = _validate_system_time(max_drift=300)
    if not time_ok:
        direction = "ahead" if drift > 0 else "behind"
        return {
            "ok": False,
            "code": "E_TIME",
            "msg": (
                f"Your system time is incorrect.\n"
                f"Local time is {abs(drift)} seconds {direction} of real time.\n\n"
                f"Please correct your system date/time and try again."
            )
        }

    now      = int(time.time())
    exp_ts   = data.get("e", 0)
    active   = now < exp_ts
    diff_sec = max(0, exp_ts - now)
    expiry_minutes = max(1, diff_sec // 60) if diff_sec > 0 else 0

    return {
        "ok": active,
        "time_str": _format_time_remaining(diff_sec),
        "expiry_minutes": expiry_minutes,
        "code": "ACTIVE" if active else "EXPIRED"
    }

def _get_hwid():
    raw = f"{uuid.getnode()}-{platform.node()}-{platform.machine()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def _test_connection(host, port=443, timeout=5):
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except Exception as e:
        return str(e)

class HTTP308RedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_308(self, req, fp, code, msg, headers):
        newurl = headers.get('Location')
        if not newurl:
            return None
        newurl = urllib.parse.urljoin(req.full_url, newurl)
        newreq = urllib.request.Request(
            newurl,
            data=req.data,
            headers=dict(req.header_items()),
            method=req.get_method(),
            unverifiable=True
        )
        for h in ('Content-Length', 'Transfer-Encoding', 'Host'):
            newreq.headers.pop(h, None)
        return self.parent.open(newreq, timeout=req.timeout)
    https_error_308 = http_error_308

def _verify_online(key, hwid):
    import ssl
    ctx = ssl._create_unverified_context()

    urls = [
        "https://shadowlab.fun/api/license/verify",
        "https://shadowlab.fun/api/license/verify/",
        "http://shadowlab.fun/api/license/verify",
        "http://shadowlab.fun/api/license/verify/",
        "http://localhost:3000/api/license/verify",
        "http://localhost:3000/api/license/verify/",
    ]

    api_url = os.environ.get("SHADOW_API_URL", "").strip()
    if api_url:
        urls.insert(0, api_url)

    payload = json.dumps({
        "license_key": key.strip(),
        "device_identifier_hash": hwid
    }).encode("utf-8")

    proxies = urllib.request.getproxies()
    handlers = [
        urllib.request.ProxyHandler(proxies),
        urllib.request.HTTPSHandler(context=ctx),
        HTTP308RedirectHandler()
    ]
    opener = urllib.request.build_opener(*handlers)

    last_error = ""
    connection_log = []

    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "ShadowVerify/3.0 (Windows NT 10.0; Win64; x64)"
                },
                method="POST"
            )
            with opener.open(req, timeout=10) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    if data.get("authorized"):
                        return {
                            "ok": True,
                            "source": "ONLINE_DATABASE",
                            "time_str": data.get("time_remaining", "Active"),
                            "plan": data.get("plan_name", "Pro"),
                            "code": "ACTIVE"
                        }
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403, 429):
                try:
                    body_text = e.read().decode("utf-8", errors="ignore")
                    err_data = json.loads(body_text)
                    err_state = err_data.get("subscription_state", "EXPIRED")
                    err_msg   = err_data.get("error", "Subscription Unauthorized")
                    return {
                        "ok": False,
                        "source": "ONLINE_DATABASE",
                        "code": err_state,
                        "msg": err_msg
                    }
                except Exception:
                    pass
            last_error = f"HTTP {e.code} on {url}"
            connection_log.append(last_error)
            continue
        except urllib.error.URLError as e:
            last_error = f"{url}: {e.reason}"
            connection_log.append(last_error)
            continue
        except Exception as e:
            last_error = f"{url}: {str(e)}"
            connection_log.append(last_error)
            continue

    tcp_test = _test_connection("shadowlab.fun", 443)
    tcp_ok = tcp_test is True

    if not tcp_ok:
        net_msg = (
            f"TCP test to shadowlab.fun:443 FAILED ({tcp_test})\n\n"
            "Your network is actively blocking the license server.\n"
            "Try using a mobile hotspot or disable VPN."
        )
    else:
        net_msg = (
            "Server is reachable but API returned an error.\n"
            "Please contact support with the error details below."
        )

    full_log = "\n".join(connection_log)
    return {
        "ok": False,
        "code": "E_NET",
        "msg": f"Could not reach license server.\n\n{net_msg}\n\nAttempt log:\n{full_log}"
    }

def _get_offline_error_msg(result):
    code = result.get("code", "")
    msgs = {
        "E_CFG": "Configuration error. Contact support.",
        "E_FMT": "Invalid license key format. Check the key and try again.",
        "E_DEC": "Could not decode license key. Check for typos.",
        "E_LEN": "License key data is too short. Key may be truncated.",
        "E_DEP": "Missing dependency: pycryptodome. Install it: pip install pycryptodome",
        "E_AES": "License key decryption failed. Key may be corrupted.",
        "E_PAD": "Invalid padding in license data.",
        "E_JSON": "License data is corrupted (invalid JSON).",
        "E_TIME": result.get("msg", "Your system time is incorrect. Please correct it and try again."),
    }
    return msgs.get(code, f"Offline validation error: {code}")

def _validate_license(key, hwid):
    offline = _verify(key)

    if offline["code"] not in ("ACTIVE", "EXPIRED"):
        return {
            "ok": False,
            "code": offline["code"],
            "msg": _get_offline_error_msg(offline),
            "source": "OFFLINE"
        }

    online = _verify_online(key, hwid)

    if online.get("code") == "E_NET":
        return online

    if not online.get("ok") and online.get("code") in ("REVOKED", "DEVICE_LOCKED"):
        return online

    offline_active = offline["ok"]
    online_active = online.get("ok", False)

    if offline_active and online_active:
        return {
            "ok": True,
            "code": "ACTIVE",
            "time_str": online.get("time_str", offline.get("time_str", "Active")),
            "expiry_minutes": offline.get("expiry_minutes", 0),
            "plan": online.get("plan", "Pro"),
            "source": "DUAL_VERIFIED"
        }

    if not offline_active and not online_active:
        return {
            "ok": False,
            "code": "EXPIRED",
            "msg": "Your subscription has expired. Please renew your subscription.",
            "time_str": offline.get("time_str", online.get("time_str", "Expired")),
            "expiry_minutes": offline.get("expiry_minutes", 0)
        }

    off_status = "ACTIVE" if offline_active else offline.get("code", "EXPIRED")
    on_status = "ACTIVE" if online_active else online.get("code", "FAILED")
    return {
        "ok": False,
        "code": "E_MISMATCH",
        "msg": (
            f"License validation mismatch.\n"
            f"Offline check: {off_status}\n"
            f"Online check: {on_status}\n\n"
            "License may be tampered, cloned, or server data is out of sync."
        )
    }

def _error_details(result):
    code = result.get("code", "")
    msg  = result.get("msg", "")

    if code == "E_NET":
        return (msg, "Buy Subscription")
    elif code == "E_MISMATCH":
        return (msg, "Buy Subscription")
    elif code == "E_TIME":
        return (msg, "Close")
    elif code == "REVOKED" or "REVOKED" in msg:
        return ("This license key was revoked. Contact support.", "Buy Subscription")
    elif code == "DEVICE_LOCKED" or "HWID_MISMATCH" in msg:
        return ("License is bound to another PC. Reset in Dashboard.", "Buy Subscription")
    elif code == "EXPIRED":
        return ("Your subscription has expired. Please renew your subscription.", "Renew Subscription")
    elif code == "E_FMT":
        return ("Invalid license key format. Check the key and try again.", "Buy Subscription")
    elif code == "E_SIG":
        return ("This key has been modified. Contact support.", "Buy Subscription")
    elif code in ("E_CFG", "E_DEC", "E_LEN", "E_DEP", "E_AES", "E_PAD", "E_JSON"):
        return (msg or "License validation failed.", "Buy Subscription")
    else:
        if msg:
            return (msg, "Buy Subscription")
        return ("Your license is not valid or has expired. Contact support.", "Buy Subscription")

def _find_injector():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

        # Path where the PowerShell install script downloads & extracts files
    temp_base = os.path.join(os.environ.get('TEMP', ''), 'safeit_tmp')

    candidates = [
        # ─── Same-folder / sibling-folder (standard install) ───
        os.path.join(base, "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(os.path.dirname(base), "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(base, "dll_injector", "dll_injector.exe"),
        os.path.join(base, "DLL_Injector", "dll_injector.exe"),

        # ─── PowerShell script download location (TEMP\safeit_tmp) ───
        os.path.join(temp_base, "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "DLL_Injector", "dll_injector.exe"),
        os.path.join(temp_base, "dll_injector", "dll_injector.exe"),

        # ─── If zip extracts into a subfolder (common patterns) ───
        os.path.join(temp_base, "shadowhide4-main", "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "shadowhide4-main", "DLL_Injector", "dll_injector.exe"),
        os.path.join(temp_base, "shadowhide2-main", "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "shadowhide2-main", "DLL_Injector", "dll_injector.exe"),
        os.path.join(temp_base, "shadowhide-main", "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "shadowhide-main", "DLL_Injector", "dll_injector.exe"),
        os.path.join(temp_base, "shadowhide2", "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "shadowhide2", "DLL_Injector", "dll_injector.exe"),
        os.path.join(temp_base, "shadowhide", "DLL_Injector", "DLL_Injector.exe"),
        os.path.join(temp_base, "shadowhide", "DLL_Injector", "dll_injector.exe"),

        # ─── Manual / legacy fallback ───
        r"C:\Users\Stranger\Desktop\shadowhide2\DLL_Injector\DLL_Injector.exe",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    if os.path.isdir(temp_base):
        for root, dirs, files in os.walk(temp_base):
            for file in files:
                if file.lower() == "dll_injector.exe":
                    return os.path.join(root, file)

    return None

# ═══ FIX: Debug log so we can see what Python actually did (console may be hidden) ═══
def _debug_log(msg):
    try:
        log_path = os.path.join(tempfile.gettempdir(), "shadowlauncher_debug.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass

def _launch_injector(expiry_minutes=None):
    injector_path = _find_injector()
    if not injector_path:
        _show_msg("Error", "DLL_Injector.exe not found.", 0x10)
        return False

    timer_val = int(expiry_minutes) if expiry_minutes is not None else 0
    if timer_val <= 0:
        _show_msg("Error", f"Invalid timer value: {timer_val}. License may be expired.", 0x10)
        return False

    _debug_log(f"=== LAUNCH START === expiry_minutes={timer_val}, injector={injector_path}")

    # 1) Write registry (both views)
    views = [
        ("64-bit", winreg.KEY_WOW64_64KEY),
        ("32-bit", winreg.KEY_WOW64_32KEY),
    ]
    for view_name, view_flag in views:
        try:
            access = winreg.KEY_WRITE | view_flag
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\ShadowHide", 0, access)
            winreg.SetValueEx(key, "TimerMinutes", 0, winreg.REG_DWORD, timer_val)
            winreg.CloseKey(key)
            _debug_log(f"Registry OK ({view_name}): TimerMinutes={timer_val}")
        except Exception as e:
            _debug_log(f"Registry FAIL ({view_name}): {e}")

    # 2) Write timer file next to injector
    injector_dir = os.path.dirname(injector_path)
    timer_file = os.path.join(injector_dir, "shadowhide_timer.cfg")
    ready_file = os.path.join(injector_dir, "shadowhide_timer.ready")
    try:
        if os.path.exists(ready_file):
            os.remove(ready_file)
        with open(timer_file, "w") as f:
            f.write(str(timer_val))
            f.flush()
            os.fsync(f.fileno())
        _debug_log(f"Timer file written: {timer_file} = {timer_val}")
    except Exception as e:
        _debug_log(f"Timer file FAILED: {e}")

    # 3) CRITICAL: Wait for filesystem to commit before launching
    time.sleep(1.0)

    # 4) Write ready sentinel so C++ knows we're done writing
    try:
        with open(ready_file, "w") as f:
            f.write("1")
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        _debug_log(f"Ready file FAILED: {e}")

    params = str(timer_val)

    # DEBUG: Show what we're about to do
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Launching:\n{injector_path}\n\nTimer: {params} min\n\nIf C++ shows 'Timer=0' error, the parameter was dropped by UAC.",
        "ShadowHide Launcher Debug",
        0x40
    )

    # 5) ShellExecuteExW with runas
    shell32 = ctypes.windll.shell32
    kernel32 = ctypes.windll.kernel32
    SEE_MASK_NOCLOSEPROCESS = 0x00000040
    SEE_MASK_NO_CONSOLE = 0x00008000

    class SHELLEXECUTEINFOW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_uint32),
            ("fMask", ctypes.c_uint32),
            ("hwnd", ctypes.c_void_p),
            ("lpVerb", ctypes.c_wchar_p),
            ("lpFile", ctypes.c_wchar_p),
            ("lpParameters", ctypes.c_wchar_p),
            ("lpDirectory", ctypes.c_wchar_p),
            ("nShow", ctypes.c_int),
            ("hInstApp", ctypes.c_void_p),
            ("lpIDList", ctypes.c_void_p),
            ("lpClass", ctypes.c_wchar_p),
            ("hkeyClass", ctypes.c_void_p),
            ("dwHotKey", ctypes.c_uint32),
            ("hIconOrMonitor", ctypes.c_void_p),
            ("hProcess", ctypes.c_void_p),
        ]

    sei = SHELLEXECUTEINFOW()
    sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFOW)
    sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE
    sei.hwnd = None
    sei.lpVerb = "runas"
    sei.lpFile = injector_path
    sei.lpParameters = params
    sei.lpDirectory = injector_dir
    sei.nShow = 1  # SW_SHOWNORMAL

    _debug_log(f"ShellExecuteExW: lpFile={injector_path}, lpParameters={params}")

    ret = shell32.ShellExecuteExW(ctypes.byref(sei))

    if not ret:
        err = kernel32.GetLastError()
        err_msg = f"ShellExecuteExW failed. LastError: {err}"
        _debug_log(err_msg)
        _show_msg("Launch Error", err_msg, 0x10)
        return False

    _debug_log(f"ShellExecuteExW OK, hProcess={sei.hProcess}")

    # 6) Wait up to 5 seconds for C++ to consume the .cfg file
    # NOTE: The file is only deleted when C++ self-kills (after timer expires).
    # So we check if the process is still alive instead of checking file deletion.
    if sei.hProcess:
        wait_result = kernel32.WaitForSingleObject(sei.hProcess, 5000)
        if wait_result == 0:  # WAIT_OBJECT_0 — process already exited
            _debug_log("WARNING: C++ process exited immediately (crashed or failed to start).")
        else:
            # Process is still running — this is expected for a multi-minute timer
            _debug_log("INFO: C++ process is running. Kill-switch will fire when timer expires.")
        kernel32.CloseHandle(sei.hProcess)

    return True

def main():
    if _LICENSE_KEY and _LICENSE_KEY.strip():
        key = _LICENSE_KEY.strip()
    elif len(sys.argv) > 1:
        key = " ".join(sys.argv[1:]).strip()
    else:
        key = _ask("License Key", "Enter your license key:")

    if not key:
        _show_msg("Error", "No license key entered.", 0x10)
        sys.exit(1)

    hwid = _get_hwid()

    result = _validate_license(key, hwid)

    if not result.get("ok"):
        error_text, button_text = _error_details(result)
        _show_expired_window(error_text, button_text)
        sys.exit(1)

    expiry_minutes = result.get("expiry_minutes", 0)

    _debug_log(f"License valid. expiry_minutes={expiry_minutes}")

    ok = _launch_injector(expiry_minutes)
    if not ok:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()