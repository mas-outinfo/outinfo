# Demo file for the GML (Graph Modeling Language) format
# Note : whitespaces and newlines are not meaningful

# 'graph' block = global properties + list of nodes/edges
graph [
  title "demo graph"
  directed 1

# 'node' block = all properties for one node
node [id 1 label "A1" x 100 y 300 cluster "A"]
  node  [ id 2 label "A2" x 200 y 300 cluster "A" ]
node [ id  3   label  "A3"   x  150   y  200   cluster  "A" ]

# 'edge' block = all properties for one edge
edge [source 1 target 2 label "aa"]
edge [source 2 target 3 label "aa"]
edge [source 3 target 1 label "aa"]

node [id 4 label "B1" x 300 y 300 cluster "B"]
node [id 5 label "B2" x 400 y 300 cluster "B"]
node [id 6 label "B3" x 350 y 200 cluster "B"]
edge [source 4 target 5 label "bb"]
edge [source 5 target 6 label "bb"]
edge [source 6 target 4 label "bb"]
edge [source 2 target 4 label "ab"]
edge [source 4 target 2 label "ab"]
edge [source 3 target 6 label "ab"]
edge [source 6 target 3 label "ab"]

node [
  id 7 label "XX"
  x 250 y 100
  cluster "X" ]
edge [
  source 7 target 3
  label "xa" color "(0,0,255)" ]
edge [
  source 7 target 6
  label "xb" color "(0,255,0)" ]
edge [
  source 7 target 7
  label "self" color "(255,0,0)" ]
]