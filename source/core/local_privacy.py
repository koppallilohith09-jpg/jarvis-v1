"""Local adaptation: AI providers stay on this PC; fail closed on errors.

This is an application policy, not an OS sandbox for hostile native extensions.
Model/dependency downloads are a separate explicit setup operation.
"""
import ipaddress
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from urllib.parse import urlsplit

_installed=False
_openai_request=ContextVar('jarvis_openai_request',default=False)

@contextmanager
def gemini_access():
    token=_openai_request.set('generativelanguage.googleapis.com')
    try:yield
    finally:_openai_request.reset(token)

@contextmanager
def openai_access():
    """Narrow request scope; ordinary tools retain the local-only policy."""
    token=_openai_request.set(True)
    try:yield
    finally:_openai_request.reset(token)

def require_loopback_url(value):
    parsed=urlsplit(value if '://' in value else 'http://'+value)
    if parsed.scheme not in ('http','https') or parsed.username or parsed.password:
        raise ValueError('Strict local mode requires a loopback model URL without embedded credentials.')
    host=parsed.hostname or ''
    if host=='localhost': return
    try: allowed=ipaddress.ip_address(host.strip('[]')).is_loopback
    except ValueError: allowed=False
    if not allowed: raise ValueError('Strict local mode blocks remote AI endpoints. Use 127.0.0.1 on this PC.')

def validate_provider(provider_id,cfg):
    if provider_id in ('openai_cloud','gemini_cloud'):
        if cfg.get('cloud_enabled') is not True:raise ValueError('Enable the selected cloud AI in the connection form first.')
        if not str(cfg.get('api_key','')).strip():raise ValueError('Enter your own API key in JARVIS Settings.')
        return
    if provider_id=='cloud_setup':return
    if provider_id=='whisper':
        if cfg.get('backend','local')!='local': raise ValueError('Strict local mode requires on-device Whisper.')
    elif provider_id not in ('kokoro','piper','system_tts','pipeline'):
        raise ValueError('This provider is disabled in strict local mode: '+provider_id)

def _loopback(host):
    if isinstance(host,bytes): host=host.decode('ascii',errors='ignore')
    if host in ('localhost','127.0.0.1','::1'): return True
    try: return ipaddress.ip_address(str(host).strip('[]')).is_loopback
    except ValueError: return False

def audit_network(event,args):
    if event in ('socket.getaddrinfo','socket.gethostbyname','socket.gethostbyaddr'):
        host=args[0].decode('ascii') if isinstance(args[0],bytes) else args[0]
        permitted=_openai_request.get()
        if permitted and host==('api.openai.com' if permitted is True else permitted):return
        if not _loopback(args[0]): raise PermissionError('Strict local mode blocked external DNS/network access.')
    elif event in ('socket.connect','socket.sendto'):
        address=args[-1]
        if event=='socket.connect' and _openai_request.get() and isinstance(address,tuple) and len(address)>1 and address[1]==443:return
        if isinstance(address,tuple) and not _loopback(address[0]):
            raise PermissionError('Strict local mode blocked an external Python network request.')

def install_network_guard():
    global _installed
    if not _installed:
        sys.addaudithook(audit_network)
        _installed=True

def default_config():
    import platform
    return {'os_system':platform.system().lower(),'privacy_mode':'cloud_ai_local_speech',
        'dashboard_enabled':False,'dashboard_https':False,'morning_brief_enabled':False,
        'providers':{'mode':'pipeline','pipeline':{'stt':'whisper','llm':'cloud_setup','tts':'system_tts'},
          'sidecar':'cloud_setup','sidecar_first':True,'creds':{
            'whisper':{'backend':'local','model':'base','device':'cpu','language':'en'},'kokoro':{'voice':'bm_george','speed':1},'system_tts':{'voice':'Microsoft David Desktop'}}}}
