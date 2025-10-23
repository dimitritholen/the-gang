"""
Integration tests for knowledge graph system
"""

import json
import tempfile
from pathlib import Path
import pytest

# Add parent dir to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_tools.graph import (
    GraphStore, Feature, Requirement, Relationship,
    EntityType, RequirementType, Priority, RelationshipType
)
from code_tools.parsers.requirements_parser import RequirementsParser
from code_tools.builders.feature_graph_builder import FeatureGraphBuilder


def test_entity_serialization():
    """Test entity to_dict/from_dict roundtrip"""
    feature = Feature(
        id="feature:test",
        name="Test Feature",
        status="active",
        priority=Priority.HIGH,
        dependencies=["dep1"],
        tags=["test", "example"]
    )

    # Serialize
    data = feature.to_dict()
    assert data['id'] == "feature:test"
    assert data['type'] == "feature"
    assert data['priority'] == "high"

    # Deserialize
    restored = Feature.from_dict(data)
    assert restored.id == feature.id
    assert restored.priority == Priority.HIGH


def test_relationship_id_generation():
    """Test relationship ID generation is deterministic"""
    rel1 = Relationship(
        source_id="feature:a",
        target_id="req:b",
        type=RelationshipType.REQUIRES
    )

    rel2 = Relationship(
        source_id="feature:a",
        target_id="req:b",
        type=RelationshipType.REQUIRES
    )

    assert rel1.id == rel2.id


def test_graph_store_save_load():
    """Test JSONL persistence"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = GraphStore(Path(tmpdir))

        # Create test data
        entities = [
            Feature(
                id="feature:test",
                name="Test Feature",
                status="active"
            ),
            Requirement(
                id="req:001",
                name="Test Requirement",
                req_type=RequirementType.FUNCTIONAL,
                priority=Priority.HIGH,
                parent_feature="feature:test"
            )
        ]

        relationships = [
            Relationship(
                source_id="feature:test",
                target_id="req:001",
                type=RelationshipType.REQUIRES
            )
        ]

        # Save
        store.save_graph("test-feature", entities, relationships)

        # Verify file exists
        graph_file = Path(tmpdir) / "test-feature.jsonl"
        assert graph_file.exists()

        # Load
        graph = store.load_graph("test-feature")
        assert len(graph['entities']) == 2
        assert len(graph['relationships']) == 1
        assert 'feature:test' in graph['entities']
        assert 'req:001' in graph['entities']


def test_graph_store_query_entities():
    """Test entity querying"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = GraphStore(Path(tmpdir))

        entities = [
            Feature(id="feature:a", name="Feature A", status="active"),
            Requirement(id="req:001", name="Req 1", req_type=RequirementType.FUNCTIONAL, priority=Priority.HIGH),
            Requirement(id="req:002", name="Req 2", req_type=RequirementType.SECURITY, priority=Priority.LOW)
        ]

        store.save_graph("test", entities, [])

        # Query all requirements
        reqs = store.query_entities("test", entity_type=EntityType.REQUIREMENT)
        assert len(reqs) == 2

        # Query with filter
        high_reqs = store.query_entities("test", filters={'priority': 'high'})
        assert len(high_reqs) == 1
        assert high_reqs[0]['id'] == 'req:001'


def test_graph_store_traverse():
    """Test graph traversal"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = GraphStore(Path(tmpdir))

        entities = [
            Feature(id="feature:a", name="A"),
            Requirement(id="req:1", name="R1", req_type=RequirementType.FUNCTIONAL, priority=Priority.HIGH),
            Requirement(id="req:2", name="R2", req_type=RequirementType.FUNCTIONAL, priority=Priority.HIGH)
        ]

        relationships = [
            Relationship(source_id="feature:a", target_id="req:1", type=RelationshipType.REQUIRES),
            Relationship(source_id="feature:a", target_id="req:2", type=RelationshipType.REQUIRES)
        ]

        store.save_graph("test", entities, relationships)

        # Traverse from feature to requirements
        reached = store.traverse("test", "feature:a", RelationshipType.REQUIRES, direction="outbound")
        assert len(reached) == 2
        assert "req:1" in reached
        assert "req:2" in reached


def test_requirements_parser():
    """Test parsing EXAMPLE requirements file"""
    example_path = Path(__file__).parent.parent.parent / ".claude/memory/EXAMPLE-requirements-user-authentication.md"

    if not example_path.exists():
        pytest.skip("EXAMPLE file not found")

    parser = RequirementsParser(example_path)
    entities, relationships = parser.parse()

    # Should have feature entity
    features = [e for e in entities if e.type == EntityType.FEATURE]
    assert len(features) == 1
    assert "authentication" in features[0].name.lower()

    # Should have requirements
    requirements = [e for e in entities if e.type == EntityType.REQUIREMENT]
    assert len(requirements) > 0

    # Should have FR requirements
    fr_reqs = [r for r in requirements if r.req_type == RequirementType.FUNCTIONAL]
    assert len(fr_reqs) >= 4  # FR-001 through FR-004

    # Should have NFR requirements
    nfr_reqs = [r for r in requirements if r.req_type != RequirementType.FUNCTIONAL]
    assert len(nfr_reqs) > 0

    # Should have relationships
    assert len(relationships) > 0

    # All requirements should be linked to feature
    feature_id = features[0].id
    req_rels = [r for r in relationships if r.type == RelationshipType.REQUIRES and r.source_id == feature_id]
    assert len(req_rels) == len(requirements)


def test_feature_graph_builder():
    """Test full builder pipeline"""
    example_path = Path(__file__).parent.parent.parent / ".claude/memory/EXAMPLE-requirements-user-authentication.md"

    if not example_path.exists():
        pytest.skip("EXAMPLE file not found")

    with tempfile.TemporaryDirectory() as tmpdir:
        builder = FeatureGraphBuilder(Path(tmpdir))

        # Build from requirements
        result = builder.build_from_requirements(example_path, "user-authentication")

        assert result['feature_slug'] == "user-authentication"
        assert result['entity_count'] > 0
        assert result['relationship_count'] > 0

        # Verify JSONL created
        graph_file = Path(tmpdir) / "user-authentication.jsonl"
        assert graph_file.exists()

        # Verify can query
        store = builder.store
        entities = store.query_entities("user-authentication")
        assert len(entities) > 0

        # Get summary
        summary = builder.get_feature_summary("user-authentication")
        assert summary['total_entities'] > 0
        assert 'feature' in summary['entity_counts']
        assert 'requirement' in summary['entity_counts']


def test_cache_invalidation():
    """Test cache invalidation on file modification"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = GraphStore(Path(tmpdir))

        entities_v1 = [Feature(id="feature:a", name="V1")]
        store.save_graph("test", entities_v1, [])

        # Load (should cache)
        graph1 = store.load_graph("test")
        assert graph1['entities']['feature:a']['name'] == "V1"

        # Modify file
        entities_v2 = [Feature(id="feature:a", name="V2")]
        store.save_graph("test", entities_v2, [])

        # Load again (cache should be invalidated)
        graph2 = store.load_graph("test")
        assert graph2['entities']['feature:a']['name'] == "V2"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
