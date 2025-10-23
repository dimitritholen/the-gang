"""
Knowledge graph data models and persistence layer.

Entities represent nodes (Feature, Requirement, Task, etc.)
Relationships represent edges (requires, depends_on, implements, etc.)
JSONL format: one JSON object per line for efficient streaming and incremental updates.
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Set


# ============================================================================
# Enums
# ============================================================================

class EntityType(str, Enum):
    FEATURE = "feature"
    REQUIREMENT = "requirement"
    TECH_DECISION = "tech_decision"
    COMPONENT = "component"
    TASK = "task"
    PATTERN = "pattern"
    CONVENTION = "convention"


class RelationshipType(str, Enum):
    REQUIRES = "requires"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    FOLLOWS = "follows"
    JUSTIFIES = "justifies"
    BLOCKS = "blocks"
    DERIVED_FROM = "derived_from"


class RequirementType(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    AVAILABILITY = "availability"
    COMPLIANCE = "compliance"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"


# ============================================================================
# Base Classes
# ============================================================================

@dataclass
class Entity:
    """Base entity with common fields"""
    id: str
    name: str
    type: EntityType = EntityType.FEATURE  # Default, overridden in __post_init__
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_file: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['type'] = self.type.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        data = data.copy()
        data['type'] = EntityType(data['type'])
        return cls(**data)


@dataclass
class Relationship:
    """Edge between entities"""
    source_id: str
    target_id: str
    type: RelationshipType
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['type'] = self.type.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        data = data.copy()
        data['type'] = RelationshipType(data['type'])
        return cls(**data)

    @property
    def id(self) -> str:
        """Generate unique ID from source + target + type"""
        raw = f"{self.source_id}:{self.type.value}:{self.target_id}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ============================================================================
# Specific Entity Types
# ============================================================================

@dataclass
class Feature(Entity):
    """Feature entity"""
    status: Optional[str] = None
    priority: Optional[Priority] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = EntityType.FEATURE
        if isinstance(self.priority, str):
            self.priority = Priority(self.priority)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        if self.priority:
            d['priority'] = self.priority.value
        return d


@dataclass
class Requirement(Entity):
    """Requirement entity"""
    req_type: RequirementType = RequirementType.FUNCTIONAL
    priority: Priority = Priority.MEDIUM
    acceptance_criteria: List[str] = field(default_factory=list)
    parent_feature: Optional[str] = None
    user_story: Optional[str] = None
    target_metric: Optional[str] = None

    def __post_init__(self):
        self.type = EntityType.REQUIREMENT
        if isinstance(self.req_type, str):
            self.req_type = RequirementType(self.req_type)
        if isinstance(self.priority, str):
            self.priority = Priority(self.priority)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d['req_type'] = self.req_type.value
        d['priority'] = self.priority.value
        return d


@dataclass
class TechDecision(Entity):
    """Technical decision entity"""
    decision: str = ""
    rationale: str = ""
    alternatives: List[str] = field(default_factory=list)
    date: Optional[str] = None
    stakeholders: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = EntityType.TECH_DECISION


@dataclass
class Component(Entity):
    """Code component entity"""
    component_type: str = "unknown"  # class, function, module, service, etc.
    file_path: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    line_range: Optional[tuple[int, int]] = None

    def __post_init__(self):
        self.type = EntityType.COMPONENT


@dataclass
class Task(Entity):
    """Task entity"""
    status: TaskStatus = TaskStatus.NOT_STARTED
    dependencies: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    started: Optional[str] = None
    completed: Optional[str] = None

    def __post_init__(self):
        self.type = EntityType.TASK
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d['status'] = self.status.value
        return d


@dataclass
class Pattern(Entity):
    """Code pattern entity"""
    pattern_type: str = "unknown"  # naming, structure, error-handling, etc.
    examples: List[str] = field(default_factory=list)
    conformance_pct: Optional[float] = None
    violations: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = EntityType.PATTERN


@dataclass
class Convention(Entity):
    """Coding convention entity"""
    category: str = "unknown"  # file-naming, api-design, testing, etc.
    rule: str = ""
    conformance_pct: Optional[float] = None
    deviations: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        self.type = EntityType.CONVENTION


# ============================================================================
# Graph Store
# ============================================================================

class GraphStore:
    """
    JSONL-based graph storage with caching and mtime-based invalidation.
    Each feature has its own .jsonl file for modularity.
    """

    def __init__(self, memory_dir: Path):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._mtime_cache: Dict[str, float] = {}

    def _get_graph_path(self, feature_slug: str) -> Path:
        """Get JSONL path for feature"""
        return self.memory_dir / f"{feature_slug}.jsonl"

    def _is_cache_valid(self, path: Path) -> bool:
        """Check if cached data is still valid"""
        if not path.exists():
            return False
        current_mtime = path.stat().st_mtime
        cached_mtime = self._mtime_cache.get(str(path))
        return cached_mtime is not None and cached_mtime == current_mtime

    def load_graph(self, feature_slug: str) -> Dict[str, Any]:
        """
        Load graph from JSONL with caching.
        Returns: {entities: {id: entity_dict}, relationships: [rel_dict]}
        """
        path = self._get_graph_path(feature_slug)
        cache_key = str(path)

        if cache_key in self._cache and self._is_cache_valid(path):
            return self._cache[cache_key]

        entities = {}
        relationships = []

        if path.exists():
            with path.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    if 'source_id' in obj:  # Relationship
                        relationships.append(obj)
                    else:  # Entity
                        entities[obj['id']] = obj

        graph = {'entities': entities, 'relationships': relationships}
        self._cache[cache_key] = graph
        self._mtime_cache[cache_key] = path.stat().st_mtime if path.exists() else 0
        return graph

    def save_graph(self, feature_slug: str, entities: List[Entity], relationships: List[Relationship]) -> None:
        """Save entities and relationships to JSONL atomically"""
        path = self._get_graph_path(feature_slug)
        tmp_path = path.with_suffix('.jsonl.tmp')

        with tmp_path.open('w', encoding='utf-8') as f:
            for entity in entities:
                f.write(json.dumps(entity.to_dict(), ensure_ascii=False) + '\n')
            for rel in relationships:
                f.write(json.dumps(rel.to_dict(), ensure_ascii=False) + '\n')

        tmp_path.replace(path)

        # Invalidate cache
        cache_key = str(path)
        if cache_key in self._cache:
            del self._cache[cache_key]
        if cache_key in self._mtime_cache:
            del self._mtime_cache[cache_key]

    def query_entities(self, feature_slug: str, entity_type: Optional[EntityType] = None,
                       filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query entities with optional type and field filters"""
        graph = self.load_graph(feature_slug)
        results = []

        for entity in graph['entities'].values():
            if entity_type and entity['type'] != entity_type.value:
                continue

            if filters:
                match = True
                for key, value in filters.items():
                    if key not in entity or entity[key] != value:
                        match = False
                        break
                if not match:
                    continue

            results.append(entity)

        return results

    def query_relationships(self, feature_slug: str, source_id: Optional[str] = None,
                            target_id: Optional[str] = None, rel_type: Optional[RelationshipType] = None) -> List[Dict[str, Any]]:
        """Query relationships with optional filters"""
        graph = self.load_graph(feature_slug)
        results = []

        for rel in graph['relationships']:
            if source_id and rel['source_id'] != source_id:
                continue
            if target_id and rel['target_id'] != target_id:
                continue
            if rel_type and rel['type'] != rel_type.value:
                continue
            results.append(rel)

        return results

    def traverse(self, feature_slug: str, start_id: str, rel_type: RelationshipType,
                 direction: str = 'outbound', max_depth: int = 10) -> List[str]:
        """
        Traverse graph from start node following relationship type.
        direction: 'outbound' (source->target) or 'inbound' (target->source)
        Returns list of reached entity IDs.
        """
        graph = self.load_graph(feature_slug)
        visited: Set[str] = set()
        queue = [(start_id, 0)]
        results = []

        while queue:
            node_id, depth = queue.pop(0)
            if node_id in visited or depth > max_depth:
                continue

            visited.add(node_id)
            if node_id != start_id:
                results.append(node_id)

            for rel in graph['relationships']:
                if rel['type'] != rel_type.value:
                    continue

                if direction == 'outbound' and rel['source_id'] == node_id:
                    queue.append((rel['target_id'], depth + 1))
                elif direction == 'inbound' and rel['target_id'] == node_id:
                    queue.append((rel['source_id'], depth + 1))

        return results

    def get_entity(self, feature_slug: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get single entity by ID"""
        graph = self.load_graph(feature_slug)
        return graph['entities'].get(entity_id)

    def invalidate_cache(self, feature_slug: Optional[str] = None) -> None:
        """Invalidate cache for specific feature or all"""
        if feature_slug:
            path = self._get_graph_path(feature_slug)
            cache_key = str(path)
            if cache_key in self._cache:
                del self._cache[cache_key]
            if cache_key in self._mtime_cache:
                del self._mtime_cache[cache_key]
        else:
            self._cache.clear()
            self._mtime_cache.clear()
