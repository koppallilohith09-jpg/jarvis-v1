"""Synthetic local speech check; does not record a microphone or launch apps."""
import asyncio
import json
from pathlib import Path
import time
from core.local_privacy import install_network_guard
install_network_guard()
from providers.tts_kokoro import KokoroTTS
from providers.stt_whisper import WhisperSTT
from core.quick_commands import parse

async def main():
    voice=KokoroTTS({});hearing=WhisperSTT({'language':'en'})
    start=time.monotonic();await asyncio.gather(voice.warmup(),hearing.warmup());warm=time.monotonic()-start
    start=time.monotonic();pcm,rate=await asyncio.to_thread(voice._synth,'Open YouTube.');speak=time.monotonic()-start
    start=time.monotonic();text=await hearing.transcribe(pcm,rate);hear=time.monotonic()-start
    plan=parse(text)
    if not plan or plan.get('name')!='browser_control':raise AssertionError('Synthetic speech did not route to the browser: '+text)
    report={'startup_warmup_seconds':round(warm,2),'warm_tts_seconds':round(speak,2),'warm_stt_seconds':round(hear,2),'recognized':text,'route':plan['name'],'uses_llm_for_this_command':False,'physical_microphone_test':False}
    Path('voice-diagnostics.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':asyncio.run(main())
