from fonduer.candidates.models import candidate_subclass
from MeMoKBC.definitions.mentions.mention_subclasses import NameFull, NameAbbr, Task, AllAuthors

NameFullAbbr = candidate_subclass("NameFullAbbr", [NameFull, NameAbbr])
NameAbbrTask = candidate_subclass("NameAbbrTask", [NameAbbr, Task])
AllAuthorsTask = candidate_subclass("AllAuthorsTask", [AllAuthors, Task])