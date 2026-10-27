"""Run with Python 3. Creates only a fresh temporary repo, never touches cwd Git."""
from pathlib import Path
import subprocess
import tempfile


with tempfile.TemporaryDirectory(prefix='software-git-lab-') as temp:
    root = Path(temp)

    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.STDOUT).strip()

    git('init', '--initial-branch=main')
    git('config', 'user.name', 'Training Example')
    git('config', 'user.email', 'training@example.invalid')
    path = root / 'notes.txt'
    path.write_text('base\n'); git('add', 'notes.txt'); git('commit', '-m', 'base')
    base = git('rev-parse', 'HEAD')
    path.write_text('A\n'); git('add', 'notes.txt'); path.write_text('B\n')
    assert git('show', ':notes.txt') == 'A'
    git('commit', '-m', 'stage A')
    assert git('show', 'HEAD:notes.txt') == 'A'
    assert path.read_text() == 'B\n'
    assert '+B' in git('diff')
    # Recovery names an existing old commit; active working B stays in place.
    git('branch', 'rescue/base', base)
    assert git('show', 'rescue/base:notes.txt') == 'base'
    assert path.read_text() == 'B\n'
    print('Passed: index snapshot, working edits, and non-destructive rescue branch')
    print('Lab used a disposable repository; it is removed on exit.')
