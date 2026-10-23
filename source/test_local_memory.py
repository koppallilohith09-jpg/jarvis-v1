import asyncio,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from memory.local_database import LocalDatabase
from providers.engine_pipeline import PipelineEngine

class Model:
    caps={'tools':True,'tool_format':'openai'}
    def __init__(self):self.calls=[]
    async def chat(self,messages,tools=None):
        self.calls.append((messages,tools))
        yield {'text':'Project Cedar is due on 28 October. The budget is 4,500 rupees.'}

class Memory(unittest.IsolatedAsyncioTestCase):
    async def test_empty_model_answer_reports_failure_and_ends_turn(self):
        class Empty(Model):
            async def chat(self,messages,tools=None):
                if False:yield {}
        e=PipelineEngine(Empty(),store=self.db)
        await e.send_client_content(turns={'parts':[{'text':'What is two plus two?'}]});await e._gen
        messages=[]
        while not e._queue.empty():messages.append(e._queue.get_nowait())
        self.assertTrue(any(m.server_content and m.server_content.turn_complete for m in messages))
        self.assertNotEqual(e._history[-1]['role'],'assistant')
        await e.close()
    def test_disconnected_ai_has_no_offline_fallback(self):
        from providers.llm_cloud_setup import CloudSetup
        with self.assertRaisesRegex(RuntimeError,'AI is not connected'):CloudSetup().complete([])
    async def asyncSetUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.db=LocalDatabase(self.root/'memory.sqlite3')
    async def asyncTearDown(self):self.temp.cleanup()
    async def test_file_reaches_model_without_tool_choice_and_survives_restart(self):
        path=self.root/'notes.txt';path.write_text('Project Cedar\nDeadline: 28 October\nBudget: 4,500 rupees.')
        llm=Model();e=PipelineEngine(llm,store=self.db);await e.attach_file(path)
        shown=[];e.on_document_analysis=lambda *args:shown.append(args)
        await e.send_client_content(turns={'parts':[{'text':'analyse the uploaded file'}]});await e._gen
        self.assertEqual(len(llm.calls),1);messages,tools=llm.calls[0]
        self.assertIsNone(tools);self.assertIn('4,500',messages[-1]['content']);self.assertTrue(shown)
        self.assertIn('Cedar',self.db.search('Cedar')[0]['body']);await e.close()
        db=LocalDatabase(self.db.path);self.assertEqual(db.stats()['documents'],1)
        restarted=PipelineEngine(Model(),store=db);self.assertIn('Cedar',str(restarted._messages()));await restarted.close()
    async def test_facts_pause_clear_and_quotes(self):
        session=self.db.session();self.db.add_message(session,'user','My name is Lohith. Remember that my project is Cedar.')
        self.assertEqual(self.db.facts()[0]['value'],'Lohith')
        self.db.set_setting('remember','0');before=self.db.stats();self.db.add_message(session,'user','Do not store this')
        self.assertEqual(before,self.db.stats());self.db.search('" : bad * query')
        self.db.clear();self.assertEqual(self.db.stats()['messages'],0);self.assertEqual(self.db.facts(),[])
    async def test_encoding_and_deduplication(self):
        path=self.root/'notes.txt';path.write_bytes('Caf\u00e9 paid \u00a350'.encode('cp1252'))
        doc=self.db.import_document(path);self.assertEqual(doc,self.db.import_document(path))
        self.assertIn('Caf\u00e9',self.db.document(doc)['body'])

if __name__=='__main__':unittest.main()
