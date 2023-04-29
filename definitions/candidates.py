from fonduer.candidates.models import candidate_subclass
from definitions.mentions.mention_subclasses import NameFull, NameAbbr, Task

NameFullAbbr = candidate_subclass("NameFullAbbr", [NameFull, NameAbbr])
NameFullTask = candidate_subclass("NameFullTask", [NameFull, Task])