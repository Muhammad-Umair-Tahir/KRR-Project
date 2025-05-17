# from typing import Dict, Set, Optional

# class PrologKB:
#     def __init__(self, path: str):
#         self.parents_of: Dict[str, Set[str]] = {}
#         self.male: Set[str] = set()
#         self.female: Set[str] = set()
#         self.birth_years: Dict[str, int] = {}
#         self.current_year: Optional[int] = None
#         self._load(path)

#     def _load(self, path: str):
#         with open(path, 'r') as f:
#             for raw in f:
#                 line = raw.strip()
#                 if not line or line.startswith('%'):
#                     continue
#                 if line.startswith('parent(') and line.endswith(').'):
#                     x,y = [tok.strip() for tok in line[len('parent('):-2].split(',')]
#                     self.parents_of.setdefault(y, set()).add(x)
#                 elif line.startswith('male(') and line.endswith(').'):
#                     self.male.add(line[len('male('):-2].strip())
#                 elif line.startswith('female(') and line.endswith(').'):
#                     self.female.add(line[len('female('):-2].strip())

#     def get_relation(self, relation: str, person: str) -> str:
#         """
#         Returns a comma-separated string of names (or '' if none).
#         Supported relations:
#           - 'mother', 'father', 'parent',
#           - 'sibling', 'brother', 'sister'
#         """
#         rel = relation.lower().strip()
#         person = person.strip()

#         # helper to join results
#         def fmt(names):
#             return ', '.join(sorted(names)) if names else ''

#         if rel == 'parent':
#             return fmt(self.parents_of.get(person, []))

#         if rel in ('mother', 'father'):
#             gender = self.female if rel == 'mother' else self.male
#             return fmt(p for p in self.parents_of.get(person, []) if p in gender)

#         if rel in ('sibling', 'brother', 'sister'):
#             sibs = set()
#             for p in self.parents_of.get(person, []):
#                 for child, pars in self.parents_of.items():
#                     if child != person and p in pars:
#                         sibs.add(child)
#             if rel == 'sibling':
#                 return fmt(sibs)
#             gender = self.male if rel == 'brother' else self.female
#             return fmt(s for s in sibs if s in gender)
        
        

#         raise ValueError(f"Relation '{relation}' not supported.")
#     def check_relation(self, relation: str, subj: str, obj: str) -> bool:
#         """
#         Check if `relation(subj, obj)` holds.
#         Supported relations: 'mother', 'father', 'parent', 'sibling', 'brother', 'sister'
#         """
#         r = relation.lower().strip()
#         subj = subj.strip()
#         obj  = obj.strip()

#         # parent(X,Y)
#         if r == 'parent':
#             return subj in self.parents_of.get(obj, ())

#         # father(X,Y)
#         if r == 'father':
#             return subj in self.parents_of.get(obj, ()) and subj in self.male

#         # mother(X,Y)
#         if r == 'mother':
#             return subj in self.parents_of.get(obj, ()) and subj in self.female

#         # siblings: share at least one parent
#         if r in ('sibling', 'brother', 'sister'):
#             # they must be different people
#             if subj == obj:
#                 return False
#             # find common parents
#             parents_subj = {p for p, c in self.parents_of.items() if c == subj}
#             parents_obj  = {p for p, c in self.parents_of.items() if c == obj}
#             common = parents_subj & parents_obj
#             if not common:
#                 return False
#             if r == 'sibling':
#                 return True
#             if r == 'brother':
#                 return subj in self.male
#             if r == 'sister':
#                 return subj in self.female

#         raise ValueError(f"Relation '{relation}' not supported.")
    
#     def get_age(self, person: str) -> Optional[int]:
#             by = self.birth_years.get(person.strip())
#             if self.current_year is None or by is None:
#                 return None
#             return self.current_year - by
        

# # Example usage
# if __name__ == '__main__':
#     kb = PrologKB('prolog/family_relationship.pl')
#     print(kb.get_relation('mother', 'umair'))    # e.g. "saman"
#     print(kb.get_relation('sibling', 'umair'))  # e.g. "alia, zainab"
#     print(kb.get_relation('father', 'arshad'))   # "" if none found



# #########################################################
# NEW UPDATED CODE V-1
# #########################################################

