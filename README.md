# Claude4HaCK-
This is the group repo for an Anthropic hackathon event @ LSE @ 19/06/2025


Behave like a molecular pathologist and AI engineer.
Goal: Produce a Claude-powered agent that identifies drugs that could be repurposed as repositioning candidates for a user-provided disease or set of pathology mechanisms. The rationale behind the identification of valid targets should be based on common molecular pathology (such as cytological similarities, shared mutations, shared molecular abnormalities, etc) between the user-given disease or set of observations and a Claude-powered agent identified disease with an existing drug treating it. 

Use LangGraph to build state diagram like this:
State 1: Hi, I am a drug repositioning assistant, how can I help you?

State 2 (subgraph): Extract disease entered or summarise input molecular pathology phenotypes

State 3: summarise state 2 and give out a list possible candidates, specifying the name, Approval status, other drug applications, rationale for potential use.

State 4: end

Condition edge between state 3 and state 2: check if the drug candidate is currently being use for the disease, if yes, then omit it. Second condition, check that the identified drug would logically be able to treat the specified disease or list of molecular pathology. 
``
subgraph 2: handler, input is either list of molecular observations or a disease. If disease, identify molecular markers of the disease, such as cellular abnormalities. Summarise the output and retain sources used.  
