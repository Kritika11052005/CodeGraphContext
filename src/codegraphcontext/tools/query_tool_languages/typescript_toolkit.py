# src/codegraphcontext/tools/query_tool_languages/typescript_toolkit.py
class TypescriptToolkit:
    """Cypher queries for TypeScript graph data."""

    def get_cypher_query(self, query: str) -> str:
        query = query.strip()

        if query == "Repository":
            return """
                MATCH (r:Repository)-[:CONTAINS*]->(f:File)
                WHERE f.path ENDS WITH '.ts' OR f.path ENDS WITH '.mts' OR f.path ENDS WITH '.cts' OR f.path ENDS WITH '.d.ts' OR f.path ENDS WITH '.tsx'
                RETURN DISTINCT r.name AS name, r.path AS path
                ORDER BY r.path
            """

        if query == "Directory":
            return """
                MATCH (d:Directory)-[:CONTAINS*]->(f:File)
                WHERE f.path ENDS WITH '.ts' OR f.path ENDS WITH '.mts' OR f.path ENDS WITH '.cts' OR f.path ENDS WITH '.d.ts' OR f.path ENDS WITH '.tsx'
                RETURN DISTINCT d.name AS name, d.path AS path
                ORDER BY d.path
            """

        if query == "File":
            return """
                MATCH (f:File)
                WHERE f.path ENDS WITH '.ts' OR f.path ENDS WITH '.mts' OR f.path ENDS WITH '.cts' OR f.path ENDS WITH '.d.ts' OR f.path ENDS WITH '.tsx'
                RETURN f.name AS name, f.path AS path, f.relative_path AS relative_path
                ORDER BY f.path
            """

        if query == "Module":
            return """
                MATCH (f:File)-[i:IMPORTS]->(m:Module)
                WHERE f.path ENDS WITH '.ts' OR f.path ENDS WITH '.mts' OR f.path ENDS WITH '.cts' OR f.path ENDS WITH '.d.ts' OR f.path ENDS WITH '.tsx'
                RETURN f.name AS file_name,
                       m.name AS module_name,
                       i.imported_name AS imported_name,
                       i.full_import_name AS full_import_name,
                       i.line_number AS line_number
                ORDER BY f.path, i.line_number, m.name
            """

        if query == "Function":
            return """
                MATCH (fn:Function)
                WHERE fn.lang = 'typescript' OR fn.lang = 'tsx'
                RETURN fn.name AS name,
                       fn.path AS path,
                       fn.line_number AS line_number,
                       fn.end_line AS end_line,
                       fn.args AS args,
                       fn.docstring AS docstring,
                       fn.cyclomatic_complexity AS cyclomatic_complexity
                ORDER BY fn.path, fn.line_number
            """

        if query == "Class":
            return """
                MATCH (c:Class)
                WHERE c.lang = 'typescript' OR c.lang = 'tsx'
                RETURN c.name AS name,
                       c.path AS path,
                       c.line_number AS line_number,
                       c.end_line AS end_line,
                       c.bases AS bases,
                       c.docstring AS docstring
                ORDER BY c.path, c.line_number
            """

        if query == "Variable":
            return """
                MATCH (v:Variable)
                WHERE v.lang = 'typescript' OR v.lang = 'tsx'
                RETURN v.name AS name,
                       v.path AS path,
                       v.line_number AS line_number,
                       v.value AS value,
                       v.context AS context
                ORDER BY v.path, v.line_number
            """

        if query in ("Struct", "Enum", "Union", "Macro"):
            return f"""
                MATCH (n:{query})
                WHERE n.lang = 'typescript' OR n.lang = 'tsx'
                RETURN n.name AS name, n.path AS path, n.line_number AS line_number
                ORDER BY n.path, n.line_number
            """

        raise ValueError(f"Unsupported TypeScript query type: {query}")