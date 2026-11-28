"""Tests for scripts/edicao.py, run as a process, the way the agent calls it.

  python3 -m unittest discover -s skills/content/reel-edit/evals/scripts
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

CLI = pathlib.Path(__file__).resolve().parents[2] / 'scripts' / 'edicao.py'


def run(*args):
    p = subprocess.run([sys.executable, str(CLI), *args], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.stdout.strip() else None
    return p.returncode, out, p.stderr


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.reel = pathlib.Path(self._tmp.name)
        self.state = self.reel / 'edicao.md'

    def tearDown(self):
        self._tmp.cleanup()

    def start(self, *extra):
        (self.reel / 'roteiro.md').write_text('roteiro', encoding='utf-8')
        return run('start', str(self.reel), '--title', 'Reel do WhatsApp', '--output', 'mp4',
                   '--script', 'roteiro.md', *extra)


class Start(Base):
    def test_start_creates_the_state_file_and_status_reads_it(self):
        code, out, _ = self.start()
        self.assertEqual(code, 0)
        self.assertTrue(self.state.exists())
        code, st, _ = run('status', str(self.reel))
        self.assertEqual(code, 0)
        self.assertEqual(st['title'], 'Reel do WhatsApp')
        self.assertEqual(st['output'], 'mp4')
        self.assertEqual(st['script'], 'roteiro.md')
        self.assertEqual(st['step'], 'reel-cut')
        self.assertIsNone(st['waiting'])
        self.assertEqual(len(st['history']), 1)


class StartRefuses(Base):
    def test_start_on_a_reel_already_started_is_refused_and_changes_nothing(self):
        self.start()
        before = self.state.read_text(encoding='utf-8')
        code, out, _ = self.start()
        self.assertEqual(out['_tag'], 'AlreadyStarted')
        self.assertEqual(self.state.read_text(encoding='utf-8'), before)

    def test_start_without_a_script_takes_none(self):
        code, _, _ = run('start', str(self.reel), '--title', 'Celular', '--output', 'capcut', '--script', 'none')
        self.assertEqual(code, 0)
        self.assertEqual(run('status', str(self.reel))[1]['script'], 'none')

    def test_start_with_a_script_that_is_not_there_is_refused(self):
        code, out, _ = run('start', str(self.reel), '--title', 'x', '--output', 'mp4', '--script', 'roteiro.md')
        self.assertEqual(out['_tag'], 'MissingFile')
        self.assertFalse(self.state.exists())

    def test_status_before_start_says_to_start(self):
        code, out, _ = run('status', str(self.reel))
        self.assertEqual(out['_tag'], 'NotStarted')
        self.assertIn('start', out['next'])


class Validation(Base):
    def test_a_hand_edited_file_that_breaks_the_format_fails_every_verb_and_is_not_rewritten(self):
        self.start()
        broken = self.state.read_text(encoding='utf-8').replace('- Saída: mp4', '- Saída: mov')
        self.state.write_text(broken, encoding='utf-8')
        for args in (('status',), ('hold', '--step', 'reel-cut', '--kind', 'approval', '--reason', 'x')):
            code, out, _ = run(args[0], str(self.reel), *args[1:])
            self.assertEqual(out['_tag'], 'StateInvalid')
            self.assertIn('Saída', out['message'])
            self.assertNotIn('format', out['next'])
        self.assertEqual(self.state.read_text(encoding='utf-8'), broken)

    def test_an_unknown_waiting_kind_is_invalid(self):
        self.start()
        text = self.state.read_text(encoding='utf-8').replace(
            '## Histórico', '- Aguardando: review - reel-cut: x\n## Histórico')
        self.state.write_text(text, encoding='utf-8')
        self.assertEqual(run('status', str(self.reel))[1]['_tag'], 'StateInvalid')

    def test_no_temp_file_is_left_behind(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'approval', '--reason', 'tabela')
        self.assertEqual(sorted(p.name for p in self.reel.iterdir() if p.name.startswith('.edicao-')), [])


class Hold(Base):
    def hold_cut(self, *extra):
        (self.reel / 'cortes.json').write_text('{}', encoding='utf-8')
        return run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'approval',
                   '--reason', 'tabela de tomadas', '--file', 'cortes.json', *extra)

    def test_hold_records_the_stop_and_status_shows_it(self):
        self.start()
        code, _, _ = self.hold_cut()
        self.assertEqual(code, 0)
        _, st, _ = run('status', str(self.reel))
        self.assertEqual(st['waiting'], {'kind': 'approval', 'step': 'reel-cut', 'reason': 'tabela de tomadas'})
        self.assertIn('cortes.json', st['history'][-1])

    def test_a_second_hold_while_stopped_is_refused_and_changes_nothing(self):
        self.start()
        self.hold_cut()
        before = self.state.read_text(encoding='utf-8')
        code, out, _ = run('hold', str(self.reel), '--step', 'reel-motion', '--kind', 'approval',
                           '--reason', 'plano')
        self.assertNotEqual(code, 0)
        self.assertEqual(out['_tag'], 'AlreadyWaiting')
        self.assertIn('next', out)
        self.assertEqual(self.state.read_text(encoding='utf-8'), before)

    def test_hold_refuses_a_kind_outside_the_four(self):
        self.start()
        code, _, _ = run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'review',
                         '--reason', 'x')
        self.assertNotEqual(code, 0)


class Approve(Base):
    def test_approve_clears_the_stop_and_records_the_authors_words(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'approval', '--reason', 'tabela de tomadas')
        code, _, _ = run('approve', str(self.reel), '--via', 'live', '--quote', 'aprovado, segue')
        self.assertEqual(code, 0)
        _, st, _ = run('status', str(self.reel))
        self.assertIsNone(st['waiting'])
        self.assertEqual(st['approved'][0]['step'], 'reel-cut')
        self.assertEqual(st['approved'][0]['gate'], 'tabela de tomadas')
        self.assertEqual(st['approved'][0]['via'], 'live')
        self.assertEqual(st['approved'][0]['quote'], 'aprovado, segue')
        self.assertIn('aprovado, segue', st['history'][-1])

    def test_approve_needs_the_door_and_the_quote(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'approval', '--reason', 'tabela')
        self.assertNotEqual(run('approve', str(self.reel), '--via', 'live')[0], 0)
        self.assertNotEqual(run('approve', str(self.reel), '--quote', 'ok')[0], 0)
        self.assertNotEqual(run('approve', str(self.reel), '--via', 'live', '--quote', '  ')[0], 0)
        self.assertNotEqual(run('approve', str(self.reel), '--via', 'whatever', '--quote', 'ok')[0], 0)

    def test_approve_with_no_approval_stop_is_refused(self):
        self.start()
        code, out, _ = run('approve', str(self.reel), '--via', 'live', '--quote', 'ok')
        self.assertNotEqual(code, 0)
        self.assertEqual(out['_tag'], 'NotWaitingApproval')
        run('hold', str(self.reel), '--step', 'reel-finish', '--kind', 'human-step',
            '--reason', 'criar o projeto vazio no CapCut')
        code, out, _ = run('approve', str(self.reel), '--via', 'live', '--quote', 'ok')
        self.assertEqual(out['_tag'], 'NotWaitingApproval')

    def test_a_publish_approval_is_bound_to_the_files_by_hash(self):
        self.start()
        mp4 = self.reel / 'final.mp4'
        mp4.write_bytes(b'video')
        run('hold', str(self.reel), '--step', 'reel-finish', '--kind', 'publish', '--reason', 'postar')
        code, out, _ = run('approve', str(self.reel), '--via', 'live', '--quote', 'pode postar')
        self.assertEqual(out['_tag'], 'MissingFile')
        code, _, _ = run('approve', str(self.reel), '--via', 'live', '--quote', 'pode postar',
                         '--file', 'final.mp4')
        self.assertEqual(code, 0)
        _, st, _ = run('status', str(self.reel))
        self.assertRegex(st['approved'][0]['hash'], r'^[0-9a-f]{12}$')


class Resume(Base):
    def test_status_tells_a_fresh_session_what_to_do_next(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-motion', '--kind', 'approval', '--reason', 'stills das cenas')
        nxt = run('status', str(self.reel))[1]['next']
        self.assertIn('stills das cenas', nxt)
        self.assertIn('approve', nxt)
        run('approve', str(self.reel), '--via', 'live', '--quote', 'aprovado')
        nxt = run('status', str(self.reel))[1]['next']
        self.assertIn('reel-motion', nxt)

    def test_a_reel_folder_that_does_not_exist_is_a_clear_error(self):
        code, out, _ = run('status', str(self.reel / 'nao-existe'))
        self.assertEqual(out['_tag'], 'NotStarted')
        code, out, _ = run('hold', str(self.reel / 'nao-existe'), '--step', 'reel-cut', '--kind', 'approval',
                           '--reason', 'x')
        self.assertEqual(out['_tag'], 'NotStarted')


class Log(Base):
    def test_log_records_a_step_done_with_its_files(self):
        self.start()
        (self.reel / 'final.mp4').write_bytes(b'video')
        code, _, _ = run('log', str(self.reel), '--step', 'reel-finish', '--note', 'mp4 renderizado',
                         '--file', 'final.mp4')
        self.assertEqual(code, 0)
        _, st, _ = run('status', str(self.reel))
        self.assertEqual(st['step'], 'reel-finish')
        self.assertIn('mp4 renderizado', st['history'][-1])
        self.assertIn('final.mp4', st['history'][-1])

    def test_log_clears_a_human_step_or_problem_stop(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-finish', '--kind', 'human-step',
            '--reason', 'criar o projeto vazio no CapCut')
        code, _, _ = run('log', str(self.reel), '--step', 'reel-finish', '--note', 'projeto criado pelo autor')
        self.assertEqual(code, 0)
        self.assertIsNone(run('status', str(self.reel))[1]['waiting'])

    def test_log_does_not_clear_an_approval(self):
        self.start()
        run('hold', str(self.reel), '--step', 'reel-cut', '--kind', 'approval', '--reason', 'tabela')
        code, out, _ = run('log', str(self.reel), '--step', 'reel-motion', '--note', 'plano feito')
        self.assertEqual(out['_tag'], 'WaitingApproval')
        self.assertEqual(run('status', str(self.reel))[1]['waiting']['kind'], 'approval')

    def test_a_missing_file_is_refused(self):
        self.start()
        code, out, _ = run('log', str(self.reel), '--step', 'reel-cut', '--note', 'corte',
                           '--file', 'nao-existe.mp4')
        self.assertEqual(out['_tag'], 'MissingFile')


class Help(unittest.TestCase):
    def test_every_verb_has_help_with_an_example(self):
        for verb in ('start', 'hold', 'approve', 'log', 'status'):
            p = subprocess.run([sys.executable, str(CLI), verb, '--help'], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, verb)
            self.assertIn(f'example:\n  python3 scripts/edicao.py {verb} ', p.stdout, verb)

    def test_the_top_help_lists_the_exit_codes(self):
        p = subprocess.run([sys.executable, str(CLI), '--help'], capture_output=True, text=True)
        for tag in ('NotStarted', 'StateInvalid', 'AlreadyWaiting', 'NotWaitingApproval', 'MissingFile',
                    'WaitingApproval', 'AlreadyStarted'):
            self.assertIn(tag, p.stdout)


if __name__ == '__main__':
    unittest.main()
