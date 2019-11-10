# Search Algorithms Reference

## Generic graph searching algorithm

From Figure 3.4: Generic graph searching algorithm.

(Poole, Mackworth. Artificial Intelligence 3rd ed., 2010. Page 79)

```
procedure Search(G, S, goal)
	Inputs
		G: graph with nodes N and arcs A
		S: set of start nodes
		goal: Boolean function of states
	Output
		path from a member of S to a node for which goal is true
		or ⊥ if there are no solution paths
	Local
		Frontier: set of paths

	Frontier <- {<s> : s ∈ S}
		while Frontier != {} do
			select and remove <s0,...,sk> from Frontier
				if goal(sk) then
					return <s0,...,sk>
			Frontier <- Frontier + {<s0,...,sk,s>:(sk,s) ∈ A}
		return ⊥
```

