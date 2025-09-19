graph [
  directed 1
  title "demo graph"
  node [
    id 0
    label "A1"
    x 100
    y 300
    cluster "A"
  ]
  node [
    id 1
    label "A2"
    x 200
    y 300
    cluster "A"
  ]
  node [
    id 2
    label "A3"
    x 150
    y 200
    cluster "A"
  ]
  node [
    id 3
    label "B1"
    x 300
    y 300
    cluster "B"
  ]
  node [
    id 4
    label "B2"
    x 400
    y 300
    cluster "B"
  ]
  node [
    id 5
    label "B3"
    x 350
    y 200
    cluster "B"
  ]
  node [
    id 6
    label "XX"
    x 250
    y 100
    cluster "X"
  ]
  edge [
    source 0
    target 1
    label "aa"
  ]
  edge [
    source 1
    target 2
    label "aa"
  ]
  edge [
    source 1
    target 3
    label "ab"
  ]
  edge [
    source 2
    target 0
    label "aa"
  ]
  edge [
    source 2
    target 5
    label "ab"
  ]
  edge [
    source 3
    target 4
    label "bb"
  ]
  edge [
    source 3
    target 1
    label "ab"
  ]
  edge [
    source 4
    target 5
    label "bb"
  ]
  edge [
    source 5
    target 3
    label "bb"
  ]
  edge [
    source 5
    target 2
    label "ab"
  ]
  edge [
    source 6
    target 2
    label "xa"
    color "(0,0,255)"
  ]
  edge [
    source 6
    target 5
    label "xb"
    color "(0,255,0)"
  ]
  edge [
    source 6
    target 6
    label "self"
    color "(255,0,0)"
  ]
]