# from typing import Dict, Set, Optional

# class PrologKB:
#     def __init__(self, path: str):
#         self.parents_of: Dict[str, Set[str]] = {}
#         self.male: Set[str] = set()
#         self.female: Set[str] = set()
#         self.spouse_map: Dict[str, str] = {}
#         self.friends: Dict[str, Set[str]] = {}
#         self.best_friend_map: Dict[str, str] = {}
#         self.birth_years: Dict[str, int] = {}
#         self.current_year: Optional[int] = None
#         self._load(path)

#     def _load(self, path: str):
#         """
#         Parse Prolog facts: parent/2, spouse/2, friend/2, best_friend/2,
#         male/1, female/1, birth_year/2, current_year/1
#         Note: friend relations are symmetric; best_friend is directional or mutual if declared both ways.
#         """
#         with open(path, 'r') as f:
#             for raw in f:
#                 line = raw.strip().split('%')[0].strip()
#                 if not line:
#                     continue
#                 # parent(X, Y).
#                 if line.startswith('parent(') and line.endswith(').'):
#                     a, b = [tok.strip() for tok in line[len('parent('):-2].split(',', 1)]
#                     self.parents_of.setdefault(b, set()).add(a)
#                     continue
#                 # spouse(X, Y).
#                 if line.startswith('spouse(') and line.endswith(').'):
#                     x, y = [tok.strip() for tok in line[len('spouse('):-2].split(',', 1)]
#                     self.spouse_map[x] = y
#                     self.spouse_map[y] = x
#                     continue
#                 # friend(X, Y).
#                 if line.startswith('friend(') and line.endswith(').'):
#                     x, y = [tok.strip() for tok in line[len('friend('):-2].split(',', 1)]
#                     # symmetric
#                     self.friends.setdefault(x, set()).add(y)
#                     self.friends.setdefault(y, set()).add(x)
#                     continue
#                 # best_friend(X, Y).
#                 if line.startswith('best_friend(') and line.endswith(').'):
#                     x, y = [tok.strip() for tok in line[len('best_friend('):-2].split(',', 1)]
#                     self.best_friend_map[x] = y
#                     continue
#                 # male(X).
#                 if line.startswith('male(') and line.endswith(').'):
#                     name = line[len('male('):-2].strip()
#                     self.male.add(name)
#                     continue
#                 # female(X).
#                 if line.startswith('female(') and line.endswith(').'):
#                     name = line[len('female('):-2].strip()
#                     self.female.add(name)
#                     continue
#                 # birth_year(X, Y).
#                 if line.startswith('birth_year(') and line.endswith(').'):
#                     name, year = [tok.strip() for tok in line[len('birth_year('):-2].split(',', 1)]
#                     try:
#                         self.birth_years[name] = int(year)
#                     except ValueError:
#                         pass
#                     continue
#                 # current_year(Y).
#                 if line.startswith('current_year(') and line.endswith(').'):
#                     year = line[len('current_year('):-2].strip()
#                     try:
#                         self.current_year = int(year)
#                     except ValueError:
#                         pass
#                     continue
                
                
#     def get_relation(self, relation: str, person: str) -> str:
#         rel = relation.lower().strip()
#         person = person.strip()
#         def fmt(names): return ', '.join(sorted(names)) if names else ''

#         # Direct relations
#         if rel == 'parent':
#             return fmt(self.parents_of.get(person, []))
#         if rel in ('mother', 'father'):
#             gender_set = self.female if rel == 'mother' else self.male
#             return fmt(p for p in self.parents_of.get(person, []) if p in gender_set)
#         if rel in ('sibling', 'brother', 'sister'):
#             sibs = set(p for m in self.parents_of.get(person, []) for p, pars in self.parents_of.items() if p != person and m in pars)
#             if rel == 'sibling':
#                 return fmt(sibs)
#             gender_set = self.male if rel == 'brother' else self.female
#             return fmt(s for s in sibs if s in gender_set)
#         if rel == 'children':
#             return fmt(child for child, pars in self.parents_of.items() if person in pars)

