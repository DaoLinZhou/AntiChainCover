# AntiChainCover

```shell
python3 POSET.py --file=[filepath] [--show_steps]
```
* `--file` is the POSET description file
* `--show_steps` will show how to select anti chain cover step by step

Examples:
```shell
python .\POSET.py --file=".\poset\simple_1.json" --show_steps
python .\POSET.py --file=".\poset\simple_1.json"
```

I use json file to describe graph

`nodes` means how many nodes in the poset, the nodes will be labelled in [0...nodes-1]

`edges` describe the edges from source node to target node, the first element in the array is the source node, and reset elements are target nodes.


For example:
```json
{
  "nodes": 4,
  "edges": [
    [0, 1, 2, 3],
    [1, 2],
    [2, 3]
  ]
}
```
This sample json will create 4 nodes: node 0, 1, 2, 3

There are 5 edges in this POSET
```
[0, 1, 2, 3] means those 3 edges in the POSET
0 -> 1
0 -> 2
0 -> 3

[1, 2] means
1 -> 2

[2, 3] means
2 -> 3
```

