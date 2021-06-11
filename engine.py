from enum import Enum


class Operators(Enum):
  eq = "=="
  neq = "!="
  lt = "<"
  gt = ">"
  leq = "<="
  geq = ">="
  isin = "in"
  notin = "not in"


class Criteria:
  def __init__(self, scope: str, prop: str, val, op: Operators = Operators.eq):
    self.scope = scope
    self.prop = prop
    self.val = val
    self.op = op

  def __str__(self):
    prop, *addtl = self.prop.split('.')
    if addtl:
      return f"{{obj}}.get('{prop}').{'.'.join(addtl)} {self.op.value} {self.val}"
    return f"{{obj}}.get('{prop}') {self.op.value} {self.val}"

  def evaluate(self, **kwargs):
    eval_str = self.__str__().format(obj=kwargs.get(self.scope))
    return {'str': eval_str, 'result': eval(eval_str)}


class CriteriaSet:
  def __init__(self, set_type: str = 'all', criteria: list = None):
    self.set_type = set_type
    self.criteria = criteria or []

  def __str__(self):
    join_str = 'and' if self.set_type == 'all' else 'or'
    join_str = f" {join_str} "
    return join_str.join([str(c) for c in self.criteria])

  def evaluate(self, **kwargs):
    final_set = [c.evaluate(**kwargs) for c in self.criteria]
    fn = all if self.set_type == 'all' else any
    return {'result': fn([f.get('result') for f in final_set]), 'individual': final_set}
  

class Rule:
  def __init__(self,
               rule_id: int,
               rule_name: str = None,
               criteria: list = None,
               actions: list = None,
               enabled: bool = False,
               end_processing: bool = False,
               match_all: bool = True):
    self.ID = rule_id
    self.name = rule_name
    self.criteria = criteria or []
    self.actions = actions or []
    self.enabled = enabled
    self.end_processing = end_processing
    self.match_all = match_all
  
  def __str__(self):
    if self.name:
      return f"Rule ID {self.ID}: {self.name}"
    return f"Rule ID {self.ID}"

  def evaluate(self, **kwargs):
    preprocess_results = [c.evaluate(**kwargs) for c in self.criteria]
    overall_results = [c.get('result') for c in preprocess_results]
    fn = all if self.match_all else any
    final = fn(overall_results)
    return {'final': final, 'individual': preprocess_results}
  
  def apply(self, **kwargs):
    result = self.evaluate(**kwargs)
    if result.get('final'):
      for action in self.actions:
        action(**kwargs)
    return result
    

def example():

  drop_00_ts = Rule(rule_id=107,
                    rule_name="Drop 00:00 TimeStamps",
                    criteria=[CriteriaSet(
                      set_type='all',
                      criteria=[
                        Criteria('item', 'scheduled_time.time().hour', 0, Operators.eq)
                        Criteria('item', 'scheduled_time.time().minute', 0, Operators.eq)
                      ])],
                    actions=[
                      lambda i: i.drop_from_queue(),
                      lambda i: print(f"Dropped item {i} from queue!")
                    ],
                    enabled=True,
                    end_processing=True,
                    match_all=True)
    
  
    
