# Autonomous Legacy-to-Python Modernization & Testing Agent
Constrained reference modernization agent with stateful extract → translate → AST-check → test → Docker-validation → reflection/repair architecture, designed for LangGraph orchestration. It preserves decimal literals with `Decimal` and checks translated branch structure.

This is not a general Java transpiler. AST validation checks selected invariants; it does not prove zero semantic loss for arbitrary Java. Docker execution is an architecture boundary and requires Docker at runtime.