#         # Grandparents
#         if rel == 'maternal_grandmother':
#             mothers = self.get_relation('mother', person).split(', ')
#             return fmt(g for mom in mothers for g in self.parents_of.get(mom, []) if g in self.female)
#         if rel == 'maternal_grandfather':
#             mothers = self.get_relation('mother', person).split(', ')
#             return fmt(g for mom in mothers for g in self.parents_of.get(mom, []) if g in self.male)
#         if rel == 'paternal_grandmother':
#             fathers = self.get_relation('father', person).split(', ')
#             return fmt(g for dad in fathers for g in self.parents_of.get(dad, []) if g in self.female)
#         if rel == 'paternal_grandfather':
#             fathers = self.get_relation('father', person).split(', ')
#             return fmt(g for dad in fathers for g in self.parents_of.get(dad, []) if g in self.male)

#         # Uncles/Aunts
#         if rel == 'maternal_uncle':
#             mothers = self.get_relation('mother', person).split(', ')
#             return fmt(u for mom in mothers for u in self.get_relation('brother', mom).split(', ') if u)
#         if rel == 'maternal_aunt':
#             mothers = self.get_relation('mother', person).split(', ')
#             return fmt(a for mom in mothers for a in self.get_relation('sister', mom).split(', ') if a)
#         if rel == 'paternal_uncle':
#             fathers = self.get_relation('father', person).split(', ')
#             return fmt(u for dad in fathers for u in self.get_relation('brother', dad).split(', ') if u)
#         if rel == 'paternal_aunt':
#             fathers = self.get_relation('father', person).split(', ')
#             return fmt(a for dad in fathers for a in self.get_relation('sister', dad).split(', ') if a)

#         # Cousins
#         if rel == 'cousin':
#             cousins = set()
#             for parent in self.parents_of.get(person, []):
#                 for sib, pars in self.parents_of.items():
#                     if sib != parent and parent in pars:
#                         cousins.update(child for child, cps in self.parents_of.items() if sib in cps)
#             return fmt(cousins)
#         if rel == 'maternal_cousin':
#             cousins = set()
#             for mom in self.get_relation('mother', person).split(', '):
#                 for sib in self.get_relation('sibling', mom).split(', '):
#                     if sib:
#                         cousins.update(child for child, cps in self.parents_of.items() if sib in cps)
#             return fmt(cousins)
#         if rel == 'paternal_cousin':
#             cousins = set()
#             for dad in self.get_relation('father', person).split(', '):
#                 for sib in self.get_relation('sibling', dad).split(', '):
#                     if sib:
#                         cousins.update(child for child, cps in self.parents_of.items() if sib in cps)
#             return fmt(cousins)

#         # Niece/Nephew
#         if rel in ('niece', 'nephew'):
#             result = set()
#             for child, pars in self.parents_of.items():
#                 if any(sib for sib in self.get_relation('sibling', person).split(', ') if sib in pars):
#                     result.add(child)
#             gender_set = self.female if rel == 'niece' else self.male
#             return fmt(p for p in result if p in gender_set)

#         # Spouses
#         if rel == 'husband':
#             spouse = self.spouse_map.get(person)
#             return fmt([spouse] if spouse and spouse in self.male else [])
#         if rel == 'wife':
#             spouse = self.spouse_map.get(person)
#             return fmt([spouse] if spouse and spouse in self.female else [])
        
#          # Friend relations
#         if rel in ('friend', 'friends'):
#                 return fmt(self.friends.get(person, set()))
#         if rel == 'best_friend':
#                 bf = self.best_friend_map.get(person)
#                 return fmt([bf] if bf else [])


#         raise ValueError(f"Relation '{relation}' not supported.")


#     def check_relation(self, relation: str, subj: str, obj: str) -> bool:
#         r = relation.lower().strip()
#         subj, obj = subj.strip(), obj.strip()
#         if r == 'parent':
#             return subj in self.parents_of.get(obj, ())
#         if r == 'father':
#             return subj in self.parents_of.get(obj, ()) and subj in self.male
#         if r == 'mother':
#             return subj in self.parents_of.get(obj, ()) and subj in self.female
#         if r in ('sibling', 'brother', 'sister'):
#             if subj == obj:
#                 return False
#             psub = {p for p, c in self.parents_of.items() if c == subj}
#             pobj = {p for p, c in self.parents_of.items() if c == obj}
#             if not psub & pobj:
#                 return False
#             if r == 'sibling':
#                 return True
#             if r == 'brother':
#                 return subj in self.male
#             if r == 'sister':
#                 return subj in self.female
#         if r in ('cousin', 'maternal_cousin', 'paternal_cousin'):
#             return obj in self.get_relation(r, subj).split(', ')
#         if r == 'husband':
#             return self.spouse_map.get(obj)==subj and subj in self.male
#         if r == 'wife':
#             return self.spouse_map.get(obj)==subj and subj in self.female
        
