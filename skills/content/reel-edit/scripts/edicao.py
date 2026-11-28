#!/usr/bin/env python3
"""edicao: the only writer of a reel's edicao.md, the reel-edit state file."""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import os
import pathlib
import re
import sys
import tempfile

STATE = 'edicao.md'
STEPS = ('reel-cut', 'reel-motion', 'reel-finish')
OUTPUTS = ('capcut', 'mp4', 'both')
KINDS = ('approval', 'publish', 'human-step', 'problem')

EXIT = {'NotStarted': 3, 'StateInvalid': 4, 'AlreadyWaiting': 5, 'NotWaitingApproval': 6,
        'MissingFile': 7, 'WaitingApproval': 8, 'AlreadyStarted': 9}


class Fail(Exception):
    def __init__(self, tag, message, next_):
        super().__init__(message)
        self.tag, self.message, self.next = tag, message, next_


# ---- the file -------------------------------------------------------------

def render(s):
    lines = [f"# Edição: {s['title']}",
             f"- Roteiro: {s['script']}",
             f"- Saída: {s['output']}",
             f"- Etapa: {s['step']}"]
    for ap in s['approved']:
        h = f", {ap['hash']}" if ap.get('hash') else ''
        lines.append(f"- Aprovado: {ap['step']}: {ap['gate']} ({ap['date']}, autor, via {ap['via']}, \"{ap['quote']}\"{h})")
    w = s.get('waiting')
    if w:
        lines.append(f"- Aguardando: {w['kind']} - {w['step']}: {w['reason']}")
    lines.append('## Histórico')
    lines += [f'- {h}' for h in s['history']]
    return '\n'.join(lines) + '\n'


