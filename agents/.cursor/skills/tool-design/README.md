# Tool Design for Agents

Design tools that agents can use effectively, including when to reduce tool complexity.

## Overview

This skill covers the principles and patterns for designing tool interfaces that language model agents can discover, understand, and use correctly. Unlike traditional APIs designed for developers, agent tools must account for how models reason about intent and generate calls from natural language.

The skill includes both additive guidance (how to design good tools) and reductive guidance (when fewer tools outperform sophisticated architectures).

## Contents

```
tool-design/
├── SKILL.md                              # Main skill instructions
├── README.md                             # This file
├── references/
│   ├── best_practices.md                 # Detailed design guidelines
│   └── architectural_reduction.md        # Case study on tool minimalism
└── scripts/
    └── description_generator.py          # Tool description utilities
```

## Key Concepts

### The Consolidation Principle

If a human engineer cannot definitively say which tool should be used in a given situation, an agent cannot be expected to do better. Prefer single comprehensive tools over multiple narrow tools with overlapping functionality.

### Architectural Reduction

The consolidation principle taken to its logical extreme. Production evidence shows that reducing from 17 specialized tools to 2 primitive tools (bash command execution + SQL) achieved:

- 3.5x faster execution
- 37% fewer tokens
- 100% success rate (up from 80%)

The file system agent pattern uses standard Unix utilities (grep, cat, find, ls) instead of custom exploration tools.

### Tool Description Engineering

Tool descriptions are prompt engineering that shapes agent behavior. Effective descriptions answer:

1. What does the tool do?
2. When should it be used?
3. What inputs does it accept?
4. What does it return?

## When to Use This Skill

- Creating new tools for agent systems
- Debugging tool-related failures
- Optimizing existing tool sets
- Evaluating whether to add or remove tools
- Standardizing tool conventions

## Quick Reference

### Good Tool Design

```python
def get_customer(customer_id: str, format: str = "concise"):
    """
    Retrieve customer information by ID.
    
    Use when:
    - User asks about specific customer details
    - Need customer context for decision-making
    
    Args:
        customer_id: Format "CUST-######" (e.g., "CUST-000001")
        format: "concise" for key fields, "detailed" for complete record
    
    Returns:
        Customer object with requested fields
    
    Errors:
        NOT_FOUND: Customer ID not found
        INVALID_FORMAT: ID must match CUST-###### pattern
    """
```

### Poor Tool Design

```python
def search(query):
    """Search the database."""
    pass
```

Problems: vague name, missing parameters, no return description, no usage context, no error handling.

## Guidelines

1. Write descriptions that answer what, when, and what returns
2. Use consolidation to reduce ambiguity
3. Implement response format options for token efficiency
4. Design error messages for agent recovery
5. Question whether each tool enables or constrains the model
6. Prefer primitive, general-purpose tools over specialized wrappers
7. Invest in documentation quality over tooling sophistication
8. Build minimal architectures that benefit from model improvements

## Related Skills

- `context-fundamentals` - How tools interact with context
- `multi-agent-patterns` - Specialized tools per agent
- `evaluation` - Evaluating tool effectiveness

## References

- [SKILL.md](./SKILL.md) - Full skill instructions
- [Best Practices](./references/best_practices.md) - Detailed guidelines
- [Architectural Reduction Case Study](./references/architectural_reduction.md) - Production evidence

## Version

- **Created**: 2025-12-20
- **Last Updated**: 2025-12-23
- **Version**: 1.1.0