#         if r in ('friend', 'friends'):
#             return obj in self.friends.get(subj, set())
#         if r == 'best_friend':
#             return self.best_friend_map.get(subj) == obj
#         raise ValueError(f"Relation '{relation}' not supported.")

#     def get_age(self, person: str) -> Optional[int]:
#         """
#         Compute age = current_year - birth_year.
#         Returns None if birth_year or current_year is missing.
#         """
#         if self.current_year is None:
#             return None
#         by = self.birth_years.get(person.strip())
#         return self.current_year - by if by is not None else None

# # Example usage
# if __name__ == '__main__':
#     kb = PrologKB('prolog/family_relationship.pl')
#     print("Mother of umair:", kb.get_relation('mother', 'umair'))
#     print("Husband of razia:", kb.get_relation('husband', 'razia'))
#     print("Wife of altaf:", kb.get_relation('wife', 'altaf'))
#     print("Maternal cousins of umair:", kb.get_relation('maternal_cousin', 'umair'))
#     print("Paternal cousins of umair:", kb.get_relation('paternal_cousin', 'umair'))
#     print("All cousins of umair:", kb.get_relation('cousin', 'umair'))
#     print("Maternal grandmother of umair:", kb.get_relation('maternal_grandmother', 'umair'))
#     print("Paternal grandfather of umair:", kb.get_relation('paternal_grandfather', 'umair'))
#     print("Husband of saman:", kb.get_relation('husband', 'saman'))
#     print("Friends of umair:", kb.get_relation('friend', 'umair'))
#     print("Best friend of umair:", kb.get_relation('best_friend', 'umair'))
#     print("Check friendship umair <-> ibrahim:", kb.check_relation('friend', 'umair', 'ibrahim'))





# #########################################################
# NEW UPDATED CODE V-2 (WITH SYNONYMS)
# #########################################################

from typing import Dict, Set, Optional, Tuple, List

# Define canonical relations and their synonyms
CANONICAL_RELATIONS: Dict[str, List[str]] = {
    'parent': ['parent', 'parents'],
    'father': ['father', 'dad', 'daddy', 'abu'],
    'mother': ['mother', 'mom', 'mama', 'amma', 'ami'],
    'children': ['children', 'child'],
    'sibling': ['sibling'],
    'brother': ['brother', 'bhai'],
    'sister': ['sister', 'sis', 'behen'],
    'maternal_grandmother': ['maternal_grandmother', 'maternal grandmother', 'nani', 'nano', 'grandmother', 'grandma'],
    'maternal_grandfather': ['maternal_grandfather', 'maternal grandfather', 'nana', 'grandfather', 'grandpa'],
    'paternal_grandmother': ['paternal_grandmother', 'paternal grandmother', 'dadi', 'dado', 'grandmother', 'grandma'],
    'paternal_grandfather': ['paternal_grandfather', 'paternal grandfather', 'dada', 'grandfather', 'grandpa'],
    'maternal_uncle': ['maternal_uncle', 'maternal uncle', 'mamo', 'uncle'],
    'maternal_aunt': ['maternal_aunt', 'maternal aunt', 'mausi', 'aunt'],
    'paternal_uncle': ['paternal_uncle', 'paternal uncle', 'chacha', 'chachu', 'uncle'],
    'paternal_aunt': ['paternal_aunt', 'paternal aunt', 'chachi', 'phuphi', 'popo', 'aunt'],
    'maternal_cousin': ['maternal_cousin', 'maternal cousin'],
    'paternal_cousin': ['paternal_cousin', 'paternal cousin'],
    'cousin': ['cousin'],
    'niece': ['niece'],
    'nephew': ['nephew'],
    'husband': ['husband', 'shohar'],
    'wife': ['wife', 'begum', 'biwi'],
    'friend': ['friend', 'friends', 'frnd', 'dost'],
    'best_friends': ['best_friend', 'best friend', 'bestfriend', 'best_friends']
}

