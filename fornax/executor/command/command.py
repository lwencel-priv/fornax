from typing import List, Optional


class Command:

    def __init__(self, args: List[str], cwd: Optional[str] = None, daemon: bool = False) -> None:
        self._args: List[str] = args
        self._cwd = cwd
        self._daemon = daemon

    @property
    def args(self) -> List[str]:
        return self._args
    
    @property
    def cwd(self) -> List[str]:
        return self._cwd
        
    @property
    def daemon(self) -> List[str]:
        return self._daemon
