import sys
if sys.version_info < (3, 12):
    raise ImportError("PyGuard requires CPython 3.12 or newer")

import ast
import ctypes
import os
import threading
import time
from base64 import b64decode
from hashlib import sha512
from os import path
from string import hexdigits
from typing import override
from zlib import decompress

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from Crypto.Cipher import ChaCha20_Poly1305

__all__ = ["PyGuard", "_"] #the names that a from module import * statement exposes. Restricting it to PyGuard and _

_ = exec

_integrityEnabledSECRET: bool = True    # BUILD INJECTION POINT
_base64EnabledSECRET: bool = True       # BUILD INJECTION POINT
_chachaEnabledSECRET: bool = True       # BUILD INJECTION POINT
_aesEnabledSECRET: bool = True         # BUILD INJECTION POINT
_fernetEnabledSECRET: bool = True      # BUILD INJECTION POINT

_filehashmanifestSECRET: dict[str, str] = {}   # relpath -> sha512 hex
_literalmanifestSECRET: dict[str, bytes] = {}  # sha512 hex -> zlib literal
_recursiveIterationsSECRET: int = 0

# Per-build decoy source: inert, and ideally indistinguishable from a plausible early exit of the protected program.
_DECOY_SOURCE_SECRET = "\n"
_DECOY_FIRED_SECRET = False

# Behaviour switches
_DEBUG_ERROR_SECRET = False
_DEBUG_BUILD_SECRET = False
_MAX_INIT_SECONDS_SECRET = 10.0
_MAX_EXEC_SECONDS_SECRET = 30.0

_BANNED_MODULES_SECRET = frozenset({
    "pdb", "ipdb", "pudb", "coverage", "trace",
})
_BANNED_ENV_EXACT_SECRET = frozenset({
    "PYTHONINSPECT", "PYTHONTRACEMALLOC", "PYTHONPROFILEIMPORTTIME",
    "PYCHARM_DEBUG",
})
_BANNED_ENV_PREFIX_SECRET = frozenset({"PYDEVD_", "DEBUGPY_"})
_OPAQUE_SECRET = frozenset({
    "__dict__", "__slots__", "__weakref__", "__doc__", "__module__",
    "__qualname__", "__init_subclass__",
})

def _EnvironmentIsCleanSECRET() -> bool:
    """Fail-closed anti-analysis scan. Any exception means 'not clean'."""

    if _DEBUG_BUILD_SECRET: return True

    try:
        if sys.gettrace() is not None or sys.getprofile() is not None:
            return False
        if threading.gettrace() is not None:
            return False
        # PEP 669: debuggers, coverage tools and profilers register a named tool slot here
        for _tid in {
            getattr(sys.monitoring, "DEBUGGER_ID", 0), #official constants
            getattr(sys.monitoring, "COVERAGE_ID", 1),
            getattr(sys.monitoring, "PROFILER_ID", 2),
            getattr(sys.monitoring, "OPTIMIZER_ID", 5),
            0, 1, 2, 3,}: #fall back if a future Python version renames or removes them
            try:
                if sys.monitoring.get_tool(_tid) is not None:
                    return False
            except ValueError:
                continue
        _mods = sys.modules
        for _m in _BANNED_MODULES_SECRET:
            if _m in _mods:
                return False
        for _m in tuple(_mods):
            _ml = _m.lower()
            if "pydev" in _ml or "debugpy" in _ml or "ptvsd" in _ml:
                return False
        for _k in _BANNED_ENV_EXACT_SECRET:
            if os.environ.get(_k):
                return False
        for _k in os.environ:
            for _p in _BANNED_ENV_PREFIX_SECRET:
                if _k.startswith(_p):
                    return False
        return True
    except Exception:
        return False

def _DecoyCodeSECRET():
    global _DECOY_FIRED_SECRET
    if _DECOY_FIRED_SECRET:
        return compile("", "<string>", "exec")

    _DECOY_FIRED_SECRET = True
    try:
        return compile(_DECOY_SOURCE_SECRET, "<string>", "exec")
    except Exception:
        return compile("print(\"dome generic python error\")", "<string>", "exec")

def _WipeSECRET(buf) -> None:
    """Zero a mutable buffer with memset, then truncate it."""
    if not isinstance(buf, bytearray) or not buf:
        return
    try:
        _c = ctypes.c_char.from_buffer(buf)
        try:
            ctypes.memset(ctypes.addressof(_c), 0, len(buf))
        finally:
            del _c  # release the buffer export before resizing
    except Exception:
        pass
    try:
        del buf[:]
    except Exception:
        for _i in range(len(buf)):
            buf[_i] = 0