# Build reverse synonym map: synonym -> canonical key
RELATION_SYNONYMS: Dict[str, str] = {}
for canon, syns in CANONICAL_RELATIONS.items():
    for syn in syns:
        RELATION_SYNONYMS[syn.lower()] = canon

class PrologKB:
    def __init__(self, path: str):
        self.parents_of: Dict[str, Set[str]] = {}
        self.male: Set[str] = set()
        self.female: Set[str] = set()
        self.spouse_map: Dict[str, str] = {}
        self.friends: Dict[str, Set[str]] = {}
        self.best_friends: Dict[str, Set[str]] = {}
        self.birth_years: Dict[str, int] = {}
        self.current_year: Optional[int] = None
        self._load(path)

    def _load(self, path: str):
        with open(path, 'r') as f:
            for raw in f:
                line = raw.strip().split('%')[0].strip()
                if not line:
                    continue
                if line.startswith('parent(') and line.endswith(').'):
                    a, b = [tok.strip() for tok in line[7:-2].split(',', 1)]
                    self.parents_of.setdefault(b, set()).add(a)
                elif line.startswith('spouse(') and line.endswith(').'):
                    x, y = [tok.strip() for tok in line[7:-2].split(',', 1)]
                    self.spouse_map[x] = y
                    self.spouse_map[y] = x
                elif line.startswith('friend(') and line.endswith(').'):
                    x, y = [tok.strip() for tok in line[7:-2].split(',', 1)]
                    self.friends.setdefault(x, set()).add(y)
                    self.friends.setdefault(y, set()).add(x)
                elif line.startswith('best_friend(') and line.endswith(').'):
                    x, y = [tok.strip() for tok in line[12:-2].split(',', 1)]
                    self.best_friends.setdefault(x, set()).add(y)
                elif line.startswith('male(') and line.endswith(').'):
                    name = line[5:-2].strip()
                    self.male.add(name)
                elif line.startswith('female(') and line.endswith(').'):
                    name = line[7:-2].strip()
                    self.female.add(name)
                elif line.startswith('birth_year(') and line.endswith(').'):
                    name, year = [tok.strip() for tok in line[11:-2].split(',', 1)]
                    try:
                        self.birth_years[name] = int(year)
                    except ValueError:
                        pass
                elif line.startswith('current_year(') and line.endswith(').'):
                    try:
                        self.current_year = int(line[13:-2].strip())
                    except ValueError:
                        pass

    def get_relation(self, relation: str, person: str) -> str:
        key = relation.lower().strip()
        canon = RELATION_SYNONYMS.get(key)
        if not canon:
            print(f"Warning: unknown relation or synonym '{relation}'")
            return ''
        person = person.strip()
        def fmt(items: Set[str]) -> str:
            return ', '.join(sorted(items)) if items else ''
        try:
            if canon == 'parent':
                return fmt(self.parents_of.get(person, set()))
            if canon == 'father':
                return fmt({p for p in self.parents_of.get(person, set()) if p in self.male})
            if canon == 'mother':
                return fmt({p for p in self.parents_of.get(person, set()) if p in self.female})
            if canon == 'children':
                return fmt({c for c, pars in self.parents_of.items() if person in pars})
            if canon in ('sibling', 'brother', 'sister'):
                sibs = {c for m in self.parents_of.get(person, []) for c, pars in self.parents_of.items() if c != person and m in pars}
                if canon == 'sibling': return fmt(sibs)
                if canon == 'brother': return fmt({s for s in sibs if s in self.male})
                return fmt({s for s in sibs if s in self.female})
            if canon.endswith('grandmother') or canon.endswith('grandfather'):
                parent_rel = 'mother' if canon.startswith('maternal') else 'father'
                parents = self.get_relation(parent_rel, person).split(', ')
                gender_set = self.female if canon.endswith('grandmother') else self.male
                grands = {g for p in parents for g in self.parents_of.get(p, []) if g in gender_set}
                return fmt(grands)
            if canon.endswith('uncle') or canon.endswith('aunt'):
                parent_rel = 'mother' if canon.startswith('maternal') else 'father'
                rel_sib = 'brother' if canon.endswith('uncle') else 'sister'
                parents = self.get_relation(parent_rel, person).split(', ')
                unks = {u for p in parents for u in self.get_relation(rel_sib, p).split(', ') if u}
                return fmt(unks)
            if canon.endswith('cousin'):
                side = canon.split('_')[0]
                parents = self.get_relation(side, person).split(', ')
                cousins = {c for p in parents for s in self.get_relation('sibling', p).split(', ') if s for c in self.parents_of if s in self.parents_of[c]}
                return fmt(cousins)
            if canon in ('niece', 'nephew'):
                sibs = self.get_relation('sibling', person).split(', ')
                res = {c for c, pars in self.parents_of.items() if any(s in pars for s in sibs if s)}
                gender_set = self.female if canon == 'niece' else self.male
                return fmt({r for r in res if r in gender_set})
            if canon == 'husband':
                s = self.spouse_map.get(person)
                return fmt({s} if s and s in self.male else set())
            if canon == 'wife':
                s = self.spouse_map.get(person)
                return fmt({s} if s and s in self.female else set())
            if canon == 'friend':
                return fmt(self.friends.get(person, set()))
            if canon == 'best_friends':
                return fmt(self.best_friends.get(person, set()))
        except Exception as e:
            print(f"Error in get_relation for '{relation}' and '{person}': {e}")
        return ''

    def check_relation(self, relation: str, subj: str, obj: str) -> bool:
        key = relation.lower().strip()
        canon = RELATION_SYNONYMS.get(key)
        if not canon:
            print(f"Warning: unknown relation or synonym '{relation}'")
            return False
        subj, obj = subj.strip(), obj.strip()
        try:
            if canon == 'parent':
                return subj in self.parents_of.get(obj, set())
            if canon == 'father':
                return subj in self.parents_of.get(obj, set()) and subj in self.male
            if canon == 'mother':
                return subj in self.parents_of.get(obj, set()) and subj in self.female
            if canon == 'friend':
                return obj in self.friends.get(subj, set())
            if canon == 'best_friends':
                return obj in self.best_friends.get(subj, set())
            if canon == 'husband':
                return self.spouse_map.get(obj) == subj and subj in self.male
            if canon == 'wife':
                return self.spouse_map.get(obj) == subj and subj in self.female
            return obj in self.get_relation(canon, subj).split(', ')
        except Exception as e:
            print(f"Error in check_relation for '{relation}', '{subj}', '{obj}': {e}")
            return False

    def get_age(self, person: str) -> Optional[int]:
        if self.current_year is None:
            return None
        by = self.birth_years.get(person.strip())
        return self.current_year - by if by is not None else None

