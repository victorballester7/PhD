function getMeshSessionFiles {
    # Identify the mesh file (first one matching mesh*.xml and does not contain "old")
    mesh_file=$(ls mesh*.xml 2>/dev/null | grep -v "old" | head -n 1)

    # Identify the session file (any other .xml file that is not the mesh file and does not contain "old")
    session_file=$(ls *.xml 2>/dev/null | grep -v "old" | grep -v "^$mesh_file$" | head -n 1)
}

