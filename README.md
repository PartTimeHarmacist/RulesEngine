# RulesEngine

Proof of Concept for a Rules Engine written in Python.

Ideally, this would be incorporated into a project that necessarily needs the ability to modify multiple rules on an ad-hoc basis, without having to recode them each time.

Example of a main loop:
```py
for i in item_queue:
  for rule in rules:
    result = rule.apply(i=i)
    if result.get('final') == False and rule.end_processing:
      break
```

Based on the above example, rules could be loaded from an external source on script/program load, and applied dynamically.  Given there is a separate process to allow for creation/modification of rules, this would separate the end user from needing to code at all; while allowing for a standard that the developer can then base future code off of.