# Example usage
if __name__ == '__main__':
    kb = PrologKB('prolog/family_relationship.pl')
    # print("Mother of umair:", kb.get_relation('mother', 'umair'))
    # print("Husband of razia:", kb.get_relation('husband', 'razia'))
    # print("Wife of altaf:", kb.get_relation('wife', 'altaf'))
    # print("Maternal cousins of umair:", kb.get_relation('maternal_cousin', 'umair'))
    # print("Paternal cousins of umair:", kb.get_relation('paternal_cousin', 'umair'))
    # print("All cousins of umair:", kb.get_relation('cousin', 'umair'))
    print("Maternal grandmother of umair:", kb.get_relation('maternal_grandmother', 'umair'))
    print("Paternal grandfather of umair:", kb.get_relation('paternal_grandfather', 'umair'))
    print("Husband of saman:", kb.get_relation('husband', 'saman'))
    print("Friends of umair:", kb.get_relation('friend', 'umair'))
    print("Best friend of umair:", kb.get_relation('best_friend', 'umair'))
    print("Check friendship umair <-> ibrahim:", kb.check_relation('friend', 'umair', 'ibrahim'))
    print("Dad of umair:", kb.get_relation('dad', 'umair'))
    print("Grandma of zainab:", kb.get_relation('grandma', 'zainab'))
    print("Mamo of maria:", kb.get_relation('mamo', 'maria'))