def parse(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    def bad(what):
        return Fail('StateInvalid', f'{path}: {what}', f'put the line named here back in the format of edicao.py --help, or restore {path} from a copy; '
                    'then run status again')

    if not lines or not lines[0].startswith('# Edição: '):
        raise bad('first line must be "# Edição: <title>"')
    s = {'title': lines[0][len('# Edição: '):], 'approved': [], 'history': []}
    fields = {'Roteiro': 'script', 'Saída': 'output', 'Etapa': 'step'}
    waiting_re = re.compile(rf"- Aguardando: ({'|'.join(KINDS)}) - ({'|'.join(STEPS)}): (.+)")
    approved_re = re.compile(rf'- Aprovado: ({"|".join(STEPS)}): (.+) \((\d{{4}}-\d\d-\d\d), autor, via ([a-z-]+), "(.+)"(?:, ([0-9a-f]{{12}}))?\)')
    i = 1
    while i < len(lines) and lines[i] != '## Histórico':
        if lines[i].startswith('- Aguardando: '):
            w = waiting_re.fullmatch(lines[i])
            if not w or 'waiting' in s:
                raise bad(f'line {i + 1}: "Aguardando: <{"|".join(KINDS)}> - <step>: <reason>", once')
            s['waiting'] = {'kind': w[1], 'step': w[2], 'reason': w[3]}
            i += 1
            continue
        if lines[i].startswith('- Aprovado: '):
            ap = approved_re.fullmatch(lines[i])
            if not ap:
                raise bad(f'line {i + 1}: "Aprovado: <step>: <gate> (<date>, autor, via <door>, \"<quote>\"[, <hash>])"')
            s['approved'].append({'step': ap[1], 'gate': ap[2], 'date': ap[3], 'via': ap[4], 'quote': ap[5],
                                  'hash': ap[6]})
            i += 1
            continue
        m = re.fullmatch(r'- (\w+): (.+)', lines[i])
        if not m or m[1] not in fields:
            raise bad(f'line {i + 1}: unknown header line "{lines[i]}"')
        s[fields[m[1]]] = m[2]
        i += 1
    for k in fields.values():
        if k not in s:
            raise bad(f'missing header field for {k}')
    if s['output'] not in OUTPUTS:
        raise bad(f'Saída must be one of {", ".join(OUTPUTS)}')
    if s['step'] not in STEPS:
        raise bad(f'Etapa must be one of {", ".join(STEPS)}')
    if i == len(lines):
        raise bad('missing "## Histórico"')
    for n, line in enumerate(lines[i + 1:], i + 2):
        if not line.startswith('- '):
            raise bad(f'line {n}: history lines start with "- "')
        s['history'].append(line[2:])
    return s


def write(path, s):
    fd, tmp = tempfile.mkstemp(prefix='.edicao-', dir=path.parent)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(render(s))
    os.replace(tmp, path)


@contextlib.contextmanager
def locked(reel):
    """Hold the reel's lock across a whole read-modify-write."""
    if not pathlib.Path(reel).is_dir():
        raise Fail('NotStarted', f'{reel} is not a folder', 'pass the reel folder, the one with the raw clips')
    with open(pathlib.Path(reel) / '.edicao.lock', 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def history_line(step, what):
    return f'{datetime.date.today().isoformat()} · {step} · {what}'


# ---- verbs ----------------------------------------------------------------

def state_path(reel):
    return pathlib.Path(reel) / STATE


def read(reel):
    path = state_path(reel)
    if not path.exists():
        raise Fail('NotStarted', f'{path} does not exist',
                   'run: edicao.py start <reel-dir> --title ... --output ... --script ...')
    return path, parse(path)


def cmd_start(a):
    path = state_path(a.reel)
    if a.script != 'none':
        check_files(a.reel, [a.script])
    with locked(a.reel):
        if path.exists():
            raise Fail('AlreadyStarted', f'{path} already exists',
                       'run status and resume from it; never start a reel twice')
        return _start(a, path)


def _start(a, path):
    s = {'title': a.title, 'script': a.script, 'output': a.output, 'step': STEPS[0], 'approved': [],
         'history': [history_line('início', f'saída {a.output}, roteiro {a.script}')]}
    write(path, s)
    return status_of(s)


def files_note(files):
    return f" · arquivos: {', '.join(files)}" if files else ''


def check_files(reel, files):
    for f in files:
        if not (pathlib.Path(reel) / f).is_file():
            raise Fail('MissingFile', f'{f} is not a file in {reel}',
                       'pass paths relative to the reel folder, of files that exist')


def files_hash(reel, files):
    h = hashlib.sha256()
    for f in files:
        h.update((pathlib.Path(reel) / f).read_bytes())
    return h.hexdigest()[:12]


def cmd_hold(a):
    check_files(a.reel, a.file)
    with locked(a.reel):
        path, s = read(a.reel)
        if s.get('waiting'):
            w = s['waiting']
            raise Fail('AlreadyWaiting', f"{path} already waits for {w['kind']} at {w['step']}",
                       'clear that stop first: approve for approval or publish, log for human-step or problem')
        s['step'] = a.step
        s['waiting'] = {'kind': a.kind, 'step': a.step, 'reason': a.reason}
        s['history'].append(history_line(a.step, f'parada {a.kind}: {a.reason}{files_note(a.file)}'))
        write(path, s)
        return status_of(s)


def cmd_approve(a):
    with locked(a.reel):
        path, s = read(a.reel)
        w = s.get('waiting')
        if not w or w['kind'] not in ('approval', 'publish'):
            raise Fail('NotWaitingApproval', f'{path} has no approval or publish stop to clear',
                       'run status; approve only answers a stop recorded with hold --kind approval|publish')
        ap = {'step': w['step'], 'gate': w['reason'], 'date': datetime.date.today().isoformat(), 'via': a.via, 'quote': a.quote,
              'hash': None}
        if w['kind'] == 'publish':
            if not a.file:
                raise Fail('MissingFile', 'a publish approval needs the approved files',
                           'pass --file for each file the author approved (the mp4, the caption)')
            check_files(a.reel, a.file)
            ap['hash'] = files_hash(a.reel, a.file)
        s['approved'].append(ap)
        s['waiting'] = None
        h = f", {ap['hash']}" if ap['hash'] else ''
        s['history'].append(history_line(w['step'], f'aprovado via {a.via}: "{a.quote}"{h}'))
        write(path, s)
        return status_of(s)


def cmd_log(a):
    check_files(a.reel, a.file)
    with locked(a.reel):
        path, s = read(a.reel)
        w = s.get('waiting')
        if w and w['kind'] in ('approval', 'publish'):
            raise Fail('WaitingApproval', f"{path} waits for the author's {w['kind']} at {w['step']}",
                       'show the author what the gate shows and run approve on their word; do not go on before it')
        s['step'] = a.step
        s['waiting'] = None
        s['history'].append(history_line(a.step, f'{a.note}{files_note(a.file)}'))
        write(path, s)
        return status_of(s)


NEXT = {
    'approval': 'show the author what {step} shows at this gate ({reason}) and wait for their answer; '
                'on their word run approve with --via and --quote, then go on',
    'publish': 'show the author the files to approve ({reason}) and wait; on their word run approve '
               'with --via, --quote and --file for each approved file',
    'human-step': 'ask the author to do it ({reason}) and wait; when they say it is done, run log '
                  '--step {step} with what they did',
    'problem': 'decide with the author what to do about it ({reason}); then run log --step {step} with the decision',
}


def next_of(s):
    w = s.get('waiting')
    if w:
        return NEXT[w['kind']].format(**w)
    return f"invoke the {s['step']} skill again and go on from the last line of Histórico"


def status_of(s):
    return {'next': next_of(s), 'title': s['title'], 'script': s['script'], 'output': s['output'], 'step': s['step'],
            'approved': s['approved'], 'waiting': s.get('waiting'), 'history': s['history']}


def cmd_status(a):
    _, s = read(a.reel)
    return status_of(s)


# ---- entry point ----------------------------------------------------------

def text(v):
    v = v.strip()
    if not v or '\n' in v or '\r' in v:
        raise argparse.ArgumentTypeError('must be non-empty, on one line')
    return v


def door(v):
    if not re.fullmatch(r'[a-z-]+', v):
        raise argparse.ArgumentTypeError('one lowercase word naming where the words came from, e.g. live')
    return v


TOP_HELP = """\
edicao.md is the reel-edit state file, in the reel folder. Only these verbs write it:
start once, hold at every stop, approve on the author's word, log for work done, and
status to resume. Every verb prints JSON on stdout. A refused verb prints
{"_tag", "message", "next"}, changes nothing and exits with its kind's code:

  2  usage: a flag missing or invalid (argparse, message on stderr)
  3  NotStarted: no edicao.md (or no such folder); run start
  4  StateInvalid: edicao.md was edited by hand and breaks the format
  5  AlreadyWaiting: hold while a stop is open
  6  NotWaitingApproval: approve with no approval or publish stop open
  7  MissingFile: a --file or --script that is not in the reel folder
  8  WaitingApproval: log while the author's approval is pending
  9  AlreadyStarted: start on a reel that has edicao.md

No git, no network, no model. Paths in --file and --script are relative to the reel folder.

edicao.md format (pt-BR field names; kinds and steps as above):
  # Edição: <title>
  - Roteiro: <script file or none>
  - Saída: capcut | mp4 | both
  - Etapa: reel-cut | reel-motion | reel-finish
  - Aprovado: <step>: <gate> (<YYYY-MM-DD>, autor, via <door>, "<quote>"[, <hash>])   one per approval
  - Aguardando: <kind> - <step>: <reason>                                             only while stopped
  ## Histórico
  - <YYYY-MM-DD> · <step> · <what was done>
"""


def verb(sub, name, summary, example, fn):
    v = sub.add_parser(name, help=summary, description=summary,
                       epilog=f'example:\n  python3 scripts/edicao.py {name} {example}',
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    v.add_argument('reel', help='the reel folder, where edicao.md lives')
    v.set_defaults(fn=fn)
    return v


def parser():
    p = argparse.ArgumentParser(prog='edicao.py', description=__doc__, epilog=TOP_HELP,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='verb', required=True)
    files = dict(action='append', default=[], metavar='FILE',
                 help='a file made or approved at this point, relative to the reel folder (repeatable)')

    v = verb(sub, 'start', 'create edicao.md once the script and the output form are known',
             '"$REEL" --title "WhatsApp e as tintas" --output mp4 --script roteiro.md', cmd_start)
    v.add_argument('--title', required=True, type=text)
    v.add_argument('--output', required=True, choices=OUTPUTS)
    v.add_argument('--script', required=True, type=text, help='the script file in the reel folder, or none')

    v = verb(sub, 'hold', 'record a stop; the agent ends its turn after it',
             '"$REEL" --step reel-cut --kind approval --reason "tabela de tomadas" --file cortes.json', cmd_hold)
    v.add_argument('--step', required=True, choices=STEPS)
    v.add_argument('--kind', required=True, choices=KINDS,
                   help='approval: a result to approve; publish: something outward-facing; '
                        'human-step: work only the author can do; problem: a decision after a failure')
    v.add_argument('--reason', required=True, type=text, help='what the stop waits for, in one line')
    v.add_argument('--file', **files)

    v = verb(sub, 'approve', "clear an approval or publish stop on the author's first-hand word",
             '"$REEL" --via live --quote "aprovado, segue"', cmd_approve)
    v.add_argument('--via', required=True, type=door, help='where the words came from, e.g. live')
    v.add_argument('--quote', required=True, type=text, help="the author's words, verbatim")
    v.add_argument('--file', **{**files, 'help': 'required for a publish stop: the approved files, hashed'})

    v = verb(sub, 'log', 'record work done at a step; clears a human-step or problem stop',
             '"$REEL" --step reel-finish --note "mp4 final renderizado" --file exports/final.mp4', cmd_log)
    v.add_argument('--step', required=True, choices=STEPS)
    v.add_argument('--note', required=True, type=text, help='what was done, in one line')
    v.add_argument('--file', **files)

    verb(sub, 'status', "the reel's state and what to do next, read from edicao.md", '"$REEL"', cmd_status)
    return p


def main():
    a = parser().parse_args()
    try:
        out, code = a.fn(a), 0
    except Fail as e:
        out, code = {'_tag': e.tag, 'message': e.message, 'next': e.next}, EXIT[e.tag]
    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    sys.stdout.flush()
    sys.exit(code)


if __name__ == '__main__':
    main()