def _ReverseSECRET(buf: bytearray) -> bytearray:
    _out = bytearray(buf[::-1])
    _WipeSECRET(buf)
    return _out


class _DehasherSECRET(ast.NodeTransformer):
    def __init__(self) -> None:
        self.__literalmanifestSECRET: dict[str, bytes] = _literalmanifestSECRET

    @override
    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        _value = node.value
        if (isinstance(_value, str)
                and len(_value) == 128
                and set(_value) <= set(hexdigits.lower())
                and _value in self.__literalmanifestSECRET):
            node.value = decompress(self.__literalmanifestSECRET[_value]).decode("utf-8")
        return node


def _ForgeSECRET():
    _wipe = _WipeSECRET
    # Frame-independent slot access. Internal code touches the one instance slot through the C-level type functions
    _objget = object.__getattribute__
    _objset = object.__setattr__
    # Per-instance vault: random token -> encrypted payload (the same ciphertext the launcher file already contains on disk). Each obfuscated file constructs its own instance, so payloads never share a cell.
    # Nothing decryptable is stored: the whole pipeline runs at property-call time, and its buffers are wiped stage by stage. The decrypted code object exists only for the microsecond
    _vaults: dict = {}

    def _CheckFileIntegritySECRET(filepath: str) -> None:
        if not _filehashmanifestSECRET:
            raise RuntimeError("integrity manifest is empty - build injection failed")
        _rel = path.relpath(filepath, path.dirname(__file__))
        _expected = _filehashmanifestSECRET.get(_rel)
        if _expected is None:
            raise RuntimeError("integrity manifest has no entry for " + _rel)
        with open(filepath, "rb") as _f:
            _actual = sha512(_f.read()).hexdigest()
        if _actual != _expected:
            raise RuntimeError("integrity check failed for " + _rel)

    def _Base64SECRET(buf: bytearray) -> bytearray:
        _out = bytearray(b64decode(decompress(buf)))
        _wipe(buf)
        return _out

    def _RecursiveSECRET(buf: bytearray) -> bytearray:
        for _ in range(_recursiveIterationsSECRET):
            _n = bytearray(decompress(buf))
            _wipe(buf)
            buf = _n
            buf = _ReverseSECRET(buf)
            _n = bytearray(b64decode(buf))
            _wipe(buf)
            buf = _n
        return buf

    def _ChaChaSECRET(buf: bytearray) -> bytearray:
        __chachaKeySECRET = b""  # BUILD INJECTION POINT
        _raw = bytearray(b64decode(decompress(buf)))
        _wipe(buf)
        if len(_raw) < 24 + 16:
            raise ValueError("layer failure")
        _nonce = bytes(_raw[:24])
        _mac = bytes(_raw[-16:])
        _ct = bytes(_raw[24:-16])
        _wipe(_raw)
        return bytearray(ChaCha20_Poly1305.new(key=__chachaKeySECRET, nonce=_nonce).decrypt_and_verify(_ct, _mac))

    def _AesSECRET(buf: bytearray) -> bytearray:
        __aesKeySECRET = b""  # BUILD INJECTION POINT
        _raw = bytearray(b64decode(decompress(buf)))
        _wipe(buf)
        if len(_raw) < 12:
            raise ValueError("layer failure")
        _aead = AESGCMSIV(__aesKeySECRET)
        _nonce = bytes(_raw[:12])
        _ct = bytes(_raw[12:])
        _wipe(_raw)
        return bytearray(_aead.decrypt(_nonce, _ct, None))

    def _FernetSECRET(buf: bytearray) -> bytearray:
        __fernetKeySECRET = b""  # BUILD INJECTION POINT
        _raw = bytearray(decompress(buf))
        _wipe(buf)
        _out = bytearray(Fernet(__fernetKeySECRET).decrypt(bytes(_raw)))
        _wipe(_raw)
        return _out

    def _FinalizeSECRET(src: bytearray):
        _tree = ast.parse(bytes(src))
        _wipe(src)
        _tree = _DehasherSECRET().visit(_tree)
        ast.fix_missing_locations(_tree)
        _code = compile(_tree, "<string>", "exec")
        del _tree
        return _code

    def _DecryptSECRET(buf: bytearray):
        # Stage order is the exact inverse of MainObfuscation.Obfuscate.
        _b = buf
        if _base64EnabledSECRET:
            _b = _Base64SECRET(_b)
        _b = _ReverseSECRET(_b)
        if _recursiveIterationsSECRET:
            _b = _RecursiveSECRET(_b)
        if _chachaEnabledSECRET:
            _b = _ChaChaSECRET(_b)
        if _aesEnabledSECRET:
            _b = _AesSECRET(_b)
        if _fernetEnabledSECRET:
            _b = _FernetSECRET(_b)
        if _base64EnabledSECRET:
            _b = _Base64SECRET(_b)
        _b = _ReverseSECRET(_b)
        _src = bytearray(decompress(_b))
        _wipe(_b)
        return _FinalizeSECRET(_src)

    # Each PyGuard() instance draws 32 cryptographically secure random bytes (os.urandom) as its token. The token is stored in the instance's single mangled slot and serves as the key into the closure-local _vaults dict, which holds the encrypted payload.
    # The token is not a layer key; it is an unguessable per-instance reference that enforces one-shot execution semantics.
    class PyGuard:
        __slots__ = ("_PyGuard__token",) # The instance has exactly one attribute slot. This closes the common introspection route of dumping
        __module__ = "builtins"
        __qualname__ = "PyGuard"

        def __init__(self, enccode: bytes, filepath: str) -> None:
            _t0 = time.monotonic()
            _objset(self, "_PyGuard__token", os.urandom(32)) #generates the per-instance token and writes it into the single slot
            if not _EnvironmentIsCleanSECRET():
                # Silent inert decoy: no error, no plaintext, no signal. The vault entry stays absent, so the property decoys too.
                return
            try:
                if _integrityEnabledSECRET:
                    _CheckFileIntegritySECRET(filepath)
                # Encrypted form only. No decryption happens here: a dump of the running process fails
                _vaults[_objget(self, "_PyGuard__token")] = bytearray(enccode)
            except Exception as _err:
                _wipe(_vaults.pop(_objget(self, "_PyGuard__token"), None))
                if _DEBUG_ERROR_SECRET:
                    print("runtime error: " + repr(_err), file=sys.stderr, flush=True)
                else:
                    print("runtime error", file=sys.stderr, flush=True)
                sys.exit(1)
            if time.monotonic() - _t0 > _MAX_INIT_SECONDS_SECRET:
                # Single-stepped through the integrity read: defuse the vault.
                _wipe(_vaults.pop(_objget(self, "_PyGuard__token"), None))

        @property
        def _(self):
            _tok = _objget(self, "_PyGuard__token")
            if not _EnvironmentIsCleanSECRET():
                _wipe(_vaults.pop(_tok, None))
                return _DecoyCodeSECRET()
            _blob = _vaults.pop(_tok, None)
            if not isinstance(_blob, bytearray) or not _blob:
                return _DecoyCodeSECRET()
            # The whole pipeline runs here and only here, immediately before he launcher's exec
            _t0 = time.monotonic()
            try:
                _code = _DecryptSECRET(_blob)
            except Exception as _err:
                _wipe(_blob)
                if _DEBUG_ERROR_SECRET:
                    print("runtime error: " + repr(_err), file=sys.stderr, flush=True)
                # Fail closed and silently: a tampered or mismatched blob yields the inert decoy, not an error signal.
                return _DecoyCodeSECRET()
            if time.monotonic() - _t0 > _MAX_EXEC_SECONDS_SECRET:
                # Single-stepped through the pipeline: hand out the decoy.
                return _DecoyCodeSECRET()
            return _code

        def __del__(self) -> None:
            # Hygiene for instances that are never executed.
            try:
                _wipe(_vaults.pop(_objget(self, "_PyGuard__token"), None))
            except Exception:
                pass

        # The guards deny unconditionally; internal code never routes through them (it uses the object-level slot functions bound above).
        def __getattribute__(self, name: str):
            if name in _OPAQUE_SECRET or name.startswith("_PyGuard__"):
                raise AttributeError(name)
            return object.__getattribute__(self, name)

        def __setattr__(self, name: str, value):
            if name.startswith("_PyGuard__"):
                raise AttributeError(name)
            object.__setattr__(self, name, value)

        def __delattr__(self, name: str):
            if name.startswith("_PyGuard__"):
                raise AttributeError(name)
            object.__delattr__(self, name)

        def __dir__(self) -> list[str]:
            return []

        def __repr__(self) -> str:
            return "<built-in object>"

        __str__ = __repr__

        def __copy__(self):
            raise TypeError("cannot be copied")

        def __deepcopy__(self, memo):
            raise TypeError("cannot be copied")

        def __reduce__(self):
            raise TypeError("cannot be pickled")

        def __reduce_ex__(self, protocol):
            raise TypeError("cannot be pickled")

        def __init_subclass__(cls, **kwargs):
            raise TypeError("cannot be subclassed")

    return PyGuard


PyGuard = _ForgeSECRET()
