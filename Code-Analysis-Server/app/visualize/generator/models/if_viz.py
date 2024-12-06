from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConditionViz:
    id: int
    expr: str
    type: str
    code: str


@dataclass(frozen=True)
class IfElseDefineViz:
    depth: int
    conditions: tuple[ConditionViz, ...]
    code: str
    type: str = field(default="ifElseDefine", init=False)


@dataclass(frozen=True)
class IfElseChangeViz:
    id: int
    depth: int
    expr: str
    code: str
    type: str = field(default="ifElseChange", init=False)
